<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Traffic Flow</title>

  <!-- Lodash -->
  <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.15/lodash.min.js" integrity="sha256-VeNaFBVDhoX3H+gJ37DpT/nTuZTdjYro9yBruHjVmoQ=" crossorigin="anonymous"></script>

  <!-- Axios -->
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>

  <!-- MapBox -->
  <script src='https://api.mapbox.com/mapbox-gl-js/v1.2.0/mapbox-gl.js'></script>
  <link href='https://api.mapbox.com/mapbox-gl-js/v1.2.0/mapbox-gl.css' rel='stylesheet' />

  <!-- Leaflet -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>

  <!-- FontAwesome -->
  <link href="https://use.fontawesome.com/releases/v5.0.13/css/all.css" rel="stylesheet">

  <!-- UTF-8 Library -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/utf8/3.0.0/utf8.min.js"></script>

  <!-- VueJS -->
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

  <!-- Vuetify -->
  <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/@mdi/font@3.x/css/materialdesignicons.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>

  <!-- Vue Multiselect -->
  <script src="https://unpkg.com/vue-multiselect@2.1.0"></script>
  <link rel="stylesheet" href="https://unpkg.com/vue-multiselect@2.1.0/dist/vue-multiselect.min.css">

  <!-- Turfjs -->
  <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>

  <!-- Tensorflow -->
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.0.0/dist/tf.min.js"></script>

  <!-- SCAT Locations Data -->
  <script src="./groups.js"></script>
</head>

<style>
  html,
  body {
    overflow-y: hidden;
    position: relative;
  }

  /* General Tools */
  .top-space {
    margin-top: .5rem;
  }

  /* Major Components */
  .map {
    height: 100%;
    width: 100%;
    z-index: 10;
  }

  .search-box {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 100;

    margin-top: 1rem;
    margin-left: 1rem;
  }

  /* Selects */
  .select {
    width: 25rem;
    background-color: rgba(255, 255, 255, 0.6) !important;

    transition: background-color .1s;
  }

  .select:hover {
    background-color: rgba(255, 255, 255, 1) !important;

    transition: background-color .1s;
  }

  /* Transitions */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity .5s;
  }

  .fade-enter,
  .fade-leave-to

  /* .fade-leave-active below version 2.1.8 */
    {
    opacity: 0;
  }
</style>

