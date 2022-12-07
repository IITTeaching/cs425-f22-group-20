from decimal import Decimal
from db_execution import DBExecuter
from uuid import UUID
import config as config

def get_total_customers(
  engine
) -> Decimal:

    with engine.connect() as atomic_connection:

        dbexe = DBExecuter(atomic_connection)

        return dbexe.query_to_value(f"""
          SELECT COUNT(*) FROM Customer
        """)

def get_total_money(
  engine,
) -> Decimal:

    with engine.connect() as atomic_connection:

        dbexe = DBExecuter(atomic_connection)

        return dbexe.query_to_value(f"""
          SELECT SUM(balance) FROM Account
        """)
    
def get_total_customers_analytics(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    print("There are currently {} customers across all branches!".format(get_total_customers(engine)))
  
def get_total_money_held_by_accounts(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
  
    print("There is currently ${} held by accounts in all branches!".format(get_total_money(engine)))