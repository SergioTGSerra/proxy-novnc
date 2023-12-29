from flask import Flask, jsonify, request
import subprocess
from threading import Thread
import time

app = Flask(__name__)

# Lista para armazenar os IDs dos threads em execução
running_threads = []

def execute_command(host, port, listen_port):
    try:
        if 5900 <= port < 6080:
            command = f"./novnc/utils/novnc_proxy --vnc {host}:{port} --listen {listen_port}"
            thread = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running_threads.append({'port': port, 'thread': thread})
        else:
            print(f'Porta {port} fora do intervalo permitido.')
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar o comando para a porta {port}: {str(e)}')

# Rota para execução do comando
@app.route('/<string:host>/<int:port>', methods=['GET']) 
def get_vnc_url(host, port):
    if 5900 <= port < 6080:
        # Verifica se o thread já está em execução para a porta específica
        for thread in running_threads:
            if thread['port'] == port:
                # Se já existir, cancela o thread
                thread['thread'].kill()
                running_threads.remove(thread)
                break

        # Criando uma thread com tempo limite
        listen_port = port + 1000
        thread = Thread(target=execute_command, args=(host, port, listen_port))
        thread.start()
        # Tempo limite de 4 horas
        thread.join(4 * 60 * 60)

        return jsonify({'status': 'success', 'message': f'{request.host.split(":")[0]}:{listen_port}/vnc.html?host={request.host.split(":")[0]}:{listen_port}'}), 200
    else:
        return jsonify({'status': 'error', 'message': f'Porta {port} fora do intervalo permitido.'}), 400

if __name__ == '__main__':
    app.run(debug=True)