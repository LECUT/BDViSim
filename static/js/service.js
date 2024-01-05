Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMGNhYjhkOS00MGE2LTRkMDctOGZiYS1mZjc4MGQ0YmQyZTMiLCJpZCI6OTYzOTEsImlhdCI6MTY1NDQ5MDE5OH0.KMWej-d39eu-JXzFrpUTrc0rxYr0m5WcAriKMPSnqLs'
console.log(Date())

function CesiumTimeFormatter(datetime, viewModel) {
  var julianDT = new Cesium.JulianDate();
  Cesium.JulianDate.addHours(datetime, 8, julianDT);
  var gregorianDT = Cesium.JulianDate.toGregorianDate(julianDT);

  let hour = gregorianDT.hour + "";
  let minute = gregorianDT.minute + "";
  let second = gregorianDT.second + "";
  return `${hour.padStart(2, "0")}:${minute.padStart(2, "0")}:${second.padStart(2, "0")}`;
}

function CesiumDateFormatter(datetime, viewModel, ignoredate) {
  var julianDT = new Cesium.JulianDate();
  Cesium.JulianDate.addHours(datetime, 8, julianDT);
  var gregorianDT = Cesium.JulianDate.toGregorianDate(julianDT);

  return `${gregorianDT.year}年${gregorianDT.month}月${gregorianDT.day}日`;
}

function CesiumDateTimeFormatter(datetime, viewModel, ignoredate) {
  var julianDT = new Cesium.JulianDate();
  Cesium.JulianDate.addHours(datetime, 8, julianDT);
  var gregorianDT = Cesium.JulianDate.toGregorianDate(julianDT);

  let hour = gregorianDT.hour + "";
  let minute = gregorianDT.minute + "";
  return `${gregorianDT.day}日${hour.padStart(2, "0")}:${minute.padStart(2, "0")}`;
}

Cesium.Timeline.prototype.makeLabel = CesiumDateTimeFormatter;
var viewer = new Cesium.Viewer('cesiumContainer', {
  selectionIndicator: false,
  animation: false, 
  shouldAnimate: true,
  fullscreenButton: false, 
  timeline: false, 
  navigationHelpButton: false, 
  infoBox: false, 
  requestRenderMode: true, 
  scene3DOnly: false, 
  sceneMode: 3, 
  contextOptions: {
    webgl: {
      alpha: true,
    }
  },

});
this.viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({
  url: "http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
}))


viewer.clock.shouldAnimate = true;
viewer.clock.multiplier = 900;

viewer.scene.skyBox.show = false 
viewer.scene.backgroundColor = new Cesium.Color(0.0, 0.0, 0.0, 0.0);
viewer.scene.skyAtmosphere.show = false
viewer.scene.moon.show = false
viewer.scene.sun.show = false





function initalize() {

  if (Cesium.FeatureDetection.supportsImageRenderingPixelated()) {
    viewer.resolutionScale = window.devicePixelRatio;
  }
  viewer.scene.fxaa = true;
  viewer.scene.postProcessStages.fxaa.enabled = true;
  viewer.lightColor = new Cesium.Cartesian3(1000, 1000, 1000)
  viewer._cesiumWidget._supportsImageRenderingPixelated = Cesium.FeatureDetection.supportsImageRenderingPixelated();
  viewer._cesiumWidget._forceResize = true;
  if (Cesium.FeatureDetection.supportsImageRenderingPixelated()) {
    var vtxf_dpr = window.devicePixelRatio;
    while (vtxf_dpr >= 2.0) {
      vtxf_dpr /= 2.0;
    }
    //alert(dpr);
    viewer.resolutionScale = vtxf_dpr;
  }



  viewer.clock.onTick.addEventListener(rotate);

}

preTickTime = viewer.clock.currentTime.secondsOfDay;
degreePerSecond = 2 * 3.1415926535 / 86400;
enable = true;

function rotate() {

  if (viewer.scene.mode !== Cesium.SceneMode.SCENE3D || !enable)
    return;


  var now = viewer.clock.currentTime.secondsOfDay;
  var n = now - preTickTime;
  preTickTime = now;

  viewer.scene.camera.rotate(Cesium.Cartesian3.UNIT_Z, degreePerSecond * n);
}

initalize();
viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function (e) {
  e.cancel = true
  viewer.scene.camera.flyTo(homeCameraView);

})
var initialPosition = new Cesium.Cartesian3.fromDegrees(113.42, 10.16, 140000000);
var homeCameraView = {
  destination: initialPosition,
};
var initialPosition2 = new Cesium.Cartesian3.fromDegrees(113.42, 10.16, 30000000);
var CameraView = {
  destination: initialPosition2,
};
viewer.scene.camera.flyTo(CameraView);


var imageryLayers = viewer.scene.imageryLayers;
var tdtAnnoLayer = imageryLayers.addImageryProvider(new Cesium.WebMapTileServiceImageryProvider({
  url: "http://t0.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={TileMatrix}&TILEROW={TileRow}&TILECOL={TileCol}&tk=269b6942f19f345009e605301d0481c2",
  layer: "tdtAnnoLayer",
  style: "default",
  format: "image/jpeg",
  tileMatrixSetID: "GoogleMapsCompatible"
}));


function replace2Chinese(){

	var v0 = document.getElementById('cesiumContainer').getElementsByClassName("cesium-viewer");
	var v1 = v0[0].getElementsByClassName("cesium-viewer-toolbar");
	var v2 = v1[0].getElementsByClassName("cesium-button cesium-toolbar-button cesium-home-button");
    v2[0].title = "复位视图(View Home)";


    v2 = v1[0].getElementsByClassName("cesium-viewer-geocoderContainer");
    
	var v3 = v2[0].getElementsByClassName("cesium-geocoder-input");
	v3[0].title = "输入: 经度,纬度,视点高度(可选)。如：121,31.5,1000";
    v3[0].placeholder = "经度,纬度,高度。如：121,31.5,1000";

}      
replace2Chinese()   

station_info = ''
world_ion = ''
function openwindow() {
  document.getElementById("heatmap").style.display = "block";
  f = $.ajax({
    url: "../static/json/stations.json",
    type: "GET",
    dataType: "json",
    async: false,
    success: function (data) {
    }
  });
  h = $.ajax({
    url: "../static/json/ion_info.json",
    type: "GET",
    dataType: "json",
    async: false,
    success: function (data) {
      console.log(data)
    }
  });
  world_ion = $.parseJSON(h["responseText"]);
  station_info = $.parseJSON(f["responseText"]);

  paintmap();
  startrun();
}
function closewindow(obj) {
  document.getElementById("heatmap").style.display = "none";
  stoprun();
}


f = $.ajax({
  url: "../static/json/stations.json",
  type: "GET",
  dataType: "json",
  async: false,
  success: function (data) {
  }
});
h = $.ajax({
  url: "../static/json/ion_info.json",
  type: "GET",
  dataType: "json",
  async: false,
  success: function (data) {
  }
});
world_ion = $.parseJSON(h["responseText"]);
station_info = $.parseJSON(f["responseText"]);
var nowdate = new Date()
nowdate = (nowdate.setDate(nowdate.getDate() - 1));
nowdate = new Date(nowdate);
var year = nowdate.getFullYear().toString()
var month = (nowdate.getMonth() + 1).toString()
var day = (nowdate.getDate()).toString()
var datepick = document.getElementById("datepick")
var site_datepick = document.getElementById("site_datepick")


if (month < 10) {
  var month1 = '0' + month
}
else {
  var month1 = month
}
if (day < 10) {
  var day1 = '0' + day
}
else {
  var day1 = day
}
filedate = station_info['objtime']
datepick.value = filedate.substr(0, 10)
site_datepick.value = filedate.substr(0, 10)


paintmap();
startrun();

var wion_info = ''
let isDone1 = false;
const calcBtn1 = document.getElementById('setaltbtn');
const modal1 = document.getElementById('modal');
let confirmBtn = document.createElement('button');
calcBtn1.addEventListener('click', () => {
  isDone1 = false;
  modal.innerHTML = '计算中...';
  modal.showModal();
  document.body.style.pointerEvents = 'none';

  var alt = $('#setalt').val();
  var density = $('#density').val();
  var date = $('#datepick').val();
  var satname = satpick()
  stoprun()
  if (alt < 0 || alt >= 90) {
    isDone = true;
    modal.innerHTML = 'Error ! Input range 0-90 °';
    document.body.style.pointerEvents = 'auto';
    
    confirmBtn.textContent = '确认';
    confirmBtn.addEventListener('click', onConfirm);
    modal.appendChild(confirmBtn);
  }
  else {

    var url = '/reset'

    $.post(url, { 'alt': alt, 'density': density, 'date': date, 'satname': JSON.stringify(satname) }, function (res) {
      console.log(res)

      station_info = res;

      $.post('/ion2', { 'date': date }, function (res) {
        if (res == "false") {

          startrun()
          isDone = true;
          modal.innerHTML = date + '缺少ION文件';
          document.body.style.pointerEvents = 'auto';

          
          confirmBtn.textContent = '确认';
          confirmBtn.addEventListener('click', onConfirm);
          modal.appendChild(confirmBtn);
        }
        else {

          console.log(res)
          world_ion = res
          startrun()
          isDone = true;
          modal.innerHTML = '计算完成';
          document.body.style.pointerEvents = 'auto';
    
          
          confirmBtn.textContent = '确认';
    
          confirmBtn.addEventListener('click', onConfirm);
          modal.appendChild(confirmBtn);

        }

      })


    })


  }

});

