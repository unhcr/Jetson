import axios from 'axios';
import * as Excel from 'exceljs/dist/exceljs.min.js';

export const downloadSpreadsheet = url => {
  return new Promise(function(resolve, reject) {
    axios
      .get(url, {
        responseType: 'arraybuffer'
      })
      .then(function(response) {
        resolve(response);
      })
      .catch(function(error) {
        console.log(error);
        reject(error);
      });
  });
};

export const loadWorkbook = data => {
  return new Promise(function(resolve, reject) {
    var workbook = new Excel.Workbook();
    workbook.xlsx
      .load(data)
      .then(function() {
        resolve(workbook);
      })
      .catch(function(error) {
        console.log(error);
        reject(error);
      });
  });
};

export const downloadAndLoadWorkbook = url => {
  return new Promise(function(resolve, reject) {
    downloadSpreadsheet(url)
      .then(function(response) {
        loadWorkbook(response.data)
          .then(function(workbook) {
            resolve(workbook);
          })
          .catch(function(error) {
            console.log(error);
            reject(error);
          });
      })
      .catch(function(error) {
        console.log(error);
        reject(error);
      });
  });
};

// https://stackoverflow.com/a/30800715/2410292
export const downloadObjectAsJson = (exportObj, exportName) => {
  var dataStr =
    'data:text/json;charset=utf-8,' +
    encodeURIComponent(JSON.stringify(exportObj));
  var downloadAnchorNode = document.createElement('a');
  downloadAnchorNode.setAttribute('href', dataStr);
  downloadAnchorNode.setAttribute('download', exportName + '.json');
  downloadAnchorNode.click();
  downloadAnchorNode.remove();
};
