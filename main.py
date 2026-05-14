from pypdf import PdfReader
import requests
import os

#OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL = "qwen2.5:0.5b"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extrair_texto_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    texto = ""

    for pagina in reader.pages:
        texto += pagina.extract_text() + "\n"
    
    return texto

def perguntar_ollama(pergunta, texto):
    prompt = f"""
        Você é um assistente que responde à perguntas com
        base em um texto extraído de um arquivo PDF

        Texto do PDF:
        {texto}

        Pergunta:
        {pergunta}

        Regras:
        - Responda com base no texto do PDF fornecido.
        - Se não encontrar a resposta, diga que a informação não foi encontrada.
        - Seja objetivo
    """

    resposta = requests.post(
        #OLLAMA_URL,
        GROQ_URL,
        headers={
            "Authorization" : f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            # "prompt" : prompt,
            # "stream" : False
            "messages": [
                {
                    "role" : "user",
                    "content": prompt
                }
            ],
            "temperature" : 0.2
        },
        timeout=120
    )

    resposta.raise_for_status()
    #return resposta.json()['response']
    return resposta.json()["choices"][0]["message"]["content"]

def main():
    texto_pdf = extrair_texto_pdf("./regras_uno.pdf")

    while True:
        pergunta = input("\nPergunta sobre o PDF ou sair: ")

        if pergunta.lower() == "sair":
            break

        resposta = perguntar_ollama(pergunta, texto_pdf)

        print("\nResposta: ")
        print(resposta)

main()