from functools import wraps
from flask import session, redirect, url_for, flash, request

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta funcionalidade.', 'error')
            return redirect(url_for('usuarios.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
