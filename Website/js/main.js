var scene = $(".scene")[0];
var parallax = new Parallax(scene, {
    scalarX: 4,
    scalarY: 4
});

$(function () {
  $('[data-toggle="popover"]').popover()
})
