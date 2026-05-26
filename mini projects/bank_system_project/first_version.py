# Simple Bank System (Beginner Friendly)

accounts = {}

def create_account():
    name = input("Enter your name: ")
    acc_no = str(len(accounts) + 1)
    accounts[acc_no] = {
        "name": name,
        "balance": 0
    }
    print("Account created. Number:", acc_no)

def deposit():
    acc_no = input("Account number: ")
    if acc_no in accounts:
        amount = int(input("Amount: "))
        accounts[acc_no]["balance"] += amount
        print("Deposit successful")
    else:
        print("Account not found")

def withdraw():
    acc_no = input("Account number: ")
    if acc_no in accounts:
        amount = int(input("Amount: "))
        if amount <= accounts[acc_no]["balance"]:
            accounts[acc_no]["balance"] -= amount
            print("Withdrawal successful")
        else:
            print("Insufficient funds")
    else:
        print("Account not found")

while True:
    print("\n1.Create 2.Deposit 3.Withdraw 4.Exit")
    choice = input("Choose: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        break
    else:
        print("Invalid choice")
