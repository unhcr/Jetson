var map;
var migration_data = []; // Loaded from a CSV
var conflict_data = []; // Loaded from a CSV
var slider_start_year;
var slider_last_position = null;
var csvs_loaded = 0; // Check if all CSVs are loaded before performing some actions
var num_months;
var timeout_ids = [];

$(function () {
    initializeMap();
    $("#autoplay").click(function () {
        if ($("#autoplay").html() == '<span class="ti-control-play"></span>') {
            play();
            $("#autoplay").html('<span class="ti-control-pause"></span>');
        } else {
            clearTimeouts();
            $("#autoplay").html('<span class="ti-control-play"></span>');
        }
    });
});

$('.circle-holder').whenInViewport(function ($circ) {
        setTimeout(function () {
            $circ.addClass('active-circ');
        }, 2000);
    }, {
        threshold: -350 // difference in pixels from user scroll position
    }

);

// Read in the migration data from CSV
Papa.parse("data/data-large.csv", {
    download: true,
    dynamicTyping: true,
    worker: false,
    step: function (results) {
        migration_data.push(results.data);
    },
    complete: function () {
        console.log("Migration data from CSV loaded.");
        csvs_loaded++;
        checkAllDataLoaded();
    }
});

// Read in the conflict data from CSV
Papa.parse("data/conflict_clean.csv", {
    download: true,
    dynamicTyping: true,
    worker: false,
    step: function (results) {
        conflict_data.push(results.data);
    },
    complete: function () {
        console.log("Conflict data from CSV loaded.");
        csvs_loaded++;
        checkAllDataLoaded();
    }
});


function checkAllDataLoaded() {
    if (csvs_loaded === 2) {
        setupSlider();
        setSliderLimits();
        setupToggles();
        $('#loading').hide();
    }
}

function setupSlider() {
    // http://rangeslider.js.org/
    $('#slider').rangeslider({
        polyfill: false,
        onSlide: function (position, value) {
            if (value !== slider_last_position) {
                slider_last_position = value;
                drawMapOverlays(value);
            }
            $('.yr-btn').blur();
        },
    });
}

function setupToggles() {
    $('#display_lines, #display_heatmaps').change(function () {
        var slider_value = parseInt($('#slider').val());
        drawMapOverlays(slider_value);
    });
}

function drawMapOverlays(slider_value) {
    var years_to_add = Math.floor(slider_value / 12);
    var year = slider_start_year + years_to_add;
    var month = (slider_value % 12) + 1;

    removeLines();
    removeHeatmap();

    if ($('#display_lines').is(":checked")) {
        drawLinesByMonth(month, year);
    }
    if ($('#display_heatmaps').is(":checked")) {
        drawHeatmapByMonth(month, year);
    }
    $('#month_year').text(month + '/' + year);


    $('.yr-btn').each(function () {
        var yrid = $(this).attr('id');
        if (yrid === 'yr_' + year) {
            $('.yr-btn').removeClass('active-btn');
            $(this).addClass('active-btn');
        }
    });


}


var Baidoa, Doolow, Luuq, Mogadishu, Melkadida, Ifo, Guriceel;

var Marker = google.maps.Marker;

var Point = google.maps.Point;

var curvature = 0.2; // how curvy to make the arc

function initializeMap() {

    var mapCenter = new google.maps.LatLng(5.646663, 46.311971);

    var mapOptions = {
        zoom: 6,
        center: mapCenter,
        scrollwheel: false,
        disableDefaultUI: true,
        styles: [
            {
                "stylers": [
                    {
                        "visibility": "simplified"
            }
        ]
    },
            {
                "stylers": [
                    {
                        "color": "#131314"
            }
        ]
    },
            {
                "featureType": "water",
                "stylers": [
                    {
                        "color": "#131313"
            },
                    {
                        "lightness": 7
            }
        ]
    },
            {
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
            },
                    {
                        "lightness": 25
            }
        ]
    }
]
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    Baidoa = new RichMarker({
        position: new google.maps.LatLng(3.114676, 43.651986),
        map: map,
        draggable: false,
        content: '<div class="marker">Baidoa</div>',
        flat: true,
    });

    Mogadishu = new RichMarker({
        position: new google.maps.LatLng(2.049079, 45.317136),
        map: map,
        draggable: false,
        content: '<div class="marker main-marker">Mogadishu</div>',
        flat: true,
    });

    Doolow = new RichMarker({
        position: new google.maps.LatLng(4.164191, 42.079365),
        map: map,
        draggable: false,
        content: '<div class="marker">Doolow</div>',
        flat: true,
    });

    Luuq = new RichMarker({
        position: new google.maps.LatLng(3.813436, 42.545970),
        map: map,
        draggable: false,
        content: '<div class="marker">Luuq</div>',
        flat: true,
    });

    Ifo = new RichMarker({
        position: new google.maps.LatLng(0.110593, 40.314245),
        map: map,
        draggable: false,
        content: '<div class="marker">Ifo</div>',
        flat: true,
    });

    Guriceel = new RichMarker({
        position: new google.maps.LatLng(5.303570, 45.880022),
        map: map,
        draggable: false,
        content: '<div class="marker">Guriceel</div>',
        flat: true,
    });
}