<body>
  <div id="app">
    <v-app>
      <div class="map" id="mapid"></div>

      <div class="search-box">
        <div class="multiselect select mb-2">
          <div class="multiselect__tags" style="padding: 8px 0 0 8px !important;">

            <div class="row" style="margin-right: 0 !important; margin-left: 0 !important;">
              <!-- Hour -->
              <div class="col-5" style="padding: 0 !important">
                <input type="number" id="inputHour" placeholder="Hour" class="form-control">
                <!-- <small id="passwordHelpBlock" class="form-text text-muted">Error message here</small> -->
              </div>

              <!-- Minute -->
              <div class="col-5" style="padding: 0 !important">
                <input type="number" id="inputHour" placeholder="Minute" class="form-control">
                <!-- <small id="passwordHelpBlock" class="form-text text-muted">Error message here</small> -->
              </div>

              <!-- AM / PM -->
              <div class="col-2 text-center" style="padding: 0 !important">
                <select class="custom-select my-1 mr-sm-2" style="margin-top: 0 !important; margin-bottom: 0 !important;">
                  <option selected value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <multiselect class="select" v-model="search_origin" label="text" placeholder="From here" :options="to_options" @search-change="GeocodeFrom"></multiselect>

        <transition name="fade">
          <multiselect v-if="search_origin" class="select top-space" v-model="search_destination" label="text" placeholder="To here" :options="from_options" @search-change="GeocodeTo"></multiselect>
        </transition>
      </div>
    </v-app>
  </div>
  <script>
    var userSetIcon = L.icon({
      iconUrl: './assets/red_marker.png',
      iconSize: [36, 41],
      iconAnchor: [18, 41],

      popupAnchor: [-3, -76]
    });

    var paths = [];

    Vue.component('multiselect', window.VueMultiselect.default);

    var app = new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      icons: {
        iconfont: 'fa',
      },
      mounted: function() {
        this.InitialiseMap();
      },
      data: {
        to_options: [],
        from_options: [],

        map: null,

        search_origin: '',
        search_destination: '',
      },
      watch: {
        search_origin: function() {
          var lat = this.search_origin.geometry.coordinates[1];
          var lng = this.search_origin.geometry.coordinates[0];

          // Add Point Marker to map
          L.marker([lat, lng], {
            icon: userSetIcon
          }).addTo(this.map);

          // Link to the closest Marker
          var result = this.FindNearest(lat, lng);

          // Draw line between points
          this.DrawLine([
            [lat, lng],
            [result.nearest.lat, result.nearest.lng]
          ], 'red');
        },
        search_destination: function() {
          var lat = this.search_destination.geometry.coordinates[1];
          var lng = this.search_destination.geometry.coordinates[0];

          // Add Point Marker to map
          L.marker([lat, lng], {
            icon: userSetIcon
          }).addTo(this.map);

          // Link to the closest Marker
          var result = this.FindNearest(lat, lng);

          // Draw line between points
          this.DrawLine([
            [lat, lng],
            [result.nearest.lat, result.nearest.lng]
          ], 'red');
        }
      },
      methods: {
        InitialiseMap: function() {
          this.map = L.map('mapid', {
            zoomControl: false
          }).setView([-37.8136, 144.9631], 10);

          // Initialise Map
          L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.streets',
            accessToken: 'pk.eyJ1IjoiZGFuaWVsZmVyZ3Vzb24iLCJhIjoiY2pzeWhhYmVyMHBneTQ0cXgydXJoeDUxMCJ9.LD82Xcdk-WD3a5TMcvdwEg'
          }).addTo(this.map);

          // Create Markers
          groups.forEach(location => {
            var lat = location['lat'];
            var lng = location['lng'];
            var id = location['scat_id'];

            L.marker([lat, lng]).bindPopup("<b>Scat ID: " + id + "</b>").on('click', this.DrawConnections).addTo(this.map);
          });
        },
        DrawConnections: function(marker) {
          // Remove all current connections
          this.RemoveLines();
          paths = [];

          // Get the object of the selected marker
          var obj = _.find(groups, {
            'lat': marker.latlng.lat.toString(),
            'lng': marker.latlng.lng.toString()
          });

          // Get the objects for the selected markers neighbours
          var neighbour_objs = [];

          obj.neighbours.forEach(neighbour => {

            // Draw a line from the selected marker to the neighbour marker
            var n_obj = _.find(groups, ['scat_id', neighbour]);

            this.DrawLine([
              [obj.lat, obj.lng],
              [n_obj.lat, n_obj.lng]
            ], 'blue');
          });
        },
        FindNearest: function(lat, lng) {
          var points = [];

          // Create array of Turn Points
          groups.forEach(point => {
            points.push(
              turf.point([parseFloat(point.lat), parseFloat(point.lng)])
            );
          });

          var origin_point = turf.point([lat, lng]);

          // Find nearest Point
          var nearest_pos = turf.nearestPoint(origin_point, turf.featureCollection(points));

          // Get the Object for the nearest Point & distance to
          var nearest_obj = groups[nearest_pos.properties.featureIndex];
          var distance_to = nearest_pos.properties.distanceToPoint;

          return {
            'nearest': nearest_obj,
            'distance': distance_to
          };
        },
        CalculateDistance: function(pointOne, pointTwo) {

          var from = turf.point([pointOne[0], pointOne[1]]);
          var to = turf.point([pointTwo[0], pointTwo[1]]);
          var options = {
            units: 'kilometers'
          };

          console.log(from);
          console.log(to);

          return turf.distance(from, to, options);
        },
        DrawLine: function(latlngs, colour) {
          console.log(latlngs);

          var pointOne = [parseFloat(latlngs[0][0]), parseFloat(latlngs[0][1])];
          var pointTwo = [parseFloat(latlngs[1][0]), parseFloat(latlngs[1][1])];

          var l = L.polyline([latlngs], {
            color: colour
          }).bindPopup("Distance: <b>" + this.CalculateDistance(pointOne, pointTwo).toFixed(2) + "kms</b>").addTo(this.map);

          l.openPopup();

          paths.push(l);
        },
        RemoveLines: function() {
          paths.forEach(path => {
            this.map.removeLayer(path);
          });
        },
        GenerateURL: function(query) {
          return "https://api.mapbox.com/geocoding/v5/mapbox.places/" + encodeURI(query) + ".json?access_token=pk.eyJ1IjoiZGFuaWVsZmVyZ3Vzb24iLCJhIjoiY2pzeWhhYmVyMHBneTQ0cXgydXJoeDUxMCJ9.LD82Xcdk-WD3a5TMcvdwEg&country=au";
        },
        GeocodeFrom: function(searchQuery, id) {
          if (searchQuery) {
            axios
              .get(this.GenerateURL(searchQuery))
              .then((response) => {
                this.to_options = response.data.features
              })
              .catch((error) => (console.log(error)))
          }
        },
        GeocodeTo: function(searchQuery, id) {
          if (searchQuery) {
            axios
              .get(this.GenerateURL(searchQuery))
              .then((response) => {
                this.from_options = response.data.features
              })
              .catch((error) => (console.log(error)))
          }
        }
      }
    })
  </script>
</body>

</html>