from flask import Flask, jsonify, request
from sqlalchemy import *
from flask_pydantic_spec import FlaskPydanticSpec
from sqlalchemy.orm import Session

from models import *
from datetime import *
from _strptime import *
from dateutil.relativedelta import *
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps

app = Flask(__name__)
spec = FlaskPydanticSpec(
    'flask',
    title='Biblioteca API',
    version='1.0',
)
spec.register(app)
app.config['JWT_SECRET_KEY'] = '12tresquatro56'
jwt = JWTManager(app)

@app.route('/')
def index():
    return 'Bem vindo a Biblioteca'

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    nome = dados['nome']
    senha = dados['senha']

    db_session = SessionLocal()

    try:
        sql = select(Usuario).where(Usuario.nome == nome)
        user = db_session.execute(sql).scalar()

        if user and user.check_password_hash(senha):
            acess_token = create_access_token(identity=str(user.email))
            return jsonify(acess_token=acess_token)
        return jsonify({"msg":"Credenciais invalidas"}), 401

    finally:
        db_session.close()
@app.route("/cadastrar_usuario", methods=['POST'])
#@jwt_required()
# @admin_required
def cadastrar_usuario():
    """
    Cadastrar Usuario

    Endpoint:
    POST /cadastrar_usuario

    Parameters:
    none

    resposta JSON:
    {
        "Nome": douglas,
        "CPF": 128202523,
        "Endereco": Rua cabral
    }
    :return:
    """
    db_session = SessionLocal()
    try:
        dados_Usuario = request.get_json()
        nome = dados_Usuario['nome']
        cpf = dados_Usuario['cpf']
        email = dados_Usuario['email']
        senha = dados_Usuario['senha']
        papel = dados_Usuario['papel']
        if not nome or not cpf or not email or not senha or not papel:
            return jsonify({"mensagem": "Preencha todos os campos"}), 400
        form_evento = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha,
            papel=papel
        )

        user_id = form_evento.id_usuario
        form_evento.save(db_session)
        form_evento.set_senha_hash(senha)
        db_session.add(form_evento)
        db_session.commit()
        return jsonify({"mensagem": "Usuário criado com sucesso", "user_id": user_id}), 201

    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"})
    finally:
        db_session.close()


@app.route("/cadastrar_livro", methods=['POST'])
def cadastrar_livro():
    """
    Cadastrar Livro

    Endpoint:
    POST /cadastrar_livro

    parametros:
    none

    resposta JSON:
    {
        "ISBN": douglas,
        "titulo": A arte da guerra,
        "autor": Sun Tzu,
        "resumo": dicas de guerra para a vida,
    }
    :return:
    """
    db_session = SessionLocal()
    try:
        dados_livro = request.get_json()
        isbn = dados_livro['isbn']
        titulo = dados_livro['titulo']
        autor = dados_livro['autor']
        resumo = dados_livro['resumo']
        if not isbn and not titulo and not autor and not resumo:
            return jsonify({"mensagem": "Preencha todos os campos"}), 400

        # Verificar se o ISBN ja existe
        isbn_check = select(Livro).where(Livro.isbn == isbn)
        livro_existente = db_session.execute(isbn_check).scalar()
        if livro_existente:
            return jsonify({"mensagem": "ISBN já cadastrado"}), 400

        form_evento = Livro(
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                resumo=resumo
            )
        form_evento.save(db_session)
        return jsonify({"mensagem": "livro cadastrado com sucesso"}), 201
    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"})
    finally:
        db_session.close()

@app.route("/cadastrar_emprestimo", methods=['POST'])
def cadastrar_emprestimo():
    """
    Cadastrar Emprestimo

    Endpoint:
    POST /cadastrar_emprestimo

    parametros:
    none

    resposta JSON:
    {
        "data_emprestimo": 12/04/2020,
        "data_devolucao": 27/04/2020,
        "id_usuario": 1,
        "id_livro": 2,
    }
    :return:
    """
    db_session = SessionLocal()
    try:
        dados_emprestimo = request.get_json()
        data_emprestimo = dados_emprestimo['Data_Emprestimo']
        data_devolucao = dados_emprestimo['Data_Devolucao']
        id_usuario = dados_emprestimo['id_usuario']
        id_livro = dados_emprestimo['id_livro']
        if not data_emprestimo and not data_devolucao and not id_usuario and not id_livro:
            return jsonify({"mensagem": "Preencha todos os campos"})
        form_evento = Emprestimo(
                    data_emprestimo=data_emprestimo,
                    data_devolucao=data_devolucao,
                    id_livro=id_livro,
                    id_usuario=id_usuario
                )
        form_evento.save(db_session)
        return jsonify({"mensagem": "emprestimo cadastrado com sucesso"}), 201
    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"}), 400
    finally:
        db_session.close()


