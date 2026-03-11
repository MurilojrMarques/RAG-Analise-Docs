from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import logger, CHROMA_DB_DIR

def preparar_banco_vetorial(caminho_pdf):
    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documentos)
    logger.info(f"Documento dividido em {len(chunks)} chunks.")
    
    logger.info("Carregando modelo de embeddings local")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("Gerando vetores e salvando no ChromaDB")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    print(f"Sucesso! Banco vetorial criado na pasta '{CHROMA_DB_DIR}'.")
    return vectorstore

if __name__ == "__main__":
    preparar_banco_vetorial("docs/documento.pdf")