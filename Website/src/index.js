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
import "./intro.js";
import "./stories.js";
import "./tech.js";

Chart.defaults.line.spanGaps = true;
var data;

