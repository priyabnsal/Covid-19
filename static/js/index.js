function updateMap() {
  console.log("Updating map with realtime data");

  // https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

  fetch("/static/data.json")
    .then((response) => response.json())
    .then((rsp) => {
      // console.log(rsp.data)
      rsp.data.forEach((element) => {
        latitude = element.latitude;
        longitude = element.longitude;

        cases = element.infected;
        if (cases > 25555555) {
          color = "rgb(255, 0, 0)";
        } else {
          color = `rgb(${cases}, 0, 0)`;
        }

        // Mark on the map
        new mapboxgl.Marker({
          draggable: false,
          color: color,
        })
          .setLngLat([longitude, latitude])
          .addTo(map);
      });
    });
}

let interval = 20000;
setInterval(updateMap, interval);
