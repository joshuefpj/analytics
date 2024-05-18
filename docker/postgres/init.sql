CREATE TABLE account_details (
    account VARCHAR(255) NOT NULL,
    first_name VARCHAR(79) NOT NULL,
    last_name VARCHAR(79),
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (account)
);

CREATE TABLE transaction_logs (
    id serial, num integer, data varchar,
    log_date TIMESTAMP,
    account VARCHAR(255),
    debit FLOAT,
    credit FLOAT,
    transactions_count INT,
    PRIMARY KEY (id),
    FOREIGN KEY (account) REFERENCES account_details(account)
);