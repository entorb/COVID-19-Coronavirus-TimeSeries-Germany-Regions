function defineTable_DeDistricts() {
  var table = new Tabulator("#div_table-de-districts", {
    height: 600, // set height of table to enable virtual DOM
    layout: "fitColumns", //fit columns to width of table (optional)
    // autoColumns: true, // very nice!!!
    tooltipsHeader: true,
    selectable: true,
    columns: [ //Define Table Columns
      {
        title: "Bundesland<br/>&nbsp;<br/>&nbsp;", field: "Bundesland", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true
        // , headerFilterPlaceholder:"select"
      },
      { title: "Landkreis<br/>&nbsp;<br/>&nbsp;", field: "Landkreis", sorter: "string", headerFilter: true },
      // {
      // 	title: "ID", field: "LK_ID", sorter: "string", width: 30, sorterParams: {
      // 		alignEmptyValues: "bottom"
      // 	}, headerFilter: true
      // },
      {
        title: "Einwohner<br/>&nbsp;<br/>&nbsp;", field: "Population", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // { title: "Date", field: "Date", sorter: "date", sorterParams: { format: "YYYY-MM-DD" }, hozAlign: "center", headerFilter: true },
      {
        title: "Infizierte<br/>&nbsp;<br/>&nbsp;", field: "Cases", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Tote<br/>&nbsp;<br/>&nbsp;", field: "Deaths", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
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
      {
        title: "Infizierte<br/>pro 100t .EW.<br/>pro Woche", field: "Cases_Last_Week_Per_100000", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Tote<br/>pro Mill.EW.<br/>pro Woche", field: "Deaths_Last_Week_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Infizierte<br/>Trend<br/>Index", field: "Slope_Cases_New_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Intensivstationen<br/>% COVID-19<br/>&nbsp;", field: "DIVI_Intensivstationen_Covid_Prozent", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Intensivstationen<br/>% belegt<br/>&nbsp;", field: "DIVI_Intensivstationen_Betten_belegt_Prozent", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
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
      { title: "Country<br/>&nbsp;", field: "Country", sorter: "string", width: 100, headerFilter: true },
      {
        title: "Code<br/>&nbsp;", field: "Code", sorter: "string", width: 30, sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true
      },
      {
        title: "Population<br/>&nbsp;", field: "Population", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // { title: "Date", field: "Date", sorter: "date", sorterParams: { format: "YYYY-MM-DD" }, hozAlign: "center", headerFilter: true },
      {
        title: "Cases<br/>&nbsp;", field: "Cases", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Deaths<br/>&nbsp;", field: "Deaths", sorter: "number", width: 100, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases<br/>per Million", field: "Cases_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Deaths<br/>per Million", field: "Deaths_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases Last Week<br/>per 100000", field: "Cases_Last_Week_Per_100000", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Deaths Last Week<br/>per Million", field: "Deaths_Last_Week_Per_Million", sorter: "number", hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      {
        title: "Cases Doubling Time<br/>Days", field: "DoublingTime_Cases_Last_Week_Per_100000", sorter: "number", width: 200, hozAlign: "right", sorterParams: {
          alignEmptyValues: "bottom"
        }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      },
      // {
      // 	title: "Deaths<br/>Doubling Time (Days)", field: "Deaths_Doubling_Time", sorter: "number", hozAlign: "right", sorterParams: {
      // 		alignEmptyValues: "bottom"
      // 	}, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
      // },
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
