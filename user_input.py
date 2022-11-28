import datetime
import decimal
from decimal import Decimal
from uuid import UUID

# set precision of decimal values
decimal.getcontext().prec = 4

def getYearMonth(message) -> tuple[int, int]:
    """Gets a valid month from the user."""
    
    year = 0
    month = 0
    
    print(message, "\n")
    
    while (True):
        user_year = input("year: ").strip()
        
        try:
            year = int(user_year)
            break
        except ValueError:
            print("\n    incorrect year entered, try again\n")
    
    while (True):
        user_month = input("month: ").strip()
        
        try:
            month = int(user_month)
            if (not 0 < month <= 12):
                raise ValueError("wrong month")
            break
        except ValueError:
            print("\n    incorrect month entered, try again\n")
            
        
    return (year, month)
    
def getDate(message) -> datetime.date:
    """Gets a valid date from the user."""
    
    year = 0
    month = 0
    day = 0
    
    print(message, "\n")
    
    while (True):
        user_year = input("year OR iso date format: ").strip()
        
        try:
            return datetime.date.fromisoformat(user_year)
        
        except ValueError:
            try:
                year = int(user_year)
                break
            except ValueError:
                print("\n    incorrect year OR iso date format entered, try again\n")
    
    while (True):
        user_month = input("month: ").strip()
        
        try:
            month = int(user_month)
            if (not 0 < month <= 12):
                raise ValueError("wrong month")
            break
        except ValueError:
            print("\n    incorrect month entered, try again\n")
            
    while (True):
        user_day = input("day: ").strip()
        
        try:
            day = int(user_day)
            return datetime.date(year, month, day)
            
        except ValueError:
            print("\n    incorrect day entered, try again\n")
         
def getDecimal(message) -> Decimal:
    """Gets a valid Decimal from the user."""
    
    dec: Decimal = Decimal()
    
    while (True):
        user_dec = input(message).strip()
        
        try:
            dec = Decimal(user_dec)
            break
        except ValueError:
            print("\n    incorrect decimal entered, try again\n")
            
    return dec

def getUUID(message) -> UUID:
    """Gets a valid UUID from the user. UUID is used for accountNumber, branchID, transactionID."""
    
    _uuid: UUID = UUID("00000000-0000-4000-A000-000000000000", version=4)
    
    while (True):
        user_dec = input(message).strip()
        
        try:
            _uuid = UUID(user_dec, version=4)
            break
        except ValueError:
            print("\n    incorrect UUID entered, try again\n")
            
    return _uuid


# print(datetime.date.isoformat(getDate("hi: ")))
# print (getDecimal("hi: "))
# print (getUUID("hi: "))