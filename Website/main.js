$(function () {
    //Variables 

    var canvas = document.getElementById('myChart');

    // data
    var migrationsstatic = [40749, 91483, 142218, 161303, 180389, 189800, 199211, 201574, 203937, 207430, 210924, 207405, 203887, 231943, null, null, null, null, null];
    var migrations = [null, null, null, null, null, null, null, null, null, null, null, null, null, 231943, 260000, 270000, 280000];
    var chartlabels = ["2010", , "2011", , "2012", , "2013", , "2014", , "2015", , "2016", , "2017", , "2018"];
    var multiplier = 1;
    var multiplier2 = 1;

    var citymap = {
        Bay: {
            center: {
                lat: 2.669240,
                lng: 43.545198
            },
            population: 3248
        },
        Banadir: {
            center: {
                lat: 2.046506,
                lng: 45.317307
            },
            population: 25644
        },
        Mudug: {
            center: {
                lat: 6.583069,
                lng: 48.062141
            },
            population: 35000
        },
        Hiraan: {
            center: {
                lat: 4.266201,
                lng: 45.438034
            },
            population: 44000
        },
        Sool: {
            center: {
                lat: 8.720754,
                lng: 47.415431
            },
            population: 31000
        }
    };

    var data = {
        labels: chartlabels,
        datasets: [
            {
                label: "Historic",
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(153,56,229,1)",
                borderColor: "rgba(153,56,229,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(153,56,229,1)",
                pointBackgroundColor: "rgba(153,56,229,1)",
                borderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(153,56,229,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
                data: migrationsstatic
        },
            {
                label: "Predictive",
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(244,29,37,1)",
                borderColor: "rgba(244,29,37,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(244,29,37,1)",
                pointBackgroundColor: "rgba(244,29,37,1)",
                borderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(244,29,37,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 3,
                pointHitRadius: 10,
                data: migrations
        }
    ]
    };


    var option = {
        showLines: true,
        title: {
            display: true,
            text: 'Displacement Graph: Somalis into Dollo Ado'
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    steps: 40,
                    stepValue: 10000,
                    max: 400000 //max value for the chart is 60
                },
                scaleLabel: {
                    display: true,
                    labelString: 'INDIVIDUALS'
                }
                }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'YEAR'
                }
                }]
        }
    };

    var myLineChart = Chart.Line(canvas, {
        data: data,
        options: option
    });

    var hh = $('#myChart').height();
    $('#map').height(hh);


    // maps


    var overlay;
    USGSOverlay.prototype = new google.maps.OverlayView();

    // Initialize the map and the custom overlay.

    function initialize() {
        var mapOptions = {
            zoom: 6,
            center: {
                lat: 5.147388,
                lng: 46.200305
            },
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            backgroundColor: '#f2f2ed',
            disableDefaultUI: true,
            draggable: true,
            scaleControl: false,
            scrollwheel: false,

            styles: [
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "featureType": "landscape",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "featureType": "road",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "featureType": "administrative",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "featureType": "poi",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "featureType": "administrative",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {
                    "elementType": "labels",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
    ]
  }, {}
]
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        
    for (var city in citymap) {
        // Add the circle for this city to the map.
        var cityCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.6,
            map: map,
            zIndex:-100,
            center: citymap[city].center,
            radius: Math.sqrt(citymap[city].population) * 700
        });
        var myOptions = {
            content:"<h6 style='margin:0'>" + city + "</h6>" + citymap[city].population,
            boxStyle: {
                color: '#fff',
                textAlign: "center",
                fontSize: "8pt",
                width: "50px"
            },
            disableAutoPan: true,
            pixelOffset: new google.maps.Size(-25, -10), // left upper corner of the label
            position: new google.maps.LatLng(citymap[city].center.lat,
                                             citymap[city].center.lng), 
            closeBoxURL: "",
            isHidden: false,
            pane: "floatPane",
            zIndex: 100,
            enableEventPropagation: true
        };
   		var ib = new InfoBox(myOptions);

		ib.open(map);

    }

        var swBound = new google.maps.LatLng(-3.610372, 39.586536);
        var neBound = new google.maps.LatLng(13.081196, 53.005909);
        var bounds = new google.maps.LatLngBounds(swBound, neBound);

        var srcImage = 'img/Somalia_regions_map.svg';

        overlay = new USGSOverlay(bounds, srcImage, map);
    }
    // [END region_initialization]

    // [START region_constructor]
    /** @constructor */
    function USGSOverlay(bounds, image, map) {

        // Initialize all properties.
        this.bounds_ = bounds;
        this.image_ = image;
        this.map_ = map;

        // Define a property to hold the image's div. We'll
        // actually create this div upon receipt of the onAdd()
        // method so we'll leave it null for now.
        this.div_ = null;

        // Explicitly call setMap on this overlay.
        this.setMap(map);
    }
    // [END region_constructor]

    // [START region_attachment]
    /**
     * onAdd is called when the map's panes are ready and the overlay has been
     * added to the map.
     */
    USGSOverlay.prototype.onAdd = function () {

        var div = document.createElement('div');
        div.style.borderStyle = 'none';
        div.style.borderWidth = '0px';
        div.style.position = 'absolute';

        // Create the img element and attach it to the div.
        var img = document.createElement('img');
        img.src = this.image_;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.position = 'absolute';
        div.appendChild(img);

        this.div_ = div;

        // Add the element to the "overlayLayer" pane.
        var panes = this.getPanes();
        panes.overlayLayer.appendChild(div);
    };
    // [END region_attachment]

    // [START region_drawing]
    USGSOverlay.prototype.draw = function () {

        // We use the south-west and north-east
        // coordinates of the overlay to peg it to the correct position and size.
        // To do this, we need to retrieve the projection from the overlay.
        var overlayProjection = this.getProjection();

        // Retrieve the south-west and north-east coordinates of this overlay
        // in LatLngs and convert them to pixel coordinates.
        // We'll use these coordinates to resize the div.
        var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
        var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());

        // Resize the image's div to fit the indicated dimensions.
        var div = this.div_;
        div.style.left = sw.x + 'px';
        div.style.top = ne.y + 'px';
        div.style.width = (ne.x - sw.x) + 'px';
        div.style.height = (sw.y - ne.y) + 'px';
    };
    // [END region_drawing]

    // [START region_removal]
    // The onRemove() method will be called automatically from the API if
    // we ever set the overlay's map property to 'null'.
    USGSOverlay.prototype.onRemove = function () {
        this.div_.parentNode.removeChild(this.div_);
        this.div_ = null;
    };
    // [END region_removal]

    google.maps.event.addDomListener(window, 'load', initialize);



    $("#slider").slider({
        value: 0,
        min: 1,
        max: 1.3,
        step: 0.001,
        slide: function (event, ux) {
            multiplier = ux.value;
            migrations2 = migrations.map(function (el, i) {
                return i >= 14 ? el * multiplier : el
            });
            myLineChart.data.datasets[1].data = migrations2;
            myLineChart.update();
            var num = migrations[14] * multiplier;
            num = num.toFixed(0);
            var rightx = 40 - ((multiplier / 1.3) * 40);
            if (multiplier == 1) {
                rightx = 40
            };


            citymap = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    population: 1800 * (multiplier + 0.5)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    population: 1900 * (multiplier + 0.5)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    population: 35000 * (multiplier + 0.5)
                },
                Hiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    population: 44000 * (multiplier + 0.5)
                },
                Sool: {
                    center: {
                        lat: 8.720754,
                        lng: 47.415431
                    },
                    population: 31000 * (multiplier + 0.5)
                }
            };

            initialize()
        }
    });

    $("#slider2").slider({
        value: 0,
        min: 1,
        max: 1.2,
        step: 0.001,
        slide: function (event, ui) {
            multiplier2 = ui.value;
            migrations2 = migrations.map(function (el, i) {
                return i >= 14 ? el * multiplier2 : el
            });
            myLineChart.data.datasets[1].data = migrations2;
            myLineChart.update();
            var num = migrations[14] * multiplier2;
            num = num.toFixed(0);
            var rightx = 40 - ((multiplier2 / 1.2) * 40);
            if (multiplier2 == 1) {
                rightx = 40
            };



            citymap = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    population: 1800 * (multiplier2 + 0.5)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    population: 1900 * (multiplier2 + 0.5)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    population: 35000 * (multiplier2 + 0.5)
                },
                Hiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    population: 44000 * (multiplier2 + 0.5)
                },
                Sool: {
                    center: {
                        lat: 8.720754,
                        lng: 47.415431
                    },
                    population: 31000 * (multiplier2 + 0.5)
                }
            };;

            initialize()
        }
    });
});

$(window).resize(function () {
    var hh = $('#myChart').height();
    $('#map').height(hh);
})