@app.route("/livros", methods=['GET'])
def livros():
    """
    Listar Livros

    Endpoint:
    GET /livros

    parametros:
    none

    resposta JSON:

    :return:
    """
    db_session = SessionLocal()
    sql_livros = Select(Livro)
    lista_livros = db_session.execute(sql_livros).scalars().all()
    print(lista_livros)
    resultado = []
    for livro in lista_livros:
        resultado.append(livro.serialize())
    print(resultado)
    return jsonify(resultado), 200

@app.route("/usuarios", methods=['GET'])
# @jwt_required()
def usuarios():
    """
    listar Usuarios

    Endpoint:
    GET /usuarios

    parametros:
    none

    resposta JSON:

    :return:
    """
    db_session = SessionLocal()
    sql_usuarios = Select(Usuario)
    lista_usuarios = db_session.execute(sql_usuarios).scalars().all()
    print(lista_usuarios)
    resultado = []
    for usuario in lista_usuarios:
        resultado.append(usuario.serialize())
    print(resultado)
    return jsonify(resultado), 200


@app.route("/emprestimos", methods=['GET'])
def emprestimos():
    """
    listar Emprestimos

    Endpoint:
    GET /emprestimos

    parametros:
    none

    resposta JSON:

    :return:
    """
    db_session = SessionLocal()
    sql_emprestimos = Select(Emprestimo)
    lista_emprestimos = db_session.execute(sql_emprestimos).scalars().all()
    print(lista_emprestimos)
    resultado = []
    for emprestimo in lista_emprestimos:
        resultado.append(emprestimo.serialize())
    print(resultado)
    return jsonify(resultado), 200

@app.route("/editar_usuario/<int:id_usuario>", methods=['PUT'])
@jwt_required()
def editar_usuario(id_usuario):
    """
    Editar Usuario

    Endpoint:
    PUT /editar_usuario/<id_usuario>

    parametros:
    id_usuario

    resposta JSON:

    :param id_usuario:
    :return:
    """
    db_session = SessionLocal()
    usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == id_usuario)).scalar()

    if usuario is None:
        return jsonify({"mensagem": "Usuario nõo encontrado"})

    dados_usuario = request.get_json()
    nome = dados_usuario['nome']
    cpf = dados_usuario['cpf']
    email = dados_usuario['email']

    usuario.nome = nome
    usuario.cpf = cpf
    usuario.email = email

    usuario.save()
    return jsonify({"mensagem": "usuario editado com sucesso"})

@app.route("/editar_livro/<int:id_livro>", methods=['PUT'])
def editar_livro(id_livro):
    """
    Editar Livro

    Endpoint:
    PUT /editar_livro/<id_livro>

    parametros:
    id_livro

    resposta JSON:

    :param id_livro:
    :return:
    """
    db_session = SessionLocal()
    livro = db_session.execute(select(Livro).where(Livro.id_livro == id_livro)).scalar()

    if livro is None:
        return jsonify({"mensagem": "Livro nõo encontrado"})

    dados_livro = request.get_json()
    isbn = dados_livro['isbn']
    titulo = dados_livro['titulo']
    autor = dados_livro['autor']
    resumo = dados_livro['resumo']

    livro.isbn = isbn
    livro.titulo = titulo
    livro.autor = autor
    livro.resumo = resumo

    livro.save()
    return jsonify({"mensagem": "livro editado com sucesso"})


@app.route("/deletar_usuario/<int:id_usuario>", methods=['DELETE'])
def deletar_usuario(id_usuario):
    db_session = SessionLocal()
    try:
        usuario = db_session.query(Usuario).get(id_usuario)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404

        db_session.delete(usuario)
        db_session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir usuário: {str(e)}"}), 500
    finally:
        db_session.close()

@app.route("/deletar_livro/<int:id_livro>", methods=['DELETE'])
def deletar_livro(id_livro):
    db_session = SessionLocal()
    try:
        livro = db_session.select(Livro).get(id_livro)
        if not livro:
            return jsonify({"message": "Livro não encontrado"}), 404

        db_session.delete(livro)
        db_session.commit()
        return jsonify({"message": "Livro excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir o livro: {str(e)}"}), 500
    finally:
        db_session.close()

@app.route("/deletar_emprestimo/<int:id_emprestimo>", methods=['DELETE'])
def deletar_emprestimo(id_emprestimo):
    db_session = SessionLocal()
    try:
        emprestimo = db_session.query(Usuario).get(id_emprestimo)
        if not emprestimo:
            return jsonify({"message": "Emprestimo não encontrado"}), 404

        db_session.delete(emprestimo)
        db_session.commit()
        return jsonify({"message": "Emprestimo excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir emprestimo: {str(e)}"}), 500
    finally:
        db_session.close()

def status_emprestimo(id_emprestimo, dia, mes, ano):
    try:
        emprestimo = datetime.now().date()
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
        data_devolucao = datetime(ano, mes, dia).date()
        data_atual = datetime.now().date()

        validade_prazo = 15
        data_validade = data_devolucao + relativedelta(days=validade_prazo)


    except Exception as e:
        return jsonify({"message": f"Erro ao excluir emprestimo: {str(e)}"}), 500










if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)