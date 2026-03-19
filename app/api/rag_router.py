from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.core.config import logger
from app.services.rag_service import rag_chain_instance
from app.services import document_service
from app.services import history_service

router = APIRouter(prefix="/api/v1/rag", tags=["Inteligência Artificial"])

class PerguntaRequest(BaseModel):
    pergunta: str = Field(..., min_length=3, description="A pergunta a ser feita baseada no documento.")

@router.post("/upload", summary="Faz o upload de um PDF e adiciona à base de conhecimento da IA")
async def upload_documento(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .pdf são permitidos.")
    try:
        document_service.processar_upload_pdf(file)
        return {
            "mensagem": "Arquivo processado com sucesso!",
            "arquivo": file.filename,
            "status": "Vetorizado e pronto para perguntas"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao processar o documento.")

@router.get("/documentos", summary="Lista todos os documentos disponíveis")
async def listar_documentos():
    arquivos = document_service.listar_todos_documentos()
    return {"documentos": arquivos}

@router.get("/documento/{nome_arquivo}", summary="Baixa um documento enviado")
async def baixar_documento(nome_arquivo: str):
    caminho_arquivo = document_service.obter_caminho_documento(nome_arquivo)
    if not caminho_arquivo:
        raise HTTPException(status_code=404, detail="Documento não encontrado no servidor.")
    return FileResponse(path=caminho_arquivo, filename=nome_arquivo, media_type='application/pdf')

@router.delete("/documento/{nome_arquivo}", summary="Remove um documento enviado")
async def remover_documento(nome_arquivo: str):
    removido = document_service.deletar_documento(nome_arquivo)
    if not removido:
        raise HTTPException(status_code=404, detail="Documento não encontrado no servidor.")
    return {
        "mensagem": f"Documento '{nome_arquivo}' removido do armazenamento.",
        "aviso": "Os dados vetorizados podem ainda existir na memória da IA."
    }

@router.post("/perguntar", summary="Faz uma pergunta para a IA sobre os documentos enviados")
async def fazer_pergunta(request: PerguntaRequest):
    logger.info(f"Recebendo pergunta: '{request.pergunta}'")
    try:
        resposta = rag_chain_instance.invoke(request.pergunta)
        history_service.guardar_interacao(request.pergunta, resposta)
        
        logger.info("Resposta gerada e guardada no histórico com sucesso.")
        return {
            "pergunta": request.pergunta,
            "resposta": resposta,
        }
    except Exception as e:
        logger.error("Erro interno ao invocar a cadeia do LangChain", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro ao processar a sua solicitação junto à Inteligência Artificial."
        )
    
@router.get("/historico", summary="Lista todo o histórico de conversas")
async def listar_historico():
    """Retorna todas as perguntas e respostas guardadas."""
    historico = history_service.obter_historico()
    return {"historico": historico}

@router.get("/perguntas", summary="Lista apenas as perguntas feitas anteriormente")
async def listar_perguntas():
    """Filtra o histórico para retornar apenas as perguntas."""
    historico = history_service.obter_historico()
    perguntas = [{"id": item["id"], "pergunta": item["pergunta"], "data": item["data_hora"]} for item in historico]
    return {"perguntas": perguntas}

@router.get("/respostas", summary="Lista apenas as respostas geradas anteriormente")
async def listar_respostas():
    """Filtra o histórico para retornar apenas as respostas."""
    historico = history_service.obter_historico()
    respostas = [{"id": item["id"], "resposta": item["resposta"], "data": item["data_hora"]} for item in historico]
    return {"respostas": respostas}