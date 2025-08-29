# ByeCaptcha Audio Transcription API

🎯 **API FastAPI para transcrever áudios de reCAPTCHA usando OpenAI `gpt-4o-mini-transcribe`**

## ✨ Características

- ⚡ **Modelo de última geração**: `gpt-4o-mini-transcribe`
- 📊 **Métricas de tempo**: Medição precisa de processamento
- 🐳 **Docker ready**: Container otimizado para produção
- 🛡️ **Seguro**: Usuário não-root, validações robustas
- 📈 **Monitoramento**: Health checks e logs estruturados
- 🌐 **CORS habilitado**: Pronto para frontend

## 📁 Estrutura do Projeto

```
byecaptcha-api/
├── main.py                 # API FastAPI principal
├── requirements.txt        # Dependências Python
├── Dockerfile             # Container otimizado
├── docker-compose.yml     # Orquestração
├── .env.example           # Template de configuração
├── .gitignore             # Exclusões Git
├── .dockerignore          # Exclusões Docker
├── test_api.py            # Script de teste
└── README.md              # Este arquivo
```

## 🚀 Instalação e Uso

### **Opção 1: Docker (Recomendado)**

```bash
# 1. Clonar repositório
git clone https://github.com/FresHHerB/ByeCaptcha.git
cd ByeCaptcha

# 2. Configurar variáveis
cp .env.example .env
# Edite .env com sua chave da OpenAI

# 3. Build e run
docker-compose up -d

# 4. Testar
python test_api.py test_audio.wav http://localhost:1910
```

### **Opção 2: Local**

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis
export OPENAI_API_KEY="sua_chave_aqui"

# 3. Executar
python main.py
```

## 🌐 Deploy no Easypanel

### **1. Configurações no Easypanel:**

- **Type**: Docker
- **Repository**: `FresHHerB/ByeCaptcha`
- **Branch**: `main`
- **Port**: `1910`
- **Health Check**: `/health`

### **2. Variáveis de Ambiente:**

## 🔌 Uso da API

### **Endpoints Disponíveis:**

| Endpoint | Método | Descrição |
|----------|---------|-----------|
| `/` | GET | Informações da API |
| `/health` | GET | Health check |
| `/byeCaptcha` | POST | Transcrição de áudio |
| `/docs` | GET | Documentação Swagger |

### **Endpoint Principal: `/byeCaptcha`**

**POST** `/byeCaptcha`

#### Request:
```bash
curl -X POST \
  http://localhost:1910/byeCaptcha \
  -F "file=@audio.wav"
```

#### Response:
```json
{
  "text": "Imagine the wildest idea that you've ever had...",
  "usage": {
    "type": "tokens",
    "input_tokens": 14,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 14
    },
    "output_tokens": 45,
    "total_tokens": 59
  },
  "processing_times": {
    "openai_request_time_ms": 1250.75,
    "total_processing_time_ms": 1267.32
  },
  "openai_response_details": {
    "language": "english",
    "duration": 5.2
  }
}
```

#### **Campos de Tempo:**
- **`openai_request_time_ms`**: ⏱️ Tempo da requisição à OpenAI
- **`total_processing_time_ms`**: ⏱️ Tempo total do endpoint

## 🎵 Formatos Suportados

A API aceita arquivos de até 25MB nos formatos:
- **MP3**, **WAV**, **M4A**, **FLAC**
- **MP4**, **MPEG**, **MPGA**
- **OGA**, **OGG**, **WEBM**

## 🧪 Testes

```bash
# Testar API local
python test_api.py test_audio.wav

# Testar API remota
python test_api.py test_audio.wav https://sua-api.easypanel.host

# Health check manual
curl http://localhost:1910/health
```

## 📊 Monitoramento

### **Health Check:**
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": 1693420800.123,
  "api_key_configured": true
}
```

### **Logs:**
```bash
# Ver logs do container
docker logs byecaptcha-api

# Com docker-compose
docker-compose logs -f
```

## ⚠️ Limites e Restrições

- 🔢 **Tamanho máximo**: 25MB por arquivo
- ⏰ **Timeout**: 60 segundos para OpenAI
- 🔐 **Rate limiting**: Conforme limites da OpenAI
- 🌍 **Linguagens**: Suporte multilíngue automático

## 🔧 Solução de Problemas

### **Erros Comuns:**

| Erro | Causa | Solução |
|------|--------|---------|
| `401 Unauthorized` | API key inválida | Verificar `OPENAI_API_KEY` |
| `413 Request Too Large` | Arquivo >25MB | Dividir ou comprimir arquivo |
| `504 Timeout` | Arquivo muito longo | Reduzir duração do áudio |
| `429 Rate Limit` | Muitas requisições | Aguardar alguns minutos |

### **Debug:**

```bash
# Verificar configuração
curl http://localhost:1910/health

# Verificar logs
docker logs byecaptcha-api

# Testar com arquivo pequeno
python test_api.py small_test.wav
```

## 🚀 Performance

- ⚡ **Modelo otimizado**: `gpt-4o-mini-transcribe` é mais rápido que Whisper
- 🔄 **Async**: Processamento não-bloqueante
- 📦 **Container otimizado**: Build multi-stage, cache eficiente
- 🛡️ **Health checks**: Monitoramento automático

## 📈 Melhorias Futuras

- [ ] Cache de respostas para áudios idênticos
- [ ] Suporte a lotes (batch processing)
- [ ] Métricas Prometheus
- [ ] Rate limiting customizado
- [ ] Webhook callbacks

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [OpenAI Audio API Docs](https://platform.openai.com/docs/guides/speech-to-text)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Easypanel Documentation](https://easypanel.io/docs)

---

⭐ **Se este projeto foi útil, considere dar uma star!**
