
import pandas as pd # type: ignore 
import decimal
from decimal import Decimal
from uuid import UUID
from helpers.postgres.db_execution import DBExecuter

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

from branch_query_functions import all_branches

# set precision of decimal values
decimal.getcontext().prec = 4



def insert_account(
    engine,
    customer_ssns: tuple[str, ...],
    accesstype: str,
    overdrafttype: str,
    hasmonthlyfee: bool,
    interestrate: Decimal = Decimal("0")
) -> UUID:
    """Creates a new account. Saves all related customers in Holds relation. 
    Returns its generated accountNumber."""
    
    # accountnumber
    accountnumber = None
    
    # run queries as atomic unit
    with engine.connect() as atomic_connection:
        
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
    
        # create new account and get its accountNumber from result
        accountnumber = dbexe.query_to_value(f"""
            INSERT INTO Account (accessType, overdraftType, hasMonthlyFee, interestRate)
            VALUES ('{accesstype}', '{overdrafttype}', {hasmonthlyfee}, {str(interestrate)})
            RETURNING accountNumber
        """)
        
        # if there are customers given for Holds relationship
        if (len(customer_ssns) > 0):
            # run query to insert all tuples (customerSSN, accountNumber)
            holds_values: str = ", ".join(
                f"('{ssn}', '{accountnumber}')" 
                for ssn in customer_ssns
            )
            dbexe.run_query(f"""
                INSERT INTO Holds (ssn, accountNumber)
                VALUES {holds_values}
            """)
            
        dbexe.commit()
    
    return accountnumber


def remove_account(
    engine,
    accountnumber: UUID
):
    """Deletes account with given accountnumber from Account relation."""
    
    # run queries as atomic unit
    with engine.connect() as atomic_connection:
        
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
    
        # delete matching account
        dbexe.run_query(f"""
            DELETE FROM Account
            WHERE accountnumber = '{accountnumber}'
        """)
        
        dbexe.commit()




def create_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
):
    print("\n~ Create an account ~")
    
    if (user_is_customer):
        # if user is a customer, just attach the customer to the account
        
        customer_ssns = (customer_ssn,)
    else:
        # if user is a manager, let them add multiple account holders 
        
        # let user choose a branch to create account for
        branches: pd.DataFrame = all_branches(engine)
    
        # show user the branches
        pprint_df(branches)
        
        branch_index = getMultipleChoice(
            "\nChoose a branch: ", 
            tuple(b for b in branches["address"])
        )
        branch = branches["branchid"][branch_index]
        
        # let user choose customers from that branch to create account for
        customer_choices = pd.DataFrame()
        
        with engine.connect() as atomic_connection:
            
            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)
            
            customer_choices = dbexe.query_to_df(f"""
                SELECT *
                FROM Customer
                WHERE branch = '{branch}'
            """)
            
        # if no accounts to work with, return
        if (customer_choices.empty):
            print("\nNo customers found to grant a new account to.")
            return
        
        # show user the customer options
        pprint_df(customer_choices)
        
        num_holders = 0
        customer_ssns = tuple()
        another = True
        
        while (num_holders < 1 or another):
            
            customer_index = getMultipleChoice(
                "\nChoose an account holder: ", 
                tuple(f"({ssn}) {name}" for ssn, name in zip(customer_choices["ssn"], customer_choices["name"]))
            )
            ssn = customer_choices["ssn"][customer_index]
            
            customer_ssns += (ssn,)
            num_holders += 1
            
            customer_choices = customer_choices.drop([customer_index])
            
            if (customer_choices.empty):
                another = False
            else:
                another = getYorN("\nWant to add another account holder?")
            
    
    
    access_types = ("checking", "savings")
    overdraft_types = ("regular", "reject", "charge")
    
    accesstype = access_types[getMultipleChoice(
        "\nChoose an access type:", 
        access_types
    )]
    
    overdrafttype = overdraft_types[getMultipleChoice(
        "\nChoose an overdraft type:", 
        overdraft_types
    )]
    
    hasmonthlyfee = getYorN("\nDoes this account have a monthly fee?")
    
    interestrate = getDecimal(
        "\nWhat is the interest rate on this account? For no interest, just put 0: ", 
        0, True
    )
    
    # save account in database
    accountnumber = insert_account(
        engine, customer_ssns, accesstype,
        overdrafttype, hasmonthlyfee, interestrate
    )
    
     
    print("\nAccount created successfully.")
    
    account = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
            
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        account = dbexe.query_to_df(f"""
            SELECT *
            FROM Account
            WHERE accountNumber = '{accountnumber}'
        """)
    
    pprint_df(account)




def delete_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
):
    print("\n~ Delete an account ~")
    
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
        print("\nNo accounts found to delete.")
        return
    
    # let user choose an account
    pprint_df(account_choices)
    
    account_index = getMultipleChoice(
        "\nChoose an account to delete: ", 
        tuple(a for a in account_choices["accountnumber"])
    )
    accountnumber = account_choices["accountnumber"][account_index]
    
    remove_account(engine, accountnumber)
    
    print("\nAccount deleted successfully.")