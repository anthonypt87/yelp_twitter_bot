/**
 * Script to query Yahoo Placespotter API.
 * Usage:
 *	node placespotter.js CONSUMER_KEY CONSUMER_SECRET QUERY
 */

var args = process.argv.slice(2);
consumerKey = args[0];
consumerSecret = args[1];
placespotterQuery = args[2];

var BossGeoClient = require('bossgeo').BossGeoClient;

var bossGeo = new BossGeoClient(
	consumerKey,
	consumerSecret
);

bossGeo.placespotter({
	documentType: 'text/plain',
	documentContent: placespotterQuery
}, function(err, res) {
	if (err) {
		console.log('error: ' + err);
		return;
	}

	console.log(JSON.stringify(res, null, 4));
});
