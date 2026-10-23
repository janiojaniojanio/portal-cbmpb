/**
 * Portal Institucional CBMPB - Scripts de Interatividade e Acessibilidade Mobile-First
 * Inspirado nos componentes dinâmicos do template "Current"
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. HEADER SCROLL & BACK TO TOP BUTTON
  const header = document.querySelector('.main-header');
  const backToTopBtn = document.getElementById('backToTopBtn');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    if (scrollY > 30) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }

    if (scrollY > 350) {
      if (backToTopBtn) backToTopBtn.style.display = 'flex';
    } else {
      if (backToTopBtn) backToTopBtn.style.display = 'none';
    }
  });

  backToTopBtn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 2. HERO SLIDER COM SUPORTE A SWIPE TOUCH & DOTS NO MOBILE
  const sliderWrap = document.getElementById('heroSlider');
  const slides = document.querySelectorAll('.hero-slide');
  const prevBtn = document.getElementById('slider-prev');
  const nextBtn = document.getElementById('slider-next');
  const dotsContainer = document.getElementById('sliderDots');

  let currentSlide = 0;
  let sliderInterval = null;

  // Gerar dots dinamicamente
  if (dotsContainer && slides.length > 1) {
    slides.forEach((_, idx) => {
      const dot = document.createElement('button');
      dot.className = `slider-dot ${idx === 0 ? 'active' : ''}`;
      dot.setAttribute('aria-label', `Ir para slide ${idx + 1}`);
      dot.addEventListener('click', () => {
        showSlide(idx);
        resetSliderTimer();
      });
      dotsContainer.appendChild(dot);
    });
  }

  function updateDots(index) {
    const dots = document.querySelectorAll('.slider-dot');
    dots.forEach((dot, idx) => {
      if (idx === index) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }

  function showSlide(index) {
    if (!slides.length) return;
    slides.forEach((slide) => slide.classList.remove('active'));
    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
    updateDots(currentSlide);
  }

  function nextSlide() {
    showSlide(currentSlide + 1);
  }

  function prevSlide() {
    showSlide(currentSlide - 1);
  }

  if (slides.length > 1) {
    nextBtn?.addEventListener('click', () => {
      nextSlide();
      resetSliderTimer();
    });

    prevBtn?.addEventListener('click', () => {
      prevSlide();
      resetSliderTimer();
    });

    function startSliderTimer() {
      sliderInterval = setInterval(nextSlide, 7000);
    }

    function resetSliderTimer() {
      clearInterval(sliderInterval);
      startSliderTimer();
    }

    startSliderTimer();

    // Suporte a Touch Gestures / Swipe no Mobile
    let touchStartX = 0;
    let touchEndX = 0;

    sliderWrap?.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    sliderWrap?.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const swipeDistance = touchEndX - touchStartX;
      if (Math.abs(swipeDistance) > 45) {
        if (swipeDistance < 0) {
          nextSlide(); // Deslizar para a esquerda -> próximo slide
        } else {
          prevSlide(); // Deslizar para a direita -> slide anterior
        }
        resetSliderTimer();
      }
    }
  }

  // 3. ACESSIBILIDADE - ALTO CONTRASTE (DESKTOP E MOBILE)
  const contrastBtn = document.getElementById('toggle-contrast');
  const mobileContrastBtn = document.getElementById('mobile-toggle-contrast');
  const savedContrast = localStorage.getItem('cbmpb-contrast');

  if (savedContrast === 'true') {
    document.body.classList.add('high-contrast');
  }

  function toggleContrast() {
    document.body.classList.toggle('high-contrast');
    const isContrast = document.body.classList.contains('high-contrast');
    localStorage.setItem('cbmpb-contrast', isContrast);
  }

  contrastBtn?.addEventListener('click', toggleContrast);
  mobileContrastBtn?.addEventListener('click', toggleContrast);

  // 4. ACESSIBILIDADE - TAMANHO DA FONTE
  const btnFontIncrease = document.getElementById('font-increase');
  const btnFontDecrease = document.getElementById('font-decrease');
  const btnFontReset = document.getElementById('font-reset');

  btnFontIncrease?.addEventListener('click', () => {
    if (document.body.classList.contains('font-lg')) {
      document.body.classList.remove('font-lg');
      document.body.classList.add('font-xl');
    } else {
      document.body.classList.add('font-lg');
    }
  });

  btnFontDecrease?.addEventListener('click', () => {
    if (document.body.classList.contains('font-xl')) {
      document.body.classList.remove('font-xl');
      document.body.classList.add('font-lg');
    } else {
      document.body.classList.remove('font-lg');
    }
  });

  btnFontReset?.addEventListener('click', () => {
    document.body.classList.remove('font-lg', 'font-xl');
  });

  // 5. ANIMAÇÃO DE CONTADORES ESTATÍSTICOS
  const counters = document.querySelectorAll('.stat-number');
  let animated = false;

  function runCounters() {
    counters.forEach(counter => {
      const targetText = counter.innerText.trim();
      const hasPlus = targetText.includes('+');
      const hasPercent = targetText.includes('%');
      const numericVal = parseInt(targetText.replace(/\D/g, ''), 10);

      if (isNaN(numericVal)) return;

      let count = 0;
      const speed = Math.ceil(numericVal / 35);
      const timer = setInterval(() => {
        count += speed;
        if (count >= numericVal) {
          count = numericVal;
          clearInterval(timer);
          counter.innerText = count.toLocaleString('pt-BR') + (hasPlus ? '+' : '') + (hasPercent ? '%' : '');
        } else {
          counter.innerText = count.toLocaleString('pt-BR') + (hasPlus ? '+' : '') + (hasPercent ? '%' : '');
        }
      }, 30);
    });
  }

  const observerOptions = {
    threshold: 0.2
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        animated = true;
        runCounters();
        obs.disconnect();
      }
    });
  }, observerOptions);

  const statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    observer.observe(statsSection);
  }
});