function setSliderLimits() {
    // Calculate the number of values to add to the slider
    // A value here is a month in a year

    // Get the first data line's year
    var date = migration_data[0][0][0];
    var date_split = date.split('/');
    var max_year = parseInt(date_split[2]);
    var min_year = parseInt(date_split[2]);

    for (var x in migration_data) {
        if (x === 0) {
            continue; // Already checked this data point above
        }
        var data_line = migration_data[x][0];
        var date = data_line[0];
        var date_split = date.split('/');
        var year = parseInt(date_split[2]);

        if (year < min_year) {
            min_year = year;
        }

        if (year > max_year) {
            max_year = year;
        }
    }

    for (var x in conflict_data) {
        if (x === 0) {
            continue; // Don't check the first header line
        }
        var data_line = conflict_data[x][0];
        var date = data_line[0];
        var date_split = date.split('/');
        var year = parseInt(date_split[0]);

        if (year < min_year) {
            min_year = year;
        }

        if (year > max_year) {
            max_year = year;
        }
    }

    slider_start_year = min_year;

    // Calculate the min month in the first year and max month in the last year?
    num_months = (max_year - min_year + 1) * 12 - 1;

    $('#slider').attr({
        min: 0,
        max: num_months,
    });

    $('#slider').rangeslider('update', true);
}


var polylines = [];
var markers = [];

function drawLinesByMonth(month_in, year_in) {

    var lineSymbol = {
        path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
    };

    // Draw polylines for all lines in the csv that fall within a month and year
    for (var x in migration_data) {
        var data_line = migration_data[x][0];
        var date = data_line[0];
        var date_split = date.split('/');
        var month = parseInt(date_split[1]);
        var year = parseInt(date_split[2]);

        if (month === month_in && year === year_in) {
            var previous_coord = {
                lat: data_line[10],
                lng: data_line[11]
            };
            var current_coord = {
                lat: data_line[5],
                lng: data_line[6]
            };

            // Check validity of data
            if (previous_coord.lat === '' || previous_coord.lng === '' ||
                current_coord.lat === '' || current_coord.lng === '') {
                // console.log('Invalid coordintate(s) on row ' + x + 1)
                continue;
            }

            var polygon_path = [previous_coord, current_coord];

            var pos1 = previous_coord;
            var pos2 = current_coord;

            var markerP1 = new Marker({
                position: pos1,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 1.25,
                    fillColor: '#FFAA00',
                    fillOpacity: 0.35,
                    strokeWeight: 0
                },
                draggable: true
            });
            var markerP2 = new Marker({
                position: pos2,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 1.25,
                    fillColor: '#00f5a7',
                    fillOpacity: 0.35,
                    strokeWeight: 0
                },
                draggable: true,
            });


            markers.push(markerP1)
            markers.push(markerP2)

            var curveMarker;

            //        var pos1 = data_line[11]+','+data_line[12], // latlng
            //            pos2 = data_line[5]+','+data_line[6],

            function updateCurveMarker() {
                var pos1 = markerP1.getPosition(), // latlng
                    pos2 = markerP2.getPosition(),
                    projection = map.getProjection(),
                    p1 = projection.fromLatLngToPoint(pos1), // xy
                    p2 = projection.fromLatLngToPoint(pos2);
                // Calculate the arc.
                // To simplify the math, these points 
                // are all relative to p1:
                var e = new Point(p2.x - p1.x, p2.y - p1.y), // endpoint (p2 relative to p1)
                    m = new Point(e.x / 2, e.y / 2), // midpoint
                    o = new Point(e.y, -e.x), // orthogonal
                    c = new Point( // curve control point
                        m.x + curvature * o.x,
                        m.y + curvature * o.y);

                var pathDef = 'M 0,0 ' +
                    'q ' + c.x + ',' + c.y + ' ' + e.x + ',' + e.y;

                var zoom = map.getZoom(),
                    scale = 1 / (Math.pow(2, -zoom));

                var symbol = {
                    path: pathDef,
                    scale: scale,
                    strokeColor: '#00a2ff',
                    strokeOpacity: 0.3,
                    strokeWeight: 0.7
                };


                curveMarker = new Marker({
                    position: pos1,
                    clickable: false,
                    icon: symbol,
                    zIndex: 0, // behind the other markers
                    map: map
                });
            }

            updateCurveMarker();




            // Sets the map on all markers in the array.
            function setMapOnAll(map) {
                for (var i = 0; i < markers.length; i++) {
                    markers[i].setMap(map);
                }
            }

            polylines.push(curveMarker);


            var line = polylines[polylines.length - 1];


            google.maps.event.addListener(map, 'projection_changed', updateCurveMarker);
            google.maps.event.addListener(map, 'zoom_changed', updateCurveMarker);

            google.maps.event.addListener(markerP1, 'position_changed', updateCurveMarker);
            google.maps.event.addListener(markerP2, 'position_changed', updateCurveMarker);


            //            animateCircle(line);

            // Use the DOM setInterval() function to change the offset of the symbol
            // at fixed intervals.
            //            function animateCircle(line) {
            //                var count = 0;
            //                window.setInterval(function () {
            //                    count = (count + 1) % 120;
            //
            //                    var icons = line.get('icons');
            //                    icons[0].offset = (count / 1.2) + '%';
            //                    line.set('icons', icons);
            //                }, 1);
            //            }
        }
    }




    // Draw the new polylines
    for (var x in polylines) {
        polylines[x].setMap(map);
    }
    for (var y in markers) {
        markers[y].setMap(map);
    }
}


