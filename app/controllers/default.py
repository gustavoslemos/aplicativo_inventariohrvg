from flask import render_template,flash
from flask.helpers import url_for
from flask.wrappers import Request
from app import app, db,login_manager
from app.models.tables import Inventario
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import url_for
from app.models.forms import *
from flask import Flask, request, url_for, redirect, render_template
import json
from app.models.forms import LoginForm
from app.models.tables import User
from flask_login import login_user, logout_user,login_required


@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        if User.query.filter_by(email=email).first():
            flash("Usuário ja cadastrado!",'danger')
        else:
            user = User(name, email, pwd)
            user.save()
            flash("Dados salvos com sucesso!",'success')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(pwd):
            login_user(user) 
            return redirect(url_for('home'))
        else:
            flash("Verifique suas credenciais",'danger')
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template ("index.html")

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('sem_usuario.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/cadastrar_medicamentos")
@login_required
def cadastrar_medicamentos():
    return render_template("cadastro_medicamentos.html")

@app.route("/cadastro_medicamentos", methods = ['GET', 'POST'])
@login_required
def cadastro_medicamentos():
    
    if request.method == "POST":
        medicamento = request.form.get("medicamento")
        quantidade = request.form.get("quantidade")
        
        if Inventario.query.filter_by(medicamento=medicamento).first():
            flash("Medicamento ja cadastrado!",'danger')

        else:
            
            if medicamento and quantidade:
                i = Inventario(medicamento, quantidade)
                i.save()

                flash("Medicamentos lançados com sucesso!",'success')
                
            else:
                flash("Dados Inválidos",'danger')    
            
    return render_template('cadastro_medicamentos.html')

@app.route("/lista_medicamentos")
@login_required
def lista_medicamentos():
    inventario = Inventario.query.all()
    return render_template("lista_medicamentos.html", inventario=inventario)

def voltar ():
    return render_template("index.html")

@app.route("/excluir/<int:id>")
@login_required
def excluir(id):
    inventario = Inventario.query.filter_by(id=id).first()

    db.session.delete(inventario)
    db.session.commit()

    inventario = Inventario.query.all()
    return render_template ("lista_medicamentos.html", inventario=inventario)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar(id):
    inventario = Inventario.query.filter_by(id = id).first()
    if request.method == "POST":
        medicamento = request.form.get("medicamento")
        quantidade = request.form.get("quantidade")
    
        if medicamento and quantidade:
            inventario.medicamento = medicamento
            inventario.quantidade = quantidade
            inventario.save()

            return redirect(url_for("lista_medicamentos"))
    
    return render_template ("atualizar.html", inventario=inventario)

@app.route("/lancamentos", methods=['GET', 'POST'])
@login_required
def lancamentos():
    form = LancamentoForm()
    if form.validate_on_submit():
        medicamento = Inventario.query.filter_by(medicamento = form.medicamentos.data).first()
        if medicamento:
            if medicamento.quantidade >= form.quantidade.data:
                medicamento.quantidade -= form.quantidade.data
                medicamento.save()
                log = Log(medicamento.id,form.quantidade.data,form.nome_pessoa.data)
                log.save()
                flash("Medicamentos retirados com sucesso!",'success')
            else:
                flash("Quantidade solicitada não disponivel, favor verificar o estoque.",'danger')
        else:
            flash("Medicamento não encontrado.",'danger')

    log = Log.query.all()

    return render_template ("lancamentos.html",form = form,log=log)

@app.route("/devolucoes", methods=['GET', 'POST'])
@login_required
def devolucoes():
    formdev = DevolucaoForm()
    if formdev.validate_on_submit():
        medicamento = Inventario.query.filter_by(medicamento = formdev.medicamentos.data).first()
        if medicamento:
                medicamento.quantidade += formdev.quantidade.data
                medicamento.save()
                dev = Dev(medicamento.id,formdev.quantidade.data,formdev.nome_pessoa_devolucao.data)
                dev.save()
                flash("Medicamentos devolvidos com sucesso!",'success')
        else:
            flash("Medicamento não encontrado.",'danger')

    dev = Dev.query.all()

    return render_template ("devolucoes.html",formdev = formdev,dev=dev)

