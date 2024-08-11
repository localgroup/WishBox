document.addEventListener('DOMContentLoaded', function() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(productCard) {
      productCard.addEventListener('click', function() {
        const url = productCard.getAttribute('product-url');
        window.location.href = url;
      });
    });
  });