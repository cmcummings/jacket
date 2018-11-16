function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

$(function () {
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": getCookie("csrftoken")
		}
	});
});

function update() {
	console.log('xd')
	$.ajax({
		type: 'POST',
		url: '{% url 'get-messages' %}',
		data: {
			'room_key': roomKey
		},
		dataType: 'json',
		success: function(data) {
			messages = data.messages;
		}
	});
}

// this is the id of the form
$("#send-message").submit(function(e) {
	var content = $("#msg-content").val() // Get message contents
	console.log(content)
	$("#msg-content").val('') // Reset text input
	console.log("{% url 'send-message' %}")

	$.ajax({
		type: 'POST',
		url: '{% url 'send-message' %}',
		data: {
			'room_key': roomKey,
			'content': content
		},
		dataType: 'json',
		success: function(data) {
			update()
		},
		failure: function(data) {
			alert('Failed to send message.')
		}
	});
	e.preventDefault();
});
