import os
import shutil
from fastapi import UploadFile
from app.core.config import logger
from app.services.ingestao import preparar_banco_vetorial

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def processar_upload_pdf(file: UploadFile) -> str:
    caminho_arquivo = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Arquivo salvo fisicamente em: {caminho_arquivo}")
        preparar_banco_vetorial(caminho_arquivo)
        return caminho_arquivo
        
    except Exception as e:
        logger.error(f"Erro na camada de serviço ao processar upload: {str(e)}", exc_info=True)
        raise e 

def obter_caminho_documento(nome_arquivo: str):
    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    return caminho

def listar_todos_documentos() -> list:
    try:
        return [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
    except Exception as e:
        logger.error(f"Erro ao listar documentos: {str(e)}")
        return []

def deletar_documento(nome_arquivo: str) -> bool:
    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
    if os.path.exists(caminho):
        try:
            os.remove(caminho)
            logger.info(f"Documento '{nome_arquivo}' removido fisicamente.")
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar arquivo físico: {str(e)}")
            raise e
    return False