var lon1 = document.getElementById('leftp').value.split(',')[0].replace('°', '')
var lon2 = document.getElementById('rightp').value.split(',')[0].replace('°', '')
var lat1 = document.getElementById('leftp').value.split(',')[1].replace('°', '')
var lat2 = document.getElementById('rightp').value.split(',')[1].replace('°', '')

function paintmap() {
  var timerange = document.getElementById("timerange").value;

  var timenum = document.getElementById("timenum");
  year = datepick.value.substr(0, 4)
  month = Math.floor(datepick.value.substr(5, 2))
  day = Math.floor(datepick.value.substr(8, 2))
  if (month < 10) {
    var month1 = '0' + month
  }
  else {
    var month1 = month
  }
  if (day < 10) {
    var day1 = '0' + day
  }
  else {
    var day1 = day
  }
  datepick.value = year + '-' + month1 + '-' + day1

  var minute = '00'
  if (timerange < 10) { var hour = '0' + timerange }
  else { var hour = timerange }
  var stime = year + '/' + month + '/' + day + '/' + hour + ':' + minute
  timeid = year + month + day + hour + minute
  timenum.value = stime;
  lon1 = document.getElementById('leftp').value.split(',')[0].replace('°', '')
  lon2 = document.getElementById('rightp').value.split(',')[0].replace('°', '')
  lat1 = document.getElementById('leftp').value.split(',')[1].replace('°', '')
  lat2 = document.getElementById('rightp').value.split(',')[1].replace('°', '')
  paintnums()
  paintGDOP()
  paintPDOP()
  paintHDOP()
  paintVDOP()
  paintTDOP()

  if (!window.world_ion[timeid]) {

  }
  else {
    painionmap()
  }



}

function paintTDOP() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)

  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".TDOP .chart"));
  var str1 = 'TDOP'
  var textname = 'TDOP'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }
  var alt = $('#setalt').val();



  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [
        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",
          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°W'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°E'
            }
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );


  // })
}
function paintVDOP() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".VDOP .chart"));
  var str1 = 'VDOP'
  var textname = 'VDOP'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }

  var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [


        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",
          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°W'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°E'
            }
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );

  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
function paintHDOP() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".HDOP .chart"));
  var str1 = 'HDOP'
  var textname = 'HDOP'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }

  var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [


        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",
          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°W'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°E'
            }
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );


  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
function paintPDOP() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".PDOP .chart"));
  var str1 = 'PDOP'
  var textname = 'PDOP'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }

  var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [


        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",
          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°W'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°E'
            }
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );

  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
function paintGDOP() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".GDOP .chart"));
  var str1 = 'GDOP'
  var textname = 'GDOP'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }
  // console.log(lat,lon)
  var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [


        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",
          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°W'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°E'
            }
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );

  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
function paintnums() {
  var vmin = 10;
  var vmax = 2;
  var density = $('#density').val();
  density = Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".num .chart"));
  var str1 = 'counts'
  var textname = '卫星可见数目'
  var zz = 0
  for (var c in station_info) {
    for (var t in station_info[c]) {
      if (!window.station_info[c][t]) {
        // console.log(c)
        break
      }
      var i = station_info[c][t][str1]
      if (vmax < i) {
        if (i - vmax > 10) { continue }
        vmax = Math.ceil(i)
      }
      if (vmin > i) {
        vmin = Math.floor(i)
      }
    }
  }

  var data1 = []
  var k = 0
  var z = bd - 1
  var jj = 90
  for (var i = 0; i < bd; i++) {
    var zz = -180

    for (var j = 0; j < ld; j++) {

      if (!window.station_info[k][timeid][str1] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {

        data1.push([j, z, NaN])
      }
      else {
        data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])
      }
      k += 1
      zz = zz + density

    }
    z = z - 1
    jj -= density
  }
  var lon = []
  d = -180
  for (var i = 0; i < ld; i++) {
    lon.push(d)
    d = d + density
  }
  var lat = []
  d = 90
  for (var i = 0; i < bd; i++) {
    lat.push(d)
    d = d - density
  }

  // console.log(Math.floor((lon.length-1)/2-2)/2)
  var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname + '(elevation>' + alt + '°)',

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * density
          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * density
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [


        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      // ['180°W','120°W','60°W','0','60°E','120°E','180°E']
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",

          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value
            // if (listData < 0) {
            //   listData = Math.abs(listData) + '°W'
            // }
            // else if (listData == 0) {
            //   listData = Math.abs(listData) + '°'
            // }
            // else if (listData > 0) {
            //   listData = Math.abs(listData) + '°E'
            // }

            if (value == -180) {
              listData = '180°W'
              // console.log(listData)
            }
            else if (value == -90) {

              listData = '90°W'
              // console.log(listData)
            }
            else if (value == 0) {
              listData = '0°'
            }
            else if (value == 90) {
              listData = '90°E'
            }
            else if (value == 180) {
              listData = '180°E'
            }
            else {
              listData = ''
            }
            // console.log(listData)
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: vmin,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );

  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
