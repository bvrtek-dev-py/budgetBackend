# Home Budget Management

Manage your home budget efficiently with this Python-based application powered by FastAPI and MySQL.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#main-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Launching the project](#launching-the-project)


## Project Overview

Home Budget Management is a web application designed to help users track and manage their household expenses. Users can create accounts, manage multiple wallets, and categorize spendings based on different criteria such as categories and time periods.

## Main Features

1. **User Accounts:**
   - Users can create accounts to personalize their budget management experience.

2. **Multiple Wallets:**
   - Each user can have multiple wallets to organize and track expenses separately.

3. **Group Spendings:**
   - Users can categorize their spendings to gain insights into where their money is going.

4. **Time-based Tracking:**
   - Spendings can be grouped based on different periods of time, providing a historical view of expenses.

5. **Wallet Statistics:**
   - Users can view detailed statistics for each of their wallets, including the total balance, spending patterns, and income trends
   
## Tech Stack

- Python 3.11.5
- FastAPI
- MySQL

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.11.5
- MySQL 8.0

### Launching the Project

#### Step 1: Clone the Repository

```bash
git clone https://github.com/bvrtek-dev-py/budgetBackend
```

#### Step 2: Copy variables from .env.example to .env

```
DB_ROOT_PASSWORD=enter-variable
DB_USER=enter-variable
DB_PASSWORD=enter-variable
DB_HOST=enter-variable
DB_PORT=enter-variable
DB_NAME=enter-variable

SECRET_KEY=test-secret-key (paste generated key)
REFRESH_TOKEN_SECRET_KEY=test-refresh-secret-key (paste generated key)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Step 3: Set database .env variables to database properties from Dockerfile
```
DB_ROOT_PASSWORD=root_password
DB_USER=my_user
DB_PASSWORD=my_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=my_database
```


#### Step 4: Open terminal in backend directory

```bash
cd backend
```

#### Step 5: Install dependencies

```bash
poetry install
```

#### Step 6: Open Docker Desktop application


#### Step 7: Jump to docker dir and build container

```bash
cd docker
```

```bash
docker-compose up -d
```

#### Step 8: Go back to backend and run migrations

```bash
cd ..
```

```bash
alembic upgrade head
```

#### Step 9. Run main.py file

#### Step 10. Open web browser on 127.0.0.1/docs

![obraz](https://github.com/bvrtek-dev-py/budgetBackend/assets/112180048/0f6a61df-e1a1-4cea-b1c8-9c49bd639faa)

