from random import randint
from string import punctuation
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash


class BankAccount:
    all_bank_accounts = []
    JSON_FILE = "accounts.json"

    def __init__(self, user_name: str, user_surname: str, user_age: int, phone_number: str, balance: float,
                 password: str, card_number: str = None) -> None:
        self.__user_name = user_name
        self.__user_surname = user_surname
        self.__user_age = user_age
        self.__phone_number = phone_number
        self.__balance = balance
        self.__password = password
        self.__card_number = card_number if card_number else self.generate_card_number()
        BankAccount.all_bank_accounts.append(self)

    def __repr__(self) -> str:
        return (f"[{type(self).__name__}('{self.__card_number}'), ('{self.__user_name} {self.__user_surname}'), "
                f"({self.__user_age}yo), ('{self.__phone_number}'), ({self.__balance:,.2f}$)]")

    def __str__(self) -> str:
        return (f"Credit card number: {self.__card_number}\n"
                f"Card holder: {self.__user_name} {self.__user_name}\n"
                f"Card holder age: {self.__user_age}yo\n"
                f"Balance: {self.__balance:,.2f}$")

    @classmethod
    def load_accounts(cls):
        try:
            with open(cls.JSON_FILE, "r") as file:
                data = json.load(file)
                cls.all_bank_accounts = [cls(**account) for account in data]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.all_bank_accounts = []

    @classmethod
    def save_accounts(cls):
        data = [
            {
                "user_name": account.user_name,
                "user_surname": account.user_surname,
                "user_age": account.age,
                "phone_number": account.phone_number,
                "balance": account.balance,
                "password": account.password,
                "card_number": account.card_number
            }
            for account in cls.all_bank_accounts
        ]

        with open(cls.JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def generate_card_number() -> str:
        return "-".join(str(randint(1000, 9999)) for _ in range(4))

    @property
    def card_number(self) -> str:
        return self.__card_number

    @classmethod
    def list_all_bank_accounts(cls) -> None:
        if not cls.all_bank_accounts:
            print("Cannot list, no accounts have been created yet\n")
            return

        print(f"Number of created bank accounts: {len(cls.all_bank_accounts)}")
        for i, bank_user in enumerate(cls.all_bank_accounts, 1):
            print(f"{i}. {repr(bank_user)}")

    @property
    def user_name(self) -> str:
        return self.__user_name

    @staticmethod
    def validate_user_name(user_name: str) -> str:
        if not user_name:
            raise ValueError("Error! Name cannot be empty.")
        if not user_name.isalpha():
            raise ValueError("Error! Name must contain only letters.")
        if not 2 <= len(user_name) <= 12:
            raise ValueError("Error! Name must contain between 2 and 12 characters.")

        return user_name.capitalize()

    @property
    def user_surname(self) -> str:
        return self.__user_surname

    @staticmethod
    def validate_user_surname(user_surname: str) -> str:
        if not user_surname:
            raise ValueError("Error! Surname cannot be empty.")
        if not user_surname.isalpha():
            raise ValueError("Error! Surname must contain only letters.")
        if not 2 <= len(user_surname) <= 12:
            raise ValueError("Error! Surname must contain between 2 and 12 characters.")

        return user_surname.capitalize()

    @property
    def age(self) -> int:
        return self.__user_age

    @staticmethod
    def validate_age(age: str) -> int:
        if not age:
            raise ValueError("Error! Age cannot be empty.")
        if not age.isdigit():
            raise ValueError("Error! Age must be a valid integer.")
        age = int(age)
        if not 18 <= age <= 50:
            raise ValueError("Error! Age must be between 18 and 50")

        return age

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @classmethod
    def validate_phone_number(cls, phone_number):
        if not re.fullmatch(r"\+49\d{10}", phone_number):
            raise ValueError("Error! Phone number must start with +49 and have exactly 10 digits after it.")

        return phone_number

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, new_balance: float | int) -> None:
        self.__balance = float(new_balance)

    @staticmethod
    def validate_balance(balance: str) -> float:
        if balance is None:
            raise ValueError("Error! Balance cannot be empty.")
        balance = float(balance)
        if balance < 0:
            raise ValueError("Error! Balance cannot be less than 0$.")
        if balance > 100000000:
            raise ValueError("Error! Balance cannot be more than 100,000,000.00$.")

        return balance

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str) -> None:
        self.__password = new_password

    @staticmethod
    def validate_password(password: str) -> str:
        if (len(password) < 8 or
                not any(c.isdigit() for c in password) or
                not any(c.isalpha() for c in password) or
                not any(c in punctuation for c in password)):
            raise ValueError("Error! Password must contain >= 8 characters (min 1 digit, alpha and special char)")

        return password

    @classmethod
    def login(cls) -> "BankAccount | None":
        max_attempt = 5
        if not cls.all_bank_accounts:
            print("No accounts have been created yet.")
            return

        while True:
            card_number_entry = input("Enter your credit card number: ")
            found_account = next((i for i in cls.all_bank_accounts if i.card_number == card_number_entry), None)
            if found_account is None:
                print("Error! Card number don't exist in our system.")
            else:
                for _ in range(max_attempt):
                    password_input = input("Enter your password: ")
                    if check_password_hash(found_account.password, password_input):
                        print(f"Successfully logged in as {found_account.user_name} {found_account.user_surname}")
                        return found_account
                    else:
                        max_attempt -= 1
                        if max_attempt > 0:
                            print(f"Wrong password. You can try {max_attempt} more times.")
                        else:
                            print("Too many failed attempts... Try again later.")
                            return

    @staticmethod
    def validate_transaction(money: str) -> float:
        if money is None:
            raise ValueError("Error! Transaction cannot be empty.")
        if not money.isdigit():
            raise ValueError("Error! Please enter valid transaction.")
        money = float(money)
        if money < 1:
            raise ValueError("Error! Transaction cannot be less then 1$.")
        if money > 10000:
            raise ValueError("Error! Transaction cannot be more than 10,000.00$")

        return money

    @classmethod
    def deposit_money(cls) -> None:
        found_account = cls.login()
        if not found_account:
            print("Cannot deposit.\n")
            return
        while True:
            try:
                money_to_deposit = input("How much money would you like to deposit into your account?: ")
                money_to_deposit = cls.validate_transaction(money_to_deposit)
                found_account.balance += money_to_deposit
                cls.save_accounts()
                print("Successfully deposited!")
                return
            except ValueError as e:
                print(e)

    @classmethod
    def withdraw_money(cls) -> None:
        found_account = cls.login()
        if not found_account:
            print("Cannot withdraw.\n")
            return
        while True:
            try:
                money_to_withdraw = input("How much money would you like to withdraw into your account?: ")
                money_to_withdraw = cls.validate_transaction(money_to_withdraw)
                found_account.balance -= money_to_withdraw
                cls.save_accounts()
                print("Successfully withdrew")
                return
            except ValueError as e:
                print(e)

    @classmethod
    def update_password(cls) -> None:
        found_account = cls.login()
        if not found_account:
            print("Cannot update password.\n")
            return
        while True:
            try:
                new_password = input("Enter new password: ")
                if not check_password_hash(found_account.password, new_password):
                    new_password = cls.validate_password(new_password)
                    new_password_confirm = input("Confirm new password: ")
                    if new_password_confirm == new_password:
                        new_hashed_password = generate_password_hash(new_password)
                        found_account.password = new_hashed_password
                        print("Passwords successfully updated!")
                        cls.save_accounts()
                        return
                    else:
                        print("Error! Passwords don't match.")
                else:
                    print("Error! Cannot set old password as new.")
            except ValueError as e:
                print(e)

    @classmethod
    def delete_account(cls) -> None:
        found_account = cls.login()
        if not found_account:
            print("Cannot delete.\n")
            return
        max_attempts = 3
        while True:
            query = input("Do you want to delete your account (y/n): ")
            if query.lower() in ("y", "yes"):
                for _ in range(max_attempts):
                    confirm_password = input("Confirm your password: ")
                    if check_password_hash(found_account.password, confirm_password):
                        while True:
                            query_confirm = input("Are you sure (YES)?: ")
                            if query_confirm == "YES":
                                print("Your account has been successfully deleted.")
                                cls.all_bank_accounts.remove(found_account)
                                cls.save_accounts()
                                return
                            elif query_confirm.lower() in ("n", "no", "cancel"):
                                print("Deleting account canceled.")
                                return
                            else:
                                print("Wrong option.")
                    else:
                        max_attempts -= 1
                        if max_attempts > 0:
                            print(f"Wrong password. You can try {max_attempts} more times.")
                        else:
                            print("Too many failed attempts...Try again later.")
                            return
            elif query.lower() in ("n", "no"):
                print("Ok, bye.")
                return
            else:
                print("Wrong option.")

    @classmethod
    def sort_by_balance(cls) -> None:
        if not cls.all_bank_accounts:
            print("No accounts have been created yet.\nCannot sort.\n")
            return

        while True:
            print("1. High to low")
            print("2. Low to high")
            option = input("Chose: ")
            match option:
                case '1':
                    high_to_low = sorted(cls.all_bank_accounts, key=lambda account: account.balance, reverse=True)
                    for i, bank_account in enumerate(high_to_low, 1):
                        print(f"{i}. {repr(bank_account)}")
                    return
                case '2':
                    low_to_high = sorted(cls.all_bank_accounts, key=lambda account: account.balance, reverse=False)
                    for i, bank_account in enumerate(low_to_high, 1):
                        print(f"{i}. {repr(bank_account)}")
                    return
                case _:
                    print("Wrong option.")

    @classmethod
    def create_bank_account(cls) -> "BankAccount":
        print("Creating new bank account...")
        while True:
            try:
                name = input("Enter your name: ")
                name = cls.validate_user_name(name)
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                surname = input("Enter your surname: ")
                surname = cls.validate_user_surname(surname)
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                age = input("Enter your age: ")
                age = cls.validate_age(age)
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                phone_number = input("Enter your phone number: ")
                existing_phone_number = next((i for i in cls.all_bank_accounts if i.phone_number == phone_number), None)
                if existing_phone_number:
                    raise ValueError("Error! That phone number already exist.")
                phone_number = cls.validate_phone_number(phone_number)
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                balance = input("Enter your balance: ")
                balance = cls.validate_balance(balance)
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                password = input("Enter your password: ")
                password = cls.validate_password(password)
                hashed_password = generate_password_hash(password)
                print(hashed_password)
                break
            except ValueError as e:
                print(e)

        while True:
            password_confirm = input("Confirm password: ")
            if password_confirm == password:
                break
            else:
                print("Passwords don't match.")

        new_account = cls(name, surname, age, phone_number, balance, hashed_password)
        cls.save_accounts()
        print("Congratulations! You have created bank account.")
        print(f"Your card number is {new_account.card_number}")

        return new_account


def main() -> None:
    BankAccount.load_accounts()
    while True:
        print("1. Create new bank account")
        print("2. List all bank accounts")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Update password")
        print("6. Delete bank account")
        print("7. Sort by balance")
        print("8. Exit")

        option = input("Enter one option: ")
        match option:
            case '1':
                BankAccount.create_bank_account()
            case '2':
                BankAccount.list_all_bank_accounts()
            case '3':
                BankAccount.deposit_money()
            case '4':
                BankAccount.withdraw_money()
            case '5':
                BankAccount.update_password()
            case '6':
                BankAccount.delete_account()
            case '7':
                BankAccount.sort_by_balance()
            case '8':
                print("Goodbye")
                exit()
            case _:
                print("Wrong option, try again.\n")


if __name__ == "__main__":
    main()
