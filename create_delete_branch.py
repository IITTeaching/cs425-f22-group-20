import pandas as pd # type: ignore 
import decimal
from decimal import Decimal
from uuid import UUID
from db_execution import DBExecuter

from pretty_printing import pprint_df

from user_input import (
    getMultipleChoice,
    getDecimal,
    getText,
)

from branch_query_functions import all_branches

# set precision of decimal values
decimal.getcontext().prec = 4

def insert_branch(
    engine,
    address: str,
    overdraftFee: Decimal = Decimal("0"),
    monthlyFee: Decimal = Decimal("0"),
    waiveFeeMin: Decimal = Decimal("0"), 
) -> UUID:
  """Creates a new branch."""
  # run queries as atomic unit
  with engine.connect() as atomic_connection:
    dbexe = DBExecuter(atomic_connection)
    dbexe.run_query(f"""
        INSERT INTO Branch (address, overdraftFee, monthlyFee, waiveFeeMin)
        VALUES ('{address}', '{str(overdraftFee)}', {str(monthlyFee)}, {str(waiveFeeMin)})
    """)
    
    dbexe.commit()
    
def remove_branch(
    engine,
    uuid: UUID,
):
  """Deletes a branch with a given UUID."""

  with engine.connect() as atomic_connection:      
    dbexe = DBExecuter(atomic_connection)

    # delete matching account
    dbexe.run_query(f"""
      DELETE FROM Branch
      WHERE ssn = '{str(uuid)}'
    """)
    
    dbexe.commit()

def create_branch(
    engine,
) -> UUID:
  print("\n~ Create a branch ~")
  return insert_branch(
    engine,
    getText("What is the Branch address? "),
    getDecimal("What is the overdraft fee? "),
    getDecimal("What is the monehtly fee? "),
    getDecimal("What is the $ value to waive the minimum fee? ")
  )
        

def delete_branch(
    engine,
    uuid: UUID,
):
  remove_branch(engine, uuid)
  print("\Branch deleted successfully.")