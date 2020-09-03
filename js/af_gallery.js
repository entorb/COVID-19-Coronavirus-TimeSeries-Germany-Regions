function af_gallery_hideAll(results_div) {
  var results = document.getElementById(results_div);
  var element = results.getElementsByTagName("article");

  for (i = 1; i < element.length; i++) {
    element[i].style.display = "none";
  }
}

function af_gallery_show(results_div, hash) {
  var results = document.getElementById(results_div);
  var element = results.getElementsByTagName("article");

  for (i = 0; i < element.length; i++) {
    if (hash === element[i].id) {
      element[i].style.display = ""
    } else {
      element[i].style.display = "none";
    }
  }
}

// function filter() {
// 	var input, filter, ul, li, a, i;
// 	input = document.getElementById("filter");
// 	filter = input.value.toUpperCase();
// 	div = document.getElementById("dropdown");
// 	element = div.getElementsByTagName("a");
// 	for (i = 0; i < element.length; i++) {
// 		textValue = element[i].textContent || element[i].innerText;
// 		if (textValue.toUpperCase().indexOf(filter) > -1) {
// 			element[i].style.display = "";
// 		} else {
// 			element[i].style.display = "none";
// 		}
// 	}
// }
