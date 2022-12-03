
import pandas as pd # type: ignore 
import datetime
import decimal
from decimal import Decimal
from uuid import UUID
from db_execution import DBExecuter

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

# set precision of decimal values
decimal.getcontext().prec = 4


def simple_access(
    engine, 
    transaction_type: str,
    accountnumber: UUID, 
    amount: Decimal,
    transaction_date: datetime.date,
    description: str
) -> UUID:
    """Adds given amount to given account and 
    creates a matching Transaction.
    Returns the new Transaction's transactionID."""
    
    # account strart balance
    start_balance: Decimal = Decimal()
    # run queries
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        # get current account balance
        start_balance = dbexe.query_to_value(f"""
            SELECT balance FROM Account WHERE accountNumber = '{accountnumber}'
        """)
        
    # new transactionID
    transactionID = None
        
    # run queries as an atomic unit
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
    
        # add/remove money from account
        dbexe.run_query(f"""
            UPDATE Account
            SET balance = balance + {str(amount)}
            WHERE accountNumber = '{accountnumber}'
        """)
        
        # create transaction and add it to Transaction relation
        transactionID = dbexe.query_to_value(f"""
            INSERT INTO Transaction (transactionType, amount, transactionDate, 
                    description, accountTo, startBalance)
            VALUES ('{transaction_type}', {str(amount)}, '{transaction_date}', 
                    '{description}', '{accountnumber}', {str(start_balance)})
            RETURNING transactionID
        """)
        
        # save changes
        dbexe.commit()
    
    # return new Transaction's transactionID
    return transactionID


def deposit(
    engine, 
    accountnumber: UUID, 
    amount: Decimal,
    transaction_date: datetime.date,
    description: str
) -> UUID:
    """Deposits given amount from given account and 
    creates a 'deposit' Transaction. 
    Returns the new Transaction's transactionID."""
    # deposit by adding amount
    return simple_access(engine, "deposit", accountnumber, amount, transaction_date, description)




def make_deposit(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    print("\n~ Make a deposit ~")
    
    # find all allowed accounts
    account_choices: pd.DataFrame = pd.DataFrame()
    
    if (user_is_customer): # user is a customer, so find all user's accounts
        with engine.connect() as atomic_connection:
            
            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)
            
            account_choices = dbexe.query_to_df(f"""
                SELECT accountNumber, balance, accessType, overdraftType, hasMonthlyFee, interestRate 
                FROM Account natural join Holds
                WHERE ssn = '{customer_ssn}'
            """)
    else: # user is a manager/teller, so find all accounts
        with engine.connect() as atomic_connection:
            
            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)
            
            account_choices = dbexe.query_to_df(f"""
                SELECT *
                FROM Account
            """)
            
    # if no accounts to work with, return
    if (account_choices.empty):
        print("\nNo accounts found to make a deposit.")
        return
    
    # show user the account options
    pprint_df(account_choices)
    
    account_index = getMultipleChoice(
        "\nChoose an account to deposit into: ", 
        tuple(a for a in account_choices["accountnumber"])
    )
    accountnumber = account_choices["accountnumber"][account_index]
    
    # get a positive Decimal amount from user
    amount = getDecimal("\nHow much to deposit: $ ", 0)
    
    # if not customer, let the user override today's date
    transaction_date = datetime.date.today()
    if (not user_is_customer):
        
        override_date = getYorN("\nDo you want to override today's date?")
        
        if (override_date):
            transaction_date = getDate("\nEnter a date for this transaction: ")
    
    # get description from user
    description = getText("\nWrite a description for this deposit.")
    
    # execute transaction in database
    transactionID = deposit(
        engine, accountnumber, amount,
        transaction_date, description
    )
    
    print("\nDeposit made successfully.")
    
    transaction = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
            
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        transaction = dbexe.query_to_df(f"""
            SELECT transactionID, transactionType, amount, 
                transactionDate, description, accountTo, startBalance
            FROM Transaction
            WHERE transactionID = '{transactionID}'
        """)
    
    pprint_df(transaction)