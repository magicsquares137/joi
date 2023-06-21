// Filter Category JS
$('.owl-carousel').owlCarousel({
    margin:15,
    loop:false,
    autoWidth:true,
    items:1,
    nav:true,
});

// Cards Slider JS
function isSmallScreen() {
  return window.innerWidth <= 1024;
}
function initOwlCarousel() {
  $('.cards-slider').owlCarousel({
    margin: 17,
    loop: false,
    autoWidth: true,
    responsiveClass: true,
    items: 4,
    nav: true,
  });
}

function handleResize() {
  if (!isSmallScreen()) {
    initOwlCarousel();
  } else {
    $('.cards-slider').trigger('destroy.owl.carousel'); // Destroy the carousel on small screens
  }
}

window.addEventListener('resize', handleResize);
handleResize();





// Form Password Eye
$(document).ready(function() {
    $('.eye').click(function() {
      $(this).toggleClass('fa-eye-slash');
      var passwordInput = $('.passwordShow');
      var type = passwordInput.attr('type') === 'password' ? 'text' : 'password';
      passwordInput.attr('type', type);
    });
  });
 


// Search Pop
  function openNav() {
    document.getElementById("mobile-search").style.height = "100%";
  }
  function closeNav() {
    document.getElementById("mobile-search").style.height = "0%";
  }