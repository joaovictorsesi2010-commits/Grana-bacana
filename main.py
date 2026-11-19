
#Importa as ferramentas do Flask necessárias.
from flask import Flask, render_template, request, redirect, url_for, flash, session

#Importa funções para proteger e verificar senhas.
from werkzeug.security import generate_password_hash, check_password_hash

import fdb

app = Flask(__name__, static_folder='Static', template_folder='Templates', static_url_path='/static')

app.config['SECRET_KEY'] = '****'

host = "localhost"
database = r"C:\Users\Aluno\Downloads\bolso-em-dia2-main (1)\Projeto-Solo-J\BANCO.FDB"
user = "sysdba"
#Define a senha utilizada para acessar o banco de dados.
password = "sysdba"

#Realiza a conexão com o banco de dados, permitindo que o sistema consulte e cadastre informações.
con = fdb.connect(host=host, database=database, user=user, password=password)

#Define a rota principal do sistema, representada pelo endereço "/".
#methods: tipos de requisição HTTP (mensagem do cliente ao servidor) que aquela rota tem permissão para processar.
#GET: permite acessar a página.
#POST: permite enviar informações preenchidas no formulário.
@app.route('/', methods=['GET', 'POST'])
def pagina_cadastro():
    #Verifica se o formulário foi enviado pelo método POST.
    if request.method == 'POST':
        #Salva o nome, e-mail e senha em variáveis.
        #request.form pega o valor de acordo com "name" no input.
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmarSenha']

        #Pega os valores e tenta converter para float para validar.
        try:
            Vdiaria = float(request.form['Vdiaria'])
            minPacotes = int(request.form['minPacotes'])
            adicional = float(request.form['adicional'])
        except Exception as erro:
            #Caso o usuário digite letras no lugar de números.
            #flash cria uma mensagem temporária.
            #category permite filtrar ou modificar o visual
            flash('Insira apenas números nos campos de valor', 'error')
            return redirect(url_for('pagina_cadastro'))

        #.strip() remove espaços vazios para garantir que não mandaram só " ".
        #if not inverte o resultado do strip (lembrando que null = false)
        if not nome.strip() or not email.strip() or not senha.strip():
            flash('Preencha todos os campos', 'error')
            return redirect(url_for('pagina_cadastro'))

        #Verifica se algum dos valores numéricos é menor ou igual a zero.
        if Vdiaria <= 0 or minPacotes <= 0 or adicional <= 0:
            flash('Os valores não podem ser negativos ou 0.', 'error')
            return redirect(url_for('pagina_cadastro'))

        #Cria um cursor para executar comandos no banco.
        cursor = con.cursor()

        #Inicia o tratamento de erros.
        try:
            #Verifica se a senha e a confirmação são diferentes.
            if senha != confirmar_senha:
                #Mesma lógica de antes, só que para senhas diferentes.
                flash('As senhas não são iguais', 'error')
                #Retorna para a página de cadastro.
                #url_for cria o caminho para uma função.
                return redirect(url_for('pagina_cadastro'))

            #Criptografa a senha
            senha_hash = generate_password_hash(senha)

            #Executa um comando para inserir um novo usuário no banco.
            cursor.execute("""
                --Informa onde os dados serão cadastrados.
                INSERT INTO USUARIO
                --Define as colunas que receberão os valores.
                (NOME_COMPLETO, EMAIL, SENHA, STATUS, VALOR_DIARIA, ADICIONAL, MIN_PACOTES)
                --Define os valores que serão inseridos em cada coluna.
                --Cada ? representa um valor que será enviado.
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, email, senha_hash, 1, Vdiaria, adicional, minPacotes))

            #Confirma e salva as alterações no banco de dados.
            con.commit()

            #Exibe uma mensagem informando que o cadastro foi realizado com sucesso.
            flash('Cadastro realizado com sucesso', 'success')

            #Guarda algumas informações do usuário na sessão.
            #A senha não é armazenada na sessão por segurança.
            session['informacoes'] = {
                'nome': nome,
                'email': email
            }

        #Caso aconteça algum erro durante o cadastro, executa este bloco.
        except Exception as erro:
            #Cancela as alterações realizadas no banco de dados.
            con.rollback()

            #Exibe uma mensagem informando qual erro aconteceu.
            flash(f'Ocorreu um erro: {erro}', 'error')

        #O finally é executado independentemente de ocorrer um erro ou não.
        finally:
            #Fecha o cursor para liberar o recurso utilizado.
            cursor.close()

        #Redireciona o usuário novamente para a página de cadastro.
        return redirect(url_for('pagina_cadastro'))

    #Caso o usuário apenas acesse a página, sem enviar o formulário,
    #carrega o arquivo cadastro.html.
    return render_template('cadastro.html')


#Verifica se o arquivo está sendo executado diretamente.
if __name__ == "__main__":
    #Inicia o servidor Flask em modo de desenvolvimento.
    app.run(debug=True)
