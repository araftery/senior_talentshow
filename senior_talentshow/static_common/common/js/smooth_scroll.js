(function($){
  $(document).ready(function(){
    var hash = window.location.hash;
    if (hash)
    {
      $.scrollTo($(hash), 600, {
        offset: -75, // height of navbar
      });
    }
  });
})(jQuery);