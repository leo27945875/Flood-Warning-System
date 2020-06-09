let map = L.map('map', {
    center: [24.7868518, 120.9972911],
    zoom: 15.5
});


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let imgURL = "../static/img/flood_range.png";
let imgJSON = "../static/img/coordinate.json";
let coordinate = {
    "UpperLeft": [24.79183338625162, 120.99176139902661],
    "LowwerRight": [24.781595108230306, 121.00279871880039],
    "Start": [24.78960351283472, 120.99715264006558]
}

let icon = L.icon({
    iconUrl: "https://image.flaticon.com/icons/svg/1627/1627389.svg",
    iconSize: [40, 40],
    popupAnchor: [0, -30]
})
let start = L.marker(coordinate["Start"], {
    icon: icon
}).addTo(map);
start.bindPopup("Raspberry pi 所在地。");


let flood = L.imageOverlay(imgURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);;
let intervalID = setInterval(() => {
    flood.remove();
    let now = new Date();
    let newURL = `${imgURL}?ver=${now.toString().split(" ").join("_")}`;
    flood = L.imageOverlay(newURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);
    console.log(`Update flood range (${now.toString()}) !`);
}, 5000);