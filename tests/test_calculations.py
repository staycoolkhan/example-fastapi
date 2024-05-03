import pytest
from app.calculations import BankAccount, add, subtract, multiply, divide, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected): 
    print("test add function")
    assert add(num1, num2) == expected

def test_substract() -> None:
    assert subtract(9, 4) == 5
    
def test_multiply() -> None:
    assert multiply(4, 3) == 12   
    
def test_divide() -> None:
    assert divide(25, 5) == 5   


def test_bank_set_initial_amout():
    back_account = BankAccount(50)
    assert back_account.balance == 50

def test_bank_default_amout(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposite(bank_account):
    bank_account.deposite(20)
    assert bank_account.balance == 70
    
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55



@pytest.mark.parametrize("deposited, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
      zero_bank_account.deposite(deposited)
      zero_bank_account.withdraw(withdraw)
      assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
        
