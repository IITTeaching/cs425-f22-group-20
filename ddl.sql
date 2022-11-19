CREATE TABLE Branch (
  branchID UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  address VARCHAR(255) NOT NULL,
  overdraftFee FLOAT,
  monthlyFee FLOAT,
  waiveFeeMin FLOAT
);

CREATE TYPE EMP_ROLES AS ENUM ('teller', 'loan specialist', 'manager');

CREATE TABLE Employee (
  ssn TEXT NOT NULL PRIMARY KEY,
  emp_name TEXT NOT NULL,
  address TEXT NOT NULL,
  salary FLOAT,
  emp_role EMP_ROLES NOT NULL,
  branch UUID references Branch(branchID)
);

CREATE TYPE ACCESS_TYPE AS ENUM ('checking', 'savings');
CREATE TYPE OVERDRAFT_TYPE AS ENUM ('regular', 'reject', 'charge');

CREATE TABLE Account (
  accountNumber UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  balance FLOAT,
  accessType ACCESS_TYPE,
  overdraftType OVERDRAFT_TYPE,
  hasMonthlyFee BOOLEAN,
  disallowNegativeBalance BOOLEAN,
  interestRate FLOAT,
  CONSTRAINT CHK_balance CHECK (balance > 0 OR NOT disallowNegativeBalance) 
);

CREATE TABLE Customer (
  ssn TEXT NOT NULL PRIMARY KEY,
  accountNumber UUID NOT NULL UNIQUE,
  FOREIGN KEY (accountNumber) REFERENCES Account,
  emp_name TEXT NOT NULL,
  address TEXT NOT NULL,
  branch UUID references Branch(branchID)
);

CREATE TYPE TRANSACTION_TYPE AS ENUM ('deposit', 'withdrawal', 'transfer', 'external transfer');

CREATE TABLE Transaction (
  transactionID UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  transactionType TRANSACTION_TYPE,
  amount FLOAT NOT NULL,
  transactionDate DATE NOT NULL,
  description TEXT,
  accountFrom UUID NOT NULL UNIQUE,
  FOREIGN KEY (accountFrom) REFERENCES Account,
  accountTo UUID NOT NULL UNIQUE,
  FOREIGN KEY (accountTo) REFERENCES Account
);
