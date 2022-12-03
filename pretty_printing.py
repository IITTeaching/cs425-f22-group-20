
import numpy as np # type: ignore 
import pandas as pd # type: ignore
from db_execution import DBExecuter

def pprint_df(df: pd.DataFrame):
    """Pretty prints a pandas DataFrame"""
    
    # crop long values in table
    def crop_long(val):
        return v[:8] + "..." if( len(v := str(val)) > 20) else val
    crop_long_all = np.frompyfunc(crop_long, 1, 1)
    
    # def crop_long_colname(val):
    #     return val[:10] if( len(val) > 10) else val

    # df.columns = (crop_long_colname(val) for val in df.columns)

    print("\n", df.apply(crop_long_all).to_string(), sep="")
    
def pprint_relation(dbexe: DBExecuter, table_name: str):
    """Pretty prints the SELECT * FROM {table_name}"""
    df = dbexe.query_to_df(f"""
        SELECT *
        FROM {table_name}
    """)
    pprint_df(df)