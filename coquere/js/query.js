function getQueryVariable(variable){
	console.log(window.location.search.substring(1));
	var query=window.location.search.substring(1);
	console.log(query);
	var vars = query.split("&");
	for (var i=0; i<vars.length; i++){
		var pair=vars[i].split("=");
		if (pair[0] == variable) {
			return pair[1];
		}
	}
}
function loadMap() {
	contentUrl = document.getElementById("wm").contentWindow.location.href;
	if (contentUrl == "ingredientNets/worldmap.html"){
		document.getElementById("wmback").style.display = 'none';
		document.getElementById("wmback").href="";
	}
	else{
		console.log(contentUrl)
	}

}
