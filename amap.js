/**
 * csv文件解析 
 */
$(document).ready(function () {
    var myItems;

    $.getJSON('data/testData.json', function (data) {
        myItems = data.items;
        console.log(myItems);
    });
});

/**
 * 可视化
 */
var map = new AMap.Map("container", {
    // center: [110.981331, 33.155814],
    zoom: 14,
    viewMode: "2D",
    pitch: 30
});

//贝赛尔曲线经过的起点，途经点，控制点，终点的二维数组
var startPoint = [114.028356, 22.607177];
var endPoint = [116.379064, 39.864462];

var middlePoint = [((startPoint[0] + endPoint[0]) / 2).toFixed(6), ((startPoint[1] + endPoint[1]) / 2).toFixed(6)];
var offset = 15;
var middleBez = [(middlePoint[0] - Math.sqrt(offset)).toFixed(6), (middlePoint[1] - Math.sqrt(offset)).toFixed(6)]
var startBez = [startPoint]; // 起点
var endBez = [middleBez, endPoint]; // 控制点，终点

var path = [
    startBez,
    endBez
];

// 设置了样式索引的点标记数组 json
var data = [{
    lnglat: startPoint,
    title: '深圳北',
    id: 0
}, {
    lnglat: endPoint,
    title: '北京南',
    id: 1
} //, …,{}, …
];

var bezierCurve = new AMap.BezierCurve({
    path: path,
    isOutline: true,
    outlineColor: '#ffeeff',
    borderWeight: 1,
    strokeColor: "#3366FF",
    strokeOpacity: 1,
    strokeWeight: 1,
    // 线样式还支持 'dashed'
    strokeStyle: "solid",
    // strokeStyle是dashed时有效
    strokeDasharray: [10, 10],
    lineJoin: 'round',
    lineCap: 'round',
    zIndex: 50,
    showDir: true
});

// 创建样式对象
var styleMarks = [{
    url: 'img/pin03.png',  // 图标地址
    size: new AMap.Size(20, 20),      // 图标大小
    // rotation:45,
    anchor: new AMap.Pixel(10, 20) // 图标显示位置偏移量，基准点为图标左上角
}];

// 实例化 AMap.MassMarks
var massMarks = new AMap.MassMarks(data, {
    zIndex: 5, 	// 海量点图层叠加的顺序
    zooms: [3, 19],	 // 在指定地图缩放级别范围内展示海量点图层
    // size: new AMap.Size(11, 11),
    // url: '//vdata.amap.com/icons/b18/1/2.png',
    // anchor: new AMap.Pixel(5, 5)
    cursor: 'pointer',
    style: styleMarks 	//多种样式对象的数组
});

// 将数组设置到 massMarks 图层
// massMarks.setData(data);

// 将 massMarks 添加到地图实例
massMarks.setMap(map);
// map.add(massMarks);
map.add(bezierCurve);

map.setFitView([bezierCurve])

map.setMapStyle("amap://styles/whitesmoke");
map.plugin(["AMap.ToolBar", "AMap.Scale", "AMap.Geolocation", "AMap.OverView"],
    function () {
        map.addControl(new AMap.ToolBar());
        map.addControl(new AMap.Scale());
        // map.addControl(new AMap.Geolocation());
        // map.addControl(new AMap.OverView({ isOpen: true }));
    });