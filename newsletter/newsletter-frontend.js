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

function ensureHashIsValid() {
    // This dirty workaround is needed for Edge and IE :-(
    if ('search' in window.location) {
        urlParams = URLToParameterArray(window.location.search);
    } else {
        alert("Error: URL Parameter fehlt!");
    }
    if (!'hash' in urlParams) {
        alert("Error: Hash Parameter fehlt!");
    } else {
        hash = urlParams.hash;
    }
}

// ASync JQuery fetching
function fetch_table_data() {
    table.setData("https://entorb.net/COVID-19-coronavirus/data/de-districts/de-districts-results-V2.json", {}, "get")
}

function fetch_userdata() {
    const url = "https://entorb.net/COVID-19-coronavirus/newsletter-backend.py";
    return $.get(url, { action: "getUserdata", hash: hash }, function (response) {
    })
        .done(function (response) {
            console.log(response);
            if (response.status == "ok") {
                refresh_form(response);
            }
        });
}



function refresh_form(response) {
    if (response.userdata.regions === null) {
        l_my_regions = []
    } else {
        l_my_regions = response.userdata.regions.split(",");
    }
    input_email.value = response.userdata.email;
    input_frequency.value = response.userdata.frequency;
    input_threshold.value = response.userdata.threshold;
    // if (response.userdata.verified = 1) {
    //   input_verified.checked = true;
    // }
    //input_regions.value = response.userdata.regions;
}

function write_to_backend(param) {
    console.log("Request:");
    console.log(param);
    $.get("https://entorb.net/COVID-19-coronavirus/newsletter-backend.py", param,
        function (response) {
            console.log("Response:");
            console.log(response);
            if (response.status == "ok") {
                refresh_form(response);
            }
        }
    );
}
function setVerified() {
    param = { action: "verify", hash: hash };
    write_to_backend(param);
}
function setFrequency() {
    param = { action: "setFrequency", hash: hash, frequency: input_frequency.value };
    write_to_backend(param);
}
function setThreshold() {
    param = { action: "setThreshold", hash: hash, threshold: input_threshold.value };
    write_to_backend(param);
}
// Landkreise
function addRegion(region_id) {
    param = { action: "addRegion", hash: hash, region: region_id };
    write_to_backend(param);
}
function removeRegion(region_id) {
    param = { action: "removeRegion", hash: hash, region: region_id };
    write_to_backend(param);
}
function unsubscribe() {
    param = { action: "unsubscribe", hash: hash };
    response = write_to_backend(param);
    input_email.value = "";
    hash = "";
    alert("Abgemeldet, bitte diese Seite nun schließen.")
    // TODO: replace page by blank one or close it
}

function refresh_table_selections() {
    var rows = table.getRows();
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var rowData = row.getData();
        var lk_id = rowData["LK_ID"];
        // this landkreis_id in selection fetched from Backend?
        if (l_my_regions.indexOf(lk_id) > -1) {
            row.select();
        } else {
            row.deselect();
        }
    }
}

function refresh_userdata() {
    promises.push(fetch_userdata());

    // Wait for all async promises to be done (all data is fetched)
    Promise.all(promises).then(function () {
        // run code after table has been successfully updated
        refresh_table_selections();
    }
    );
}



function defineTable() {
    var table = new Tabulator("#div_table-de-districts", {
        height: 600, // set height of table to enable virtual DOM
        layout: "fitColumns", //fit columns to width of table (optional)
        // autoColumns: true, // very nice!!!
        tooltipsHeader: true,
        selectable: true,
        columns: [ //Define Table Columns
            // not using the checkbox column, as clicking the checkbox is not the same as clicking the row
            // { formatter: "rowSelection", titleFormatter: "rowSelection", align: "center", headerSort: true },
            {
                title: "Bundesland<br/>&nbsp;<br/>&nbsp;", field: "Bundesland", sorterParams: {
                    alignEmptyValues: "bottom"
                }, width: 150, headerFilter: true
                // , headerFilterPlaceholder:"select"
            },
            { title: "Landkreis<br/>&nbsp;<br/>&nbsp;", field: "Landkreis", sorter: "string", headerFilter: true },
            // {
            // 	title: "ID", field: "LK_ID", sorter: "string", width: 30, sorterParams: {
            // 		alignEmptyValues: "bottom"
            // 	}, headerFilter: true
            // },
            // {
            //     title: "Einwohner<br/>&nbsp;<br/>&nbsp;", field: "LK_Einwohner", sorter: "number", width: 130, hozAlign: "right", sorterParams: {
            //         alignEmptyValues: "bottom"
            //     }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            // },
            // { title: "Date", field: "Date", sorter: "date", sorterParams: { format: "YYYY-MM-DD" }, hozAlign: "center", headerFilter: true },
            // {
            //     title: "Infizierte<br/>&nbsp;<br/>&nbsp;", field: "Cases", sorter: "number", width: 120, hozAlign: "right", sorterParams: {
            //         alignEmptyValues: "bottom"
            //     }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            // },
            // {
            //     title: "Tote<br/>&nbsp;<br/>&nbsp;", field: "Deaths", sorter: "number", width: 75, hozAlign: "right", sorterParams: {
            //         alignEmptyValues: "bottom"
            //     }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            // },
            // {
            //     title: "Infizierte<br/>gesamt<br/>pro Mill.EW.", field: "Cases_Per_Million", sorter: "number", width: 135, hozAlign: "right", sorterParams: {
            //         alignEmptyValues: "bottom"
            //     }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            // },
            // {
            //     title: "Tote<br/>pro Mill.EW.<br/>&nbsp;", field: "Deaths_Per_Million", sorter: "number", width: 135, hozAlign: "right", sorterParams: {
            //         alignEmptyValues: "bottom"
            //     }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            // },
            {
                title: "Infizierte<br/>letzte Woche<br/>pro 100t EW.", field: "Cases_Last_Week_Per_100000", width: 135, sorter: "number", hozAlign: "right", sorterParams: {
                    alignEmptyValues: "bottom"
                }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            },
            {
                title: "Infizierte<br/>letzte Woche<br/>gesamt", field: "Cases_Last_Week", sorter: "number", width: 135, hozAlign: "right", sorterParams: {
                    alignEmptyValues: "bottom"
                }, headerFilter: true, headerFilterPlaceholder: "filter >=", headerFilterFunc: ">="
            },
        ],
        rowClick: function (e, row) {
            var rowData = row.getData();
            // console.log(row._row);
            // console.log(rowData);

            var clickedCode = rowData["LK_ID"];
            var clickedDistrict = rowData["Landkreis"];
            if (row._row.modules.select.selected == true) {
                addRegion(clickedCode);
                alert(clickedDistrict + " zur Auswahl hinzugefügt")
            } else {
                removeRegion(clickedCode);
                alert(clickedDistrict + " von Auswahl entfernt")
            }

            // var selectedRows = table.getSelectedRows();
            // console.log(selectedRows);
        },
    });

    table.setSort([
        { column: "Landkreis", dir: "asc" },
        { column: "Bundesland", dir: "asc" },
        { column: "Cases_Last_Week_Per_100000", dir: "desc" }, //sort by this first
    ]);

    return table;
}