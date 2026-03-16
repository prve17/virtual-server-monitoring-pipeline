# Virtual Server Monitoring & Performance Optimization

This project demonstrates an end-to-end **data engineering pipeline** to monitor the performance of virtual servers.  
The pipeline ingests server logs, processes them, stores the results in a cloud database, and visualizes insights using a Power BI dashboard.

The goal of the project is to help identify performance issues such as high CPU usage, memory pressure, or unusual network traffic.

---

## Architecture

The solution follows a simple data pipeline architecture:

Server Logs (CSV)  
↓  
Azure Blob Storage  
↓  
Python ETL Pipeline  
↓  
Azure SQL Database  
↓  
Power BI Dashboard  

<img src="https://github.com/prve17/virtual-server-monitoring-pipeline/blob/main/Architecture.png">

---

## Technologies Used

- **Azure Blob Storage** – storing raw server log files  
- **Python (Pandas)** – data ingestion and transformation  
- **Azure SQL Database** – storing processed monitoring metrics  
- **Power BI** – building the monitoring dashboard  
- **GitHub** – version control and project sharing  

---

## Data Pipeline

### 1. Data Ingestion
Server log data is uploaded to **Azure Blob Storage**.  
The Python script connects to Azure and downloads the data for processing.

### 2. Data Transformation
The pipeline performs several cleaning and transformation steps:

- Standardizes column names
- Removes duplicate records
- Converts timestamps for time-based analysis
- Calculates monitoring metrics such as CPU and memory status

Example derived metric:

resource_utilization_score = (cpu_utilization + memory_usage) / 2


### 3. Security Handling
Sensitive information such as **IP addresses** is masked using hashing to avoid exposing raw infrastructure details.

### 4. Data Storage
The cleaned dataset is stored in **Azure SQL Database**, making it easy to query and connect with Power BI.

---

## Power BI Dashboard

The Power BI dashboard provides an overview of server health and performance.

Main features include:

- Average CPU Utilization
- Average Memory Usage
- Total Servers
- Total Downtime
- CPU utilization trend over time
- Network traffic comparison by server
- CPU status distribution
- Server distribution by region

Filters allow users to explore the data by:

- Server Location
- Operating System
- Hostname

### Dashboard Preview

<img src="https://github.com/prve17/virtual-server-monitoring-pipeline/blob/main/Dashboard.png">

---

## Project Structure

```text
virtual-server-monitoring-pipeline/
│
├── pipeline.py
├── requirements.txt
├── README.md
├── .env.example
├── architecture.png
├── dashboard.png
├── server_monitoring_dashboard.pbix
└── server_monitoring_pipeline_presentation.pptx
```

---

## Running the Pipeline

Install dependencies:

- pip install -r requirements.txt

Run the pipeline:
- python pipeline.py


The script will:
1. Download logs from Azure Blob Storage
2. Transform the dataset
3. Load the processed data into Azure SQL Database

---

## Future Improvements

Possible enhancements for this project include:

- Real-time log ingestion
- Automated alerts for high CPU servers
- Machine learning-based anomaly detection
- Integration with cloud monitoring services

---

## Author

This project was created as part of a **data engineering case study** focused on building a cloud-based server monitoring pipeline.
