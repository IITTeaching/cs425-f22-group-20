
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
    getYearMonth
)

from branch_query_functions import (
    all_branches
)

from user_query_functions import (
    user_is_in_database,
    insert_custumer,
    insert_employee,
    get_customer,
    get_employee
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
