function get_table_hq(wHqs, wChars, wHqsChars) {
	var table = '<table align="center" class="table_itens">'
	if (wHqs.length > 0) {
		var count = 0;
		table += '<tr align="center" class="tr_itens">';
		for (var i = 0; i < wHqs.length; i++) {
			var chars = format_characters_to_string(wHqs[i]['id'], wChars, wHqsChars);
			table += '<td align="center" class="td_itens">\
						<table class="item_table">\
							<tr>\
								<td align="center" class="item_title">'+substring(wHqs[i]['hq_title'], 12)+'</td>\
								<td align="center" class="item_edit" onclick="edit_item('+wHqs[i]['id']+');" align="center" valign="center">e</td>\
								<td align="center" class="item_delete" onclick="delete_hq('+wHqs[i]['id']+');" align="center" valign="center">x</td>\
							</tr>\
							<tr>\
								<td align="center" class="item_desc" colspan="3">\
									<div class="div_desc">\
										<span>'+wHqs[i]['hq_description']+'</span>\
									</div>\
								</td>\
							</tr>\
							<tr>\
								<td align="center" class="item_char" colspan="3">\
									<div class="div_char">\
										<span>'+chars+'</span>\
									</div>\
								</td>\
							</tr>\
							<tr>\
								<td align="center" class="item_year" colspan="3" align="center">Ano: '+wHqs[i]['hq_year']+'</td>\
							</tr>\
						</table>\
					</td>';
			count++;
			if (count == 5) {
				count = 0;
				table += '</tr><tr class="tr_itens">'
			}
		}
		for (var j = 0; j < 5-count; j++) table += '<td class="td_itens"></td>';
		table += '</tr>';
	}
	else {
		table += '<tr><td align="center"><span style="color: white; font-size: 30px;">Não há Hqs cadastradas</td></tr>';
	}
	table += '</table>';
	return table;
}