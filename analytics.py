from decimal import Decimal
from db_execution import DBExecuter
import config as config

def get_total_customers(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False, 
) -> Decimal:
  # This function gets the total amount of customers in a manager branch

  if user_is_customer:
    return

  with engine.connect() as atomic_connection:
      dbexe = DBExecuter(atomic_connection)

      branchID = dbexe.query_to_value(f"""
        SELECT branch FROM Employee WHERE ssn = '{manager_ssn}'
      """)

      return dbexe.query_to_value(f"""
        SELECT COUNT(*) FROM Customer WHERE branch = '{branchID}'
      """)

def get_total_money(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False, 
) -> Decimal:
  # This function gets the total amount of $ in a managers branch

  # sanity check
  if user_is_customer:
    return

  with engine.connect() as atomic_connection:
      dbexe = DBExecuter(atomic_connection)

      accounts = dbexe.query_to_df(f"""
        SELECT * 
        FROM Holds
      """)

      total_money = 0

      for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
        branchID = dbexe.query_to_value(f"""
          SELECT branch FROM Employee WHERE ssn = '{manager_ssn}'
        """)
        
        customerBranchID = dbexe.query_to_value(f"""
          SELECT branch FROM Customer WHERE ssn = '{ssn}'
        """)

        if branchID == customerBranchID:
          total_money = total_money + dbexe.query_to_value(f"""
            SELECT balance FROM Account WHERE accountNumber = '{accountnumber}'
          """)

      return total_money

def get_total_employee_salary_(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False, 
) -> Decimal:
  # This function gets the total amount of $ in a managers branch

  # sanity check
  if user_is_customer:
    return

  with engine.connect() as atomic_connection:
      dbexe = DBExecuter(atomic_connection)

      branchID = dbexe.query_to_value(f"""
        SELECT branch FROM Employee WHERE ssn = '{manager_ssn}'
      """)

      return dbexe.query_to_value(f"""
        SELECT SUM(salary) FROM Employee WHERE branch = '{branchID}'
      """)
    
def get_total_customers_analytics(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    print("There are currently {} customers across your managed branch.".format(get_total_customers(engine)))
  
def get_total_money_held_by_accounts(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
  
    print("There is currently ${} held by accounts in your managed branch.".format(get_total_money(engine)))

def get_total_salaries_of_employees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:

    print("There is currently ${} being paid to each employee of your managed branch.".format(get_total_employee_salary_(engine, manager_ssn, user_is_customer)))