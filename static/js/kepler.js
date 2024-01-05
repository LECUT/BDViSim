Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMGNhYjhkOS00MGE2LTRkMDctOGZiYS1mZjc4MGQ0YmQyZTMiLCJpZCI6OTYzOTEsImlhdCI6MTY1NDQ5MDE5OH0.KMWej-d39eu-JXzFrpUTrc0rxYr0m5WcAriKMPSnqLs'


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

// Cesium.Timeline.prototype.makeLabel = CesiumDateTimeFormatter;
var viewer = new Cesium.Viewer('cesiumContainer', {
  selectionIndicator: false,
  animation: false, 
  // shouldAnimate: true,
  // homeButton: false, 
  // fullscreenButton: false, 
  //  baseLayerPicker: false, 
  geocoder: false, 
  timeline: false, 
  // sceneModePicker: false, 
  // navigationHelpButton: false, 
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

// viewer.scene.debugShowFramesPerSecond = true;
viewer.baseLayerPicker.viewModel.selectedImagery = viewer.baseLayerPicker.viewModel.imageryProviderViewModels[3];

viewer.clock.shouldAnimate = true;
// viewer.animation.viewModel.dateFormatter = CesiumDateFormatter;
// viewer.animation.viewModel.timeFormatter = CesiumTimeFormatter;

// viewer.scene.skyBox.show = false 
// viewer.scene.backgroundColor = new Cesium.Color(0.0, 0.0, 0.0, 0.0);
// viewer.scene.skyAtmosphere.show = false
// viewer.scene.moon.show = false
// viewer.scene.sun.show = false



viewer.scene.skyBox = new Cesium.SkyBox({
  sources: {
    positiveX: '../static/images/stars/starmap_2020_16k_px.jpg',
    negativeX: '../static/images/stars/starmap_2020_16k_mx.jpg',
    positiveY: '../static/images/stars/starmap_2020_16k_py.jpg',
    negativeY: '../static/images/stars/starmap_2020_16k_my.jpg',
    positiveZ: '../static/images/stars/starmap_2020_16k_pz.jpg',
    negativeZ: '../static/images/stars/starmap_2020_16k_mz.jpg'
  }
});


czml = '../static/czml/keplerorbit.czml'

var stationdataSource = new Cesium.CzmlDataSource(czml);

stationdataSource.load(czml);
viewer.dataSources.add(stationdataSource);

function initalize() {

  // viewer.scene.globe.enableLighting = true;
  // viewer.shadows = true;

  
  var stages = viewer.scene.postProcessStages;
  viewer.scene.brightness = viewer.scene.brightness || stages.add(Cesium.PostProcessStageLibrary.createBrightnessStage());
  viewer.scene.brightness.enabled = true;
  viewer.scene.brightness.uniforms.brightness = Number(1.2);


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



  // viewer.clock.onTick.addEventListener(rotate);

  var imageryLayers = viewer.scene.imageryLayers;
  var tdtAnnoLayer = imageryLayers.addImageryProvider(new Cesium.WebMapTileServiceImageryProvider({
    url: "http://t0.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={TileMatrix}&TILEROW={TileRow}&TILECOL={TileCol}&tk=269b6942f19f345009e605301d0481c2",
    layer: "tdtAnnoLayer",
    style: "default",
    format: "image/jpeg",
    tileMatrixSetID: "GoogleMapsCompatible"
  }));




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

var initialPosition = new Cesium.Cartesian3.fromDegrees(35.42, 30.16, 180000000);
var homeCameraView = {
  destination: initialPosition,
};
viewer.scene.camera.flyTo(homeCameraView);
//汉化
function replace2Chinese() {

  var cesium_baseLayerPicker_sectionTitle = document.getElementsByClassName("cesium-baseLayerPicker-sectionTitle");
  cesium_baseLayerPicker_sectionTitle[0].innerHTML = '影像';
  cesium_baseLayerPicker_sectionTitle[1].innerHTML = '地形';

  var cesium_baseLayerPicker_itemLabel = document.getElementsByClassName("cesium-baseLayerPicker-itemLabel");
  // cesium_baseLayerPicker_itemLabel[cesium_baseLayerPicker_itemLabel.length - 1].innerHTML = 'STK World Terrain';

  var cesium_navigation_button_left = document.getElementsByClassName("cesium-navigation-button-left");
  cesium_navigation_button_left[0].innerHTML = cesium_navigation_button_left[0].innerHTML.replace('>Mouse', '>鼠标');

  var cesium_navigation_button_right = document.getElementsByClassName("cesium-navigation-button-right");
  cesium_navigation_button_right[0].innerHTML = cesium_navigation_button_right[0].innerHTML.replace('>Touch', '>触屏');

  var cesium_navigation_help_instructions = document.getElementsByClassName("cesium-navigation-help-instructions");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Pan view", "平移视图");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Left click + drag", "点击左键 + 拖拽");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Zoom view", "缩放视图");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Right click + drag, or", "点击右键 + 拖拽; 或上下滚动鼠标滚轮");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Mouse wheel scroll", "");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Rotate view", "旋转视图");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("Middle click + drag, or", "中键点击 + 拖拽; 或CTRL + 点击左/右键 + 拖拽");
  cesium_navigation_help_instructions[0].innerHTML = cesium_navigation_help_instructions[0].innerHTML.replace("CTRL + Left/Right click + drag", "");

  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Pan view", "平移视图");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("One finger drag", "单指拖拽");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Zoom view", "缩放视图");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Two finger pinch", "两指控制缩放");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Tilt view", "倾斜视图");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Two finger drag, same direction", "两指向同一方向拖拽");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Rotate view", "旋转视图");
  cesium_navigation_help_instructions[1].innerHTML = cesium_navigation_help_instructions[1].innerHTML.replace("Two finger drag, opposite direction", "两指向相反方向拖拽");


  var v0 = document.getElementById('cesiumContainer').getElementsByClassName("cesium-viewer");
  var v1 = v0[0].getElementsByClassName("cesium-viewer-toolbar");
  var v2 = v1[0].getElementsByClassName("cesium-button cesium-toolbar-button cesium-home-button");
  v2[0].title = "复位视图(View Home)";

  // v2[0].innerHTML =
  //     '<img src="Cesium_1.49/Widgets/Images/ImageryProviders/earthfull.png" width="30" height="30" />';



  v2 = v1[0].getElementsByClassName("cesium-button cesium-toolbar-button cesium-navigation-help-button");
  v2[0].title = "操作指南";

  v2 = v1[0].getElementsByClassName("cesium-viewer-geocoderContainer");


  v1 = v0[0].getElementsByClassName("cesium-viewer-fullscreenContainer");
  v2 = v1[0].getElementsByClassName("cesium-button cesium-fullscreenButton");
  v2[0].title = "全屏(Full Screen)";

  $($('.cesium-toolbar-button')[5]).attr('title', '2.5D');
  $('.cesium-sceneModePicker-buttonColumbusView').attr('title', '2.5D');


  var xxx = $('.cesium-baseLayerPicker-categoryTitle')[0];
  $(xxx).text('Cesium ion内置影像');

  xxx = $('.cesium-baseLayerPicker-categoryTitle')[1];
  $(xxx).text('第三方影像');

  xxx = $('.cesium-baseLayerPicker-categoryTitle')[2];
  $(xxx).text('国产影像');

  xxx = $('.cesium-baseLayerPicker-categoryTitle')[3];
  $(xxx).text('Cesium ion内置地形');

  // xxx = $('.cesium-baseLayerPicker-categoryTitle')[3];
  //$(xxx).text('地表形态');
  //xxx = $('.cesium-baseLayerPicker-itemLabel')[1];
  //$(xxx).text('光滑椭球体(WGS84)');
}
replace2Chinese()





