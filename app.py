import os
import json
import gspread
from flask import Flask, render_template, request, redirect, url_for, jsonify
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
# --- CONFIGURAÇÃO DO GOOGLE SHEETS (versão para Vercel) ---
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # VERIFICA SE ESTAMOS NO AMBIENTE DA VERCEL
    # A Vercel define a variável 'VERCEL' automaticamente.
    # LÓGICA PARA A VERCEL (usa a variável de ambiente)
    creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json_str:
        raise Exception("Vercel: Variável GOOGLE_CREDENTIALS_JSON não encontrada.")
    creds_dict = json.loads(creds_json_str)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    sheet = client.open("Levantamento de Bens - FUNDEC").sheet1 
    return sheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    # A página agora carrega TODOS os itens via JS a partir do endpoint /api/items
    return render_template('inventario.html')

# API: retorna todos os itens como JSON (incluindo número da linha)
@app.route('/api/items')
def api_items():
    try:
        sheet = get_sheet()
        all_values = sheet.get_all_values()
        if not all_values:
            return jsonify(items=[])
        headers = all_values[0]
        rows = all_values[1:]
        items = []
        for idx, row in enumerate(rows, start=2):  # row 1 = headers, dados iniciam em 2
            # Garante que o row tenha o mesmo tamanho dos headers
            padded = row + [""] * (len(headers) - len(row))
            item = {
                "row_number": idx,
                "unidade": padded[0],
                "categoria": padded[1],
                "descricao": padded[2],
                "marca": padded[3],
                "n_serie": padded[4],
                "estado": padded[5],
                "timestamp": padded[6] if len(padded) > 6 else ""
            }
            items.append(item)
        return jsonify(items=items)
    except gspread.exceptions.SpreadsheetNotFound:
        return jsonify(error="Planilha não encontrada"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# API: atualiza uma linha pelo número da linha (JSON)
@app.route('/api/update_row', methods=['POST'])
def api_update_row():
    try:
        data = request.get_json()
        if not data or 'row_number' not in data:
            return jsonify(error="Parâmetros inválidos"), 400

        row_number = int(data['row_number'])
        linha_atualizada = [
            data.get('unidade', ""),
            data.get('categoria', ""),
            data.get('descricao', ""),
            data.get('marca', ""),
            data.get('n_serie', ""),
            data.get('estado', ""),
            data.get('timestamp', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        ]

        sheet = get_sheet()
        range_para_atualizar = f'A{row_number}:G{row_number}'
        sheet.update(range_para_atualizar, [linha_atualizada])

        return jsonify(success=True)
    except gspread.exceptions.SpreadsheetNotFound:
        return jsonify(error="Planilha não encontrada"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

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
        
        return redirect(url_for('inventario'))

    except Exception as e:
        return f"Ocorreu um erro ao atualizar: {e}"


@app.route('/submit', methods=['POST'])
def submit():
    try:
        unidade = request.form['unidade']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        marca = request.form['marca']
        estado = request.form['estado']
        
        quantidade = int(request.form.get('quantidade', 1))
        serial_igual = request.form.get('serial_igual')

        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        linhas_para_adicionar = []

        if serial_igual == 'sim':
            n_serie_unico = request.form['n_serie_unico']
            for _ in range(quantidade):
                nova_linha = [unidade, categoria, descricao, marca, n_serie_unico, estado, timestamp]
                linhas_para_adicionar.append(nova_linha)
        else:
            lista_de_series = request.form.getlist('n_serie_multiplos[]')
            for n_serie in lista_de_series:
                nova_linha = [unidade, categoria, descricao, marca, n_serie, estado, timestamp]
                linhas_para_adicionar.append(nova_linha)

        if linhas_para_adicionar:
            sheet = get_sheet()
            sheet.append_rows(linhas_para_adicionar)

        return redirect(url_for('sucesso'))

    except gspread.exceptions.SpreadsheetNotFound:
        return "Erro: A planilha não foi encontrada. Verifique o nome no código e o compartilhamento."
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return f"Ocorreu um erro inesperado: {e}"

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)
