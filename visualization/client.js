function clientSetup(wrapper) {
	this.wrapper = wrapper
}

clientSetup.prototype.setupWebSockets = function(){

	var that = this;

	var updateData = function(newTextToAdd) {
		that.wrapper.append("<p>" + newTextToAdd + "</p>");
	}

	var ws = new WebSocket("ws://localhost:8888/ws");

	ws.onmessage = function(evt) {
		updateData(evt.data);
	};
	ws.onclose = function(evt) {};
	ws.onopen = function(evt) {};
}
