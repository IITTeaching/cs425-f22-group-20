from db_execution import DBExecuter
from uuid import UUID
import config as config

def get_total_customers(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False,
) -> None:

  if (user_is_customer):
    return

  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    return dbexe.query_to_value(f"""
      SELECT COUNT(*) FROM Customer
    """)

def get_total_money(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False,
) -> None:

  if (user_is_customer):
    return

  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    return dbexe.query_to_value(f"""
      SELECT SUM(balance) FROM Account
    """)