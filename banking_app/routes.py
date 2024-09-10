from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from sqlalchemy import text
from .forms import RegistrationForm, LoginForm, TransferForm, AdminLoginForm
from .models import db, User, Account, Transaction, Admin
from datetime import datetime
from . import create_app
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/rce', methods=['GET', 'POST'])
def rce():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('main.login'))
    output = ""
    if request.method == 'POST':
        command = request.form.get('command')
        # Vulnerable to RCE
        output = os.popen(command).read()
    return render_template('rce.html', output=output)

@main_bp.route('/rce_2', methods=['GET', 'POST'])
def rce_2():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('main.login'))
    output = ""
    if request.method == 'POST':
        command = request.form.get('command')
        # Vulnerable to RCE
        output = os.popen(command).read()
    return render_template('rce.html', output=output)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        account = Account(user_id=user.id, balance=0.0)
        db.session.add(account)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/account')
def account():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('main.login'))
    user = User.query.get(user_id)
    account = Account.query.filter_by(user_id=user.id).first()
    return render_template('account.html', user=user, account=account)

@main_bp.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('main.login'))
    form = TransferForm()
    if form.validate_on_submit():
        sender = User.query.get(user_id)
        recipient = User.query.filter_by(username=form.recipient.data).first()
        if recipient:
            transaction = Transaction(sender_id=sender.id, recipient_id=recipient.id, amount=form.amount.data, timestamp=datetime.now())
            db.session.add(transaction)
            sender_account = Account.query.filter_by(user_id=sender.id).first()
            recipient_account = Account.query.filter_by(user_id=recipient.id).first()
            sender_account.balance -= form.amount.data
            recipient_account.balance += form.amount.data
            db.session.commit()
            flash('Transfer successful!', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Recipient not found', 'danger')
    return render_template('transfer.html', form=form)

@main_bp.route('/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page', 'danger')
        return redirect(url_for('main.login'))
    transactions = Transaction.query.filter((Transaction.sender_id==user_id) | (Transaction.recipient_id==user_id)).all()
    return render_template('history.html', transactions=transactions)

@main_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Vulnerable to SQL injection
        query = text(f"SELECT * FROM admin WHERE username='{username}' AND password='{password}'")
        result = db.session.execute(query).fetchone()
        if result:
            session['admin_id'] = result.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Admin login unsuccessful. Please check username and password', 'danger')
    return render_template('admin_login.html', form=form)

@main_bp.route('/admin_dashboard')
def admin_dashboard():
    admin_id = session.get('admin_id')
    if not admin_id:
        flash('Please log in as admin to access this page', 'danger')
        return redirect(url_for('main.admin_login'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)