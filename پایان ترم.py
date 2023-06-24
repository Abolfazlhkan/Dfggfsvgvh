import sqlite3
from datetime import datetime


class User:
    def __init__(self, name, last_name, f_name, birth_date, city, 
                 mobile, code_mile, phone=None, user_id=None):
        self.name = name
        self.last_name = last_name
        self.f_name = f_name
        self.birth_date = birth_date
        self.city = city
        self.mobile = mobile
        self.code_mile = code_mile
        self.phone = phone
        self.user_id = user_id

    def info(self):
        print(f"Name: {self.name} {self.last_name}\nFather Name: {self.f_name}")
        print(f"Birth Date: {self.birth_date}\nCity: {self.city}\nMobile: {self.mobile}")
        print(f"National ID: {self.code_mile}")
        

class Account:
    def __init__(self, user, account_type, account_id=None):
        self.user = user
        self.account_type = account_type
        self.created_at = datetime.now()
        self.balance = 0
        self.account_id = account_id

    def withdraw(self, amount):
        if( amount > self.balance ) and ( amount < 500000):
            print("Not enough balance")
        else:
            self.balance -= amount
            print("Withdrawal successful")

    def deposit(self, amount):
        self.balance += amount
        print("Deposit successful")

    def info(self):
        print(f"Account Holder Name: {self.user.name} {self.user.last_name}")
        print(f"Account Type: {self.account_type}\nCreated At: {self.created_at}\nBalance: {self.balance}")

class Bank:
    def __init__(self):
        self.users = []
        self.accounts = []
        self.mydb = sqlite3.connect('Abol_bank.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.mydb.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           last_name TEXT,
                           f_name TEXT,
                           birth_date TEXT,
                           city TEXT,
                           mobile TEXT,
                           code_mile TEXT,
                           phone TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                          (account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER,
                           account_type TEXT,
                           created_at TEXT,
                           balance INTEGER,
                           FOREIGN KEY(user_id) REFERENCES users(user_id))''')
        self.mydb.commit()

    # تعریف کاربر جدید و ذخیره در پایگاه داده
    def create_user(self, name, last_name, f_name, birth_date, city, mobile, code_mile, phone=None):
        cursor = self.mydb.cursor()
        sql = "INSERT INTO users (name, last_name, f_name, birth_date, city, mobile, code_mile, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        val = (name, last_name, f_name, birth_date, city, mobile, code_mile, phone)
        cursor.execute(sql, val)
        self.mydb.commit()
        user_id = cursor.lastrowid
        user = User(name, last_name, f_name, birth_date, city, mobile, code_mile, phone, user_id)
        self.users.append(user)
        return user

    # تعریف حساب جدید و ذخیره در پایگاه داده
    def create_account(self, user, account_type):
        cursor = self.mydb.cursor()
        sql = "INSERT INTO accounts (user_id, account_type,created_at, balance) VALUES (?, ?, ?, ?)"
        val = (user.user_id, account_type, datetime.now(), 0)
        cursor.execute(sql, val)
        self.mydb.commit()
        account_id = cursor.lastrowid
        account = Account(user, account_type, account_id)
        self.accounts.append(account)
        return account

    # جستجوی کاربر با استفاده از کدملی
    def search_user_by_code_mile(self, code_mile):
        for user in self.users:
            if user.code_mile == code_mile:
                return user
        return None

    # جستجوی حساب با استفاده از شماره حساب
    def search_account_by_id(self, account_id):
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        return None

    # ورود به سیستم مدیریت بانک
    def admin_login(self, username, password):
        if username == "Admin" and password == "admin":
            return True
        else:
            return False

    # نمایش جزئیات کاربر و حساب‌هایش
    def show_user_details(self, user):
        user.info()
        for account in self.accounts:
            if account.user == user:
                account.info()

    # محاسبه موجودی کل بانک
    def total_balance(self):
        total = 0
        for account in self.accounts:
            total += account.balance
        return total
    
    def show_all_users_and_accounts(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        for user in users:
            user_id, name, last_name, f_name, birth_date, city, mobile, code_mile, phone = user
            user_obj = User(name, last_name, f_name, birth_date, city, mobile, code_mile, phone, user_id)
            self.users.append(user_obj)

        for acc in accounts:
            account_id, user_id, account_type, created_at, balance = acc
            user_obj = self.search_user_by_id(user_id)
            account_obj = Account(user_obj, account_type, account_id)
            account_obj.balance = balance
            self.accounts.append(account_obj)

        for user in self.users:
            user.info()
            for account in self.accounts:
                if account.user.user_id == user.user_id:
                    account.info()
    
bank = Bank()
admin = None
while True:
        print("1. Admin Login")
        print("2. Create Account")
        print("3. Search User")
        print("4. Search Account")
        print("5. Show Total Balance")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if bank.admin_login(username, password):
                print("Admin login successful")
                print("1. Show users and accounts")
                print("2. Bank Total")
                print("3. Exit")
                admin = True
                user_input = input("ADMIN> ")
                if user_input == "1":
                    bank.show_all_users_and_accounts()
                elif user_input == "2":
                    print(f"All Balance in bank is {bank.total_balance()}")
                else:
                    print("Thanks for be with us")
                    exit()

            else:
                print("Invalid username or password")
        elif choice == "2":
            name = input("Enter name: ")
            last_name = input("Enter last name: ")
            f_name = input("Enter father name: ")
            birth_date = input("Enter birth date (YYYY-MM-DD): ")
            city = input("Enter city: ")
            mobile = input("Enter mobile number: ")
            code_mile = input("Enter national ID: ")
            phone = input("Enter phone number (optional): ")
            user = bank.create_user(name, last_name, f_name, birth_date, city, mobile, code_mile, phone)
            account_type = input("Enter account type: ")
            account = bank.create_account(user, account_type)
            print(f"Account created successfully. Account ID: {account.account_id}")
        elif choice == "3":
            if admin:
                code_mile = input("Enter national ID: ")
                user = bank.search_user_by_code_mile(code_mile)
                if user:
                    bank.show_user_details(user)
                else:
                    print("User not found")
            else:
                print("Admin login required")
        elif choice == "4":
            if admin:
                account_id = int(input("Enter account ID: "))
                account = bank.search_account_by_id(account_id)
                if account:
                    account.info()
                else:
                    print("Account not found")
            else:
                print("Admin login required")
        elif choice == "5":
            if admin:
                total_balance = bank.total_balance()
                print(f"Total balance: {total_balance}")
            else:
                print("Admin login required")
        elif choice == "6":
            break
        else:
            print("Invalid choice")