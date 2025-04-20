from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'  # Troque por algo mais seguro

# Lista de confirmados (simples, em memória)
confirmados = []

@app.route('/')
def index():
    return render_template('index.html', total_confirmados=len(confirmados))

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    if nome:
        confirmados.append(nome)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'Ane2001':  # Defina sua senha aqui
            session['logado'] = True
            return redirect(url_for('lista_confirmados'))
        else:
            return render_template('login.html', erro="Senha incorreta!")
    return render_template('login.html')

@app.route('/confirmados')
def lista_confirmados():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('confirmados.html', nomes=confirmados)

@app.route('/excluir/<int:index>', methods=['POST'])
def excluir(index):
    if not session.get('logado'):
        return redirect(url_for('login'))
    if 0 <= index < len(confirmados):
        del confirmados[index]
    return redirect(url_for('lista_confirmados'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
