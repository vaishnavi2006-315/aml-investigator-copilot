# AML Investigator Copilot

An AI-assisted Anti-Money Laundering (AML) investigation platform for identifying suspicious accounts, analyzing transaction behavior, and tracing potentially illicit transaction networks.

## 🚀 Overview

**AML Investigator Copilot** combines transaction-level risk analysis with graph-based investigation to help investigators identify suspicious financial activity.

The system analyzes transaction data, assigns account-level risk indicators, detects suspicious patterns, and uses **Neo4j** to investigate relationships between accounts.

The project provides a **FastAPI backend** and an interactive **Streamlit dashboard** for conducting AML investigations.

---

## 🎯 Problem Statement

Traditional AML investigation involves analyzing large numbers of financial transactions and identifying suspicious relationships manually.

This project aims to simplify that process by providing:

* Account-level risk scoring
* Suspicious activity detection
* High-risk account identification
* Multi-hop transaction tracing
* Circular transaction detection
* Graph-based account investigation
* Automated AML investigation reports

---

## 🏗️ System Architecture

```text
                    Transaction Dataset
                           │
                           ▼
                  Data Preprocessing
                           │
                           ▼
                Risk Detection Module
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       Risk Score CSV               Neo4j Graph
             │                           │
             │                    Graph Investigation
             │                           │
             └─────────────┬─────────────┘
                           ▼
                      FastAPI
                    Backend API
                           │
                           ▼
                    Streamlit UI
                           │
                           ▼
              AML Investigator Copilot
```

---

## ✨ Key Features

### 1. Account Risk Detection

The system evaluates account-level transaction behavior and generates:

* Risk Score
* Risk Level
* Suspicious Flag
* Risk Reasons
* Smurfing Flag
* Mule Account Flag
* Known Laundering Account indicator

---

### 2. High-Risk Account Detection

The system identifies accounts classified as **High Risk** and displays them in the investigation dashboard.

---

### 3. Neo4j Transaction Graph

Financial transactions are represented as a graph:

```text
Account A ───────► Account B
             ₹689.98
```

Accounts are represented as nodes and transactions as relationships.

This makes it possible to investigate relationships that may not be obvious from a traditional transaction table.

---

### 4. Multi-Hop Transaction Tracing

The system can trace transaction paths between connected accounts.

Example:

```text
Account A
   │
   ▼
Account B
   │
   ▼
Account C
```

This helps investigators identify chains of transactions across multiple accounts.

---

### 5. Circular Transaction Detection

The system identifies potentially circular transaction patterns.

Example:

```text
A → B → C → A
```

Circular movement of funds can be an important investigation signal.

---

### 6. FastAPI Backend

The backend exposes APIs for accessing investigation data.

Available endpoints include:

```text
GET /
GET /summary
GET /transactions
GET /risk/{account_id}
GET /high-risk
GET /graph/{account_id}
```

Example:

```text
GET /risk/8014C7B60
```

---

### 7. Streamlit Investigation Dashboard

The Streamlit dashboard provides:

* Overall transaction statistics
* Total accounts
* High-risk account count
* Suspicious account count
* Account investigation
* Risk analysis
* Detected suspicious patterns
* Transaction network information
* Generated AML reports
* High-risk account table

---

## 🛠️ Technology Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### Graph Database

* Neo4j

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

### API Communication

* Requests

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
aml-investigator-copilot/
│
├── backend/
│   ├── backend.py
│   ├── backendapp.py
│   ├── db.py
│   ├── graph_api.py
│   ├── load_graph.py
│   ├── multi_hop_trace.py
│   ├── circular_detection.py
│   ├── query_graph.py
│   ├── risk_detection.py
│   └── neo4j_db.py
│
├── frontend/
│   └── aml_copilot_app.py
│
├── data/
│   └── processed/
│       ├── transactions_processed.csv
│       ├── account_risk_scores.csv
│       ├── account_summary.csv
│       └── graph_metrics.csv
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The processed transaction dataset contains transaction-level information including:

* Timestamp
* Sender account
* Receiver account
* Transaction amount
* Payment currency
* Payment format
* Laundering indicator
* Time-related features
* Amount difference
* Currency matching
* Same-bank indicator
* Large transaction indicator

The project currently uses a processed dataset containing **100,000 transactions**.

---

## 🔍 Investigation Workflow

An investigator can enter an account ID into the dashboard.

For example:

```text
8014C7B60
```

The system then:

```text
Account ID
    │
    ▼
Risk Analysis
    │
    ├── Risk Score
    ├── Risk Level
    ├── Suspicious Flag
    └── Risk Reasons
    │
    ▼
Pattern Detection
    │
    ├── Smurfing
    ├── Mule Account
    └── Known Laundering
    │
    ▼
Neo4j Investigation
    │
    ├── Connected Accounts
    ├── Transaction Paths
    └── Transaction Relationships
    │
    ▼
AML Investigation Report
```

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/vaishnavi2006-315/aml-investigator-copilot.git
```

Navigate to the project:

```bash
cd aml-investigator-copilot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Neo4j Setup

Start your Neo4j database.

The application uses:

```text
Bolt URI:
bolt://127.0.0.1:7687
```

The Neo4j credentials are configured in the backend modules.

> For production deployment, credentials should be stored using environment variables rather than being written directly in source code.

---

## ▶️ Running the Application

### 1. Start FastAPI

From the project root:

```bash
python -m uvicorn backend.backend:app --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

### 2. Start Streamlit

Open another terminal:

```bash
python -m streamlit run frontend/aml_copilot_app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

## 🧪 Example Investigation

Enter:

```text
8014C7B60
```

The system can return information such as:

```text
Risk Score
Risk Level
Suspicious Flag
Risk Reasons
Smurfing Flag
Mule Account Flag
Known Laundering Account
Transaction Network
```

The graph API can also return connected transaction relationships.

Example:

```json
{
  "nodes": [
    "8014C7B60",
    "8017559F0"
  ],
  "relationships": [
    {
      "source": "8014C7B60",
      "target": "8017559F0",
      "amount": 689.98
    }
  ]
}
```

---

## 🔐 Security Note

This project is intended for educational and demonstration purposes.

For production use:

* Store credentials in environment variables
* Add authentication and authorization
* Encrypt sensitive financial data
* Add proper logging and auditing
* Implement secure API access
* Apply appropriate financial compliance requirements

---

## 🚀 Future Improvements

Possible future enhancements include:

* Machine-learning based anomaly detection
* Real-time transaction monitoring
* Advanced graph visualization
* Community detection
* Centrality-based risk analysis
* Explainable AI for risk scores
* Investigator case management
* Authentication and role-based access
* Real-time Neo4j transaction ingestion
* LLM-powered investigation assistance
* Automated regulatory report generation

---

## 👩‍💻 Author

**Vaishnavi**

Artificial Intelligence and Data Science

---

## 📌 Project Status

**Core MVP completed.**

The current implementation supports:

* Transaction analysis
* Account risk detection
* High-risk account identification
* Neo4j graph modeling
* Multi-hop transaction tracing
* Circular transaction detection
* FastAPI backend
* Streamlit investigation dashboard
* AML report generation
