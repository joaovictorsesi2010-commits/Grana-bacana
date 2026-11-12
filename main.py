# Importa as ferramentas do Flask necessárias.
from flask import Flask, render_template, request, redirect, url_for, flash, session
# Importa funções para criptografar e verificar senhas.
from werkzeug.security import generate_password_hash, check_password_hash
# Importa a biblioteca responsável pela conexão com o banco de dados.
import fdb

# Cria a aplicação flask.
# static_folder: indica a pasta onde ficam os arquivos estáticos (CSS, JS e imagens).
# template_folder: indica a pasta onde ficam os arquivos HTML.
# static_url_path: define o endereço utilizado para acessar os arquivos estáticos.
app = Flask(__name__, static_folder='Static', template_folder='Templates', static_url_path='/static')

# Define uma chave secreta utilizada pelo Flask para proteger sessões e mensagens.
# Ela deve ser mantida em segredo.
app.config['SECRET_KEY'] = '****'

# Define o endereço do computador onde está o banco de dados.
host = "localhost"
# Informa o caminho do arquivo do banco de dados.
database = r"C:\Users\Aluno\Downloads\Grana-bacana-main\Grana-bacana-main\BANCO.FDB"
# Define o usuário utilizado para acessar o banco de dados.
user = "sysdba"
# Define a senha utilizada para acessar o banco de dados.
password = "sysdba"

# Realiza a conexão com o banco de dados, permitindo que o sistema consulte e cadastre informações.
con = fdb.connect(host=host, database=database, user=user, password=password)


# Define a rota principal do sistema, representada pelo endereço "/".
# methods: tipos de requisição HTTP que aquela rota tem permissão para processar.
# GET: permite acessar a página.
# POST: permite enviar informações preenchidas no formulário.
@app.route('/', methods=['GET', 'POST'])
def pagina_cadastro():
    # Verifica se o formulário foi enviado pelo metodo POST.
    if request.method == 'POST':
        # Salva o nome, e-mail e senha em variáveis.
        # request.form pega o valor de acordo com "name" no input
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Pega a confirmação da senha.
        confirmar_senha = request.form['confirmarSenha']
        # Pega o valor da diária.
        Vdiaria = request.form['Vdiaria']
        # Pega a quantidade mínima de pacotes.
        minPacotes = request.form['minPacotes']
        # Pega o valor adicional.
        adicional = request.form['adicional']

        # Cria um cursor para executar comandos SQL no banco de dados.
        cursor = con.cursor()

        # Inicia um bloco de tratamento de erros.
        try:

            # Verifica se a senha e a confirmação são diferentes.
            if senha != confirmar_senha:
                # Exibe uma mensagem informando que as senhas não são iguais.
                flash('As senhas não são iguais', 'error')
                # Retorna para a página de cadastro.
                return redirect(url_for('pagina_cadastro'))

            # Executa um comando SQL para inserir um novo usuário no banco.
            cursor.execute("""
                # Informa a tabela onde os dados serão cadastrados.
                INSERT INTO USUARIO
                # Define as colunas que receberão os valores.
                (NOME_COMPLETO, EMAIL, SENHA, STATUS, VALOR_DIARIA, ADICIONAL, MIN_PACOTES)
                # Define os valores que serão inseridos em cada coluna.
                # Cada interrogação (?) representa um valor que será enviado depois.
                VALUES (?, ?, ?, ?, ?, ?, ?)
            # Envia os valores na mesma ordem das colunas acima.
            """, (nome, email, senha, 1, Vdiaria, adicional, minPacotes))

            # Confirma e salva definitivamente as alterações no banco de dados.
            con.commit()
            # Exibe uma mensagem informando que o cadastro foi realizado.
            flash('Cadastro realizado com sucesso', 'success')

            # Guarda algumas informações do usuário na sessão.
            # A sessão permite manter informações disponíveis entre páginas.
            session['informacoes'] = {
                # Guarda o nome do usuário.
                'nome': nome,
                # Guarda o e-mail do usuário.
                'email': email,
                # Guarda a senha do usuário.
                'senha': senha
            }


        # Caso aconteça algum erro durante o cadastro, executa este bloco.
        except Exception as erro:
            # Desfaz as alterações feitas no banco caso ocorra um erro.
            con.rollback()
            # Exibe uma mensagem mostrando qual foi o erro encontrado.
            flash(f'Ocorreu um erro: {erro}', 'error')


        # Este bloco é executado independentemente de ter ocorrido um erro ou não.
        finally:
            # Fecha o cursor para liberar os recursos utilizados.
            cursor.close()
        # Redireciona o usuário novamente para a página de cadastro.
        return redirect(url_for('pagina_cadastro'))

    # Se a página for acessada sem enviar o formulário (GET),
    # carrega o arquivo cadastro.html.
    return render_template('cadastro.html')


# Verifica se este arquivo está sendo executado diretamente.
if __name__ == "__main__":
    # Inicia o servidor Flask.
    # debug=True permite visualizar erros e atualiza o servidor
    # automaticamente quando o código é alterado.
    app.run(debug=True)
