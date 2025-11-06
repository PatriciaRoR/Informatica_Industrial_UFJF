
import socket
import numpy as np
import cv2
import os

from servidor_base import Servidor 

HOST = '127.0.0.1'  
PORT = 65432        

class ServidorImagem(Servidor): # HERDA da classe Servidor
    """ 
    Classe ServidorImagem - Sobrescreve _service com a lógica de reconhecimento facial. 
    """

    def __init__(self, host, port):
        # Chama o construtor da classe base
        super().__init__(host, port)
        
        # Lógica de carregamento do classificador de faces (Do código base do professor)
        xml_classificador = os.path.join(os.path.relpath(
            cv2.__file__).replace('__init__.py', ''), 'data\haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier(xml_classificador)
        
        if self.face_cascade.empty():
            print("AVISO: Classificador de faces não carregado. Verifique o caminho.")
    
    
    def _receive_data(self, con, size):
        """ Função auxiliar para receber dados em chunks até atingir o tamanho especificado. """
        buffer_data = b''
        bytes_restantes = size
        
        while bytes_restantes > 0:
            chunk = con.recv(min(bytes_restantes, 4096))
            if not chunk:
                raise ConnectionResetError("Conexão encerrada pelo cliente") 
            buffer_data += chunk
            bytes_restantes -= len(chunk)
            
        return buffer_data

    # MÉTODOS CHAVE: SOBRESCRITA do _service
    def _service(self, con, client):
        """
        Implementa o serviço de recepção, processamento e envio da imagem.
        """
        print("Atendendo cliente ", client)
        
        try:
            # 1. RECEPÇÃO DO TAMANHO (O cliente enviou o tamanho em 4 bytes)
            tamanho_bytes = con.recv(4) # **RECEBE 4 BYTES, conforme o código do professor!**
            if not tamanho_bytes:
                 print("Cliente ", client, ": Conexão encerrada.")
                 return

            tamanho_imagem = int.from_bytes(tamanho_bytes, 'big') 
            print(f"Cliente {client} -> Recebendo imagem de {tamanho_imagem} bytes")
            
            # 2. RECEPÇÃO E DECODIFICAÇÃO
            buffer_imagem = self._receive_data(con, tamanho_imagem)
            print("Imagem recebida. Processando...")

            # Decodifica os bytes para imagem (igual ao código base do professor)
            img = cv2.imdecode(np.frombuffer(buffer_imagem, np.uint8), cv2.IMREAD_COLOR)

            # --- 3. PROCESSAMENTO (Lógica de Detecção do professor) ---
            if img is None:
                raise ValueError("Erro ao decodificar a imagem recebida.")
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # Desenha retângulos
            for (x, y, w, h) in faces:
                # Usa cor azul (255, 0, 0) para seguir o requisito do desafio
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


            # --- 4. ENVIAR O TAMANHO E A IMAGEM PROCESSADA ---
            # Codifica a imagem processada de volta para bytes JPEG
            _, buffer_envio = cv2.imencode('.jpg', img)
            bytes_para_enviar = buffer_envio.tobytes()
            tamanho_envio = len(bytes_para_enviar)
            
            # Envia o novo tamanho (em 4 bytes, para ser consistente com a recepção)
            con.sendall(tamanho_envio.to_bytes(4, 'big')) 
            
            # Envia os dados da imagem
            con.sendall(bytes_para_enviar)
            print(client, f" -> Imagem processada enviada ({tamanho_envio} bytes)")

        except ConnectionResetError:
            print("Conexão perdida com o cliente ", client)
        except Exception as e:
            print(f"Erro no processamento dos dados do cliente {client}: {e}")
            
        finally:
            con.close() 

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    servidor_de_imagens = ServidorImagem(HOST, PORT)
    servidor_de_imagens.start()