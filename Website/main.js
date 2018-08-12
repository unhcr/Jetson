$('#play').click(function () {
    $(this).toggleClass('active');
    $(this).find('h5').toggle();
    $('.alert').alert('close')
    $(this).find('span').toggleClass('ti-control-play').toggleClass('ti-control-pause');
   if ($("#video").get(0).paused) {
       $("#video").get(0).play();
   } else {
       $("#video").get(0).pause();
  }
});

$('#playO').click(function () {
    $(this).toggleClass('active');
    $(this).find('h5').toggle();
    $(this).find('span').toggleClass('ti-control-play').toggleClass('ti-control-pause');
   if ($("#videoO").get(0).paused) {
       $("#videoO").get(0).play();
   } else {
       $("#videoO").get(0).pause();
  }
});

iFrameResize({log:true}, '#engineIframe')