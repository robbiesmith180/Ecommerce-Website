from shop import db


class Item(db.Model): #Telling flask this class is a model
    id = db.Column(db.Integer(), primary_key = True) #Creating ID as primary keys
    name = db.Column(db.String(length=30), nullable = False, unique = True ) #Can only have max 30 characters, cannot be empty, must be a unique field name
    price = db.Column(db.Integer(), nullable = False)
    description = db.Column(db.String(length = 1024), nullable = False, unique = True)
    environmental_impact = db.Column(db.Integer(), nullable = False)

    #Returns string representation of the object
    def __repr__(self):
        return f'Item {self.name}'