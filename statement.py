import sqlalchemy as db
import user_input as uin
from helpers.postgres.db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation
from datetime import date
import calendar as cal
import config as config


# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(config.database_username, config.database_password, config.database_name),
    future=True
)

metadata = db.MetaData()

# QUERIES

with engine.connect() as atomic_connection: # TRANSFER QUERY
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)

    #TODO: Make UUID Based on user
    userRole = 'Customer'
    userUUID = ''
    if userRole == 'Customer':
        userUUID = '073ad8a7-6527-4e0a-9748-cd3d7a66c193'
    elif userRole == 'Manager':
        userUUID = uin.getUUID('Please enter the user\'s UUID')
    else:
        #TODO: Make it stop executing everything else
        print('Insufficient Permissions')
    #TODO: Determine whether to end if month is invalid or to keep continuing until they enter a valid month
    stmtTime = uin.getYearMonth('Which month do you want to view your statement on?')
    stmtYear = stmtTime[0]
    stmtMonth = stmtTime[1]
    monthString = cal.month_name[stmtMonth]
    transactions = dbexe.query_to_df(f"""
        SELECT * 
        FROM transaction 
        WHERE accountto = '{userUUID}' AND 
            date_part('year', transactiondate) = '{stmtYear}' AND 
            date_part('month', transactiondate) = '{stmtMonth}' 
        ORDER BY transactiondate 
    """)
    currentValue = dbexe.query_to_value(f"""
        SELECT startbalance 
        FROM transaction 
        WHERE accountto = '{userUUID}' 
        ORDER BY transactiondate DESC LIMIT 1
    """)
    if stmtYear == date.today().year and stmtMonth == date.today().month:
        pprint_df(transactions)
        print('Full Statement is not available until the month ends')
    elif stmtYear > date.today().year or (stmtYear == date.today().year and stmtMonth > date.today().month): 
        print('You cannot view a statement in the future')
    elif transactions.empty:
        print('No Transactions occured on the specified month')
    else:
        pprint_df(transactions)
        print(f"""Full Statement for {monthString} {stmtYear} """)
        print(f"""Current Account Balance is {currentValue} """)
            
        
            
        
            

