import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def preparar_banco_vetorial(caminho_pdf, diretorio_db="./chroma_db"):
    load_dotenv()
    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documentos)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("Gerando vetores e salvando no ChromaDB")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=diretorio_db
    )
    print(f"Sucesso! Banco vetorial criado na pasta '{diretorio_db}'.")
    return vectorstore

if __name__ == "__main__":
    preparar_banco_vetorial("docs/documento.pdf")