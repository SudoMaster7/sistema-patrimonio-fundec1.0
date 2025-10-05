import os
import json
import gspread
from flask import Flask, render_template,request, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


app = Flask(__name__)

# Google Sheets setup
# --- CONFIGURAÇÃO DO GOOGLE SHEETS (versão para Vercel) ---
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Pega as credenciais da variável de ambiente
    creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json_str:
        raise Exception("Variável de ambiente GOOGLE_CREDENTIALS_JSON não encontrada.")

    # Converte a string JSON em um dicionário Python
    creds_dict = json.loads(creds_json_str)
    
    # Autoriza usando o dicionário de credenciais
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Abre a planilha
    sheet = client.open("Patrimônio FUNDEC").sheet1 
    return sheet

@app.route('/')
def index():
    # Esta página agora é simples, apenas renderiza o formulário.
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    itens_com_linha = []
    try:
        sheet = get_sheet()
        todos_os_valores = sheet.get_all_values()[1:] 
        ultimos_itens = todos_os_valores[-20:] # Aumentei para mostrar os últimos 20, você pode ajustar
        ultimos_itens.reverse()

        for i, item in enumerate(ultimos_itens):
            numero_da_linha = len(todos_os_valores) - i + 1
            itens_com_linha.append((numero_da_linha, item))
    except gspread.exceptions.SpreadsheetNotFound:
        print("Planilha não encontrada. Verifique o nome e o compartilhamento.")
    except Exception as e:
        print(f"Um erro ocorreu ao buscar os dados: {e}")

    # Renderiza a nova página de inventário, passando os itens para a tabela.
    return render_template('inventario.html', items=itens_com_linha)


@app.route('/update', methods=['POST'])
def update():
    try:
        dados = request.form
        numero_da_linha = dados['row_number']
        
        linha_atualizada = [
            dados['unidade'], dados['categoria'], dados['descricao'],
            dados['marca'], dados['n_serie'], dados['estado'],
            dados.get('timestamp', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        ]

        sheet = get_sheet()
        range_para_atualizar = f'A{numero_da_linha}:G{numero_da_linha}'
        sheet.update(range_para_atualizar, [linha_atualizada])
        
        # ATUALIZADO: Redireciona de volta para a página do inventário
        return redirect(url_for('inventario'))

    except Exception as e:
        return f"Ocorreu um erro ao atualizar: {e}"


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Pega os dados comuns do formulário
        unidade = request.form['unidade']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        marca = request.form['marca']
        estado = request.form['estado']
        
        # Pega os novos dados de quantidade e a escolha sobre o serial
        quantidade = int(request.form.get('quantidade', 1))
        serial_igual = request.form.get('serial_igual')

        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        linhas_para_adicionar = []

        if serial_igual == 'sim':
            # Pega o único número de série
            n_serie_unico = request.form['n_serie_unico']
            for _ in range(quantidade):
                nova_linha = [unidade, categoria, descricao, marca, n_serie_unico, estado, timestamp]
                linhas_para_adicionar.append(nova_linha)
        else: # serial_igual == 'nao'
            # Pega a LISTA de números de série
            lista_de_series = request.form.getlist('n_serie_multiplos[]')
            for n_serie in lista_de_series:
                nova_linha = [unidade, categoria, descricao, marca, n_serie, estado, timestamp]
                linhas_para_adicionar.append(nova_linha)

        # Adiciona todas as linhas na planilha de uma vez (mais eficiente!)
        if linhas_para_adicionar:
            sheet = get_sheet()
            # Usamos append_rows para adicionar múltiplas linhas com uma única requisição à API
            sheet.append_rows(linhas_para_adicionar)

        return redirect(url_for('sucesso'))

    except gspread.exceptions.SpreadsheetNotFound:
        return "Erro: A planilha não foi encontrada. Verifique o nome no código e o compartilhamento."
    except Exception as e:
        # Para depuração, é útil ver o erro exato
        print(f"Ocorreu um erro inesperado: {e}")
        return f"Ocorreu um erro inesperado: {e}"

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)