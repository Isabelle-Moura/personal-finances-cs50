# 🌐 Language / Idioma

As this project is intended for a global audience, I've strive for documentation accessibility. The primary file is in English, but a complete localized version is available for Portuguese speakers.

**🇺🇸 English:** This is the main documentation file.  
**🇧🇷 Português:** Este projeto possui documentação completa em português. Clique [aqui](README_pt-br.md) para acessar o `README_pt-br.md`.

---

# 💻 Development Environment Setup

To ensure portability and avoid dependency conflicts, this project uses a Python virtual environment. Follow the steps below to set up your development environment.

## Step 1: Create and Activate the Virtual Environment

Navigate to the project root directory and create the virtual environment by running the following command:

```json
python -m venv venv
```

Then activate it with the appropriate command for your operating system:

**For macOS/Linux:**

```json
source venv/bin/activate
```

**For Windows:**

----> **Command Prompt:**

```json
venv\Scripts\activate
```

----> **PowerShell:**

```json
.\venv\Scripts\activate
```

_If you are using Git Bash or another Linux-style terminal on Windows, use the command for macOS/Linux._

---

## Step 2: Install Dependencies

With the virtual environment activated, install all necessary libraries listed in the `requirements.txt` file using `pip`.

```json
pip install -r requirements.txt
```

After that, you will need to install the front-end dependencies, found in the `package.json` file, using the following command:

```json
npm install
```

That's it. The development environment is now configured and ready to use.

---

## Step 3: Initializing the Database

Before starting the application, you must configure the database. This project uses PostgreSQL and Flask CLI to create tables from Python models.

#### Prerequisites:

- Ensure that the `PostgreSQL` server is running.
- Ensure that the database (the name defined in `DATABASE_URL` in your `.env` file) has already been created in your PostgreSQL.

### 3.1 Creating the Local Database (PostgreSQL):

If you do not have the main database created, follow these instructions in your terminal.

- **Step by Step via Terminal**:

---> **Access the PostgreSQL Terminal (psql)**:

```json
psql -U postgres
```

The system will ask for your postgres user password.

---> **Create the Database**:

```json
CREATE DATABASE finance_db;
```

---> **Create the Database User (Optional, but Recommended)**:

```json
CREATE USER your_username WITH PASSWORD ‘your_secret_password’;
```

---> **Grant Essential Permissions to the User**:

These commands are crucial to allow the user to create tables and sequences in the `public` schema.

---- **1. Basic permission to connect and use the database:**

```json
GRANT ALL PRIVILEGES ON DATABASE finance_db TO your_username;
```

---- **2. Connect to the new database to grant schema permissions:**

```json
\c finance_db;
```

---- **3. Permission to create tables in the default ‘public’ schema:**

```json
GRANT ALL ON SCHEMA public TO your_username;
```

---- **4. Ensures that any TABLE or SEQUENCE created in the FUTURE in this schema also belongs to this user:**

```json
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_username;
```

Replace `your_username` with the actual user that is in your `.env`.

---> **Exit psql**:

```json
\q
```

- **Final Adjustment in .env**:

After creating the user and database, make sure your `.env` file uses exactly these values.

---- **Example of how it should look after creation:**

```json
DATABASE_URL=‘postgresql://your_username:your_secret_password@localhost:5432/finance_db’
```

With the database created and the .env adjusted, your backend is ready to connect!

### 3.2 Steps to Create Tables

Follow these steps in your project root directory:

- **Activate the Virtual Environment (venv)**:

It is crucial that the virtual environment is active for the flask command to work correctly. If you have not activated it yet, check `Step 1: Create and Activate the Virtual Environment`.

- **Execute the Creation Command**:

Run the `flask create-tables` command that was configured in the `create_db.py` file.

```json
flask create-tables
```

The system will connect to PostgreSQL and create the tables `User, Transaction, Category`, and `Budget`.

- **Option: Clear and Recreate Tables:**

If you need to delete all data and recreate the tables from scratch (useful during development and testing), use the `--drop` flag:

```json
flask create-tables --drop
```

WARNING: This command will **IRREVERSIBLY DELETE** all existing data in the tables. _Use with caution!_

---
