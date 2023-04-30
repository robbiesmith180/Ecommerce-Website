from flask import redirect, render_template, request, session, url_for
from shop.models import Item, User
from shop import app, db

@app.route('/intro')
def intro_page():
    return render_template('intro.html')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/shop')
def shop_page():
    items = Item.query.all()
        
    return render_template('shop.html', items=items)

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home_page'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        error = None

    return render_template('login.html')


@app.route('/poorfromyou')
def funny_page():
    return render_template('funny.html')

@app.route('/register', methods=['POST', 'GET'])
def signup_page():
    if request.method == "POST":
        username = request.form['username']
        email_address = request.form['email_address']
        password1 = request.form['password1']
        password2 = request.form['password2']

        #Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Username already exists'
            return render_template('signup.html', error=error)

        #Check if email exists
        email = User.query.filter_by(email_address=email_address).first()
        if email:
            error = 'Email already exists'
            return render_template('signup.html', error=error)

        #Check if passwords match
        if password1 != password2:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)

        #Add user to database
        new_user = User(username=username, email_address=email_address, password=password1)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home_page'))
    else:
        error = None
        return render_template('signup.html', error=error)