function removeLines() {
    // Remove existing polylines from the map
    for (var x in polylines) {
        polylines[x].setMap(null);
    }
    for (var y in markers) {
        markers[y].setMap(null);
    }

    polylines = [];
    markers = [];
}


var heatmap;

function drawHeatmapByMonth(month_in, year_in) {

    removeHeatmap();

    var heatmapData = []

    // Draw a heatmap for conflict data points that exist in the csv
    for (var x in conflict_data) {
        if (x === 0) {
            continue; // Don't check the first header line
        }

        var data_line = conflict_data[x][0];
        var date = data_line[0];
        var date_split = date.split('/');
        var month = parseInt(date_split[1]);
        var year = parseInt(date_split[0]);

        if (month === month_in && year === year_in) {
            var current_coord = {
                lat: data_line[2],
                lng: data_line[3]
            };
            var fatalities = (parseInt(data_line[4])) * 0.5;

            // Check validity of data
            if (current_coord.lat === '' || current_coord.lng === '') {
                console.log('Invalid coordintate(s) on row ' + x + 1)
                continue;
            }

            heatmapData.push({
                location: new google.maps.LatLng(
                    current_coord.lat, current_coord.lng
                ),
                weight: fatalities
            })
        }
    }

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        dissipating: false,
        radius: 0.5
    });

    console.log('Drawing the heatmap.')

    // Draw the new heatmap
    heatmap.setMap(map);

    var gradient = [
          'rgba(131, 0, 70, 0)',
          'rgba(164, 0, 89, 0.4)',
          'rgba(201, 0, 71, 0.6)',
          'rgba(255, 0, 0, 1)'
        ]
    heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function removeHeatmap() {
    if (heatmap !== undefined) {
        heatmap.setMap(null);
    }
}

function playFromStart() {
    // Reset the slider
    $('#slider').val(0).change();
    play();
}

function play() {
    var interval = 100;

    function incrementSlider(value) {
        var current_val = parseInt($('#slider').val());
        $('#slider').val(current_val + 1).change();
    }

    for (var x = 0; x <= num_months; x++) {
        timeout_ids.push(window.setTimeout(incrementSlider, interval * (x + 1)));
    }

    // console.log(timeout_ids);
}

// button functions

$('#yr_2010').click(function () {
    $('#slider').val(0).change();
});
$('#yr_2011').click(function () {
    $('#slider').val(12).change();
});
$('#yr_2012').click(function () {
    $('#slider').val(24).change();
});
$('#yr_2013').click(function () {
    $('#slider').val(36).change();
});
$('#yr_2014').click(function () {
    $('#slider').val(48).change();
});
$('#yr_2015').click(function () {
    $('#slider').val(60).change();
});
$('#yr_2016').click(function () {
    $('#slider').val(72).change();
});
$('#yr_2017').click(function () {
    $('#slider').val(84).change();
});




function clearTimeouts() {
    for (var x = 0; x <= timeout_ids.length; x++) {
        window.clearTimeout(timeout_ids[x]);
    }
}

/* start animations */

$('#prc_btn').click(function () {
    $('body').addClass('active-canv');
    $('body').append('<div class="overlay"></div>')
    $('#process').addClass('active-content');
    $('body, html').animate({
        scrollTop: $('#prc_data').offset().top
    }, 500);
});

$('#dta_btn').click(function () {
    $('body').addClass('active-canv');
    $('body').append('<div class="overlay"></div>')
    $('#data').addClass('active-content');
    $('body, html').animate({
        scrollTop: $('#prc_data').offset().top
    }, 500);
});


$('.close-btn').click(function () {
    $('body').removeClass('active-canv');
    $('.overlay').remove();
    $('.off-canvas-content').removeClass('active-content');
    $('body, html').animate({
        scrollTop: $('#prc_data').offset().top
    }, 500);
});

$('#engineshow').click(function () {
    $('.engine-if').show();
    $('.engine-bg').show();
});

$('#enginehide').click(function () {
    $('.engine-if').hide();
    $('.engine-bg').hide();
})


$(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();

    $('body, html').animate({
        scrollTop: $($.attr(this, 'href')).offset().top - 0
    }, 500);
});


$(window).scroll(function () {
    if ($(this).scrollTop() >= 400) { // this refers to window
        $('nav').addClass('fixed-nav').removeClass('rel-nav');
    } else {
        $('nav').addClass('rel-nav').removeClass('fixed-nav');
    }
});