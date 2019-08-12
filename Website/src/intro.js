import $ from "jquery";
import {
    GoogleCharts
} from "google-charts";
import iso3166 from "iso-3166-2";
import Chart from "chart.js";
import Swiper from "swiper";
import {
    downloadAndLoadWorkbook
} from "./spreadsheet";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

var shapeanimations = ['fast-spin-right', 'fast-spin-left', 'spin-left', 'spin-right']
$('.anim-shape').each(function () {
    var rand = ~~(Math.random() * shapeanimations.length)
    $(this).addClass(shapeanimations[rand])
});


// Jetson Intro

$.ajax({
    url: "https://www.unhcr.org/innovation/wp-json/wp/v2/pages/27745",
    // url: "json/intro.json",
    type: "GET",
    success: data => {


        // Main intro

        $(".hero-caption .content").prepend(data.acf.intro);

        //
        // Tech specs intro

        $('#techspecsintro').html(data.acf.technical_specs_intro);


        // Story intro

        $('#storyintro').html(data.acf.stories_intro);


        // Disclaimer

        $("#disclaimer .content").html(data.acf.disclaimer);


    }
}).done(function () {

    $(() => {
        $('[data-toggle="tooltip"]').tooltip();
    });

    // Slider

    var episwiper = new Swiper('#epilogue', {
        slidesPerView: 1,
        direction: 'vertical',
        parallax: true,
        speed: 1000,
        mousewheel: true
        // init: false,
    });


    $('#epibutton').click(function () {
        episwiper.slideNext();
    });

});
