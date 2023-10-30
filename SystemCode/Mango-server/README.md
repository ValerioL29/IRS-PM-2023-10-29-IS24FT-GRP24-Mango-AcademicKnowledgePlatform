# 🥭 Mango Server

## 📖 Introduction

Mango Server is the backend component of the Mango project. It has -

* A **RESTful** API server written in Python using the FastAPI framework.
* A **DuckDB** embedding database to store the data.
* A Vector Search component to query embeddings and perform efficient searching for papers based on **Milvus**.

## 🚀 Getting Started

Run the command below to start the server.

```bash
uvicorn main:app --reload
```