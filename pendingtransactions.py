import pandas as pd
from db_execution import DBExecuter
from pretty_printing import pprint_df
from datetime import date

from user_input import (
    getMultipleChoice
)


# Similar to view_month_statement, but is executed for the current month instead,
# removes the print for current balance, and indicates the date range of the transactions.

def view_pending_transactions(
        engine,
        customer_ssn: str,
        user_is_customer: bool
) -> None:
    print("\n~ View Pending Transactions ~")

    # find all allowed accounts
    account_choices: pd.DataFrame = pd.DataFrame()

    if user_is_customer:  # user is a customer, so find all user's accounts
        with engine.connect() as atomic_connection:

            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)

            account_choices = dbexe.query_to_df(f"""
                                SELECT accountNumber, balance, accessType, overdraftType, hasMonthlyFee, interestRate 
                                FROM Account natural join Holds
                                WHERE ssn = '{customer_ssn}'
                            """)
    else:  # user is a manager/teller, so find all accounts
        with engine.connect() as atomic_connection:

            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)

            account_choices = dbexe.query_to_df(f"""
                                SELECT *
                                FROM Account
                            """)

    # if no accounts to work with, return
    if account_choices.empty:
        print("\nNo accounts found to view pending transactions.")
        return

    # show user the account options
    pprint_df(account_choices)

    account_index = getMultipleChoice(
        "\nChoose an account to view their pending transactions: ",
        tuple(a for a in account_choices["accountnumber"])
    )

    accountnumber = account_choices["accountnumber"][account_index]
    with engine.connect() as atomic_connection:

        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        currentYear = date.today().year
        currentMonth = date.today().month

        transactions = dbexe.query_to_df(f"""
        SELECT * 
        FROM transaction 
        WHERE accountto = '{accountnumber}' AND 
            date_part('year', transactiondate) = '{currentYear}' AND 
            date_part('month', transactiondate) = '{currentMonth}' 
        ORDER BY transactiondate 
                """)

        if not transactions.empty:
            currentValue = dbexe.query_to_df(f"""
                 SELECT endbalance 
                 FROM transaction 
                 WHERE accountto = '{accountnumber}' AND 
                     date_part('year', transactiondate) = '{currentYear}' AND 
                     date_part('month', transactiondate) = '{currentMonth}' 
                 ORDER BY transactiondate DESC LIMIT 1
                         """)
            pprint_df(transactions)
            print(f"""Partial Statement from {currentYear}-{currentMonth}-01 - {date.today()}""")
        else:
            print('No transactions found for the current month')
