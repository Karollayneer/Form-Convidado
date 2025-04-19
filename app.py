from flask import Flask, render_template, request, redirect
app = Flask(__name__)

confirmados = []

@app.route('/')
def index():
    return render_template('index.html', total_confirmados=len(confirmados))

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form['nome']
    if nome and nome not in confirmados:
        confirmados.append(nome)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
