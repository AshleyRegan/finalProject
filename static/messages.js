var model = {
	messages: ko.observableArray(),

	name: ko.observable(),
	message: ko.observable(),
	createMessage: function() {
		$.post('/msg', {from: model.name, message: model.message});
		model.message('');
	}
};

ko.applyBindings(model);

function updateMessages()
{
	$.getJSON('/msg', function(data) {
		model.messages.removeAll();
		for(var i = 0; i < data.messages.length; i++)
			model.messages.push(data.messages[i]);
	});

	window.setTimeout(updateMessages, 1000);
}
updateMessages();
