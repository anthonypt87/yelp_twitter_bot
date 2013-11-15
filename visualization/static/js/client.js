function clientSetup(wrapper) {
	this.wrapper = wrapper
}

clientSetup.prototype.setupWebSockets = function(){
	var that = this;

	var updateData = function(rawTweet) {
		var tweetWithLocation = jQuery.parseJSON(rawTweet);
		var tweet = tweetWithLocation["tweet"]


		var locationFromTweet;
		var tweetPlace = tweet["place"];
		if (tweetPlace) {
			locationFromTweet = tweetPlace["full_name"];
		} else {
			locationFromTweet = 'N/A';
		}

		var extractedLocation = tweet['location'] || 'N/A'

		var tweetElementToAdd = $("<div class='tweet'>");

		var profileImageUrl = tweet['user']['profile_image_url']
		if (profileImageUrl) {
			tweetElementToAdd.append('<img class="twitter_photo" src="' + profileImageUrl + '">');
		}
		

		var tweetInfo = $("<div class='tweet_info'>");
		tweetInfo.append("<h2>New Tweet</h2>");
		var tweetInfo = $("<ul>");
		tweetInfo.append("<li> User: " + tweet["user"]["screen_name"] + "</li>");
		tweetInfo.append("<li> Text: " + tweet["text"] + "</li>");
		tweetInfo.append(
			"<li> Location from Tweet: " + locationFromTweet+ "</li>"
		);
		tweetInfo.append(
			"<li>Extracted Location: " + extractedLocation + "</li>"
		);

		tweetElementToAdd.append(tweetInfo);
		that.wrapper.append(tweetElementToAdd);
	}

	// TODO: pass this in later
	var ws = new WebSocket("ws://localhost:8888/ws");
	ws.onmessage = function(evt) {
		updateData(evt.data);
	};
	ws.onclose = function(evt) {};
	ws.onopen = function(evt) {};
}
