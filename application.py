
import config

from decimal import Decimal
from uuid import UUID
import sqlalchemy as db # type: ignore
import pandas as pd # type: ignore 
import numpy as np # type: ignore

from db_execution import DBExecuter

from roles import Role

from user_input import (
    Menu,
    getMultipleChoice
)

from app_functions import (
    # create_customer,
    # delete_customer,
    make_withdrawal,
    # make_deposit,
    # make_transfer,
    
    # create_account,
    # delete_account,
    view_month_statement,
    view_pending_transactions,
    # add_interest,
    # apply_overdraft_fees,
    # apply_monthly_fees,
    
    get_total_customers_analytics,
    get_total_money_held_by_accounts,
    get_total_employee_salary
)

from user_app_functions import (
    create_user
)
from deposit import (
    make_deposit
)
from create_delete_account import (
    create_account, 
    delete_account
)
from create_delete_customer import (
    create_customer,
    delete_customer,
)
from interes_overdrafts_monthlyfee import (
    apply_interest_rates as add_interest,
    apply_overdraft_fees,
    apply_monthly_fees
)

from transfer import (
    make_transfer
)

# DATABASE CONNECTION STUFF

engine = db.create_engine(
    'postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(config.database_username, config.database_password, config.database_name),
    future=True
)

metadata = db.MetaData()


# INIT TABLES and SAMPLE DATA

with engine.connect() as atomic_connection:
    
    # make a database executer for this atomic block of SQL queries
    dbexe = DBExecuter(atomic_connection)
    
    
    with open("reset_all_ddl.sql") as ddl_file:
        dbexe.run_query(ddl_file.read())

    with open("insertion.sql") as insertion_file:
        dbexe.run_query(insertion_file.read())
    
    dbexe.commit()




class BankApp:
    
    user_role: Role
    user_ssn: str

    main_menu: Menu
    transaction_menu: Menu
    management_menu: Menu
    analytics_menu: Menu
    
    def __init__(self) -> None:
        self.user_ssn = ""
        pass
    
    
    def login(self) -> None:
        # reset menus
        self.setup()
        
        # get user login info
        user_choice: int = getMultipleChoice(
            "\nWhat role are you signing in to?", (
                "Customer",
                "Manager",
                "Teller"
            )
        )
        
        self.user_role = Role(user_choice+1)
        
        self.user_ssn = input("\nEnter your SSN: ")
        
        create_user(engine, self.user_ssn, self.user_role)
        
        # reflect changes in user role
        self.init_access_control()
        
        
    def setup(self):
        """Set up menu interface."""
        
        self.transaction_menu = Menu(
            "\nAccount Transactions:", (
                ("Make withdrawal", self.call(make_withdrawal)),
                ("Make deposit",    self.call(make_deposit)),
                ("Make transfer",   self.call(make_transfer))
            ),
            run_only_once=True
        )
        
        self.management_menu = Menu(
            "\nAccount Management:", (
                ("Create customer",             self.call(create_customer)),
                ("Delete customer",             self.call(delete_customer)),
                ("Create account",              self.call(create_account)),
                ("Delete account",              self.call(delete_account)),
                ("View month statement",        self.call(view_month_statement)),
                ("View pending transactions",   self.call(view_pending_transactions)),
                ("Add interest",                self.call(add_interest)),
                ("Apply overdraft fees",        self.call(apply_overdraft_fees)),
                ("Apply monthly fees",          self.call(apply_monthly_fees))
            ),
            run_only_once=True
        )
        
        self.analytics_menu = Menu(
            "\nAnalytics:", (
                ("Get total customers in your managed branch", self.call(get_total_customers_analytics)),
                ("Get total amount of money held by accounts in your managed branch", self.call(get_total_money_held_by_accounts)),
                ("Get total employees salary of Employees in your managed branch", self.call(get_total_employee_salary))
            ),
            run_only_once=True
        )
        
        self.main_menu = Menu(
            "\nThis is main menu.", (
                ("Account Transactions", self.transaction_menu),
                ("Account Management",   self.management_menu),
                ("Analytics",            self.analytics_menu),
                ("Log out",     Menu.Action.EXIT),
                ("Exit",        Menu.Action.EXIT)
            )
        )
        
    def init_access_control(self):
        """Init access control so different users can only do what they're allowed."""
        
        if (self.user_role == Role.Customer):
            self.main_menu.remove_options(
                "Analytics"
            )
            self.management_menu.remove_options(
                "Add interest", 
                "Apply overdraft fees",
                "Apply monthly fees",
                "Create customer",
                "Delete customer"
            )
        elif (self.user_role == Role.Teller):
            self.main_menu.remove_options(
                "Account Management",
                "Analytics"
            )
            self.transaction_menu.remove_options(
                "Make transfer"
            )
            
    
    def run(self):
        """Run app loop until user exits."""
        
        running = True
        
        while (running):
        
            self.login()
            last_choice = self.main_menu.run()
            
            if (last_choice == self.main_menu.get_option_index("Log out")):
                print("\nLogged out successfully.")
            elif (last_choice == self.main_menu.get_option_index("Exit")):
                print("\nExiting")
                running = False
                
        
    def call(self, funct: "function"):
        """Call a function and pass in the engine, the user's ssn, and the isCustomer boolean."""
        
        def f():
            funct(engine, self.user_ssn, self.user_role == Role.Customer)
        
        return f
    
        
        
        
# RUN APP
        
bank_app = BankApp()
bank_app.run()