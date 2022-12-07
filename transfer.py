from typing import Tuple, Any

import sqlalchemy as db
from db_execution import DBExecuter
from pretty_printing import pprint_df, pprint_relation
import datetime 
from uuid import UUID
import decimal
from decimal import Decimal
import config as config
import app_functions as ap
import pandas as pd

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
    getYorN,

)


# set precision of decimal values
decimal.getcontext().prec = 4

def simple_access(
    engine, 
    transaction_type: str,
    accountfrom: UUID,
    accountto: UUID, 
    amount: Decimal,
    transaction_date: datetime.date,
    description: str
) -> tuple[UUID, UUID]:

    """Adds given amount to given account and 
    creates a matching Transaction.
    Returns the new Transaction's transactionID."""
    
    # account end balance
    end_balance: Decimal = Decimal()
        
    # new transactionID
    transactionID = None
        
    # run queries as an atomic unit
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)

        # add/remove money from account
        dbexe.run_query(f"""
            UPDATE Account
            SET balance = balance - {str(amount)}
            WHERE accountNumber = '{accountfrom}'
        """)

        dbexe.run_query(f"""
            UPDATE Account
            SET balance = balance + {str(amount)}
            WHERE accountNumber = '{accountto}'
        """)

        end_balance_from = dbexe.query_to_value(f"""
            SELECT balance FROM Account WHERE accountNumber = '{accountfrom}'
        """)

        end_balance_to = dbexe.query_to_value(f"""
            SELECT balance FROM Account WHERE accountNumber = '{accountto}'
        """)
        
        # create transaction and add it to Transaction relation
        transactionIDFrom = dbexe.query_to_value(f"""
            INSERT INTO transaction (transactiontype, amount, transactiondate, 
                description, accountfrom, accountto, startbalance)
            VALUES('{transaction_type}', '{amount}', '{transaction_date}', 
                '{description}', '{accountfrom}', '{accountto}', '{end_balance_to}')
                RETURNING transactionID
        """)
        transactionIDTo = dbexe.query_to_value(f"""
            INSERT INTO transaction (transactiontype, amount, transactiondate, 
                description, accountfrom, accountto, startbalance)
            VALUES('{transaction_type}', '-{amount}', '{transaction_date}', 
                '{description}', '{accountto}', '{accountfrom}', '{end_balance_from}')
                RETURNING transactionID
        """)
        
        dbexe.commit()
    return transactionIDFrom, transactionIDTo


def transfer(
    engine,
    transfertype: str,
    accountfrom: UUID,
    accountto: UUID,
    amount: Decimal,
    transaction_date: datetime.date,
    description: str
) -> (UUID,UUID):
    """Deposits given amount from given account and 
    creates a 'deposit' Transaction. 
    Returns the new Transaction's transactionID."""
    # deposit by adding amount
    return simple_access(engine, transfertype, accountfrom, accountto, amount, transaction_date, description)


def make_transfer (
    engine,
    customer_ssn: str,
    user_is_customer: bool
):

    print("\n~ Make a transfer ~")
    
    # find all allowed accounts
    account_choices: pd.DataFrame = pd.DataFrame()

    if user_is_customer:
        with engine.connect() as atomic_connection: # TRANSFER QUERY
            
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
        print("\nNo accounts found to make a transfer.")
        return
    
    # show user the account options
    pprint_df(account_choices)
    
    account_from_index = getMultipleChoice(
        "\nChoose an account to transfer from: ", 
        tuple(a for a in account_choices["accountnumber"])
    )

    accountfrom = account_choices["accountnumber"][account_from_index]
    if user_is_customer:
        if len(account_choices) > 0:
            otheracc = getYorN("\nWould you like to transfer to one of your other accounts: ")
            if otheracc:
                account_to_index = getMultipleChoice(
                    "\nChoose an account to transfer to: ",
                    tuple(a for a in account_choices["accountnumber"])
                )
                while account_to_index == account_from_index:
                    print('Cannot select the same account')
                    account_to_index = getMultipleChoice(
                        "\nChoose an account to transfer to: ",
                        tuple(a for a in account_choices["accountnumber"]))
                accountto = account_choices["accountnumber"][account_to_index]
            else:
                accountto = getUUID("\nEnter the UUID of the account you want to transfer to: ")
    else:
        account_to_index = getMultipleChoice(
            "\nChoose an account to transfer to: ",
            tuple(a for a in account_choices["accountnumber"])
        )
        while account_to_index == account_from_index:
            print('Cannot select the same account')
            account_to_index = getMultipleChoice(
                "\nChoose an account to transfer to: ",
                tuple(a for a in account_choices["accountnumber"]))
        accountto = account_choices["accountnumber"][account_to_index]

    amount = getDecimal('Enter how much you want to transfer: $ ', 0)
    
    transaction_date = datetime.date.today()
    if not user_is_customer:
        override_date = getYorN("\nDo you want to override today's date?")
    
        if (override_date):
            transaction_date = getDate("\nEnter a date for this transaction: ")


    # get overdraft type from user

    with engine.connect() as atomic_connection:

        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        overdraftType = dbexe.query_to_value(f"""
                SELECT overdrafttype 
                FROM account 
                WHERE accountnumber = '{accountfrom}' 
            """)
        accountfrombal = dbexe.query_to_value(f"""
                SELECT balance 
                FROM account 
                WHERE accountnumber = '{accountfrom}' 
            """)
        if accountfrombal - amount < 0 and overdraftType == 'reject':
            print('\nInsufficient funds')
            return

        else:

            # SELECT DISTINCT here

            fromBranch = dbexe.query_to_value(f"""
                SELECT branch 
                FROM customer JOIN holds on customer.ssn = holds.ssn 
                WHERE accountnumber = '{accountfrom}' 
            """)
            toBranch = dbexe.query_to_value(f"""
                SELECT branch 
                FROM customer JOIN holds on customer.ssn = holds.ssn 
                WHERE accountnumber = '{accountto}' 
            """)
            if fromBranch == toBranch:
                transactionType = 'transfer'
            else:
                transactionType = 'external transfer'
            
    # get description from user
    description = getText("\nWrite a description for this deposit.")

    # execute transaction in database
    transactionID = transfer(
        engine, transactionType, accountfrom, accountto, amount,
        transaction_date, description
    )

    print("\nTransfer made successfully.")
    
    transaction = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
            
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        transaction = dbexe.query_to_df(f"""
                        SELECT transactionID, transactionType, amount, 
                            transactionDate, description, accountTo, startBalance
                        FROM Transaction
                        WHERE transactionID = '{transactionID[0]}'
                    """)
        pprint_df(transaction)
        if not user_is_customer:
            transaction2 = dbexe.query_to_df(f"""
                            SELECT transactionID, transactionType, amount, 
                                transactionDate, description, accountTo, startBalance
                            FROM Transaction
                            WHERE transactionID = '{transactionID[1]}'
                        """)
            pprint_df(transaction2)

    

       

            

            
        

