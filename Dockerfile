# Dockerfile

# 1. Use uma imagem base oficial do Python.
FROM python:3.11-slim

# 2. Defina o diretório de trabalho dentro do contêiner.
WORKDIR /app

# 3. Copie o arquivo de dependências para o contêiner.
COPY requirements.txt .

# 4. Instale as dependências do projeto.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie o restante dos arquivos da aplicação para o contêiner.
COPY . .

# 6. Exponha a porta em que a aplicação irá rodar.
EXPOSE 1910

# 7. Defina o comando para iniciar a aplicação quando o contêiner for executado.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1910"]