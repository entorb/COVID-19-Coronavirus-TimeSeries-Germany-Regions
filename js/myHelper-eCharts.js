// -------------
// Setting up Chart DeStates
// -------------
var codes_DeStates = ["BB", "BE", "BW", "BY", "HB", "HE", "HH", "MV", "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH", "DE-total"];
var mapDeStatesNames = {
    "BB": "Brandenburg",
    "BE": "Berlin",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "HB": "Bremen",
    "HE": "Hessen",
    "HH": "Hamburg",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SH": "Schleswig-Holstein",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "TH": "Thüringen",
    "DE-total": "DEUTSCHLAND"
};
const data_object_DeStates = {}; // We store all the data in an object
// For each DE state we fetch the data
for (let i = 0; i < codes_DeStates.length; i++) {
    promises.push(fetchData('DeState', codes_DeStates[i], data_object_DeStates));
}
// Wraps the refreshChart function so it is more readable, takes less space
function refreshDeStatesChartWrapper() {
    refreshDeChart(
        eChart_DeStates,
        codes_DeStates,
        data_object_DeStates,
        mapDeStatesNames,
        select_yAxisProperty_DeStates,
        select_xAxisTimeRange_DeStates,
        select_sorting_DeStates,
        update_url = false // false here becasue url is hard coded in refreshDeChart
    );
}


// -------------
// Setting up Chart DeDistricts
// -------------
var mapDeDistrictNames = {};

const data_object_DE_districts = {}; // We store all the data in an object

// For each district code we fetch the data
for (let i = 0; i < list_of_codes_to_plot_DeDistricts.length; i++) {
    promises.push(fetchData('DeDistrict', list_of_codes_to_plot_DeDistricts[i], data_object_DE_districts));
}

// chart parameter option lists
// const options_xAxisProperty
const options_yAxisProperty_DeDistricts = [
    "Cases_Last_Week_Per_100000",
    "Cases_Last_Week_Per_Million",
    "Cases_Per_Million",
    "Cases_New_Per_Million",
    "Cases",
    "Cases_Last_Week",
    "Cases_New",
    "Deaths_Last_Week_Per_Million",
    "Deaths_Per_Million",
    "Deaths_New_Per_Million",
    "Deaths",
    "Deaths_Last_Week",
    "Deaths_New",
    "DIVI_Intensivstationen_Covid_Prozent",
    "DIVI_Intensivstationen_Betten_belegt_Prozent",
];



// fetch mapping_landkreis_ID_name.json reference data like code and continent
function fetch_mapRefDeDistrictData(mapDeDistrictNames) {
    const url =
        "https://entorb.net/COVID-19-coronavirus/data/de-districts/mapping_landkreis_ID_name.json";
    return $.getJSON(url, function (data) {
        console.log("success: mapDeDistrictNames");
    })
        .done(function (data) {
            console.log("done: mapDeDistrictNames");
            $.each(data, function (key, val) {
                mapDeDistrictNames[key] = val;
            });
        })
        .fail(function () {
            console.log("fail: mapDeDistrictNames");
        });
}
// Wraps the refreshChart function so it is more readable, takes less space
function refreshDeDistrictsChartWrapper() {
    refreshDeChart(
        eChart_DeDistricts,
        list_of_codes_to_plot_DeDistricts,
        data_object_DE_districts,
        mapDeDistrictNames,
        select_yAxisProperty_DeDistricts,
        select_xAxisTimeRange_DeDistricts,
        select_sorting_DeDistricts,
        update_url = true
    );
}

// -------------
// Setting up Chart Countries
// -------------
// fetch ref list: Country Code -> Country Name
var mapCountryNames = {};
var mapContinentCountries = {};
const data_object_countries = {}; // We store all the data in an object
// For each country code we fetch the data
for (let i = 0; i < list_of_codes_to_plot_countries.length; i++) {
    promises.push(fetchData('Country', list_of_codes_to_plot_countries[i], data_object_countries));
}
// chart parameter option lists
const options_xAxisProperty = [
    "Date",
    "Days_Since_2nd_Death",
    "Days_Past",
    "Deaths_Per_Million",
    "Deaths_Last_Week_Per_Million",
    "Deaths_New_Per_Million",
    "Deaths",
    "Deaths_Last_Week",
    "Deaths_New",
    "Cases_Per_Million",
    "Cases_Last_Week_Per_100000",
    "Cases_Last_Week_Per_Million",
    "Cases_New_Per_Million",
    "Cases",
    "Cases_Last_Week",
    "Cases_New",
];
// "Deaths_Doubling_Time",
// "Cases_Doubling_Time"
const options_yAxisProperty = [
    "Deaths_Last_Week_Per_Million",
    "Deaths_Per_Million",
    "Deaths_New_Per_Million",
    "Deaths",
    "Deaths_Last_Week",
    "Deaths_New",
    "Cases_Last_Week_Per_100000",
    "Cases_Last_Week_Per_Million",
    "Cases_Per_Million",
    "Cases_New_Per_Million",
    "Cases",
    "Cases_Last_Week",
    "Cases_New",
    "Deaths_Per_Cases",
    "Deaths_Per_Cases_Last_Week",
];

