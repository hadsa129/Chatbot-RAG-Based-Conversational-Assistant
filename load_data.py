import os
import shutil
import random
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def load_and_process_data(data_dir="data_client", persist_directory="./chroma_db", max_rows=100):
    # ---- CLEAN OLD DATABASE (optional) ----
    if os.path.exists(persist_directory):
        print(f"🗑️  Removing existing ChromaDB directory...")
        shutil.rmtree(persist_directory)
        print(f"✅ Cleared old database.")

    # ---- INIT EMBEDDINGS ----
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # ---- INIT TEXT SPLITTER ----
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=200
    )

    # ---- GET CSV FILES ----
    csv_files = [
        os.path.join(data_dir, file)
        for file in os.listdir(data_dir)
        if file.endswith(".csv")
    ]

    print(f"📂 Found {len(csv_files)} CSV files in '{data_dir}'")

    # ---- PROCESS EACH FILE ----
    for path in csv_files:
        file_name = os.path.basename(path)
        print(f"\n🚀 Processing file: {file_name}")

        try:
            # Load CSV into LangChain Documents
            loader = CSVLoader(file_path=path, csv_args={'delimiter': ','})
            docs = loader.load()

            # Limit to MAX_ROWS (échantillonnage aléatoire)
            if len(docs) > max_rows:
                docs = random.sample(docs, max_rows)
            print(f"✅ Loaded {len(docs)} documents from {file_name} (limited to {max_rows} for testing)")

            # Split into chunks
            chunks = text_splitter.split_documents(docs)
            print(f"✂️  Created {len(chunks)} text chunks")

            # Create or update vectorstore
            if not os.path.exists(persist_directory):
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=persist_directory
                )
            else:
                vectorstore = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=embeddings
                )
                vectorstore.add_documents(chunks)
            
            vectorstore.persist()
            print(f"✅ Stored {file_name} in vector database")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

    print("\n🔄 ChromaDB loaded successfully and ready for queries!")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

if __name__ == "__main__":
    load_and_process_data()