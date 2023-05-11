import sqlite3
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from shop.models import Item, User
from shop import app, db


@app.route('/intro')
def intro_page():
    #Return Intro Page
    return render_template('intro.html')

@app.route('/home')
def home_page():
    #Return Home Page
    return render_template('home.html')

@app.route('/shop')
def shop_page():
    #Get all items and item info from database
    items = Item.query.all()
        
    return render_template('shop.html', items=items)

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Check if username exists
        user = User.query.filter((User.username == username) | (User.email_address == username)).first()
        #Check if password is correct
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('clear_cart'))
        else:
            #If username or password is incorrect
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        error = None

    return render_template('login.html')

@app.route('/logout')
def logout():
    #Remove user from session
    session.pop('user_id', None)
    #Clears Current Cart
    return redirect(url_for('clear_cart'))

@app.route('/item/<int:item_id>')
def item_info(item_id):
    #Get item info from database
    item = Item.query.get(item_id)
    if not item:
        return 'Item not found'
    else:
        return render_template('item_info.html', item=item)

@app.route('/account')
def account_page():
    #Get user info from database
    user = User.query.filter_by(id=session['user_id']).first()
    session['user_id'] = user.id
    session['username'] = user.username
    session['email_address'] = user.email_address

    #Return Account Page with current user info
    return render_template('account.html', user=user, username=session['username'], email_address=session['email_address'])


@app.route('/poorfromyou')
def funny_page():
    return render_template('funny.html')

@app.route('/register', methods=['POST', 'GET'])
def signup_page():
    #Retrieves user info from form
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

@app.route('/add_to_cart/<int:item_id>', methods=['POST', 'GET'])
def add_to_cart(item_id):
    item = Item.query.get(item_id)

    #Creates new empty cart if one does not exist
    cart = session.get('cart', [])

    #Get all the item ids from cart
    for cart_item in cart:
        if cart_item['id'] == item.id:
            cart_item['quantity'] += 1
            session['cart'] = cart
            flash(f'Added {item.name} to cart')
            return redirect(url_for('view_cart'))
        
    #Add item to cart
    cart.append(dict(id=item.id, name=item.name, price=item.price, quantity=1))
    session['cart'] = cart

    flash(f'Added {item.name} to cart')
    return redirect(url_for('view_cart'))


@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    #Gets the current cart using sessions
    cart = session.get('cart', [])
    item_ids = [item['id'] for item in cart]
    items = Item.query.filter(Item.id.in_(item_ids)).all()
    #Calculates total price 
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    #Gets quantity of each item in cart
    for item in items:
        for cart_item in cart:
            if cart_item['id'] == item.id:
                item.quantity = cart_item['quantity']
                break
    
    return render_template('cart.html', items=items, cart=cart, total_price=total_price)


@app.route('/clear_cart')
def clear_cart():
    #Clears the current cart
    session.pop('cart', None)
    return redirect(url_for('home_page'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST', 'GET'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    #Removes item from cart 
    for item in cart:
        if item['id'] == item_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
                session['cart'] = cart
                flash(f'Removed one item from cart')
            else:
                #Removes whole item if quantity is 1
                cart.remove(item)
                session['cart'] = cart
                flash(f'Removed item from cart')
            break

    return redirect(url_for('view_cart'))
    

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    #Gets the current cart using sessions
    cart = session.get('cart', [])
    items_ids = [item['id'] for item in cart]
    items = Item.query.filter(Item.id.in_(items_ids)).all()
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    return render_template('checkout.html', items=items, cart=cart, total_price=total_price)
    

@app.route('/search', methods=['GET'])
def search():
    #Uses form to compare to items in database
    search_query = request.args.get('search')
    items = Item.query.filter(Item.name.ilike(f'%{search_query}%')).all()
    return render_template('shop.html', items=items)


