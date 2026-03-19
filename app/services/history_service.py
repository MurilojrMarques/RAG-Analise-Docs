import sqlite3
import os
from datetime import datetime
from app.core.config import logger
DB_PATH = "./historico_rag.db"

def inicializar_base_dados():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_chat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pergunta TEXT NOT NULL,
                    resposta TEXT NOT NULL,
                    data_hora TEXT NOT NULL
                )
            ''')
            conn.commit()
            logger.info("Base de dados de histórico inicializada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar base de dados de histórico: {e}")

def guardar_interacao(pergunta: str, resposta: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO historico_chat (pergunta, resposta, data_hora) VALUES (?, ?, ?)",
                (pergunta, resposta, data_hora)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Erro ao guardar interação no histórico: {e}", exc_info=True)

def obter_historico() -> list:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historico_chat ORDER BY id DESC")
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico: {e}", exc_info=True)
        return []

inicializar_base_dados()