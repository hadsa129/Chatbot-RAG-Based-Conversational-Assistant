# Chatbot-RAG-Based-Conversational-Assistant

## Overview

The **RAG Chatbot** is a Retrieval-Augmented Generation (RAG)-based intelligent assistant designed to answer questions about Orange Tunisia’s products, services, and customer data.  
It combines **retrieval-based search** with **generative AI (LLMs)** to deliver contextually relevant and accurate responses.

---

## Features

- 💬 **Interactive Chat Interface** built with Streamlit  
- 📊 **Data Retrieval** from multiple CSV files (purchases, recharges, churn, segmentation, etc.)  
- 🧩 **Context-aware Answers** using a local RAG pipeline  
- ⚙️ **Vector Search** powered by **ChromaDB**  
- 🧠 **Local Embeddings & LLMs** using Ollama:
  - Embeddings model: `mxbai-embed-large`
  - Language model: `qwen2.5:3b`
- 🗂️ **Multi-file Support** – automatically processes all CSVs in the `data_client/` folder

---

## Architecture

The chatbot is built using the **RAG pipeline** (Retrieval-Augmented Generation):

1. **Data Loading (`load_data.py`)**
   - Loads all CSV files in `data_client/`
   - Converts them into text documents
   - Splits them into small chunks for embedding
   - Stores vector embeddings in a **Chroma** database

2. **Retrieval (`app.py`)**
   - When a query is received, similar chunks are retrieved based on embeddings

3. **Generation**
   - The model `qwen2.5:3b` (via **Ollama**) generates an answer using the retrieved context

4. **User Interface (`st.py`)**
   - Streamlit provides a chat interface with persistent chat history
   - Users can view sources used to generate each response

---

## 🧩 Components

| Component | Description |
|------------|-------------|
| **Ollama LLM** | Large Language Model used for response generation (`qwen2.5:3b`) |
| **Ollama Embeddings** | Used for semantic similarity search (`mxbai-embed-large`) |
| **ChromaDB** | Vector store for efficient document retrieval |
| **LangChain** | Framework managing retrieval, embeddings, and prompt chaining |
| **Streamlit** | Web interface for interactive chatting |

---

## 🧰 Installation

### Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # (on Mac/Linux)
venv\Scripts\activate     # (on Windows)
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Install and run Ollama
```bash
ollama pull qwen2.5:3b
ollama pull mxbai-embed-large
```
### Run the chatbot
```bash
streamlit run st.py
```

## Author

Hadil Sahraoui
Data & BI Engineer
