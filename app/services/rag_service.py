import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import logger, CHROMA_DB_DIR

def inicializar_rag():
    if not os.path.exists(CHROMA_DB_DIR):
       logger.warning("A pasta ./chroma_db não foi encontrada. Certifique-se de rodar o script de ingestão antes.")
        
    logger.info("Conectando com o banco vetorial")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    logger.info("Conectando ao modelo LLM via Groq")
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.1)

    prompt_template = """
    Você é um assistente especialista em análise de documentos.
    Responda à pergunta do usuário baseando-se EXCLUSIVAMENTE no contexto fornecido abaixo.
    Se a resposta não estiver no contexto, diga "Não encontrei informações sobre isso no documento." e não invente dados.

    Contexto do Documento:
    {context}

    Pergunta do Usuário: {input}

    Responda em português:
    """
    prompt = PromptTemplate.from_template(prompt_template)

    def formatar_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

rag_chain_instance = inicializar_rag()