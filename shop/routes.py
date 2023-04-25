from flask import render_template
from shop.models import Item
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

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/poorfromyou')
def funny_page():
    return render_template('funny.html')

@app.route('/register')
def signup_page():
    return render_template('signup.html')