function painionmap() {
  var vmin = 10;
  var vmax = 2;
  // var density=$('#density').val();
  // density=Math.floor(density)
  var bd = 180 / density + 1
  var ld = 360 / density + 1
  var heatmap1 = echarts.init(document.querySelector(".ionmap .chart"));

  // var str1 = 'counts'
  var textname = '电离层电子含量'
  var zz = 0
  // for (var c in world_ion) {
  for (var k in world_ion[timeid]) {
    if (!window.world_ion[timeid][k]) {
      // console.log(c)
      break
    }
    var i = world_ion[timeid][k]
    if (vmax < i) {
      if (i - vmax > 10) { continue }
      vmax = Math.ceil(i)
    }
    if (vmin > i) {
      vmin = Math.floor(i)
    }
  }


  //  }

  var data1 = []
  var k = 0
  var z = 36
  var jj = 90
  for (var i = 0; i < 37; i++) {
    var zz = -180
    for (var j = 0; j < 73; j++) {
      if (i == 0) {
        data1.push([j, z, NaN])
      }
      else {
        if (!window.world_ion[timeid][k] || zz < lon1 || zz > lon2 || jj < lat2 || jj > lat1) {
          data1.push([j, z, NaN])
        }
        else {
          data1.push([j, z, parseFloat(world_ion[timeid][k]).toFixed(2)])
        }
        k += 1
      }

      zz = zz + 5
      // console.log(k,timeid,str1)
      // data1.push([j, z, station_info[k][timeid][str1].toFixed(2)])

    }
    // console.log(k)
    z = z - 1
    jj -= 5
  }
  var lon = []
  d = -180
  for (var i = 0; i < 73; i++) {
    lon.push(d)
    d = d + 5
  }
  var lat = []
  d = 90
  for (var i = 0; i < 37; i++) {
    lat.push(d)
    d = d - 5
  }

  // console.log(Math.floor((lon.length-1)/2-2)/2)
  // var alt = $('#setalt').val();





  heatmap1.setOption(
    (option = {
      grid: {
        top: "13%",
        // left: "%",
        right: "5.5%",
        bottom: "3%",
        show: true,
        borderColor: "#012f4a",
        containLabel: true,
        width: '90%',
        height: '80%'
      },
      title: {
        show: false,
        top: 3,
        left: 'center',

        textStyle: {

          color: 'white',

          fontStyle: 'normal',

          fontWeight: 'bold',

          fontFamily: 'sans-serif',
          
          fontSize: 5
        },

        text: textname,

      },
      tooltip: {
        position: 'top',
        formatter: (value) => { 
          var obj = value
          var name = obj.seriesName
          var y = obj.value[1]
          y = 90 - y * 5

          if (y < 0) {
            y = Math.abs(y) + '°N'
          }
          else if (y == 0) {
            y = Math.abs(y) + '°'
          }
          else if (y > 0) {
            y = Math.abs(y) + '°S'
          }
          var x = obj.value[0]
          x = -180 + x * 5
          if (x < 0) {
            x = Math.abs(x) + '°W'
          }
          else if (x == 0) {
            x = Math.abs(x) + '°'
          }
          else if (x > 0) {
            x = Math.abs(x) + '°E'
          }
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
          content = name + "</br>" + p + x + ',' + y + ': ' + obj.value[2]
          return content
        }
      },
      series: [

        {
          name: textname,
          type: 'heatmap',
          data: data1,
          emphasis: {
            itemStyle: {
              borderColor: '#333',
              borderWidth: 1,
            }
          },
          itemStyle: {
            opacity: 0.8,
          },
        },

      ],
      // ['180°W','120°W','60°W','0','60°E','120°E','180°E']
      xAxis: {
        name: 'Longitude',
        nameTextStyle: {
          color: 'white',
          padding: [3, 0, 0, 0]
        },
        nameLocation: 'center',
        data: lon,
        axisTick: {
          show: false  
        },

        axisLabel: {
          color: "white",

          interval: (Math.floor((lon.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 
            var listData = value

            if (value == -180) {
              listData = '180°W'
              // console.log(listData)
            }
            else if (value == -90) {

              listData = '90°W'
              // console.log(listData)
            }
            else if (value == 0) {
              listData = '0°'
            }
            else if (value == 90) {
              listData = '90°E'
            }
            else if (value == 180) {
              listData = '180°E'
            }
            else {
              listData = ''
            }
            // console.log(listData)
            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        },
      },

      yAxis: {

        name: 'Latitude',
        nameTextStyle: {
          color: 'white',
          padding: [0, 0, 15, 0]
        },
        nameLocation: 'center',
        left: 0,
        data: lat,
        axisTick: {
          show: false  
        },
        axisLabel: {
          color: "white",
          interval: (Math.floor((lat.length - 1) / 2 - 2) / 2),
          textStyle: {
            fontSize: 9
          },
          formatter: (value) => { 

            var listData = value
            if (listData < 0) {
              listData = Math.abs(listData) + '°N'
            }
            else if (listData == 0) {
              listData = Math.abs(listData) + '°'
            }
            else if (listData > 0) {
              listData = Math.abs(listData) + '°S'
            }

            return listData
          }
        },
        axisLine: {

          lineStyle: {
            color: 'white',  
          },
        }

      },
      visualMap: {

        itemWidth: 10,
        itemHeight: 60,
        min: 0,
        max: vmax,
        calculable: true,
        textStyle: {
          color: 'white'
        },
        orient: 'horizontal',
        top: 0,
        left: 'center',
        realtime: false,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      }
    })
  );

  window.addEventListener('resize', function () {
    heatmap1.resize()
  })
}
var satSource = ''
function choosepoint() {
  viewer.scene.mode = Cesium.SceneMode.SCENE2D
  viewer.dataSources.remove(satSource);
  viewer._container.style.cursor = "crosshair";
  // document.getElementById("pickstation_bar").style.display = 'none';

  var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction(function (event) {

    var ellipsoid = viewer.scene.globe.ellipsoid;
    var cartesian = viewer.camera.pickEllipsoid(event.position, ellipsoid);

    var cartographic = Cesium.Cartographic.fromCartesian(cartesian);

    var lon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(3);
    var lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(3);
    var height = Math.ceil(this.viewer.camera.positionCartographic.height);
    var height = 0
    var height1 = viewer.scene.globe.getHeight(cartographic);
    var height2 = cartographic.height;

    alert(lon + ' , ' + lat)
    document.getElementById("site_lon").value = lon
    document.getElementById("site_lat").value = lat

    handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)
    alert('完成选点')
    viewer._container.style.cursor = "auto";


  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)

}
function setstation() {
  var name = document.getElementById("satname").value
  var position = [document.getElementById("lontext").value, document.getElementById("lattext").value, 0]
  var stationczmlFile = [{
    "id": "document",
    "name": "CZML Point",
    "version": "1.0"
  }, {
    "id": name,
    "name": name,
    "label": {

      "font": "6pt Lucida Console",
      "outlineWidth": 2,
      "outlineColor": { "rgba": [255, 0, 0, 255] },
      "horizontalOrigin": "LEFT",
      "pixelOffset": { "cartesian2": [12, 0] },
      "fillColor": { "rgba": [213, 255, 0, 255] },
      "text": name
    },
    "billboard": {
      "image": { "uri": "../static/images/station.png" },
      "scale": 0.1
    },
    "position": {
      "cartographicDegrees": position
    },
  }
  ];
  satSource = new Cesium.CzmlDataSource(stationczmlFile);
  satSource.load(stationczmlFile);
  viewer.dataSources.add(satSource);
  viewer._container.style.cursor = "default";
}


function picktypediv() {
  id = $("input[name='picktype']:checked").val();

  if (id == 'World') {

    stoprun2()
    viewer.dataSources.removeAll()
    document.getElementsByClassName("world")[0].style.display = 'block';
    document.getElementsByClassName("world")[1].style.display = 'block';
    document.getElementsByClassName("world")[2].style.display = 'block';
    document.getElementById("world_set").style.display = 'block';
    document.getElementsByClassName("onesat")[0].style.display = 'none';
    document.getElementsByClassName("onesat")[1].style.display = 'none';
    document.getElementsByClassName("onesat")[2].style.display = 'none';
    document.getElementById("onesat_set").style.display = 'none';
    document.getElementById("areabox").style.display = 'block';
    document.getElementById("areabtn").style.display = 'block';
    document.getElementById("sitebox").style.display = 'none';
    document.getElementById("sitebtn").style.display = 'none';
    document.getElementById("pickareabtn").style.display = 'none';
    document.getElementById("site_snums").style.display = 'none';
    document.getElementById('leftp').value = '-180°,90°'
    document.getElementById('rightp').value = '180°,-90°'
    document.getElementById("leftp").disabled = true;
    document.getElementById("rightp").disabled = true;
    startrun();
    if (rectangleEntity) {
      viewer.entities.remove(rectangleEntity);
    }
  }
  if (id == 'area') {

    stoprun2()
    viewer.dataSources.removeAll()
    document.getElementsByClassName("world")[0].style.display = 'block';
    document.getElementsByClassName("world")[1].style.display = 'block';
    document.getElementsByClassName("world")[2].style.display = 'block';
    document.getElementById("world_set").style.display = 'block';
    document.getElementsByClassName("onesat")[0].style.display = 'none';
    document.getElementsByClassName("onesat")[1].style.display = 'none';
    document.getElementsByClassName("onesat")[2].style.display = 'none';
    document.getElementById("onesat_set").style.display = 'none';
    document.getElementById("areabox").style.display = 'block';
    document.getElementById("areabtn").style.display = 'block';
    document.getElementById("pickareabtn").style.display = 'inline';
    document.getElementById("sitebox").style.display = 'none';
    document.getElementById("sitebtn").style.display = 'none';
    document.getElementById("site_snums").style.display = 'none';
    document.getElementById("leftp").disabled = false;
    document.getElementById("rightp").disabled = false;
    startSelection()
    // setarea()
  }
  if (id == 'onesat') {
    // startrun2();
    stoprun();
    if (rectangleEntity) {
      viewer.entities.remove(rectangleEntity);
    }
    document.getElementById('panel').style.display = 'block'
    document.getElementById('openbar').style.display = 'none'
    document.getElementById('panel').style.display == 'block'
    document.getElementById('openbar').style.display == 'none'
    document.getElementsByClassName("onesat")[0].style.display = 'block';
    document.getElementsByClassName("onesat")[1].style.display = 'block';
    document.getElementsByClassName("onesat")[2].style.display = 'block';
    document.getElementById("onesat_set").style.display = 'block';
    document.getElementById("site_snums").style.display = 'block';
    // document.getElementById("onesat_panel").style.display = 'block';

    document.getElementsByClassName("world")[0].style.display = 'none';
    document.getElementsByClassName("world")[1].style.display = 'none';
    document.getElementsByClassName("world")[2].style.display = 'none';
    document.getElementById("world_set").style.display = 'none';
    document.getElementById("areabox").style.display = 'none';
    document.getElementById("areabtn").style.display = 'none';
    document.getElementById("sitebox").style.display = 'block';
    document.getElementById("sitebtn").style.display = 'block';
  }
}
function closesetdiv() {
  document.getElementById("pickstation_bar").style.display = 'none';
}

station = []
ion_info = {}
satczml = {}
satSource1 = {}

let isDone = false;
const calcBtn = document.getElementById('setbtn');
const modal = document.getElementById('modal');

calcBtn.addEventListener('click', () => {
  isDone = false;
  modal.innerHTML = '计算中...';
  modal.showModal();

  document.body.style.pointerEvents = 'none';

  var timeid = year + month + day + '00' + '00'

  var alt = $('#site_alt').val();
  var lon = $('#site_lon').val();
  var lat = $('#site_lat').val();
  var siteheight = $('#site_h').val();
  var date = $('#site_datepick').val();
  var pickp = $('#pickp').val();
  // var url = $('#urlpick').val();
  // alert(url)
  // var url = '/paintchart'
  var satname = satpick()
  // console.log(pickp)
  var name = document.getElementById("site_name").value

  if (alt < 0 || alt > 90 || alt == '') {
    // alert('Error ! Input range 0-90 °')
    isDone = true;
    modal.innerHTML = 'Error ! Input range 0-90 °';
    document.body.style.pointerEvents = 'auto';

    
    confirmBtn.textContent = '确认';

    confirmBtn.addEventListener('click', onConfirm);
    modal.appendChild(confirmBtn);
  }
  else {
  
    var url = '/rinexpaint'
    // var url = '/paintchart'

    $.post(url, { 'alt': alt, 'height': siteheight, 'lon': lon, 'lat': lat, 'date': date, 'satname': JSON.stringify(satname), 'pickp': pickp }, function (res) {
      if (res == "false") {
        
        isDone = true;
        modal.innerHTML = date + '缺少星历文件';
        document.body.style.pointerEvents = 'auto';
    
        
        confirmBtn.textContent = '确认';

        confirmBtn.addEventListener('click', onConfirm);
        modal.appendChild(confirmBtn);
      }
      else {
        station = res;
        var infochart = echarts.init(document.querySelector(".distribution_map .chart"));
        infochart.clear();
        paintmap2();
        var url2 = '/ion'
        $.post(url2, { 'lon': lon, 'lat': lat, 'date': date }, function (res) {
          if (res == "false") {
            alert(date + '缺少电离层文件')
            var infochart = echarts.init(document.querySelector(".ionosphereInfo .chart"));
            infochart.clear();
          }
          else {
            ion_info = res

            painionosphereInfo(ion_info)
          }
        })
        $.post('/satnumsv2', { 'lon': lon, 'lat': lat, 'height': siteheight, 'name': name, 'alt': alt, 'satname': JSON.stringify(satname), 'date': date }, function (res) {
          satczml = res[0]
          viewer.dataSources.removeAll()
          satSource1 = new Cesium.CzmlDataSource(satczml);
          viewer.scene.mode = Cesium.SceneMode.SCENE3D

          satSource1.load(satczml);
          viewer.dataSources.add(satSource1);
          viewer._container.style.cursor = "default";
          div = document.getElementById('heatmap')

          viewer.scene.camera.flyTo(homeCameraView);
        })

        isDone = true;
        modal.innerHTML = '计算完成';
        document.body.style.pointerEvents = 'auto';
    
        
        confirmBtn.textContent = '确认';

        confirmBtn.addEventListener('click', onConfirm);
        modal.appendChild(confirmBtn);
      }

    })



    switchbar()
  }
});
function onConfirm() {
  modal.close();
  modal.removeChild(confirmBtn);
}
function switchlabel() {
  var sat = satSource1.entities.values
  for (var i in sat) {
    if (sat[i].label == undefined) {
      continue
    }
    else {
      if (sat[i].label.show == false) {
        sat[i].label.show = true;
      }
      else {
        sat[i].label.show = false;

      }
    }
  }

}

xdata = []
function paintmap2() {


  var timenum = document.getElementById("timenum2");
  // console.log(datepick.value)
  year = site_datepick.value.substr(0, 4)
  month = Math.floor(site_datepick.value.substr(5, 2))
  day = Math.floor(site_datepick.value.substr(8, 2))
  // console.log(year,month,day)
  if (month < 10) {
    var month1 = '0' + month
  }
  else {
    var month1 = month
  }
  if (day < 10) {
    var day1 = '0' + day
  }
  else {
    var day1 = day
  }
  site_datepick.value = year + '-' + month1 + '-' + day1

  var minute = '00'
  if (timerange < 10) { var hour = '0' + timerange }
  else { var hour = timerange }
  var stime = year + '/' + month + '/' + day + '/' + hour + ':' + minute
  timeid = year + month + day + hour + minute
  timenum.value = stime;

  id = $("input[name='types2']:checked").val();

  xdata = []
  for (var i in station) {
    xdata.push(station[i]['time'].slice(11, 16))
  }

  var sat = {}
  for (var i = 1; i < 63; i++) {

    if (i < 10) {
      i = "0" + i
    }
    sat["C" + i] = {}
    sat["C" + i]['AH'] = []
    sat["C" + i]['hH'] = []
  }
  for (var i in sat) {
    for (var j = 0; j < 96; j++) {
      sat[i]['AH'][j] = 0
      sat[i]['hH'][j] = 0

    }
  }
  var xlabel = {}


  painalt(sat, xdata, xlabel)
  painnums(xdata)
  painDOP(xdata)
  var infochart = echarts.init(document.querySelector(".distribution_map .chart"));
  infochart.clear();
  painvisibility(sat, xdata)
  painAccuracy(xdata)
  c2 = 0
  startrun2()
}

function painalt(sat, xdata) {
  var infochart = echarts.init(document.querySelector(".alt .chart"));
  infochart.clear();
  var seriesdata = []
  var textname = '卫星高度角'
  var n = 0
  for (var i in station) {
    for (var j in station[i]['visibility']) {
      sat[j]['hH'][n] = station[i]['visibility'][j][0]
    }
    for (var i in sat) {
      if (sat[i]['hH'][n] == 0) {
        sat[i]['hH'][n] = null;
      }
    }
    n += 1
  }

  for (var i in sat) {
    var z = 0
    for (var j in sat[i]['hH']) {
      if (sat[i]['hH'][j] != null) { z += 1 }

    }
    if (z == 0) {

      delete sat[i]
    }
  }
  var s = {}
  for (var i in sat) {
    s = {
      name: i,
      type: 'line',
      data: sat[i]['hH'],

      symbol: 'rect',
    }
    seriesdata.push(s)

  }

  var tooltipdata = {
    formatter: (value) => { 
      var obj = value
      var time = obj.name
      var title = year + '/' + month + '/' + day + '/' + time
      var name = obj.seriesName


      var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
      content = title + "</br>" + p + name + ': ' + obj.data.toFixed(2) + '°'
      return content
    }
  }
  var ydata = {
    name: '高度角',
    nameLocation: "center",
    nameTextStyle: {
      fontSize: 16,
      padding: 15,
      color: 'white'
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed',
      }
    },
    axisLine: {
      lineStyle: {
        color: 'white',  
      },
    },
    axisLabel: {
      color: "white",
      formatter: (value) => {
        return value + '°';
      }
    }

  }
  var grid1 = {
    top: "7%",
    // left: "%",
    right: "5.5%",
    bottom: "3%",
    show: true,
    borderColor: "#012f4a",
    containLabel: true,
    width: '90%',
    height: '80%'
  }
  option = {
    title: {
      show: false,
      left: 'center',
      textStyle: {

        color: 'white',

        fontStyle: 'normal',

        fontWeight: 'bold',

        fontFamily: 'sans-serif',
        
        fontSize: 18
      },
      text: textname,
    },
    grid: grid1,
    tooltip: tooltipdata,
    legend: {
      show: false
    },
    xAxis: {
      name: '时间',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',  
        },
      },
    },
    yAxis: ydata,
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 4,
        lineStyle: {
          width: 4
        }
      }
    })
  })
  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 2,
        lineStyle: {
          width: 2
        }
      }
    })
  })
  window.addEventListener('resize', function () {
    infochart.resize()
  })

}
function painnums(xdata) {

  var infochart = echarts.init(document.querySelector(".nums .chart"));
  infochart.clear();

  var textname = '卫星可见数'
  var seriesdata = []
  var sdata = []
  for (var i in station) {
    sdata.push(station[i]['counts'])
  }
  var s = {
    type: 'line',
    data: sdata,
    areaStyle: {}
  }
  seriesdata.push(s)
  var tooltipdata = {
    formatter: (value) => { 
      var obj = value[0]
      var time = obj.name
      var title = year + '/' + month + '/' + day + '/' + time


      var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
      content = title + "</br>" + p + '可见卫星数: ' + obj.data
      return content
    },
    trigger: 'axis',
    showSymbol: false,
  }
  var ydata = {
    name: '可见卫星数',
    nameLocation: "center",
    nameTextStyle: {
      fontSize: 16,
      padding: 15,
      color: 'white'
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed',
      }
    },
    axisLine: {
      lineStyle: {
        color: 'white',  
      },
    },
    axisLabel: {
      color: "white",
    }
  }

  option = {
    title: {
      show: false,
      left: 'center',
      textStyle: {

        color: 'white',

        fontStyle: 'normal',

        fontWeight: 'bold',

        fontFamily: 'sans-serif',
        
        fontSize: 18
      },
      text: textname,
    },
    grid: {
      top: "7%",
      // left: "%",
      right: "3%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true,
      width: '90%',
      height: '80%'
    },
    tooltip: tooltipdata,
    legend: {
      show: false

    },
    xAxis: {
      name: '时间',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',  
        },
      },
    },
    yAxis: ydata,
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 4,
        lineStyle: {
          width: 4
        }
      }
    })
  })
  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 2,
        lineStyle: {
          width: 2
        }
      }
    })
  })
  window.addEventListener('resize', function () {
    infochart.resize()
  })
}
function painDOP(xdata) {
  console.log(station)
  var infochart = echarts.init(document.querySelector(".DOP .chart"));
  infochart.clear();
  var textname = 'DOP值'

  var seriesdata = []
  var GDOPdata = []
  var HDOPdata = []
  var PDOPdata = []
  var TDOPdata = []
  var VDOPdata = []
  for (var i in station) {
    GDOPdata.push(station[i]['GDOP'])
    PDOPdata.push(station[i]['PDOP'])
    HDOPdata.push(station[i]['HDOP'])
    VDOPdata.push(station[i]['VDOP'])
    TDOPdata.push(station[i]['TDOP'])
  }
  var ymax = 0
  var ymin = 1
  for (var i in GDOPdata) {
    if (GDOPdata[i] >= 10) {
      GDOPdata[i] = NaN
    }
    if (HDOPdata[i] >= 10) {
      HDOPdata[i] = NaN
    }
    if (PDOPdata[i] >= 10) {
      PDOPdata[i] = NaN
    }
    if (TDOPdata[i] >= 10) {
      TDOPdata[i] = NaN
    }
    if (VDOPdata[i] >= 10) {
      VDOPdata[i] = NaN
    }
  }

  var s1 = {
    name: 'GDOP(几何)',
    type: 'line',
    symbol: 'rect',
    data: GDOPdata,

  }
  seriesdata.push(s1)
  var s2 = {
    name: 'HDOP(水平)',
    type: 'line',
    data: HDOPdata,
    symbol: 'diamond',

  }
  seriesdata.push(s2)
  var s3 = {
    name: 'PDOP(位置)',
    type: 'line',
    data: PDOPdata,
    symbol: 'arrow',

  }
  seriesdata.push(s3)
  var s4 = {
    name: 'TDOP(时间)',
    type: 'line',
    data: TDOPdata,
    symbol: 'triangle',

  }
  seriesdata.push(s4)
  var s5 = {
    name: 'VDOP(垂直)',
    type: 'line',
    data: VDOPdata,
    symbol: 'circle',


  }
  seriesdata.push(s5)
  var tooltipdata = {
    formatter: (value) => {
      var GDOP = value[0]
      var PDOP = value[1]
      var HDOP = value[2]
      var VDOP = value[3]
      var TDOP = value[4]
      var time = GDOP.name
      var title = year + '/' + month + '/' + day + '/' + time
      var p1 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + GDOP.color + '"></span>'
      var p2 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + PDOP.color + '"></span>'
      var p3 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + HDOP.color + '"></span>'
      var p4 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + VDOP.color + '"></span>'
      var p5 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + TDOP.color + '"></span>'
      content = title + "</br>" + p1 + GDOP.seriesName + ': ' + GDOP.data.toFixed(2)
        + "</br>" + p2 + PDOP.seriesName + ': ' + PDOP.data.toFixed(2)
        + "</br>" + p3 + HDOP.seriesName + ': ' + HDOP.data.toFixed(2)
        + "</br>" + p4 + VDOP.seriesName + ': ' + VDOP.data.toFixed(2)
        + "</br>" + p5 + TDOP.seriesName + ': ' + TDOP.data.toFixed(2)
      return content
    },
    trigger: 'axis',
  }
  var ydata = {
    name: '精度因子的值',
    nameLocation: "center",
    nameTextStyle: {
      fontSize: 16,
      padding: 15,
      color: 'white'
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed',
      }
    },
    axisLine: {
      lineStyle: {
        color: 'white',  
      },
    },
    axisLabel: {
      color: "white",

    },
    scale: true


  }

  option = {
    color: ['#9370DB', '#87CEFA', '#90EE90', '#FF4500', '#FF1493'],
    title: {
      show: false,
      left: 'center',
      textStyle: {
        color: 'white',
        fontStyle: 'normal',
        fontWeight: 'bold',
        fontFamily: 'sans-serif',
        fontSize: 18
      },
      text: textname,
    },
    grid: {
      top: "7%",
      // left: "7%",
      right: "3%%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true,
      width: '90%',
      height: '80%'
    },
    tooltip: tooltipdata,
    legend: {
      show: false

    },
    xAxis: {
      name: '时间',
      scale: true,
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',
        },
      },
    },
    yAxis: ydata,
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 4,
        lineStyle: {
          width: 4
        }
      }
    })
  })
  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 2,
        lineStyle: {
          width: 2
        }
      }
    })
  })
  window.addEventListener('resize', function () {
    infochart.resize()
  })
}
function painvisibility(sat, xdata) {
  var infochart = echarts.init(document.querySelector(".visibility .chart"));
  infochart.clear();
  var textname = '可见性'

  var seriesdata = []
  var sdata = []
  var n = 0
  for (var i in station) {
    for (var j in station[i]['visibility']) {
      sat[j]['hH'][n] = station[i]['visibility'][j][0]
    }
    for (var i in sat) {
      if (sat[i]['hH'][n] == 0) {
        sat[i]['hH'][n] = null;
      }
    }
    n += 1
  }
  var zz = 1

  for (var i in sat) {
    var z = 0

    for (var j in sat[i]['hH']) {
      if (sat[i]['hH'][j] != null) {
        z += 1
        sat[i]['hH'][j] = zz
      }

    }
    if (z == 0) { delete sat[i] }
    zz += 1
  }
  // console.log(sat)
  for (var i in sat) {



    var s = {
      name: i,
      type: 'line',
      data: sat[i]['hH'],
      symbolSize: 8,
      symbol: 'line',
      itemStyle: {
        normal: {
          lineStyle: {
            width: 4
          }
        },
        showSymbol: false,
        hoverAnimation: false
      }
    }
    seriesdata.push(s)

  }
  // console.log(s)
  var tooltipdata = {
    formatter: (value) => { 
      // console.log(value)
      var obj = value[0]

      var time = obj.name
      var title = year + '/' + month + '/' + day + '/' + time
      var content = ''
      content = title + "</br>"
      var n = 0
      for (var i = 0; i < value.length; i++) {
        if (value[i].value != undefined) {
          var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + value[i].color + '"></span>'
          content = content + p + value[i].seriesName + ' '
          n += 1
        }


        if (n == 5) {
          content = content + "</br>"
          n = 0
        }
      }


      return content
    },
    trigger: 'axis',
    showSymbol: false,
    axisPointer: {
      animation: false,
      snap: true
    },
    enterable: true

  }
  var ydata = {
    name: '卫星',
    max: 47,
    nameLocation: "center",
    nameTextStyle: {
      fontSize: 16,
      padding: 15,
      color: 'white'
    },
    splitLine: {
      show: false,
      lineStyle: {
        type: 'dashed',
      }
    },
    // minInterval: 1,
    interval: 5,
    axisLabel: {
      color: 'white',
      textStyle: { fontSize: 8 },
      formatter: function (value) {
        if(value==0){
          value='C01'
        }
        else if(value==50){
          value=''
        }
        else{
          for(var i in sat){
            var name=i
            if(sat[i]['hH'].includes(value)){
              value=name
            }
          }
        }
        console.log(value)
        return value;
      }
    },
    axisLine: {
      lineStyle: {
        color: 'white',  
      },
    }


  }

  option = {
    title: {
      show: false,
      left: 'center',
      textStyle: {

        color: 'white',

        fontStyle: 'normal',

        fontWeight: 'bold',

        fontFamily: 'sans-serif',
        
        fontSize: 18
      },
      text: textname,
    },
    grid: {
      top: "7%",
      // left: "%",
      right: "3%%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true,
      width: '90%',
      height: '80%'
    },
    tooltip: tooltipdata,
    legend: {
      show: false

    },
    xAxis: {
      name: '时间',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',  
        },
      },
    },
    yAxis: ydata,
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 5,
        lineStyle: {
          width: 5
        }
      }
    })
  })

  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 8,
        lineStyle: {
          width: 4
        }
      }
    })
  })

}
function painAccuracy(xdata) {
  let input = document.getElementById('site_name');
  let h2 = document.getElementById('Accuracy_h2');
  h2.innerText = input.value;
  var infochart = echarts.init(document.querySelector(".Accuracy .chart"));
  infochart.clear();
  var textname = '站点精度'
  var seriesdata = []
  var hdata = []
  var pdata = []
  var vdata = []
  for (var i in station) {
    hdata.push(station[i]['Horizontal'])
    pdata.push(station[i]['Position'])
    vdata.push(station[i]['Vertical'])
  }
  for (var i in hdata) {
    if (hdata[i] >= 20) {
      hdata[i] = NaN
    }
    if (pdata[i] >= 20) {
      pdata[i] = NaN
    }
    if (vdata[i] >= 20) {
      vdata[i] = NaN
    }
  }
  var s1 = {
    name: 'Horizontal',
    type: 'line',
    data: hdata,
    symbol: 'diamond',

  }
  seriesdata.push(s1)
  var s2 = {
    name: 'Position',
    type: 'line',
    data: pdata,
    symbol: 'arrow',

  }
  seriesdata.push(s2)
  var s3 = {
    name: 'Vertical',
    type: 'line',
    data: vdata,
    symbol: 'triangle',

  }
  seriesdata.push(s3)
  var tooltipdata = {
    formatter: (value) => { 
      var h = value[0]
      var p = value[1]
      var v = value[2]
      var time = h.name
      var title = year + '/' + month + '/' + day + '/' + time
      var p1 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + h.color + '"></span>'
      var p2 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + p.color + '"></span>'
      var p3 = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + v.color + '"></span>'
      content = title + "</br>" + p1 + h.seriesName + ': ' + h.data.toFixed(2)
        + "</br>" + p2 + p.seriesName + ': ' + p.data.toFixed(2)
        + "</br>" + p3 + v.seriesName + ': ' + v.data.toFixed(2)
      return content
    },
    trigger: 'axis',
  }
  var ydata = {
    name: '精度[m]',
    nameLocation: "center",
    nameTextStyle: {
      fontSize: 16,
      padding: 12,
      color: 'white'
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed',
      }
    },
    axisLine: {
      lineStyle: {
        color: 'white',  
      },
    },
    axisLabel: {
      color: "white",
    }
  }

  option = {
    color: ['#87CEFA', '#90EE90', '#FF1493'],
    title: {
      show: false,
      left: 'center',
      textStyle: {

        color: 'white',

        fontStyle: 'normal',

        fontWeight: 'bold',

        fontFamily: 'sans-serif',
        
        fontSize: 18
      },
      text: textname,
    },
    grid: {
      top: "7%",
      // left: "%",
      right: "3%%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true,
      width: '90%',
      height: '80%'
    },
    tooltip: tooltipdata,
    legend: {
      show: false

    },
    xAxis: {
      name: '时间',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',  
        },
      },
    },
    yAxis: ydata,
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 4,
        lineStyle: {
          width: 4
        }
      }
    })
  })
  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 2,
        lineStyle: {
          width: 2
        }
      }
    })
  })
  window.addEventListener('resize', function () {
    infochart.resize()
  })
}
function painionosphereInfo(ion_info) {

  id = $("input[name='types2']:checked").val();

  // X轴数据
  // var xdata = []
  // for (var i in station) {
  //   xdata.push(station[i]['time'].slice(11, 16))
  // }

  // console.log(xdata)

  var infochart = echarts.init(document.querySelector(".ionosphereInfo .chart"));
  infochart.clear();
  var textname = '电离层信息'
  // document.getElementById("height").value = ion_info['height'];

  var seriesdata = []
  var sdata = []
  for (var i = 0; i < ion_info['tec'].length; i++) {
    sdata.push(ion_info['tec'][i].toFixed(2))
  }
  var s = {
    type: 'line',
    data: sdata,
  }
  seriesdata.push(s)

  option = {
    color: '#FF1493',
    title: {
      show: false,
      left: 'center',
      textStyle: {

        color: 'white',

        fontStyle: 'normal',

        fontWeight: 'bold',

        fontFamily: 'sans-serif',
        
        fontSize: 18
      },
      text: textname,
    },
    grid: {
      top: "7%",
      left: "7%",
      // right: "3%%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true,
      width: '90%',
      height: '70%'
    },
    tooltip: {
      formatter: (value) => { 
        var obj = value[0]
        var time = obj.name
        var title = year + '/' + month + '/' + day + '/' + time


        var p = '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + obj.color + '"></span>'
        content = title + "</br>" + p + '总电子含量: ' + obj.data
        return content
      },
      trigger: 'axis',
      showSymbol: false,
    },
    legend: {
      show: false

    },
    xAxis: {
      name: '时间',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 15,
        color: 'white'
      },
      data: xdata,
      axisLabel: {
        color: "white",
        interval: 11,

      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {

        lineStyle: {
          color: 'white',  
        },
      },
    },
    yAxis: {
      name: '电子含量',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 55,
        color: 'white'
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
        }
      },
      axisLabel: {
        color: "white",
        formatter: function (value) {
          // console.log(value)
          value = value + ' TECU'
          return value;
        }
      },
      axisLine: {
        lineStyle: {
          color: 'white',  
        },
      }
    },
    series: seriesdata
  };
  infochart.setOption(option);
  infochart.on('mouseover', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 4,
        lineStyle: {
          width: 4
        }
      }
    })
  })
  infochart.on('mouseout', function (params) {
    infochart.setOption({
      series: {
        name: params.seriesName,
        symbolSize: 2,
        lineStyle: {
          width: 2
        }
      }
    })
  })
  window.addEventListener('resize', function () {
    infochart.resize()
  })
}
function paindistribution_map() {
  
  var sat = {}
  for (var i = 1; i < 65; i++) {

    if (i < 10) {
      i = "0" + i
    }
    sat["C" + i] = {}
    sat["C" + i]['AH'] = []
    sat["C" + i]['hH'] = []
  }
  for (var i in sat) {
    for (var j = 0; j < 96; j++) {
      sat[i]['AH'][j] = 0
      sat[i]['hH'][j] = 0
    }
  }

  var timerange2 = document.getElementById("timerange2").value;

  var timenum3 = document.getElementById("timenum3");
  year = site_datepick.value.substr(0, 4)
  month = Math.floor(site_datepick.value.substr(5, 2))
  day = Math.floor(site_datepick.value.substr(8, 2))
  // console.log(year,month,day)
  if (month < 10) {
    var month1 = '0' + month
  }
  else {
    var month1 = month
  }
  if (day < 10) {
    var day1 = '0' + day
  }
  else {
    var day1 = day
  }
  site_datepick.value = year + '-' + month1 + '-' + day1
  var hour = Math.floor(timerange2 / 4)
  var minute = (timerange2 - hour * 4) * 15
  if (hour < 10) { hour = '0' + hour }
  else { hour = hour }
  var stime = year + '/' + month + '/' + day + '/' + hour + ':' + minute
  var timeid = year + month + day + hour + minute
  timenum3.value = stime;

  var infochart = echarts.init(document.querySelector(".distribution_map .chart"));
  // infochart.clear();
  var seriesdata = []
  var polardata = {}
  var satdata = []
  var n = 0
  for (var i in station) {
    for (var j in station[i]['visibility']) {
      sat[j]['hH'][n] = station[i]['visibility'][j][0]
      sat[j]['AH'][n] = station[i]['visibility'][j][1]
    }
    for (var i in sat) {
      if (sat[i]['hH'][n] == 0) {
        sat[i]['AH'][n] = null;
        sat[i]['hH'][n] = null;
      }
    }
    n += 1
  }
  var zz = 1
  for (var i in sat) {
    var z = 0

    for (var j in sat[i]['hH']) {
      if (sat[i]['hH'][j] != null) {
        z += 1
      }

    }
    if (z == 0) { delete sat[i] }
    zz += 1
  }

  for (var i in sat) {

    polardata[i] = []
    satdata.push([sat[i]['hH'][timerange2], sat[i]['AH'][timerange2], i])

  }
  var s = {

    type: 'scatter',
    data: satdata,
    coordinateSystem: 'polar',
    label: {
      show: true,
      position: "right",
      color: '#f3f8fa',
      formatter: '{@value}'   // 点旁边显示label，这里使用name: '横坐标'这样写也可以，鼠标移入出现提示。
    },
    symbol: 'image://../static/images/icon/scattericon.png',
    symbolSize: 15,
    itemStyle: {
      normal: {
        color: ' #f52020',
      }
    },


  }
  seriesdata.push(s)
  for (var i in sat) {


    for (var j = 0; j < 96; j++) {
      polardata[i][j] = [sat[i]['hH'][j], sat[i]['AH'][j]]
    }


    var s2 = {
      name: i,
      type: 'line',
      data: polardata[i],
      coordinateSystem: 'polar',
      showSymbol: false,
      itemStyle: {
        normal: {
          color: '#7acdf7',
        }
      },
    }

    seriesdata.push(s2)

  }
  var altdata = []
  for (var i = 0; i < 73; i++) {
    altdata.push([$('#alttext').val(), i * 5])
  }
  var s3 = {
    name: '截止高度角',
    type: 'line',
    data: altdata,
    coordinateSystem: 'polar',
    showSymbol: false,
    itemStyle: {
      normal: {
        color: '#3f81f4',
      }
    },
  }
  seriesdata.push(s3)
  const AH = [
    0, 90, 180, 270, 360
  ];
  const hH = [
    0, 30, 60, 90
  ];
  option = {
    title: {
      show: false
    },
    grid: {
      top: "7%",
      left: "7%",
      // right: "3%%",
      bottom: "3%",
      width: '90%',
      height: '70%'
    },
    legend: {
      orient: 'vertical',      
      
      x: 'left',               
      y: '20px'
      ,

      backgroundColor: 'rgba(0,0,0,0)',
      borderColor: '#ccc',      
      borderWidth: 0,            
      padding: 5,                
      itemGap: 10,              
      itemWidth: 20,             
      itemHeight: 20,           
      textStyle: {
        color: 'white'          
      },
      icon: 'image://../static/images/icon/scattericon.png',
      formatter: function (params) {

        return params
      },
      show: false

    },
    polar: {},
    tooltip: {
      formatter: function (params) {
        var time = year + '/' + month + '/' + day + '/' + hour + ':' + minute
        var text = time + '<br>' + params.value[2] + ': ' + params.value[0].toFixed(2) + ', ' + params.value[1].toFixed(2)
        return text;
      }
    },
    angleAxis: {
      type: 'value',
      data: AH,
      min: 0,
      max: 360,
      boundaryGap: false,
      splitLine: {
        show: true
      },
      axisLine: {
        // show: false
        lineStyle: {
          color: 'white',  
        },
      },
      axisLabel: {
        formatter: '{value} °'
      },
      axisTick: { show: false }
    },
    radiusAxis: {
      inverse: true,
      type: 'value',
      data: hH,
      min: 0,
      max: 90,
      axisLine: {
        show: false
      },
      axisLabel: {
        // rotate: 45
        show: false
      },
    },
    series: seriesdata
  };
  // infochart.clear();
  infochart.setOption(option);
  delete sat
}
//计时器 
var c2 = 0;
var t2;
var timer_is_on2 = 0;
function timedCount2() {
  document.getElementById("timerange2").value = c2;
  paindistribution_map();
  // console.log(station)
  var j = 0
  var snums = []
  for (var i in station) {
    snums[j] = station[i]['counts']
    j += 1
  }
  document.getElementById("snums").value = snums[c2];
  c2 = c2 + 1;
  t2 = setTimeout(function () { timedCount2() }, 1000);
  if (c2 > 96) { c2 = 0 }
}
function startrun2() {
  viewer.clock.shouldAnimate = true;
  if (!timer_is_on2) {
    timer_is_on2 = 1;
    timedCount2();
  }
}
function stoprun2() {
  viewer.clock.shouldAnimate = false;
  clearTimeout(t2);
  timer_is_on2 = 0;
}


