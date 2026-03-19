# 🧠 Agente RAG - API de Inteligência Artificial para Análise de Documentos

Uma API RESTful avançada, desenvolvida em Python, que permite o upload dinâmico de documentos PDF e utiliza Inteligência Artificial (Arquitetura RAG - *Retrieval-Augmented Generation*) para responder a perguntas baseadas estritamente no conteúdo enviado.

O projeto foi construído focando em **Clean Architecture**, escalabilidade e boas práticas de Engenharia de Software, demonstrando a integração de Modelos de Linguagem (LLMs) em sistemas de backend tradicionais.

## 🚀 Tecnologias e Decisões Arquiteturais

* **FastAPI:** Framework assíncrono para roteamento HTTP ágil e geração automática de documentação interativa (Swagger/OpenAPI).
* **LangChain (LCEL):** Orquestração moderna do fluxo de dados para conectar o banco vetorial, *prompts* e o modelo de linguagem.
* **Groq (Llama 3.1 8B):** Motor de inferência (LLM) ultrarrápido para a geração das respostas com base no contexto recuperado.
* **HuggingFace Embeddings:** Vetorização de texto rodando localmente para economia de custos e privacidade de dados.
* **ChromaDB:** Banco de dados vetorial embutido para busca semântica ágil dos trechos mais relevantes do documento.
* **SQLite:** Persistência relacional leve para rastreabilidade e auditoria (histórico de perguntas e respostas).
* **Python-Multipart:** Processamento de formulários HTTP para upload de arquivos pesados.

## 🛠️ Como Executar Localmente

### Pré-requisitos
* Python 3.12+
* Chave de API do Groq (Gratuita em [console.groq.com](https://console.groq.com))

### Passo a Passo

**1. Clone este repositório:**
```bash
git clone [https://github.com/MurilojrMarques/RAG-Analise-Docs.git](https://github.com/MurilojrMarques/RAG-Analise-Docs.git)
cd RAG-Analise-Docs
```

**2. Crie e ative o ambiente virtual:**
```bash
# No Linux/macOS:
python -m venv venv
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**
Crie um arquivo `.env` na raiz do projeto e adicione a sua chave:
```env
GROQ_API_KEY=sua_chave_api_aqui
```

**5. Inicie o servidor em modo de desenvolvimento:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3333 --reload
```

**6. Acesse a documentação interativa (Swagger):**
Abra o navegador e acesse: [http://localhost:3333/docs](http://localhost:3333/docs)

## 🔗 Endpoints Principais

A API está documentada dinamicamente via Swagger. O fluxo principal consiste em:

* **`POST /api/v1/rag/upload`**: Recebe um arquivo `.pdf` via `multipart/form-data`, salva no disco, extrai o texto, converte em embeddings e atualiza a base de conhecimento (ChromaDB).
* **`POST /api/v1/rag/perguntar`**: Recebe um JSON com a pergunta, busca o contexto no banco vetorial, aciona o LLM via Groq e salva a interação no histórico (SQLite).
* **`GET /api/v1/rag/historico`**: Retorna a trilha de auditoria completa com todas as interações passadas.
* **`GET /api/v1/rag/perguntas`**: Retorna apenas as perguntas feitas.
* **`GET /api/v1/rag/respostas`**: Retorna apenas as respostas feitas.
* **`GET /api/v1/rag/documentos`**: Lista os PDFs atualmente disponíveis no armazenamento do servidor.
* **`GET /api/v1/rag/documentos/{nome_do_arquivo}`**: Faz download do arquivo escolhido.
* **`DELETE /api/v1/rag/documento/{nome_do_arquivo}`**: Remove documentos específicos do armazenamento físico.