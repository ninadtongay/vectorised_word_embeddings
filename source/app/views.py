# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory, jsonify
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Query processing routes
@app.route('/execute', methods=['GET'])
def execute():
    from app.business_logic.vecnlp import entrypoint
    os.remove('position_city_database_with_embeddings.db')
    n1 = request.args.get('n1')
    n2 = request.args.get('n2')
    choice = request.args.get('choice')
    city = request.args.get('city')
    post = request.args.get('post')
    thresh = request.args.get('thresh')
    expected_output_city = request.args.getlist('expected_output_city')
    expected_output_post = request.args.getlist('expected_output_post')
    print(expected_output_post)
    print(expected_output_city)
    response = entrypoint(int(n1),int(n2),choice,city,post,float(thresh), expected_output_city, expected_output_post)
    return jsonify(response)


@app.route('/get_all_items', methods=['GET'])
def get_all_items():
    from app.dashboard_controller import get_all_items
    response = [z.to_json() for z in get_all_items()]
    return jsonify(response)

@app.route('/delete_item', methods=['GET'])
def delete_item():
    from app.dashboard_controller import delete_item
    item_id = request.args.get('item_id')
    response = [z.to_json() for z in delete_item(item_id)]
    return jsonify(response)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    from app.dashboard_controller import add_new_item
    item_type = request.args.get('item_type')
    item_name = request.args.get('item_name')
    item_price = request.args.get('item_price')

    result = add_new_item(item_type, item_name, item_price)
    response = [z.to_json() for z in result]
    return jsonify(response)

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))
            
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'pages/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        company_name = request.form.get('company_name', '', type=str)
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str)
        role    = request.form.get('role'   , '', type=str)
        phone    = request.form.get('phone'   , '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(name=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(company_name, username, email, phone, pw_hash, role)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'pages/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(name=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'pages/login.html', form=form, msg=msg )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None
    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template( 'pages/'+path )
    
    except:
        
        return render_template( 'pages/error-404.html' )

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
