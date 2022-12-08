from db_execution import DBExecuter
import config as config
import pandas as pd
import datetime

from pretty_printing import pprint_df

from user_input import (
    Menu,
    getMultipleChoice,
    getChoice,
    getDate,
    getDecimal,
    getInt,
    getUUID,
    getYearMonth,
    getText,
    getYorN
)

def make_withdrawal(
  engine,
  customer_ssn: str,
  user_is_customer: bool = False, 
):
  # This function withdraws from an account
  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    account_choices: pd.DataFrame = pd.DataFrame()
    
    if (user_is_customer): # user is a customer, so find all user's accounts
      account_choices = dbexe.query_to_df(f"""
          SELECT accountNumber, balance, accessType, overdraftType, hasMonthlyFee, interestRate 
          FROM Account natural join Holds
          WHERE ssn = '{customer_ssn}'
      """)
    else: # user is a manager/teller, so find all accounts
      account_choices = dbexe.query_to_df(f"""
          SELECT *
          FROM Account
      """)
            
    # if no accounts to work with, return
    if (account_choices.empty):
        print("\nNo accounts found to make a withdraw from.")
        return
    
    # show user the account options
    pprint_df(account_choices)
    
    account_index = getMultipleChoice(
        "\nChoose an account to withdraw from: ", 
        tuple(a for a in account_choices["accountnumber"])
    )
    accountnumber = account_choices["accountnumber"][account_index]
    
    # get a positive Decimal amount from user
    amount = getDecimal("\nHow much to withdraw: $ ", 0)
    
    # if not customer, let the user override today's date
    transaction_date = datetime.date.today()
    if (not user_is_customer):
        override_date = getYorN("\nDo you want to override today's date?")
        if (override_date):
            transaction_date = getDate("\nEnter a date for this transaction: ")
    
    # get description from user
    description = getText("\nWrite a description for this withdrawal.")

    balance = dbexe.query_to_value(f"""
      SELECT balance FROM Account WHERE accountnumber = '{accountnumber}'
    """)

    dbexe.run_query(f"""
      UPDATE Account SET balance = balance - {amount} WHERE accountnumber = '{accountnumber}'
    """)

    transactionID = dbexe.query_to_value(f"""
      INSERT INTO Transaction (transactionType, amount, transactionDate, 
              description, accountTo, endBalance)
      VALUES ('withdrawal', {str(amount)}, '{transaction_date}', 
              '{description}', '{accountnumber}', {balance - amount})
      RETURNING transactionID
    """)
    
    # save changes
    dbexe.commit()

    return transactionID