var c = 0;
var t;
var timer_is_on = 0;
function timedCount() {
  document.getElementById("timerange").value = c;
  paintmap();
  c = c + 1;
  t = setTimeout(function () { timedCount() }, 1000);
  if (c > 23) { c = 0 }
}
function startrun() {
  viewer.clock.shouldAnimate = true;
  if (!timer_is_on) {
    timer_is_on = 1;
    timedCount();
  }
}
function stoprun() {
  viewer.clock.shouldAnimate = false;
  clearTimeout(t);
  timer_is_on = 0;
}



function picksats() {

  // id = $("input[name='picksats']:checked").val();
  var b2 = document.getElementById("bds_2");
  var b3 = document.getElementById("bds_3");
  var sat_igso = document.getElementsByClassName('sat_igso')
  var sat_geo = document.getElementsByClassName('sat_geo')
  var sat_meo = document.getElementsByClassName('sat_meo')
  var satnumbers = document.getElementById("satnums");
  var allsatnums = document.getElementById("allsatnums");
  var allsats = document.getElementsByTagName('li')

  console.log()

  if (pick_geo.checked == true) {
    for (var i = 0; i < sat_geo.length; i++) { sat_geo[i].style.display = 'block'; }
  }
  else if (pick_geo.checked != true) {
    for (var i = 0; i < sat_geo.length; i++) { sat_geo[i].style.display = 'none'; }
  }
  if (pick_igso.checked == true) {
    for (var i = 0; i < sat_igso.length; i++) { sat_igso[i].style.display = 'block'; }
  }
  else if (pick_igso.checked != true) {
    for (var i = 0; i < sat_igso.length; i++) { sat_igso[i].style.display = 'none'; }
  }
  if (pick_meo.checked == true) {
    for (var i = 0; i < sat_meo.length; i++) { sat_meo[i].style.display = 'block'; }
  }
  else if (pick_meo.checked != true) {
    for (var i = 0; i < sat_meo.length; i++) { sat_meo[i].style.display = 'none'; }
  }
  if (sat_bds2.checked == true) {
    bds_2.style.display = 'block';
    // for(var i=0;i<b2.children.length;i++){
    //   b2.children[i].style.display = 'block';
    // }
  }
  else if (sat_bds2.checked != true) {
    bds_2.style.display = 'none';
    // for(var i=0;i<b2.children.length;i++){
    //   b2.children[i].style.display = 'none';
    // }
  }
  if (sat_bds3.checked == true) {
    bds_3.style.display = 'block';
    // for(var i=0;i<b3.children.length;i++){
    //   b3.children[i].style.display = 'block';
    // }
  }
  else if (sat_bds3.checked != true) {
    bds_3.style.display = 'none';
    // for(var i=0;i<b3.children.length;i++){
    //   b3.children[i].style.display = 'none';
    // }
  }
  if (sat_bds3S.checked == true) {
    bds_3S.style.display = 'block';
    // for(var i=0;i<b3.children.length;i++){
    //   b3.children[i].style.display = 'none';
    // }
  }
  else if (sat_bds3S.checked != true) {
    bds_3S.style.display = 'none';
    // for(var i=0;i<b3.children.length;i++){
    //   b3.children[i].style.display = 'none';
    // }
  }

  satnumbers.value = numscal()
  allsatnums.value = '/' + numscal2()
}
function switchbar() {
  var cc = document.getElementById('panel')
  var bb = document.getElementById('openbar')
  // console.log(b.style.display)
  if (cc.style.display == 'none') {
    bb.style.display = 'none'
    cc.style.display = 'block'
  }
  else {

    bb.style.display = 'block'
    cc.style.display = 'none'
  }
}
function numscal() {
  var sat_igso = document.getElementsByClassName('sat_igso')
  var sat_geo = document.getElementsByClassName('sat_geo')
  var sat_meo = document.getElementsByClassName('sat_meo')
  var b2 = document.getElementById("bds_2");
  var b3 = document.getElementById("bds_3");
  var sat1 = document.getElementById('sat_all').children[0].children
  var sat2 = document.getElementById('sat_all').children[1].children
  var sat3 = document.getElementById('sat_all').children[2].children
  var satnums = 0
  var allsats = document.getElementsByTagName('li')
  if (document.getElementById('sat_all').children[0].style.display == 'block') {
    for (var i = 0; i < sat1.length; i++) {
      var obj1 = sat1[i].children;
      if (sat1[i].style.display == 'block' && $(obj1).prop("checked") == true) {
        satnums += 1
      }
    }
  }
  if (document.getElementById('sat_all').children[1].style.display == 'block') {
    for (var i = 0; i < sat2.length; i++) {
      var obj2 = sat2[i].children;
      if (sat2[i].style.display == 'block' && $(obj2).prop("checked") == true) {
        satnums += 1
      }
    }
  }
  if (document.getElementById('sat_all').children[2].style.display == 'block') {
    for (var i = 0; i < sat3.length; i++) {
      var obj3 = sat3[i].children;
      if (sat3[i].style.display == 'block' && $(obj3).prop("checked") == true) {
        satnums += 1
      }
    }
  }

  return satnums
}

