from flask import Blueprint, request, jsonify
from models import Product
from extensions import db

api = Blueprint('api', __name__)

@api.route('/api/products', methods=['GET', 'POST'])
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

@api.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'image_url': product.image_url,
        'created_at': product.created_at.isoformat() if product.created_at else None
    })
