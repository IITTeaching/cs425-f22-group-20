
from decimal import Decimal
import sqlalchemy as db # type: ignore

import db_execution
from pretty_printing import pprint_df, pprint_relation

# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://postgres:PASSWORDHERE@localhost:5432/Banking'
)

connection = engine.connect()
metadata = db.MetaData()

# make a database executer
dbexe = db_execution.DBExecuter(metadata, engine, connection)






# QUERY STUFF

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


# # run query that CHANGES DATABASE
#
# dbexe.run_query(f"""
#     INSERT INTO Account (balance, hasMonthlyFee)
#     VALUES (400.0, True)
# """)