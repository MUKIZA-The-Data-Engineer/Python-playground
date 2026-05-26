class BankATM:
    def __init__(self, initial_balance = 1600000, pin = "1234"):
        self.balance = initial_balance
        self.pin = pin
        self.is_running = True
        self.history = []

    def check_balance(self):
        print(f"\nYour current balance is: {self.balance} RWF")
    
    def deposit(self):
        try:
            amount = int(input("Enter amiunt to deposit:"))
            if amount > 0:
                self.balance += amount
                print(f"Successfully deposited {amount} RWF.")
                self,self.check_balance()

            else:
                print("Amount must be positive.")
        except ValueError:
            print("Amount must be greater than 0")

    def withdrawal(self):
        print("\n ----Withdrawal ----- ")
        try:
        
            amount  = int(input("Enter the amount: "))
            if amount % 1000 != 0:
                print("Error: Amount must be a multiple of 1000. ")
                return
            
            if amount > self.balance:
                print(f"Insufficient funds!. Balance: {self.balance} RWF")
                return 
            
            self.balance -= amount
            n5k = amount // 5000
            rem = amount % 5000
            n2k = rem // 2000
            n1k = (rem % 2000) // 1000

            print(f"Processing..... Dispensing: {n5k}*5k, {n2k}*2k, {n1k}*1k")
            print(f"withdrawal successful! Remaining: {self.balance} RWF")

        except ValueError:
            print("Invalid input.")

    def change_pin(self):
        old_pin = input("Enter current PIN: ")
        if old_pin == self.pin:
            new_pin = input("Enter new 4 digit PIN: ")

            if len(new_pin) == 4 and new_pin.isdigit():
                self.pin = new_pin
                print("PIN updated successfully! ")
            else:
                print("incorrect current PIN.")

    def fund_transfer(self):
        print("\n ----Fund transfer -----")
        try:

            account_number = input("Enter receipient account number (8 digits): ")

            if not account_number.isdigit() or len(account_number) != 8:
                print("Error: Invalid account  umber format. ")
                return
            
            amount = int(input(f"Enter amount to transfer to {account_number}: "))

            if amount <= 0:
                print("Error: Transfer amount must be greater than zero. ")
                return
            
            if amount > self.balance:
                print(f"Insuffient funds! You only have {self.balance} RWF")
                return 
            
            description = input("Enter trasnfer description (e.g., Rent, school fees, Water Bill, Electricity  )")

            self.balance -= amount
            transaction_record = f"Sent {amount} RWF to {account_number} for: {description}"
            self.history.append(transaction_record)
            print(f"\nTransferring {amount} RWF to account {account_number}...")
            print("Transfer Successful!")
            print(f"Your remaining balance: {self.balance} RWF")

        except ValueError:
            print("Invalid input. Please enter a number amount. ")


    def view_history(self):
        print("\n---- Transaction History ----")
        if not self.history:
            print("No transactions yet.")
        else:
            for item in self.history:
                print(f"- {item}")


    

    def main_menu(self):
        print("\n---- Welcome to Equity Bank ATM ----")
        while self.is_running:
            print("\n1. Balance Inquiry\n2. Withdrawal\n3.Deposit\n4. Fund Transfer\n5. PIN Change\n6. Exit ")

            choice = input("\nSelect an option (1-6): ")

            if choice == '1': self.check_balance()
            elif choice == '2': self.withdrawal()
            elif choice == '3': self.deposit()
            elif choice == '4': self.fund_transfer()
            elif choice == '5': self.change_pin()
            elif choice == '6': self.view_history()
            elif choice == '7': break
            else: print("Invalid choice.")

            cont = input("\nAny other action? (y/n): ").lower()
            if cont != 'y':
                self.is_running = False
        
        print("Thank you for using MKU Bank. Goodbye!")

# Initialize and Run
atm = BankATM()
atm.main_menu()




"""

Input Masking: For the PIN change and entry, use the getpass 
library so the PIN isn't visible on the screen while typing.

Transaction History: Add a self.history = [] list 
to the __init__ method. Every time a withdrawal or deposit happens, append a string (e.g., "Withdrew 5000") to the list. You can then add a "View Statement" menu option.

Maximum Withdrawal Limit: In the withdraw method, 
add a check to ensure the user doesn't withdraw more
 than a certain daily limit (e.g., 500,000 RWF).

Security (PIN Lock): Add a counter for incorrect PIN attempts.
 If the user fails 3 times, use sys.exit() to lock the session.

Persistence: Currently, the balance resets every time you restart 
the script. You could use a simple .txt file or a JSON file 
to save the balance and PIN so they stay updated between runs.

"""
    