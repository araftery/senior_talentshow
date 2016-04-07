$(function(){
var countdownTimer =
  countdown(
    new Date(2014, 08, 25),
    function(ts) {
      $('.js-countdown').html(ts.toHTML("strong"));
    },
    countdown.MONTHS|countdown.DAYS|countdown.HOURS|countdown.MINUTES);
});