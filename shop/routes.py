from flask import redirect, render_template, request, session, url_for
from shop.models import Item, User
from shop import app

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

@app.route('/register')
def signup_page():
    return render_template('signup.html')
