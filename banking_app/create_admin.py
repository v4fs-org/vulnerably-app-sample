from app import app, db
from models import Admin

def create_admin(username, password):
    with app.app_context():
        # Create a new admin user
        new_admin = Admin(username=username, password=password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create a new admin user.')
    parser.add_argument('username', type=str, help='The username for the new admin user.')
    parser.add_argument('password', type=str, help='The password for the new admin user.')

    args = parser.parse_args()

    create_admin(args.username, args.password)