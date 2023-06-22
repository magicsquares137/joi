// Cards Slider JS
$(document).ready(function () {
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
  
  
  // Filter Category JS
  $('.owl-carousel').owlCarousel({
  margin:15,
  loop:false,
  autoWidth:true,
  items:1,
  nav:true,
  });
  
  // Chat Textarea js
  $(document).ready(function () {
  $('textarea#id_message').attr('placeholder', 'Type a message').removeAttr('cols').removeAttr('rows').removeAttr('maxlength');
  });
  
  
  });
  
  // Form Password Eye
  // Pass Eye add html
  // Show and hide eye
  $(document).ready(function () {
  $('#id_password1').addClass('pass-field');
  $('#id_password').addClass('pass-field');
  $('.pass-field').after('<div class="password-eye"><i class="fa-solid fa-eye eye"></i></div>');
  $('.eye').click(function () {
  $(this).toggleClass('fa-eye-slash');
  var passwordInput = $('.pass-field');
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