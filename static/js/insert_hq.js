var hqs = [];
var count = 0;
var insert = 'true';
var item_edit;
var chars = [];
var hqs = [];
var hqs_chars = [];

function init_insert_hq(wChars, wHqs, wHqs_chars) {
	chars = wChars;
	hqs = wHqs;
	hqs_chars = wHqs_chars;
	fill_characters();
	fill_table_hq();
	$('#hq_year').mask("9999");
}

function submit_insert_hq() {
	var error = '';
	
	if ($('#hq_title').val() == '') error += '<p>Titulo <span class="error_description">(Não pode ser vazio)</span></p>';
	if (v_special_character($('#hq_title').val())) error += '<p>Titulo <span class="error_description">(Caraceteres especiais)</span></p>';
	if ($('#hq_character').val() == null) error += '<p>Personagens <span class="error_description">(Selecione ao menos, uma opção)</span></p>';
	if ($('#hq_description').val() == '') error += '<p>Descri&ccedil;&atilde;o <span class="error_description">(Não pode ser vazio)</span></p>';
	if ($('#hq_year').val() == '') error += '<p>Ano <span class="error_description">(Não pode ser vazio)</span></p>';
	else {
		if ( !v_year( $('#hq_year').val() ) ) error += '<p>Ano <span class="error_description">(Data inválida)</span></p>';
	}

	if (error) expose_modal('Campo(s) com problema(s)!', error);
	else {
		expose_modal('Aguarde!', '<p>Processando...</p>');
		$.ajax({
			url: '/marvel_guide/backcall/insert_hq/',
			type: "POST",
			data: {'hq_title' : $('#hq_title').val(),
				   'hq_description' : $('#hq_description').val(),
				   'hq_character' : JSON.stringify($('#hq_character').val()),
				   'hq_year' : $('#hq_year').val(),
				   'insert' : insert,
				   'item_edit' : item_edit},
			enctype: 'multipart/form-data',
			success:function(wRet){
				ret = JSON.parse(wRet);
				if (ret == 'erro') expose_modal('Problema', '<p>Tente novamente mais tarde!</p>');
				else {
					hqs = ret['hqs'];
					hqs_chars = ret['hqs_characters'];
					fill_table_hq();
				}
			},
			error: function (error) {
				close_modal();
				expose_modal('Atenção!', '<p>Ocorreu um erro!</p>');
			}
		});
	}
}

function delete_hq(wId) {
	$.ajax({
		url: '/marvel_guide/backcall/delete_hq/',
		type: "POST",
		data: {'delete' : wId},
		enctype: 'multipart/form-data',
		success:function(wRet){
			ret = JSON.parse(wRet);
			if (ret == 'erro') expose_modal('Problema', '<p>Tente novamente mais tarde!</p>');
			else {
				hqs = ret['hqs'];
				hqs_chars = ret['hqs_characters'];
				fill_table_hq();
			}
		},
		error: function (error) {
			close_modal();
			expose_modal('Atenção!', '<p>Ocorreu um erro!</p>');
		}
	});
}

function fill_table_hq() {
	$('#table_hqs').html(get_table_hq(hqs, chars, hqs_chars));
	close_modal();
}

function edit_item(wId) {
	$('#insert').val('Atualizar');
	$('#cancel').show();
	insert = 'false';
	item_edit = wId;
	for (var i = 0; i < hqs.length; i++) {
		if (hqs[i]['id'] == item_edit) {
			$('#hq_title').val(hqs[i]['hq_title']);
			var cha = [];
			for (var j = 0; j < hqs_chars.length; j++) {
				if (hqs[i]['id'] == hqs_chars[j]['hq']) cha.push(hqs_chars[j]['marvel_character']);
			}
			$('#hq_character').val(cha);
			$('#hq_character').selectpicker('refresh');
			$('#hq_description').val(hqs[i]['hq_description']);
			$('#hq_year').val(hqs[i]['hq_year']);
		}
	}
}

function cancel_edit(argument) {
	$('#insert').val('Inserir');
	$('#cancel').hide();
	$('#hq_title').val('');
	$('#hq_character').val([]);
	$('#hq_character').selectpicker('refresh');
	$('#hq_description').val('');
	$('#hq_year').val('');
	insert = 'true';
}

function fill_characters() {
	var op = '';
	for (var i = 0; i < chars.length; i++)
		op += '<option value="'+chars[i]['id']+'">'+chars[i]['char_name']+'</option>';
	$('#hq_character').html(op);
}