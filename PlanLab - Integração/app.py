import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from conexao import get_db_connection, create_tables

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




@app.route("/")
def index():
    conn = get_db_connection()  # Obtém a conexão com o banco de dados
    planos = conn.execute("SELECT * FROM aula ORDER BY data_aula DESC LIMIT 4").fetchall()  # Recupera os últimos 4 planos de aula do banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

    return render_template("index.html", planos=planos)  # Passa os últimos 4 planos de aula para o template HTML


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login_cadastro")
def login_cadastro():
    return render_template('login_cadastro.html')

@app.route("/formulario", methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        data_aula = request.form['data_aula']
        turma = request.form['turma']
        semestre = request.form['semestre']
        titulo = request.form['titulo']
        conteudo_programatico = request.form['conteudo_programatico']
        metodologia = request.form['metodologia']
        recursos_necessarios = request.form['recursos_necessarios']
        avaliacao_observacoes = request.form['avaliacao_observacoes']
        observacoes = request.form['observacoes']
        eventos_extraordinarios = request.form['eventos_extraordinarios']
        usuario_id = 1  # Substitua pelo ID do usuário logado
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO aula (data_aula, turma, semestre, titulo, conteudo_programatico, metodologia, recursos_necessarios, avaliacao_observacoes, observacoes, eventos_extraordinarios, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data_aula, turma, semestre, titulo, conteudo_programatico, metodologia, recursos_necessarios, avaliacao_observacoes, observacoes, eventos_extraordinarios, usuario_id))
        conn.commit()
        conn.close()
        return redirect(url_for('planos_de_aula'))
    return render_template('formulario.html')

@app.route("/planos_de_aula")
def planos_de_aula():
    conn = get_db_connection()  # Obtém a conexão com o banco de dados
    planos = conn.execute("SELECT * FROM aula").fetchall()  # Recupera os planos de aula do banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

    return render_template("planos_de_aula.html", planos=planos)  # Passa os planos de aula para o template HTML

if __name__ == "__main__":
    app.run(debug=True)
