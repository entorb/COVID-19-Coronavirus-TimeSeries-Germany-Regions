// -------------
// 1. Small helpers
// -------------

// remove all options of a select
// from https://stackoverflow.com/posts/3364546/timeline
function removeAllOptionsFromSelect(select) {
  var i, L = select.options.length - 1;
  for (i = L; i >= 0; i--) {
    select.remove(i);
  }
}

// Formats value "Something_Is_HERE" to "Something Is Here"
function capitalize_words(str, separator) {
  const allLowerCaseValue = str.split(separator).join(" ").toLowerCase();
  return allLowerCaseValue.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}


// Formats value "Something_Is_HERE" to "Something is here" like sentence
// value: The value to format
// separator: the separator string between words
function formatValueToSentenceLike(value, separator) { // , TODO: language
  // if (language == 'de') {
  //   value.replace("Cases", "Infektionen");
  //   value.replace("Deaths", "Tote");
  //   value.replace("_New", "_Neu");
  //   value.replace("_Last_Week", "_Letzte_Woche");
  //   value.replace("_Per_Million", "_Pro_Millionen");
  // }
  const allLowerCaseValue = value.split(separator).join(" ").toLowerCase();
  return allLowerCaseValue[0].toUpperCase() + allLowerCaseValue.substr(1);
}



// from https://love2dev.com/blog/javascript-remove-from-array/
function arrayRemove(arr, value) {
  //  return arr.filter(function (ele) { return ele != value; });
  for (let i = arr.length - 1; i >= 0; i--) {
    if (arr[i] === value) { arr.splice(i, 1); }
  }
}

// modifies array of objects by removing if value == keys
function arrayRemoveValueTextPairByValue(arr, key) {
  for (let i = arr.length - 1; i >= 0; i--) {
    if (arr[i].value === key) { arr.splice(i, 1); }
  }
}

// from https://stackoverflow.com/questions/4297765/make-a-javascript-array-from-url 
// needed as 
// const urlParams = new URLSearchParams(window.location.search); 
// is not available in Edge and IE :-(
function URLToParameterArray(url) {
  var request = {};
  var pairs = url.substring(url.indexOf('?') + 1).split('&');
  for (var i = 0; i < pairs.length; i++) {
    if (!pairs[i])
      continue;
    var pair = pairs[i].split('=');
    request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
  }
  return request;
}


// Adds options to the select, after removing all existing options
// select: The select object
// optionsArray: the options to add
// if optionsArray item consists of key, values pairs, than use the value for display, 
// else format the key to sentenceLike style
// if placeholdertext != "" than add this word as first dummy entry (for example "Choose"), important for onchange event on first selection
function setOptionsToSelect(select, optionsArray, placeholdertext) {
  removeAllOptionsFromSelect(select);
  if (placeholdertext != "") {
    // add a placeholder as first element, important for onchange event on first selection
    const option = document.createElement("option");
    option.value = "placeholder123";
    option.innerText = placeholdertext;
    select.add(option);
  }
  for (let i = 0; i < optionsArray.length; i++) {
    const option = document.createElement("option");
    if (optionsArray[i].value && optionsArray[i].text) {
      option.value = optionsArray[i].value;
      option.innerText = optionsArray[i].text;
    } else {
      option.value = optionsArray[i];
      option.innerText = capitalize_words(optionsArray[i], "_");
    }
    select.add(option);
  }
}


// -------------
// 2. My data specific functions
// -------------




// Gets the url of the given country
// type: Country or DeDistrict
// code: the code of the country e.g. "DE"
function getUrl(type, code) {
  if (type == 'Country') {
    return 'https://entorb.net/COVID-19-coronavirus/data/int/country-' + code + '.json';
  } else if (type == 'DeDistrict') {
    return 'https://entorb.net/COVID-19-coronavirus/data/de-districts/de-district_timeseries-' + code + '.json';
  } else if (type == 'DeState') {
    return 'https://entorb.net/COVID-19-coronavirus/data/de-states/de-state-' + code + '.json';
  }
}



