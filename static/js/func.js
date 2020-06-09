let map = L.map('map', {
    center: [24.7868518, 120.9972911],
    zoom: 15.5
});


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let coordinate;
let imgURL = location.protocol + "//" + location.host + "/static/img/flood_range.png";
let imgJSON = location.protocol + "//" + location.host + "/static/img/coordinate.json";
let xhr = new XMLHttpRequest();
xhr.open("GET", imgJSON, true);
xhr.send(null);
xhr.onload = () => {

    coordinate = JSON.parse(xhr.responseText);
    let flood = L.imageOverlay(imgURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);;
    let intervalID = setInterval(() => {

        flood.remove();
        let now = new Date();
        let newURL = `${imgURL}?ver=${now.toString().split(" ").join("_")}`;
        flood = L.imageOverlay(newURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);
        console.log(`Update flood range (${now.toString()}) !`);

    }, 5000);

}