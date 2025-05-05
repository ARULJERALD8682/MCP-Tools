# 🚀 MCP Tools Server with BigQuery Integration

This project demonstrates how to build and serve tools for **Model Context Protocol (MCP)** using Python, FastMCP, Google BigQuery, and Starlette. The tools include querying BigQuery datasets, retrieving schema information, and listing tables — all designed to plug into AI systems for dynamic tool usage.

---

## 🧠 What is MCP?

**Model Context Protocol (MCP)** is a protocol that allows language models to interact with external tools and APIs in a structured, declarative manner. With MCP, you can expose real-world data operations like database queries, web APIs, or even file systems to be safely invoked by LLMs.

---

## 📦 Features

- ✅ Easy integration with Google BigQuery  
- ✅ Expose tools like `get_table_list`, `get_schema`, `run_query`  
- ✅ Real-time interaction over SSE using Starlette  
- ✅ Configurable via `.env` and service account

---

## 🛠️ Tools Implemented

| Tool Name                | Description                                                |
|--------------------------|------------------------------------------------------------|
| `get_list_of_tablename`  | Lists all tables in the specified BigQuery dataset         |
| `get_table_information`  | Retrieves the schema of a specified table                  |
| `excute_qury_and_get_results` | Executes a custom SQL query and returns results        |

---

## 🔧 Setup

### 1. Clone the repo
```bash
git clone https://github.com/ARULJERALD8682/MCP-Tools.git
cd MCP-Tools 
```
### 2. Set up environment
Create a .env file with:
```
DATASET_NAME=your_dataset_name
``` 

Place your BigQuery service_account.json in the project root.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the server
```bash
python main.py --host 0.0.0.0 --port 8081
```
