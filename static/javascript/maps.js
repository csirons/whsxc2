
function findMaps() {
  var directionsMaps = document.getElementsByClassName('directions-map');
  for (var i = 0; i < directionsMaps.length; i++) {
    loadDirectionsMap(directionsMaps[i]);
  }
  var courseMaps = document.getElementsByClassName('course-map');
  for (var i = 0; i < courseMaps.length; i++) {
    loadCourseMap(courseMaps[i]);
  }
}

function loadDirectionsMap(el) {
  var geocoder = new google.maps.Geocoder();
  var address = el.getAttribute('data-address');
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      el.className += ' sized';
      var name = el.getAttribute('data-name');

      var options = {
        zoom: 12,
        scrollwheel: false,
        center: results[0].geometry.location,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };

      var map = new google.maps.Map(el, options);

      var info = '<div style="text-align: left; line-height: 17px; font-size: 13px; width: 250px;">';
      if (name) info += '<b>'+name+'</b><br><br>';
      info += address + '<br>';
      info += '<a href="http://maps.google.com/?q=to:'+address+'">Click here for directions</a>';
      info += '</div>';
      var infowindow = new google.maps.InfoWindow({
        content: info
      });

      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });

      google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
      });

      infowindow.open(map, marker);
      map.panBy(0, -70);
    }
    else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

function loadCourseMap(el) {
  el.className += ' sized';
  var coords = el.getAttribute('data-route').split(';');
  var bounds = new google.maps.LatLngBounds();
  var maxX = -100000;
  var maxY = -100000;
  var minX = 100000;
  var minY = 100000;
  for (var i = 0; i < coords.length; i++) {
    var parts = coords[i].split(',');
    if (parts[0] > maxX) { maxX = parts[0]; }
    if (parts[0] < minX) { minX = parts[0]; }
    if (parts[1] > maxY) { maxY = parts[1]; }
    if (parts[1] < minY) { minY = parts[1]; }
    coords[i] = new google.maps.LatLng(parts[1], parts[0]);
    bounds.extend(coords[i]);
  }
  console.log('max:', maxX, ',', maxY);
  console.log('min:', minX, ',', minY);

  var route = new google.maps.Polyline({
    path: coords,
    strokeColor: "#0000ec",
    strokeOpacity: 0.7,
    strokeWeight: 3
  });

  var options = {
    zoom: 1,
    scrollwheel: false,
    center: bounds.getCenter(),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  var map = new google.maps.Map(el, options);
  map.fitBounds(bounds);

  route.setMap(map);

  var sib = el.nextSibling.nextSibling;
  if (sib.className == 'course-elevation') {
    sib.className += ' sized';
    var elevator = new google.maps.ElevationService();
    var pathRequest = { path: coords, samples: 200 };
    elevator.getElevationAlongPath(pathRequest, function(results, status) {
      elevationLoaded(sib, results, status);
    });
  }
}

function elevationLoaded(el, results, status) {
  if (status == google.maps.ElevationStatus.OK) {
    var x = [];
    var min = 100000;
    for (var i = 0; i < results.length; i++) {
      x.push(i);
      results[i] = Math.round(results[i].elevation);
      if (results[i] < min) { min = results[i]; }
    }
    var r = Raphael(el);

    var padding = 10;
    var oneK = Math.round((el.clientWidth-padding*2)/5);
    var path = '';
    for (var i = 0; i < 6; i++) {
      path += 'M '+(oneK*(i)+padding)+',0 V 95 ';
    }
    r.path(path).attr({'fill': '#666', 'stroke-width': '0.5'});

    r.g.txtattr.font = "9px 'Helvetica', 'Arial', sans-serif";
    r.g.txtattr.fill = '#666';
    r.g.text(padding+16, 6, "START");
    r.g.text(oneK+padding+8, 6, "1K");
    r.g.text(oneK*2+padding+9, 6, "2K");
    r.g.text(oneK*3+padding+9, 6, "3K");
    r.g.text(oneK*4+padding+8, 6, "4K");
    r.g.text(el.clientWidth-padding-17, 6, "FINISH");

    r.g.linechart(padding, 25, el.clientWidth-padding*2, 70, x, [results], {
      colors: ['#0000ec'],
      shade: 'true',
      smooth: true,
      yrange: 45
    }).hoverColumn(function fin() {
      this.flag = r.g.popup(this.x, this.y[0], (this.values[0] || 0)-min+' ft').insertBefore(this);
    }, function fout() {
      this.flag.remove();
    });
  }
  else {
    console.log('ooops');
    console.log(status);
    console.log(results);
  }
}

document.body.onload = findMaps;
