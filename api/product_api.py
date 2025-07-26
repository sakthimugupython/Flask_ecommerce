from flask import Blueprint, request, jsonify, session
from models import Product, CartItem
from extensions import db, csrf

product_api = Blueprint('product_api', __name__)

@csrf.exempt
@product_api.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if not session.get('user_id'):
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    cart_item = CartItem.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=session['user_id'], product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message': 'Added to cart'}), 200

@csrf.exempt
@product_api.route('/api/cart', methods=['GET'])
def get_cart():
    if not session.get('user_id'):
        return jsonify({'error': 'Not logged in'}), 401
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    result = []
    for item in cart_items:
        result.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price,
            'image_url': item.product.image_url
        })
    return jsonify(result)

@csrf.exempt
@product_api.route('/api/products', methods=['GET', 'POST'])
def api_products():
    if request.method == 'POST':
        data = request.get_json()
        required = ['name', 'description', 'price', 'stock']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        try:
            product = Product(
                name=data['name'],
                description=data['description'],
                price=float(data['price']),
                stock=int(data['stock']),
                image_url=data.get('image_url')
            )
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Product created', 'id': product.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        products = Product.query.all()
        return jsonify([
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': p.price,
                'stock': p.stock,
                'image_url': p.image_url,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in products
        ])

@csrf.exempt
@product_api.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'PATCH'])
def get_or_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'image_url': product.image_url,
            'created_at': product.created_at.isoformat() if product.created_at else None
        })
    else:
        data = request.get_json()
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        if 'image_url' in data:
            product.image_url = data['image_url']
        db.session.commit()
        return jsonify({'message': 'Product updated', 'id': product.id})
