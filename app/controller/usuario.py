from app.models.usuario import db, Usuario
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import session_required
import re

user_bp = Blueprint("usuarios", __name__)


@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'usuario_id' in session:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar-senha')

        if not nome or not senha or not confirmar_senha:
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        # Não permitir espaços em nome ou senha
        if re.search(r"\s", nome) or re.search(r"\s", senha):
            flash('Nome de usuário e senha não podem conter espaços.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        # Verificar tamanho mínimo da senha
        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        # Verificar ao menos um símbolo especial na senha
        if not re.search(r"[^A-Za-z0-9]", senha):
            flash('A senha deve conter ao menos um símbolo especial.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        if Usuario.query.filter_by(nome=nome).first():
            flash('Nome de usuário já existe. Escolha outro.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        if senha != confirmar_senha:
            flash('Senhas divergentes.', 'error')
            return redirect(url_for('usuarios.cadastro'))

        usuario = Usuario(nome, senha)
        db.session.add(usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('usuarios.login'))

    return render_template('cadastro.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if not nome or not senha:
            flash('Informe nome de usuário e senha.', 'error')
            return redirect(url_for('usuarios.login'))

        # Rejeitar entradas com espaços (não permitido)
        if re.search(r"\s", nome) or re.search(r"\s", senha):
            flash('Nome de usuário e senha não podem conter espaços.', 'error')
            return redirect(url_for('usuarios.login'))

        usuario = Usuario.query.filter_by(nome=nome).first()

        if usuario and usuario.check_password(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            next_page = request.args.get('next')
            flash(f'Bem vindo, {nome}!', 'success')
            return redirect(next_page or url_for('home.home'))

        flash('Nome de usuário ou senha inválidos.', 'error')
        return redirect(url_for('usuarios.login'))

    return render_template('login.html')


@user_bp.route('/logout')
@session_required
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home.home'))

