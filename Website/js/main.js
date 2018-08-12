$(function () {
    //Variables 

    var canvas = document.getElementById('myChart');

    // data
    var migrationsstatic = [40749, 91483, 142218, 161303, 180389, 189800, 199211, 201574, 203937, 207430, 210924, 207405, 203887, 231943, null, null, null, null, null];
    var migrations = [null, null, null, null, null, null, null, null, null, null, null, null, null, 231943, 260000, 270000, 280000];
    var chartlabels = ["2010", , "2011", , "2012", , "2013", , "2014", , "2015", , "2016", , "2017", , "2018"];
    var multiplier = 1;
    var multiplier2 = 1;

    var conflictmapdata = {
        Bay: {
            center: {
                lat: 2.669240,
                lng: 43.545198
            },
            value: 1242
        },
        Banadir: {
            center: {
                lat: 2.046506,
                lng: 45.317307
            },
            value: 4165
        },
        Juba: {
            center: {
                lat: 0.222170,
                lng: 41.587848
            },
            value: 1353
        },
        Shabelle: {
            center: {
                lat: 1.885665,
                lng: 44.250723
            },
            value: 2276
        }
    };



    var foodmapdata = {
        Bay: {
            center: {
                lat: 2.669240,
                lng: 43.545198
            },
            value: 332000
        },
        Mudug: {
            center: {
                lat: 6.583069,
                lng: 48.062141
            },
            value: 286000
        },
        Hiiraan: {
            center: {
                lat: 4.266201,
                lng: 45.438034
            },
            value: 230000
        },
        Shabelle: {
            center: {
                lat: 1.885665,
                lng: 44.250723
            },
            value: 210000
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


    var hh = $('.slide-holder').height();
    $('.map').height(hh);


    // maps


    var overlay;
    USGSOverlay.prototype = new google.maps.OverlayView();

    // Initialize the map and the custom overlay.

    function initialize() {
        var mapOptions = {
            zoom: 6,
            center: {
                lat: 2.046506,
                lng: 45.317307
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

        var conflictmap = new google.maps.Map(document.getElementById('conflictmap'), mapOptions);

        for (var city in conflictmapdata) {
            // Add the circle for this city to the map.
            var cityCircle = new google.maps.Circle({
                strokeColor: '#F16521',
                strokeOpacity: 0.8,
                strokeWeight: 0,
                fillColor: '#F16521',
                fillOpacity: 0.6,
                map: conflictmap,
                zIndex: -100,
                center: conflictmapdata[city].center,
                radius: Math.sqrt(conflictmapdata[city].value) * 3000
            });
            var myOptions = {
                content: "<h4 style='margin:0'>" + conflictmapdata[city].value + "</h4><h6 style='margin:0'>Conflicts in " + city + "</h6>",
                boxStyle: {
                    color: '#fff',
                    textAlign: "center",
                    fontSize: "8pt",
                    width: "50px"
                },
                disableAutoPan: true,
                pixelOffset: new google.maps.Size(-25, -10), // left upper corner of the label
                position: new google.maps.LatLng(conflictmapdata[city].center.lat,
                    conflictmapdata[city].center.lng),
                closeBoxURL: "",
                isHidden: false,
                pane: "floatPane",
                zIndex: 100,
                enableEventPropagation: true
            };
            var ib = new InfoBox(myOptions);

            ib.open(conflictmap);

        }

        var swBound = new google.maps.LatLng(-3.610372, 39.586536);
        var neBound = new google.maps.LatLng(13.081196, 53.005909);
        var bounds = new google.maps.LatLngBounds(swBound, neBound);

        var srcImage = 'img/Somalia_regions_map.svg';

        overlay = new USGSOverlay(bounds, srcImage, conflictmap);
    }


    //  end conflict map initialization

    function initialize2() {
        var mapOptions = {
            zoom: 6,
            center: {
                lat: 4.266201,
                lng: 45.438034
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

        var foodmap = new google.maps.Map(document.getElementById('foodmap'), mapOptions);

        for (var city in foodmapdata) {
            // Add the circle for this city to the map.
            var cityCircle = new google.maps.Circle({
                strokeColor: '#48E5B1',
                strokeOpacity: 0.8,
                strokeWeight: 0,
                fillColor: '#00BFB1',
                fillOpacity: 0.6,
                map: foodmap,
                zIndex: -100,
                center: foodmapdata[city].center,
                radius: Math.sqrt(foodmapdata[city].value) * 400
            });
            var myOptions = {
                content: "<h4 style='margin:0'>" + foodmapdata[city].value + "</h4><h6 style='margin:0'> in crisis in " + city + "</h6>",
                boxStyle: {
                    color: '#fff',
                    textAlign: "center",
                    fontSize: "8pt",
                    width: "50px"
                },
                disableAutoPan: true,
                pixelOffset: new google.maps.Size(-25, -10), // left upper corner of the label
                position: new google.maps.LatLng(foodmapdata[city].center.lat,
                    foodmapdata[city].center.lng),
                closeBoxURL: "",
                isHidden: false,
                pane: "floatPane",
                zIndex: 100,
                enableEventPropagation: true
            };
            var ib = new InfoBox(myOptions);

            ib.open(foodmap);

        }

        var swBound = new google.maps.LatLng(-3.610372, 39.586536);
        var neBound = new google.maps.LatLng(13.081196, 53.005909);
        var bounds = new google.maps.LatLngBounds(swBound, neBound);

        var srcImage = 'img/Somalia_regions_map.svg';

        overlay = new USGSOverlay(bounds, srcImage, foodmap);
    }





    // [END region_initialization]

    // [START region_constructor]
    /** @constructor */
    function USGSOverlay(bounds, image, foodmap) {

        // Initialize all properties.
        this.bounds_ = bounds;
        this.image_ = image;
        this.map_ = foodmap;

        // Define a property to hold the image's div. We'll
        // actually create this div upon receipt of the onAdd()
        // method so we'll leave it null for now.
        this.div_ = null;

        // Explicitly call setMap on this overlay.
        this.setMap(foodmap);
    };


    function USGSOverlay(bounds, image, conflictmap) {

        // Initialize all properties.
        this.bounds_ = bounds;
        this.image_ = image;
        this.map_ = conflictmap;

        // Define a property to hold the image's div. We'll
        // actually create this div upon receipt of the onAdd()
        // method so we'll leave it null for now.
        this.div_ = null;

        // Explicitly call setMap on this overlay.
        this.setMap(conflictmap);
    };
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
    google.maps.event.addDomListener(window, 'load', initialize2);



    $("#banadir-conflict-slide").slider({
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * (multiplier + 0.1)).toFixed(0)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

            initialize();
        }
    });

    $("#banadir-food-slide").slider({
        value: 1.2,
        min: 1,
        max: 1.2,
        step: 0.001,
        slide: function (event, ui) {
            ui.value = (1.2 - ui.value)+1;
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * (multiplier2 + 0.1)).toFixed(0)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * (multiplier2 + 0.1)).toFixed(0)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * (multiplier2 + 0.1)).toFixed(0)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * (multiplier2 + 0.1)).toFixed(0)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * (multiplier2 + 0.1)).toFixed(0)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * (multiplier2 + 0.1)).toFixed(0)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * (multiplier2 + 0.1)).toFixed(0)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * (multiplier2 + 0.1)).toFixed(0)
                }
            };

