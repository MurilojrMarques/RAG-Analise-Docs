from fastapi import FastAPI
from app.api.rag_router import router as rag_router

app = FastAPI(
    title="Agente RAG - Análise de Documentos", 
    version="1.0",
    description="API para análise de documentos"
)

app.include_router(rag_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3333, reload=True)