// Fetches the data for one country code
// type: Country or DeDistrict
// code: the code of the country e.g. "DE"
// dataObject: the object which will contain all data about the Countries/DeDistricts
function fetchData(type, code, dataObject) {
  const url = getUrl(type, code);
  return $.getJSON(url, function () {
    // console.log(`success: ${code}`);
  })
    .done(function (data) {
      console.log('done: ' + code);
      dataObject[code] = data;
    })
    .fail(function () {
      console.log('fail:' + code);
    });
}


// Gets the series property of the chart object
// codes: the codes of the countries to display
// dataObject: the object which contains all data about the countries
// xAxis: the property displayed in the X axis
// yAxis: the property displayed in the Y axis
function getSeries(codes, dataObject, map_id_name, xAxis, yAxis, sorting) {
  //console.log(map_id_name);
  const series = [];
  const dataSymbols = new Array('circle', 'rect', 'triangle', 'diamond'); // 'roundRect', 'pin', 'arrow'

  let sortmap = [];
  const codes_ordered = [];
  // sort legend by name
  if (sorting == "Sort_by_name") {
    for (let i = 0; i < codes.length; i++) {
      sortmap.push([codes[i], map_id_name[codes[i]]]);
    }
    sortmap.sort(function (a, b) {
      return a[1] > b[1];
    });
    for (let i = 0; i < codes.length; i++) {
      codes_ordered.push(sortmap[i][0]);
    }
  }
  // sort legend by last value
  else if (sorting == "Sort_by_last_value") {
    for (let i = 0; i < codes.length; i++) {
      const values = dataObject[codes[i]]; //[key][yAxis];
      const value = values[values.length - 1][yAxis]
      sortmap.push([codes[i], value]);
    }
    sortmap.sort(function (a, b) {
      return a[1] - b[1];
    });

    for (let i = 0; i < codes.length; i++) {
      codes_ordered.push(sortmap[i][0]);
    }
    // reverse sorting, for all but the Doubling_Time series
    if (yAxis != "Cases_Doubling_Time" && yAxis != "Deaths_Doubling_Time") {
      codes_ordered.reverse();
    }
  }
  // sort by max value
  else if (sorting == "Sort_by_max_value") {
    for (let i = 0; i < codes.length; i++) {
      let max_value = 0;
      let values = dataObject[codes[i]];
      for (let j = 0; j < values.length; j++) {
        if (values[j][yAxis] > max_value) {
          max_value = values[j][yAxis];
        }
      }
      sortmap.push([codes[i], max_value]);
    }
    sortmap.sort(function (a, b) {
      return a[1] - b[1];
    });

    for (let i = 0; i < codes.length; i++) {
      codes_ordered.push(sortmap[i][0]);
    }
    codes_ordered.reverse();
  }




  codes = codes_ordered;

  for (let i = 0; i < codes.length; i++) {
    const countryLine = [];
    // We filter the data to display here using the axis data
    $.each(dataObject[codes[i]], function (key, val) {
      countryLine.push([
        dataObject[codes[i]][key][xAxis],
        dataObject[codes[i]][key][yAxis],
      ]);
    });
    const modulo = i % dataSymbols.length;

    const seria = {
      data: countryLine, // the line of the country
      name: map_id_name[codes[i]],
      type: "line",
      symbolSize: 6,
      smooth: true,
      symbol: dataSymbols[modulo],
    };
    series.push(seria);
  }
  return series;
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


// when a DeDistrict is selected for adding to the chart, this is called
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

function resetChart(type) {
  if (type == 'Country') {
    // populateCountrySelects();
    list_of_codes_to_plot_countries = ["DE"];
    refreshCountryChartWrapper();
  } else if (type == 'DeDistrict') {
    list_of_codes_to_plot_DeDistricts = [deDistrictCodesDefaultValue];
    refreshDeDistrictsChartWrapper();
  }
}

function populateCountrySelects() {
  options_countries_africa = [];
  options_countries_asia = [];
  options_countries_europe = [];
  options_countries_north_america = [];
  options_countries_south_america = [];
  options_countries_oceania = [];
  // Africa
  for (let i = 0; i < mapContinentCountries['Africa'].length; i++) {
    const code = mapContinentCountries['Africa'][i][0];
    const name = mapContinentCountries['Africa'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_africa.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_africa, options_countries_africa, "Choose");
  // Asia
  for (let i = 0; i < mapContinentCountries['Asia'].length; i++) {
    const code = mapContinentCountries['Asia'][i][0];
    const name = mapContinentCountries['Asia'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_asia.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_asia, options_countries_asia, "Choose");
  // Europe
  for (let i = 0; i < mapContinentCountries['Europe'].length; i++) {
    const code = mapContinentCountries['Europe'][i][0];
    const name = mapContinentCountries['Europe'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_europe.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_europe, options_countries_europe, "Choose");
  // North America
  for (let i = 0; i < mapContinentCountries['North America'].length; i++) {
    const code = mapContinentCountries['North America'][i][0];
    const name = mapContinentCountries['North America'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_north_america.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_north_america, options_countries_north_america, "Choose");
  // South America
  for (let i = 0; i < mapContinentCountries['South America'].length; i++) {
    const code = mapContinentCountries['South America'][i][0];
    const name = mapContinentCountries['South America'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_south_america.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_south_america, options_countries_south_america, "Choose");
  // Oceania
  for (let i = 0; i < mapContinentCountries['Oceania'].length; i++) {
    const code = mapContinentCountries['Oceania'][i][0];
    const name = mapContinentCountries['Oceania'][i][1]
    if (!(list_of_codes_to_plot_countries.indexOf(code) > -1)) {
      options_countries_oceania.push(
        { value: code, text: name }
      );
    }
  }
  setOptionsToSelect(select_countries_oceania, options_countries_oceania, "Choose");
}



// when a country is selected for adding to the chart, this is called to remove a certain value from the select
// NOT USED ANY MORE
function update_country_selects(country_code_to_add) { // , select_country, options_countries
  // TODO: unselecting a row in the table, should re-add the country to the selects. probably best done via full reset to default on each update.
  if (country_code_to_add != "placeholder123") {
    // Version 2: refresh all selects, as this is required when clicking in tabular instead of selecting via dropdown
    arrayRemoveValueTextPairByValue(options_countries_africa, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_asia, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_europe, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_north_america, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_south_america, country_code_to_add)
    arrayRemoveValueTextPairByValue(options_countries_oceania, country_code_to_add)
    setOptionsToSelect(select_countries_africa, options_countries_africa, "Choose");
    setOptionsToSelect(select_countries_asia, options_countries_asia, "Choose");
    setOptionsToSelect(select_countries_europe, options_countries_europe, "Choose");
    setOptionsToSelect(select_countries_north_america, options_countries_north_america, "Choose");
    setOptionsToSelect(select_countries_south_america, options_countries_south_america, "Choose");
    setOptionsToSelect(select_countries_oceania, options_countries_oceania, "Choose");

    // // wait for fetching to complete, than update chart
    // Promise.all(promises).then(function () {
    //   refreshCountryChartWrapper();
    // });
  }
}




// -------------
// 3. eCharts
// -------------



function refreshDeChart(
  chart,
  codes,
  dataObject,
  map_code_name,
  select_yAxisProperty,
  select_xAxisTimeRange,
  select_sorting,
  update_url
) {
  if (update_url) {
    // update/modify the URL
    window.history.pushState("object or string", "Title", "https://entorb.net/COVID-19-coronavirus/?yAxis=" + select_yAxisProperty_DeDistricts.value + "&DeDistricts=" + list_of_codes_to_plot_DeDistricts.toString() + "&Sort=" + select_sorting.value + "#DeDistrictChart");
  }
  option = {
    title: {
      // text: "COVID-19: Landkreisvergleich 7-Tages-Neuinfektionen",
      text: "COVID-19: " + capitalize_words(select_yAxisProperty.value, "_"),
      left: 'center',
      subtext: "by Torben https://entorb.net based on RKI data",
      sublink: "https://entorb.net/COVID-19-coronavirus/",
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 0,
      top: 50,
      //          bottom: 20,
    },
    xAxis: {
      // common settings for both axes
      type: 'time', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: {
        show: true,
        formatter: function (value) {
          var date = new Date(value);
          return date.toLocaleDateString("de-DE")
        }
      },
      // for x only
      name: 'Datum',
      nameLocation: 'end',

    },
    yAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: { show: true },
      // for y only
      name: capitalize_words(select_yAxisProperty.value, "_"),
      nameLocation: 'center',
      nameGap: 60,
    },
    series: getSeries(
      codes,
      dataObject,
      map_code_name,
      'Date',
      select_yAxisProperty.value,
      select_sorting.value
    ),
    tooltip: {
      trigger: 'axis', // item or axis
      axisPointer: {
        type: 'shadow',
        snap: true
      }
    },
    toolbox: {
      show: true,
      showTitle: true,
      feature: {
        // restore: {},
        dataZoom: {},
        dataView: { readOnly: true },
        saveAsImage: {},
        // magicType: {
        //  type: ['line', 'bar', 'stack', 'tiled']
        //},
        //brush: {},
      },
    },
    grid: {
      containLabel: false,
      left: 75,
      bottom: 40,
      right: 250,
    },
  };

  if (select_yAxisProperty.value == "Cases_Last_Week_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 500,
        },
      ]
    }
  }
  else if (select_yAxisProperty.value == "Cases_Last_Week_Per_100000") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 50,
        },
      ]
    }
  }
  else if (select_yAxisProperty.value.indexOf("DIVI_") == 0) {
    option.title.subtext = "by Torben https://entorb.net based on DIVI data";

  }


  // Time restriction for X Axis only
  if (select_xAxisTimeRange.value == "4weeks") {
    const daysOffset = - 4 * 7;
    const daysInterval = 7;
    // fetch latest date of first data series as basis
    const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
    const ts_last_date = Date.parse(s_data_last_date);
    var minDate = new Date(ts_last_date);
    minDate.setDate(minDate.getDate() + daysOffset);
    option.xAxis.min = minDate;
    option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
  } else if (select_xAxisTimeRange.value == "12weeks") {
    const daysOffset = - 12 * 7;
    const daysInterval = 14;
    // fetch latest date of first data series as basis
    const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
    const ts_last_date = Date.parse(s_data_last_date);
    var minDate = new Date(ts_last_date);
    minDate.setDate(minDate.getDate() + daysOffset);
    option.xAxis.min = minDate;
    option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
  }
  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}




