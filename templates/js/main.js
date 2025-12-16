// Smooth scroll animation with custom easing
document.querySelector('.scroll-button').addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector('#projects');
    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const duration = 1200;
    let start = null;

    function easeInOutCubic(t) {
        return t < 0.5
            ? 4 * t * t * t
            : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function animation(currentTime) {
        if (start === null) start = currentTime;
        const timeElapsed = currentTime - start;
        const progress = Math.min(timeElapsed / duration, 1);
        const ease = easeInOutCubic(progress);

        window.scrollTo(0, startPosition + distance * ease);

        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }

    requestAnimationFrame(animation);
});

// Modal functionality
const projectCards = document.querySelectorAll('.project-card');
const modals = document.querySelectorAll('.modal');
const closeButtons = document.querySelectorAll('.close-modal');
let lastFocusedElement = null;

function trapFocus(modal) {
  const focusableElements = getFocusableElements(modal);
  const first = focusableElements[0];
  const last = focusableElements[focusableElements.length - 1];

  // Wait for the end of animation to set focus on close button
  setTimeout(() => {
    first.focus();
  }, 250);

  modal.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}

function getFocusableElements(container) {
  return container.querySelectorAll(
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
}

// Open modal when clicking on project card
projectCards.forEach(card => {
    const openModal = function (target) {
        const modalId = target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        lastFocusedElement = document.activeElement;

        if (!modal) return;

        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        trapFocus(modal);
    };

    card.addEventListener('click', (e) => openModal(card));
    card.addEventListener('keydown', (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault(); // Prevent space from scrolling the page
        openModal(card);
      }
    });
});

function closeModal(modal) {
  modal.classList.remove('active');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';

  if (lastFocusedElement) {
    lastFocusedElement.focus();
  }
}


// Close modal when clicking close button
closeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const modal = this.closest('.modal');
        closeModal(modal)
    });
});

// Close modal when clicking outside the modal content
modals.forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal(modal)
        }
    });
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        modals.forEach(modal => {
            closeModal(modal)
        });
    }
});
