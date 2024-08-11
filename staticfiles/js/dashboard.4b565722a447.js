document.addEventListener('DOMContentLoaded', function() {
    const tableRows = document.querySelectorAll('table tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            const url = row.getAttribute('data-url');
            window.location.href = url;
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const adminCards = document.querySelectorAll('.card');
    adminCards.forEach(function(card) {
        card.addEventListener('click', function() {
            const url = card.querySelector('.card-body').getAttribute('board-url');
            window.location.href = url;
        });
    });
});