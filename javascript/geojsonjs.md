# Geojson.js



### API and Example
---

* Generate a point on GeoJson format

```javascript
/*
 * inpt : none
 * retn : point object in geojson format
 */
function GenPointGeojsonFormat()
```

* Generate a line on GeoJson format

```javascript
/*
 * inpt : none
 * retn : line object in geojson format
 */
function GenLineGeojsonFormat()
```

* Generate a polygon on GeoJson format

```javascript
/*
 * inpt : none
 * retn : polygon object in geojson format
 */
function GenPolygonGeojsonFormat()
```

* Generate a featurecollection on GeoJson format

```javascript
/*
 * inpt : none
 * retn : polygon object in geojson format
 */
function GenFeatureCollectionGeojsonFormat()
```

* Generate a point on GeoJson format from properties

```javascript
/*
 * desc : generate a geojson point object
 * getJson: { lat : 23, lon : 112, name : example, ... } 
 * |- necessary : lat, lon
 * |- others : properties 
 */
function genPointObject(getJson)
```

* Parse the google geocode into points on geojson format

```javascript
/*
 * desc : parse the google geocode into geojson   
 */
function parseGoogleGeocode2Geojson(gData)
```

* Transform leaflet point to geojson format

```javascript
/*
 * desc : transform leaflet point to geojson  
 * inpt :
 * |- leafletLayer : leaflet marker object
 * |- otherInfo : additional information written in properties, passed as dictionary format
 */
function LeafletPoint2GeojsonPoint(leafletLayer, otherInfo)
```

* Generate a line-string geojson format from leaflet object 

```javascript
/*
 * desc : generate line string from a leaflet object 
 * inpt :
 * |- startPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- endPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- otherInfo : { "key" : "value" }
 */
function LeafletPoint2GeojsonLine(startPoint, endPoint, otherInfo)
```

* Generate a line-string geojson from a polyline object 

```javascript
/*
 * desc : generate line string from polyline object 
 * inpt :
 * |- startPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- endPoint : { "lat" : 0.0, "lng" : 0.0 }
 * |- otherInfo : { "key" : "value" } 
 */
function LeafletPoint2GeojsonLineFromPolyline(startPoint, endPoint, otherInfo)
```






