function numscal2() {
  var sat1 = document.getElementById('sat_all').children[0].children
  var sat2 = document.getElementById('sat_all').children[1].children
  var sat3 = document.getElementById('sat_all').children[2].children
  var satnums = 0
  var allsats = document.getElementsByTagName('li')
  if (document.getElementById('sat_all').children[0].style.display == 'block') {
    for (var i = 0; i < sat1.length; i++) {
      if (sat1[i].style.display == 'block') {
        satnums += 1
      }
    }
  }
  if (document.getElementById('sat_all').children[1].style.display == 'block') {
    for (var i = 0; i < sat2.length; i++) {
      if (sat2[i].style.display == 'block') {
        satnums += 1
      }
    }
  }
  if (document.getElementById('sat_all').children[2].style.display == 'block') {
    for (var i = 0; i < sat3.length; i++) {
      if (sat3[i].style.display == 'block') {
        satnums += 1
      }
    }
  }

  return satnums
}
function satpick() {
  var sat1 = document.getElementById('sat_all').children[0].children
  var sat2 = document.getElementById('sat_all').children[1].children
  var sat3 = document.getElementById('sat_all').children[2].children
  var satname = []
  if (document.getElementById('sat_all').children[0].style.display == 'block') {
    for (var i = 0; i < sat1.length; i++) {
      var obj2 = sat1[i].children;
      if (sat1[i].style.display == 'block') {
        if ($(obj2).prop("checked") == true) {
          satname.push(sat1[i].id.substr(0, 3))
        }

      }
    }
  }

  if (document.getElementById('sat_all').children[1].style.display == 'block') {
    for (var i = 0; i < sat2.length; i++) {
      var obj2 = sat2[i].children;
      if (sat2[i].style.display == 'block') {
        if ($(obj2).prop("checked") == true) {
          satname.push(sat2[i].id.substr(0, 3))
        }
      }
    }
  }
  if (document.getElementById('sat_all').children[2].style.display == 'block') {
    for (var i = 0; i < sat3.length; i++) {
      var obj3 = sat3[i].children;
      if (sat3[i].style.display == 'block') {
        if ($(obj3).prop("checked") == true) {
          satname.push(sat3[i].id.substr(0, 3))
        }
      }
    }
  }


  return satname

}




