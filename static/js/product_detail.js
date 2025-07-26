// static/js/product_detail.js
// Fetch product details and render on the detail page
document.addEventListener('DOMContentLoaded', function() {
  // Get product_id from template context (injected as a JS variable)
  let productId = null;
  // Try to get from a data attribute on the container
  const container = document.getElementById('product-detail');
  if (container && container.dataset.productId) {
    productId = container.dataset.productId;
  } else {
    // fallback: try to parse from URL
    const match = window.location.pathname.match(/\/products\/(\d+)/);
    if (match) productId = match[1];
  }
  if (!productId) {
    container.innerHTML = '<div class="col-12 text-danger">Invalid product ID.</div>';
    return;
  }
  fetch(`/api/products/${productId}`)
    .then(res => {
      if (!res.ok) throw new Error('Product not found');
      return res.json();
    })
    .then(product => {
      container.innerHTML = `
        <div class="col-12 col-md-10 col-lg-8">
          <div class="row align-items-start g-4">
            <div class="col-md-6 text-center">
              <img src="${product.image_url || 'https://via.placeholder.com/400x500?text=No+Image'}" class="img-fluid rounded" alt="${product.name}" style="max-height:420px;object-fit:cover;box-shadow:0 4px 24px rgba(60,60,100,0.08);">
            </div>
            <div class="col-md-6">
              <div class="ps-md-2">
                <h2 class="fw-bold mb-2">${product.name}</h2>
                <div class="mb-2">
                  <span class="fs-5 text-muted text-decoration-line-through me-2">Was Rs.${(product.price*1.2).toFixed(2)}</span>
                  <span class="fs-3 fw-bold text-primary">Rs.${product.price.toFixed(2)}</span>
                </div>
                <div class="mb-2">
                  <span class="badge bg-success me-2">In Stock</span>
                  <span class="text-danger fw-semibold">${product.stock <= 5 ? 'Only a few left' : ''}</span>
                </div>
                <div class="mb-3">
                  <strong>Description:</strong>
                  <div class="text-secondary">${product.description}</div>
                </div>
                <form class="mb-3">
                  <div class="mb-2">
                    <label for="quantity" class="form-label mb-0">Quantity:</label>
                    <input id="quantity" type="number" min="1" max="${product.stock}" value="1" class="form-control w-auto d-inline-block ms-2" style="width:90px;">
                  </div>
                </form>
                <div class="mb-2 small text-muted">Prices do not include taxes.</div>
              </div>
              <div class="mb-2"><strong>Stock:</strong> ${product.stock}</div>
              <button class="btn btn-primary w-100" id="add-to-cart-detail">Add to Cart</button>
            </div>
          </div>
        </div>
      `;
      // Add to Cart button event
      document.getElementById('add-to-cart-detail').onclick = function() {
        alert('Added product ' + product.id + ' to cart!');
      };
    })
    .catch(err => {
      container.innerHTML = `<div class='col-12 text-danger'>${err.message}</div>`;
    });
});
