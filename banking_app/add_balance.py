from app import app, db
from models import Account
import argparse

def add_balance(account_id, amount):
    try:
        account = Account.query.get(account_id)
        if account:
            if amount < 0:
                print(f"Error: Cannot add a negative amount: ${amount}")
                return
            account.balance += amount
            db.session.commit()
            print(f"Added ${amount} to account ID {account_id}. New balance: ${account.balance}")
        else:
            print(f"Error: Account ID {account_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add balance to an account")
    parser.add_argument("account_id", type=int, help="The ID of the account")
    parser.add_argument("amount", type=float, help="The amount to add to the balance")

    args = parser.parse_args()

    if args.amount <= 0:
        print("Error: Amount must be positive.")
    else:
        with app.app_context():
            add_balance(args.account_id, args.amount)
