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

$('.circle-holder').whenInViewport(function($circ) {
    $circ.addClass('active-circ');
}, {
    threshold: -350 // difference in pixels from user scroll position
});

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
}


var Baidoa, Doolow, Luuq, Mogadishu, Melkadida, Ifo, Guriceel;

function initializeMap() {
    var mapCenter = new google.maps.LatLng(5.646663, 46.311971);

    var mapOptions = {
        zoom: 6,
        center: mapCenter,
        scrollwheel: false,
        disableDefaultUI: true,
        styles: [{
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [{
                "color": "#0070BF"
            }, {
                "lightness": 17
            }]
        }, {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [{
                "color": "#f5f5f5"
            }, {
                "lightness": 20
            }]
        }, {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [{
                "color": "#ffffff"
            }, {
                "lightness": 17
            }]
        }, {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [{
                "color": "#ffffff"
            }, {
                "lightness": 29
            }, {
                "weight": 0.2
            }]
        }, {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [{
                "color": "#ffffff"
            }, {
                "lightness": 18
            }]
        }, {
            "featureType": "road.local",
            "elementType": "geometry",
            "stylers": [{
                "color": "#ffffff"
            }, {
                "lightness": 16
            }]
        }, {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [{
                "color": "#f5f5f5"
            }, {
                "lightness": 21
            }]
        }, {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [{
                "color": "#dedede"
            }, {
                "lightness": 21
            }]
        }, {
            "elementType": "labels.text.stroke",
            "stylers": [{
                "visibility": "on"
            }, {
                "color": "#ffffff"
            }, {
                "lightness": 16
            }]
        }, {
            "elementType": "labels.text.fill",
            "stylers": [{
                "saturation": 36
            }, {
                "color": "#333333"
            }, {
                "lightness": 40
            }]
        }, {
            "elementType": "labels.icon",
            "stylers": [{
                "visibility": "off"
            }]
        }, {
            "featureType": "transit",
            "elementType": "geometry",
            "stylers": [{
                "color": "#f2f2f2"
            }, {
                "lightness": 19
            }]
        }, {
            "featureType": "administrative",
            "elementType": "geometry.fill",
            "stylers": [{
                "color": "#fefefe"
            }, {
                "lightness": 20
            }]
        }, {
            "featureType": "administrative",
            "elementType": "geometry.stroke",
            "stylers": [{
                "color": "#fefefe"
            }, {
                "lightness": 17
            }, {
                "weight": 1.2
            }]
        }]
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


var polylines = []

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
                console.log('Invalid coordintate(s) on row ' + x + 1)
                continue;
            }

            var polygon_path = [previous_coord, current_coord];

            var linePath = new google.maps.Polyline({
                path: polygon_path,
                icons: [{
                    icon: lineSymbol,
                    offset: '100%',
                    strokeColor: '#ff9000',
                    strokeOpacity: 0.6,
                    strokeWeight: 0.9
		}],
                strokeColor: '#ff9000',
                strokeOpacity: 0.6,
                strokeWeight: 0.9,
                geodesic: true
            });

            polylines.push(linePath);
            
    console.log(linePath)


            var line = polylines[polylines.length - 1];

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
}


function removeLines() {
    // Remove existing polylines from the map
    for (var x in polylines) {
        polylines[x].setMap(null);
    }

    polylines = [];
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
            var fatalities = parseInt(data_line[4]);

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
        data: heatmapData
    });

    console.log('Drawing the heatmap.')

    // Draw the new heatmap
    heatmap.setMap(map);

    var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
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
    var interval = 8000;

    function incrementSlider(value) {
        var current_val = parseInt($('#slider').val());
        $('#slider').val(current_val + 1).change();
    }

    for (var x = 0; x <= num_months; x++) {
        timeout_ids.push(window.setTimeout(incrementSlider, interval * (x + 1)));
    }

    console.log(timeout_ids);
}

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

$('#enginetoggle').click(function(){
    $('.engine-if').show()
})

$(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();

    $('body, html').animate({
        scrollTop: $($.attr(this, 'href')).offset().top - 0
    }, 500);
});


$(window).scroll(function () {
    if ($(this).scrollTop() >= 400) { // this refers to window
        $('nav').addClass('fixed-nav');
    } else {
        $('nav').removeClass('fixed-nav');
    }
});