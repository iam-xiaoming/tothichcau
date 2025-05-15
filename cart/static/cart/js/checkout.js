document.addEventListener('DOMContentLoaded', function () {
    const checkoutBtn = document.getElementById('checkout-btn');

    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(event) {
            event.preventDefault();

            // Collect item IDs from cart
            const selectedItems = [];
            document.querySelectorAll('.cart-item').forEach(item => {
                const gamePk = item.getAttribute('data-game-pk');
                const orderId = item.getAttribute('data-order-id');
                const dataType = item.getAttribute('data-type')
                if (gamePk && orderId && dataType) {
                    selectedItems.push({ item_id: gamePk, orderId: orderId, dataType: dataType });
                }
            });

            // Step 1: Check stock availability
            fetch('/api/check-stock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ items: selectedItems })
            })
            .then(response => response.json())
            .then(data => {
                if (data.out_of_stock && data.out_of_stock.length > 0) {
                    // Show popup for out-of-stock items
                    const outOfStockNames = data.out_of_stock.map(item => item.name).join(', ');
                    const message = `The following items are out of stock and will be removed from your cart: ${outOfStockNames}`;
                    if (confirm(message)) {
                        // Remove out-of-stock items
                        Promise.all(data.out_of_stock.map(item => 
                            fetch(`/cart/delete/${item.orderId}/`, {
                                method: 'POST',
                                headers: {
                                    'X-CSRFToken': getCsrfToken()
                                }
                            })
                        )).then(() => {
                            // Check if all items are out of stock
                            if (data.out_of_stock.length === selectedItems.length) {
                                // Reload the page if all items are out of stock
                                window.location.reload();
                            } else {
                                // Proceed to checkout if some items remain
                                fetch("/create-checkout-session/", {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCsrfToken()
                                    }
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.error) {
                                        alert('Error: ' + data.error);
                                    } else {
                                        stripe.redirectToCheckout({ sessionId: data.id })
                                            .then(function(result) {
                                                if (result.error) {
                                                    alert('Error: ' + result.error.message);
                                                }
                                            });
                                    }
                                })
                                .catch(error => {
                                    console.error('Error creating checkout session:', error);
                                    alert('There was an error creating the checkout session.');
                                });
                            }
                        }).catch(error => {
                            console.error('Error removing out-of-stock items:', error);
                            alert('There was an error removing out-of-stock items.');
                        });
                    }
                } else {
                    // Proceed to checkout if all items are in stock
                    fetch("/create-checkout-session/", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken()
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert('Error: ' + data.error);
                        } else {
                            stripe.redirectToCheckout({ sessionId: data.id })
                                .then(function(result) {
                                    if (result.error) {
                                        alert('Error: ' + result.error.message);
                                    }
                                });
                        }
                    })
                    .catch(error => {
                        console.error('Error creating checkout session:', error);
                        alert('There was an error creating the checkout session.');
                    });
                }
            })
            .catch(error => {
                console.error('Error checking stock:', error);
                alert('There was an error checking item availability.');
            });
        });
    } else {
        console.log('Checkout button not found');
    }
});

// Helper function to get CSRF token from cookie
function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return '';
}