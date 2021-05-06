from app import db, login_manager
from sqlalchemy import Float,Column,Integer,String,ForeignKey,DateTime,Time,Boolean
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        if self.id is not None:
            db.session.delete(self)
        db.session.commit()

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"<User {self.name}>"
    
class Inventario(db.Model):

    __tablename__ = 'medicamentos'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    medicamento = db.Column(db.String)
    quantidade = db.Column(db.Integer)


    def __init__ (self, medicamento, quantidade):
        self.medicamento = medicamento
        self.quantidade = quantidade
    
    def __repr__(self):
        return "<Inventario %r>" % self.id
  
    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        if self.id is not None:
            db.session.delete(self)
        db.session.commit()

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    id_medicamento = db.Column(db.Integer, ForeignKey('medicamentos.id'))
    quantidade = db.Column(db.String)
    nome_pessoa = db.Column(db.String)
    data = db.Column(db.DateTime,nullable=False)
    medicamento =   db.relationship("Inventario",foreign_keys=id_medicamento)

    def __init__(self, id_medicamento, quantidade, nome_pessoa, data = dt.now()):
        
        self.id_medicamento = id_medicamento
        self.quantidade = quantidade
        self.nome_pessoa = nome_pessoa
        self.data = data

    def __repr__(self):
        return "<Log %r>" % self.id

    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        if self.id is not None:
            db.session.delete(self)
        db.session.commit()
    
    def data_formatada(self):
        return self.data.strftime("%d/%m/%Y")

    @property
    def data_formatada(self):
        return self.data.strftime("%d/%m/%Y, %H:%M")
        
class Dev(db.Model):
    __tablename__ = 'devs'

    id = db.Column (db.Integer, primary_key = True)
    id_medicamento = db.Column(db.Integer, ForeignKey('medicamentos.id'))
    quantidade = db.Column(db.String)
    nome_pessoa_devolucao = db.Column(db.String)
    data = db.Column(db.DateTime,nullable=False)
    medicamento =   db.relationship("Inventario",foreign_keys=id_medicamento)

    def __init__(self, id_medicamento, quantidade, nome_pessoa_devolucao, data = dt.now()):
        
        self.id_medicamento = id_medicamento
        self.quantidade = quantidade
        self.nome_pessoa_devolucao = nome_pessoa_devolucao
        self.data = data

    def __repr__(self):
        return "<Log %r>" % self.id

    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        if self.id is not None:
            db.session.delete(self)
        db.session.commit()

    @property
    def data_formatada(self):
        return self.data.strftime("%d/%m/%Y, %H:%M")