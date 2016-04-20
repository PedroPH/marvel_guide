function expose_modal(wTitle, wBody) {
	$('#modal_title').html(wTitle);
	$('#modal_body').html(wBody);
	$('#modal_info').modal('show');
}

function close_modal() {
	$('#modal_info').modal('hide');
}