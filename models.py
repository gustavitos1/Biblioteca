from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
engine = create_engine('sqlite:///Biblioteca.db')
#db_session = scoped_session(sessionmaker(bind=engine))


#Base.query = db_session.query_property()
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Livro(Base):
    __tablename__ = 'livros'
    id_livro = Column(Integer, primary_key=True)
    isbn = Column(String, unique=True)
    titulo = Column(String, nullable=False, index=True)
    autor = Column(String, nullable=False, index=True)
    resumo = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f'<livro: {self.titulo}, isbn: {self.isbn}, autor: {self.autor}, resumo: {self.resumo}>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize(self):
        dados_Livro = {
            "id_livro": self.id_livro,
            "titulo": self.titulo,
            "isbn": self.isbn,
            "autor": self.autor,
            "resumo": self.resumo
        }
        return dados_Livro

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    papel = Column(String, nullable=False)

    def set_senha_hash(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password_hash(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f'<usuario: {self.nome}, cpf: {self.cpf}, email: {self.email}, papel: {self.papel}, senha: {self.senha}>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize(self):
        dados_Usuario = {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "papel": self.papel
        }
        return dados_Usuario

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id_emprestimo = Column(Integer, primary_key=True)
    data_emprestimo = Column(String, nullable=True)
    data_devolucao = Column(String, nullable=True)
    id_livro = Column(Integer, ForeignKey('livros.id_livro'))
    livro = relationship("Livro")
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = relationship("Usuario")

    def __repr__(self):
        return f'<emprestimo: {self.data_emprestimo}, data_devolução: {self.data_devolucao}>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def serialize(self):
        dados = {
            "id_emprestimo": self.id_emprestimo,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao": self.data_devolucao,
            "id_livro": self.id_livro,
            "id_usuario": self.id_usuario
        }
        return dados

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)