function setp1(callback) {
  setTimeout(function () {
    setp('leftp')
    callback();
  }, 1000)
}

function setarea() {

  id1 = 'leftp'
  id2 = 'rightp'
  setp1();


}
function setp1() {
  var density = $('#density').val();


  viewer.scene.mode = Cesium.SceneMode.SCENE2D
  viewer.scene.screenSpaceCameraController.enableTranslate = false;
  viewer.scene.screenSpaceCameraController.enableZoom = false;
  var rectangle = Cesium.Rectangle.fromDegrees(-180, 90, 180, -90);
  viewer.camera.setView({
    destination: rectangle,
    orientation: {
      heading: Cesium.Math.toRadians(0),
      pitch: Cesium.Math.toRadians(-90),
      roll: Cesium.Math.toRadians(0)
    }
  });

  // viewer.dataSources.remove(satSource);
  viewer._container.style.cursor = "crosshair";
  alert('选取左上角点')
  var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction(function (event) {


    var ellipsoid = viewer.scene.globe.ellipsoid;
    var cartesian = viewer.camera.pickEllipsoid(event.position, ellipsoid);

    var cartographic = Cesium.Cartographic.fromCartesian(cartesian);

    var lon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(1);
    var lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(1);
    document.getElementById('leftp').value = lon + '°,' + lat + '°'
    handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)
    viewer._container.style.cursor = "auto";
    setp2()

  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)

}
function setp2() {
  var density = $('#density').val();
  viewer.scene.mode = Cesium.SceneMode.SCENE2D
  viewer._container.style.cursor = "crosshair";
  alert('选取右下角点')
  var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction(function (event) {


    var ellipsoid = viewer.scene.globe.ellipsoid;
    var cartesian = viewer.camera.pickEllipsoid(event.position, ellipsoid);

    var cartographic = Cesium.Cartographic.fromCartesian(cartesian);

    var lon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(1);
    var lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(1);
    document.getElementById('rightp').value = lon + '°,' + lat + '°'


    handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)

    viewer._container.style.cursor = "auto";
    viewer.scene.mode = Cesium.SceneMode.SCENE3D
    viewer.scene.screenSpaceCameraController.enableTranslate = true;
    viewer.scene.screenSpaceCameraController.enableZoom = true;
    area_paint()
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)

}
function setp(id) {
  viewer.scene.mode = Cesium.SceneMode.SCENE2D
  viewer.dataSources.remove(satSource);
  viewer._container.style.cursor = "crosshair";
  var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction(function (event) {


    var ellipsoid = viewer.scene.globe.ellipsoid;
    var cartesian = viewer.camera.pickEllipsoid(event.position, ellipsoid);

    var cartographic = Cesium.Cartographic.fromCartesian(cartesian);

    var lon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(1);
    var lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(1);
    var height = Math.ceil(this.viewer.camera.positionCartographic.height);
    var height = 0
    var height1 = viewer.scene.globe.getHeight(cartographic);
    var height2 = cartographic.height;

    // alert(lon + ' , ' + lat)
    document.getElementById(id).value = lon + '°,' + lat + '°'


    handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)

    viewer._container.style.cursor = "auto";
    viewer.scene.mode = Cesium.SceneMode.SCENE3D

  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
}
function pickall(obj) {

  var sat1 = document.getElementById('sat_all').children[0].children
  var sat2 = document.getElementById('sat_all').children[1].children
  var sat3 = document.getElementById('sat_all').children[2].children
  var satnums = 0
  if (document.getElementById('sat_all').children[0].style.display == 'block') {
    for (var i = 0; i < sat1.length; i++) {
      var obj1 = sat1[i].children;
      if (sat1[i].style.display == 'block' && $(obj).prop("checked") == true && !$(obj1).is(':disabled')) {
        satnums += 1
        $(obj1).prop('checked', true)
      }
      else if (sat1[i].style.display == 'block' && $(obj).prop("checked") == false) {
        satnums += 1
        console.log(obj1)
        console.log(sat1[i])
        $(obj1).prop('checked', false)
      }
    }
  }
  if (document.getElementById('sat_all').children[1].style.display == 'block') {
    for (var i = 0; i < sat2.length; i++) {
      var obj2 = sat2[i].children;
      if (sat2[i].style.display == 'block' && $(obj).prop("checked") == true && !$(obj2).is(':disabled')) {
        satnums += 1
        $(obj2).prop('checked', true)
      }
      else if (sat2[i].style.display == 'block' && $(obj).prop("checked") == false) {
        satnums += 1
        $(obj2).prop('checked', false)
      }
    }
  }
  if (document.getElementById('sat_all').children[2].style.display == 'block') {
    for (var i = 0; i < sat3.length; i++) {
      var obj3 = sat3[i].children;
      if (sat3[i].style.display == 'block' && $(obj).prop("checked") == true && !$(obj3).is(':disabled')) {
        satnums += 1
        $(obj3).prop('checked', true)
      }
      else if (sat3[i].style.display == 'block' && $(obj).prop("checked") == false) {
        satnums += 1
        $(obj3).prop('checked', false)
      }
    }
  }
  picksats()
}
var rectangleEntity = null;
function area_paint() {
  if (rectangleEntity) {
    viewer.entities.remove(rectangleEntity);
  }
  var leftlon = document.getElementById('leftp').value.split(',')[0].replace('°', '')
  var rightlon = document.getElementById('rightp').value.split(',')[0].replace('°', '')
  var leftlat = document.getElementById('leftp').value.split(',')[1].replace('°', '')
  var rightlat = document.getElementById('rightp').value.split(',')[1].replace('°', '')

  var rec = Cesium.Rectangle.fromDegrees(leftlon, rightlat, rightlon, leftlat);
  rectangleEntity = viewer.entities.add({
    rectangle: {
      coordinates: rec,
      material: Cesium.Color.RED.withAlpha(0.5)
    }
  });

}


var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);


