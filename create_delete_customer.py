import pandas as pd # type: ignore 
import decimal
from decimal import Decimal
from uuid import UUID
from db_execution import DBExecuter

from pretty_printing import pprint_df

from user_input import (
    getMultipleChoice,
    getText,
    getYorN
)

from branch_query_functions import all_branches

# set precision of decimal values
decimal.getcontext().prec = 4

def insert_customer(
    engine,
    ssn: str,
    name: str,
    address: str,
    branch: UUID,
):
  """Creates a new customer of the given branch."""
  # run queries as atomic unit
  with engine.connect() as atomic_connection:
    dbexe = DBExecuter(atomic_connection)
    dbexe.run_query(f"""
        INSERT INTO Customer (ssn, name, address, branch)
        VALUES ('{ssn}', '{name}', {address}, {branch})
    """)
    
    dbexe.commit()
    
def remove_customer(
    engine,
    ssn: str
):
    """Deletes customer given SSN."""

    with engine.connect() as atomic_connection:      
        dbexe = DBExecuter(atomic_connection)

        # delete matching customer
        dbexe.run_query(f"""
            DELETE FROM Customer
            WHERE ssn = '{ssn}'
        """)
        
        dbexe.commit()




def create_customer(
    engine,
    _: str,
    __: bool
):
    print("\n~ Create a customer ~")

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
      
    ssn = getText("\nWhat is the Customers SSN? ")
    name = getText("\nWhat is the Customers full name? ")
    address = getText("\nWhat is the Customers address? ")

    insert_customer(engine, ssn, name, address, branch)
      
    print("\nCustomer created successfully.")
        
def delete_customer(
    engine,
    _: str,
    __: bool
):
    
    ssn = input("\nCustomer's ssn: ").strip()
    
    remove_customer(engine, ssn)
    print("\nCustomer deleted successfully.")
    