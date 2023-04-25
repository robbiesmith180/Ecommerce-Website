from shop import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False , unique=True)
    email_address = db.Column(db.String(length=60), nullable = False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable = False, unique = True)
    budget = db.Column(db.Integer(), nullable = False, default = 1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

class Item(db.Model): #Telling flask this class is a model
    id = db.Column(db.Integer(), primary_key = True) #Creating ID as primary keys
    name = db.Column(db.String(length=30), nullable = False, unique = True ) #Can only have max 30 characters, cannot be empty, must be a unique field name
    price = db.Column(db.Integer(), nullable = False)
    barcode = db.Column(db.String(length=12), nullable = False, unique = True)
    description = db.Column(db.String(length = 1024), nullable = False, unique = True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id') )

    def __repr__(self):
        return f'Item {self.name}'