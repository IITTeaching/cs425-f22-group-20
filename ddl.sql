
CREATE TABLE Branch (
  branchID UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  address VARCHAR(255) NOT NULL,
  overdraftFee DECIMAL(20,4),
  monthlyFee DECIMAL(20,4),
  waiveFeeMin DECIMAL(20,4)
);

CREATE TYPE EMP_ROLES AS ENUM ('teller', 'loan specialist', 'manager');

CREATE TABLE Employee (
  ssn TEXT NOT NULL PRIMARY KEY,
  emp_name TEXT NOT NULL,
  address TEXT NOT NULL,
  salary DECIMAL(20,4),
  emp_role EMP_ROLES NOT NULL,
  branch UUID REFERENCES Branch(branchID)
);

CREATE TYPE ACCESS_TYPE AS ENUM ('checking', 'savings');
CREATE TYPE OVERDRAFT_TYPE AS ENUM ('regular', 'reject', 'charge');

CREATE TABLE Account (
  accountNumber UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  balance DECIMAL(20,4),
  accessType ACCESS_TYPE,
  overdraftType OVERDRAFT_TYPE,
  hasMonthlyFee BOOLEAN,
  interestRate DECIMAL(20,4),
  CONSTRAINT CHK_balance CHECK (balance > 0 OR NOT overdraftType = 'reject') 
);

CREATE TABLE Customer (
  customerID UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  emp_name TEXT NOT NULL,
  address TEXT NOT NULL,
  branch UUID REFERENCES Branch(branchID)
);

CREATE TABLE Holds (
    customerID UUID REFERENCES Customer,
    accountNumber UUID REFERENCES Account,
    PRIMARY KEY (customerID, accountNumber)
);

CREATE TYPE TRANSACTION_TYPE AS ENUM ('deposit', 'withdrawal', 'transfer', 'external transfer');

CREATE TABLE Transaction (
  transactionID UUID DEFAULT (gen_random_uuid()) NOT NULL PRIMARY KEY UNIQUE,
  transactionType TRANSACTION_TYPE,
  amount DECIMAL(20,4) NOT NULL,
  transactionDate DATE NOT NULL,
  description TEXT,
  accountFrom UUID NOT NULL UNIQUE,
  FOREIGN KEY (accountFrom) REFERENCES Account,
  accountTo UUID NOT NULL UNIQUE,
  FOREIGN KEY (accountTo) REFERENCES Account
);