//            initialize();
//            initialize2();
        }
    });
    

    $("#bay-conflict-slide").slider({
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * (multiplier + 0.1)).toFixed(0)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

            initialize();
        }
    });

    $("#bay-food-slide").slider({
        value: 1.2,
        min: 1,
        max: 1.2,
        step: 0.001,
        slide: function (event, ui) {
            ui.value = (1.2 - ui.value)+1;
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * (multiplier2 + 0.1)).toFixed(0)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

            initialize2();
        }
    });
    
    

    $("#juba-conflict-slide").slider({
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * (multiplier + 0.1)).toFixed(0)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

            initialize();
        }
    });

    $("#juba-food-slide").slider({
        value: 1.2,
        min: 1,
        max: 1.2,
        step: 0.001,
        slide: function (event, ui) {
            ui.value = (1.2 - ui.value)+1;
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

//            initialize();
//            initialize2();
        }
    });
    
    

    $("#shabelle-conflict-slide").slider({
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 *  (multiplier + 0.1)).toFixed(0)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 * 1)
                }
            };

            initialize();
        }
    });

    $("#shabelle-food-slide").slider({
        value: 1.2,
        min: 1,
        max: 1.2,
        step: 0.001,
        slide: function (event, ui) {
            ui.value = (1.2 - ui.value)+1;
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


            conflictmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (1242 * 1)
                },
                Banadir: {
                    center: {
                        lat: 2.046506,
                        lng: 45.317307
                    },
                    value: (4165 * 1)
                },
                Juba: {
                    center: {
                        lat: 0.222170,
                        lng: 41.587848
                    },
                    value: (1353 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (2276 * 1)
                }
            };

            foodmapdata = {
                Bay: {
                    center: {
                        lat: 2.669240,
                        lng: 43.545198
                    },
                    value: (332000 * 1)
                },
                Mudug: {
                    center: {
                        lat: 6.583069,
                        lng: 48.062141
                    },
                    value: (286000 * 1)
                },
                Hiiraan: {
                    center: {
                        lat: 4.266201,
                        lng: 45.438034
                    },
                    value: (230000 * 1)
                },
                Shabelle: {
                    center: {
                        lat: 1.885665,
                        lng: 44.250723
                    },
                    value: (210000 *  (multiplier2 + 0.1)).toFixed(0)
                }
            };

            initialize2();
        }
    });
    
  
    
});

$(window).resize(function () {
    var hh = $('.slide-holder').height();
    $('.map').height(hh);
})