from shop import db
from shop.models import Item, User, Cart, CartItem

def add_item_to_cart(item_id, user_id):
    item = Item.query.filter_by(id=item_id).first()
    user = User.query.filter_by(id=user_id).first()
    cart = Cart.query.filter_by(user_id=user_id).first()

    if cart is None:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
    
    cart_item = CartItem(item_id=item_id, cart_id=cart.id)
    db.session.add(cart_item)
    db.session.commit()