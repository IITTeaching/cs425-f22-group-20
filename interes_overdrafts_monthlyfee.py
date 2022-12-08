from db_execution import DBExecuter
from uuid import UUID
import config as config

def apply_overdraft_fees(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False,
) -> None:

  if (user_is_customer):
    print("Customers cannot do this feature.")
    return

  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    accounts = dbexe.query_to_df(f"""
      SELECT * 
      FROM Holds
    """)

    manager_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Employee 
        WHERE ssn = '{manager_ssn}'
    """)

    for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):

      customer_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Customer 
        WHERE ssn = '{ssn}'
      """)

      if (customer_branchID == str(manager_branchID)):
        balance, overdraftType = dbexe.query_to_value(f"""
          SELECT balance, overdraftType
          FROM Account 
          WHERE accountnumber = '{accountnumber}'
        """)

        if (overdraftType == 'charge'):
          overdraftFee = dbexe.query_to_value(f"""
            SELECT overdraftFee 
            FROM Branch 
            WHERE branchID = '{customer_branchID}'
          """)

          if balance < 0:
            dbexe.run_query(f"""
              UPDATE Account 
              SET balance = {balance - overdraftFee} 
              WHERE accountnumber = '{accountnumber}'
            """)

          print("Overdraft fees have been processed successfully!")

def apply_interest_rates(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False,
) -> None:

  if (user_is_customer):
    print("Customers cannot do this feature.")
    return

  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    accounts = dbexe.query_to_df(f"""
      SELECT * 
      FROM Holds
    """)

    manager_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Employee 
        WHERE ssn = '{manager_ssn}'
      """)

    for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
      customer_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Customer 
        WHERE ssn = '{ssn}'
      """)
      if (customer_branchID == str(manager_branchID)):
        interestRate, balance = dbexe.query_to_value(f"""
          SELECT interestRate, balance 
          FROM Account 
          WHERE accountNumber = '{accountnumber}'
        """)

        dbexe.run_query(f"""
          UPDATE Account 
          SET balance = {balance + (balance * interestRate)} 
          WHERE accountnumber = '{accountnumber}'
        """)

        print("Interested applied successfully!")

def apply_monthly_fees(
  engine,
  manager_ssn: str,
  user_is_customer: bool = False,
) -> None:

  if (user_is_customer):
    print("Customers cannot do this feature.")
    return

  with engine.connect() as atomic_connection:

    dbexe = DBExecuter(atomic_connection)

    accounts = dbexe.query_to_df(f"""
      SELECT * 
      FROM Holds
    """)

    manager_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Employee 
        WHERE ssn = '{manager_ssn}'
      """)

    for ssn, accountnumber in zip(accounts["ssn"], accounts["accountnumber"]):
      customer_branchID = dbexe.query_to_value(f"""
        SELECT branch 
        FROM Customer 
        WHERE ssn = '{ssn}'
      """)
      if (customer_branchID == str(manager_branchID)):
        hasMonthlyFee = dbexe.query_to_value(f"""
          SELECT hasMonthlyFee 
          FROM Account 
          WHERE accountNumber = '{accountnumber}'
        """)
      
        if hasMonthlyFee:
          balance = dbexe.query_to_value(f"""
            SELECT balance 
            FROM account 
            WHERE accountnumber = '{accountnumber}'
          """)

          branchID = dbexe.query_to_value(f"""
            SELECT branch 
            FROM Customer 
            WHERE ssn = '{ssn}'
          """)

          waiveFeeMin, monthlyFee  = dbexe.query_to_value(f"""
            SELECT waiveFeeMin, monthlyFee
            FROM Branch 
            WHERE branchID = '{branchID}'
          """)

          if balance < waiveFeeMin:
            dbexe.run_query(f"""
              UPDATE Account
              SET balance = {balance - monthlyFee} 
              WHERE accountnumber = '{accountnumber}'
            """)