function range() {
  var erange = document.getElementById('e_range').value
  var I_0range = document.getElementById('I_0_range').value
  var sqrt_Arange = document.getElementById('sqrt_A_range').value
  var OMEGArange = document.getElementById('OMEGA_range').value
  var wrange = document.getElementById('w_range').value
  var M0range = document.getElementById('M0_range').value
  // console.log('first: ' ,erange,I_0range,sqrt_Arange,OMEGArange,wrange,M0range)
  document.getElementById('e_value').value = erange
  document.getElementById('I_0_value').value = I_0range
  document.getElementById('sqrt_A_value').value = sqrt_Arange
  document.getElementById('OMEGA_value').value = OMEGArange
  document.getElementById('w_value').value = wrange
  document.getElementById('M0_value').value = M0range
  paintorbit()
}

function paintorbit() {
  var e = document.getElementById('e_value').value
  // toe = 345600.0000
  var I_0 = document.getElementById('I_0_value').value
  // OMEGA_DOT = -4.7787704835E-009
  var sqrt_A = document.getElementById('sqrt_A_value').value
  var OMEGA = document.getElementById('OMEGA_value').value
  var w = document.getElementById('w_value').value
  var M0 = document.getElementById('M0_value').value
  // console.log(e,I_0,sqrt_A,OMEGA,w,M0 )
  $.post('/keplercal', { 'e': e, 'I_0': I_0, 'sqrt_A': sqrt_A, 'OMEGA': OMEGA, 'w': w, 'M0': M0 }, function (res) {
    // console.log(res)
    viewer.dataSources.remove(stationdataSource)

    var newczml = res[0]
    stationdataSource = new Cesium.CzmlDataSource(newczml);
    stationdataSource.load(newczml);
    viewer.dataSources.add(stationdataSource);
    var sat = stationdataSource.entities.values
    getascend(res[1], res[0][1],res[2])
    // getinterpotint()
  })
}

