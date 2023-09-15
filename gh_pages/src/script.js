const slides = document.querySelector('.slides');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');

let currentIndex = 0;

function showSlide(index) {
  slides.style.transform = `translateX(-${index * 100}%)`;
}

prevButton.addEventListener('click', () => {
  currentIndex = Math.max(currentIndex - 1, 0);
  showSlide(currentIndex);
});

nextButton.addEventListener('click', () => {
  currentIndex = Math.min(currentIndex + 1, 11);
  showSlide(currentIndex);
});


function autoSlide() {
  setInterval(() => {
    currentIndex = (currentIndex + 1) % 12;
    showSlide(currentIndex);
  }, 10000);
}

autoSlide();
