
import pandas as pd # type: ignore 
from db_execution import DBExecuter
from roles import Role


def user_is_in_database(
    engine,
    user_role: Role, 
    user_ssn: str
) -> bool:
    """Rerurn True if user is in database."""
    
    in_database = False
    
    if (user_role == Role.Customer):
        # search Customer
        
        with engine.connect() as atomic_connection:
    
            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)
            
            in_database = not dbexe.query_to_df(f"""
                SELECT 1
                FROM Customer
                WHERE ssn = '{user_ssn}'
            """).empty
    else: 
        # search Employee and check emp_role
        
        emp_role = "manager" if (user_role == Role.Manager) else "teller"
        
        with engine.connect() as atomic_connection:
    
            # make a database executer for this atomic block of SQL queries
            dbexe = DBExecuter(atomic_connection)
            
            in_database = not dbexe.query_to_df(f"""
                SELECT 1
                FROM Employee
                WHERE ssn = '{user_ssn}' AND
                        emp_role = '{emp_role}'
            """).empty
    
    return in_database
 

def insert_custumer(
    engine,
    ssn: str,
    name: str,
    address: str,
    branchID: str
):
    """Insert new customer."""
    
    branch = f"'{branchID}'" if (branchID) else "NULL"
    
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        dbexe.run_query(f"""
            INSERT INTO Customer (ssn, name, address, branch)
            VALUES ('{ssn}', '{name}', '{address}', {branch})
        """)
        
        dbexe.commit()
 
def insert_employee(
    engine,
    role: Role,
    ssn: str,
    name: str,
    address: str,
    branchID: str
):
    """Insert new employee."""
    
    branch = f"'{branchID}'" if (branchID) else "NULL"
    
    role_names = {
        Role.Manager : "manager",
        Role.Teller : "teller"
    }
    
    salaries = {
        Role.Manager : 300000,
        Role.Teller : 100500
    }
    
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        dbexe.run_query(f"""
            INSERT INTO Employee (emp_role, salary, ssn, emp_name, address, branch)
            VALUES ('{role_names[role]}', {salaries[role]}, '{ssn}', '{name}', '{address}', {branch})
        """)
        
        dbexe.commit()
 
 
   
def get_customer(
    engine,
    ssn: str
) -> pd.DataFrame:
    """Get customer info dataframe."""
    
    customer: pd.DataFrame = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        customer = dbexe.query_to_df(f"""
            SELECT *
            FROM Customer
            WHERE ssn = '{ssn}'
        """)
    
    return customer
        
def get_employee(
    engine,
    ssn: str
) -> pd.DataFrame:
    """Get employee info dataframe."""
    
    employee: pd.DataFrame = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        employee = dbexe.query_to_df(f"""
            SELECT *
            FROM Employee
            WHERE ssn = '{ssn}'
        """)
    
    return employee
 