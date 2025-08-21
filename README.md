# smog-video-downloads
Um baixador simples de vídeos do YouTube desenvolvido por mim.  
Já pensou em baixar seus vídeos do YouTube na melhor qualidade possível, sem anúncios chatos, de forma rápida e intuitiva?  
Essa aplicação é exatamente isso: simples, rápida e eficaz. 🚀

---

## Tecnologias usadas

### Front-end
- TailwindCSS

### Back-end
- Django (Python)
- yt-dlp (Python)
- Redis (cache/result backend)
- RabbitMQ (message broker)
- Celery (processamento de tarefas em segundo plano)

### Deploy
- Docker e Docker Compose

---

## Como funciona
1. O usuário envia o link do vídeo pelo front-end.  
2. O back-end cria uma tarefa de download e envia para a fila (RabbitMQ).  
3. O Celery executa o worker e baixa o vídeo usando **yt-dlp**.  
4. Enquanto isso, o front-end faz polling (2 em 2 segundos) para verificar o status da tarefa.  
5. Quando o download termina, o usuário recebe um link direto para baixar o arquivo.  

---

## Como rodar o projeto

### Pré-requisitos
- Python (>= 3.10)
- Docker e Docker Compose instalados

### Passo 1 - Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 2 - Rodar o Docker-compose
```bash
docker-compose up -d
```