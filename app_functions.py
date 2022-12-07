

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
    
    getMultipleChoice("You're viewing make_transfer!", ("yes",))
    
    
def create_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're viewing create_account!", ("yes",))
    
def delete_account(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:

    getMultipleChoice("You're viewing delete_account!", ("yes",))

def create_customer(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:
    
    getMultipleChoice("You're viewing create_customer!", ("yes",))
    
def delete_customer(
    engine,
    customer_ssn: str,
    user_is_customer: bool
) -> None:

    getMultipleChoice("You're viewing delete_customer!", ("yes",))
    
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
    
    getMultipleChoice("You're viewing add_interest!", ("yes",))
    
def apply_overdraft_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing apply_overdraft_fees!", ("yes",))
    
def apply_monthly_fees(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing apply_monthly_fees!", ("yes",))
    
def get_total_customers_analytics(
    engine,
    manager_ssn: str,
    user_is_customer: bool = False, 
) -> None:
    
    getMultipleChoice("You're viewing analytics 1!", ("yes",))
  
def get_total_money_held_by_accounts(
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
    

