from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import fdb

app = Flask(__name__, static_folder='Static', template_folder='Templates', static_url_path='/static')

app.config['SECRET_KEY'] = '****'

host = "localhost"
database = r"C:\Users\Aluno\Downloads\bolso-em-dia2-main (1)\Projeto-Solo-J\BANCO.FDB"
user = "sysdba"
password = "sysdba"

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/', methods=['GET', 'POST'])
def pagina_cadastro():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmarSenha']
        Vdiaria = request.form['Vdiaria']
        minPacotes = request.form['minPacotes']
        adicional = request.form['adicional']

        cursor = con.cursor()

        try:
            if senha != confirmar_senha:
                flash('As senhas não são iguais', 'error')
                return redirect(url_for('pagina_cadastro'))

            cursor.execute("""
                INSERT INTO USUARIO
                (NOME_COMPLETO, EMAIL, SENHA, STATUS, VALOR_DIARIA, ADICIONAL, MIN_PACOTES)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, email, senha, 1, Vdiaria, adicional, minPacotes))

            con.commit()
            flash('Cadastro realizado com sucesso', 'success')

            session['informacoes'] = {
                'nome': nome,
                'email': email,
                'senha': senha
            }

        except Exception as erro:
            con.rollback()
            flash(f'Ocorreu um erro: {erro}', 'error')

        finally:
            cursor.close()

        return redirect(url_for('pagina_cadastro'))

    return render_template('cadastro.html')

if __name__ == "__main__":
    app.run(debug=True)
