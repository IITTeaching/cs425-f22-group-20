import datetime
import decimal
from decimal import Decimal
from uuid import UUID
import enum
from enum import Enum
from typing import Union

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
    
def getDate(message, future = False) -> datetime.date:
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
                if (not future and 
                    year > datetime.date.today().year):
                    raise ValueError("Invalid future date")
                break
            except ValueError:
                print("\n    incorrect year OR iso date format entered, try again\n")
    
    while (True):
        user_month = input("month: ").strip()
        
        try:
            month = int(user_month)
            if (not 0 < month <= 12):
                raise ValueError("wrong month")
            if (not future and 
                datetime.date(year, month, 1) > datetime.date.today()):
                raise ValueError("Invalid future date")
            break
        except ValueError:
            print("\n    incorrect month entered, try again\n")
            
    while (True):
        user_day = input("day: ").strip()
        
        try:
            day = int(user_day)
            if (not future and 
                datetime.date(year, month, day) > datetime.date.today()):
                raise ValueError("Invalid future date")
            return datetime.date(year, month, day)
            
        except ValueError:
            print("\n    incorrect day entered, try again\n")
         
def getDecimal(message, min = None, inclusive = False) -> Decimal:
    """Gets a valid Decimal from the user."""
    
    dec: Decimal = Decimal()
    
    while (True):
        user_dec = input(message).strip()
        
        try:
            dec = Decimal(user_dec)
            if (min != None and 
                ((inclusive and dec < min) or
                 (not inclusive and dec <= min))):
                raise ValueError("Does not exceed minimum")
            break
        except ValueError:
            print(f"\n    incorrect integer entered, " +
                  (("must be >" + ("=" if (inclusive) else "") + f" {min}, ") 
                        if (min != None) else "") +
                  f"try again\n")
            
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

def getInt(message, min = None, inclusive = False) -> int:
    """Gets a valid integer from the user."""
    
    i: int = 0
    
    while (True):
        user_int = input(message).strip()
        
        try:
            i = int(user_int)
            if (min != None and 
                ((inclusive and i < min) or
                 (not inclusive and i <= min))):
                raise ValueError("Does not exceed minimum")
            break
        except ValueError:
            print(f"\n    incorrect integer entered, " +
                  (("must be >" + ("=" if (inclusive) else "") + f" {min}, ") 
                        if (min != None) else "") +
                  f"try again\n")
            
    return i


def getText(message) -> str:
    """Gets long text from the user."""
    
    satisfied = False
    
    while (not satisfied):
    
        txt = ""
        
        print(message, "\n")
        
        print("    End with a '\\' to finish: \n")
        
        while (len(txt) == 0 or txt[-2] != "\\"):
            txt += input("    ").rstrip() + "\n"
            
        
        txt = txt[:-2]
        
        print("\nAre you satisfied with your text?\n")
        print(
            "\n".join(
                ("    " if (i != 0) else "   '") + line 
                for i, line in enumerate(txt.split("\n"))
            ) + "'\n"
        )

        satisfied = getYorN("...")
        
    return txt
    

def getYorN(message) -> bool:
    
    return getChoice(f"{message} (Y/N): ",  ("Y", "N")) == 0
    


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
    option_names: tuple[str, ...]
) -> int:
    """Get a choice from the user, given a message,     \n
    and a tuple of option names                         \n
    Prints a very pretty prompt for the user to see their options. \n
    Returns the index of the user's choice from the tuple of options."""
    
    # this is really messy code, but I was having fun
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    prompt = (
        message + "\n" +
        "".join(f"    {letter}: {option_name}\n" 
         for (letter, option_name) in zip(letters, option_names)) + "\n" +
        "       : "
    )
    
    user_choice: int = getChoice(prompt, tuple(iter(letters[:len(option_names)])))
    
    return user_choice



class Menu:
    
    message: str
    options: tuple[tuple[str, Union["function", "Menu.Action", "Menu"]], ...]
    run_only_once: bool
    
    class Action(Enum):
        EXIT = enum.auto()
    
    def __init__(
        self, 
        message: str, 
        options: tuple[tuple[str, Union["function", "Menu.Action", "Menu"]], ...],
        run_only_once: bool = False
    ) -> None:
        self.message = message
        self.options = options
        self.run_only_once = run_only_once
        pass
    
    
    def run(self) -> int:
        """Run menu loop, if (run_only_once), then loop ends after 1 round.
        Returns the last user choice index upon ending."""
        
        
        running = True
        
        user_choice: int = -1
        
        while (running):
            
            user_choice = getMultipleChoice(
                self.message,
                self.get_option_names()
            )
            
            action = self.options[user_choice][1]
            
            if (callable(action)):
                action()
            elif (type(action) == Menu):
                action.run()
            elif (action == Menu.Action.EXIT):
                running = False
                
            if (self.run_only_once):
                running = False
                
        return user_choice
    
    
    def remove_options(self, *rm_option_names: str) -> None:
        
        names = self.get_option_names()
        if (all((n in names) for n in rm_option_names)):
            self.options = tuple(
                option 
                for option in self.options
                if option[0] not in rm_option_names
            )
        else:
            raise ValueError("Some of the given option names to remove are not options in this menu.")
    
    def get_option_names(self) -> tuple[str, ...]:
        return tuple(o[0] for o in self.options)
    
    def get_option_index(self, option_name: str) -> int:
        return self.get_option_names().index(option_name)



# print(datetime.date.isoformat(getDate("date: ")))
# print (getDecimal("hi: "))
# print (getUUID("hi: "))


# index = getMultipleChoice(
#     "hello?",
#     (
#         ("get", "ready!"),
#         ("set", "go!"),
#         ("yay", "neigh!"),
#         ("go", "hohoho!")
#     )
# )
# print("index: " + str(index))

# index2 = getChoice("question: ", ("yes", "no"))
# print("index: " + str(index2))

# getInt("int: ", 0, True)

# print(getText("\nwrite something"))