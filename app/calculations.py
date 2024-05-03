def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance
    
    def deposite(self, amout):
        self.balance += amout
    
    def withdraw(self, amout):
        if amout > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amout
    
    
    def collect_interest(self):
        self.balance *= 1.1
    