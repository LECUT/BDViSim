Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMGNhYjhkOS00MGE2LTRkMDctOGZiYS1mZjc4MGQ0YmQyZTMiLCJpZCI6OTYzOTEsImlhdCI6MTY1NDQ5MDE5OH0.KMWej-d39eu-JXzFrpUTrc0rxYr0m5WcAriKMPSnqLs'

// cesium时钟时间格式化
function CesiumTimeFormatter(datetime, viewModel) {
  var julianDT = new Cesium.JulianDate();
  Cesium.JulianDate.addHours(datetime, 8, julianDT);
  var gregorianDT = Cesium.JulianDate.toGregorianDate(julianDT);

  let hour = gregorianDT.hour + "";
  let minute = gregorianDT.minute + "";
  let second = gregorianDT.second + "";
  return `${hour.padStart(2, "0")}:${minute.padStart(2, "0")}:${second.padStart(2, "0")}`;
}
//cesium时钟日期格式化
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
  // animation: false, //是否显示动画控件
  shouldAnimate: true,
  // homeButton: false, //是否显示Home按钮
  // fullscreenButton: false, //是否显示全屏按钮
  //  baseLayerPicker: false, //是否显示图层选择控件
  geocoder: false, //是否显示地名查找控件
  // timeline: false, //是否显示时间线控件
  // sceneModePicker: false, //是否显示投影方式控件
  // navigationHelpButton: false, //是否显示帮助信息控件
  // infoBox: false, //是否显示点击要素之后显示的信息
  requestRenderMode: true, //启用请求渲染模式
  scene3DOnly: false, //每个几何实例将只能以3D渲染以节省GPU内存
  sceneMode: 3, //初始场景模式 1 2D模式 2 2D循环模式 3 3D模式  Cesium.SceneMode
  contextOptions: {
    webgl: {
      alpha: true,
    }
  },
});

// viewer.scene.debugShowFramesPerSecond = true;
viewer.baseLayerPicker.viewModel.selectedImagery = viewer.baseLayerPicker.viewModel.imageryProviderViewModels[3];
// viewer.scene.skyBox.show = false //关闭天空盒，否则会显示天空颜色
//     //背景透明
// viewer.scene.backgroundColor = new Cesium.Color(0.0, 0.0, 0.0, 0.0);
//     //关闭大气
// viewer.scene.skyAtmosphere.show = false
//     //清除月亮太阳
// viewer.scene.moon.show = false
// viewer.scene.sun.show = false
viewer.clock.shouldAnimate = true;
viewer.animation.viewModel.dateFormatter = CesiumDateFormatter;
viewer.animation.viewModel.timeFormatter = CesiumTimeFormatter;

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

  // viewer.scene.globe.enableLighting = true;
  // viewer.shadows = true;

  // 亮度设置
  // var stages = viewer.scene.postProcessStages;
  // viewer.scene.brightness = viewer.scene.brightness || stages.add(Cesium.PostProcessStageLibrary.createBrightnessStage());
  // viewer.scene.brightness.enabled = true;
  // viewer.scene.brightness.uniforms.brightness = Number(1.2);

// 抗锯齿
  //是否开启抗锯齿
  if (Cesium.FeatureDetection.supportsImageRenderingPixelated()) {//判断是否支持图像渲染像素化处理
    viewer.resolutionScale = window.devicePixelRatio;
  }
  viewer.scene.fxaa = true;
  viewer.scene.postProcessStages.fxaa.enabled = true;
 

// 解决模型变黑
viewer.lightColor = new Cesium.Cartesian3(1000, 1000, 1000)

// 解决画面模糊
  viewer._cesiumWidget._supportsImageRenderingPixelated = Cesium.FeatureDetection.supportsImageRenderingPixelated();
  viewer._cesiumWidget._forceResize = true;
  if (Cesium.FeatureDetection.supportsImageRenderingPixelated()) {
    var vtxf_dpr = window.devicePixelRatio;
    // 适度降低分辨率
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
viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(e) {
  e.cancel = true
  viewer.scene.camera.flyTo(homeCameraView);

})
//设置初始位置为中国
var initialPosition = new Cesium.Cartesian3.fromDegrees(113.42, 34.16, 150000000);
var homeCameraView = {
  destination: initialPosition,
};
viewer.scene.camera.flyTo(homeCameraView);

//添加天地图标注
var imageryLayers = viewer.scene.imageryLayers;
var tdtAnnoLayer = imageryLayers.addImageryProvider(new Cesium.WebMapTileServiceImageryProvider({
  url: "http://t0.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={TileMatrix}&TILEROW={TileRow}&TILECOL={TileCol}&tk=269b6942f19f345009e605301d0481c2",
  layer: "tdtAnnoLayer",
  style: "default",
  format: "image/jpeg",
  tileMatrixSetID: "GoogleMapsCompatible"
}));



         var esriMap = new Cesium.ArcGisMapServerImageryProvider({
            url:'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer',
            enablePickFeatures:false
        });
        //设置ProviderViewModel：
        var esriMapModel = new Cesium.ProviderViewModel({
            name:'esri Maps',
            iconUrl:Cesium.buildModuleUrl('./Widgets/Images/ImageryProviders/esriWorldImagery.png'),
            tooltip:'ArcGIS 地图服务',
            creationFunction:function () {
                return esriMap;
            }
        });
        var godMap = new Cesium.UrlTemplateImageryProvider({
          url:"http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
          enablePickFeatures:false
        });
        var godMapModel = new Cesium.ProviderViewModel({
          name:'高德 Maps',
          iconUrl:Cesium.buildModuleUrl('/static/images/mapicon/godicon.png'),
          tooltip:'高德 地图服务',
          creationFunction:function () {
              return godMap;
          }
      });
      var tencentMap =new Cesium.UrlTemplateImageryProvider({
        // 影像图
        url: "https://p2.map.gtimg.com/sateTiles/{z}/{sx}/{sy}/{x}_{reverseY}.jpg?version=400",
        customTags: {
            sx: function(imageryProvider, x, y, level) {
                return x >> 4;
            },
            sy: function(imageryProvider, x, y, level) {
                return ((1 << level) - y) >> 4
            }
        }
     });

    var tencentMapModel = new Cesium.ProviderViewModel({
      name:'腾讯 Maps',
      iconUrl:Cesium.buildModuleUrl('/static/images/mapicon/tencenticon.png'),
      tooltip:'腾讯 地图服务',
      creationFunction:function () {
          return tencentMap;
      }
  });


      //新增
      var providerViewModels = viewer.baseLayerPicker.viewModel.imageryProviderViewModels;
      providerViewModels.push(esriMapModel);
      providerViewModels.push(godMapModel);
      providerViewModels.push(tencentMapModel);
      viewer.baseLayerPicker.viewModel.imageryProviderViewModels = providerViewModels;
 
//汉化
function replace2Chinese(){

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
    v2[0].title = "操作指南";//"操作指南(Navigation Instructions)"

    v2 = v1[0].getElementsByClassName("cesium-viewer-geocoderContainer");
    
	var v3 = v2[0].getElementsByClassName("cesium-geocoder-input");
	v3[0].title = "输入: 经度,纬度,视点高度(可选)。如：121,31.5,1000";
    v3[0].placeholder = "经度,纬度,高度。如：121,31.5,1000";
    //v2[0].innerHTML =
    //    '<img src="Cesium_1.49/Widgets/Images/ImageryProviders/earth3.png" width="30" height="30" />';


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
// replace2Chinese()

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