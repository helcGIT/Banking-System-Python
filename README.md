# Banking System Python

This is a CLI (Command Line Interface) CRUD (Create, Read, Update, Delete) program written in Python that simulates a banking system. It allows users to create, read, update, delete, deposit and withdraw money. All passwords are hashed, even the admin has no access to users' passwords, reinforcing top-tier security standards. All users information are storaged in JSON file, included passwords (hashed passwords with generate_has_password() function from werkzeug.security library) The program uses libraries such as `re`, `string`, `random`, `werkzeug.security`, and `json`.

## Features

- Create a new bank account
- View accounts details
- Deposit money
- Withdraw money
- Update password
- Delete an account
- Sort by balance

## Requirements

- Python 3.x
- `werkzeug` library

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/helcGIT/Banking-System-Python.git
   cd Banking-System-Python
   ```

2. Install the required libraries:
   ```bash
   pip install werkzeug
   ```

## Usage

To run the program, use the following command:
```bash
python bank_account_cli.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.