const options_xaxis_time_range = [
    { value: "12weeks", text: "12 weeks" },
    { value: "4weeks", text: "4 weeks" },
    { value: "all", text: "all time" },
];

const options_axis_scales = [
    { value: "linscale", text: "linear" },
    { value: "logscale", text: "logarithmic" },
];
// country arrays
var options_countries_africa = [];
var options_countries_asia = [];
var options_countries_europe = [];
var options_countries_north_america = [];
var options_countries_south_america = [];
var options_countries_oceania = [];
// Wraps the refreshChart function so it is more readable, takes less space
function refreshCountryChartWrapper() {
    refreshCountryChart(
        eChart_countries,
        list_of_codes_to_plot_countries,
        data_object_countries,
        select_xAxisProperty,
        select_yAxisProperty,
        select_xAxisTimeRange,
        select_xAxisScale,
        select_yAxisScale,
        select_sorting_Countries,
        update_url = true
    );
}






// -------------
// Common Functions
// -------------

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


// De States Chart
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
            right: 200,
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
                {
                    yAxis: 1000,
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
                {
                    yAxis: 100,
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




function create_latest_data_plot(type, eChartsObjectID, property, property_for_color) {
    let array_data_latest = {}
    console.log('create_latest_data_plot: ' + type)
    if (type == 'Country') {
        array_data_latest = array_countries_latest;
    } else if (type == 'DeStates') {
        array_data_latest = array_states_latest;
    }
    let sortmap = [];
    const codes_ordered = [];
    // var data_names = [];
    // var data_values = [];
    var data_values_property_for_color = [];
    var data_set = [];
    var max_property_for_color = 0;
    let ordering = 'ASC';
    if (property == 'DoublingTime_Cases_Last_Week_Per_100000') {
        ordering = 'DESC';
    }

    for (const [key, values] of Object.entries(array_data_latest)) {
        if (property in values) {
            value = values[property];
            sortmap.push([key, value]);
        }
    }
    sortmap.sort(function (a, b) {
        return a[1] - b[1];
    });

    for (let i = 0; i < sortmap.length; i++) {
        codes_ordered.push(sortmap[i][0]);
    }

    if (ordering == 'DESC') {
        codes_ordered.reverse();
    }

    for (let i = 0; i < codes_ordered.length; i++) {

        if (type == 'Country') {
            name = array_data_latest[codes_ordered[i]]['Country'];
        } else if (type == 'DeStates') {
            name = array_data_latest[codes_ordered[i]]['State'];
        }
        value = array_data_latest[codes_ordered[i]][property];
        value_property_for_color = array_data_latest[codes_ordered[i]][property_for_color];
        if (value_property_for_color > max_property_for_color) {
            max_property_for_color = value_property_for_color;
        }
        data_set.push([name, value, value_property_for_color]);
    }

    option = {
        title: {
            // text: "COVID-19: Landkreisvergleich 7-Tages-Neuinfektionen",
            text: "COVID-19: " + capitalize_words(property, "_"),
            left: 'center',
            // subtext: "by Torben https://entorb.net based on JHU data",
            sublink: "https://entorb.net/COVID-19-coronavirus/",
        },
        yAxis: {
            type: 'category',
            // data: data_names,
        },
        xAxis: {
            type: 'value',
            position: 'top',
        },
        dataset: {
            source: data_set,
        },
        series: [{
            // data: data_values,
            datasetIndex: 0,
            type: 'bar'
        }],
        tooltip: {
            trigger: 'item', // item or axis

        },
        toolbox: {
            show: true,
            showTitle: true,
            feature: {
                saveAsImage: {},
            },
        }, grid: {
            containLabel: false,
            left: 200,
            bottom: 20,
            top: 90,
            right: 20,
        },
        visualMap: {
            dimension: 2,
            min: 0,
            max: max_property_for_color,
            text: [max_property_for_color, 0],
            // top: '60',
            show: false,
            // dataValue corresponding to the two handles.
        }
    };

    // fine tuning
    if (property == 'DoublingTime_Cases_Last_Week_Per_100000') {
        option.title.text = 'COVID-19: New Cases Doubling Time (days)'
    }
    if (type == 'Country') {
        option.title.subtext = "by Torben https://entorb.net based on JHU data"
    }
    else if (type == 'DeStates') {
        option.title.subtext = "by Torben https://entorb.net based on RKI data"
    }

    let echartsObj = echarts.init(document.getElementById(eChartsObjectID));
    echartsObj.setOption(option)
}
