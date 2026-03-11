from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core.config import logger
from app.services.rag_service import rag_chain_instance

class PerguntaRequest(BaseModel):
    pergunta: str = Field(..., min_length=3, description="A pergunta a ser feita baseada no documento.")

app = FastAPI(title="Agente RAG - Análise de Documentos", version="2.0")

@app.post("/perguntar")
async def fazer_pergunta(request: PerguntaRequest):
    logger.info(f"Processando pergunta: '{request.pergunta}'")
    try:
        resposta = rag_chain_instance.invoke(request.pergunta)
        logger.info("Resposta gerada com sucesso.")
        
        return {
            "pergunta": request.pergunta,
            "resposta": resposta,
        }
    except Exception as e:
        logger.error("Erro interno ao processar a corrente do RAG", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro ao processar a sua solicitação junto à Inteligência Artificial."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3333, reload=True)