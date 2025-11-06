# ===============================================
# ARQUIVO: processamento.py
# Propósito: Contém a lógica de detecção de faces (OpenCV).
# ===============================================

import cv2
import numpy as np

# Acessa o arquivo do classificador de faces pré-treinado do OpenCV
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def processar_imagem(img):
    """Aplica a técnica de reconhecimento de faces e desenha um retângulo azul."""

    # Verifica se o detector de faces foi carregado corretamente
    if face_cascade.empty():
        print("AVISO: Detector de faces não carregado. Retornando imagem original.")
        return img

    # Converte para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta as faces: usa o modelo pré-treinado
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Desenha o retângulo azul (cor BGR: Azul = 255, 0, 0)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 4)

    return img
