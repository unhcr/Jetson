dc.config.defaultColors(d3.schemeCategory20c);
//Create the dc.js chart objects and link to div

var displaceTotalNumber = dc.numberDisplay("#dc-displace-total-number");

var displaceReasonChart = dc.rowChart("#dc-displace-reason-chart");
var displaceNeedChart = dc.rowChart("#dc-displace-need-chart");

var prevRegionChart = dc.rowChart("#dc-prev-region-chart");
var currRegionChart = dc.rowChart("#dc-curr-region-chart");

// var prevRegionMap = dc.geoChoroplethChart("#dc-prev-region-map");
// var currRegionMap = dc.geoChoroplethChart("#dc-curr-region-map");

var prevDistrictMap = dc.geoChoroplethChart("#dc-prev-district-map");
var currDistrictMap = dc.geoChoroplethChart("#dc-curr-district-map");

var displaceYearChart = dc.barChart("#dc-year-chart");
var displaceMonthChart = dc.barChart("#dc-month-chart");
var displaceWeekChart = dc.compositeChart("#dc-week-chart");

// return max year remains constant once max value is assigned
var yearFilter = 0; 

// Implement bookmarking chart filters status 
// Serializing filters values in URL
function getFiltersValues() {

  var filters = [
    { name: 'reason', value: displaceReasonChart.filters() },
    { name: 'month', value: resetFilter(displaceMonthChart.filters()) },
    { name: 'need', value: displaceNeedChart.filters() },
    { name: 'pregion', value: prevRegionChart.filters() },
    // { name: 'pregionmap', value: prevRegionMap.filters() },
    { name: 'pdistrictmap', value: prevDistrictMap.filters() },
    { name: 'cregion', value: currRegionChart.filters() },
    // { name: 'cregionmap', value: currRegionMap.filters() },
    { name: 'cdistrictmap', value: currDistrictMap.filters() },
    { name: 'year', value: displaceYearChart.filters()}

  ];

  var recursiveEncoded = $.param(filters);
  location.hash = recursiveEncoded;

}


function initFilters() {
  
  // Get hash values
  var parseHash = /^#reason=([A-Za-z0-9,_\-\/\s]*)&month=([\d{4}-\d{2}-\d{2},\d{4}-\d{2}-\d{2}]*)&need=([A-Za-z0-9,_\-\/\s]*)&pregion=([A-Za-z0-9,_\-\/\s]*)&pdistrictmap=([A-Za-z0-9,_\-\/\s]*)&cregion=([A-Za-z0-9,_\-\/\s]*)&cdistrictmap=([A-Za-z0-9,_\-\/\s]*)&year=([A-Za-z0-9,_\-\/\s]*)$/;

  var parsed = parseHash.exec(decodeURIComponent(location.hash));

  function filter(chart, rank) {  // for instance chart = sector_chart and rank in URL hash = 1

    // sector chart
    if (parsed[rank] == "") {
      
      if (rank == 8) {
        chart.filter(yearFilter);
        getFiltersValues();
      } else {
        chart.filter(null);
        getFiltersValues();
      }

    } else if (rank == 2) {

      var filterValues = parsed[rank].split(",");

      var start = new Date(filterValues[0]);
      var end = new Date(filterValues[1]);

      // initialize date to midnight
      start.setHours(0, 0, 0, 0);
      end.setHours(0, 0, 0, 0);

      var filter = dc.filters.RangedFilter(start, dayOffset(end, 1));
      // var filter = dc.filters.RangedFilter(new Date(2017,2,1), new Date(2017,2,31));              
      chart.filter(filter);
      getFiltersValues();
    } else if (rank == 8) {
      var filterValues = parsed[rank].split(",");

      var filter = filterValues[0] == "" ? yearFilter : Number(filterValues[0]);
      chart.filter(filter);
      getFiltersValues();
    } else {
      
      var filterValues = parsed[rank].split(",");
      for (var i = 0; i < filterValues.length; i++) {
        chart.filter(filterValues[i]);
      }
      getFiltersValues();
    }
  }

  if (parsed) {
    
    filter(displaceReasonChart, 1);
    filter(displaceMonthChart, 2);
    filter(displaceNeedChart, 3);
    filter(prevRegionChart, 4);
    // filter(prevRegionMap, 5);
    filter(prevDistrictMap, 5);
    filter(currRegionChart, 6);
    // filter(currRegionMap, 8);
    filter(currDistrictMap, 7);
    filter(displaceYearChart, 8);
  } else {
    
    // assign default year
    displaceYearChart.filter(yearFilter);
    getFiltersValues();

  }
}

