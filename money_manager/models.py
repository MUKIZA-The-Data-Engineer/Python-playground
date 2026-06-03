from datetime import datetime
from config import date_format

class transactions:
    def __init__(self,
        transaction_id=None, transaction_type=None, amount=None,
         category=None, account=None,note=None, descritpion=None,
         date=None, currency=None):

        self.id = transaction_id   
        self.type = transaction_type
        self.amount = amount
        self.category = category
        self.account = account
        self.note = note
        self.descritpion = descritpion
        self.date = date if date else datetime.now().strftime(date_format)
        self.currency = currency

    def to_turple(self):

        return (self.type, self.amount, self.category, self.account,
                self.note, self.descritpion, self.date, self.currency)
    
    @staticmethod
    def from_row(row):
        """Create Transaction from daatabase"""

        return transactions(

            transaction_id = row[0],
            transaction_type = row[1],
            amount = row[2],
            category= row[3],
            account=[4],
            note= row[5],
            description = row[6],
            date = row[8]
        )
    def __str__(self):
        icon = "💰" if self.type == "income" else "💸"
        return f"{icon} {self.date} | {self.category} | {self.account} | {self.currency} {self.amount: 2f} | {self.note}"
    
class budget:
    def __init__(self, category=None, account=None, limit=None, currency=None, spent=0):
        self.category = category
        self.account = account
        self.limit = limit
        self.currency = currency
        self.spent = spent

    def remaining(self):
        return self.limit - self.spent
    
    def is_exceeded(self):
        return self.spent >= self.limit
    
    def can_add_expense(self, amount):
        return(self.spent + amount) <= self.limit
    
class Account:
    def __init__(self, name=None, account_type=None, currency=None, initial_balance=0):
        self.name = name
        self.type = account_type
        self.cuurency = currency
        self.balance = initial_balance
        


        



