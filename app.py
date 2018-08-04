#coding:utf-8

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Pessoa(db.Model):

	__tablename__ = 'cliente'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String)
	data = db.Column(db.String)
	cpf = db.Column(db.String)
	conta = db.Column(db.String)

	def __init__(self, nome, data, cpf, conta):
		self.nome  =nome
		self. data = data
		self.cpf = cpf
		self.conta = conta

class Conta(db.Model):

	__tablename__= 'contasbanco'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	numero = db.Column(db.String)
	nomebanco = db.Column(db.String)
	agencia = db.Column(db.String)
	numeroconta = db.Column(db.String)


	def __init__(self, numero, nomebanco, agencia, numeroconta):
		self.numero = numero
		self.nomebanco = nomebanco
		self.agencia = agencia
		self.numeroconta = numeroconta




db.create_all()

@app.route("/cadastroconta")
def cadastroconta():
	return render_template("cadastroconta.html")


@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/pesquisacpf")
def pesquisacpf():
	return render_template("pesquisacpf.html")


@app.route("/cadastrar")
def cadastrar():
	return render_template("cadastro.html")

@app.route("/cadastro", methods = ['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		nome = request.form.get("nome")
		data = request.form.get("data")
		cpf = request.form.get("cpf")
		conta = request.form.get("conta")

		if nome and data and cpf and conta :
			p = Pessoa(nome, data, cpf, conta)
			db.session.add(p)
			db.session.commit()

	return redirect(url_for("lista"))


@app.route("/cadastrarconta", methods= ['GET', 'POST'])
def cadastrarconta():
	if request.method == "POST":
		numero = request.form.get("numero")
		nomebanco = request.form.get("nomebanco")
		agencia = request.form.get("agencia")
		numeroconta = request.form.get("numeroconta")

		if numero and nomebanco and agencia and numeroconta:
			c = Conta(numero, nomebanco, agencia, numeroconta)
			db.session.add(c)
			db.session.commit()

	return redirect(url_for("listaconta"))




@app.route("/pesquisarcpf", methods = ['POST','GET'])
def pesquisarcpf():
	if request.method == "POST":
		cpf = request.form.get("cpf")
		pessoa = Pessoa.query.filter_by(cpf=cpf).first()
		return render_template("pesquisarcpf.html", pessoa=pessoa)

	return render_template("pesquisarcpf.html")










@app.route("/lista")
def lista():
	pessoas = Pessoa.query.all()
	return render_template("lista.html", pessoas=pessoas)

@app.route("/listaconta")
def listaconta():
	contas = Conta.query.all()
	return render_template("listaconta.html", contas=contas)



@app.route("/excluir/<int:id>") ##funcao excluir 
def excluir(id):
	pessoa = Pessoa.query.filter_by(_id=id).first()

	db.session.delete(pessoa)
	db.session.commit()


	pessoas = Pessoa.query.all()
	return render_template("lista.html", pessoas=pessoas)


@app.route("/excluirconta/<int:id>") ##funcao excluir 
def excluirconta(id):
	conta = Conta.query.filter_by(_id=id).first()

	db.session.delete(conta)
	db.session.commit()


	contas = Conta.query.all()
	return render_template("listaconta.html", contas=contas)



@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	pessoa = Pessoa.query.filter_by(_id=id).first()

	if request.method == "POST":
		nome = request.form.get("nome")
		data = request.form.get("data")
		conta = request.form.get("conta")

		if nome and data and conta :
			pessoa.nome = nome
			pessoa.data = data
			pessoa.conta= conta

			db.session.commit()

			return redirect(url_for("lista"))

	return render_template("atualizar.html", pessoa= pessoa)


@app.route("/atualizarconta/<int:id>", methods=['GET', 'POST'])
def atualizarconta(id):
	conta = Conta.query.filter_by(_id=id).first()

	if request.method == "POST":
		numero = request.form.get("numero")
		nomebanco = request.form.get("nomebanco")
		agencia = request.form.get("agencia")
		numeroconta = request.form.get("numeroconta")

		if numero and nomebanco and agencia and numeroconta :
			conta.numero = numero
			conta.nomebanco = nomebanco
			conta.agencia= agencia
			conta.numeroconta = numeroconta

			db.session.commit()

			return redirect(url_for("listaconta"))

	return render_template("atualizarconta.html", conta= conta)










if __name__ == '__main__':
	app.run(debug=True)


