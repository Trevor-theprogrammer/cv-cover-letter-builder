// Mobile Navigation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileNavToggle && mainNav) {
        mobileNavToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            const icon = mobileNavToggle.querySelector('i');
            if (mainNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close mobile nav when clicking on a link
        const navLinks = mainNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mainNav.classList.remove('active');
                const icon = mobileNavToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        });

        // Close mobile nav when clicking outside
        document.addEventListener('click', function(event) {
            if (!mainNav.contains(event.target) && !mobileNavToggle.contains(event.target)) {
                mainNav.classList.remove('active');
                const icon = mobileNavToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Touch-friendly enhancements
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.style.minHeight = '44px';
        button.style.minWidth = '44px';
    });

    // Prevent zoom on iOS when focusing inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            document.body.style.zoom = '1';
        });
    });
});