var numberFormat = d3.format(",.0f");

var dateFormat = d3.timeFormat("%d %b %Y");
var yearFormat = d3.timeFormat("%Y");

var monthNameFormat = d3.timeFormat("%b %Y");

var dateLongFormat = d3.timeFormat("%Y-%m-%d");

var monthBarTip = d3.tip()
  .attr('class', 'd3-month-tip')
  .offset([-5, 0])
  .html(function (d) {
    // var months = d.data.key.split('-');
    // var date = new Date(months[0], months[1]-1, 1);
    var date = d.data.key;
    return "<div class='dc-tooltip'><span class='dc-tooltip-title'>" + monthNameFormat(date) + "</span> | <span class='dc-tooltip-value'>" + numberFormat(rndFig(d.y)) + "</span></div>";
  });

var yearBarTip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-5, 0])
  .html(function (d) { 
    return "<div class='dc-tooltip'><span class='dc-tooltip-title'>" + (d.data.key) + "</span> | <span class='dc-tooltip-value'>" + numberFormat(rndFig(d.data.value)) + "</span></div>"; 
  });

var barTip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-5, 0])
  .html(function (d) { 
    return "<div class='dc-tooltip'><span class='dc-tooltip-title'>" + (d.key) + "</span> | <span class='dc-tooltip-value'>" + numberFormat(rndFig(d.value)) + "</span></div>"; 
  });

var lineTip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-5, 0])
  .html(function (d) { 
    return "<div class='dc-tooltip'><span class='dc-tooltip-title'>" + (d.layer) + " Week "  + d.data.key +"</span> | <span class='dc-tooltip-value'>" + numberFormat(rndFig(d.data.value)) +"</span></div>"; 
  });

var mapTip = d3.tip()
  .attr('class', 'd3-map-tip')
  .offset([-5, 0])
  .html(function (d) {
    var t = d3.select(this).select('title').html();
    var tA = t.split(':');
    return "<div class='dc-tooltip'><span class='dc-tooltip-title'>" + (tA[0]) + "</span> | <span class='dc-tooltip-value'>" + (tA[1]) + "</span></div>";
  });

// Correct end date due to month rounding off 
// by adding or deducting a day
var dayOffset = d3.timeDay.offset;

var monthOffset = d3.timeMonth.offset;

var rangeDate = function(y) {
  var range = [new Date(y, 0, 1), new Date(y + 1, 0, 31)];
  return range;
}

var resetFilter = function (filterValues) {
  if (filterValues.length == 0) return filterValues;
  var start = filterValues[0][0];
  var end = dayOffset(filterValues[0][1], -1);
  var filter = dc.filters.RangedFilter(dateLongFormat(start), dateLongFormat(end));
  return filter;
}

// spinner options
var opts = {
  lines: 10, // The number of lines to draw
  length: 10, // The length of each line
  width: 3, // The line thickness
  radius: 10, // The radius of the inner circle
  scale: 2, // Scales overall size of the spinner
  corners: 0.5, // Corner roundness (0..1)
  color: '#ff0000', // CSS color or array of colors
  fadeColor: 'transparent', // CSS color or array of colors
  speed: 1.9, // Rounds per second
  rotate: 0, // The rotation offset
  animation: 'spinner-line-fade-quick', // The CSS animation name for the lines
  direction: 1, // 1: clockwise, -1: counterclockwise
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  className: 'spinner', // The CSS class to assign to the spinner
  top: '50%', // Top position relative to parent
  left: '50%', // Left position relative to parent
  shadow: '0 0 1px transparent', // Box-shadow for the lines
  position: 'absolute' // Element positioning
};

// loader settings
var target = document.getElementById('dc-curr-region-chart');

// trigger loader
var spinner = new Spinner(opts).spin(target);