function switchbar() {
  c = document.getElementById('control_bar')
  b = document.getElementById('openbar')
  console.log(b.style.display)
  if (c.style.display == 'none') {
    b.style.display = 'none'
    c.style.display = 'block'
  }
  else {

    b.style.display = 'block'
    c.style.display = 'none'
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




var purpleArrow = viewer.entities.add({
  name: 'x',
  position: Cesium.Cartesian3.fromDegrees(-3, 0, 50000000),
  label: {
    text: 'X',
    font: '16px sans-serif',
    fillColor: Cesium.Color.YELLOW,
    outlineColor: Cesium.Color.WHITE,
    outlineWidth: 2,
    style: Cesium.LabelStyle.FILL_AND_OUTLINE
  },
  polyline: {
    positions: Cesium.Cartesian3.fromDegreesArrayHeights([0, 0, 0,
      0, 0, 50000000]),
    width: 10,
    followSurface: false,
    material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.WHITE)
  }
}
);
var purpleArrow2 = viewer.entities.add({
  position: Cesium.Cartesian3.fromDegrees(87, 0, 50000000),
  label: {
    text: 'Y',
    font: '16px sans-serif',
    fillColor: Cesium.Color.YELLOW,
    outlineColor: Cesium.Color.WHITE,
    outlineWidth: 2,
    style: Cesium.LabelStyle.FILL_AND_OUTLINE
  },
  polyline: {
    positions: Cesium.Cartesian3.fromDegreesArrayHeights([90, 0, 0,
      90, 0, 50000000]),
    width: 10,
    followSurface: false,
    material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.WHITE)
  }
}
)
var purpleArrow3 = viewer.entities.add({
  name: 'z',
  position: Cesium.Cartesian3.fromDegrees(0, 87, 50000000),
  label: {
    text: 'Z',
    font: '16px sans-serif',
    fillColor: Cesium.Color.YELLOW,
    outlineColor: Cesium.Color.WHITE,
    outlineWidth: 2,
    style: Cesium.LabelStyle.FILL_AND_OUTLINE
  },
  polyline: {
    positions: Cesium.Cartesian3.fromDegreesArrayHeights([0, 90, 0,
      0, 90, 50000000]),
    width: 10,
    followSurface: false,
    material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.WHITE)
  }
}
)

