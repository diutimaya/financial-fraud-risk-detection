-- Total Trasanctions

SELECT COUNT(*) FROM transactions;

--  Fraud vs Normal Transactions

SELECT Class, COUNT(*) 
FROM transactions
GROUP BY Class;

--  Average Transaction amount

SELECT AVG(Amount) 
FROM transactions;

-- Fraud transactions average amount

SELECT AVG(Amount)
FROM transactions
WHERE Class = 1;

-- Top 10 highest transactions

SELECT *
FROM transactions
ORDER BY Amount DESC
LIMIT 10;

