# hclTech_teamFalcon
# 🧾 Retail Sales Data Validation Pipeline

## 📌 Overview
This project implements an **end-to-end data validation and reconciliation pipeline** for retail sales data received from multiple source systems such as POS terminals and web orders.

The pipeline ensures that **only clean, accurate, and reliable data** is stored in production tables, while invalid data is quarantined for audit and correction.

---

## 📂 Input Data
The pipeline processes two raw CSV files:

- **sales_header.csv** – Transaction-level information  
- **sales_line_items.csv** – Item-level purchase details  

These files may contain:
- Invalid IDs  
- Incorrect amounts  
- Bad date formats  
- Inconsistent totals  

---

## 🏗️ Pipeline Stages

### 1️⃣ Data Ingestion
- CSV files are read using **Pandas**
- Initial profiling is performed
- Data is loaded into memory as DataFrames

---

### 2️⃣ Raw Staging Layer
- Data is stored in raw database tables:
  - `raw_sales_header`
  - `raw_sales_line_items`
- All fields are stored as strings
- Purpose: preserve original data for auditing

---

### 3️⃣ Reference Data Loading
Validation reference data is loaded:
- Valid store IDs
- Valid product IDs
- Valid customer IDs
- Valid promotion IDs

---

### 4️⃣ Header-Level Validation
Each transaction is validated using business rules:
- Store ID validity
- Customer ID validity
- Total amount > 0
- Valid date format and range
- Data type checks

Validation results:
- `is_valid` flag
- `validation_errors` description

---

### 5️⃣ Line Item Validation
Each line item is checked for:
- Valid product ID
- Quantity > 0
- Non-negative amount
- Valid promotion ID (if present)

---

### 6️⃣ Cross-Validation (Reconciliation)
- Transaction total is compared with the sum of line items
- Mismatches are marked invalid
- Helps detect data entry and system calculation errors

---

### 7️⃣ Data Classification
Data is split into:
- **Clean data** – ready for production
- **Invalid data** – moved to quarantine

---

### 8️⃣ Data Type Conversion
Clean records are converted to proper data types:
- Dates → DateTime
- Amounts → Decimal
- Quantities → Integer

---

### 9️⃣ Production Tables
Clean data is inserted into:
- `store_sales_header`
- `store_sales_line_items`

The database enforces:
- Foreign key constraints
- NOT NULL checks
- Data type integrity

---

### 🔟 Quarantine Invalid Data
Invalid records are stored with:
- Original record (JSON format)
- Validation error messages
- Timestamp

Purpose:
- Audit trail
- Root cause analysis
- Source system correction

---

### 1️⃣1️⃣ Reporting & Logging
A summary report is generated:
- Total records processed
- Valid vs invalid counts
- Error-wise breakdown
- Processing time

---

## 📊 Sample Output
- Total records received: **1000**
- Valid records: **950 (95%)**
- Invalid records: **50 (5%)**
- Processing time: **~2.3 seconds**

---

## 🛠️ Technologies Used
- Python  
- Pandas  
- SQL (Relational Database)  

---

## 🎯 Business Value
- Improves data quality and trust  
- Prevents incorrect revenue reporting  
- Enables reliable analytics and decision-making  
- Provides full auditability of invalid data  
<img width="2914" height="1627" alt="image" src="https://github.com/user-attachments/assets/11c2c760-f0b6-49ae-a607-1d1c2efa18ec" />

---

## 🚀 Future Enhancements
- Rule configuration using YAML/JSON
- Parallel processing for large datasets
- Data quality dashboard
- Automated alerts for high error rates
