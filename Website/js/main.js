$(window).on('load', function () {
     $('#disclaimer').modal('show');
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$('a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function (event) {
        // On-page links
        if (
            location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') &&
            location.hostname == this.hostname
        ) {
            // Figure out element to scroll to
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            // Does a scroll target exist?
            if (target.length) {
                // Only prevent default if animation is actually gonna happen
                event.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000, function () {
                    // Callback after animation
                    // Must change focus!
                    var $target = $(target);
                    $target.focus();
                    if ($target.is(":focus")) { // Checking if the target was focused
                        return false;
                    } else {
                        $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                        $target.focus(); // Set focus again
                    };
                });
            }
        }
    });

google.charts.load('current', {
    'packages': ['geochart'],
    // Note: you will need to get a mapsApiKey for your project.
    // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
    'mapsApiKey': 'AIzaSyBt2m_IULu3HeqlBxOn8OcSTO9HCtCkrVU'
});
google.charts.setOnLoadCallback(drawRegionsMap);


var options = {
    legend:'none',
    region: 'SO',
    backgroundColor: '#000E4A',
    resolution: 'provinces',
    colorAxis: {
        minValue: 1,
        colors: ['#2c5df5', '#b400ff', '#ff0000']
    },
    datalessRegionColor: '#000E4A'
};


/* Start data parse */
///////////////////////////////////////////////////////////////////////////////
var mapdata = [

      ['Region', 'Displacement Severity']
];

var month;

var status;

function downloadSpreadsheet(url) {
    return new Promise(function (resolve, reject) {
        axios.get(url, {
            responseType: 'arraybuffer'
        }).then(function (response) {
            resolve(response)
        }).catch(function (error) {
            console.log(error);
            reject(error);
        });
    })
}

function loadWorkbook(data) {
    return new Promise(function (resolve, reject) {
        var workbook = new window.ExcelJS.Workbook();
        workbook.xlsx.load(data).then(function () {
            resolve(workbook);
        }).catch(function (error) {
            console.log(error);
            reject(error);
        });
    });
}

function downloadAndLoadWorkbook(url) {
    return new Promise(function (resolve, reject) {
        downloadSpreadsheet(url).then(function (response) {
            loadWorkbook(response.data).then(function (workbook) {
                resolve(workbook);
            }).catch(function (error) {
                console.log(error);
                reject(error);
            });
        }).catch(function (error) {
            console.log(error);
            reject(error);
        });
    });
}

