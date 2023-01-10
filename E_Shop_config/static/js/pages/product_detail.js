var form = document.getElementById('payment-form');
form.addEventListener('submit', function (event) {
    var productId = "{{ product.id }}";
    var quantity = "{{ product.count }}";

    if (quantity < 1) {
        alert('This product is out of stock!');
        event.preventDefault();
    } else {
        return true;
    }
});