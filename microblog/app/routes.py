# The routes are the different URLs that the application implements.
# In Flask, handlers for the application routes are written as Python functions,
# called view functions. View functions are mapped to one or more route URLs so
# that Flask knows what logic to execute when a client requests a given URL.

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
# imports the various form types created in forms.py so that they can be used on certain application routes
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, GameForm
from app.models import User, Post
from datetime import datetime
# initial attempt at importing game logic so that it an be returned in the gamepage viewfunction
import game_logic_v2


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# The two strange @app.route lines above the function are decorators, a unique
# feature of the Python language. A decorator modifies the function that follows
# it. A common pattern with decorators is to use them to register functions as
# callbacks for certain events. In this case, the @app.route decorator creates an
# association between the URL given as an argument and the function. In this
# example there are two decorators, which associate the URLs / and /index to
# this function. This means that when a web browser requests either of these two
# URLs, Flask is going to invoke this function and pass the return value of it
# back to the browser as a response.


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    # return render_template() comes from the Flask framework and invokes the jinja2 template
    # engine returns a specific html template from the template folder when the route specified
    # above is called.  the additional arguments included in the function draw on the other
    # code in the view function, and inform what appears in the variable sections of the template's html
    # jinja2 replaces placeholders captured in {{ }} and control statements captured in {% %}
    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


# the form=form argument in a render_template() call passes the form object imported from
# forms.py to the template with the name form so that it can be rendered
# indicating methods =['GET', 'POST'] lets flask know that this view function needs to be
# able to get and post requests (defaults to just 'GET')
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = requests.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# Creating the route needed to support follow functionality
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


# Creating the route needed to support unfollow functionality
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are no longer following {}!'.format(username))
    return redirect(url_for('user', username=username))


# Introduces an 'explore view' for easier discovery of other users
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


# Initial attempt at creating a basic game view function that takes GameForm and renders it on a page
@app.route('/gamepage', methods=['GET', 'POST'])
@login_required
def gamepage():
    form = GameForm()
    if form.validate_on_submit():
        flash('the game would run now')
        return render_template('gamepage.html', title='Game Page', game_output=game_logic_v2.game(5, ['scott', 'nicole', 'jane', 'don', 'meg']))
    return render_template('gamepage.html', title='Game Page', form=form)
