# 📺 youtube summarizer

**YouTube Summarizer** é uma ferramenta de linha de comando que extrai a transcrição de vídeos do YouTube e gera resumos automáticos com inteligência artificial, utilizando a API do **Google Gemini**. 

## 🚀 Funcionalidades

- 📥 Aceita a URL de qualquer vídeo do YouTube
- 🎙️ Extrai a transcrição oficial diretamente do YouTube (sem precisar baixar ou converter o áudio)
- 🤖 Gera resumos com IA usando a API do Google Gemini
- 📄 Salva o resumo automaticamente em um arquivo `.txt`

# 🧩 Bibliotecas Utilizadas

- [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) – para obter a transcrição oficial do vídeo
- [`google-generativeai`](https://pypi.org/project/google-generativeai/) – para interagir com a API do Google Gemini
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) – para carregar variáveis de ambiente de um arquivo `.env`
- Bibliotecas padrão do Python: `sys`, `os`, `urllib.parse`

## 📦 Requisitos

- Python 3.8+
- Chave de API do Google Gemini (configure no arquivo `.env`)

## 📚 Instalação

```bash
git clone https://github.com/flavinhojrz/youtube_summarizer.git
cd youtube_summarizer
pip install -r requirements.txt
```
## 🛠️ Como usar

- Crie um arquivo `.env` com sua chave da API do Google
```bash
GOOGLE_API_KEY='sua-chave-aqui'
```
- Depois execute o script no terminal
```bash
python3 main.py "https://www.youtube.com/watch?v=ABC123xyz"
```

## 📁 Estrutura do Projeto
```
youtube_summarizer/
├── src/
│   └── main.py              # Script principal do projeto
├── .gitignore               # Arquivos e pastas ignoradas pelo Git
├── README.md                # Documentação do projeto
├── requirements.txt         # Lista de dependências
└── .env                     # Variáveis de ambiente (API key)
```



## 🤖 Tecnologias utilizadas

- Youtube Transcript API
- Google Gemini (https://aistudio.google.com/)
- Python3

## 👨‍💻 Autor
- flavinhojrz
```bash
flavinhoolvs@gmail.com
```
