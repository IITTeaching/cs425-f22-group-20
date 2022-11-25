from typing import Any
import sqlalchemy as db # type: ignore
import pandas as pd # type: ignore 

class DBExecuter:
    
    """An object that executes database queries 
       and gets database objects, like tables"""
    
    def __init__(self, metadata, engine, connection):
        self.metadata = metadata
        self.engine = engine
        self.connection = connection

    def get_table(self, table_name: str) -> db.Table:
        """Gets a table from the database"""
        # get table from database
        return db.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)


    def query_to_df(self, query: str) -> pd.DataFrame:
        """Turns a SQL query (that returns a table) into a pandas DataFrame"""
        # execute query and get result set
        ResultProxy = self.connection.execute(query)
        
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
        
    def query_to_value(self, query: str) -> Any:
        """Turns a SQL query (that returns a table with 1 value) into its single value"""
        df = self.query_to_df(query)
        if (len(df.columns) == 1 and len(df[df.columns[0]]) == 1):
            # return single value
            return df[df.columns[0]][0]
        elif (len(df.columns) == 0 or len(df[df.columns[0]]) == 0):
            raise ValueError(
                "This query returns an empty table, \n  "
                "so there is no value to return. \n  "
            )
        else:
            raise ValueError(
                "This query returns a table that has more than one value, \n  "
                "so it should be converted to a dataframe to be manipulated/viewed. \n  "
                "Only call query_to_value() when you expect 1 value. \n  "
                "Call query_to_df() to convert to a dataframe."
            )
            
    def run_query(self, query: str) -> None:
        """Runs a SQL query (that updates the database without returning a table)"""
        # execute query
        ResultProxy = self.connection.execute(query)
        
        # if there is a resulting table
        if (ResultProxy.returns_rows):
            raise ValueError(
                "This query returns a table, \n  "
                "so it should be converted to a dataframe to be viewed. \n  "
                "Only call run_query() with non-SELECT and non-RETURNING statements. \n  "
                "Call query_to_df() to convert to a dataframe."
            )
        