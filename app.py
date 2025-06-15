from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
import json
import os

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'  # Troque por algo mais seguro

# Caminho para o arquivo JSON
ARQUIVO_CONFIRMADOS = 'confirmados.json'

# Carrega a lista de confirmados do arquivo JSON
def carregar_confirmados():
    if os.path.exists(ARQUIVO_CONFIRMADOS):
        with open(ARQUIVO_CONFIRMADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Salva a lista de confirmados no arquivo JSON
def salvar_confirmados(lista):
    with open(ARQUIVO_CONFIRMADOS, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

# Lista de confirmados carregada do arquivo
confirmados = carregar_confirmados()

@app.route('/')
def index():
    mensagem_confirmacao = session.pop('mensagem_confirmacao', None)
    return render_template('index.html', total_confirmados=len(confirmados), mensagem_confirmacao=mensagem_confirmacao)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    if nome:
        confirmados.append(nome)
        salvar_confirmados(confirmados)
        session['mensagem_confirmacao'] = f"Presença confirmada, {nome}! 🎉"
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'Ane2001':
            session['logado'] = True
            return redirect(url_for('lista_confirmados'))
        else:
            return render_template('login.html', erro="Senha incorreta!")
    return render_template('login.html')

@app.route('/confirmados')
def lista_confirmados():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('confirmados.html', nomes=confirmados, total=len(confirmados))

@app.route('/excluir/<int:index>', methods=['POST'])
def excluir(index):
    if not session.get('logado'):
        return redirect(url_for('login'))
    if 0 <= index < len(confirmados):
        del confirmados[index]
        salvar_confirmados(confirmados)
    return redirect(url_for('lista_confirmados'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
