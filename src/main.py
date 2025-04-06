from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from google.genai import types
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()
google_api = os.getenv("API_KEY")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoURL(BaseModel):
    url: str

def get_videoID(url):
    video_url = urlparse(url)

    if "youtube.com" in video_url.netloc:
        query = parse_qs(video_url.query)
        return query.get("v", [None])[0]
    elif "youtube.be" in video_url.netloc:
        return video_url.path.lstrip("/")
    
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
        text = ' '.join([item['text'] for item in transcript])
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter transcrição: {str(e)}")

def generate(transcript):
    client = genai.Client(
        api_key=google_api,
    )
    prompt = f"""
        Você é um especialista em análise de conteúdo e geração de resumos informativos e objetivos. 
        Receberá um texto completo e deverá produzir um resumo de alta qualidade, mantendo as informações mais importantes 
        e eliminando redundâncias ou detalhes desnecessários.

        Seu resumo deve ser:
        - Claro e direto
        - Bem estruturado em parágrafos
        - Focado nas ideias principais
        - Livre de repetições e floreios
        - Escrito com linguagem natural e fluida
        - Ideal para quem quer entender o conteúdo rapidamente, sem ler tudo

        Aqui está o texto a ser resumido:

        {transcript}

        Agora, gere um resumo profissional e preciso com base no conteúdo acima.
    """
    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )
    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text
    
    return response

@app.post("/summarize")
def get_summary(req: VideoURL):
    video_id = get_videoID(req.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="URL do vídeo invalida")
    
    transcript = get_transcript(video_id)
    summary = generate(transcript)
    return {"summary": summary}

# def program():
#     video_url = sys.argv[1]
#     video_id = get_videoID(video_url)
#     transcript = get_transcript(video_id)
#     generate(transcript)
#     print("summary saved in 'summary.txt'")

# if __name__ == "__main__":
#     program();