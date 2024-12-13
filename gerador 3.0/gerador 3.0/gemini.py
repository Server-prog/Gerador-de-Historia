import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCnKaZ0_sk6uP1TETWoGJXLCVhiN2Vqvg0")

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
response = model.generate_content("cria uma história falando sobre um menino chamado David")
print(response.text)