import sqlalchemy as db
from helpers.create_insert_delete.create_delete_account import insert_account
from helpers.create_insert_delete.create_delete_branch import create_branch
from helpers.create_insert_delete.create_delete_customer import create_customer
from helpers.create_insert_delete.create_insert_employee import create_employee
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

create_customer(engine)

# QUERIES

with engine.connect() as atomic_connection: # TRANSFER QUERY
  # make a database executer for this atomic block of SQL queries
  dbexe = DBExecuter(atomic_connection)

  # TODO get from current user
  userRole = 'manager'
  managerUUID = '123'
  if userRole == 'manager':
    print ('Authenticated')
    accounts = dbexe.query_to_value(f"""
        SELECT * 
        FROM Holds
    """)
    accounts
  else:
    print ('Insufficient permissions')
    dbexe.commit()



  
    