var spos0 = Cesium.Cartesian3.fromDegrees(0, 0, 0); 
var spos = Cesium.Cartesian3.fromDegrees(0, 0, (document.getElementById('sqrt_A_value').value) * (document.getElementById('sqrt_A_value').value) - 6378137); 
// var springline = viewer.entities.add({
//   id:'springline',
//   polyline: {
//     positions: [spos0, spos],
//     width: 1,
//     material: new Cesium.PolylineDashMaterialProperty({
//       color: Cesium.Color.CYAN
//   })
//   }
// });
// var earthpoint =viewer.entities.add({
//   id:'earthpoint',
//   name:'地心',
//   position : Cesium.Cartesian3.fromDegrees(0, 0, -6378137),
//   label:{
//     // font: "6pt Lucida Console",
//     // outlineWidth: 2,
//     // outlineColor: {"rgba": [255, 0, 0, 255]},
//     // horizontalOrigin: "LEFT",
//     // pixelOffset: {"cartesian2": [20, 14]},
//     // fillColor: {"rgba": [213, 255, 0, 255]},

//     font: '10pt Lucida Console',
//     fillColor: Cesium.Color.RED,
//     pixelOffset: new Cesium.Cartesian2(50, -14),
//     text: '地心'
//   },
//   point : {
//     pixelSize : 20,
//     color : Cesium.Color.BLUE,
//     heightReference : Cesium.HeightReference.NONE
//   }
// });
function getascend(ascendpos, sat,truepos) {
  if (point != '') {
    viewer.entities.removeById("point");
  }
  if (spoint != '') {
    viewer.entities.removeById("spoint");
  }
  if (equator != '') {
    viewer.entities.removeById("equator");
  }
  if (npoint != '') {
    viewer.entities.removeById("npoint");
  }
  if (acendline != '') {
    viewer.entities.removeById("acendline");
  }
  if (acendangle != '') {
    viewer.entities.removeById("acendangle");
  }
  if (acendanglelabel != '') {
    viewer.entities.removeById("acendanglelabel");
  }
  if (inclinationangle != '') {
    viewer.entities.removeById("inclinationangle");
  }

  if (npointangle != '') {
    viewer.entities.removeById("npointangle");
  }
  if (npoitntanglelabel != '') {
    viewer.entities.removeById("npoitntanglelabel");
  }
  if (satline != '') {
    viewer.entities.removeById("satline");
  }
  if (satline != '') {
    viewer.entities.removeById("semiMajorAxisline");
  }
  if (trueangle != '') {
    viewer.entities.removeById("trueangle");
  }
  if (trueanglelabel != '') {
    viewer.entities.removeById("trueanglelabel");
  }
  if (inclinationanglelabel != '') {
    viewer.entities.removeById("inclinationanglelabel");
  }
  if (equatorpos!= '') {
    viewer.entities.removeById("equatorpos");
  }
  if (orbitpoint != '') {
    viewer.entities.removeById("orbitpoint");
  }


  var semimajoraxis = (document.getElementById('sqrt_A_value').value) * (document.getElementById('sqrt_A_value').value)

  var e = document.getElementById('e_value').value;
  var inclination = document.getElementById('I_0_value').value;
  var longitudeOfAscendingNode=parseFloat(document.getElementById('OMEGA_value').value)-10.5;
  // var longitudeOfAscendingNode = ascendpos[1]+4;
  var ω = document.getElementById('w_value').value;
  var E = document.getElementById('M0_value').value;


  const ascNodeLongitudeRadians = (longitudeOfAscendingNode * Math.PI) / 180; 
  const ascNodeLatitudeRadians = (0 * Math.PI) / 180; 
  const x = Math.cos(ascNodeLongitudeRadians) * Math.cos(ascNodeLatitudeRadians);
  const y = Math.sin(ascNodeLongitudeRadians) * Math.cos(ascNodeLatitudeRadians);
  const z = Math.sin(ascNodeLatitudeRadians);


  const argOfPerigeeRadians = (ω * Math.PI) / 180; 
  const inclinationRadians = (inclination * Math.PI) / 180; 
  const distanceToPerigee = Math.cos(argOfPerigeeRadians);
  const xPerigee = x * Math.cos(argOfPerigeeRadians) - y * Math.sin(argOfPerigeeRadians) * Math.cos(inclinationRadians);
  const yPerigee = x * Math.sin(argOfPerigeeRadians) + y * Math.cos(argOfPerigeeRadians) * Math.cos(inclinationRadians);
  const zPerigee = z * Math.sin(inclinationRadians);


var perigeeLongitude = calculatePerigeeLongitude( longitudeOfAscendingNode, ω);

  // const perigeeLatitude = calculatePerigeeLatitude(semimajoraxis, e, inclination, ω, longitudeOfAscendingNode);

  const perigeeLatitude = calculatePerigeeLatitude(inclination, ω);

  const earthRadius = 6371000; 
  const perigeeAltitude = semimajoraxis + (Math.sqrt(xPerigee ** 2 + yPerigee ** 2 + zPerigee ** 2) - earthRadius) - (e * semimajoraxis);
  var ascendingNodeAltitude=ascendpos[2]
  
  var nearpoint = Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, perigeeAltitude)
  var shengjiaodian = Cesium.Cartesian3.fromDegrees(longitudeOfAscendingNode, 0, ascendingNodeAltitude)

  var point = new Cesium.Entity({
    id: 'point',
    name: '升交点',
    position: shengjiaodian,
    label: {
      font: '10pt Lucida Console',
      fillColor: Cesium.Color.RED,
      pixelOffset: new Cesium.Cartesian2(30, -14),
      text: '升交点'
    },
    point: {
      pixelSize: 20,
      color: Cesium.Color.RED,
      heightReference: Cesium.HeightReference.NONE
    }
  });
  var npoint = new Cesium.Entity({
    id: 'npoint',
    name: '近地点',
    position: nearpoint,
    label: {
      // font: "6pt Lucida Console",
      // outlineWidth: 2,
      // outlineColor: {"rgba": [255, 0, 0, 255]},
      // horizontalOrigin: "LEFT",
      // pixelOffset: {"cartesian2": [20, 14]},
      // fillColor: {"rgba": [213, 255, 0, 255]},

      font: '10pt Lucida Console',
      fillColor: Cesium.Color.fromBytes(255, 20, 147),
      pixelOffset: new Cesium.Cartesian2(30, -14),
      text: '近地点'
    },
    point: {
      pixelSize: 20,
      color: Cesium.Color.fromBytes(255, 20, 147),
      heightReference: Cesium.HeightReference.NONE
    }
  });
  var spoint = new Cesium.Entity({
    id: 'spoint',
    name: '春分点',
    label: {
      font: '10pt Lucida Console',
      fillColor: Cesium.Color.YELLOW,
      pixelOffset: new Cesium.Cartesian2(-50, 14),
      text: '春分点'
    },
    position: Cesium.Cartesian3.fromDegrees(0, 0, semimajoraxis - 6378137),
    point: {
      pixelSize: 20,
      color: Cesium.Color.YELLOW,
      heightReference: Cesium.HeightReference.NONE
    }
  });
  var equator = new Cesium.Entity({
    id: 'equator',
    name: '赤道面',
    // label:{
    //   font: '10pt Lucida Console',
    //   fillColor: Cesium.Color.YELLOW,
    //   pixelOffset: new Cesium.Cartesian2(160, 14),
    //   text: '赤道面'
    // },
    position: Cesium.Cartesian3.fromDegrees(0, 0, -6378137),
    ellipsoid: {
      radii: new Cesium.Cartesian3(semimajoraxis + 6378137, semimajoraxis + 6378137, 1),
      material:  Cesium.Color.fromBytes(139,137,137).withAlpha(0.3),
    }
  });




  var pointPosition = Cesium.Cartesian3.fromDegrees(longitudeOfAscendingNode, 0, ascendingNodeAltitude); 

  var groundPosition = Cesium.Cartesian3.fromDegrees(longitudeOfAscendingNode, 0, 0); 
  var acendline = new Cesium.Entity({
    id: 'acendline',
    polyline: {
      positions: [pointPosition, groundPosition],
      width: 2,
      material: new Cesium.PolylineDashMaterialProperty({
        color: Cesium.Color.RED
      })
    }
  });

  var acendpos = Cesium.Cartesian3.fromDegrees(parseFloat(longitudeOfAscendingNode) + 0.0125, 0, ascendingNodeAltitude / 6);
  var midpos = Cesium.Cartesian3.fromDegrees(parseFloat(longitudeOfAscendingNode) / 2, 0, (semimajoraxis - 6378137 + ascendingNodeAltitude) / 12);
  var spos = Cesium.Cartesian3.fromDegrees(0, 0, (semimajoraxis - 6378137) / 6);
  var acendangle = new Cesium.Entity({
    id: 'acendangle',
    polyline: {
      positions: [spos, midpos, acendpos],
      width:8,
      material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.RED)
    },


  });
  var acendanglelabel = new Cesium.Entity({
    id: 'acendanglelabel',
    position: midpos,
    label: {
      font: '12pt Lucida Console',
      fillColor: Cesium.Color.RED,
      pixelOffset: new Cesium.Cartesian2(30, 10),
      text: '升交点赤经'
    }
  });
  //  var nearpoint=Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, perigeeAltitude)
  var groundnpointpos = Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, 0); 
  //  console.log(groundnpointpos)


  //  var semiMajorAxislinepos = Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude,perigeeAltitude-semimajoraxis);
  var semiMajorAxisline = new Cesium.Entity({
    id: 'semiMajorAxisline',
    name: '近地点连线',
    polyline: {
      positions: [nearpoint, groundnpointpos],
      width: 2,
      arcType: "NONE",
      //   material: new Cesium.PolylineGlowMaterialProperty({
      //     glowPower: 0.2,
      //     color: Cesium.Color.BLUE
      // })
      material: new Cesium.PolylineDashMaterialProperty({
        color:Cesium.Color.fromBytes(255, 20, 147),
      })

    }
  });





  //  var midlon=(parseFloat(ω))/2+parseFloat(longitudeOfAscendingNode)
  var midlon = calculatePerigeeLongitude(longitudeOfAscendingNode, ω / 2);
  //  console.log(midlon,perigeeLatitude)
  var midlat = calculatePerigeeLatitude(inclination, ω / 2);
  var midnpos = Cesium.Cartesian3.fromDegrees(midlon, midlat, (perigeeAltitude + ascendingNodeAltitude) / 8);
  var npos = Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, perigeeAltitude / 4);

  var npointangle = new Cesium.Entity({
    id: 'npointangle',
    polyline: {
      positions: [Cesium.Cartesian3.fromDegrees(parseFloat(longitudeOfAscendingNode) + 0.0125, 0, ascendingNodeAltitude / 4), midnpos, npos],
      width:8,
      material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.fromBytes(255, 20, 147))
    },


  });

  var npoitntanglelabel = new Cesium.Entity({
    id: 'npoitntanglelabel',
    position: midnpos,
    label: {
      font: '12pt Lucida Console',
      fillColor: Cesium.Color.fromBytes(255, 20, 147),
      pixelOffset: new Cesium.Cartesian2(40, 10),
      text: '近地点角距'
    }
  });




  if (sat != '') {
    // console.log(sat.position.cartesian,sat.position.cartesian.indexOf(acendposz),acendposz)
    var id = sat.position.cartesian.indexOf("2022-09-15T00:00:00+00:00")
    var realsatx = sat.position.cartesian[id + 1]
    var realsaty = sat.position.cartesian[id + 2]
    var realsatz = sat.position.cartesian[id + 3]
    // console.log(realsatx,realsaty,realsatz)

    var satpos = new Cesium.Cartesian3(realsatx, realsaty, realsatz);
    var cartographic = Cesium.Cartographic.fromCartesian(satpos);
    var satlongitude = Cesium.Math.toDegrees(cartographic.longitude);
    var satlatitude = Cesium.Math.toDegrees(cartographic.latitude);
    var satheight = truepos[2]
    var satlon = truepos[1]
    var satlat = truepos[0]
    // satpos = new Cesium.Cartesian3(truepos[0], truepos[1], truepos[2]);
    satpos = Cesium.Cartesian3.fromDegrees(satlon, satlat, satheight);

    var groundsatpos = Cesium.Cartesian3.fromDegrees(satlon, satlat, 0);
    var satline = new Cesium.Entity({
      id: 'satline',
      polyline: {
        positions: [satpos, groundsatpos],
        width: 2,
        arcType: "NONE",
        material: new Cesium.PolylineDashMaterialProperty({
          color: Cesium.Color.fromBytes(0, 250, 154)
        })
      }
    });

    viewer.entities.add(satline);

    var truemidlon = calculatePerigeeLongitude(longitudeOfAscendingNode, parseFloat(ω) + (parseFloat(E) / 2));
    //  console.log(midlon,perigeeLatitude)
    var truemidlat = calculatePerigeeLatitude(inclination, parseFloat(ω) + (parseFloat(E) / 2));
    var truemidnpos = Cesium.Cartesian3.fromDegrees(truemidlon, truemidlat, satheight / 2);
    var midsatpos = Cesium.Cartesian3.fromDegrees(satlon, satlat, satheight / 2);

    var trueangle = new Cesium.Entity({
      id: 'trueangle',
      polyline: {
        positions: [Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, perigeeAltitude / 2), truemidnpos, midsatpos],
        width:8,
        material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.fromBytes(0, 250, 154))
      },


    });

    var trueanglelabel = new Cesium.Entity({
      id: 'trueanglelabel',
      position: truemidnpos,
      label: {
        font: '12pt Lucida Console',
        fillColor:Cesium.Color.fromBytes(0, 250, 154),
        pixelOffset: new Cesium.Cartesian2(20, -20),
        text: '平近点角'
      }
    });

  }
  else {
    var truemidlon = calculatePerigeeLongitude(longitudeOfAscendingNode, 73);
    var truemidlat = calculatePerigeeLatitude(inclination, 73);
    var truemidnpos = Cesium.Cartesian3.fromDegrees(truemidlon, truemidlat, semimajoraxis / 2);
    var midsatpos = Cesium.Cartesian3.fromDegrees(calculatePerigeeLongitude(longitudeOfAscendingNode, 104), calculatePerigeeLatitude(inclination, 104), semimajoraxis / 2);
    var satline = new Cesium.Entity({
      id: 'satline',
      polyline: {
        positions: [Cesium.Cartesian3.fromDegrees(calculatePerigeeLongitude(longitudeOfAscendingNode, 104), calculatePerigeeLatitude(inclination, 104), semimajoraxis-6778137), Cesium.Cartesian3.fromDegrees(calculatePerigeeLongitude(longitudeOfAscendingNode, 104), calculatePerigeeLatitude(inclination, 104), 0)],
        width: 2,
        arcType: "NONE",
        material: new Cesium.PolylineDashMaterialProperty({
          color: Cesium.Color.fromBytes(0, 250, 154)
        })
      }
    });

    viewer.entities.add(satline);
    var trueangle = new Cesium.Entity({
      id: 'trueangle',
      polyline: {
        positions: [Cesium.Cartesian3.fromDegrees(perigeeLongitude, perigeeLatitude, perigeeAltitude / 2), truemidnpos, midsatpos],
        width:8,
        material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.fromBytes(0, 250, 154))
      },


    });

    var trueanglelabel = new Cesium.Entity({
      id: 'trueanglelabel',
      position: truemidnpos,
      label: {
        font: '12pt Lucida Console',
        fillColor: Cesium.Color.fromBytes(0, 250, 154),
        pixelOffset: new Cesium.Cartesian2(20, -20),
        text: '平近点角',
        disableDepthTestDistance: Number.POSITIVE_INFINITY
        // text: '真近点角:' + E + '°'
      }
    });
  }
  var inclinationpos = new Cesium.Cartesian3.fromDegrees(calculatePerigeeLongitude(longitudeOfAscendingNode, 90), calculatePerigeeLatitude(inclination, 90), perigeeAltitude)
  var inclinationangle = new Cesium.Entity({
    id: 'inclinationangle',
    polyline: {
      positions: [Cesium.Cartesian3.fromDegrees(parseFloat(longitudeOfAscendingNode) + 90, 0, ascendingNodeAltitude), inclinationpos],
      width:8,
      material: new Cesium.PolylineArrowMaterialProperty(Cesium.Color.fromBytes(255, 127, 0))
    },
  });
  var inclinationanglelabel = new Cesium.Entity({
    id: 'inclinationanglelabel',
    position: new Cesium.Cartesian3.fromDegrees(calculatePerigeeLongitude(longitudeOfAscendingNode, 90), calculatePerigeeLatitude(inclination, 90) / 2, perigeeAltitude),
    label: {
      font: '12pt Lucida Console',
      fillColor: Cesium.Color.fromBytes(255, 127, 0),
      pixelOffset: new Cesium.Cartesian2(40, 10),
      text: '轨道倾角' 
      // text: '轨道倾角:' + inclination + '°'
    }
  });
  var orbitpoint = new Cesium.Entity({
    id: 'orbitpoint',
    label: {
      font: '10pt Lucida Console',
      fillColor: Cesium.Color.fromBytes(255, 127, 0),
      pixelOffset: new Cesium.Cartesian2(50, -24),
      text: '轨道面'
    },
    position: inclinationpos,
  });
  var equatorpos = new Cesium.Entity({
    id: 'equatorpos',
    label: {
      font: '10pt Lucida Console',
      fillColor: Cesium.Color.fromBytes(255, 127, 0),
      pixelOffset: new Cesium.Cartesian2(50, 14),
      text: '赤道面'
    },
    position: Cesium.Cartesian3.fromDegrees(parseFloat(longitudeOfAscendingNode) + 90, 0, ascendingNodeAltitude),
  });

  viewer.entities.add(npoint);
  viewer.entities.add(point);
  viewer.entities.add(spoint);
  viewer.entities.add(equator);
  viewer.entities.add(acendline);
  viewer.entities.add(acendangle);
  viewer.entities.add(acendanglelabel);
  viewer.entities.add(npointangle);
  viewer.entities.add(npoitntanglelabel);
  viewer.entities.add(semiMajorAxisline);
  viewer.entities.add(trueangle);
  viewer.entities.add(trueanglelabel);
  viewer.entities.add(inclinationangle);
  viewer.entities.add(inclinationanglelabel);
  viewer.entities.add(equatorpos);
  viewer.entities.add(orbitpoint);
}



