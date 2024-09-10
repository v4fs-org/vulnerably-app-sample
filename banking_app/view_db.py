from app import app, db
from models import User, Account, Transaction

def view_users():
    users = User.query.all()
    print("Users:")
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

def view_accounts():
    accounts = Account.query.all()
    print("\nAccounts:")
    for account in accounts:
        print(f"ID: {account.id}, User ID: {account.user_id}, Balance: {account.balance}")

def view_transactions():
    transactions = Transaction.query.all()
    print("\nTransactions:")
    for transaction in transactions:
        print(f"ID: {transaction.id}, Sender ID: {transaction.sender_id}, Recipient ID: {transaction.recipient_id}, Amount: {transaction.amount}, Timestamp: {transaction.timestamp}")

if __name__ == "__main__":
    with app.app_context():
        view_users()
        view_accounts()
        view_transactions()
