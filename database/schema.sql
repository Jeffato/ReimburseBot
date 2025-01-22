CREATE TABLE approval_queue (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    requestor TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    date_purchase DATE NOT NULL,
    description TEXT,
    submit_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE receipts (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    requestor TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    date_purchase DATE NOT NULL,
    description TEXT,
    submit_time TIMESTAMP DEFAULT NOW()
);