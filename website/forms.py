from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
# ***********************************************************************************************
# FORMULARIO LOGIN
# ***********************************************************************************************
class FormLogin(FlaskForm):
	email = EmailField(
		'Email',
		validators = [
		DataRequired(message=('Este campo é obrigatório!')),
		Email(message=('Digite um email válido!')),
		])
	senha = PasswordField(
		'Senha',
		validators = [
		DataRequired(message=('Este campo é obrigatório!')),
		Length(min=6, message=('Pelo menos 6 caracteres!'))
		])

# ***********************************************************************************************
# FORMULARIO CADASTRO USUARIOS
# ***********************************************************************************************
class CadastroUsuario(FlaskForm):
	nome = StringField(
		'Nome',
		validators= [
		DataRequired(message=("Este campo é obrigatório!")),
		Length(min=4, message=("Pelo menos 4 caracteres!"))
		])
	email = EmailField(
		'Email',
		validators = [
		DataRequired(message=('Este campo é obrigatório!')),
		Email(message=('Digite um email válido!')),
		])
	senha = PasswordField(
		'Senha',
		validators = [
		DataRequired(message=('Este campo é obrigatório!')),
		Length(min=6, message=('Pelo menos 6 caracteres!')),
		EqualTo('confirmar', message=("Senhas não conferem!"))
		])
	confirmar = PasswordField(
		'Senha (Confirmar)',
		validators = [
		DataRequired(message=('Este campo é obrigatório!')),
		Length(min=6, message=('Pelo menos 6 caracteres!'))
		])

# ***********************************************************************************************
# FORMULARIO CADASTRO CLIENTES
# ***********************************************************************************************
class CadastroCliente(FlaskForm):
	nome = StringField(
	'Nome',
	validators= [
	DataRequired(message=("Este campo é obrigatório!")),
	Length(min=4, message=("Pelo menos 4 caracteres!"))
	])
	fone = StringField(
	'Celuar',
	validators= [
	DataRequired(message=("Este campo é obrigatório!")),
	Length(min=16,max=16, message=("Número celuar inválido!"))
	])

