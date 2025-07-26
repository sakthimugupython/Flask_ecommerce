// static/js/products.js
// Fetch products from API and render them on the products page
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/products')
        .then(res => res.json())
        .then(products => {
            const row = document.getElementById('products-row');
            if (!products.length) {
                row.innerHTML = '<div class="col-12 text-center">No products available.</div>';
                return;
            }
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'col-12 col-sm-6 col-md-4 col-lg-3';
                card.innerHTML = `
          <div class="card h-100 shadow-lg border-0 product-card" style="transition: transform 0.2s, box-shadow 0.2s;">
            <div class="position-relative">
              <img src="${product.image_url || 'https://via.placeholder.com/300x200?text=No+Image'}" class="card-img-top rounded-top product-img" alt="${product.name}" style="object-fit:cover;height:200px;width:100%;max-width:100%;">
              <span class="badge bg-primary position-absolute top-0 end-0 m-2 fs-6">Rs.${product.price.toFixed(2)}</span>
            </div>
            <div class="card-body d-flex flex-column" style="background: linear-gradient(135deg, #f8fafc 60%, #e0e7ff 100%);">
              <h5 class="card-title"><a href="/products/${product.id}" class="text-decoration-none text-dark product-link">${product.name}</a></h5>
              <p class="card-text text-truncate" title="${product.description}">${product.description}</p>
              <div class="mt-auto">
                <div class="mb-2"><strong>Price:</strong> Rs.${product.price.toFixed(2)}</div>
                <div class="mb-2"><strong>Stock:</strong> ${product.stock}</div>
                <button class="btn btn-gradient w-100 add-to-cart-btn mt-2" data-id="${product.id}" style="background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: #fff; border: none;">Add to Cart</button>
              </div>
            </div>
          </div>
        `;
                row.appendChild(card);
            });
            // Add event listeners for Add to Cart
            document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const productId = this.getAttribute('data-id');
                    // Add to Cart: call cart API
                    fetch('/api/cart/add', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ product_id: productId, quantity: 1 })
                    })
                    .then(res => res.json().then(data => ({status: res.status, body: data})))
                    .then(({status, body}) => {
                        if (status === 200) {
                            alert('Added to cart!');
                        } else if (body && body.error) {
                            alert('Error: ' + body.error);
                        } else {
                            alert('Error adding to cart.');
                        }
                    })
                    .catch(() => {
                        alert('Network error adding to cart.');
                    });
                });
            });
        })
        .catch(err => {
            document.getElementById('products-row').innerHTML = '<div class="col-12 text-danger">Error loading products.</div>';
        });
});