from flask import Flask, request, jsonify
import face_recognition as fr
import boto3
from PIL import Image
from io import BytesIO
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5501"], methods=["GET", "POST"], allow_headers=["Content-Type"])

# Configurações do AWS S3
BUCKET_NAME = 'imagens-face-recognition'
PREFIXO_IMAGENS = 'imagens/'

# Função para carregar e codificar todas as imagens do S3
def carregar_imagens_s3(bucket_name, prefixo_imagens):
    s3_client = boto3.client('s3')
    codificacoes = []
    nomes_imagens = []
    continuacao = None

    while True:
        kwargs = {'Bucket': bucket_name, 'Prefix': prefixo_imagens}
        if continuacao:
            kwargs['ContinuationToken'] = continuacao
        
        response = s3_client.list_objects_v2(**kwargs)
        
        for obj in response.get('Contents', []):
            nome_arquivo = obj['Key']
            if not nome_arquivo.endswith('/'):
                s3_object = s3_client.get_object(Bucket=bucket_name, Key=nome_arquivo)
                imagem_bytes = s3_object['Body'].read()
                img = Image.open(BytesIO(imagem_bytes))
                img = img.convert('RGB')
                img_np = np.array(img)
                codificacoes_faces = fr.face_encodings(img_np)
                for codificacao in codificacoes_faces:
                    codificacoes.append(codificacao)
                    nomes_imagens.append(nome_arquivo)

        if response.get('IsTruncated'):
            continuacao = response.get('NextContinuationToken')
        else:
            break
    
    return codificacoes, nomes_imagens

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem fornecida'}), 400

    file = request.files['image']
    file_name = file.filename

    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, BUCKET_NAME, f'{PREFIXO_IMAGENS}{file_name}')
    
    return jsonify({'message': 'Imagem cadastrada com sucesso', 'filename': file_name})

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem fornecida'}), 400

    file = request.files['image']
    img = Image.open(file.stream)
    img = img.convert('RGB')
    img_np = np.array(img)
    face_encodings = fr.face_encodings(img_np)

    if not face_encodings:
        return jsonify({'error': 'Nenhum rosto encontrado na imagem'}), 400

    # Carregar codificações do S3
    codificacoes_imagens, nomes_imagens = carregar_imagens_s3(BUCKET_NAME, PREFIXO_IMAGENS)
    
    min_distancia = float('inf')
    nome_imagem_identificado = None

    for face_encoding in face_encodings:
        for i, codificacao in enumerate(codificacoes_imagens):
            distancia = fr.face_distance([codificacao], face_encoding)[0]
            # Adiciona log para depuração
            print(f'Distância calculada: {distancia}')
            if distancia < min_distancia:
                min_distancia = distancia
                if distancia < 0.45:  # Ajuste o limiar conforme necessário
                    nome_imagem_identificado = nomes_imagens[i]
    
    if nome_imagem_identificado:
        url_imagem = f'https://{BUCKET_NAME}.s3.amazonaws.com/{nome_imagem_identificado}'
        return jsonify({
            'result': 'Rosto identificado',
            'image_url': url_imagem,
            'name': nome_imagem_identificado
        })
    else:
        return jsonify({'result': 'Rosto não identificado'})

if __name__ == '__main__':
    app.run(port=8080)