import pandas as pd # type: ignore 
import decimal
from decimal import Decimal
from uuid import UUID
from helpers.postgres.db_execution import DBExecuter

from pretty_printing import pprint_df

from user_input import (
    getMultipleChoice,
    getDecimal,
    getText,
)

from branch_query_functions import all_branches

# set precision of decimal values
decimal.getcontext().prec = 4

def insert_employee(
    engine,
    ssn: str,
    address: str,
    emp_name: str,
    salary: Decimal,
    emp_role: str,
    branch: UUID,
):
  """Creates a new employee for the given branch."""
  # run queries as atomic unit
  with engine.connect() as atomic_connection:
    dbexe = DBExecuter(atomic_connection)
    dbexe.run_query(f"""
        INSERT INTO Employee (ssn, emp_name, address, salary, emp_role, branch)
        VALUES ('{ssn}', '{emp_name}', '{address}', {str(salary)}, '{emp_role}', '{branch}')
    """)
    
    dbexe.commit()
    
def remove_employee(
    engine,
    ssn: str,
):
  """Deletes an employee given their SSN."""

  with engine.connect() as atomic_connection:      
    dbexe = DBExecuter(atomic_connection)

    # delete matching account
    dbexe.run_query(f"""
      DELETE FROM Employee
      WHERE ssn = '{ssn}'
    """)
    
    dbexe.commit()

def create_employee(
    engine,
):
  print("\n~ Create an employee ~")

  # let user choose a branch to create account for
  branches: pd.DataFrame = all_branches(engine)

  # show user the branches
  pprint_df(branches)
      
  if (branches.empty):
    print("No branches found! Please create one.")
    return

  branch_index = getMultipleChoice(
    "\nChoose a branch: ", 
    tuple(b for b in branches["address"])
  )

  branch = branches["branchid"][branch_index]

  # let user choose customers from that branch to create account for
  customer_choices = pd.DataFrame()
      
  ssn = getText("What is the employees SSN? ");
  emp_name = getText("What is the employees full name? ");
  address = getText("What is the employees address? ");
  salary = getDecimal("What is the employees salary? ");
  emp_role = getText("What is the employees role? (teller, loan specialist, manager) ");

  insert_employee(engine, ssn, address, emp_name, salary, emp_role, branch)
        

def delete_employee(
    engine,
    ssn: str,
):
  remove_employee(engine, ssn)
  print("\Employee deleted successfully.")