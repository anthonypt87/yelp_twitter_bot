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

		var extractedLocation = tweetWithLocation['location'] || 'N/A'

		var tweetElementToAdd = tweetWithLocation['location'] ? $("<div class='tweet-highlight'>") : $("<div class='tweet'>");

		var profileImageUrl = tweet['user']['profile_image_url']
		if (profileImageUrl) {
			tweetElementToAdd.append('<img class="twitter-photo img-rounded" src="' + profileImageUrl + '">');
		}

		var tweetInfoWrapper = $("<div class='tweet-info-wrapper'>");
		var tweetInfo = $("<ul class='tweet-info'>");
		var username = tweet["user"]["screen_name"]
		tweetInfo.append("<li> User: " + username + "</li>");
		tweetInfo.append("<li> Text: " + tweet["text"] + "</li>");
		tweetInfo.append(
			"<li> Location from Tweet: " + locationFromTweet+ "</li>"
		);
		tweetInfo.append(
			"<li>Extracted Location: " + extractedLocation + "</li>"
		);

		if (tweetWithLocation['yelp_url']) {
			tweetInfo.append(
				"<li>Let's Tweet!: @" + username + ' We know just the place: ' + tweetWithLocation['yelp_url'] + "</li>"
			);
		}
		tweetInfoWrapper.append(tweetInfo);
		tweetElementToAdd.append(tweetInfoWrapper);

		while ($(".tweet").length >= 7) {
			var lastChild = $(".tweet:last-child")
			lastChild.fadeOut('slow', function() {
				lastChild.remove()
			});
			sleep(100);
		}
		that.wrapper.prepend(tweetElementToAdd);
	}

	// TODO: pass this in later
	var ws = new WebSocket("ws://localhost:8888/ws");
	ws.onmessage = function(evt) {
		updateData(evt.data);
	};
	ws.onclose = function(evt) {};
	ws.onopen = function(evt) {};
}
