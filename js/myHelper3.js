// -------------
// 0. Variables and code to run
// -------------


// array of promises for async fetching, used for eCharts plots
const promises = [];

// here we store latest data for countries and states
var array_countries_latest = {};
var array_states_latest = {};

// This dirty workaround is needed for Edge and IE :-(
var urlParams = [];
if ('search' in window.location) {
  urlParams = URLToParameterArray(window.location.search);
}
const options_eCharts_sorting = [
  "Sort_by_last_value",
  "Sort_by_max_value",
  "Sort_by_name"
]


// Initial list of DeDistrict codes
var deDistrictCodesDefaultValue = "02000"; // do not delete, used in reset function as well
if ('DeDistricts' in urlParams) {
  var list_of_codes_to_plot_DeDistricts = urlParams.DeDistricts.split(",");
  // Adding an entry to this array draws a new line
  // read districts list from URL parameter if set
} else {
  // Adding an entry to this array draws a new line
  // read districts list from URL parameter if set
  // 02000 = Hamburg
  // 05558 = Coesfeld
  // 05370 = Heinsberg
  var list_of_codes_to_plot_DeDistricts = [deDistrictCodesDefaultValue];
}


// Initial list of country codes
if ('countries' in urlParams) {
  var list_of_codes_to_plot_countries = urlParams.countries.split(",");
} else {
  // Adding a new country code to this array draws a new line
  var list_of_codes_to_plot_countries = ["DE"];
}

// -------------
// fetching data
// -------------
function fetch_countries_latest(array_countries_latest) {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/int/countries-latest-all.json";
  return $.getJSON(url, function (data) {
    console.log("success: array_countries_latest");
  })
    .done(function (data) {
      console.log("done: array_countries_latest");
      $.each(data, function (key, val) {
        code = data[key]['Code'];
        array_countries_latest[code] = val;
        delete array_countries_latest[code]['Code'];
      });
      // console.log(array_countries_latest);

    })
    .fail(function () {
      console.log("fail: array_countries_latest");
    });
}



function fetch_states_latest(array_states_latest) {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/de-states/de-states-latest-list.json";
  return $.getJSON(url, function (data) {
    console.log("success: array_states_latest");
  })
    .done(function (data) {
      console.log("done: array_states_latest");
      $.each(data, function (key, val) {
        code = data[key]['Code'];
        array_states_latest[code] = val;
        delete array_states_latest[code]['Code'];
      });
      // console.log(array_states_latest);

    })
    .fail(function () {
      console.log("fail: array_states_latest");
    });
}


// populates
// de_district_multiplot_sel_kreis
// icu_forecast_sel_de_districts
// TODO: for icu_forecast_sel_de_districts filter auf /data/de-districts/lkids.json
function populate_de_district_multiplot_and_icu_select() {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/de-districts/mapping_landkreis_ID_name.json";
  return $.getJSON(url, function (data) {
    console.log("success: mapping_landkreis_ID_name.json");
  })
    .done(function (data) {
      console.log("done: mapping_landkreis_ID_name.json");
      de_district_multiplot_sel_kreis = document.getElementById("de_district_multiplot_sel_kreis");
      icu_forecast_sel_de_districts = document.getElementById("icu_forecast_sel_de_districts");

      // TODO: this is quite a dirty hack
      var data2 = {};
      // swap key and value for sorting
      $.each(data, function (key, val) {
        data2[val] = key;
      });

      Object.keys(data2)
        .sort()
        .forEach(function (v, i) {
          var opt1 = document.createElement('option');
          opt1.innerHTML = v;
          opt1.value = data2[v];
          de_district_multiplot_sel_kreis.appendChild(opt1);
          // TODO: cloning of object needed, here dirty hack
          var opt2 = document.createElement('option');
          opt2.innerHTML = v;
          opt2.value = data2[v];
          icu_forecast_sel_de_districts.appendChild(opt2);
        });
    });
}

function de_district_multiplot_selected() {
  document.getElementById("de_district_multiplot_img").src =
    "plots-python/de-districts/de-district-" +
    document.getElementById("de_district_multiplot_sel_kreis").value
    + ".png";
}



// populates
// icu_forecast_sel_de_district_group
function icu_forecast_sel_de_district_group_populate_select() {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/de-divi/lk-groups.json";
  return $.getJSON(url, function (data) {
    console.log("success: de-divi/lk-groups.json");
  })
    .done(function (data) {
      console.log("done: de-divi/lk-groups.json");
      icu_forecast_sel_de_district_group = document.getElementById("icu_forecast_sel_de_district_group");

      var data2 = {};

      for (const d of data) {
        val = d["title"]
        key = d["id"]
        data2[val] = key;
      }

      Object.keys(data2)
        .sort()
        .forEach(function (v, i) {
          var opt2 = document.createElement('option');
          opt2.innerHTML = v;
          opt2.value = data2[v];
          icu_forecast_sel_de_district_group.appendChild(opt2);
        });
    });
}



function icu_forecast_sel_de_states_selected() {
  document.getElementById("icu_forecast_img").src =
    "plots-python/icu-forecast/de-states/" +
    document.getElementById("icu_forecast_sel_de_states").value
    + ".png";
  document.getElementById("icu_forecast_img_zoom").src =
    "plots-python/icu-forecast/de-states/" +
    document.getElementById("icu_forecast_sel_de_states").value
    + "-zoom.png";
}

function icu_forecast_sel_de_districts_selected() {
  document.getElementById("icu_forecast_img").src =
    "plots-python/icu-forecast/single/" +
    document.getElementById("icu_forecast_sel_de_districts").value
    + ".png";
  document.getElementById("icu_forecast_img_zoom").src =
    "plots-python/icu-forecast/single/" +
    document.getElementById("icu_forecast_sel_de_districts").value
    + "-zoom.png";
}

function icu_forecast_sel_de_district_group_selected() {
  document.getElementById("icu_forecast_img").src =
    "plots-python/icu-forecast/de-district-group/" +
    document.getElementById("icu_forecast_sel_de_district_group").value
    + ".png";
  document.getElementById("icu_forecast_img_zoom").src =
    "plots-python/icu-forecast/de-district-group/" +
    document.getElementById("icu_forecast_sel_de_district_group").value
    + "-zoom.png";
}


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
  str = str.replace("Cases_Last_Week_Per_100000", "Inzidenz");
  const allLowerCaseValue = str.split(separator).join(" ").toLowerCase();
  return allLowerCaseValue.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}


// Formats value "Something Is HERE" to "Something is here" like sentence
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
// dataObject: the object which will updated with data about the Countries/DeDistricts
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


// fetch countries-latest-all.json containing country reference data like code and continent
function fetch_mapRefCountryData(mapCountryNames, mapContinentCountries) {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/int/countries-latest-all.json";
  return $.getJSON(url, function (data) {
    console.log("success: mapCountryNames");
  })
    .done(function (data) {
      console.log("done: mapCountryNames");
      $.each(data, function (key, val) {
        mapCountryNames[data[key].Code] = data[key].Country;
        const this_continent = data[key].Continent;
        if (!(this_continent in mapContinentCountries)) {
          mapContinentCountries[this_continent] = [];
        }
        mapContinentCountries[this_continent].push([data[key].Code, data[key].Country]);  // pair of country_code , country_name
      });
    })
    .fail(function () {
      console.log("fail: mapCountryNames");
    });
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



// NOT USED ANY MORE
// when a country is selected for adding to the chart, this is called to remove a certain value from the select
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
