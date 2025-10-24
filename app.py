from langchain_community.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from typing import List, Dict, Any

class OrangeChatbot:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        self.llm = OllamaLLM(model="qwen2.5:3b")
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def get_response(self, query: str) -> Dict[str, Any]:
        """Get response from the chatbot"""
        # Retrieve relevant documents
        docs = self.vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create prompt with context
        system_prompt = f"""You are a helpful assistant for Orange Tunisia. 
        Answer the question based only on the following context. 
        If you don't know the answer, say you don't know.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:"""
        
        # Get response from LLM
        response = self.llm.invoke(system_prompt)
        
        return {
            "answer": response,
            "sources": [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        }