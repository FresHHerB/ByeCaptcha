# main.py

import time
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from openai import AsyncOpenAI
from dotenv import load_dotenv

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
    raise RuntimeError("A variável de ambiente OPENAI_API_KEY não foi definida.")

client = AsyncOpenAI(api_key=api_key)

# --- Definição do Endpoint ---
@app.post("/byeCaptcha")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Recebe um arquivo de áudio, transcreve usando o modelo gpt-4o-mini-transcribe
    e retorna a resposta da OpenAI com tempos de processamento.
    """
    # Inicia a contagem do tempo total de processamento do endpoint
    start_total_time = time.perf_counter()

    # Validação básica do arquivo de áudio
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Apenas áudio é permitido.")

    try:
        # Lê o conteúdo do arquivo de áudio em memória
        audio_content = await file.read()

        # Inicia a contagem do tempo da chamada à API da OpenAI
        start_openai_time = time.perf_counter()

        # Envia o áudio para a API de transcrição da OpenAI
        transcription_response = await client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=("audio.mp3", audio_content, file.content_type)
        )

        # Finaliza a contagem do tempo da chamada à API
        end_openai_time = time.perf_counter()

        # Finaliza a contagem do tempo total do endpoint
        end_total_time = time.perf_counter()

        # Calcula as durações em milissegundos (ms)
        openai_processing_time_ms = (end_openai_time - start_openai_time) * 1000
        total_processing_time_ms = (end_total_time - start_total_time) * 1000

        # Converte o objeto de resposta da OpenAI para um dicionário
        response_data = transcription_response.model_dump()

        # Adiciona os campos de tempo de processamento ao dicionário
        response_data['openai_processing_time_ms'] = round(openai_processing_time_ms)
        response_data['total_processing_time_ms'] = round(total_processing_time_ms)

        return response_data

    except Exception as e:
        # Em caso de erro com a API da OpenAI ou outro problema
        raise HTTPException(status_code=500, detail=str(e))

# --- Execução do Servidor (para desenvolvimento local) ---
if __name__ == "__main__":
    import uvicorn
    # Para rodar localmente: uvicorn main:app --host 0.0.0.0 --port 1910 --reload
    uvicorn.run(app, host="0.0.0.0", port=1910)