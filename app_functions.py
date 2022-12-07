from interes_overdrafts_monthlyfee import apply_interest_rates
from user_input import getMultipleChoice
from create_delete_customer import (
    create_customer as create_customer_intern,
    delete_customer as delete_customer_intern,
)
from create_delete_account import (
    create_account as create_account_intern,
    delete_account as delete_account_intern,
)


"""placeholders until real functions are all finished"""

""" Make real functions in another file in this format """

def make_withdrawal(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're withdrawing!", ("yes",))

def make_deposit(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're depositing!", ("yes",))
    
def make_transfer(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're transferring!", ("yes",))
    
def create_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    choice = getMultipleChoice("Are you sure you'd like to create a new account?", ("Yes", "No"))
    if choice == 0:
        create_account_intern(engine)
    
def delete_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:

    choice = getMultipleChoice("Are you sure you'd like to delete an account?", ("Yes", "No"))
    if choice == 0:
        delete_account_intern(engine)

def create_customer(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    choice = getMultipleChoice("Are you sure you'd like to create a new customer?", ("Yes", "No"))
    print(choice)
    if choice == 0:
        create_customer_intern(engine)
    
def delete_customer(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:

    choice = getMultipleChoice("Are you sure you'd like to delete a customer?", ("Yes", "No"))
    if choice == 0:
        delete_customer_intern(engine)
    
def view_month_statement(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're viewing a month statement!", ("yes",))
    
def view_pending_transactions(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're viewing pending transactions!", ("yes",))
    
def add_interest(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    choice = getMultipleChoice("Are you sure you'd like to add interest?", ("Yes", "No"))
    if choice == 0:
        apply_interest_rates(engine, manager_ssn, user_is_customer) 
    
def apply_overdraft_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    choice = getMultipleChoice("Are you sure you'd like to apply overdraft fees?", ("Yes", "No"))
    if choice == 0:
        apply_overdraft_fees(engine, manager_ssn, user_is_customer)
    
def apply_monthly_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    choice = getMultipleChoice("Are you sure you'd like to apply monthly fees?", ("Yes", "No"))
    if choice == 0:
        apply_monthly_fees(engine, manager_ssn, user_is_customer)
    
def insert_analytics_name_1_here(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing analytics 1!", ("yes",))
  
def insert_analytics_name_2_here(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing analytics 2!", ("yes",))
  
def insert_analytics_name_3_here(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing analytics 3!", ("yes",))
    

