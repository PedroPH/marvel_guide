function substring(wString, wSize) {
	if (wString.length > wSize) return wString.substring(0, wSize) + '...';
	return wString;
}

function format_characters_to_string(wHqId, wChars, wHqsChars) {
	var s_chars = '';
	for (var i = 0; i < wHqsChars.length; i++) {
		if (wHqsChars[i]['hq'] == wHqId) {
			for (var j = 0; j < wChars.length; j++) {
				if (wChars[j]['id'] == wHqsChars[i]['marvel_character'])
					s_chars += wChars[j]['char_name'] + '\n';
			}
		}
	}
	return s_chars;
}