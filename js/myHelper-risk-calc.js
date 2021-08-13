function rc_calc_en() {

  document.getElementById("rc_input_cases_last_week_100k").value = document.getElementById("rc_input_cases_last_week_100k_en").value;
  document.getElementById("rc_input_factor_unreported").value = document.getElementById("rc_input_factor_unreported_en").value;
  document.getElementById("rc_input_num_people").value = document.getElementById("rc_input_num_people_en").value;
  document.getElementById("rc_input_factor_unreported").value = document.getElementById("rc_input_factor_unreported_en").value;
  rc_calc();
  document.getElementById("rc_output_infectious_pop_en").value = document.getElementById("rc_output_infectious_pop").value;

  document.getElementById("rc_output_prop_someone_at_event_is_infectious_en").value = document.getElementById("rc_output_prop_someone_at_event_is_infectious").value;

}

function rc_calc() {
  const cases_last_week_100k = document.getElementById("rc_input_cases_last_week_100k").value;
  var string_prop_someone_at_event_is_infectious_in_percent;
  if (cases_last_week_100k >= 100000) {
    string_prop_someone_at_event_is_infectious_in_percent = "100%"
    document.getElementById("rc_output_infectious_pop").value = 100000;
  } else {
    const factor_unreported = document.getElementById("rc_input_factor_unreported").value;
    // const factor_unreported = 4;
    const people = document.getElementById("rc_input_num_people").value;
    const cases_last_week_100k_reported_and_unreported = cases_last_week_100k * factor_unreported;
    document.getElementById("rc_output_infectious_pop").value = cases_last_week_100k_reported_and_unreported.toFixed(1);
    const prop_1_random_person_is_infectious = cases_last_week_100k_reported_and_unreported / 100000;
    const prop_no_one_at_event_is_infectious = Math.pow((1 - prop_1_random_person_is_infectious), people)
    const prop_someone_at_event_is_infectious = 1 - prop_no_one_at_event_is_infectious;
    string_prop_someone_at_event_is_infectious_in_percent = (prop_someone_at_event_is_infectious * 100).toFixed(1) + "%";
  }
  // console.log(string_prop_someone_at_event_is_infectious_in_percent);

  document.getElementById("rc_output_prop_someone_at_event_is_infectious").value = string_prop_someone_at_event_is_infectious_in_percent;
}



// TODO: provide selection of Bundesland or District
// fetches DE_states_latest data and populates selects for risk calculator
function rc_fetch_DE_states_and_populate_risk_calc_select() {
  const url =
    "https://entorb.net/COVID-19-coronavirus/data/de-states/de-states-latest.json";
  return $.getJSON(url, function (data) {
    console.log("success: de-states-latest");
  })
    .done(function (data) {
      console.log("done: de-states-latest");
      rc_sel_bundesland = document.getElementById("rc_sel_bundesland");

      // console.log(data);

      list_of_de_states = [
        "DE-total"
        , "BW"
        , "BY"
        , "BE"
        , "BB"
        , "HB"
        , "HH"
        , "HE"
        , "MV"
        , "NI"
        , "NW"
        , "RP"
        , "SL"
        , "SN"
        , "ST"
        , "SH"
        , "TH"];

      // $.each(data, function (bl_key, bl_data) {
      for (var i = 0; i < list_of_de_states.length; i++) {
        bl_data = data[list_of_de_states[i]];
        // mapDeDistrictNames[key] = val;
        var opt = document.createElement('option');
        opt.innerHTML = bl_data['State'];
        // ensure value >= 1
        if (bl_data['Cases_Last_Week_Per_100000'] >= 1) {
          opt.value = bl_data['Cases_Last_Week_Per_100000'];
        } else {
          opt.value = 1.0;
        }
        rc_sel_bundesland.appendChild(opt);


      }
      // set inital value to DE-total
      document.getElementById("rc_input_cases_last_week_100k").value = data["DE-total"]["Cases_Last_Week_Per_100000"];      // });
    })
    .fail(function () {
      console.log("fail: de-states-latest");
    });
}
promises.push(rc_fetch_DE_states_and_populate_risk_calc_select());


function rc_sel_bundesland_selected() {
  document.getElementById("rc_input_cases_last_week_100k").value = document.getElementById("rc_sel_bundesland").value;
  rc_calc();
}



		// populate select
		// rc_sel_bundesland = document.getElementById("rc_sel_bundesland");
		// for (var i = 0; i <= 16; i++) {
		// 	var opt = document.createElement('option');
		// 	opt.value = i;
		// 	opt.innerHTML = i;
		// rc_sel_bundesland.appendChild(opt);
		// }
