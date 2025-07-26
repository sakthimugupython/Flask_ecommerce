// static/js/cart.js
// Fetch and render cart items for the logged-in user

document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-items-container');
    const cartTotal = document.getElementById('cart-total');
    fetch('/api/cart')
        .then(res => res.json())
        .then(items => {
            console.log('Cart API response:', items);
            if (Array.isArray(items) && items.length > 0) {
                let total = 0;
                cartContainer.innerHTML = '';
                items.forEach(item => {
                    const subtotal = item.price * item.quantity;
                    total += subtotal;
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><img src="${item.image_url || 'https://via.placeholder.com/60x60?text=No+Image'}" alt="${item.product_name}" style="width:60px;height:60px;object-fit:cover;border-radius:8px;"></td>
                        <td>${item.product_name}</td>
                        <td>Rs.${item.price.toFixed(2)}</td>
                        <td>${item.quantity}</td>
                        <td>Rs.${subtotal.toFixed(2)}</td>
                    `;
                    cartContainer.appendChild(row);
                });
                cartTotal.textContent = 'Rs.' + total.toFixed(2);
            } else if (items.error) {
                cartContainer.innerHTML = `<tr><td colspan="5" class="text-danger">${items.error}</td></tr>`;
                cartTotal.textContent = 'Rs.0.00';
            } else {
                cartContainer.innerHTML = '<tr><td colspan="5" class="text-center">Your cart is empty.</td></tr>';
                cartTotal.textContent = 'Rs.0.00';
            }
        })
        .catch(() => {
            cartContainer.innerHTML = '<tr><td colspan="5" class="text-danger">Error loading cart.</td></tr>';
            cartTotal.textContent = 'Rs.0.00';
        });
});