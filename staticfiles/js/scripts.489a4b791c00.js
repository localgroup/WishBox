document.addEventListener('DOMContentLoaded', function() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(productCard) {
      productCard.addEventListener('click', function() {
        const url = productCard.getAttribute('product-url');
        window.location.href = url;
      });
    });
  });

document.addEventListener('DOMContentLoaded', function() {
  const categoryCards = document.querySelectorAll('.category-card');
  categoryCards.forEach(function(card) {
      card.addEventListener('click', function() {
          const url = card.dataset.categoryUrl; // can be used because the data attribute in the div starts with 'data-'
          window.location.href = url;
      });
  });
});