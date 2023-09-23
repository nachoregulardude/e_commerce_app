from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from .models import User, db

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Incorrect username/password', category='error')
        else:
            flash('Login success!')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("login.html", username='bharath', user=current_user)


@auth.route("/logout")
@login_required
def logout():
    flash('Logged out!')
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_data = {
            'email':
            request.form['email'],
            'first_name':
            request.form['first_name'],
            'password':
            generate_password_hash(
                request.form['password'],
                method='sha256',
            )
        }
        password = request.form['password']
        password_confirm = request.form['password1']
        if password != password_confirm:
            flash("Passwords don't match", category='error')
        else:
            if User.query.filter_by(email=user_data['email']).first():
                flash('Email already exists!')
            else:
                new_user = User(**user_data)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created", category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
