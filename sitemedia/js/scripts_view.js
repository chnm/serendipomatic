var $container = $('#container')
// initialize Isotope
$container.isotope({
  // options...
  resizable: false, // disable normal resizing
  // set columnWidth to a percentage of container width
  masonry: { columnWidth: $container.width() / 5 }
});

// update columnWidth on window resize
$(window).smartresize(function(){
  $container.isotope({
    // update columnWidth to a percentage of container width
    masonry: { columnWidth: $container.width() / 5 }
  });
});