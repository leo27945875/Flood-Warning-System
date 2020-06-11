// 放置OSM:
let map = L.map('map', {
    center: [24.7868518, 120.9972911],
    zoom: 15.5
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// AJAX取得各式座標資訊:
let coordinate;
let imgURL = location.protocol + "//" + location.host + "/static/img/flood_range.png";
let imgJSON = location.protocol + "//" + location.host + "/static/img/coordinate.json";
let xhr = new XMLHttpRequest();

while (true) {
    try {
        xhr.open("GET", imgJSON, true);
        break;
    } catch (e) {
        continue;
    }
}

xhr.send(null);
xhr.onload = () => {

    coordinate = JSON.parse(xhr.responseText);

    // 標示Raspberry pi的位置:
    let icon = L.icon({
        iconUrl: "https://image.flaticon.com/icons/svg/1627/1627389.svg",
        iconSize: [40, 40],
        iconAnchor: [20, 40],
        popupAnchor: [0, -30]
    })
    let start = L.marker(coordinate["Start"], {
        icon: icon
    }).addTo(map);
    start.bindPopup("Raspberry pi 所在地。");

    // 繪製有地形圖資的範圍:
    let rectangle = L.rectangle([coordinate["UpperLeft"], coordinate["LowwerRight"]], {
        fill: false,
        color: "#333",
        dashArray: [0, 10, 30, 10]
    }).addTo(map);

    // 繪製淹水範圍圖:
    let flood = L.imageOverlay(imgURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);;
    let intervalID = setInterval(() => {

        flood.remove();
        let now = new Date();
        let newURL = `${imgURL}?ver=${now.toString().split(" ").join("_")}`;
        flood = L.imageOverlay(newURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);
        console.log(`Update flood range (${now.toString()}) !`);

    }, 5000);
}