// Refreshes the country chart
// list_of_codes_to_plot_countries: the codes of the countries to display
// countriesDataObject: the object which contains all data about the countries
// select_xAxisProperty: the select of the X axis
// select_yAxisProperty: the select of the Y axis
function refreshCountryChart(
  chart,
  list_of_codes_to_plot_countries,
  countriesDataObject,
  select_xAxisProperty,
  select_yAxisProperty,
  select_xAxisTimeRange,
  select_xAxisScale,
  select_yAxisScale,
  select_sorting,
  update_url
) {
  if (update_url) {
    // update/modify the URL
    window.history.pushState("object or string", "Title", "https://entorb.net/COVID-19-coronavirus/?yAxis=" + select_yAxisProperty.value + "&countries=" + list_of_codes_to_plot_countries.toString() + "&Sort=" + select_sorting.value + "#CountriesCustomChart");
  }


  // disable time selection for non-time series 
  if (select_xAxisProperty.value == "Date" || select_xAxisProperty.value == "Days_Past") {
    select_xAxisTimeRange.disabled = false;
  } else {
    select_xAxisTimeRange.disabled = true;
  }
  // disable logscale for time series
  if (select_xAxisProperty.value == "Date" || select_xAxisProperty.value == "Days_Past") {
    select_xAxisScale.disabled = true;
    select_xAxisScale.value = 'linscale';
  } else {
    select_xAxisScale.disabled = false;
  }
  // disable logscale for deaths_per_cases
  if (select_yAxisProperty.value == "Deaths_Per_Cases" || select_yAxisProperty.value == "Deaths_Per_Cases_Last_Week") {
    select_yAxisScale.disabled = true;
    select_yAxisScale.value = 'linscale';
  }


  option = {}
  // optionsAxisCommon = {
  //   // settings for both axis
  //   boundaryGap: false,
  //   nameTextStyle: { fontWeight: "bold" },
  //   minorTick: { show: true },
  //   minorSplitLine: {
  //     show: true
  //   },
  //   axisTick: { inside: true },
  //   axisLabel: { show: true },
  // }

  //  text: "COVID-19 Country Comparison Custom Chart",

  option = {
    title: {
      text: "COVID-19: " + capitalize_words(select_yAxisProperty.value, "_"),
      left: 'center',
      subtext: "by Torben https://entorb.net based on JHU data",
      sublink: "https://entorb.net/COVID-19-coronavirus/",
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 0,
      top: 50,
      //          bottom: 20,
    },
    xAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: {
        show: true,
      },
      // for x only
      name: capitalize_words(select_xAxisProperty.value, "_"),
      nameLocation: 'end',
    },
    // in type log : setting min is required
    yAxis: {
      // common settings for both axes
      type: 'value', // will be overwritten if needed below
      boundaryGap: false,
      nameTextStyle: { fontWeight: "bold" },
      minorTick: { show: true },
      minorSplitLine: {
        show: true
      },
      axisTick: { inside: true },
      axisLabel: { show: true },
      // for y only
      name: capitalize_words(select_yAxisProperty.value, "_"),
      nameLocation: 'center',
      nameGap: 60,
    },
    series: getSeries(
      list_of_codes_to_plot_countries,
      countriesDataObject,
      mapCountryNames,
      select_xAxisProperty.value,
      select_yAxisProperty.value,
      select_sorting.value
    ),
    tooltip: {
      trigger: 'axis', // item or axis
      axisPointer: {
        type: 'shadow',
        snap: true
      }
    },
    toolbox: {
      show: true,
      showTitle: true,
      feature: {
        // restore: {},
        dataZoom: {},
        dataView: { readOnly: true },
        saveAsImage: {},
        // magicType: {
        //  type: ['line', 'bar', 'stack', 'tiled']
        //},
        //brush: {},
      },
    },
    grid: {
      containLabel: false,
      left: 75,
      bottom: 40,
      right: 180,
    },
  };

  if (select_xAxisProperty.value == "Date") {
    option.xAxis.type = "time";
    option.xAxis.axisLabel.formatter = function (value) {
      var date = new Date(value);
      return date.toLocaleDateString("de-DE")
    }

    // trying to modify the date format
    // option.xAxis.axisLabel.formatter = function (value, index) {
    //   // Formatted to be month/day; display year only in the first label
    //   var date = new Date(value);
    //   var texts = [(date.getMonth() + 1), date.getDate()];
    //   if (index === 0) {
    //     texts.unshift(date.getYear());
    //   }
    //   return texts.join('-');
    // }
  }

  // For doubling time: invert axis, only for Y
  if (select_yAxisProperty.value == "Cases_Doubling_Time" || select_yAxisProperty.value == "Deaths_Doubling_Time") {
    option.yAxis.inverse = true;
    option.yAxis.name = option.yAxis.name + " (days)";
    // option.yAxis.nameLocation = "start";
  }

  // Time restriction for X Axis only
  if (select_xAxisTimeRange.value == "4weeks") {
    const daysOffset = - 4 * 7;
    const daysInterval = 7;
    if (select_xAxisProperty.value == "Days_Past") {
      option.xAxis.min = daysOffset;
      option.xAxis.interval = daysInterval;
    }
    else if (select_xAxisProperty.value == "Date") {
      // fetch latest date of first data series as basis
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
      const ts_last_date = Date.parse(s_data_last_date);
      var minDate = new Date(ts_last_date);
      minDate.setDate(minDate.getDate() + daysOffset);
      option.xAxis.min = minDate;
      option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
    }
  } else if (select_xAxisTimeRange.value == "12weeks") {
    const daysOffset = - 12 * 7;
    const daysInterval = 14;
    if (select_xAxisProperty.value == "Days_Past") {
      option.xAxis.min = daysOffset;
      option.xAxis.interval = daysInterval;
    }
    else if (select_xAxisProperty.value == "Date") {
      // fetch latest date of first data series as basis
      const s_data_last_date = option.series[0].data[option.series[0].data.length - 1][0];
      const ts_last_date = Date.parse(s_data_last_date);
      var minDate = new Date(ts_last_date);
      minDate.setDate(minDate.getDate() + daysOffset);
      option.xAxis.min = minDate;
      option.xAxis.interval = 3600 * 1000 * 24 * daysInterval;
    }
  }

  // Logscale for X Axis (eCharts allows either time axis or log axis)
  if (select_xAxisProperty.value != "Date") {
    if (select_xAxisScale.value == "linscale") {
      option.xAxis.type = "value";
    } else {
      option.xAxis.type = "log";
      // for logscale we need to set the min value to avoid 0 is not good ;-)
      if (select_xAxisProperty.value == "Deaths_New_Per_Million") {
        option.xAxis.min = 0.1;
      } else {
        option.xAxis.min = 1;
      }
    }
  }
  // Logscale for Y Axis (eCharts allows either time axis or log axis)
  if (select_yAxisScale.value == "linscale") {
    option.yAxis.type = "value";
  } else {
    option.yAxis.type = "log";
    // for logscale we need to set the min value to avoid 0 is not good ;-)
    if (select_yAxisProperty.value == "Deaths_New_Per_Million" || select_yAxisProperty.value == "Deaths_Last_Week_Per_Million") {
      option.yAxis.min = 0.1;
    } else {
      option.yAxis.min = 1;
    }
  }

  // Marklines
  if (select_yAxisProperty.value == "Deaths_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        // { type: 'average', name: '123' },
        {
          yAxis: 9,
          name: 'US 9/11',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 44,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104,
          name: 'US traffic 2018 and flu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }
  if (select_yAxisProperty.value == "Deaths_New_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 44 / 365,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104 / 365,
          name: 'US traffic 2018 and flu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205 / 365,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857 / 365,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 8638 / 365,
          name: 'US total mortality 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }
  if (select_yAxisProperty.value == "Deaths_Last_Week_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 44 / 52.14,
          name: 'US guns 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 104 / 52.14,
          name: 'US traffic 2018 and flu 2018/19',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 205 / 52.14,
          name: 'US drugs 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 1857 / 52.14,
          name: 'US cancer 2018',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
        {
          yAxis: 8638 / 52.14,
          name: 'US total mortality 2017',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name
          },
        },
      ]
    }
  }
  else if (select_yAxisProperty.value == "Cases_Last_Week_Per_Million") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 500,
          name: '500',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name        
          },
        },
      ]
    }
  }
  else if (select_yAxisProperty.value == "Cases_Last_Week_Per_100000") {
    option.series[0].markLine = {
      symbol: 'none',
      silent: true,
      animation: false,
      lineStyle: {
        color: "#0000ff"
        //type: 'solid'
      },
      data: [
        {
          yAxis: 50,
          name: '50',
          // value: 'value',
          label: {
            position: 'insideStartTop',
            formatter: '{b}' // b -> name        
          },
        },
      ]
    }
  }

  chart.clear(); // needed as setOption does not reliable remove all old data, see https://github.com/apache/incubator-echarts/issues/6202#issuecomment-460322781
  chart.setOption(option, true);
}




