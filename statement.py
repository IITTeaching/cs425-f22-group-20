import pandas as pd
from db_execution import DBExecuter
from pretty_printing import pprint_df
from datetime import date
import calendar as cal


from user_input import (
    getMultipleChoice,
    getYearMonth,
)

#Generates A monthly statement based on what month and year the user wants to view.
def view_month_statement(
        engine,
        customer_ssn: str,
        user_is_customer: bool
) -> None:

    print("\n~ View Monthly Statement ~")

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
        print("\nNo accounts found to view a statement.")
        return

    # show user the account options
    pprint_df(account_choices)

    account_index = getMultipleChoice(
        "\nChoose an account to view their statement: ",
        tuple(a for a in account_choices["accountnumber"])
    )

    accountnumber = account_choices["accountnumber"][account_index]
    with engine.connect() as atomic_connection:

        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)

        stmtTime = getYearMonth('Which month do you want to view your statement on?')
        stmtYear = stmtTime[0]
        stmtMonth = stmtTime[1]
        currentValue = None
        monthString = cal.month_name[stmtMonth]
        transactions = dbexe.query_to_df(f"""
        SELECT * 
        FROM transaction 
        WHERE accountto = '{accountnumber}' AND 
            date_part('year', transactiondate) = '{stmtYear}' AND 
            date_part('month', transactiondate) = '{stmtMonth}' 
        ORDER BY transactiondate 
                """)

        if not transactions.empty:
            currentValue = dbexe.query_to_df(f"""
                 SELECT endbalance 
                 FROM transaction 
                 WHERE accountto = '{accountnumber}' AND 
                     date_part('year', transactiondate) = '{stmtYear}' AND 
                     date_part('month', transactiondate) = '{stmtMonth}' 
                 ORDER BY transactiondate DESC LIMIT 1
                         """)
            if stmtYear == date.today().year and stmtMonth == date.today().month:
                print('Month is still in progress. Please use "view pending transactions" to view the current month')
            else:
                pprint_df(transactions)
                print(f"""Full Statement for {monthString} {stmtYear} """)
                print(f"""Current Account Balance is {currentValue} """)
        elif stmtYear > date.today().year or (stmtYear == date.today().year and stmtMonth > date.today().month):
            print('You cannot view a statement in the future')
        elif transactions.empty:
            print('No Transactions occurred on the specified month')







