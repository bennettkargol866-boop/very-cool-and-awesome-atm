import json
import os
import sys

ACCOUNTS_FILE = "accounts.json"
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        print("No accounts found – Please contact the bank.")
        sys.exit()
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("No accounts found – Please contact the bank.")
        sys.exit()


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


def authenticate(accounts):
    while True:
        account_number = input("Enter your 5-digit account number (or 'q' to quit): ").strip()
        if account_number.lower() == 'q':
            sys.exit("Goodbye!")
        pin = input("Enter your 4-digit PIN: ").strip()
        for user in accounts:
            if str(user["accountNumber"]) == account_number and str(user["pin"]) == pin:
                print(f"\nWelcome {user['firstName']} {user['lastName']}!\n")
                return user
        print("No account with that set of credentials found.\n")

def deposit(user, accounts):
    while True:
        account_type = input("Deposit into (checking/savings): ").strip().lower()
        if account_type not in ["checking", "savings"]:
            print("Invalid account type. Please enter 'checking' or 'savings'.")
            continue
        break

    while True:
        try:
            amount = float(input("Enter deposit amount: "))
            if amount < 0:
                print("Amount must be >= 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    key = f"{account_type}Balance"
    user[key] += amount
    transaction = f"Deposit into {account_type.capitalize()} in amount of ${amount:.2f}"
    user["transactions"].append(transaction)
    save_accounts(accounts)
    print(f"Deposited ${amount:.2f} into {account_type}.\n")

def withdraw(user, accounts):
    while True:
        account_type = input("Withdraw from (checking/savings): ").strip().lower()
        if account_type not in ["checking", "savings"]:
            print("Invalid account type. Please enter 'checking' or 'savings'.")
            continue
        break

    key = f"{account_type}Balance"
    while True:
        try:
            amount = float(input("Enter withdrawal amount: "))
            if amount < 0:
                print("Amount must be >= 0.")
                continue
            if amount > user[key]:
                print(f"Insufficient funds. Your {account_type} balance is ${user[key]:.2f}")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    user[key] -= amount
    transaction = f"Withdrawal from {account_type.capitalize()} in amount of ${amount:.2f}"
    user["transactions"].append(transaction)
    save_accounts(accounts)
    print(f"dispensing ${amount:.2f}\n")

def check_balance(user):
    print(f"Checking: ${user['checkingBalance']:.2f}")
    print(f"Savings: ${user['savingsBalance']:.2f}\n")

def view_transactions(user):
    if not user["transactions"]:
        print("No transactions found.\n")
        return
    for i, t in enumerate(user["transactions"], start=1):
        print(f"{i}) {t}")
    print("")

def main_menu(user, accounts):
    while True:
        print("Main Menu:")
        print("1) Deposit")
        print("2) Withdrawal")
        print("3) Check Balance")
        print("4) View Transactions")
        print("5) Logout")
        print("q) Quit")
        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            deposit(user, accounts)
        elif choice == '2':
            withdraw(user, accounts)
        elif choice == '3':
            check_balance(user)
        elif choice == '4':
            view_transactions(user)
        elif choice == '5':
            print("Logging out...\n")
            break
        elif choice == 'q':
            sys.exit("Goodbye!")
        else:
            print("Invalid option. Please try again.\n")

def main():
    accounts = load_accounts()
    while True:
        user = authenticate(accounts)
        main_menu(user, accounts)

if __name__ == "__main__":
    main()
