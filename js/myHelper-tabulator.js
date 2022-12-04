function defineTable_DeDistricts() {
  var table = new Tabulator("#div_table-de-districts", {
    height: 600, // set height of table to enable virtual DOM
    layout: "fitColumns", //fit columns to width of table (optional)
    // autoColumns: true, // very nice!!!
    tooltipsHeader: true,
    selectable: true,
    columns: [ //Define Table Columns
      { title: "Landkreis<br/>&nbsp;<br/>&nbsp;", field: "Landkreis", sorter: "string", headerFilter: true },
      {
        title: "Bundesland<br/>&nbsp;<br/>&nbsp;", field: "Bundesland", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true
        // , headerFilterPlaceholder:"select"
      },
      // {
      // 	title: "ID", field: "LK_ID", sorter: "string", width: 30, sorterParams: {
      // 		alignEmptyValues: "bottom"
      // 	}, headerFilter: true
      // },
      // {
      //   title: "Einwohner<br/>&nbsp;<br/>&nbsp;", field: "Population", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      // { title: "Date", field: "Date", sorter: "date", sorterParams: { format: "YYYY-MM-DD" }, hozAlign: "center", headerFilter: true },
      {
        title: "Inzidenz<br/>&nbsp;<br/>&nbsp;", field: "Cases_Last_Week_Per_100000", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Inzidenz<br/>Veränderung<br/>7 Tage in %", field: "Cases_Last_Week_7Day_Percent", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Intensivstationen<br/>% COVID-19<br/>&nbsp;", field: "DIVI_Intensivstationen_Covid_Prozent", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // {
      //   title: "Infizierte<br/>&nbsp;<br/>&nbsp;", field: "Cases", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      // {
      //   title: "Tote<br/>&nbsp;<br/>&nbsp;", field: "Deaths", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      {
        title: "Tote<br/>pro Mill.EW.<br/>letzte Woche", field: "Deaths_Last_Week_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Infizierte<br/>pro Mill.EW.<br/>gesamt", field: "Cases_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Tote<br/>pro Mill.EW.<br/>gesamt", field: "Deaths_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // {
      //   title: "Infizierte<br/>Trend<br/>Index", field: "Slope_Cases_New_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      // {
      //   title: "Intensivstationen<br/>% belegt<br/>&nbsp;", field: "DIVI_Intensivstationen_Betten_belegt_Prozent", sorter: "number", hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
    ],
    rowClick: function (e, row) {
      var rowData = row.getData();
      // console.log(rowData)
      var clickedCode = rowData["LK_ID"];
      var clickedDistrict = rowData["Landkreis"];
      if (row._row.modules.select.selected == true) {
        tabulator_row_clicked('DeDistrict', 'selected', clickedCode);
        alert(clickedDistrict + " zum Chart unten hinzugefügt")
      } else {
        if (list_of_codes_to_plot_DeDistricts.length > 1) {
          tabulator_row_clicked('DeDistrict', 'unselected', clickedCode);
          // alert(clickedDistrict + " von Auswahl entfernt");
        }
      }
    },
  });

  table.setSort([
    { column: "Landkreis", dir: "asc" },
    { column: "Bundesland", dir: "asc" },
    { column: "Cases_Last_Week_Per_100000", dir: "desc" }, //sort by this first
  ]);

  return table;
}




function defineTable_Countries() {
  table = new Tabulator("#div_table-countries-latest-all", {
    height: 600, // set height of table to enable virtual DOM
    layout: "fitColumns", //fit columns to width of table (optional)
    // autoColumns: true, // very nice!!!
    tooltipsHeader: true,
    selectable: true,
    columns: [ //Define Table Columns
      { title: "Country<br/>&nbsp;", field: "Country", sorter: "string", width: 100, headerFilter: true },
      {
        title: "Continent<br/>&nbsp;", field: "Continent", width: 75, editor: "select", sorter: "string", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterParams: {
          "": "any",
          "Africa": "Africa",
          "Asia": "Asia",
          "Europe": "Europe",
          "North America": "North America",
          "South America": "South America",
          "Oceania": "Oceania"
          // "Antarctica": "Antarctica",
        }
        // , headerFilterPlaceholder:"select"
      },
      // {
      //   title: "Code<br/>&nbsp;", field: "Code", sorter: "string", width: 30, sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true
      // },
      {
        title: "Deaths Last Week<br/>per Million", field: "Deaths_Last_Week_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Incidence<br/>7-days", field: "Cases_Last_Week_Per_100000", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Incidence-Change<br/>7-days", field: "Cases_Last_Week_7Day_Percent", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases Doubling Time<br/>Days", field: "DoublingTime_Cases_Last_Week_Per_100000", sorter: "number", width: 200, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // { title: "Date", field: "Date", sorter: "date", sorterParams: { format: "YYYY-MM-DD" }, hozAlign: "center", headerFilter: true },
      // {
      //   title: "Cases<br/>&nbsp;", field: "Cases", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      // {
      //   title: "Deaths<br/>&nbsp;", field: "Deaths", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      {
        title: "Total Cases<br/>per Million", field: "Cases_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Total Deaths<br/>per Million", field: "Deaths_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // {
      // 	title: "Deaths<br/>Doubling Time (Days)", field: "Deaths_Doubling_Time", sorter: "number", hozAlign: "right", sorterParams: {
      // 		alignEmptyValues: "bottom"
      // 	}, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
      {
        title: "Population<br/>&nbsp;", field: "Population", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
    ],
    rowClick: function (e, row) {
      var rowData = row.getData();
      var clickedCode = rowData["Code"];
      var clickedCountry = rowData["Country"];
      if (row._row.modules.select.selected == true) {
        tabulator_row_clicked('Country', 'selected', clickedCode);
        alert(clickedCountry + " added to country chart below")
      } else {
        if (list_of_codes_to_plot_countries.length > 1) {
          tabulator_row_clicked('Country', 'unselected', clickedCode);
        }
      }
    },
  });


  table.setSort([
    { column: "Country", dir: "asc" }, //then sort by this second
    { column: "Deaths_Last_Week_Per_Million", dir: "desc" }, //sort by this first
  ]);

  return table;
}




function defineTable_Countries_Doubling() {
  table = new Tabulator("#div_table-countries-doubling", {
    height: 600, // set height of table to enable virtual DOM
    layout: "fitColumns", //fit columns to width of table (optional)
    // autoColumns: true, // very nice!!!
    tooltipsHeader: true,
    selectable: true,
    columns: [ //Define Table Columns
      { title: "Country<br/>&nbsp;", field: "Country", sorter: "string", width: 100, headerFilter: true },
      // {
      //   title: "Code<br/>&nbsp;", field: "Code", sorter: "string", width: 30, sorterParams: {
      //     alignEmptyValues: "bottom"
      //   }, headerFilter: true
      // },
      {
        title: "Continent<br/>&nbsp;", field: "Continent", width: 75, editor: "select", sorter: "string", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterParams: {
          "": "any",
          "Africa": "Africa",
          "Asia": "Asia",
          "Europe": "Europe",
          "North America": "North America",
          "South America": "South America",
          "Oceania": "Oceania"
          // "Antarctica": "Antarctica",
        }
      },
      {
        title: "Incidence<br/>7-days", field: "Cases_Last_Week_Per_100000", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases Doubling Time<br/>Days", field: "DoublingTime_Cases_Last_Week_Per_100000", sorter: "number", width: 200, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Population<br/>&nbsp;", field: "Population", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases<br/>&nbsp;", field: "Cases", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases<br/>per Million", field: "Cases_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
    ],
    rowClick: function (e, row) {
      var rowData = row.getData();
      var clickedCode = rowData["Code"];
      var clickedCountry = rowData["Country"];
      if (row._row.modules.select.selected == true) {
        tabulator_row_clicked('Country', 'selected', clickedCode);
        alert(clickedCountry + " added to country chart above")
      } else {
        if (list_of_codes_to_plot_countries.length > 1) {
          tabulator_row_clicked('Country', 'unselected', clickedCode);
        }
      }
    },
  });


  table.setSort([
    { column: "Country", dir: "asc" }, //then sort by this second
    { column: "DoublingTime_Cases_Last_Week_Per_100000", dir: "asc" }, //sort by this first
  ]);

  return table;
}





// when a row is selected for adding to the chart, this is called
// type: Country or DeDistrict
// action: 'selected' or 'unselected'
function tabulator_row_clicked(type, action, clickedCode) {
  var list_of_codes_to_plot;
  if (type == 'Country') {
    list_of_codes_to_plot = list_of_codes_to_plot_countries;
  } else if (type == 'DeDistrict') {
    list_of_codes_to_plot = list_of_codes_to_plot_DeDistricts;
  }
  if (action == 'selected') {
    // append to list of codes, if not already included
    if (list_of_codes_to_plot.indexOf(clickedCode) == -1) {
      list_of_codes_to_plot.push(clickedCode);
    }

    // start fetching / download of data
    var dataObject;
    if (type == 'Country') {
      dataObject = data_object_countries;
    } else if (type == 'DeDistrict') {
      dataObject = data_object_DE_districts;
    }
    promises.push(fetchData(type, clickedCode, dataObject));
  }
  else if (action == 'unselected') {
    if (list_of_codes_to_plot.length > 1) {
      list_of_codes_to_plot = arrayRemove(list_of_codes_to_plot, clickedCode);
    }
  }
  // wait for fetching to complete, than update chart
  Promise.all(promises).then(function () {

    refresh_table_selections(type);
    if (type == 'Country') {
      // for simplicity: I do no longer remove selected countries from the selects
      // populateCountrySelects();
      // update_country_selects(clickedCode);
      refreshCountryChartWrapper();
    } else if (type == 'DeDistrict') {
      refreshDeDistrictsChartWrapper();
    }
  });
}


// updates selected rows of table type = (Country,DeDistrict)
function refresh_table_selections(type) {
  var myTable;
  var list_of_codes_to_plot;
  if (type == 'Country') {
    myTable = table_Countries;
    list_of_codes_to_plot = list_of_codes_to_plot_countries;
  } else if (type == 'DeDistrict') {
    myTable = table_DeDistricts;
    list_of_codes_to_plot = list_of_codes_to_plot_DeDistricts;
  }
  var rows = myTable.getRows();

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var rowData = row.getData();
    var id;
    if (type == 'Country') {
      id = rowData["Code"];
    } else if (type == 'DeDistrict') {
      id = rowData["LK_ID"];
    }
    if (list_of_codes_to_plot.indexOf(id) > -1) {
      row.select();
    } else {
      row.deselect();
    }
  }
}
