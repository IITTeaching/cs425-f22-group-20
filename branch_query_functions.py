
import pandas as pd # type: ignore 
from helpers.postgres.db_execution import DBExecuter

def all_branches(engine) -> pd.DataFrame:
    """Get branches dataframe."""
    
    branches: pd.DataFrame = pd.DataFrame()
    
    with engine.connect() as atomic_connection:
    
        # make a database executer for this atomic block of SQL queries
        dbexe = DBExecuter(atomic_connection)
        
        branches = dbexe.query_to_df(f"""
            SELECT *
            FROM Branch
        """)
    
    return branches