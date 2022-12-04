import sqlalchemy as db
import pandas as pd
from create_delete_account import create_account, insert_account
from create_delete_branch import create_branch
from create_delete_customer import create_customer
from create_insert_employee import create_employee
import user_input as uin
from db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation
from datetime import date
from uuid import UUID
import config as config

# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(config.database_username, config.database_password, config.database_name),
    future=True
)

metadata = db.MetaData()

# QUERIES

def applyOverdraft(dbexe: DBExecuter, accounts: pd.DataFrame):
  for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
    balance = dbexe.query_to_value(f"""
      SELECT balance 
      FROM Account 
      WHERE accountnumber = '{accountnumber}'
    """)

    overdraftType = dbexe.query_to_value(f"""
      SELECT overdraftType 
      FROM Account 
      WHERE accountnumber = '{accountnumber}'
    """)

    if (overdraftType == 'charge'):
      branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Customer 
        WHERE ssn = '{ssn}'
      """)

      overdraftFee = dbexe.query_to_value(f"""
        SELECT overdraftFee 
        FROM Branch 
        WHERE branchID = '{branchID}'
      """)

      if balance < 0:
        balance = dbexe.run_query(f"""
        UPDATE Account 
        SET balance = {balance - overdraftFee} 
        WHERE accountnumber = '{accountnumber}'
      """)

def applyInterest(dbexe: DBExecuter, accounts: pd.DataFrame):
  for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
    interestRate = dbexe.query_to_value(f"""
      SELECT interestRate 
      FROM Account 
      WHERE accountNumber = '{accountnumber}'
    """)

    balance = dbexe.query_to_value(f"""
      SELECT balance 
      FROM account 
      WHERE accountnumber = '{accountnumber}'
    """)

    dbexe.run_query(f"""
      UPDATE Account 
      SET balance = {balance + (balance * interestRate)} 
      WHERE accountnumber = '{accountnumber}'
    """)

def applyMonthlyFee(dbexe: DBExecuter, accounts: pd.DataFrame):
  for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
    hasMonthlyFee = dbexe.query_to_value(f"""
      SELECT hasMonthlyFee 
      FROM Account 
      WHERE accountNumber = '{accountnumber}'
    """)
    
    if hasMonthlyFee:
      balance = dbexe.query_to_value(f"""
        SELECT balance 
        FROM account 
        WHERE accountnumber = '{accountnumber}'
      """)

      branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Customer 
        WHERE ssn = '{ssn}'
      """)

      waiveFeeMin = dbexe.query_to_value(f"""
        SELECT waiveFeeMin 
        FROM Branch 
        WHERE branchID = '{branchID}'
      """)

      monthlyFee = dbexe.query_to_value(f"""
        SELECT monthlyFee 
        FROM Branch 
        WHERE branchID = '{branchID}'
      """)

      if balance < waiveFeeMin:
        dbexe.run_query(f"""
          UPDATE Account
          SET balance = {balance - monthlyFee} 
          WHERE accountnumber = '{accountnumber}'
        """)
    

    #dbexe.run_query(f"""
    #  UPDATE Account 
    #  SET balance = {balance - monthlyFee} 
    #  WHERE accountnumber = '{accountnumber}'
    #""")

with engine.connect() as atomic_connection: # TRANSFER QUERY
  # make a database executer for this atomic block of SQL queries
  dbexe = DBExecuter(atomic_connection)

  # TODO get uuid from current manager (if they're a manager)
  #create_employee()
  userRole = 'manager'
  if userRole == 'manager':
    print ('Authenticated')
    # TODO get based on managers branch
    accounts = dbexe.query_to_df(f"""
      SELECT * 
      FROM Holds
    """)
    applyOverdraft(dbexe, accounts)
    applyInterest(dbexe, accounts)
    applyMonthlyFee(dbexe, accounts)
    dbexe.commit()
  else:
    print ('Insufficient permissions')
    dbexe.commit()



  
    