// Load data from CSV file
d3.csv("data/PRMNDataset.csv", function (data) {
  // Load data from JSON file
  d3.json("data/Som_Admbnda_Adm1_UNDP.json", function (regionJson) {
    d3.json("data/Som_Admbnda_Adm2_UNDP.json", function (districtJson) {

      // stop the loader
      spinner.stop();

      // format our data
      data.forEach(function (d) {
        d.id = +d.id;
        d.tpeople = +d.tpeople;
        d.yr = +d.yr;
        if (yearFilter < d.yr) yearFilter = d.yr; 
        // d.yrmonthnum = +d.yrmonthnum;
      });

      // run the data thru crossfilter
      var facts = crossfilter(data);

      // create people dimension and group
      var peopleGroup = facts.groupAll().reduceSum(function (d) {
        return d.tpeople;
      });

      displaceTotalNumber
        .group(peopleGroup)
        .formatNumber(numberFormat)
        .transitionDuration(500)
        .valueAccessor(function (d) { return rndFig(d); });

      // configure displacement year dimension and group
      var displaceYear = facts.dimension(function (d) {
        return d.yr;
      });
      var displaceYearGroup = displaceYear.group()
        .reduceSum(function (d) {
          return d.tpeople;
        });

      // Configure displacement year bar chart parameters
      displaceYearChart.height(170)
        .width($('#dc-year-chart').width())
        .margins({ top: 5, right: 10, bottom: 60, left: 80 })
        .dimension(displaceYear)
        .group(displaceYearGroup, "Year")
        .gap(1)
        .ordinalColors(['#338EC9'])
        .renderHorizontalGridLines(true)
        .controlsUseVisibility(true)
        .x(d3.scaleBand())
        .xUnits(dc.units.ordinal)
        .brushOn(false)
        .elasticY(true)
        .on("filtered", getFiltersValues)
        .on("filtered", function(){
          var filter = displaceYearChart.filters()[0];
          // get filtered year 
          filter = filter == undefined ? yearFilter : Number(filter);
          
          // reset min and max date based on filtered year
          displaceMonthChart.x(d3.scaleTime().domain(rangeDate(filter)));
        })
        .title(function (d) {
          // return d3.format(",")(d.value);
          return '';
        })        
        .yAxis().ticks(5);    

      displaceYearChart.filterPrinter(function(filters){
        return "[" + filters[0] + "]";
      });

      // single select
      displaceYearChart.addFilterHandler(function(filters, filter) {return [filter];}); // this
      // custom filter handler (no-op)
      displaceYearChart.removeFilterHandler(function(filters, filter) {
        return filters;
        // return [filter]
      });

      // Rotate x-axis labels
      displaceYearChart.on('renderlet', function (chart) {
        // move x axis slightly to the right
        chart.selectAll("g.axis.x")
          .attr('transform', "translate(58,110)");        
        chart.selectAll('g.x text')
          .attr('transform', 'translate(10,10) rotate(270)')
          .style('text-anchor', 'end')
          .transition()
          .duration(500)
          .style('opacity', 1);

        chart.selectAll('rect')
          .attr('data-tooltip', 'hello');
        
        chart.selectAll(".bar").call(yearBarTip);
        chart.selectAll(".bar").on('mouseover', yearBarTip.show)
          .on('mouseout', yearBarTip.hide);

      });


      // configure displacement month dimension and group
      var displaceMonth = facts.dimension(function (d) {
        var months = d.monthend.split('\/');
        var date = new Date(months[2], months[1] - 1, months[0]);
        return d3.timeMonth(date);
        // return date;
      });
      var displaceMonthGroup = displaceMonth.group()
        .reduceSum(function (d) {
          return d.tpeople;
        });

      // Configure displacement month bar chart parameters

      // Get minimum and maximum date
      // var minDate = new Date(2016, 0, 1);
      // var maxDate =  new Date(2019 + 1, 2, 31);

      // var keys = removeEmptyBins(displaceMonthGroup).all().map(dc.pluck('key')).slice();
      // var minDate = keys[0]; 
      // var maxDate =  dayOffset(monthOffset(keys[keys.length -1],1));
      // console.log(minDate, maxDate)
      // function removeEmptyBins(source_group) {
      //     return {
      //       all: () => {
      //           return source_group.all().filter(function(d) {
      //               // here your condition
      //               return d.key !== null && d.key !== '' && d.value !== 0; // etc. 
      //           });
      //       }
      //   };
      // }

      displaceMonthChart.height(170)
        .width($('#dc-month-chart').width() * 0.95)
        .margins({ top: 5, right: -15, bottom: 60, left: 50 })
        .dimension(displaceMonth)
        .group(displaceMonthGroup, "Year-Month")
        .valueAccessor(function (d) {
          return d.value;
        })
        .gap(1)
        // .barPadding(0.1)
        // .outerPadding(0.05)
        // .centerBar(true)
        .ordinalColors(['#338EC9'])
        .renderHorizontalGridLines(true)
        .controlsUseVisibility(true)
        .round(d3.timeMonth.round) 
        .x(d3.scaleTime().domain(rangeDate(yearFilter)))
        // .x(d3.scaleTime().domain([minDate, maxDate]))
        .xUnits(d3.timeMonths)
        .round(d3.timeMonth)
        .brushOn(true)
        // .elasticX(true)
        .elasticY(true)
        .on("filtered", getFiltersValues)
        .title(function (d) {
          // return d3.format(",")(d.value);
          return '';
        })
        .yAxis().ticks(5);       

      displaceMonthChart.filterPrinter(function(filters){
        // var s = "Period: ";  
        var s = "[";  
        var start = filters[0][0];
        var end = dayOffset(filters[0][1],-1);    // correct month rounding off 
        s += dateFormat(start) + ' - ' + dateFormat(end) + "]";
        return s;        
      });

      displaceMonthChart.xAxis()
        .tickFormat(function (d) {
          return monthNameFormat(d);
        })
        .ticks(12);
        // .ticks(keys.length);

      // Rotate x-axis labels
      displaceMonthChart.on('renderlet', function (chart) {
        // move x axis slightly to the right
        chart.selectAll("g.axis.x")
          .attr('transform', "translate(62,110)");               
        
        chart.selectAll('g.x text')
          .attr('transform', 'translate(-10, 10) rotate(270)')
          .style('text-anchor', 'end')
          .transition()
          .duration(500)
          .style('opacity', 1);

        chart.selectAll(".bar").call(monthBarTip);
        chart.selectAll(".bar").on('mouseover', monthBarTip.show)
          .on('mouseout', monthBarTip.hide);

      });


      // Configure weekly displacements parameters
      var displaceWeek = facts.dimension(function (d) {
        return +d.weeknum;
      });

      var displaceWeekGroup1 = displaceWeek.group()
        .reduceSum(function (d) {
          return +d.yr2016;
        });
      var displaceWeekGroup2 = displaceWeek.group()
        .reduceSum(function (d) {
          return +d.yr2017;
        });
      var displaceWeekGroup3 = displaceWeek.group()
        .reduceSum(function (d) {
          return +d.yr2018;
        });
      var displaceWeekGroup4 = displaceWeek.group()
        .reduceSum(function (d) {
          return +d.yr2019;
        });
      var displaceWeekGroup5 = displaceWeek.group()
        .reduceSum(function (d) {
          return +d.yr2020;
        });

      // displaceWeekChart helper function
      // function lineChartKey(d){
      //   // split yrweeknum into two
      //   var arr = d.key.split("-");
      //   return parseInt(arr[1]);
      // }

      displaceWeekChart
        .height(180)
        .width($('#dc-week-chart').width())     
        .margins({ top: 15, right: 70, bottom: 35, left: 50 }) 
        .title(function (d) {
          // return "Week " + d.key + ": "
          //          + d3.format(",")(d.value);
          return '';
        })
        .compose([
          dc.lineChart(displaceWeekChart)
            .dimension(displaceWeek)
            // .keyAccessor(function(d){
            //   return +d.key.substr(4,6);
            // })
            .colors('#bdbdbd') // gray
            .dashStyle([3,2])
            .group(displaceWeekGroup1, "2016")
            .useRightYAxis(true),
          dc.lineChart(displaceWeekChart)
            .dimension(displaceWeek)
            // .keyAccessor(function(d){
            //   return +d.key.substr(4,6);
            // })
            .colors('#ffc04c')  // orange 
            .dashStyle([3,2])
            .group(displaceWeekGroup2, "2017")
            .useRightYAxis(true),
          dc.lineChart(displaceWeekChart)
            .dimension(displaceWeek)
            // .keyAccessor(function(d){
            //   return +d.key.substr(4,6);
            // })
            .colors('#addd8e') // green 
            .dashStyle([3,2])
            .group(displaceWeekGroup3, "2018")
            .useRightYAxis(true),
          dc.lineChart(displaceWeekChart)
            .dimension(displaceWeek)
            // .keyAccessor(function(d){
            //   return +d.key.substr(4,6);
            // })
            .colors('#5ba4d3') // blue
            .dashStyle([3,2])
            .group(displaceWeekGroup4, "2019")
            .useRightYAxis(true),
          dc.lineChart(displaceWeekChart)
            .dimension(displaceWeek)
            // .keyAccessor(function(d){
            //   return +d.key.substr(4,6);
            // })
            .colors('#e7646a') // red e7646a 
            .group(displaceWeekGroup5, "2020")
            // .useRightAxisGridLines(true)
          
        ]) 
        .legend(dc.legend().horizontal(true).x(0).y(0).gap(0))
        // .legend(dc.legend().x(370).y(5).itemHeight(13).gap(5))
        // .shareTitle(false)
        .brushOn(false) 
        // .mouseZoomable(true)
        .renderHorizontalGridLines(true)
        .x(d3.scaleLinear().domain([0,53]))
        .elasticY(true) 
        .elasticX(false) 
        .yAxisLabel("2020")
        .rightYAxisLabel("2016...2019")
        .yAxis().ticks(4);

      displaceWeekChart
        .useRightAxisGridLines(true)
        .rightYAxis().ticks(4);

      displaceWeekChart
        .xAxis().ticks(26);

      displaceWeekChart.on('renderlet', function (chart) {
        chart.selectAll(".dot").call(lineTip);
        chart.selectAll(".dot").on('mouseover.tip', lineTip.show)
          .on('mouseout.tip', lineTip.hide);
      });
  

        // create displacement reason dimension and group
      var displaceReason = facts.dimension(function (d) {
        return d.creason;
      });
      var displaceReasonGroup = displaceReason.group().reduceSum(
        function (d) {
          return d.tpeople;
        }
      );

      // configure displacement reason chart parameters
      displaceReasonChart
        .width($('#dc-displace-reason-chart').width())
        .height(150)
        .margins({ top: 0, right: 10, bottom: 20, left: 10 })
        .dimension(displaceReason)
        .group(displaceReasonGroup)
        .valueAccessor(function (d) {
          return (d.value);
        })
        .ordering(function (d) { return -d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(d3.scale.category20())
        // .colors('#4292c6')
        // .ordinalColors(['#F5C300','#66D1C1','#72879D','#338EC9'])
        .ordinalColors(['#f7941d', '#e7646a', '#a07b5e', '#c974a2'])
        .label(function (d) {
          return _.upperFirst(d.key);
        })
        .title(function (d) {
          // return _.upperFirst(d.key) + ": "
          //          + d3.format(",")(d.value);
          return '';
        })
        .elasticX(true)
        .xAxis().ticks(4);

      displaceReasonChart.on('renderlet', function (chart) {
        chart.selectAll(".row").call(barTip);
        chart.selectAll(".row").on('mouseover', barTip.show)
          .on('mouseout', barTip.hide);
      });

      

      // create displacement need dimension and group
      var displaceNeed = facts.dimension(function (d) {
        return d.cneed;
      });

      var displaceNeedGroup = displaceNeed.group().reduceSum(function (d) {
        return d.tpeople;
      });
      // var displaceNeedGroup = displaceNeed.group().reduceCount();

      var arr = [];

      // configure current region chart parameters
      displaceNeedChart
        .width($('#dc-displace-need-chart').width())
        // .height($('.text-section').height()-50)
        .height(230)
        .margins({ top: 0, right: 10, bottom: 30, left: 10 })
        .dimension(displaceNeed)
        .group(displaceNeedGroup)
        .ordering(function (d) { return -d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(d3.scale.ordinal().range(colorbrewer.Set2[6]))
        .colors('#338EC9')
        .label(function (d) {
          var percent;
          var totalPeopleSelect = peopleGroup.value();
          var needValue = d.value;
          var filters = displaceNeedChart.filters();          

          function getPercent() {
            return (needValue / totalPeopleSelect * 100).toFixed(0)
          }

          if (filters.length !== 0) {
            filters.find(function(el){
              if (el === d.key) {
                percent = getPercent()
              };
            });
          } else {
            percent = getPercent()
          }

          if (isNaN(percent)) percent = 0;
          // percent = (d.value / peopleGroup.value() * 100).toFixed(0)
          return d.key + ' | ' + d3.format(".0f")(percent) + '%';

        })
        .title(function (d) {
          // var percent = (d.value / peopleGroup.value() * 100).toFixed(0);
          // return d.key + ": " + d3.format(",")(percent) + '%';
           return '';
        })
        .elasticX(true)
        .xAxis().ticks(3);

      // displaceNeedChart.on('renderlet', function (chart) {
      //   chart.selectAll(".row").call(percentBarTip);
      //   chart.selectAll(".row").on('mouseover', percentBarTip.show)
      //     .on('mouseout', percentBarTip.hide);
      // });
      
      

      // create previous region dimension and group
      var prevRegion = facts.dimension(function (d) {
        return d.pregion;
      });

      var prevRegionGroup = prevRegion.group().reduceSum(function (d) {
        return d.tpeople;
      });

      // configure previous region chart parameters
      prevRegionChart
        .width($('#dc-prev-region-chart').width())
        // .height($('.text-section').height()-50)
        .height(400)
        .margins({ top: 0, right: 10, bottom: 20, left: 10 })
        .dimension(prevRegion)
        .valueAccessor(function (d) { return d.value; })
        .group(prevRegionGroup)
        .ordering(function (d) { return -d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(d3.scale.ordinal().range(colorbrewer.Set2[6]))
        .ordinalColors(['#F26E80'])
        .label(function (d) {
          return d.key;
        })
        .title(function (d) {
          // return d.key + ": " + d3.format(",")(d.value);
          return '';
        })
        // .x(d3.scale.linear().domain([0, 300000]))
        .elasticX(true)
        .xAxis().ticks(3)

      prevRegionChart.on('renderlet', function (chart) {
        chart.selectAll(".row").call(barTip);
        chart.selectAll(".row").on('mouseover', barTip.show)
          .on('mouseout', barTip.hide);
      });



      // create current region dimension and group
      var currRegion = facts.dimension(function (d) {
        return d.cregion;
      });

      var currRegionGroup = currRegion.group().reduceSum(function (d) {
        return d.tpeople;
      });

      // configure current region chart parameters
      currRegionChart
        .width($('#dc-curr-region-chart').width())
        // .height($('.text-section').height()-50)
        .height(400)
        .margins({ top: 0, right: 10, bottom: 20, left: 10 })
        .dimension(currRegion)
        .valueAccessor(function (d) { return d.value; })
        .group(currRegionGroup)
        .ordering(function (d) { return -d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(d3.scale.ordinal().range(colorbrewer.Set2[6]))
        .colors('#338EC9')
        .label(function (d) {
          return d.key;
        })
        .title(function (d) {
          // return d.key + ": " + d3.format(",")(d.value);
          return '';
        })
        .elasticX(true)
        .xAxis().ticks(3);

      currRegionChart.on('renderlet', function (chart) {
        chart.selectAll(".row").call(barTip);
        chart.selectAll(".row").on('mouseover', barTip.show)
          .on('mouseout', barTip.hide);
      });


      // create map dimension and group
      // var prevRegion = facts.dimension(function (d) {
      //   return d.pregion;
      // });
      // var prevRegionGroup = prevRegion.group().reduceSum(function (d) {
      //   return d.tpeople;
      // });

      // Convert zipped shapefiles to GeoJSON with mapshaper (mapshaper.org).
      // Use d3.geoMercator projections and play around with the scale and 
      // translate method parameters to get the right fit for the map. 
      // The maximum value for colorDomain can be automatically calculated 
      // from the dataset.
      // colorAccessor returns a grey color for 0 or undefined data values. 
      // Remember to set the 'stroke' color for the admin1 borders to stand-out,
      // to increase thickness set 'stroke-width' to 2px or more. See 'style.css'.
      // prevRegionMap
      //   .width($('#leftPanel').width())
      //   .height(380)
      //   .transitionDuration(1000)
      //   .dimension(prevRegion)
      //   .group(prevRegionGroup)
      //   .projection(d3.geoMercator()
      //     .scale(1490)
      //     .translate([-1030, 320])
      //   )
      //   .keyAccessor(function (d) { return d.key; })
      //   .valueAccessor(function (d) { return d.value; })
      //   .on("filtered", getFiltersValues)
      //   .controlsUseVisibility(true)
      //   // .colors(['#ccc'].concat(colorbrewer.Blues[9])) 
      //   // .colors(d3.scaleQuantize().range(['#F592A0','#F26E80','#EF4A60','#B33848']))

      //   .colors(d3.scaleQuantize().range(['#F9B7BF', '#F592A0', '#F26E80', '#EF4A60', '#B33848']))
      //   .colorDomain([0, prevRegionGroup.top(1)[0].value / 2])

      //   .colorCalculator(function (d) { return d ? prevRegionMap.colors()(d) : '#ccc'; })
      //   .overlayGeoJson(regionJson.features, "admin1Name", function (d) {
      //     return d.properties.admin1Name;
      //   })
      //   .title(function (d) {
      //     return d.key + ": " + d3.format(",")(rndFig(d.value));
      //     // return '';
      //   });

      // prevRegionMap.on('renderlet', function (chart) {
      //   chart.selectAll(".admin1Name").call(mapTip);
      //   chart.selectAll(".admin1Name").on('mouseover', mapTip.show)
      //     .on('mouseout', mapTip.hide);
      // });

      // create map dimension and group
      var prevDistrict = facts.dimension(function (d) {
        return d.pdistrict;
      });

      var prevDistrictGroup = prevDistrict.group().reduceSum(function (d) {
        return d.tpeople;
      });

      var prevDistrictScale = d3.scaleCluster()
          .domain(d3.range(10).map(function(i){
            return prevDistrictGroup.top(1)[0].value * i/10;
          }))
          .range(['#f7ebec', '#efd7da', '#e8c3c8', '#e0afb5', '#d99ba3', '#d18791', '#c9737e', '#c25f6c', '#ba4b5a', '#b33848']);
      
      prevDistrictMap
        .width($('#dc-prev-district-map').width())
        .height(380)
        .transitionDuration(1000)
        .dimension(prevDistrict)
        .group(prevDistrictGroup)
        .projection(d3.geoMercator()
          .scale(1490)
          .translate([-1065, 320])

        )
        .keyAccessor(function (d) { return d.key; })
        .valueAccessor(function (d) { return d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(['#ccc'].concat(colorbrewer.Blues[9])) 
        // .colors(d3.scaleQuantize().range(['#F9B7BF', '#F592A0', '#F26E80', '#EF4A60', '#B33848']))
        .colors(prevDistrictScale.range())
        // .colorDomain([0, prevDistrictGroup.top(1)[0].value / 2])
        .colorDomain(prevDistrictScale.domain())
        .colorCalculator(function (d) { return d ? prevDistrictMap.colors()(d) : '#ccc'; })
        .overlayGeoJson(districtJson.features, "admin2Name", function (d) {
          return d.properties.admin2Name;

        })
        .title(function (d) {
          return d.key + ": " + d3.format(",")(rndFig(d.value));
          // return '';

        });

      prevDistrictMap.on('renderlet', function (chart) {
        chart.selectAll(".admin2Name").call(mapTip);
        chart.selectAll(".admin2Name").on('mouseover', mapTip.show)
          .on('mouseout', mapTip.hide);
      });

      prevDistrictMap.on("preRender", function(chart){
          chart.colorDomain(d3.extent(chart.group().all(), chart.valueAccessor()));
      });
      prevDistrictMap.on("preRedraw", function(chart){
          chart.colorDomain(d3.extent(chart.group().all(), chart.valueAccessor()));
      });

      // create map dimension and group
      // var currRegion = facts.dimension(function (d) {
      //   return d.cregion;
      // });
      // var currRegionGroup = currRegion.group().reduceSum(function (d) {
      //   return d.tpeople;
      // });

      // currRegionMap
      //   .width($('#leftPanel').width())

      //   .height(400)
      //   .transitionDuration(1000)
      //   .dimension(currRegion)
      //   .group(currRegionGroup)
      //   .projection(d3.geoMercator()
      //     .scale(1490)
      //     .translate([-1030, 320])
      //   )
      //   .keyAccessor(function (d) { return d.key; })
      //   .valueAccessor(function (d) { return d.value; })
      //   .on("filtered", getFiltersValues)
      //   .controlsUseVisibility(true)
      //   // .colors(['#ccc'].concat(colorbrewer.Blues[9])) 
      //   // .colors(["#CCC", '#E2F2FF','#C4E4FF','#9ED2FF','#81C5FF','#6BBAFF','#51AEFF','#36A2FF','#1E96FF','#0089FF','#0061B5'])
      //   .colors(d3.scaleQuantize().range(['#99C7E4', '#66AAD7', '#338EC9', '#0072BC', '#00568D']))
      //   .colorDomain([0, currRegionGroup.top(1)[0].value / 2])
      //   .colorCalculator(function (d) { return d ? currRegionMap.colors()(d) : '#ccc'; })
      //   .overlayGeoJson(regionJson.features, "admin1Name", function (d) {
      //     return d.properties.admin1Name;
      //   })
      //   .title(function (d) {
      //     return d.key + ": " + d3.format(",")(rndFig(d.value));
      //     // return '';
      //   });

      // currRegionMap.on('renderlet', function (chart) {
      //   chart.selectAll(".admin1Name").call(mapTip);
      //   chart.selectAll(".admin1Name").on('mouseover', mapTip.show)
      //     .on('mouseout', mapTip.hide);
      // });



      // create map dimension and group 
      var currDistrict = facts.dimension(function (d) {
        return d.cdistrict;
      });

      var currDistrictGroup = currDistrict.group().reduceSum(function (d) {
        return d.tpeople;
      });
      
      var currDistrictScale = d3.scaleCluster()
      .domain(d3.range(10).map(function(i){
        return currDistrictGroup.top(1)[0].value * i/10;
      }))
      .range(['#e5eef3', '#ccdde8', '#b2ccdc', '#99bbd1', '#7faac6', '#6699ba', '#4c88af', '#3277a3', '#196698', '#00568d']);

      currDistrictMap
        .width($('#dc-curr-district-map').width())
        .height(370)
        .transitionDuration(1000)
        .dimension(currDistrict)
        .group(currDistrictGroup)
        .projection(d3.geoMercator()
          .scale(1490)
          .translate([-1065, 320])

        )
        .keyAccessor(function (d) { return d.key; })
        .valueAccessor(function (d) { return d.value; })
        .on("filtered", getFiltersValues)
        .controlsUseVisibility(true)
        // .colors(['#ccc'].concat(colorbrewer.Blues[9])) 
        // .colors(d3.scaleQuantize().range(['#99C7E4', '#66AAD7', '#338EC9', '#0072BC', '#00568D']))
        .colors(currDistrictScale.range())
        // .colorDomain([0, currDistrictGroup.top(1)[0].value / 2])
        .colorDomain(currDistrictScale.domain())
        .colorCalculator(function (d) { return d ? currDistrictMap.colors()(d) : '#ccc'; })
        .overlayGeoJson(districtJson.features, "admin2Name", function (d) {
          return d.properties.admin2Name;

        })
        .title(function (d) {
          return d.key + ": " + d3.format(",")(rndFig(d.value));
          // return '';

        });

      currDistrictMap.on('renderlet', function (chart) {
        chart.selectAll(".admin2Name").call(mapTip);
        chart.selectAll(".admin2Name").on('mouseover', mapTip.show)
          .on('mouseout', mapTip.hide);
      });

      currDistrictMap.on("preRender", function(chart){
          chart.colorDomain(d3.extent(chart.group().all(), chart.valueAccessor()));
      });
      currDistrictMap.on("preRedraw", function(chart){
          chart.colorDomain(d3.extent(chart.group().all(), chart.valueAccessor()));
      });


      
      // Render the charts
      dc.renderAll();
      
      initFilters();

      dc.redrawAll();

      // setResizingSvg();


    });
  });
});

// function setResizingSvg() {
//   // set resizing viewbox

//   // 
// }

// Utilities
// var uri = "https://unhcr.github.io/dataviz-somalia-prmn/index.html#reason=&month=&pregion=&pregionmap=&cregion=&cregionmap=&@UNHCRSom";

// rounds figures
function rndFig(num) {
  // Excel function:
  //=IF(C9<100,C9,IF(AND(C9>=100,C9<1000),ROUND(C9,-1),IF(AND(C9>=1000,C9<10000),ROUND(C9,-2),IF(C9>=10000,ROUND(C9,-3),0))))
  //  var num = 767; 
  if (num == null) { // null == undefined
    res = 0;

  }
  else if (num <= 4) {
    res = num;

  }
  else if (num > 4 && num < 100) {
    res = Math.round(num / 10) * 10;

  }
  else if (num >= 100 && num < 1000) {
    res = Math.round(num / 100) * 100;

  }
  else if (num >= 1000) {
    res = Math.round(num / 1000) * 1000;

  }
  // else if (num>=10000) {
  //   res = Math.round(num/10000)*10000;
  // }

  return res;
}

// help popups
$('.question')
  .popup({
    on: 'hover'
  })
;

$('.ui.primary.button')
  .popup({
    on: 'hover'
  })
;