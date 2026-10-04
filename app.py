# https://github.com/fvaladares/exemploBasicoFlask

from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar os dados do sensor e a temperatura
banco_em_memoria = []

# Rota para receber a leitura do sensor (Método POST)
@app.route('/sensores/clima', methods=['POST'])
def registrar_leitura():
    dados = request.get_json()
    
    # Adiciona a temperatura informada à nossa lista
    if 'id' not in dados or 'temperatura' not in dados:
        return jsonify({"erro": "Os campos 'id' e 'temperatura' são obrigatórios."}), 400

    banco_em_memoria.append(dados)

    return jsonify({"mensagem": "Leitura registrada com sucesso!", "dados": dados}), 201

# Rota para consultar o resumo das leituras (Método GET)
@app.route('/sensores/clima', methods=['GET'])
def listar_todos():
    acima_de = request.args.get('acima_de')

    leituras = banco_em_memoria
    if acima_de is not None:
        try:
            limite = float(acima_de)
            leituras = [leitura for leitura in banco_em_memoria if leitura.get('temperatura', 0) > limite]
        except ValueError:
            return jsonify({"erro": "O parâmetro 'acima_de' deve ser um número válido."}), 400

    return jsonify({"total_registros": len(leituras), "leituras": leituras}), 200


# NOVA ROTA: Busca um sensor específico pelo ID passado na URL
@app.route('/sensores/clima/<int:sensor_id>', methods=['GET'])
def buscar_por_id(sensor_id):
    for leitura in banco_em_memoria:
        if leitura['id'] == sensor_id:
            return jsonify(leitura), 200

    # Se o laço terminar e não encontrar o ID, retorna 404 Not Found
    return jsonify({"erro": f"Sensor '{sensor_id}' não encontrado."}), 404


@app.route('/sensores/clima/<int:sensor_id>', methods=['PUT'])
def atualizar_sensor(sensor_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido ou ausente."}), 400

    for leitura in banco_em_memoria:
        if leitura['id'] == sensor_id:
            # Atualiza 'temperatura' (ou 'valor', se enviado)
            if 'temperatura' in dados:
                leitura['temperatura'] = dados['temperatura']
            elif 'valor' in dados:
                leitura['temperatura'] = dados['valor']

            return jsonify({"mensagem": "Sensor atualizado com sucesso!", "dados": leitura}), 200

    return jsonify({"erro": f"Sensor '{sensor_id}' não encontrado."}), 404

# NOVA ROTA: Remove um sensor específico da lista
@app.route('/sensores/clima/<int:sensor_id>', methods=['DELETE'])
def deletar_sensor(sensor_id):
    global banco_em_memoria
    tamanho_original = len(banco_em_memoria)

    # Recria a lista mantendo apenas os sensores com ID diferente do informado
    banco_em_memoria = [leitura for leitura in banco_em_memoria if leitura['id'] != sensor_id]

    if len(banco_em_memoria) < tamanho_original:
        return jsonify({"mensagem": f"Sensor '{sensor_id}' removido com sucesso."}), 200

    return jsonify({"erro": f"Sensor '{sensor_id}' não encontrado para exclusão."}), 404


# def consultar_resumo():
#     # Verifica se a lista está vazia para evitar erro de divisão por zero
#     if len(banco_em_memoria) == 0:
#         return jsonify({"mensagem": "Nenhuma leitura registrada ainda."}), 404
#
#     # Calcula a média das temperaturas
#     media = sum(banco_em_memoria) / len(banco_em_memoria)
#
#     # Lógica de verificação dos alertas
#     alerta = "Clima agradável"
#     if media > 30:
#         alerta = "Alerta de calor"
#     elif media < 15:
#         alerta = "Alerta de frio"
#
#     # Monta a resposta JSON
#     resposta = {
#         "total_de_leituras": len(banco_em_memoria),
#         "media_temperatura": round(media, 2), # Arredonda para 2 casas decimais
#         "status_alerta": alerta
#     }
#
#     return jsonify(resposta), 200

def emTeste():
    pass


if __name__ == '__main__':
    app.run(debug=True)

# TODO (1)
# Teste de Validação (Tratamento de Erros):
# Enviaem um POST via Postman/Insomnia/Bruno contendo apenas
# {"temperatura": 25.0} (omitindo o ID).
# O que aconteceu?
# deu Erro 401
#
 # TODO(2)
# Implementação do Método PUT:
#  Criar uma nova rota @app.route('/sensores/clima/<sensor_id>', methods=['PUT']).
#  A rota deve buscar o sensor pelo ID e atualizar o
#  valor da temperatura com o novo dado enviado
#  no corpo (JSON) da requisição.
# TODO (3)
# Filtros via Query Parameters: Modificar a rota GET /sensores/clima geral.
# Use o método request.args.get('acima_de') para capturar um
#  parâmetro na URL (ex: /sensores/clima?acima_de=30) e fazer a API retornar
#  apenas as leituras de temperatura maiores que o valor informado.
# Testando...
#