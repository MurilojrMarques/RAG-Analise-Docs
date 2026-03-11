from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class PerguntaRequest(BaseModel):
    pergunta: str

app = FastAPI(title="Agente RAG - Análise de Documentos", version="1.0")

print("Iniciando a API e conectando com o banco")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("Conectando ao GROQ")
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

rag_chain = (
    {"context": retriever | formatar_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@app.post("/perguntar")
async def fazer_pergunta(request: PerguntaRequest):
    try:
        resposta = rag_chain.invoke(request.pergunta)

        return {
            "pergunta": request.pergunta,
            "resposta": resposta,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)