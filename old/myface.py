from flask import Flask, request, jsonify
import face_recognition as fr
import boto3
from PIL import Image
from io import BytesIO
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://lookid.tec.br/"], methods=["GET", "POST"], allow_headers=["Content-Type"])

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
                codificacao = fr.face_encodings(img_np)
                if codificacao:
                    codificacoes.append(codificacao[0])
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
    face_encoding = fr.face_encodings(img_np)

    if not face_encoding:
        return jsonify({'error': 'Nenhum rosto encontrado na imagem'}), 400

    codificacoes_imagens, nomes_imagens = carregar_imagens_s3(BUCKET_NAME, PREFIXO_IMAGENS)
    comparacoes = fr.compare_faces(codificacoes_imagens, face_encoding[0])
    distancias = fr.face_distance(codificacoes_imagens, face_encoding[0])

    if any(comparacoes):
        index = comparacoes.index(True)
        nome_imagem = nomes_imagens[index]
        url_imagem = f'https://{BUCKET_NAME}.s3.amazonaws.com/{nome_imagem}'
        return jsonify({
            'result': 'Rosto identificado',
            'image_url': url_imagem,
            'name': nome_imagem
        })
    else:
        return jsonify({'result': 'Rosto não identificado'})

if __name__ == '__main__':
    app.run(port=8080)