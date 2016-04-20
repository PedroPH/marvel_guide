var special_character = '[^A-Za-z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\n ]+';

function v_year(wYear) {
	var year = new Date();
	year = year.getFullYear();
	if (wYear.length != 4) return false;
	if (wYear < 1961 || wYear > year) return false;
	return true;
}

function v_special_character(wString) {
	return wString.match(special_character) != null
}