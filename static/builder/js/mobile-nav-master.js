// Mobile Navigation Master Script
// Handles responsive navigation for CV Cover Letter Builder

document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu toggle functionality
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  const navOverlay = document.querySelector('.nav-overlay');

  if (mobileMenuToggle && navMenu) {
    mobileMenuToggle.addEventListener('click', function (e) {
      e.preventDefault();
      toggleMobileMenu();
    });
  }

  // Close menu when clicking overlay
  if (navOverlay) {
    navOverlay.addEventListener('click', function () {
      closeMobileMenu();
    });
  }

  // Close menu when clicking nav links (for single page navigation)
  const navLinks = document.querySelectorAll('.nav-menu a');
  navLinks.forEach((link) => {
    link.addEventListener('click', function () {
      if (window.innerWidth <= 768) {
        closeMobileMenu();
      }
    });
  });

  // Handle window resize
  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
      closeMobileMenu();
    }
  });

  function toggleMobileMenu() {
    const isOpen = navMenu.classList.contains('active');

    if (isOpen) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }

  function openMobileMenu() {
    navMenu.classList.add('active');
    mobileMenuToggle.classList.add('active');
    document.body.classList.add('nav-open');

    if (navOverlay) {
      navOverlay.classList.add('active');
    }

    // Prevent body scroll when menu is open
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    navMenu.classList.remove('active');
    mobileMenuToggle.classList.remove('active');
    document.body.classList.remove('nav-open');

    if (navOverlay) {
      navOverlay.classList.remove('active');
    }

    // Restore body scroll
    document.body.style.overflow = '';
  }

  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((link) => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');

      if (href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();

        const offsetTop = target.offsetTop - 80; // Account for fixed header

        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth',
        });
      }
    });
  });

  // Add scroll effect to header
  const header = document.querySelector('header, .navbar');
  if (header) {
    let lastScrollTop = 0;

    window.addEventListener('scroll', function () {
      const scrollTop =
        window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > 100) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }

      // Hide/show header on scroll (optional)
      if (scrollTop > lastScrollTop && scrollTop > 200) {
        header.classList.add('header-hidden');
      } else {
        header.classList.remove('header-hidden');
      }

      lastScrollTop = scrollTop;
    });
  }

  // Form enhancements
  const forms = document.querySelectorAll('form');
  forms.forEach((form) => {
    // Add loading state to submit buttons
    form.addEventListener('submit', function () {
      const submitBtn = form.querySelector(
        'button[type="submit"], input[type="submit"]'
      );
      if (submitBtn) {
        submitBtn.disabled = true;
        const originalText = submitBtn.textContent || submitBtn.value;

        if (submitBtn.tagName === 'BUTTON') {
          submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
        } else {
          submitBtn.value = 'Processing...';
        }

        // Re-enable after 10 seconds as fallback
        setTimeout(() => {
          submitBtn.disabled = false;
          if (submitBtn.tagName === 'BUTTON') {
            submitBtn.textContent = originalText;
          } else {
            submitBtn.value = originalText;
          }
        }, 10000);
      }
    });
  });

  // File upload enhancements
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener('change', function () {
      const fileName = this.files[0]?.name;
      const label = this.nextElementSibling || this.previousElementSibling;

      if (fileName && label) {
        label.textContent = fileName;
        label.classList.add('file-selected');
      }
    });
  });

  // Tooltip functionality
  const tooltips = document.querySelectorAll('[data-tooltip]');
  tooltips.forEach((element) => {
    element.addEventListener('mouseenter', showTooltip);
    element.addEventListener('mouseleave', hideTooltip);
    element.addEventListener('focus', showTooltip);
    element.addEventListener('blur', hideTooltip);
  });

  function showTooltip(e) {
    const text = e.target.getAttribute('data-tooltip');
    if (!text) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    document.body.appendChild(tooltip);

    const rect = e.target.getBoundingClientRect();
    tooltip.style.left =
      rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

    setTimeout(() => tooltip.classList.add('show'), 10);
  }

  function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
      tooltip.remove();
    }
  }

  // Progress indicators for multi-step forms
  const progressSteps = document.querySelectorAll('.progress-step');
  if (progressSteps.length > 0) {
    updateProgressIndicator();
  }

  function updateProgressIndicator() {
    const currentStep = document.querySelector('.form-step.active');
    if (!currentStep) return;

    const stepIndex = Array.from(
      document.querySelectorAll('.form-step')
    ).indexOf(currentStep);

    progressSteps.forEach((step, index) => {
      if (index <= stepIndex) {
        step.classList.add('completed');
      } else {
        step.classList.remove('completed');
      }
    });
  }
});

// Utility functions
window.CVBuilder = {
  // Show notification
  showNotification: function (message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
      notification.remove();
    }, 5000);

    // Manual close
    notification
      .querySelector('.notification-close')
      .addEventListener('click', () => {
        notification.remove();
      });
  },

  // Confirm dialog
  confirm: function (message, callback) {
    if (confirm(message)) {
      callback();
    }
  },

  // Copy to clipboard
  copyToClipboard: function (text) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        this.showNotification('Copied to clipboard!', 'success');
      })
      .catch(() => {
        this.showNotification('Failed to copy to clipboard', 'error');
      });
  },
};
