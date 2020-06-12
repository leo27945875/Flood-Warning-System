// 放置OSM:
let map = L.map('map', {
    center: [24.7868518, 120.9972911],
    zoom: 15.5
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// AJAX取得各式座標資訊:
let coordinate;
let height;
let imgURL = location.protocol + "//" + location.host + "/static/img/flood_range.png";
let imgJSON = location.protocol + "//" + location.host + "/static/img/coordinate.json";
let heightJSON = location.protocol + "//" + location.host + "/static/img/flood_new_height.json";
let xhr = new XMLHttpRequest();

while (true) {
    try {
        xhr.open("GET", imgJSON, true);
        break;
    } catch (e) {
        console.log(e.message);
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
        popupAnchor: [0, -35]
    });

    let start = L.marker(coordinate["Start"], {
        icon: icon
    }).addTo(map);

    xhr.open("GET", height, true);
    xhr.send(null);
    xhr.onload = () => {
        while (true) {
            try {
                height = JSON.parse(xhr.responseText);
                break;
            } catch (e) {
                console.log(e.message);
                continue;
            }
        }

        height = height["MostNewHeightData"];
        start.bindPopup(`
        <h3 style="text-align:center">Raspberry pi 所在地</h3>
            <p>目前偵測到淹水高度 = 
                <span style="color:red">${height}</span> (cm)
            </p>`);
        start.openPopup();
    };


    // 繪製有地形圖資的範圍:
    let rectangle = L.rectangle([coordinate["UpperLeft"], coordinate["LowwerRight"]], {
        fill: false,
        color: "#333",
        dashArray: [0, 10, 30, 10]
    }).addTo(map);

    // 不斷更新資訊:
    let flood = L.imageOverlay(imgURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);
    let intervalID = setInterval(() => {

        flood.remove();

        let now = new Date();
        let xhr = new XMLHttpRequest();
        let newCoordinateURL = `${imgURL}?ver=${now.toString().split(" ").join("_")}`;
        let newHeightURL = `${heightJSON}?ver=${now.toString().split(" ").join("_")}`;

        // 繪製淹水範圍圖:
        flood = L.imageOverlay(newCoordinateURL, [coordinate["UpperLeft"], coordinate["LowwerRight"]]).addTo(map);

        // 更改Popup內容:

        xhr.open("GET", newHeightURL, true);
        xhr.send(null);
        xhr.onload = () => {
            height = JSON.parse(xhr.responseText);
            height = height["MostNewHeightData"];
            start.bindPopup(`
            <h3 style="text-align:center">Raspberry pi 所在地</h3>
                <p>目前偵測到淹水高度 = 
                    <span style="color:red">${height}</span> (cm)
                </p>`);
        }

        console.log(`Update flood range (${now.toString()}) !`);

    }, coordinate["UpdateTime"] * 1000);
}