# ===============================================
# ARQUIVO: client.py
# Propósito: Cliente de socket que envia UMA imagem e recebe o resultado.
# ===============================================

import socket
import numpy as np
import cv2
import os

# --- CONFIGURAÇÕES DE REDE ---
HOST = '127.0.0.1'      
PORT = 65432            
# Arquivo fixo a ser enviado:
IMAGE_PATH = 'imagem_teste.jpg' 

def iniciar_cliente():
    
    # 1. PREPARAR IMAGEM PARA ENVIO
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Erro: Arquivo '{IMAGE_PATH}' não encontrado. Crie um para enviar.")
        return

    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print("❌ Erro ao carregar a imagem. Verifique o arquivo.")
        return

    _, buffer_envio = cv2.imencode('.jpg', img)
    bytes_para_enviar = buffer_envio.tobytes()
    tamanho_imagem = len(bytes_para_enviar)

    # 2. COMUNICAÇÃO VIA SOCKET
    try:
        # Cria o socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Sockets: connect (conecta ao servidor)
            s.connect((HOST, PORT))
            print(f"✅ Conectado ao servidor em {HOST}:{PORT}")
            
            # --- ENVIAR O TAMANHO E A IMAGEM ORIGINAL ---
            s.sendall(tamanho_imagem.to_bytes(8, 'big')) # Envia o tamanho
            s.sendall(bytes_para_enviar) # Envia a imagem
            print(f"Imagem original ({tamanho_imagem} bytes) enviada.")
            
            # --- RECEBER O TAMANHO E A IMAGEM PROCESSADA ---
            
            # Sockets: read (recebe o tamanho de resposta)
            tamanho_bytes_recebido = s.recv(8)
            if not tamanho_bytes_recebido:
                 print("Erro: Servidor não enviou o tamanho de resposta.")
                 return
                 
            tamanho_recebido = int.from_bytes(tamanho_bytes_recebido, 'big')
            
            # Sockets: read (recebe a imagem em pedaços)
            buffer_recepcao = b''
            bytes_restantes = tamanho_recebido
            
            while bytes_restantes > 0:
                chunk = s.recv(min(bytes_restantes, 4096))
                if not chunk:
                    break
                buffer_recepcao += chunk
                bytes_restantes -= len(chunk)
                
            print("Imagem processada recebida.")
            
            # 3. EXIBIR A IMAGEM PROCESSADA
            np_arr = np.frombuffer(buffer_recepcao, np.uint8)
            imagem_processada = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            cv2.imshow('Imagem Processada (Face Detectada)', imagem_processada)
            cv2.waitKey(0) 
            cv2.destroyAllWindows()

    except ConnectionRefusedError:
        # [cite_start]Tratamento de exceção de conexão [cite: 159, 230]
        print("❌ Erro: Não foi possível conectar. Certifique-se de que o servidor está rodando!")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    iniciar_cliente()