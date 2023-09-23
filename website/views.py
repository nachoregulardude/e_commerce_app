from datetime import datetime
import json

from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Cart, Note, db, Productdetails as ProductDetails

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home')
@login_required
def home():
    if request.method == 'POST':
        if len(request.form['note']) < 2:
            flash('Note is too short!', category='error')
        else:
            note_data = {
                'data': request.form['note'],
                'user_id': current_user.id,
            }
            new_note = Note(**note_data)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html",
                           user=current_user,
                           products=ProductDetails.query.limit(25))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    print(note)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})


@views.route('/add-to-cart/<int:product_id>')
@login_required
def add_product_to_cart(product_id: int):
    current_user._add_to_cart(product_id)
    flash('Item added')
    return jsonify({})


@views.route('/delete-from-cart/<int:product_id>')
@login_required
def remove_from_cart(product_id: int):
    current_user._delete_from_cart(product_id)
    flash('Item removed')
    return jsonify({})


@views.route("/view-cart", methods=["GET", "POST"])
@login_required
def cart():
    cart = ProductDetails.query.join(Cart).add_columns(
        Cart.quantity, ProductDetails.price, ProductDetails.name,
        ProductDetails.id).filter_by(item_buyer=current_user).all()
    subtotal = 0
    for item in cart:
        subtotal += int(item.price) * int(item.quantity)

    if request.method == "POST":
        qty = request.form.get("qty")
        idpd = request.form.get("idpd")
        cartitem = Cart.query.filter_by(product_id=idpd).first()
        cartitem.quantity = qty
        db.session.commit()
        cart = ProductDetails.query.join(Cart).add_columns(
            Cart.quantity, ProductDetails.price, ProductDetails.name,
            ProductDetails.id).filter_by(item_buyer=current_user).all()
        subtotal = 0
        for item in cart:
            subtotal += int(item.price) * int(item.quantity)
    return render_template(
        'view_cart.html',
        cart=cart,
        # noOfItems=noOfItems,
        subtotal=subtotal,
        user=current_user)
