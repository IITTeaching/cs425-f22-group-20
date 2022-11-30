import sqlalchemy as db
import user_input as uin
from db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation
from datetime import date
import pandas as pd

# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://postgres:test@localhost:5432/cs425_final',
    future=True
)

metadata = db.MetaData()

# QUERIES


with engine.connect() as atomic_connection: # TRANSFER QUERY
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)

    #TEMPORARY, only will work between people with these specific UUIDs (CHANGE LATER)
    #VAR userRole, determines what uuids are selected based on role (May be temporary/May need to tweak)
    userRole = 'Customer'
    uuidFrom = uuidTo = ''
    if userRole == 'Customer':
        uuidFrom = '073ad8a7-6527-4e0a-9748-cd3d7a66c193' #TODO: Make this based on user who executes cmd
        uuidTo = uin.getUUID('Enter the UUID of the person you would like to transfer the money to: ')
    elif userRole == 'Teller' or userRole == 'Manager':
        uuidFrom = uin.getUUID('Enter the UUID of the person you would like to transfer the money from: ')
        uuidTo = uin.getUUID('Enter the UUID of the person you would like to transfer the money to: ')
    else:
        print ('Insufficient permissions')
        #TODO: Make it so it doesn't execute the rest of the code
    
    transferType = ''

    amountToTransfer = uin.getDecimal('Enter how much you want to transfer: ')
    currentBalFrom = dbexe.query_to_value(f"""SELECT balance FROM account WHERE accountnumber = :uuid """, **{'uuid': uuidFrom})    
    currentBalTo = dbexe.query_to_value(f"""SELECT balance FROM account WHERE accountnumber = :uuid """, **{'uuid': uuidTo})
    newBalFrom = currentBalFrom - amountToTransfer
    overdraftType = dbexe.query_to_value(f"""SELECT overdrafttype FROM account WHERE accountnumber = :uuid """, **{'uuid': uuidFrom})
    if newBalFrom >= 0 and overdraftType != 'reject':
        print('Insufficient funds')
    else:
        fromBranch = dbexe.query_to_value(f"""SELECT branch FROM customer JOIN holds on customer.ssn = holds.ssn WHERE accountnumber = :uuid """, **{'uuid': uuidFrom})
        toBranch = dbexe.query_to_value(f"""SELECT branch FROM customer JOIN holds on customer.ssn = holds.ssn WHERE accountnumber = :uuid """, **{'uuid': uuidTo})
        if fromBranch == toBranch:
            transferType = 'transfer'
        else:
            transferType = 'external transfer'

        newBalTo = currentBalTo + amountToTransfer
        currentDate = date.today()
        descInput = input("Enter A description for the Transaction: ")
        dbexe.run_query(f"""UPDATE account SET balance = :bal WHERE accountnumber = :fromuuid """, **{'bal': newBalFrom, 'fromuuid': uuidFrom})
        dbexe.run_query(f"""UPDATE account SET balance = :bal WHERE accountnumber = :touuid """, **{'bal': newBalTo, 'touuid': uuidTo})
        dbexe.run_query(f"""INSERT INTO transaction
        (transactiontype, amount, transactiondate, description, accountfrom, accountto, startbalance)
        VALUES(:type, :amt, :date, :desc, :fromuuid, :touuid, :bal)
        """, **{'type': transferType, 'amt': -amountToTransfer, 'date': currentDate, 'desc': descInput,
                'fromuuid': uuidFrom, 'touuid': uuidTo, 'bal': currentBalTo})
        dbexe.run_query(f"""INSERT INTO transaction
        (transactiontype, amount, transactiondate, description, accountfrom, accountto, startbalance)
        VALUES(:type, :amt, :date, :desc, :fromuuid, :touuid, :bal)
        """, **{'type': transferType, 'amt': amountToTransfer, 'date': currentDate, 'desc': descInput,
                'fromuuid': uuidFrom, 'touuid': uuidTo, 'bal': currentBalTo})
        dbexe.commit()
    
