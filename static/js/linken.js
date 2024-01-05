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

  return `${gregorianDT.year}year${gregorianDT.month}mongth${gregorianDT.day}day`;
}

function CesiumDateTimeFormatter(datetime, viewModel, ignoredate) {
  var julianDT = new Cesium.JulianDate();
  Cesium.JulianDate.addHours(datetime, 8, julianDT);
  var gregorianDT = Cesium.JulianDate.toGregorianDate(julianDT);

  let hour = gregorianDT.hour + "";
  let minute = gregorianDT.minute + "";
  return `${gregorianDT.day}day${hour.padStart(2, "0")}:${minute.padStart(2, "0")}`;
}

Cesium.Timeline.prototype.makeLabel = CesiumDateTimeFormatter;
var viewer = new Cesium.Viewer('cesiumContainer', {
  shouldAnimate: true,
  geocoder: false, 
  // infoBox: false,
  requestRenderMode: true, 
  scene3DOnly: false, 
  sceneMode: 3, 
  contextOptions: {
    webgl: {
      alpha: true,
    }
  },
});


viewer.baseLayerPicker.viewModel.selectedImagery = viewer.baseLayerPicker.viewModel.imageryProviderViewModels[3];
viewer.clock.shouldAnimate = true;
// viewer.animation.viewModel.dateFormatter = CesiumDateFormatter;
// viewer.animation.viewModel.timeFormatter = CesiumTimeFormatter;

czml='../static/czml/starlink/starlink.czml'
var stationdataSource = new Cesium.CzmlDataSource(czml);
stationdataSource.load(czml);
viewer.dataSources.add(stationdataSource);


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
viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(e) {
  e.cancel = true
  viewer.scene.camera.flyTo(homeCameraView);

})
// Set the initial position to China
var initialPosition = new Cesium.Cartesian3.fromDegrees(113.42, 34.16, 180000000);
var homeCameraView = {
  destination: initialPosition,
};
viewer.scene.camera.flyTo(homeCameraView);

  // Add Tian Maps annotations
  var imageryLayers = viewer.scene.imageryLayers;
  var tdtAnnoLayer = imageryLayers.addImageryProvider(new Cesium.WebMapTileServiceImageryProvider({
    url: "http://t0.tianditu.gov.cn/eia_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=eia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={TileMatrix}&TILEROW={TileRow}&TILECOL={TileCol}&tk=269b6942f19f345009e605301d0481c2",
    layer: "tdtAnnoLayer",
    style: "default",
    format: "image/jpeg",
    tileMatrixSetID: "GoogleMapsCompatible"
  }));

  var esriMap = new Cesium.ArcGisMapServerImageryProvider({
    url: 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer',
    enablePickFeatures: false
  });

  var esriMapModel = new Cesium.ProviderViewModel({
    name: 'esri Maps',
    iconUrl: Cesium.buildModuleUrl('./Widgets/Images/ImageryProviders/esriWorldImagery.png'),
    tooltip: 'ArcGIS Map Service',
    creationFunction: function () {
      return esriMap;
    }
  });
  var godMap = new Cesium.UrlTemplateImageryProvider({
    url: "http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
    enablePickFeatures: false
  });
  var godMapModel = new Cesium.ProviderViewModel({
    name: 'Gaode Maps',
    iconUrl: Cesium.buildModuleUrl('/static/images/mapicon/godicon.png'),
    tooltip: 'Gaode Map Service',
    creationFunction: function () {
      return godMap;
    }
  });
  var tencentMap = new Cesium.UrlTemplateImageryProvider({

    url: "https://p2.map.gtimg.com/sateTiles/{z}/{sx}/{sy}/{x}_{reverseY}.jpg?version=400",
    customTags: {
      sx: function (imageryProvider, x, y, level) {
        return x >> 4;
      },
      sy: function (imageryProvider, x, y, level) {
        return ((1 << level) - y) >> 4
      }
    }
  });

  var tencentMapModel = new Cesium.ProviderViewModel({
    name: 'Tencent Maps',
    iconUrl: Cesium.buildModuleUrl('/static/images/mapicon/tencenticon.png'),
    tooltip: 'Tencent Map Service',
    creationFunction: function () {
      return tencentMap;
    }
  });


 
  var providerViewModels = viewer.baseLayerPicker.viewModel.imageryProviderViewModels;
  providerViewModels.push(esriMapModel);
  providerViewModels.push(godMapModel);
  providerViewModels.push(tencentMapModel);
  viewer.baseLayerPicker.viewModel.imageryProviderViewModels = providerViewModels;
 


  function linkswitch(){

    var c1 = document.getElementById("c1");
    var c2 = document.getElementById("c2");
    var c3 = document.getElementById("c3");
      var c4 = document.getElementById("c4");
  
      if (c4.checked == true) {
       
      }
  
      for (var i = 0; i < stationdataSource.entities.values.length; i++) {
        var entities = stationdataSource.entities.values[i];
        if(c1.checked==true){
          if (entities._id == 'Satellite-ground link') {
              entities.polyline.show = true;
          }
        }
        if(c1.checked==false){
          
          if (entities._id == 'Satellite-ground link') {
            
              entities.polyline.show = false;
          }
        }
        if(c2.checked==true){
          if (entities._id == 'Same orbit plane inter-satellite link(C26-C23)'||entities._id == 'Same orbit plane inter-satellite link(C26-C24)'||entities._id == 'Same orbit plane inter-satellite link(C26-C25)'||entities._id == 'Same orbit plane inter-satellite link(C26-C37)') {
              entities.polyline.show = true;
          }
        }
        if(c2.checked!=true){
          if (entities._id == 'Same orbit plane inter-satellite link(C26-C23)'||entities._id == 'Same orbit plane inter-satellite link(C26-C24)'||entities._id == 'Same orbit plane inter-satellite link(C26-C25)'||entities._id == 'Same orbit plane inter-satellite link(C26-C37)'){
              entities.polyline.show = false;
          }
        }
        if(c3.checked==true){
          if (entities._id == 'Different orbit plane inter-satellite link(C26-C33)'||entities._id == 'Different orbit plane inter-satellite link(C26-C34)') {
              entities.polyline.show = true;
          }
        }
        if(c3.checked!=true){
          if (entities._id == 'Different orbit plane inter-satellite link(C26-C33)'||entities._id == 'Different orbit plane inter-satellite link(C26-C34)'){
              entities.polyline.show = false;
          }
        }
        if(c4.checked==true){
          if (entities._id == 'High-middle orbit plane inter-satellite link(C26-C38)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C39)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C61)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C60)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C59)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C40)') {
              entities.polyline.show = true;
          }
        }
        if(c4.checked!=true){
          if (entities._id == 'High-middle orbit plane inter-satellite link(C26-C38)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C39)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C61)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C60)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C59)'||entities._id == 'High-middle orbit plane inter-satellite link(C26-C40)'){
              entities.polyline.show = false;
          }
        }
  
  
      }
  
  
  }
function switchbar(){
  c=document.getElementById('control_bar')
  b=document.getElementById('openbar')
  console.log(b.style.display)
  if(c.style.display=='none'){
    b.style.display='none'
    c.style.display='block'
  }
  else{

    b.style.display='block'
    c.style.display='none'
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