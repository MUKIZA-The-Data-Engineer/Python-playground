from datetime import datetime

class transaction_management:

    def __init__(self, amount, category, balance, descirption="", date=None):

        self.amount = amount # positive = income, negative = expense
        self.category = category
        self.balance = balance
        self.description = descirption
        self.date  = datetime.now().strftime("%m-%d-%y")


    def expense_is(self):
        return self.amount

    def income_is(self):
        return self.amount 
    

    #here I learned how to add values of functions
    def current_balance(self):
        balance = self.income_is() - self.expense_is()
        return balance

    def absolute_amount(self):
        return abs(self.amount)
    
    def to_dict(self):
        return{
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date

        }
    
    def __str__(self):
        type_icon = "💰" if self.income_is() else "💸"
        return f"{type_icon} {self.date}: {self.category} - ${self.absolute(): .2f}({self.description})"
    