function calculatePerigeeLongitude(longitudeOfAscendingNode, argumentOfPerigee) {

  const longitudeOfAscendingNodeRad = (Math.PI / 180) * longitudeOfAscendingNode;
  const argumentOfPerigeeRad = (Math.PI / 180) * argumentOfPerigee;

  const perigeeLongitude = (longitudeOfAscendingNodeRad + argumentOfPerigeeRad) % (2 * Math.PI);

  const perigeeLongitudeDeg = ((perigeeLongitude * 180 / Math.PI + 180) % 360) - 180;

  return perigeeLongitudeDeg;
}

function calculatePerigeeLatitude(inclination, argumentOfPerigee) {

  inclination = inclination * Math.PI / 180;
  argumentOfPerigee = argumentOfPerigee * Math.PI / 180;

  var periapsisLatitude = Math.atan(Math.tan(inclination) * Math.sin(argumentOfPerigee)) * 180 / Math.PI;


  return periapsisLatitude;
}


function calculateAscendingNodeAltitude(semiMajorAxis, eccentricity, radius) {
  const ascendingNodeAltitude = semiMajorAxis * (1 - eccentricity) - radius;

  return ascendingNodeAltitude;
}
var apos=[-3.823199,65.4235886,28368269.16476831]
var tpos=[38.896360629321265,176.19257412863277,28678462.754278094]
getascend(apos, '',tpos)


