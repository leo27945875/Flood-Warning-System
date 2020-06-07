let map = L.map('map', {
    center: [24.7868518, 120.9972911],
    zoom: 15.5
});


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);