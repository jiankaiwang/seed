/*
 * Generate a Geojson object
 * dependencies
 * |- seed : Common
 */

/*
 * desc : generate point feature in geojson format
 */
function GenPointGeojsonFormat() {
	var point = { 
        "type": "Feature", 
        "geometry": { 
            "type": "Point",
            "coordinates": [0,0] 
        }, 
        "properties": {} 
    };
	
	return point;
}

/*
 * desc : generate line feature in geojson format
 */
function GenLineGeojsonFormat() {
	var line = {
			"type": "Feature",
			"properties": {},
			"geometry": {
				"type": "LineString",
				"coordinates": []
			}
	}
	
	return line;
}

/*
 * desc : generate polygon feature in geojson format
 */
function GenPolygonGeojsonFormat() {
	var polygon = {
			"type": "Feature",
			"properties": {},
			"geometry": {
				"type": "Polygon",
				"coordinates": []
			}
	}
	
	return polygon;
}

/*
 * desc : generate featurecollections in geojson format 
 */
function GenFeatureCollectionGeojsonFormat() {
	var collections = {
			"type": "FeatureCollection",
			"features": []
	};
	
	return collections;
}

/*
 * desc : generate a geojson point object
 * getJson: { lat : 23, lon : 112, name : example, ... } 
 * |- necessary : lat, lon
 * |- others : properties 
 */
function genPointObject(getJson) {
		var allKeys = getDictionaryKeyList(getJson);
		var points = GenPointGeojsonFormat();
		
		for(var i = 0 ; i < allKeys.length; i++) {
			switch(allKeys[i]) {
				case "lon":
					if($.isNumeric(getJson[allKeys[i]])) {
						points["geometry"]["coordinates"][0] = Number(getJson[allKeys[i]]);
					} else {
						points["geometry"]["coordinates"][0] = getJson[allKeys[i]];
					}
					break;
				case "lat":
					if($.isNumeric(getJson[allKeys[i]])) {
						points["geometry"]["coordinates"][1] = Number(getJson[allKeys[i]]);
					} else {
						points["geometry"]["coordinates"][0] = getJson[allKeys[i]];
					}
					break;
				default:
					points["properties"][allKeys[i]] = getJson[allKeys[i]]; 
					break;
			}
		}
		
		return points;
}

/*
 * desc : parse the google geocode into geojson   
 */
function parseGoogleGeocode2Geojson(gData) {
	var allKeys = getDictionaryKeyList(gData);
	var points = GenPointGeojsonFormat();
	
	for(var i = 0 ; i < allKeys.length; i++) {
		switch(allKeys[i]) {
			case "geometry":
				points["geometry"]["coordinates"][0] = Number(gData["geometry"]["location"]["lng"]);
				points["geometry"]["coordinates"][1] = Number(gData["geometry"]["location"]["lat"]);
				points["properties"]["location_type"] = gData["geometry"]["location_type"];
				break;
			case "address_components":
				var getNameComponent = [];
				for(var j = 0 ; j < gData["address_components"].length ; j++) {
					getNameComponent.push(gData["address_components"][j]["short_name"]);
				}
				points["properties"]["address_components"] = getNameComponent.join(", ");
				break;
			case "place_id":
				points["properties"]["place_id"] = gData["place_id"];
				break;
		}
	}
	
	return points;
}

/*
 * desc : transform leaflet point to geojson  
 * inpt :
 * |- leafletLayer : leaflet marker object
 * |- otherInfo : additional information written in properties, passed as dictionary format
 */
function LeafletPoint2GeojsonPoint(leafletLayer, otherInfo) {
	var geojson = GenPointGeojsonFormat();
	
	// set coordinates
	geojson["geometry"]["coordinates"][0] = leafletLayer.getLatLng()["lng"];
	geojson["geometry"]["coordinates"][1] = leafletLayer.getLatLng()["lat"];
	
	// set properties and add others properties
	var keyList = getDictionaryKeyList(otherInfo);
	for(var i = 0 ; i < keyList.length ; i++) {
		geojson["properties"][keyList[i]] = otherInfo[keyList[i]];
	}
	
	return geojson;
}

/*
 * desc : generate line string from a leaflet object 
 * inpt :
 * |- startPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- endPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- otherInfo : { "key" : "value" }
 */
function LeafletPoint2GeojsonLine(startPoint, endPoint, otherInfo) {
	var geojson = GenLineGeojsonFormat();
	
	// set coordinates
	geojson["geometry"]["coordinates"][0] = [startPoint.getLatLng()["lng"], startPoint.getLatLng()["lat"]];
	geojson["geometry"]["coordinates"][1] = [endPoint.getLatLng()["lng"], endPoint.getLatLng()["lat"]];
	
	// set properties and add others properties
	var keyList = getDictionaryKeyList(otherInfo);
	for(var i = 0 ; i < keyList.length ; i++) {
		geojson["properties"][keyList[i]] = otherInfo[keyList[i]];
	}	
	
	return geojson;
}

/*
 * desc : generate line string from polyline object 
 * inpt :
 * |- startPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- endPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- otherInfo : { "key" : "value" }
 */
function LeafletPoint2GeojsonLineFromPolyline(startPoint, endPoint, otherInfo) {
	var geojson = GenLineGeojsonFormat();
	
	// set coordinates
	geojson["geometry"]["coordinates"][0] = [startPoint["lng"], startPoint["lat"]];
	geojson["geometry"]["coordinates"][1] = [endPoint["lng"], endPoint["lat"]];
	
	// set properties and add others properties
	var keyList = getDictionaryKeyList(otherInfo);
	for(var i = 0 ; i < keyList.length ; i++) {
		geojson["properties"][keyList[i]] = otherInfo[keyList[i]];
	}	
	
	return geojson;
}







