import time
import os
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente (útil para desenvolvimento local)
load_dotenv()

# --- Configuração da Aplicação FastAPI ---
app = FastAPI(
    title="byeCaptcha API",
    description="Endpoint para transcrever áudios de reCAPTCHA usando a API da OpenAI.",
    version="1.0.0"
)

# --- Configuração do Cliente OpenAI ---
# A chave da API é lida da variável de ambiente, como solicitado para o EasyPanel.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY não configurada!")
    raise RuntimeError("A variável de ambiente OPENAI_API_KEY não foi definida.")

client = AsyncOpenAI(api_key=api_key)

# --- Endpoints ---
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "byeCaptcha Audio Transcription API", 
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint para monitoramento"""
    return {
        "status": "healthy", 
        "timestamp": time.time(),
        "api_key_configured": bool(api_key)
    }

@app.post("/byeCaptcha")
async def transcribe_audio(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Recebe um arquivo de áudio, transcreve usando o modelo gpt-4o-mini-transcribe
    e retorna a resposta formatada com tempos de processamento.
    """
    # Inicia a contagem do tempo total de processamento do endpoint
    start_total_time = time.perf_counter()

    # Validação básica do arquivo de áudio
    # Aceita também arquivos sem content_type específico (comum em uploads)
    if file.content_type and not (
        file.content_type.startswith("audio/") or 
        file.content_type.startswith("video/") or
        file.content_type == "application/octet-stream"
    ):
        logger.warning(f"Tipo de arquivo questionável: {file.content_type}")
        # Continua mesmo assim - OpenAI pode aceitar
    
    # Verificar extensão do arquivo como fallback
    if file.filename:
        valid_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.mp4', '.mpeg', '.mpga', '.oga', '.ogg', '.webm']
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext and file_ext not in valid_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Formato de arquivo não suportado: {file_ext}. Formatos aceitos: {', '.join(valid_extensions)}"
            )

    try:
        # Lê o conteúdo do arquivo de áudio em memória
        audio_content = await file.read()
        
        if not audio_content:
            raise HTTPException(status_code=400, detail="Arquivo de áudio vazio")
        
        # Verificar tamanho do arquivo (limite OpenAI: 25MB)
        file_size_mb = len(audio_content) / (1024 * 1024)
        if file_size_mb > 25:
            raise HTTPException(
                status_code=413, 
                detail=f"Arquivo muito grande ({file_size_mb:.1f}MB). Limite: 25MB"
            )
        
        logger.info(f"Arquivo recebido: {file.filename}, Tamanho: {file_size_mb:.2f}MB")

        # Inicia a contagem do tempo da chamada à API da OpenAI
        start_openai_time = time.perf_counter()

        # Envia o áudio para a API de transcrição da OpenAI
        transcription_response = await client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=(file.filename or "audio.wav", audio_content, file.content_type or "audio/wav"),
            response_format="verbose_json"  # Para obter informações detalhadas
        )

        # Finaliza a contagem do tempo da chamada à API
        end_openai_time = time.perf_counter()

        # Finaliza a contagem do tempo total do endpoint
        end_total_time = time.perf_counter()

        # Calcula as durações em milissegundos (ms)
        openai_processing_time_ms = round((end_openai_time - start_openai_time) * 1000, 2)
        total_processing_time_ms = round((end_total_time - start_total_time) * 1000, 2)

        # Formatar resposta no formato solicitado
        text_content = transcription_response.text
        word_count = len(text_content.split()) if text_content else 0
        
        # Aproximação de tokens baseada no tamanho do arquivo e palavras
        estimated_input_tokens = int(len(audio_content) / 1000)  # ~1 token por KB
        
        response_data = {
            "text": text_content,
            "usage": {
                "type": "tokens",
                "input_tokens": estimated_input_tokens,
                "input_token_details": {
                    "text_tokens": 0,
                    "audio_tokens": estimated_input_tokens
                },
                "output_tokens": word_count,
                "total_tokens": estimated_input_tokens + word_count
            },
            "processing_times": {
                "openai_request_time_ms": openai_processing_time_ms,
                "total_processing_time_ms": total_processing_time_ms
            },
            "openai_response_details": {
                "language": getattr(transcription_response, 'language', None),
                "duration": getattr(transcription_response, 'duration', None)
            }
        }
        
        logger.info(f"Transcrição concluída em {total_processing_time_ms}ms (OpenAI: {openai_processing_time_ms}ms)")
        
        return response_data

    except Exception as e:
        logger.error(f"Erro durante transcrição: {str(e)}")
        # Em caso de erro com a API da OpenAI ou outro problema
        if "rate limit" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limit excedido. Tente novamente em alguns minutos.")
        elif "timeout" in str(e).lower():
            raise HTTPException(status_code=504, detail="Timeout na requisição para OpenAI")
        else:
            raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {str(e)}")

# --- Execução do Servidor (para desenvolvimento local) ---
if __name__ == "__main__":
    import uvicorn
    # Para rodar localmente: uvicorn main:app --host 0.0.0.0 --port 1910 --reload
    uvicorn.run(app, host="0.0.0.0", port=1910)
