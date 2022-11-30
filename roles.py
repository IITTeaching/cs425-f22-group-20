
import enum
from enum import Enum

class Role(Enum):
    Customer = enum.auto()
    Manager = enum.auto()
    Teller = enum.auto()
    
    
# Customers:        (ONLY FOR THEIR OWN)
#
#   withdrawal, deposit, transfer
#
#   create account, delete account, 
#   month statement, pending transactions

# Managers:         EVERYTHING

# Tellers:
#
#   withdrawal, deposit






