from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from urllib.parse import urlparse, parse_qs
import sys
from dotenv import load_dotenv
import os

load_dotenv()
google_api = os.getenv("API_KEY")

def get_videoID(url):
    video_url = urlparse(url)

    if "youtube.com" in video_url.netloc:
        query = parse_qs(video_url.query)
        return query.get("v", [None])[0]
    elif "youtube.be" in video_url.netloc:
        return video_url.path.lstrip("/")
    
    return None

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
    text = ' '.join([item['text'] for item in transcript])
    return text

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

    with open("summary.txt", "w", encoding="utf-8") as f:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            f.write(chunk.text)

def program():
    video_url = sys.argv[1]
    video_id = get_videoID(video_url)
    transcript = get_transcript(video_id)
    generate(transcript)
    print("summary saved in 'summary.txt'")

if __name__ == "__main__":
    program();