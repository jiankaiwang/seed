var getDictionaryLength = function(getDictObj) {
	var dictLength = 0;
	for (var key in getDictObj) {
			if (getDictObj.hasOwnProperty(key)) {
					dictLength += 1;
			}
	}
	return dictLength;
}