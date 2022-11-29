
from decimal import Decimal
import sqlalchemy as db # type: ignore

from db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation

"""added code to reset all SQL tables/data to empty"""
"""changed db.create_engine() to include future=True"""


# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://postgres:{}@localhost:5432/Banking'.format("password"),
    future=True
)

metadata = db.MetaData()

 
# INIT TABLES TO EMPTY
    
with engine.connect() as atomic_connection:
    
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)
    
    with open("reset_all_ddl.sql") as ddl_file:
        dbexe.run_query(ddl_file.read())
        
    # commit to end atomic and save changes
    # without this, changes will be rolled back
    dbexe.commit()
 
 
 
# QUERY STUFF

with engine.connect() as atomic_connection:
    
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)

    # print relation
    pprint_relation(dbexe, "Branch")

    # print relation
    pprint_relation(dbexe, "Account")

    # print relation
    pprint_relation(dbexe, "Customer")


    # turn query into dataframe
    df = dbexe.query_to_df(f"""
        SELECT address, waiveFeeMin
        FROM Branch
    """)
    # print dataframe
    pprint_df(df)


with engine.connect() as atomic_connection:
    
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)
    
    # run query that CHANGES DATABASE
    
    dbexe.run_query(f"""
        INSERT INTO Account (balance, hasMonthlyFee)
        VALUES (400.0, True)
    """)
    
    # commit to end atomic and save changes
    # without this, changes will be rolled back
    dbexe.commit()