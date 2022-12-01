import cv2
import face_recognition as fr
from flask import Flask, make_response, jsonify, request
import base64
import io
import PIL.Image as Image
import os 
import json

# Metodo POST
app = Flask(__name__)
@app.route('/pessoas', methods=['POST']) 
def busca_foto():
    dados = request.json
    
    # Extrai exatamente as fotos a serem comparadas ainda em base64
    for i in dados:
        img1 = i['foto']
        img2 = i['fotoAtual']

    # Função para transformar base64 em imagem
    fotoA = base64.b64decode(img1)
    fotoB = base64.b64decode(img2)

    foto1 = Image.open(io.BytesIO(fotoA))
    foto2 = Image.open(io.BytesIO(fotoB))
    # foto1.show()
    # foto2.show()

    # Salva as imagens para comparação 
    foto1.save('Pessoa.jpg')
    foto2.save('PessoaAtual.jpg')

    # Transformar as fotos em RGB
    img = fr.load_image_file('Pessoa.jpg')
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    imgTest = fr.load_image_file('PessoaAtual.jpg')
    imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

    # Gera os pontos de expressão para comparação
    encode = fr.face_encodings(img)[0]
    encodeTest = fr.face_encodings(imgTest)[0]

    # Comparação
    comparacao = fr.compare_faces([encode],encodeTest)
    # print(comparacao)

    # Remove as fotos após comparar
    os.remove('Pessoa.jpg')
    os.remove('PessoaAtual.jpg')

    # Transforma a resposta em json para o envio
    if comparacao:
        resposta_json='{"id": 1, "resp": "true"}'
    else:
        resposta_json='{"id": 2, "resp": "false"}'

    return resposta_json
    

app.run()