function startSelection() {
  viewer.scene.mode = Cesium.SceneMode.SCENE2D
  var rectangle = Cesium.Rectangle.fromDegrees(-180, 90, 180, -90);
  alert('请框选区域')
  viewer.camera.setView({
    destination: rectangle,
    orientation: {
      heading: Cesium.Math.toRadians(0),
      pitch: Cesium.Math.toRadians(-90),
      roll: Cesium.Math.toRadians(0)
    }
  });
  
  viewer.scene.screenSpaceCameraController.enableRotate = false;
  viewer.scene.screenSpaceCameraController.enableTranslate = false;
  viewer.scene.screenSpaceCameraController.enableZoom = false;
  viewer.scene.screenSpaceCameraController.enableTilt = false;
  viewer.scene.screenSpaceCameraController.enableLook = false;
  viewer.container.style.cursor = 'crosshair';
  handler.setInputAction(startDrawing, Cesium.ScreenSpaceEventType.LEFT_DOWN);
}
var startMousePosition;
var start = new Cesium.Cartesian2();
var rectangleElement;
function startDrawing(event) {
  startMousePosition = new Cesium.Cartesian2(event.position.x, event.position.y);
  start = Cesium.Cartesian3.clone(event.position);
  console.log(start)
  rectangleElement = document.createElement('div');
  rectangleElement.className = 'rectangle';
  rectangleElement.style.left = start.x + 'px';
  rectangleElement.style.top = start.y + 'px';
  rectangleElement.style.position = 'absolute';
  rectangleElement.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
  rectangleElement.style.border = '1px solid rgba(255, 255, 255, 0.7)';
  rectangleElement.style.pointerEvents = 'none';
  rectangleElement.style.zIndex = '9999';
  viewer.container.appendChild(rectangleElement);
  handler.setInputAction(updateDrawing, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
  handler.setInputAction(endSelection, Cesium.ScreenSpaceEventType.LEFT_UP);
}

function updateDrawing(event) {
  if (!Cesium.Cartesian3.equals(start, Cesium.Cartesian3.ZERO)) {
    var end = Cesium.Cartesian3.clone(event.endPosition);
    var width = Math.abs(end.x - start.x);
    var height = Math.abs(end.y - start.y);
    rectangleElement.style.width = width + 'px';
    rectangleElement.style.height = height + 'px';
    if (end.x < start.x) {
      rectangleElement.style.left = end.x + 'px';
    }
    if (end.y < start.y) {
      rectangleElement.style.top = end.y + 'px';
    }
  }
}

var endMousePosition;
function endSelection(event) {
  viewer.scene.morphTo3D();
  handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_DOWN);
  handler.removeInputAction(Cesium.ScreenSpaceEventType.MOUSE_MOVE);
  handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_UP);
  viewer.container.removeChild(rectangleElement);
  viewer.container.style.cursor = 'default';
  viewer.scene.screenSpaceCameraController.enableRotate = true;
  viewer.scene.screenSpaceCameraController.enableTranslate = true;
  viewer.scene.screenSpaceCameraController.enableZoom = true;
  viewer.scene.screenSpaceCameraController.enableTilt = true;
  viewer.scene.screenSpaceCameraController.enableLook = true;
  endMousePosition = new Cesium.Cartesian2(event.position.x, event.position.y);
  var startCartesian3 = viewer.camera.pickEllipsoid(startMousePosition, viewer.scene.globe.ellipsoid);
  var endCartesian3 = viewer.camera.pickEllipsoid(endMousePosition, viewer.scene.globe.ellipsoid);
  if (!startCartesian3 || !endCartesian3) {
    alert('超出地图区域')
    startSelection()
  }
  else {
    var startCartographic = viewer.scene.globe.ellipsoid.cartesianToCartographic(startCartesian3);
    var endCartographic = viewer.scene.globe.ellipsoid.cartesianToCartographic(endCartesian3);
    var west = Cesium.Math.toDegrees(Math.min(startCartographic.longitude, endCartographic.longitude));
    var east = Cesium.Math.toDegrees(Math.max(startCartographic.longitude, endCartographic.longitude));
    var south = Cesium.Math.toDegrees(Math.min(startCartographic.latitude, endCartographic.latitude));
    var north = Cesium.Math.toDegrees(Math.max(startCartographic.latitude, endCartographic.latitude));
    document.getElementById('leftp').value = west.toFixed(1) + '°,' + north.toFixed(1) + '°'
    document.getElementById('rightp').value = east.toFixed(1) + '°,' + south.toFixed(1) + '°'
    alert('完成')
    startrun();
    area_paint()
  }
}
function switchabout() {
  aboutdiv = document.getElementById('about')

  if (aboutdiv.style.display == 'none') {
    aboutdiv.style.display = 'block'
  }
  else {
    aboutdiv.style.display = 'none'
  }
}
