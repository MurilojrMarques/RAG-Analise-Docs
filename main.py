import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    logger.error("A variável de ambiente GROQ_API_KEY não foi encontrada.")
    raise RuntimeError("GROQ_API_KEY ausente. Configure o arquivo .env.")

if not os.path.exists("./chroma_db"):
    logger.warning("A pasta ./chroma_db não foi encontrada. Certifique-se de rodar o script de ingestão antes.")

class PerguntaRequest(BaseModel):
    pergunta: str = Field(..., min_length=3, description="A pergunta a ser feita baseada no documento.")

app = FastAPI(title="Agente RAG - Análise de Documentos", version="1.1")

try:
    logger.info("Iniciando a API e conectando com o banco")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    logger.info("Conectando ao modelo LLM via Groq")
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.1)

except Exception as init_error:
    logger.error(f"Erro crítico na inicialização dos modelos: {init_error}")
    raise RuntimeError("Falha ao inicializar o motor de IA.")

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

rag_chain = (
    {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@app.post("/perguntar")
async def fazer_pergunta(request: PerguntaRequest):
    logger.info(f"Processando pergunta: '{request.pergunta}'")
    try:
        resposta = rag_chain.invoke(request.pergunta)
        logger.info("Resposta gerada com sucesso.")
        
        return {
            "pergunta": request.pergunta,
            "resposta": resposta,
        }
    except Exception as e:
        logger.error("Erro interno ao processar a corrente do RAG", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro ao processar a sua solicitação junto à Inteligência Artificial. Tente novamente mais tarde."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)