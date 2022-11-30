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

def getInt(message) -> int:
    """Gets a valid integer from the user."""
    
    i: int = 0
    
    while (True):
        user_int = input(message).strip()
        
        try:
            i = int(user_int)
            break
        except ValueError:
            print("\n    incorrect integer entered, try again\n")
            
    return i


def getChoice(message, options: tuple[str, ...]) -> int:
    """Gets a choice from the user, given a message and     \n
    a tuple of string options.                              \n
    Returns the index of the user's choice from the tuple of options."""
    
    c: int = 0
    
    while (True):
        user_choice = input(message).strip().lower()
        
        try:
            c = tuple(choice.lower() for choice in options).index(user_choice)
            break
        except ValueError:
            print("\n    incorrect choice entered, try again\n")
            
    return c


def getMultipleChoice(
    message: str, 
    options: tuple[str, ...], 
    responses: tuple[str, ...]
) -> int:
    """Get a choice from the user, given a message,     \n
    a tuple of string options, and                      \n
    a tuple of responses to print after they choose.    \n
    Prints a very pretty prompt for the user to see their options.
    Returns the index of the user's choice from the tuple of options."""
    
    # this is really messy code, but I was having fun
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    prompt = (
        message + "\n" +
        "".join(f"    {letter}: {choice}\n" 
         for (letter, choice) in zip(letters, options)) + "\n" +
        "       : "
    )
    
    user_choice: int = getChoice(prompt, tuple(iter(letters[:len(options)])))
    
    print(responses[user_choice])
    
    return user_choice





# print(datetime.date.isoformat(getDate("hi: ")))
# print (getDecimal("hi: "))
# print (getUUID("hi: "))


# index = getMultipleChoice(
#     "hello?",
#     ("get", "ready", "go", "set", "up"),
#     ("yay", "neigh", "hohoho", "SHEESH", "cool")
# )
# print("index: " + str(index))