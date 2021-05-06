from flask_wtf import FlaskForm
from flask_wtf import Form
from sqlalchemy.sql.sqltypes import Numeric
from wtforms import StringField, PasswordField, BooleanField,SelectField,IntegerField, DateField
from wtforms.validators import DataRequired,Required
from flask_wtf.file import FileAllowed, FileRequired
from app.models.tables import *


class InventarioForm(FlaskForm):
    medicamento    = StringField("medicamento", validators=[DataRequired()])
    quantidade     = StringField("quantidade", validators=[DataRequired()])

class LancamentoForm(FlaskForm):  
    medicamentos = SelectField(u'medicamentos', choices = [], validators = [Required()])
    quantidade = IntegerField('quantidade',validators = [Required()])
    nome_pessoa = StringField('nome_pessoa',validators = [Required()])

    def __init__(self,*args, **kwargs):
        super(LancamentoForm, self).__init__(*args, **kwargs)
        choices = [x.medicamento for x in Inventario.query.all()]
        self.medicamentos.choices = choices

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class LogForm(FlaskForm):
    id_medicamento             = StringField("nome_medicamento", validators=[DataRequired()])
    quantidade             = StringField("quantidade", validators=[DataRequired()])
    nome_pessoa           = StringField("nome_pessoa", validators=[DataRequired()])
    data            = DateField('Start Date', format='%d/%m/%Y', validators=[DataRequired()])

class DevolucaoForm(FlaskForm):  
    medicamentos = SelectField(u'medicamentos', choices = [], validators = [Required()])
    quantidade = IntegerField('quantidade',validators = [Required()])
    nome_pessoa_devolucao = StringField('nome_pessoa_devolucao',validators = [Required()])

    def __init__(self,*args, **kwargs):
        super(DevolucaoForm, self).__init__(*args, **kwargs)
        choices = [x.medicamento for x in Inventario.query.all()]
        self.medicamentos.choices = choices

class DevForm(FlaskForm):
    id_medicamento             = StringField("nome_medicamento", validators=[DataRequired()])
    quantidade             = StringField("quantidade", validators=[DataRequired()])
    nome_pessoa_devolucao           = StringField("nome_pessoa_devolucao", validators=[DataRequired()])
    data            = DateField('Start Date', format='%d/%m/%Y', validators=[DataRequired()])

