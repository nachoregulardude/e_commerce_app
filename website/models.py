from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(4))
    first_name = db.Column(db.String(150))
    number_of_transactions = db.Column(db.Integer)
    cart = db.relationship('Cart', backref='item_buyer')

    def _add_to_cart(self, product_id: int) -> None:
        existing_product_in_cart = Cart.query.filter(
            product_id=product_id, item_buyer=self.id).fist()
        if existing_product_in_cart:
            existing_product_in_cart.quantity += 1
        else:
            selected_item = Cart(product_id=product_id, user_id=self.id)
            db.session.add(selected_item)
        db.session.commit()

    def _remove_from_cart(self, product_id: int) -> None:
        existing_product_in_cart = Cart.query.filter(
            product_id=product_id, item_buyer=self.id).fist()
        if existing_product_in_cart:
            existing_product_in_cart.quantity -= 1
        else:
            selected_item = Cart(product_id=product_id, user_id=self.id)
            db.session.delete(selected_item)
        db.session.commit()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Productdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    available_stock = db.Column(db.Integer)
    items_sold = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('productdetails.id'),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
