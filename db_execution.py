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
            raise ValueError("This query doesn't return a table, "
                             "so it can't be converted to a dataframe. \n"
                             "Only call query_to_df() with a `SELECT` statement, \n"
                             "or an `INSERT INTO table(column(s)...) VALUES (value(s)...) RETURNING (column(s)...)` \n"
                             "statement. \n"
                             "Call run_query() to just update the database.") from e
            
    def run_query(self, query: str) -> None:
        """Runs a SQL query (that updates the database without returning a table)"""
        # execute query
        ResultProxy = self.connection.execute(query)
        
        # if there is a resulting table
        if (ResultProxy.returns_rows):
            raise ValueError("This query returns a table, "
                             "so it should be converted to a dataframe to be viewed. \n"
                             "Only call run_query() with non-SELECT statements. \n"
                             "Call query_to_df() to convert to a dataframe.")
        