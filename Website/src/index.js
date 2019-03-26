import "@babel/polyfill";
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
import "./style.scss";

Chart.defaults.line.spanGaps = true;
var data;

$.ajax({
    // url: "https://www.unhcr.org/innovation/wp-json/wp/v2/pages/27745",
    url: "json/data.json",
    type: "GET",
    success: data => {
        // Section
        $(".hero .content").prepend(data.acf.intro);
        $(".intro .content").prepend(data.acf.first_section);
        $(".prediction .content").prepend(data.acf.jetson_models);
        $(".engine .content").prepend(data.acf.second_section);
        $(".epilogue .content").prepend(data.acf.third_section);

        // Articles
        $(".article-one h2").html(data.acf.articles[0].article_title);
        $(".article-one h5").html(data.acf.articles[0].article_type);
        $(".article-one a").attr("href", data.acf.articles[0].article_link);

        $(".article-two h2").html(data.acf.articles[1].article_title);
        $(".article-two h5").html(data.acf.articles[1].article_type);
        $(".article-two a").attr("href", data.acf.articles[1].article_link);

        // FAQS
        var faqlist = data.acf.faqs;
        var ids = 0;

        faqlist.forEach(i => {
            ids = ids + 1;
            $(".faqs-row").append(
                '<div class="col-sm-4"><h4 data-toggle="modal" data-target="#q' +
                ids +
                '"><span class="num"><span class="ti-comment-alt"></span></span> <strong>' +
                i.faq_title +
                "</strong></h4></div>"
            );

            $("body").append(
                '<div class="modal fade" id="q' +
                ids +
                '" tabindex="-1" role="dialog" aria-labelledby="q' +
                ids +
                '"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">' +
                i.faq_title +
                '</h4></div><div class="modal-body">' +
                i.faq_content +
                "</div></div></div></div>"
            );
        });

        // Disclaimer
        $("#disclaimer .content").html(data.acf.disclaimer);
    }
});

$(() => {
    $('[data-toggle="tooltip"]').tooltip();
});

// Slider

var sourcesswiper = new Swiper('#sources', {
    slidesPerView: 6,
    spaceBetween: 20,
    centerInsufficientSlides: true,
    slidesOffsetBefore:10,
    slidesOffsetAfter:10,
    // init: false,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        1024: {
            slidesPerView: 4,
            spaceBetween: 40,
        },
        768: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        640: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 10,
        }
    }
});

var partnerswiper = new Swiper('#partners', {
    slidesPerView: 6,
    spaceBetween: 20,
    centerInsufficientSlides: true,
    slidesOffsetBefore:10,
    slidesOffsetAfter:10,
    // init: false,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        1024: {
            slidesPerView: 4,
            spaceBetween: 40,
        },
        768: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        640: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 10,
        }
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
            target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
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

var regionHistoryChart;

const drawRegionsMap = () => {
    $("#show_map").click(() => {
        var data = GoogleCharts.api.visualization.arrayToDataTable(mapdata);
        var regionMap = new GoogleCharts.api.visualization.GeoChart(
            document.getElementById("regions_div")
        );

        $("#regions_div").slideToggle("normal", () => {
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
                    }, (row, rowNumber) => {
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
                        predictionsWorkbook
                            .getWorksheet("Red Light Test")
                            .eachRow({
                                includeEmpty: false
                            }, redLightRow => {
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
                            });

                        let actual = null;
                        predictionsWorkbook
                            .getWorksheet("Arrivals_Historical")
                            .eachRow({
                                includeEmpty: false
                            }, arrivalsRow => {
                                const arrivalDate = arrivalsRow.getCell(1).value.result;
                                if (
                                    arrivalDate instanceof Date &&
                                    arrivalDate.getTime() === date.getTime()
                                ) {
                                    actual = arrivalsRow.getCell(regionCol).value.result;
                                }
                            });

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
                    });

                    console.log(datelLabels);
                    console.log(lowData);
                    console.log(actualData);
                    console.log(highData);

                    if (regionHistoryChart) {
                        regionHistoryChart.destroy();
                    }


                    const ctx = document.getElementById("region-chart").getContext("2d");


                    var gradient = ctx.createLinearGradient(0, 0, 0, 400);
                    gradient.addColorStop(0, 'rgba(179,38,251,0.5)');
                    gradient.addColorStop(1, 'rgba(48,98,241,0.5)');

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
                                    fontColor: 'rgba(255, 255, 255, 0.8)'
                                }
                            },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        fontColor: 'rgba(255, 255, 255, 0.8)'
                                    }
                    }],
                                xAxes: [{
                                    ticks: {
                                        fontColor: 'rgba(255, 255, 255, 0.8)'
                                    }
                    }]
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

            regionMap.draw(data, options);

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
        });
    });
};

GoogleCharts.load(drawRegionsMap, {
    packages: ["geochart"],
    mapsApiKey: "AIzaSyBt2m_IULu3HeqlBxOn8OcSTO9HCtCkrVU"
});

var options = {
    legend: "none",
    region: "SO",
    backgroundColor: "#000E4A",
    enableRegionInteractivity: true,
    resolution: "provinces",
    colorAxis: {
        minValue: 0,
        values: [0, 1, 2, 3],
        colors: ["#000E4A", "#2c5df5", "#b400ff", "#ff0000"]
    },
    datalessRegionColor: "#000E4A"
};

/* Start data parse */
///////////////////////////////////////////////////////////////////////////////
var mapdata = [["Region", "Displacement Severity"]];
var month;

var predictionsWorkbook;

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

            $(".loader").fadeOut(200, function () {
                // $("#disclaimer").modal("show");
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
            });

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
                    const algorithmsWithValues = algorithms.map((algorithmName, idx) => {
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
                                        algorithmValue = correlationsRow.getCell(columnIndex).value;
                                        return;
                                    }
                                }
                            }
                        );

                        return {
                            name: algorithmName,
                            value: algorithmValue
                        };
                    });

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
        } else if (item["status"][1] == region || item["status"][1] == badregion) {
            finalstatus = 2;
            console.log("mid " + region + " " + item["status"][1]);
        } else if (item["status"][2] == region || item["status"][2] == badregion) {
            finalstatus = 1;
            console.log("low " + region + " " + item["status"][2]);
        } else {
            finalstatus = 0;
            console.log("low " + region + " " + finalstatus);
        }

        mapdata.push([region, finalstatus]);
    }
});