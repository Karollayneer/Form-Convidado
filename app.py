from flask import Flask, render_template, request, redirect, url_for # type: ignore

app = Flask(__name__)
confirmados = []

@app.route('/')
def index():
    return render_template('index.html', total_confirmados=len(confirmados))

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form['nome'].strip().upper()
    if nome and nome not in confirmados:
        confirmados.append(nome)
    return redirect(url_for('confirmados_view'))

@app.route('/confirmados')
def confirmados_view():
    return render_template('confirmados.html', lista=confirmados, total=len(confirmados))

@app.route('/excluir/<nome>')
def excluir(nome):
    nome = nome.upper()
    if nome in confirmados:
        confirmados.remove(nome)
    return redirect(url_for('confirmados_view'))

if __name__ == '__main__':
    app.run(debug=True)
