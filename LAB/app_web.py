from flask import Flask, render_template, request, jsonify
import time
import csv
from datetime import datetime
import random # Para simulação

app = Flask(__name__)

# --- DADOS GLOBAIS DO PROJETO ---
# Variáveis que guardam o estado do teste
estado = {
    "aluno_atual": "Nenhum",
    "procedimento_ativo": False,
    "start_time_ms": 0,
    "sequencia": 1,
    "resultados_teste_atual": [] # {ponto, tempo_ms}
}

historico_completo = []

# --- FUNÇÕES DE LÓGICA DE DADOS ---

def salvar_csv():
    """Salva todo o histórico em um arquivo CSV."""
    if not historico_completo:
        print("Aviso: Nada para salvar.")
        return False
        
    # Salva na mesma pasta do projeto, com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"relatorio_bronquico_{timestamp}.csv"
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["Data/Hora", "Aluno", "Tempo Total (s)", "Sequencia", "Ponto Detectado", "Tempo do Evento (s)"])
            
            for registro in historico_completo:
                aluno = registro["aluno"]
                tempo_total_s = f"{registro['tempo_total_s']:.2f}".replace('.', ',')

                if registro["eventos"]:
                    for evento in registro["eventos"]:
                        tempo_evento_s = f"{evento['tempo_s']:.2f}".replace('.', ',')
                        writer.writerow([
                            registro["data_hora_fim"],
                            aluno,
                            tempo_total_s,
                            evento['sequencia'],
                            evento['ponto'],
                            tempo_evento_s
                        ])
                else:
                    writer.writerow([registro["data_hora_fim"], aluno, tempo_total_s, "-", "Nenhum", "-"])

        print(f"✅ Histórico salvo em: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")
        return False


# --- ROTAS DA INTERFACE (ACESSADAS PELO CELULAR) ---

@app.route('/')
def interface():
    """Renderiza a interface principal que o professor acessa no navegador."""
    # Envia o estado atual do teste para o HTML
    return render_template('interface.html', estado=estado)

@app.route('/iniciar_teste', methods=['POST'])
def iniciar_teste():
    """Recebe o comando INICIAR da interface do professor."""
    aluno = request.form.get('aluno_nome').strip()
    
    if not aluno:
        return jsonify({"status": "erro", "mensagem": "Nome do aluno é obrigatório."}), 400

    # Lógica de INÍCIO
    estado["aluno_atual"] = aluno
    estado["procedimento_ativo"] = True
    estado["start_time_ms"] = int(time.time() * 1000)
    estado["sequencia"] = 1
    estado["resultados_teste_atual"] = []
    
    print(f"\n🎓 INICIADO: Teste para {aluno}")
    
    # ********* AQUI SERIA O COMANDO PARA O ESP32 REAL *********
    # Ex: enviar_comando_para_esp32("INICIAR") 
    
    return jsonify({"status": "sucesso", "aluno": aluno})

@app.route('/finalizar_teste', methods=['POST'])
def finalizar_teste():
    """Recebe o comando FINALIZAR da interface do professor."""
    global historico_completo
    
    if not estado["procedimento_ativo"]:
        return jsonify({"status": "erro", "mensagem": "Nenhum teste ativo."}), 400

    estado["procedimento_ativo"] = False
    
    tempo_total_ms = int(time.time() * 1000) - estado["start_time_ms"]
    tempo_total_s = tempo_total_ms / 1000.0
    
    # Consolida e adiciona ao histórico
    registro = {
        "aluno": estado["aluno_atual"],
        "tempo_total_s": tempo_total_s,
        "eventos": estado["resultados_teste_atual"],
        "data_hora_fim": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    historico_completo.append(registro)
    
    # Reseta o estado
    estado["aluno_atual"] = "Nenhum"
    
    # ********* AQUI SERIA O COMANDO PARA O ESP32 REAL *********
    # Ex: enviar_comando_para_esp32("FIM")
    
    print(f"🏁 FINALIZADO: Tempo total {tempo_total_s:.2f}s. Salvo em memória.")
    
    return jsonify({"status": "sucesso", "tempo_total": f"{tempo_total_s:.2f}"})

@app.route('/salvar', methods=['POST'])
def salvar_dados():
    """Rota para salvar o histórico em CSV."""
    if salvar_csv():
        return jsonify({"status": "sucesso", "mensagem": "Dados salvos com sucesso!"})
    return jsonify({"status": "erro", "mensagem": "Erro ao salvar dados."}), 500


# --- ROTAS DE DADOS (ACESSADAS PELO ESP32 REAL ou Simulação) ---

@app.route('/registrar_ponto')
def registrar_ponto():
    """
    Rota que o ESP32 real usaria para enviar uma detecção (HTTP GET).
    Exemplo de URL (quando real): http://IP_DO_NOTEBOOK:5000/registrar_ponto?ponto=Traqueia
    """
    if not estado["procedimento_ativo"]:
        return jsonify({"status": "erro", "mensagem": "Procedimento não ativo."}), 200 # OK, mas sem registro
        
    ponto_detectado = request.args.get('ponto')
    
    if not ponto_detectado:
        return jsonify({"status": "erro", "mensagem": "Ponto de detecção não fornecido."}), 400

    # Lógica de registro
    tempo_decorrido = int(time.time() * 1000) - estado["start_time_ms"]
    
    evento = {
        "sequencia": estado["sequencia"],
        "ponto": ponto_detectado,
        "tempo_ms": tempo_decorrido,
        "tempo_s": tempo_decorrido / 1000.0
    }
    
    estado["resultados_teste_atual"].append(evento)
    estado["sequencia"] += 1
    
    print(f"-> Detecção (Simulada/Real): {ponto_detectado} em {evento['tempo_s']:.2f}s")
    
    return jsonify({"status": "sucesso", "sequencia": estado["sequencia"] - 1})

@app.route('/status_teste')
def status_teste():
    """Rota para a interface buscar o estado atual e a lista de eventos (AJAX)."""
    return jsonify(estado)


# --- ROTA DE MOCK DATA (Simulação Interna) ---

@app.route('/simular_ponto', methods=['POST'])
def simular_ponto():
    """Rota para o botão de simulação na interface."""
    ponto_simulado = random.choice(["Traqueia", "Bronquio_Direito", "Bronquio_Esquerdo"])
    
    # Chama a rota que seria usada pelo ESP32 (reutiliza a lógica)
    with app.test_request_context(f'/registrar_ponto?ponto={ponto_simulado}'):
        return registrar_ponto()


if __name__ == '__main__':
    # Roda o servidor. '0.0.0.0' permite que o celular/tablet acesse o notebook na rede Wi-Fi.
    print("\n\n--- INICIANDO SERVIDOR FLASK ---")
    print("💻 Para acessar a interface (celular/PC):")
    print("   1. Descubra o IP do seu notebook na rede Wi-Fi (Ex: 192.168.1.10)")
    print("   2. Acesse no navegador: http://[SEU_IP]:5000/")
    print("--------------------------------------\n")
    app.run(host='0.0.0.0', port=5000, debug=True)