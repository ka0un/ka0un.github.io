// Image Carousel
document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.querySelector('.carousel-container');
  const slides = document.querySelectorAll('.carousel-slide');
  let currentSlide = 0;
  let isAnimating = false;

  function showSlide(index) {
    if (isAnimating) return;
    isAnimating = true;

    // Remove all classes
    slides.forEach(slide => {
      slide.classList.remove('active', 'prev');
    });

    // Add classes for animation
    slides[currentSlide].classList.add('prev');
    slides[index].classList.add('active');

    // Update current slide
    currentSlide = index;

    // Reset animation flag after transition
    setTimeout(() => {
      isAnimating = false;
    }, 800);
  }

  function nextSlide() {
    const nextIndex = (currentSlide + 1) % slides.length;
    showSlide(nextIndex);
  }

  // Start automatic slideshow
  setInterval(nextSlide, 5000);
}); 