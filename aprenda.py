#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for, \
    g, flash
import db, hashlib

app = Flask(__name__)
app.secret_key = '\xdb\xa5{\xa1\xa6\x7f\xe6\x9c\xc6\xa0\x8e=]\x9a\x0c\x97 >\xaf\xe9\xa9\tyk'

def check_password_hash(senhaform, senhabd):
    m = hashlib.md5()
    m.update(senhaform)
    senhaform = m.hexdigest()
    return senhaform == senhabd

@app.before_request
def before_request():
    g.usuario = None
    if 'nomeusuario' in session:
        print "Ta na sessuam"
        g.usuario = db.get_usuario(session['nomeusuario'])


@app.route('/')
def index():
    dbtopicos = db.get_topicos()
    return render_template('topicos.html', topicos = dbtopicos)

@app.route('/t/<int:topicoid>')
def topico(topicoid):
    dbtopico = db.get_topico(topicoid)
    dblivros = db.get_livros_topico(topicoid)
    return render_template('topico.html', topico = dbtopico)

@app.route('/livro/<int:isbn>')
def livro(isbn):
    pass

@app.route('/link/<linkid>')
def link(linkid):
    pass

@app.route('/logreg', methods=['GET', 'POST'])
def logreg():
    if g.usuario:
        return redirect(url_for('/'))
    error = None
    if request.method == 'POST':
        if request.form['btn'] == 'reg':
            valido = db.validar_usuario(request.form['nomeusuario'],
                    request.form['email'])
            if valido:
                print "Aee"
            else:
                print "Ahh"
        elif request.form['btn'] == 'log':
            usuario = db.get_usuario(request.form['nomeusuario'])
            if usuario == None:
                print "Usuário inválido"
                erro = "Usuário inválido"
            elif not check_password_hash(request.form['password'], usuario['senha']):
                print "Senha incorreta"
                erro = "Senha incorreta"
            else:
                session['nomeusuario'] = usuario['nome_usuario']
                return redirect(url_for('index'))

    return render_template('logreg.html', error=error)

@app.route('/logout')
def logout():
    flash('You were logged out')
    session.pop('nomeusuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
