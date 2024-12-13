from flask import Flask, request, render_template, jsonify, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import requests
from PIL import Image
import io


app = Flask(__name__)


cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


genai.configure(api_key="AIzaSyCnKaZ0_sk6uP1TETWoGJXLCVhiN2Vqvg0")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
HF_API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_image(prompt):
    """Gera uma imagem a partir do Hugging Face"""
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Erro ao gerar imagem: {response.text}")

@app.route('/')
def index():
    return render_template('StoryGenerator.html')  

@app.route('/enviar_historia', methods=['POST'])
def enviar_historia():
    try:
        
        titulo = request.form.get('titulo')
        personagem = request.form.get('personagem')
        descricao = request.form.get('descricao')
        capa = request.files.get('imagem')  

        if not titulo or not personagem or not descricao:
            return render_template("StoryGenerator.html", mensagem="Todos os campos são obrigatórios.", tipo="erro")

        
        capa_path = None
        if capa and allowed_file(capa.filename):
            filename = secure_filename(capa.filename)
            capa_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            capa.save(capa_path)
        else:
            
            prompt = f"Uma capa para uma história com o título '{titulo}' envolvendo o personagem '{personagem}'."
            image_bytes = generate_image(prompt)
            filename = f"{titulo.replace(' ', '_')}_generated.png"
            capa_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(capa_path, 'wb') as f:
                f.write(image_bytes)

        
        prompt = f"Gere uma história com o título '{titulo}', envolvendo o personagem '{personagem}' e baseando-se nesta descrição: {descricao}."
        response = model.generate_content(prompt)
        historia_gerada = response.text  

        
        doc_ref = db.collection('historias').document()
        doc_ref.set({
            'titulo': titulo,
            'personagem': personagem,
            'descricao': descricao,
            'historia': historia_gerada,
            'capa': capa_path
        })

        
        return render_template('Result.html', titulo=titulo, personagem=personagem, historia=historia_gerada, capa=url_for('static', filename=f'uploads/{filename}'))

    except Exception as e:
        return render_template('StoryGenerator.html', mensagem=f"Erro ao processar: {str(e)}", tipo="erro")

if __name__ == '__main__':
    app.run(debug=True)
