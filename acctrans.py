import sqlalchemy as db
import user_input as uin
from db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation
from datetime import date
from uuid import UUID

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
    #TODO: Change userRole to customer boolean
    userRole = 'Teller'
    uuidFrom = uuidTo = ''
    if userRole == 'Customer':
        uuidFrom = UUID('073ad8a7-6527-4e0a-A748-cd3d7a66c193', version=4) #TODO: Make this based on user who executes cmd
        uuidTo = uin.getUUID('Enter the UUID of the person you would like to transfer the money to: ')
    elif userRole == 'Teller' or userRole == 'Manager':
        uuidFrom = uin.getUUID('Enter the UUID of the person you would like to transfer the money from: ')
        uuidTo = uin.getUUID('Enter the UUID of the person you would like to transfer the money to: ')
    else:
        print ('Insufficient permissions')
        #TODO: Make it so it doesn't execute the rest of the code
    amountToTransfer = uin.getDecimal('Enter how much you want to transfer: ')
    currentDate = date.today()
    descInput = input("Enter A description for the Transaction: ")
    currentBalFrom = dbexe.query_to_value(f"""
        SELECT balance 
        FROM account 
        WHERE accountnumber = '{uuidFrom}'
    """)    
    currentBalTo = dbexe.query_to_value(f"""
        SELECT balance 
        FROM account 
        WHERE accountnumber = '{uuidTo}'
    """)
    newBalFrom = currentBalFrom - amountToTransfer
    newBalTo = currentBalTo + amountToTransfer
    overdraftType = dbexe.query_to_value(f"""
        SELECT overdrafttype 
        FROM account 
        WHERE accountnumber = '{uuidFrom}' 
    """)
    transferType = ''
    if newBalFrom < 0 and overdraftType == 'reject':
        print('Insufficient funds')
    else:
        
        # SELECT DISTINCT here
        
        fromBranch = dbexe.query_to_value(f"""
            SELECT branch 
            FROM customer JOIN holds on customer.ssn = holds.ssn 
            WHERE accountnumber = '{uuidFrom}' 
        """)
        toBranch = dbexe.query_to_value(f"""
            SELECT branch 
            FROM customer JOIN holds on customer.ssn = holds.ssn 
            WHERE accountnumber = '{uuidTo}' 
        """)
        if fromBranch == toBranch:
            transferType = 'transfer'
        else:
            transferType = 'external transfer'

        
        dbexe.run_query(f"""
            UPDATE account 
            SET balance = '{newBalFrom}'
            WHERE accountnumber = '{uuidFrom}'
        """)
        dbexe.run_query(f"""
            UPDATE account
            SET balance = '{newBalTo}' 
            WHERE accountnumber = '{uuidTo}' 
        """)
        dbexe.run_query(f"""
            INSERT INTO transaction (transactiontype, amount, transactiondate, 
                description, accountfrom, accountto, startbalance)
            VALUES('{transferType}', '{amountToTransfer}', '{currentDate}', 
                '{descInput}', '{uuidFrom}', '{uuidTo}', '{newBalTo}')
        """)
        dbexe.run_query(f"""
            INSERT INTO transaction (transactiontype, amount, transactiondate, 
                description, accountfrom, accountto, startbalance)
            VALUES('{transferType}', '-{amountToTransfer}', '{currentDate}', 
                '{descInput}', '{uuidTo}', '{uuidFrom}', '{newBalFrom}')
        """)
        
        dbexe.commit()
    
