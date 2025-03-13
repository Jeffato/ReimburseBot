CREATE TYPE approval_status AS ENUM ('Under-Review', 'Pending-Reimbursement', 'Approved', 'Rejected');

-- TODO: figure out if there is a Way for user to interact with category enums?
-- Note: category types just for reference + testing
CREATE TYPE budget_category AS ENUM ('Social', 'Fundraising', 'Cats');

CREATE TABLE ledger (
    id SERIAL PRIMARY KEY,
    category budget_category NOT NULL,
    requestor TEXT NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    date_purchase DATE NOT NULL,    
    description TEXT,
    submit_time TIMESTAMP DEFAULT NOW()
    approval_time TIMESTAMP,
    reimburse_time TIMESTAMP,
    approval_status approval_status DEFAULT 'Under-Review',
    image_url TEXT
);