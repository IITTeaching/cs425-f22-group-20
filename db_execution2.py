from typing import Any
import sqlalchemy as db # type: ignore
import pandas as pd # type: ignore 



"""
  changed DBExecuter so now it works with SQLAlchemy's Connection context manager
    for atomic blocks of SQL queries;
  got rid of DBExecuter.get_table()
"""


class DBExecuter:
    
    """
        An object that uses a Connection to execute database queries
        A Connection can be used to execute an atomic block of SQL queries
        
        To make an atomic block of SQL queries, do this:
        
        
        with engine.connect() as atomic_connection:     # begin atomic block
    
                # make a database executer for this atomic block of SQL queries
                
                dbexe = DBExecuter(atomic_connection)
                
                # (code here using database executer to execute queries)...
                
                
                # optional: commit all changes
                        without this call to commit, changes will be 
                        rolled back like the ROLLBACK statement in SQL
                # committing is not needed for SELECT statements,
                        since they don't change the database
                
                dbexe.commit()
    """
    
    def __init__(self, connection):
        self.connection = connection
        
    def commit(self):
        self.connection.commit()

    def query_to_df(self, query: str, **vari: any) -> pd.DataFrame:
        """Turns a SQL query (that returns a table) into a pandas DataFrame"""
        # execute query and get result set

        ResultProxy = self.connection.execute(db.text(query), vari)
        
        # if there is a resulting table
        if (ResultProxy.returns_rows):
            ResultSet = ResultProxy.fetchall()

            # convert to dataframe
            df: pd.DataFrame = None
            if (len (ResultSet) > 0):
                df = pd.DataFrame(ResultSet)
                df.columns = ResultSet[0].keys()
            else:    
                df = pd.DataFrame([], columns=tuple(ResultProxy.keys()))
        
            return df 
        # no resulting table
        try:
            ResultSet = ResultProxy.fetchall()
        except db.exc.ResourceClosedError as e:
            raise ValueError(
                "This query doesn't return a table, \n  "
                "so it can't be converted to a dataframe. \n  "
                "Only call query_to_df() with a `SELECT` statement, \n  "
                "or a statement with a `RETURNING` clause. \n  "
                "Call run_query() to just update the database."
            ) from e
        
    def query_to_value(self, query: str, **vari: any) -> Any:
        """Turns a SQL query (that returns a table with 1 value) into its single value"""
        ResultProxy = self.connection.execute(db.text(query), vari)
        
        # if there is a resulting table
        if (ResultProxy.returns_rows):
            ResultSet = ResultProxy.fetchall()

            # convert to dataframe
            df: pd.DataFrame = None
            if (len (ResultSet) > 0):
                df = pd.DataFrame(ResultSet)
                df.columns = ResultSet[0].keys()
            else:    
                df = pd.DataFrame([], columns=tuple(ResultProxy.keys()))
            return df[df.columns[0]][0] 
        # no resulting table
        try:
            ResultSet = ResultProxy.fetchall()
        except db.exc.ResourceClosedError as e:
            raise ValueError(
                "This query doesn't return a table, \n  "
                "so it can't be converted to a dataframe. \n  "
                "Only call query_to_df() with a `SELECT` statement, \n  "
                "or a statement with a `RETURNING` clause. \n  "
                "Call run_query() to just update the database."
            ) from e
        
        
            
    def run_query(self, query: str, **vari) -> None:
        """Runs a SQL query (that updates the database without returning a table)"""
        # execute query
        ResultProxy = self.connection.execute(db.text(query), vari)
        
        # if there is a resulting table
        if (ResultProxy.returns_rows):
            raise ValueError(
                "This query returns a table, \n  "
                "so it should be converted to a dataframe to be viewed. \n  "
                "Only call run_query() with non-SELECT and non-RETURNING statements. \n  "
                "Call query_to_df() to convert to a dataframe."
            )
    
