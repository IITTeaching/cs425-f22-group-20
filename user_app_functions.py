
import pandas as pd # type: ignore 
from roles import Role
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

from branch_query_functions import (
    all_branches
)

from user_query_functions import (
    user_is_in_database,
    insert_custumer,
    insert_employee,
    get_customer,
    get_employee,
    
    remove_customer,
    remove_employee
)


def create_user(
    engine, 
    ssn: str,
    user_role: Role
):
    
    if user_is_in_database(engine, user_role, ssn):
        return
    
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    
    branches: pd.DataFrame = all_branches(engine)
    
    # show user the branches
    pprint_df(branches)
    
    branch_index = getMultipleChoice(
        "\nChoose a branch: ", 
        tuple(b for b in branches["address"])
    )
    
    branchID = branches["branchid"][branch_index]
    
    if (user_role == Role.Customer):
        insert_custumer(engine, ssn, name, address, branchID)
        pprint_df(get_customer(engine, ssn))
    else:
        insert_employee(engine, user_role, ssn, name, address, branchID)
        pprint_df(get_employee(engine, ssn))
        
    print("\nNew user created successfully!")



# not used yet
def delete_customer(
    engine
):
    ssn = input("\nCustomer's ssn: ").strip()
    
    remove_customer(engine, ssn)
    print("\nCustomer deleted successfully.")
    
# not used yet  
def delete_employee(
    engine,
):
    ssn = input("\nEmployee's ssn: ").strip()
    
    remove_employee(engine, ssn)
    print("\nEmployee deleted successfully.")
    




# not used yet
def create_customer(
    engine
):
    print("\n~ Create a customer ~")

    # let user choose a branch to create account for
    branches: pd.DataFrame = all_branches(engine)

    # show user the branches
    pprint_df(branches)
        
    if (branches.empty):
        print("No branches found! Please create one.")
        return

    branch_index = getMultipleChoice(
        "\nChoose a branch: ", 
        tuple(b for b in branches["address"])
    )
    branch = branches["branchid"][branch_index]
    
    ssn = getText("What is the Customers SSN? ");
    name = getText("What is the Customers full name? ");
    address = getText("What is the Customers address? ");
        
    insert_customer(engine, ssn, name, address, branch)
  

# not used yet
def create_employee(
    engine
):
    print("\n~ Create an employee ~")

    # let user choose a branch to create account for
    branches: pd.DataFrame = all_branches(engine)

    # show user the branches
    pprint_df(branches)
        
    if (branches.empty):
        print("No branches found! Please create one.")
        return

    branch_index = getMultipleChoice(
        "\nChoose a branch: ", 
        tuple(b for b in branches["address"])
    )

    branch = branches["branchid"][branch_index]

    # let user choose customers from that branch to create account for
    customer_choices = pd.DataFrame()
        
    ssn = getText("What is the employees SSN? ");
    emp_name = getText("What is the employees full name? ");
    address = getText("What is the employees address? ");
    salary = getDecimal("What is the employees salary? ");
    emp_role = getText("What is the employees role? (teller, loan specialist, manager) ");

    insert_employee(engine, ssn, address, emp_name, salary, emp_role, branch)
