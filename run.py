from shop import app
from shop import db
from shop.models import Item, User


#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
        #Runs the app
        app.run(debug=True)