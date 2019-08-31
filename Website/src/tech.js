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

var shapeanimations = [
  "fast-spin-right",
  "fast-spin-left",
  "spin-left",
  "spin-right"
];
$(".anim-shape").each(function () {
    var rand = ~~(Math.random() * shapeanimations.length);
    $(this).addClass(shapeanimations[rand]);
});

var mapdata;
var predictionsWorkbook;
var month;

const state = {
    loading: false
};

// Data

$.ajax({
      url: "https://www.unhcr.org/innovation/wp-json/wp/v2/pages/29889",
//    url: "json/tech.json",
    type: "GET",
    success: data => {


        $('.place-cont').hide();
        // Title

        $(".techtitle").html(data.title.rendered);

        // Sections

        var sectionlist = data.acf.sections;
        var ids = 0;
        var articlesliders = 0;
        var logosliders = 0;

        sectionlist.forEach(i => {
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

                faqlist.forEach(i => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var articleslides = i.article_slider;
                        articleslides.forEach(x => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var articleslides = i.article_slider;

                        articleslides.forEach(x => {
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
                            .attr("id", next1);
                        var prevarrow1 = document.createElement("div");
                        $(prevarrow1)
                            .attr("class", "swiper-button-prev")
                            .attr("id", prev1);

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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var articleslides = i.article_slider;
                        articleslides.forEach(x => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var articleslides = i.article_slider;

                        articleslides.forEach(x => {
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
                            .attr("id", next1);
                        var prevarrow1 = document.createElement("div");
                        $(prevarrow1)
                            .attr("class", "swiper-button-prev")
                            .attr("id", prev1);

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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var logoslides = i.logo_slider;
                        logoslides.forEach(x => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var logoslides = i.logo_slider;
                        logoslides.forEach(x => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var logoslides = i.logo_slider;
                        logoslides.forEach(x => {
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
                            padding: "10px 0 80px"
                        });

                        // Add to slider
                        var logoslides = i.logo_slider;
                        logoslides.forEach(x => {
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

            $(".maintech").append(section);
        });

        // Disclaimer
        $("#disclaimer .content").html(data.acf.disclaimer);
    }
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
        mousewheel: true
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
            prevEl: "#prev1"
        }
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
            prevEl: "#prev2"
        }
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
            clickable: true
        },
        navigation: {
            nextEl: "#next3",
            prevEl: "#prev3"
        }
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
            clickable: true
        },
        navigation: {
            nextEl: "#next4",
            prevEl: "#prev4"
        }
    });

    $('a[href*="#"]')
        // Remove links that don't actually link to anything
        .not('[href="#"]')
        .not('[href="#0"]')
        .click(event => {
            // On-page links
            if (
                location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
                location.hostname == this.hostname
            ) {
                // Figure out element to scroll to
                var target = $(this.hash);
                target = target.length ?
                    target :
                    $("[name=" + this.hash.slice(1) + "]");
                // Does a scroll target exist?
                if (target.length) {
                    // Only prevent default if animation is actually gonna happen
                    event.preventDefault();
                    $("html, body").animate({
                            scrollTop: target.offset().top
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

    $("#disclaimer").modal("show");
    $("section")
        .not(".prediction, .faqs, .articles, .page-content")
        .each(function () {
            if ($(this).height() > 500) {
                $(this)
                    .addClass("minified")
                    .append(
                        '<div class="more view"><div class="container"><button class="showme btn">Expand this section <span class="ti-arrow-down"></span></button><button class="hideme btn"> Minimise this section <span class="ti-arrow-up"></span></button></div></div>'
                    );
                $(".more")
                    .unbind("click")
                    .click(function (e) {
                        e.stopPropagation();
                        $(this)
                            .parent()
                            .toggleClass("minified");
                        $(this).toggleClass("view");
                        console.log(
                            $(this)
                            .parent()
                            .attr("class")
                        );
                    });
            }
        });

    $("#show_map").click(function () {
        document.getElementById(
            "regions_div"
        ).innerHTML = `<div style="display: flex; align-items: center; justify-content: center; height: 100%;">Loading...</div>`;

        $("#regions_div").slideToggle("normal");

        var regionHistoryChart;

        const drawRegionsMap = () => {
            var data = GoogleCharts.api.visualization.arrayToDataTable(mapdata);
            var regionMap = new GoogleCharts.api.visualization.GeoChart(
                document.getElementById("regions_div")
            );

            GoogleCharts.api.visualization.events.addListener(
                regionMap,
                "regionClick",
                e => {
                    // https://en.wikipedia.org/wiki/ISO_3166-2:SO
                    const countryName = iso3166.country(e.region) ?
                        iso3166.country(e.region).name :
                        null;
                    const regionName = iso3166.subdivision(e.region) ?
                        iso3166.subdivision(e.region).name :
                        null;
                    if (!regionName && !countryName) {
                        return;
                    }

                    $("#region-modal .modal-title").text(
                        countryName ? countryName : regionName
                    );

                    const winnersSheet = predictionsWorkbook.getWorksheet(
                        "MODEL TRENDS - WINNERS"
                    );

                    let regionNames = [];
                    let regionCol = null;
                    let regionSheetName = null;
                    winnersSheet.getRow(1).eachCell((cell, colNumber) => {
                        if (colNumber === 1) {
                            return;
                        }
                        regionNames.push(cell.value);
                        // Get the column number for the region that was clicked
                        if (cell.value === regionName) {
                            regionCol = colNumber;
                            regionSheetName = cell.value;
                        } else {
                            // Somali spellings
                            if (
                                (regionName === "Galguduud" && cell.value === "Galgaduud") ||
                                (regionName === "Shabeellaha Dhexe" &&
                                    cell.value === "Middle Shabelle") ||
                                (regionName === "Shabeellaha Hoose" &&
                                    cell.value === "Lower Shabelle") ||
                                (regionName === "Jubbada Dhexe" &&
                                    cell.value === "Middle Juba") ||
                                (regionName === "Jubbada Hoose" && cell.value === "Lower Juba")
                            ) {
                                regionCol = colNumber;
                                regionSheetName = cell.value;
                            }
                        }
                    });

                    let lowData = [];
                    let actualData = [];
                    let highData = [];
                    let datelLabels = [];

                    winnersSheet.eachRow({
                            includeEmpty: false
                        },
                        (row, rowNumber) => {
                            if (rowNumber === 1 || !row.getCell(1).value) {
                                return;
                            }
                            const date = row.getCell(1).value;
                            // Read the winning models from regionCol at the current row and subsequent two rows

                            const winningPredictions = [
                winnersSheet.getCell(rowNumber, regionCol).value,
                winnersSheet.getCell(rowNumber + 1, regionCol).value,
                winnersSheet.getCell(rowNumber + 2, regionCol).value
              ];

                            /*
                        Find the corresponding value for the winning algorithms in the 'Red Light Test' sheet
                        For each row
                        Check the first cell and match the date
                        Check the second cell and match the region
            
                        Find the min and max from cells 7, 8 and 9

                        For each row in the 'Arrivals_Historical' sheet, match the date with the first cell
                        Use the regionCol col above to find the actual value for this region
                        */

                            let predictionMax = null;
                            let predictionMin = null;
                            predictionsWorkbook.getWorksheet("Red Light Test").eachRow({
                                    includeEmpty: false
                                },
                                redLightRow => {
                                    const redLightDate = redLightRow.getCell(1).value;
                                    if (
                                        redLightDate instanceof Date &&
                                        redLightDate.getTime() === date.getTime() &&
                                        redLightRow.getCell(2).value.replace("_", " ") ===
                                        regionSheetName
                                    ) {
                                        predictionMax = Math.max(
                                            redLightRow.getCell(7).value,
                                            redLightRow.getCell(8).value,
                                            redLightRow.getCell(9).value
                                        );
                                        predictionMin = Math.min(
                                            redLightRow.getCell(7).value,
                                            redLightRow.getCell(8).value,
                                            redLightRow.getCell(9).value
                                        );
                                    }
                                }
                            );

                            let actual = null;
                            predictionsWorkbook.getWorksheet("Arrivals_Historical").eachRow({
                                    includeEmpty: false
                                },
                                arrivalsRow => {
                                    const arrivalDate = arrivalsRow.getCell(1).value.result;
                                    if (
                                        arrivalDate instanceof Date &&
                                        arrivalDate.getTime() === date.getTime()
                                    ) {
                                        actual = arrivalsRow.getCell(regionCol).value.result;
                                    }
                                }
                            );

                            datelLabels.push(date.toLocaleDateString());
                            lowData.push({
                                x: date.getTime(),
                                y: predictionMin
                            });
                            actualData.push({
                                x: date.getTime(),
                                y: actual
                            });
                            highData.push({
                                x: date.getTime(),
                                y: predictionMax
                            });
                        }
                    );

                    console.log(datelLabels);
                    console.log(lowData);
                    console.log(actualData);
                    console.log(highData);

                    if (regionHistoryChart) {
                        regionHistoryChart.destroy();
                    }

                    const ctx = document.getElementById("region-chart").getContext("2d");

                    var gradient = ctx.createLinearGradient(0, 0, 0, 400);
                    gradient.addColorStop(0, "rgba(179,38,251,0.5)");
                    gradient.addColorStop(1, "rgba(48,98,241,0.5)");

                    regionHistoryChart = new Chart(ctx, {
                        type: "line",
                        data: {
                            labels: datelLabels,
                            datasets: [
                                {
                                    label: "Highest prediction",
                                    fill: false,
                                    borderColor: "rgba(179,38,251,1)",
                                    backgroundColor: "rgba(179,38,251,1)",
                                    borderWidth: 1.8,
                                    pointRadius: 2.8,
                                    data: highData
                },
                                {
                                    label: "Actual",
                                    fill: false,
                                    borderColor: "#5ca91d",
                                    backgroundColor: "#5ca91d",
                                    borderWidth: 1.8,
                                    pointRadius: 2.8,
                                    data: actualData
                },
                                {
                                    label: "Lowest prediction",
                                    fill: "-2",
                                    borderWidth: 1.8,
                                    pointRadius: 2.8,
                                    borderColor: "rgba(48,98,241,1)",
                                    backgroundColor: gradient,
                                    data: lowData
                }
              ]
                        },
                        options: {
                            legend: {
                                lineWidth: 8,
                                labels: {
                                    fontColor: "rgba(255, 255, 255, 0.8)"
                                }
                            },
                            scales: {
                                yAxes: [
                                    {
                                        ticks: {
                                            fontColor: "rgba(255, 255, 255, 0.8)"
                                        }
                  }
                ],
                                xAxes: [
                                    {
                                        ticks: {
                                            fontColor: "rgba(255, 255, 255, 0.8)"
                                        }
                  }
                ]
                            },

                            layout: {
                                padding: {
                                    left: 20,
                                    right: 20,
                                    top: 20,
                                    bottom: 20
                                }
                            }
                        }
                    });
                    $("#region-modal").modal("show");
                }
            );

            var options = {
                legend: "none",
                region: "SO",
                backgroundColor: "#ffffff",
                enableRegionInteractivity: true,
                resolution: "provinces",
                colorAxis: {
                    minValue: 0,
                    values: [0, 1, 2, 3],
                    colors: ["#ffffff", "#0072BC", "#4D00BC", "#BC0094"]
                },
                datalessRegionColor: "#ffffff"
            };

            regionMap.draw(data, options);
            console.log(data);

            const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ];

            const d = new Date(month);
            month = monthNames[d.getMonth()];

            $(".map-title h2").html(
                '<span class="ti-calendar"></span> Predictions for the month of ' +
                month
            );

            $(".map-title").toggle();

            const now = new Date();
            const current = new Date(now.getFullYear(), now.getMonth() - 1, 1);

            var nextmonth = monthNames[current.getMonth()];
            if (month != nextmonth) {
                $(".warning").show();
            }
        };

        /* Start data parse */
        ///////////////////////////////////////////////////////////////////////////////
        mapdata = [["Region", "Displacement Severity"]];

        const getCombinedData = () => {
            return new Promise((resolve, reject) => {
                const predictionsXLSXURL =
                    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRWHN3E7tMgskw5R7u-MQwkuI9TnxeTfYQdWF96D5bZWgpMjfwcZNJ5HS_80LdsSTrUICGdbUo05iWi/pub?output=xlsx";
                const correlationsXLXSURL =
                    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGcnmYMki3euv4bcsgBqBRY1-sDl6zkVl0gGC8THLygJoYlYnfm4cY5bVCA8BXnmciFXnp6aEvow31/pub?output=xlsx";

                console.log("Loading workbooks...");

                let loadPredictions = downloadAndLoadWorkbook(predictionsXLSXURL);
                let loadCorrelations = downloadAndLoadWorkbook(correlationsXLXSURL);

                Promise.all([loadPredictions, loadCorrelations]).then(workbooks => {
                    console.log("Workbooks loaded.");

                    predictionsWorkbook = workbooks[0];
                    const correlationsWorkbook = workbooks[1];
                    const latestResultsSheet = predictionsWorkbook.getWorksheet(
                        "LATEST RESULTS"
                    );

                    var latestResultsCombined = [];

                    latestResultsSheet.eachRow({
                            includeEmpty: false
                        },
                        (latestResultRow, rowNumber) => {
                            if (rowNumber === 1) {
                                return;
                            }

                            const latestResultMonth = latestResultRow.getCell(1).value;
                            const region = latestResultRow.getCell(2).value;
                            const algorithms = [
                latestResultRow.getCell(3).value,
                latestResultRow.getCell(4).value,
                latestResultRow.getCell(5).value
              ];

                            const predstatus = [
                latestResultRow.getCell(7).value,
                latestResultRow.getCell(8).value,
                latestResultRow.getCell(9).value
              ];

                            // Get the values for the algorithms
                            const algorithmsWithValues = algorithms.map(
                                (algorithmName, idx) => {
                                    // Clean up sheet names (remove underscores)
                                    let correlationsSheetName = region.replace("_", " ");

                                    // The sheet names are not correct...
                                    if (correlationsSheetName === "Middle Juba") {
                                        correlationsSheetName = "Middle_(D)_Jubbada";
                                    } else if (correlationsSheetName === "Lower Juba") {
                                        correlationsSheetName = "Lower_(H)_Jubbada";
                                    } else if (correlationsSheetName === "Middle Shabelle") {
                                        correlationsSheetName = "Middle_(D)_Shabelle";
                                    } else if (correlationsSheetName === "Lower Shabelle") {
                                        correlationsSheetName = "Lower_(H)_Shabelle";
                                    } else if (correlationsSheetName === "Woqooyi Galbeed") {
                                        correlationsSheetName = "Woqooyi";
                                    } else if (correlationsSheetName === "Dollo Ado") {
                                        correlationsSheetName = "Dollo";
                                    }

                                    // Read the relevant sheet for the algorithm
                                    const correlationsSheet = correlationsWorkbook.getWorksheet(
                                        correlationsSheetName
                                    );

                                    if (correlationsSheet === undefined) {
                                        console.log(
                                            'Could not find sheet "' +
                                            correlationsSheetName +
                                            '" in the "correlations" workbook.'
                                        );
                                        return;
                                    }

                                    let algorithmValue = null;
                                    let correlationHeaderRow = null;
                                    correlationsSheet.eachRow({
                                            includeEmpty: false
                                        },
                                        (correlationsRow, rowNumber) => {
                                            if (rowNumber === 1) {
                                                correlationHeaderRow = correlationsRow.values;
                                                return;
                                            }
                                            const correlationDate = correlationsRow.getCell(1).value;

                                            const d1 = new Date(latestResultMonth);
                                            const d2 = new Date(correlationDate);

                                            if (
                                                d1.getYear() === d2.getYear() &&
                                                d1.getMonth() === d2.getMonth()
                                            ) {
                                                // Get the correct cell index based on the position of the column
                                                // in correlationHeaderRow
                                                const columnIndex = correlationHeaderRow.indexOf(
                                                    algorithmName
                                                );
                                                if (columnIndex !== -1) {
                                                    algorithmValue = correlationsRow.getCell(columnIndex)
                                                        .value;
                                                    return;
                                                }
                                            }
                                        }
                                    );

                                    return {
                                        name: algorithmName,
                                        value: algorithmValue
                                    };
                                }
                            );

                            // Append the results to the output array
                            latestResultsCombined.push({
                                month: latestResultMonth,
                                region: region,
                                algorithms: algorithmsWithValues,
                                status: predstatus
                            });
                        }
                    );

                    resolve(latestResultsCombined);
                });
            });
        };

        getCombinedData().then(data => {
            for (var x = 0; x < data.length; x++) {
                var item = data[x];

                var region = item["region"];
                var badregion;

                month = item["month"];
                // function to change names to regions
                if (region == "Middle_Shabelle") {
                    badregion = region;
                    region = "Shabeellaha Dhexe";
                }
                if (region == "Lower_Shabelle") {
                    badregion = region;
                    region = "Shabeellaha Hoose";
                }
                if (region == "Woqooyi_Galbeed") {
                    badregion = region;
                    region = "Woqooyi Galbeed";
                }
                if (region == "Galgaduud") {
                    badregion = region;
                    region = "Galguduud";
                }
                if (region == "Middle_Juba") {
                    badregion = region;
                    region = "Jubbada Dhexe";
                }
                if (region == "Lower_Juba") {
                    badregion = region;
                    region = "Jubbada Hoose";
                }
                if (region == "Hiraan") {
                    badregion = region;
                    region = "Hiiraan";
                }
                if (region == "Banadir") {
                    badregion = region;
                    region = "Banaadir";
                }
                if (region == "Dollo_Ado") {
                    badregion = region;
                    region = "Dollo Ado";
                }

                let finalstatus;

                if (item["status"][0] == region || item["status"][0] == badregion) {
                    finalstatus = 3;
                    console.log("critical " + region + " " + item["status"][0]);
                } else if (
                    item["status"][1] == region ||
                    item["status"][1] == badregion
                ) {
                    finalstatus = 2;
                    console.log("mid " + region + " " + item["status"][1]);
                } else if (
                    item["status"][2] == region ||
                    item["status"][2] == badregion
                ) {
                    finalstatus = 1;
                    console.log("low " + region + " " + item["status"][2]);
                } else {
                    finalstatus = 0;
                    console.log("low " + region + " " + finalstatus);
                }

                mapdata.push([region, finalstatus]);
            }

            state.loading = false;

            GoogleCharts.load(drawRegionsMap, {
                packages: ["geochart"],
                mapsApiKey: "AIzaSyBt2m_IULu3HeqlBxOn8OcSTO9HCtCkrVU"
            });
        });
    });
});