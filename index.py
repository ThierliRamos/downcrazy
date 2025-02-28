from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta'  # Necessário para gerenciar sessões

def verificar_credenciais(usuario, senha):
    # Lê o arquivo de usuários
    with open('usuarios.txt', 'r') as f:
        for linha in f:
            login, senha_arquivo = linha.strip().split('|')
            if login == usuario and senha_arquivo == senha:
                return True
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if verificar_credenciais(usuario, senha):
            session['logged_in'] = True  # Marca como logado
            return redirect(url_for('main'))
        else:
            return "Usuário ou senha inválidos!"
    return render_template('index.html')

@app.route('/templates/main.html')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redireciona para login se não estiver logado
    return render_template('templates/main.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove a sessão
    return redirect(url_for('login'))  # Redireciona para a página de login

if __name__ == '__main__':
    app.run(debug=True)