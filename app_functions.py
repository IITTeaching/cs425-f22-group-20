
from user_input import getMultipleChoice


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
    
    getMultipleChoice("You're creating an account!", ("yes",))
    
def delete_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're deleting an account!", ("yes",))
    
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
    
    getMultipleChoice("You're adding interest!", ("yes",))
    
def apply_overdraft_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're applying overdraft fees!", ("yes",))
    
def apply_monthly_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're applying monthly fees!", ("yes",))
    
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
    