// https://stackoverflow.com/a/30800715/2410292
function downloadObjectAsJson(exportObj, exportName) {
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

function getCombinedData() {
    return new Promise(function (resolve, reject) {

        const predictionsXLSXURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRWHN3E7tMgskw5R7u-MQwkuI9TnxeTfYQdWF96D5bZWgpMjfwcZNJ5HS_80LdsSTrUICGdbUo05iWi/pub?output=xlsx";
        const correlationsXLXSURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGcnmYMki3euv4bcsgBqBRY1-sDl6zkVl0gGC8THLygJoYlYnfm4cY5bVCA8BXnmciFXnp6aEvow31/pub?output=xlsx";

        console.log('Loading workbooks...');

        let loadPredictions = downloadAndLoadWorkbook(predictionsXLSXURL);
        let loadCorrelations = downloadAndLoadWorkbook(correlationsXLXSURL);

        Promise.all([loadPredictions, loadCorrelations]).then(function (workbooks) {
            console.log('Workbooks loaded.');

            const predictionsWorkbook = workbooks[0];
            const correlationsWorkbook = workbooks[1];
            const latestResultsSheet = predictionsWorkbook.getWorksheet("LATEST RESULTS");

            var latestResultsCombined = [];

            latestResultsSheet.eachRow({
                includeEmpty: false
            }, function (latestResultRow, rowNumber) {
                if (rowNumber === 1) {
                    return;
                }

                const latestResultMonth = latestResultRow.values[1];
                const region = latestResultRow.values[2];
                const algorithms = [
                    latestResultRow.values[3],
                    latestResultRow.values[4],
                    latestResultRow.values[5]
                  ];



                const predstatus = [
                    latestResultRow.values[7],
                    latestResultRow.values[8],
                    latestResultRow.values[9]
                  ];


                // Get the values for the algorithms
                const algorithmsWithValues = algorithms.map(function (algorithmName, idx) {
                    // Clean up sheet names (remove underscores)
                    const correlationsSheetName = region.replace('_', ' ');

                    // Read the relevant sheet for the algorithm
                    const correlationsSheet = correlationsWorkbook.getWorksheet(
                        correlationsSheetName
                    );

                    if (correlationsSheet === undefined) {
                        console.log('Could not find sheet "' + correlationsSheetName + '" in the "correlations" workbook.');
                        return;
                    }

                    let algorithmValue = null;
                    let correlationHeaderRow = null;
                    correlationsSheet.eachRow({
                        includeEmpty: false
                    }, function (correlationsRow, rowNumber) {
                        if (rowNumber === 1) {
                            correlationHeaderRow = correlationsRow.values;
                            return
                        }
                        const correlationDate = correlationsRow.values[1];

                        const d1 = new Date(latestResultMonth);
                        const d2 = new Date(correlationDate);

                        if (d1.getYear() === d2.getYear() && d1.getMonth() === d2.getMonth()) {
                            // Get the correct cell index based on the position of the column
                            // in correlationHeaderRow
                            const columnIndex = correlationHeaderRow.indexOf(algorithmName)
                            if (columnIndex !== -1) {
                                algorithmValue = correlationsRow.values[columnIndex];
                                return;
                            }
                        }
                    });

                    return {
                        name: algorithmName,
                        value: algorithmValue
                    }
                });

                // Append the results to the output array
                latestResultsCombined.push({
                    month: latestResultMonth,
                    region: region,
                    algorithms: algorithmsWithValues,
                    status: predstatus
                })

            });

            resolve(latestResultsCombined);
        });
    });
}

// Usage

getCombinedData().then(function (data) {
    for (var x = 0; x < data.length; x++) {

        var item = data[x];

        var region = item['region'];
        var badregion;

        month = item['month'];

//        var alg1 = item['algorithms'][0].value;
//        var alg2 = item['algorithms'][1].value;
//        var alg3 = item['algorithms'][2].value;

        // function to change names to regions
        if (region == 'Middle_Shabelle') {
            badregion = region;
            region = 'Shabeellaha Dhexe'
        };
        if (region == 'Lower_Shabelle') {
            badregion = region;
            region = 'Shabeellaha Hoose'
        };
        if (region == 'Woqooyi_Galbeed') {
            badregion = region;
            region = 'Woqooyi Galbeed'
        };
        if (region == 'Galgaduud') {
            badregion = region;
            region = 'Galguduud'
        };
        if (region == 'Middle_Juba') {
            badregion = region;
            region = 'Jubbada Dhexe'
        };
        if (region == 'Lower_Juba') {
            badregion = region;
            region = 'Jubbada Hoose'
        };
        if (region == 'Hiraan') {
            badregion = region;
            region = 'Hiiraan'
        };
        if (region == 'Banadir') {
            badregion = region;
            region = 'Banaadir'
        };
        if (region == 'Dollo_Ado') {
            badregion = region;
            region = 'Dollo Ado'
        };
        
        

        // function for status update


        if ((item['status'][0] == region) || (item['status'][0] == badregion)) {
            finalstatus = 3;
            console.log('critical ' + region + ' ' + item['status'][0]);
        };

        if ((item['status'][1] == region) || (item['status'][1] == badregion)) {
            finalstatus = 2;
            console.log('mid ' + region + ' ' + item['status'][1]);
        };

        if ((item['status'][2] == region) || (item['status'][2] == badregion)) {
            finalstatus = 1;
            console.log('low ' + region + ' ' + item['status'][2]);
        };
        //        
        //   
        console.log(data);     

//        var avg = (alg1 + alg2 + alg3) / 3;
//
//        function round(number, precision) {
//            var shift = function (number, precision, reverseShift) {
//                if (reverseShift) {
//                    precision = -precision;
//                }
//                var numArray = ("" + number).split("e");
//                return +(numArray[0] + "e" + (numArray[1] ? (+numArray[1] + precision) : precision));
//            };
//            return shift(Math.round(shift(number, precision, false)), precision, true);
//        }
//        avg = round(avg, 0);

        mapdata.push(
        [region, finalstatus]
        );

    }

    //    mapdata = JSON.stringify([mapdata]);
    //    
    //    mapdata;
    // Uncomment the next line to download the JSON file in the browser
    // downloadObjectAsJson(data, 'data')
})


/* End data parse */
///////////////////////////////////////////////////////////////////////////////


function drawRegionsMap() {

    $('#show_map').click(function () {

        var data = google.visualization.arrayToDataTable(mapdata);

        console.log(mapdata);

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

        $("#regions_div").slideToggle("normal", function () {
            chart.draw(data, options);

            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

            const d = new Date(month);
            month = monthNames[d.getMonth()];

            $(".map-title h2").html('<span class="ti-calendar"></span> Predictions for the month of ' + month);
            $(".map-title").toggle()
        });
    });
}