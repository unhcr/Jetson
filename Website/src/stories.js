import $ from "jquery";
import Swiper from "swiper";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

var shapeanimations = [
  "fast-spin-right",
  "fast-spin-left",
  "spin-left",
  "spin-right",
];
$(".anim-shape").each(function () {
  var rand = ~~(Math.random() * shapeanimations.length);
  $(this).addClass(shapeanimations[rand]);
});

// Data

$.ajax({
  url: "https://www.unhcr.org/innovation/wp-json/wp/v2/pages/29887",
  //    url: "json/stories.json",
  type: "GET",
  success: (data) => {
    $(".place-cont").hide();
    // Title

    $(".storytitle").html(data.title.rendered);

    // Sections

    var sectionlist = data.acf.sections;
    var ids = 0;
    var articlesliders = 0;
    var logosliders = 0;

    sectionlist.forEach((i) => {
      ids = ids + 1;

      var section = document.createElement("section");
      $(section).attr("class", i.section_style);

      ////////// Text Section

      if (i.acf_fc_layout == "text_section") {
        $(section).html(
          '<div class="container"><h2>' + i.title + "</h2>" + i.text + "</div>"
        );
      }

      ////////// Code Section
      else if (i.acf_fc_layout == "code_section") {
        $(section).html(
          '<div class="container"><h2>' +
            i.title +
            "</h2>" +
            i.text +
            "" +
            i.code +
            "</div>"
        );
      }

      ////////// FAQ Section
      else if (i.acf_fc_layout == "faq_section") {
        $(section).html(
          '<div class="container"><h2>' + i.title + "</h2>" + i.text + "</div>"
        );

        var faqcontainer = document.createElement("div");
        $(faqcontainer).addClass("container");
        $(faqcontainer).append(
          '<div class="container"><h2>' + i.title + "</h2>" + i.text + "</div>"
        );

        var faqrow = document.createElement("div");
        $(faqrow).addClass("row");

        // FAQS
        var faqlist = i.faqs;
        var fids = 0;

        faqlist.forEach((i) => {
          fids = fids + 1;
          $(faqrow).append(
            '<div class="col-sm-4"><h4 data-toggle="modal" data-target="#q' +
              fids +
              '"><span class="num"><span class="ti-comment-alt"></span></span> <strong>' +
              i.faq_title +
              "</strong></h4></div>"
          );

          $("body").append(
            '<div class="modal fade" id="q' +
              fids +
              '" tabindex="-1" role="dialog" aria-labelledby="q' +
              fids +
              '"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">' +
              i.faq_title +
              '</h4></div><div class="modal-body">' +
              i.faq_content +
              "</div></div></div></div>"
          );
        });

        $(faqcontainer).append(faqrow);
      }

      ///////////// Article Slider
      else if (i.acf_fc_layout == "article_slider") {
        articlesliders = articlesliders + 1;

        // Check if only article slider
        if (articlesliders == 1) {
          // Check if contains text
          if (i.text > -1) {
            $(section).html(
              '<div class="container"><h2>' +
                i.title +
                "</h2>" +
                i.text +
                "</div>"
            );

            // Create slider
            var articleslider = document.createElement("div");
            $(articleslider)
              .attr("class", "swiper-container article-slider")
              .attr("id", "article-slider-1");

            var articlesliderwrapper = document.createElement("div");
            $(articlesliderwrapper).attr("class", "swiper-wrapper");
            $(articlesliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var articleslides = i.article_slider;
            articleslides.forEach((x) => {
              $(articlesliderwrapper).append(
                '<div class="swiper-slide single-article-thumb"><a href="' +
                  x.article_link +
                  '" target="_blank"><div class="thumb-cover"><h3>' +
                  x.article_title +
                  "</h3><span>View paper</span></div></a>"
              );
            });

            // Add wrapper to slider

            $(articleslider).append(articlesliderwrapper);

            // Add controls

            var nextarrow1 = document.createElement("div");
            $(nextarrow1)
              .attr("class", "swiper-button-next")
              .attr("id", "next1");
            var prevarrow1 = document.createElement("div");
            $(prevarrow1)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev1");

            $(articleslider).append(nextarrow1);
            $(articleslider).append(prevarrow1);

            // Add slider to Section

            $(section).append(articleslider);
          } else if (i.text < 1) {
            $(section).html(
              '<div class="container"><h2>' + i.title + "</h2></div>"
            );

            // Create slider
            var articleslider = document.createElement("div");
            $(articleslider)
              .attr("class", "swiper-container article-slider")
              .attr("id", "article-slider-1");

            var articlesliderwrapper = document.createElement("div");
            $(articlesliderwrapper).attr("class", "swiper-wrapper");
            $(articlesliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var articleslides = i.article_slider;

            articleslides.forEach((x) => {
              $(articlesliderwrapper).append(
                '<div class="swiper-slide single-article-thumb"><a href="' +
                  x.article_link +
                  '" target="_blank"><div class="thumb-cover"><h3>' +
                  x.article_title +
                  "</h3><span>View paper</span></div></a>"
              );
            });

            // Add wrapper to slider

            $(articleslider).append(articlesliderwrapper);

            // Add controls

            var nextarrow1 = document.createElement("div");
            $(nextarrow1).attr("class", "swiper-button-next").attr("id", next1);
            var prevarrow1 = document.createElement("div");
            $(prevarrow1).attr("class", "swiper-button-prev").attr("id", prev1);

            $(articleslider).append(nextarrow1);
            $(articleslider).append(prevarrow1);

            // Add slider to Section

            $(section).append(articleslider);
          }
        } else if (articlesliders > 1) {
          // Check if contains text
          if (i.text > -1) {
            $(section).html(
              '<div class="container"><h2>' +
                i.title +
                "</h2>" +
                i.text +
                "</div>"
            );

            // Create slider
            var articleslider = document.createElement("div");
            $(articleslider)
              .attr("class", "swiper-container article-slider")
              .attr("id", "article-slider-2");

            var articlesliderwrapper = document.createElement("div");
            $(articlesliderwrapper).attr("class", "swiper-wrapper");
            $(articlesliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var articleslides = i.article_slider;
            articleslides.forEach((x) => {
              $(articlesliderwrapper).append(
                '<div class="swiper-slide single-article-thumb"><a href="' +
                  x.article_link +
                  '" target="_blank"><div class="thumb-cover"><h3>' +
                  x.article_title +
                  "</h3><span>View paper</span></div></a>"
              );
            });

            // Add wrapper to slider

            $(articleslider).append(articlesliderwrapper);

            // Add controls

            var nextarrow2 = document.createElement("div");
            $(nextarrow1)
              .attr("class", "swiper-button-next")
              .attr("id", "next2");
            var prevarrow2 = document.createElement("div");
            $(prevarrow1)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev2");

            $(articleslider).append(nextarrow2);
            $(articleslider).append(prevarrow2);

            // Add slider to Section

            $(section).append(articleslider);
          } else if (i.text < 1) {
            $(section).html(
              '<div class="container"><h2>' + i.title + "</h2></div>"
            );

            // Create slider
            var articleslider = document.createElement("div");
            $(articleslider)
              .attr("class", "swiper-container article-slider")
              .attr("id", "article-slider-2");

            var articlesliderwrapper = document.createElement("div");
            $(articlesliderwrapper).attr("class", "swiper-wrapper");
            $(articlesliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var articleslides = i.article_slider;

            articleslides.forEach((x) => {
              $(articlesliderwrapper).append(
                '<div class="swiper-slide single-article-thumb"><a href="' +
                  x.article_link +
                  '" target="_blank"><div class="thumb-cover"><h3>' +
                  x.article_title +
                  "</h3><span>View paper</span></div></a>"
              );
            });

            // Add wrapper to slider

            $(articleslider).append(articlesliderwrapper);

            // Add controls

            var nextarrow1 = document.createElement("div");
            $(nextarrow1).attr("class", "swiper-button-next").attr("id", next1);
            var prevarrow1 = document.createElement("div");
            $(prevarrow1).attr("class", "swiper-button-prev").attr("id", prev1);

            $(articleslider).append(nextarrow1);
            $(articleslider).append(prevarrow1);

            // Add slider to Section

            $(section).append(articleslider);
          }
        }
      }

      ////////// Logo Slider
      else if (i.acf_fc_layout == "logo_slider") {
        logosliders = logosliders + 1;

        // Check if only logo slider
        if (logosliders == 1) {
          // Check if contains text
          if (i.text > -1) {
            $(section).html(
              '<div class="container"><h2>' +
                i.title +
                "</h2>" +
                i.text +
                "</div>"
            );

            // Create slider
            var logoslider = document.createElement("div");
            $(logoslider)
              .attr("class", "swiper-container logo-slider")
              .attr("id", "logo-slider-1");

            var logosliderwrapper = document.createElement("div");
            $(logosliderwrapper).attr("class", "swiper-wrapper");
            $(logosliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var logoslides = i.logo_slider;
            logoslides.forEach((x) => {
              $(logosliderwrapper).append(
                '<div class="swiper-slide"><img src="' +
                  x.logo +
                  '" /><a href="' +
                  x.logo_link +
                  '" target="_blank"><span>Visit Website</a>'
              );
            });

            // Add wrapper to slider

            $(logoslider).append(logosliderwrapper);

            // Add controls

            var nextarrow3 = document.createElement("div");
            $(nextarrow3)
              .attr("class", "swiper-button-next")
              .attr("id", "next3");
            var prevarrow3 = document.createElement("div");
            $(prevarrow3)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev3");

            $(logoslider).append(nextarrow3);
            $(logoslider).append(prevarrow3);

            // Add slider to Section

            $(section).append(logoslider);
          } else if (i.text < 1) {
            $(section).html(
              '<div class="container"><h2>' + i.title + "</h2></div>"
            );

            // Create slider
            var logoslider = document.createElement("div");
            $(logoslider)
              .attr("class", "swiper-container logo-slider")
              .attr("id", "logo-slider-1");

            var logosliderwrapper = document.createElement("div");
            $(logosliderwrapper).attr("class", "swiper-wrapper");
            $(logosliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var logoslides = i.logo_slider;
            logoslides.forEach((x) => {
              $(logosliderwrapper).append(
                '<div class="swiper-slide"><img src="' +
                  x.logo +
                  '" /><a href="' +
                  x.logo_link +
                  '" target="_blank"><span>Visit Website</a>'
              );
            });

            // Add wrapper to slider

            $(logoslider).append(logosliderwrapper);

            // Add controls

            var nextarrow3 = document.createElement("div");
            $(nextarrow3)
              .attr("class", "swiper-button-next")
              .attr("id", "next3");
            var prevarrow3 = document.createElement("div");
            $(prevarrow3)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev3");

            $(logoslider).append(nextarrow3);
            $(logoslider).append(prevarrow3);

            // Add slider to Section

            $(section).append(logoslider);
          }
        } else if (logosliders > 1) {
          // Check if contains text
          if (i.text > -1) {
            $(section).html(
              '<div class="container"><h2>' +
                i.title +
                "</h2>" +
                i.text +
                "</div>"
            );

            // Create slider
            var logoslider = document.createElement("div");
            $(logoslider)
              .attr("class", "swiper-container logo-slider")
              .attr("id", "logo-slider-2");

            var logosliderwrapper = document.createElement("div");
            $(logosliderwrapper).attr("class", "swiper-wrapper");
            $(logosliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var logoslides = i.logo_slider;
            logoslides.forEach((x) => {
              $(logosliderwrapper).append(
                '<div class="swiper-slide"><img src="' +
                  x.logo +
                  '" /><a href="' +
                  x.logo_link +
                  '" target="_blank"><span>Visit Website</a>'
              );
            });

            // Add wrapper to slider

            $(logoslider).append(logosliderwrapper);

            // Add controls

            var nextarrow4 = document.createElement("div");
            $(nextarrow4)
              .attr("class", "swiper-button-next")
              .attr("id", "next4");
            var prevarrow4 = document.createElement("div");
            $(prevarrow4)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev4");

            $(logoslider).append(nextarrow4);
            $(logoslider).append(prevarrow4);

            // Add slider to Section

            $(section).append(logoslider);
          } else if (i.text < 1) {
            $(section).html(
              '<div class="container"><h2>' + i.title + "</h2></div>"
            );

            // Create slider
            var logoslider = document.createElement("div");
            $(logoslider)
              .attr("class", "swiper-container logo-slider")
              .attr("id", "logo-slider-2");

            var logosliderwrapper = document.createElement("div");
            $(logosliderwrapper).attr("class", "swiper-wrapper");
            $(logosliderwrapper).css({
              marginBottom: -50,
              padding: "10px 0 80px",
            });

            // Add to slider
            var logoslides = i.logo_slider;
            logoslides.forEach((x) => {
              $(logosliderwrapper).append(
                '<div class="swiper-slide"><img src="' +
                  x.logo +
                  '" /><a href="' +
                  x.logo_link +
                  '" target="_blank"><span>Visit Website</a>'
              );
            });

            // Add wrapper to slider

            $(logoslider).append(logosliderwrapper);

            // Add controls

            var nextarrow4 = document.createElement("div");
            $(nextarrow4)
              .attr("class", "swiper-button-next")
              .attr("id", "next4");
            var prevarrow4 = document.createElement("div");
            $(prevarrow4)
              .attr("class", "swiper-button-prev")
              .attr("id", "prev4");

            $(logoslider).append(nextarrow4);
            $(logoslider).append(prevarrow4);

            // Add slider to Section

            $(section).append(logoslider);
          }
        }
      }

      $(".mainstory").append(section);
    });

    // Disclaimer
    $("#disclaimer .content").html(data.acf.disclaimer);
  },
}).done(function () {
  $(() => {
    $('[data-toggle="tooltip"]').tooltip();
  });

  // Slider

  var episwiper = new Swiper("#epilogue", {
    slidesPerView: 1,
    direction: "vertical",
    parallax: true,
    speed: 1000,
    mousewheel: true,
    // init: false,
  });

  $("#epibutton").click(function () {
    episwiper.slideNext();
  });

  // 1st Article slider
  var articleswiper = new Swiper("#article-slider-1", {
    slidesPerView: "auto",
    spaceBetween: 30,
    centerInsufficientSlides: true,
    slidesOffsetBefore: 40,
    slidesOffsetAfter: 10,
    navigation: {
      nextEl: "#next1",
      prevEl: "#prev1",
    },
  });

  // 2nd Article slider
  var articleswiper2 = new Swiper("#article-slider-2", {
    slidesPerView: "auto",
    spaceBetween: 30,
    centerInsufficientSlides: true,
    slidesOffsetBefore: 40,
    slidesOffsetAfter: 10,
    navigation: {
      nextEl: "#next2",
      prevEl: "#prev2",
    },
  });

  var logoswiper = new Swiper("#logo-slider-1", {
    slidesPerView: "auto",
    spaceBetween: 20,
    centerInsufficientSlides: true,
    slidesOffsetBefore: 10,
    slidesOffsetAfter: 10,
    // init: false,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: "#next3",
      prevEl: "#prev3",
    },
  });

  var logoswiper2 = new Swiper("#logo-slider-2", {
    slidesPerView: "auto",
    spaceBetween: 20,
    centerInsufficientSlides: true,
    slidesOffsetBefore: 10,
    slidesOffsetAfter: 10,
    // init: false,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: "#next4",
      prevEl: "#prev4",
    },
  });

  $('a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click((event) => {
      // On-page links
      if (
        location.pathname.replace(/^\//, "") ==
          this.pathname.replace(/^\//, "") &&
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length
          ? target
          : $("[name=" + this.hash.slice(1) + "]");
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $("html, body").animate(
            {
              scrollTop: target.offset().top,
            },
            1000,
            () => {
              // Callback after animation
              // Must change focus!
              var $target = $(target);
              $target.focus();
              if ($target.is(":focus")) {
                // Checking if the target was focused
                return false;
              } else {
                $target.attr("tabindex", "-1"); // Adding tabindex for elements not focusable
                $target.focus(); // Set focus again
              }
            }
          );
        }
      }
    });
});
