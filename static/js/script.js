// Basic form validation (optional)
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(event) {
        const email = document.querySelector('input[type="email"]').value;
        const password = document.querySelector('input[type="password"]').value;

        if (!email || !password) {
            alert('All fields must be filled!');
            event.preventDefault();
        }
    });
});

