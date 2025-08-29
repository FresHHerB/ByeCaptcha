# 🔐 Autenticação

A API requer autenticação via **Authorization Bearer token** para todos os endpoints de transcrição.

## 📋 Como Usar

### **Headers Obrigatórios:**
```
Authorization: Bearer sua_auth_key_aqui
```

### **Exemplo com cURL:**
```bash
curl -X POST \
  https://dash-yt-byecaptcha.h5wo9n.easypanel.host/byeCaptcha \
  -H "Authorization: Bearer byecaptcha_secure_token_2024_xyz789" \
  -F "file=@audio.mp3"
```

### **Exemplo com Python:**
```python
import requests

headers = {
    "Authorization": "Bearer byecaptcha_secure_token_2024_xyz789"
}

with open("audio.mp3", "rb") as f:
    files = {"file": ("audio.mp3", f, "audio/mpeg")}
    response = requests.post(
        "https://dash-yt-byecaptcha.h5wo9n.easypanel.host/byeCaptcha",
        headers=headers,
        files=files
    )
```

### **Exemplo com JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', audioFile);

fetch('https://dash-yt-byecaptcha.h5wo9n.easypanel.host/byeCaptcha', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer byecaptcha_secure_token_2024_xyz789'
    },
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## ⚙️ Configuração

### **No Easypanel:**
Adicione a variável de ambiente:
```
AUTH_KEY=byecaptcha_secure_token_2024_xyz789
```

### **Localmente:**
No arquivo `.env`:
```bash
AUTH_KEY=byecaptcha_secure_token_2024_xyz789
OPENAI_API_KEY=sua_chave_openai
```

## 🚫 Endpoints Sem Autenticação

Apenas estes endpoints são públicos:
- `GET /` - Informações da API
- `GET /health` - Health check para monitoramento
- `GET /docs` - Documentação Swagger

## 🔒 Erros de Autenticação

### **401 - Authorization header obrigatório:**
```json
{"detail": "Authorization header obrigatório"}
```

### **401 - Token inválido:**
```json
{"detail": "Token de autorização inválido"}
```
