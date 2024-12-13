from flask import Flask, request, render_template, redirect, url_for
import firebase_admin
from firebase_admin import auth, credentials

app = Flask(__name__)

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate("firebase-key.json")  # Substitua pelo caminho do seu arquivo JSON do Firebase
firebase_admin.initialize_app(cred)


@app.route('/')
def index():
    return render_template('registro.html', mensagem="", tipo="")


@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se os campos estão preenchidos
        if not nome or not email or not password:
            return render_template('registro.html', mensagem="Todos os campos são obrigatórios.", tipo="erro")

        # Cria o usuário no Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )

        # Redireciona para a página de login após o cadastro
        return render_template('login.html', mensagem=f"Usuário {nome} cadastrado com sucesso. Faça login para continuar.")

    except Exception as e:
        return render_template('registro.html', mensagem=f"Erro ao cadastrar usuário: {str(e)}", tipo="erro")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se os campos foram preenchidos
        if not email or not password:
            return render_template('login.html', mensagem="E-mail e senha são obrigatórios.", tipo="erro")

        try:
            # Verifica se o e-mail existe no Firebase
            user = auth.get_user_by_email(email)
            
            # Para autenticar a senha, isso precisa ser feito no lado do cliente com o SDK do Firebase para JavaScript
            # Aqui estamos apenas simulando a verificação do e-mail.
            
            if user.email == email:
                # Se o e-mail for encontrado, exibe uma mensagem de boas-vindas (simulação de login bem-sucedido)
                return render_template('dashboard.html', mensagem=f"Bem-vindo, {user.display_name or 'usuário'}!")

        except auth.UserNotFoundError:
            # Se o usuário não for encontrado, exibe uma mensagem de erro
            return render_template('login.html', mensagem="E-mail não registrado. Por favor, faça o cadastro.", tipo="erro")
        
        except Exception as e:
            # Se ocorrer um erro com a senha ou outro erro inesperado
            return render_template('login.html', mensagem="Senha incorreta. Tente novamente.", tipo="erro")

    return render_template('login.html', mensagem="", tipo="")


@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html', mensagem="Cadastro realizado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)

