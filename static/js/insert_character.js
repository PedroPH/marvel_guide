var characters = [];

function previewImage(wImg) {

    if (wImg.files && wImg.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img_preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(wImg.files[0]);
    }
}

function fillTableCharacters() {
	var table = '<table>';
	for (var i = 0; i < characters.length; i++) {
		table += '<tr>\
					<td>'+characters[i]['name']+'</td>\
					<td>'+characters[i]['cat']+'</td>\
				</tr>';
	}
	table += '</table>';
	$('#table_characters').html(table);
}