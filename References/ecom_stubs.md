# Sample e-commerce platform backend

## User Registration & Authentication

```
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password_hash=hashed_password,
                    email=data['email'], role="shopper")
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = create_auth_token()
    return jsonify({'token': token})
```

#### We will require three decorators for authentication and authorization - `@token_required`, `@role_required`, & `@ownership_required`.

`@token_required`: authenticate users

`@role_required`: authenticate sellers

`@ownership_required`: authenticate ownership of product

#### They are not implemented, but will be used in the following routes.

## Shopping Cart Management (Add/Remove, View)

```
@app.route('/cart', methods=['POST'])
@token_required
def add_to_cart():
    data = request.get_json()
    cart = ShoppingCart.query.filter_by(user_id=g.user.id).first()
    if not cart:
        cart = ShoppingCart(user_id=g.user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, product_id=data['product_id']).first()
    if cart_item:
        cart_item.quantity += data['quantity']
    else:
        cart_item = CartItem(
            cart_id=cart.id, product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart'})


@app.route('/cart/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_cart(product_id):
    cart = ShoppingCart.query.filter_by(user_id=g.user.id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'})


@app.route('/cart', methods=['GET'])
@token_required
def view_cart():
    cart = ShoppingCart.query.filter_by(user_id=g.user.id).first()
    if not cart:
        return jsonify({'message': 'Cart is empty'}), 404
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    return jsonify([{'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items])
```

## Product Management (CRUD)

We utilise `@role_required` for these routes. Sellers are allowed to CRUD products that belong to them, while shoppers can only R.

```
@app.route('/products', methods=['POST'])
@token_required
@role_required('seller')
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created'}), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
@token_required
@role_required('seller')
@ownership_required
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated'})


@app.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
@ownership_required
@role_required('seller')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})


@app.route('/products', methods=['GET'])
@token_required
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price} for product in products])
```

# Order placement and tracking

```
@app.route('/orders', methods=['POST'])
@token_required
def place_order():
    data = request.get_json()
    cart = ShoppingCart.query.filter_by(user_id=g.user.id).first()
    if not cart:
        return jsonify({'message': 'Cart is empty'}), 400

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    total_amount = sum(
        item.quantity * Product.query.get(item.product_id).price for item in cart_items)
    new_order = Order(
        user_id=g.user.id, payment_id=data['payment_id'], total_amount=total_amount, status='Pending')
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=new_order.id, product_id=item.product_id,
                               quantity=item.quantity, price=Product.query.get(item.product_id).price)
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'Order placed', 'order_id': new_order.id})


@app.route('/orders/<int:order_id>', methods=['GET'])
@token_required
def track_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=g.user.id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    return jsonify({
        'order_id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'items': [{'product_id': item.product_id, 'quantity': item.quantity, 'price': item.price} for item in order_items]
    })
```
