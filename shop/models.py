from flask import session
from shop import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True) #Creating ID as primary keys
    username = db.Column(db.String(length=40), nullable = False, unique = True ) #Can only have max 30 characters, cannot be empty, must be a unique field name
    email_address = db.Column(db.String(length=50), nullable = False, unique = True )
    password = db.Column(db.String(length=60), nullable = False)

    def  is_authenticated(self):
        return 'username' in session
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return not self.is_authenticated()
    
    def get_id(self):
        return str(self.id)


class Item(db.Model): #Telling flask this class is a model
    id = db.Column(db.Integer(), primary_key = True) #Creating ID as primary keys
    name = db.Column(db.String(length=30), nullable = False, unique = True ) #Can only have max 30 characters, cannot be empty, must be a unique field name
    price = db.Column(db.Integer(), nullable = False)
    description = db.Column(db.String(length = 1024), nullable = False, unique = True)
    environmental_impact = db.Column(db.Integer(), nullable = False)


    #Returns string representation of the object
    def __repr__(self):
        return f'Item {self.name}'

# class Cart(db.Model):
#     id = db.Column(db.Integer(), primary_key = True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)
#     items = db.relationship('Item', secondary='cart_item', backref='carts', lazy=True)

# cart_item = db.Table('cart_item',
#     db.Column('cart_id', db.Integer(), db.ForeignKey('cart.id'), primary_key=True),
#     db.Column('item_id', db.Integer(), db.ForeignKey('item.id'), primary_key=True)
#     )
