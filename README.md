# Financial Fraud Risk Detection System

---

## Project Overview

This project develops a **Financial Fraud Risk Detection System** using **SQL and Machine Learning** to identify potentially fraudulent financial transactions.

Financial fraud detection is a critical problem for banks and financial institutions. The objective of this project is to analyze historical transaction data stored in a SQL database and build a machine learning model capable of detecting fraudulent activities.

The project demonstrates a complete **end-to-end data science workflow**, including:

* Data storage using SQL
* Data extraction and preprocessing using Python
* Exploratory Data Analysis (EDA)
* Handling imbalanced datasets
* Machine learning model training and evaluation
* Fraud risk prediction

The final system uses a **Random Forest Classifier** to identify suspicious transactions.

---

## Dataset

This project uses the **Credit Card Fraud Detection Dataset**, which contains real-world anonymized financial transaction data.

Dataset characteristics:

* **284,807 total transactions**
* **492 fraudulent transactions**
* Highly **imbalanced dataset**
* Features include anonymized variables (`V1` to `V28`) along with:

  * Transaction Time
  * Transaction Amount
  * Transaction Class

Transaction class values:

* **0 → Normal transaction**
* **1 → Fraudulent transaction**

**Note:**
The dataset is relatively large and therefore **not included in this repository**.

You can download the dataset from Kaggle:

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

After downloading, place the dataset in the following directory:

```
data/creditcard.csv
```

---

## Technologies Used

* **Python**
* **SQL (SQLite)**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Seaborn**
* **Scikit-learn**
* **Imbalanced-learn (SMOTE)**
* **Jupyter Notebook**
* **Git & GitHub**

---

## Project Structure

```
financial-fraud-risk-detection
│
├── data
│   └── creditcard.csv
│
├── database
│   └── fraud_detection.db
│
├── images
│   ├── fraud_vs_normal.png
│   ├── transaction_amount_distribution.png
│   ├── fraud_vs_amount.png
│   ├── confusion_matrix.png
│   └── roc_curve.png
│
├── models
│   └── fraud_model.pkl
│
├── notebook
│   └── fraud_analysis.ipynb
│
├── sql
│   └── queries.sql
│
├── src
│   ├── create_database.py
│   ├── load_from_sql.py
│   ├── train_model.py
│   └── predict_transaction.py
│
├── requirements.txt
│
└── README.md
```

---

## Data Storage Using SQL

The dataset is first stored in a **SQLite database**, simulating how financial institutions store transaction records in production environments.

Example SQL queries used in this project include:

* Total number of transactions
* Fraud vs normal transaction counts
* Average transaction amount
* Fraud transaction statistics
* Highest transaction values

These queries help analyze transaction patterns directly from the database.

---

## Data Preprocessing

The following preprocessing steps were performed:

* Loaded transaction data from SQL into Python
* Checked for missing values
* Standardized features using **StandardScaler**
* Split the dataset into **training and testing sets**
* Addressed class imbalance using **SMOTE (Synthetic Minority Oversampling Technique)**

Handling class imbalance is essential because fraud transactions represent only a small fraction of the dataset.

---

## Machine Learning Models

Two models were trained and evaluated:

### Logistic Regression

Used as a baseline model to understand linear relationships between features and fraud detection.

### Random Forest Classifier

An ensemble learning method that builds multiple decision trees and combines their predictions.
This model performs better for complex datasets with non-linear relationships.

After evaluation, **Random Forest was selected as the final model** due to superior performance in detecting fraudulent transactions.

---

## Model Evaluation

Model performance was evaluated using the following metrics:

* **Precision**
* **Recall**
* **F1 Score**
* **Confusion Matrix**
* **ROC Curve**
* **ROC-AUC Score**

These metrics provide a comprehensive evaluation of the model's ability to correctly identify fraudulent transactions while minimizing false positives.

---

## Visualizations

The project includes multiple visualizations to better understand transaction behavior and model performance:

* Fraud vs Normal Transaction Distribution
* Transaction Amount Distribution
* Fraud vs Transaction Amount Comparison
* Confusion Matrix
* ROC Curve

These visualizations help interpret both the dataset and the machine learning model's effectiveness.

---

## How to Run the Project

Clone the repository:

```
git clone https://github.com/diutimaya/financial-fraud-risk-detection.git
```

Navigate to the project directory:

```
cd financial-fraud-risk-detection
```

Install required dependencies:

```
pip install -r requirements.txt
```

Create the database:

```
python src/create_database.py
```

Train the fraud detection model:

```
python src/train_model.py
```

For a detailed step-by-step analysis, open the notebook:

```
notebook/fraud_analysis.ipynb
```

---

## Future Improvements

Potential improvements for this project include:

* Implementing advanced models such as **XGBoost or LightGBM**
* Building a **real-time fraud detection system**
* Integrating streaming transaction data
* Deploying the model as an **API or analytics dashboard**
* Performing advanced **feature engineering**

---

## Author

**Diutimaya Mohanty**
B.Tech Student — Data Science Specialization
