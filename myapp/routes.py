from flask import render_template, flash, redirect, url_for, request
from myapp import app, db
from myapp.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from myapp.models import User, Post
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required

def index():
    posts = []
    posts_list = Post.query.all()
    for post in posts_list:
        user = User.query.filter_by(id=post.user_id).first()
        posts.append({
            'author': user.first_name,
            'subject': post.subject,
            'title': post.title,
            'body': post.body})
    return render_template('index.html', title='Hysterical Caracal', posts=posts)

@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/new_post', methods=['GET', 'POST'])

def new_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(title = form.title.data, body = form.body.data,\
            subject = form.subject.data, user_id = current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form)
