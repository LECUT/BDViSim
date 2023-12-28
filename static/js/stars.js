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

//cesium时间轴格式化
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
  sceneModePicker: true,
  baseLayerPicker:true,
    requestRenderMode: true, //启用请求渲染模式
  scene3DOnly: false, //每个几何实例将只能以3D渲染以节省GPU内存
  sceneMode: 3, //初始场景模式 1 2D模式 2 2D循环模式 3 3D模式  Cesium.SceneMode
  contextOptions: {
    webgl: {
      alpha: true,
    }
  },
  // vrButton: true
});
// viewer.scene.debugShowFramesPerSecond = true;

viewer.baseLayerPicker.viewModel.selectedImagery = viewer.baseLayerPicker.viewModel.imageryProviderViewModels[3];


viewer.clock.shouldAnimate = true;
viewer.animation.viewModel.dateFormatter = CesiumDateFormatter;
viewer.animation.viewModel.timeFormatter = CesiumTimeFormatter;

// viewer.scene.skyBox.show = false //关闭天空盒，否则会显示天空颜色
//     //背景透明
// viewer.scene.backgroundColor = new Cesium.Color(0.0, 0.0, 0.0, 0.0);
//     //关闭大气
// viewer.scene.skyAtmosphere.show = false
//     //清除月亮太阳
// viewer.scene.moon.show = false
// viewer.scene.sun.show = false

var satczml = '../static/czml/stellites.czml';

var satdata = new Cesium.CzmlDataSource(satczml);
satdata.load(satczml).then(function () {
  var sat = satdata.entities.values
  // console.log(obj)
  for (var i in sat) {
    if (sat[i]['_id'].search("points") != -1) {
      sat[i].polyline.show = false;
      sat[i].point.show = false;

    }
    if (sat[i]['_id'].search("points") == -1) {
      sat[i].billboard.scaleByDistance = new Cesium.NearFarScalar(150000000, 1.0, 900000000, 0);
      sat[i].label.scaleByDistance = new Cesium.NearFarScalar(1.5e2, 2.0, 250000000, 0);
      sat[i].label.eyeOffset = new Cesium.Cartesian3(0, 0, -10000)
      // console.log(sat[i].model)

    }
    // if(sat[i]['_id']=="C01(abnormality)" ){
    //   sat[i].billboard.show=false
    //   sat[i].label.show=false
    //   sat[i].model.show = false;
    //   sat[i].path.show = false;
    //   // console.log(sat[i].model)

    // }

  }

});
viewer.dataSources.add(satdata);



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
var initialPosition = new Cesium.Cartesian3.fromDegrees(113.42, 24.16, 150000000);
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
replace2Chinese()    
function flyTo(obj) {
  var object = $(obj).parents();
  var id = $(object).attr('id');
  id=id.substr(0,3)
  var sat = satdata.entities.values

  for (var i in sat) {
    if (sat[i]['_id'] == id) {
      viewer.selectedEntity = sat[i];
      viewer.infoBox.viewModel.show = false;
      viewer.flyTo(sat[i], {
        duration: 1,
        offset: new Cesium.HeadingPitchRange(0, -90, 3000000)
      });
      viewer.trackedEntity = sat[i];
      satPostDisplaySelected = sat[i]._id;
    }
  }
}
function switchpath(obj) {
  var object = $(obj).parents();
  var id = $(object).attr('id');
  id=id.substr(0,3)
  var sat = satdata.entities.values
  for (var i in sat) {
    if (sat[i]['_id'] == id) {
      if (obj.checked) {
        console.log(sat[i]['_id'])
        sat[i].path.show = true;
      }
      else {
        sat[i].path.show = false;
      }
    }
  }

}
function switchpoint(obj) {
  var object = $(obj).parents();
  var id = $(object).attr('id');
  id=id.substr(0,3)
  var sat = satdata.entities.values
  for (var i in sat) {
    if (sat[i]['_id'] == id + 'points') {
      console.log(sat[i]['_id'])
      if (obj.checked) {
        sat[i].polyline.show = true;
        sat[i].point.show = true;
      }
      else {
        sat[i].polyline.show = false;
        sat[i].point.show = false;
      }
    }
  }

}
function switchbillboard(obj) {
  var object = $(obj).parents();
  var id = $(object).attr('id');
  id=id.substr(0,3)
  var sat = satdata.entities.values
  for (var i in sat) {
    if (sat[i]['_id'] == id) {
      if (obj.checked) {
        sat[i].billboard.show = true;
        sat[i].label.show = true;
        sat[i].model.show = true;
      }
      else {
        console.log(sat[i])
        sat[i].billboard.show = false;
        sat[i].label.show = false;
        sat[i].model.show = false;
      }
    }
  }
}
// 未使用
function switchAllpath(obj) {
  var sat = satdata.entities.values
  for (var i in sat) {
    if (obj.checked) {
      sat[i].path.show = true;
    }
    else {
      sat[i].path.show = false;
    }
  }
}
// 未使用
function switchAllpoint(obj) {
  var sat = satdata.entities.values
  for (var i in sat) {
    if (obj.checked) {
      sat[i].polyline.show = true;
      sat[i].point.show = true;
    }
    else {
      sat[i].polyline.show = false;
      sat[i].point.show = false;
    }
  }

}
// function showall(){
//   var allsats=document.getElementsByTagName('li')
//   console.log(allsats)
//   for(var i=0;i<allsats.length;i++){
//     var obj2 = allsats[i].getElementsByTagName('input');
//     if(allsats[i].style.display=='block'){
//       obj2[0].checked = true;
//       obj2[2].checked = true;
//       var sat = satdata.entities.values
//       for (var j in sat) {
//         if (sat[j].id == allsats[i].id.substr(0,3) ) {
//           sat[j].billboard.show = true;
//           sat[j].path.show = true;
//           sat[j].label.show = true;
//           sat[j].model.show = true;
//         }
//       }
//     }
//     else{
//       obj2[0].checked = false;
//       obj2[2].checked = false;
//       var sat = satdata.entities.values
//       for (var j in sat) {
//         if (sat[j].id == allsats[i].id.substr(0,3) ) {
//           sat[j].billboard.show = false;
//           sat[j].path.show = false;
//           sat[j].label.show =false;
//           sat[j].model.show = false;
//         }
//       }
//     }
//   }
// }
function showall(){
  var sat1=document.getElementById('sat_all').children[0].children
  var sat2=document.getElementById('sat_all').children[1].children
  var sat3=document.getElementById('sat_all').children[2].children
  
  for(var i=0;i<sat1.length;i++){
    var obj2 = sat1[i].getElementsByTagName('input');
    var sat = satdata.entities.values
    if(sat1[i].style.display=='block'&& document.getElementById('sat_all').children[0].style.display=='block')
    {     
      obj2[0].checked = true;
      obj2[2].checked = true;
      for (var j in sat) {

            if (sat[j].id == sat1[i].id.substr(0,3) ) {
              sat[j].billboard.show = true;
              sat[j].path.show = true;
              sat[j].label.show = true;
              sat[j].model.show = true;
            }
      }
    }
    else{
      obj2[0].checked = false;
      obj2[2].checked = false;
      for (var j in sat) {
        if (sat[j].id == sat1[i].id.substr(0,3) ) {
          sat[j].billboard.show = false;
          sat[j].path.show = false;
          sat[j].label.show = false;
          sat[j].model.show = false;
        }
      }}
  }
  for(var i=0;i<sat2.length;i++){
    var obj2 = sat2[i].getElementsByTagName('input');

    var sat = satdata.entities.values
    if(sat2[i].style.display=='block'&& document.getElementById('sat_all').children[1].style.display=='block')
    {
      obj2[0].checked = true;
      obj2[2].checked = true;
    for (var j in sat) {
          if (sat[j].id == sat2[i].id.substr(0,3)) {
            sat[j].billboard.show = true;
            sat[j].path.show = true;
            sat[j].label.show = true;
            sat[j].model.show = true;
          }}
    }
    else{
      obj2[0].checked = false;
      obj2[2].checked = false;
      for (var j in sat) {
        if (sat[j].id == sat2[i].id.substr(0,3) ) {
          sat[j].billboard.show = false;
          sat[j].path.show = false;
          sat[j].label.show = false;
          sat[j].model.show = false;
        }
      }
    }
  }
  for(var i=0;i<sat3.length;i++){
    var obj2 = sat3[i].getElementsByTagName('input');

    var sat = satdata.entities.values
    if(sat3[i].style.display=='block'&& document.getElementById('sat_all').children[2].style.display=='block')
    {
      obj2[0].checked = true;
      obj2[2].checked = true;
    for (var j in sat) {
          if (sat[j].id == sat3[i].id.substr(0,3)) {
            sat[j].billboard.show = true;
            sat[j].path.show = true;
            sat[j].label.show = true;
            sat[j].model.show = true;
          }}
    }
    else{
      obj2[0].checked = false;
      obj2[2].checked = false;
      for (var j in sat) {
        if (sat[j].id == sat3[i].id.substr(0,3) ) {
          sat[j].billboard.show = false;
          sat[j].path.show = false;
          sat[j].label.show = false;
          sat[j].model.show = false;
        }
      }
    }
  }

}
function closeall() {
  var sat1=document.getElementById('sat_all').children[0].children
  var sat2=document.getElementById('sat_all').children[1].children
  var sat3=document.getElementById('sat_all').children[2].children
  if(bds_2.style.display=='block'){
    for(var i=0;i<sat1.length;i++){
      if(sat1[i].style.display=='block'){
        var obj = sat1[i].getElementsByTagName('input');
        var sat = satdata.entities.values
        obj[0].checked = false;
        obj[2].checked = false;
        for (var j in sat) {
          if (sat[j].id == sat1[i].id.substr(0,3)) {
            sat[j].billboard.show = false;
            sat[j].path.show = false;
            sat[j].label.show = false;
            sat[j].model.show = false;
          }}
      }
    }
  }
  if(bds_3.style.display=='block'){
    for(var i=0;i<sat2.length;i++){
      if(sat2[i].style.display=='block'){
        var obj = sat2[i].getElementsByTagName('input');
        var sat = satdata.entities.values
        obj[0].checked = false;
        obj[2].checked = false;
        for (var j in sat) {
          if (sat[j].id == sat2[i].id.substr(0,3)) {
            sat[j].billboard.show = false;
            sat[j].path.show = false;
            sat[j].label.show = false;
            sat[j].model.show = false;
          }}
      }
    }
  }
  if(bds_3S.style.display=='block'){
    for(var i=0;i<sat3.length;i++){
      if(sat3[i].style.display=='block'){
        var obj = sat3[i].getElementsByTagName('input');
        var sat = satdata.entities.values
        obj[0].checked = false;
        obj[2].checked = false;
        for (var j in sat) {
          if (sat[j].id == sat3[i].id.substr(0,3)) {
            sat[j].billboard.show = false;
            sat[j].path.show = false;
            sat[j].label.show = false;
            sat[j].model.show = false;
          }}
      }
    }
  }
}


function switchAllsat(obj) {
  id = $("input[name='picksats']:checked").val();
  var sat = satdata.entities.values
  
  for (var i in sat) {
    if (obj.checked) {
      if (id == "sat_all") {
        sat[i].billboard.show = true;
        sat[i].path.show = true;
        sat[i].label.show = true;
      }
      if (id == "sat_igso") {
        if (sat[i].id.indexOf("IGSO") != -1 || sat[i].id == 'BEIDOU 8 (C08)' || sat[i].id == 'BEIDOU 5 (C06)' || sat[i].id == 'BEIDOU 9 (C09)' || sat[i].id == 'BEIDOU 7 (C07)' || sat[i].id == 'BEIDOU 20 (C18)' || sat[i].id == 'BEIDOU 17 (C31)' || sat[i].id == 'BEIDOU 10 (C10)') {
          sat[i].billboard.show = true;
          sat[i].path.show = true;
          sat[i].label.show = true;
        }
        else {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
      }
      if (id == "sat_geo") {
        if (sat[i].id.indexOf("G2") != -1 || sat[i].id.indexOf("G1") != -1 || sat[i].id.indexOf("G7") != -1 || sat[i].id.indexOf("G3") != -1 || sat[i].id.indexOf("G8") != -1 || sat[i].id == 'BEIDOU 3 (C01)' || sat[i].id == 'BEIDOU 6 (C04)' || sat[i].id == 'BEIDOU 16 (C02)' || sat[i].id == 'BEIDOU 11 (C05)') {
          sat[i].billboard.show = true;
          sat[i].path.show = true;
          sat[i].label.show = true;
        }
        else {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
      }
      if (id == "sat_meo") {
        if (sat[i].id.indexOf("IGSO") != -1 || sat[i].id == 'BEIDOU 8 (C08)' || sat[i].id == 'BEIDOU 5 (C06)' || sat[i].id == 'BEIDOU 9 (C09)' || sat[i].id == 'BEIDOU 7 (C07)' || sat[i].id == 'BEIDOU 20 (C18)' || sat[i].id == 'BEIDOU 17 (C31)' || sat[i].id == 'BEIDOU 10 (C10)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else if (sat[i].id.indexOf("G2") != -1 || sat[i].id.indexOf("G1") != -1 || sat[i].id.indexOf("G7") != -1 || sat[i].id.indexOf("G3") != -1 || sat[i].id.indexOf("G8") != -1 || sat[i].id == 'BEIDOU 3 (C01)' || sat[i].id == 'BEIDOU 6 (C04)' || sat[i].id == 'BEIDOU 16 (C02)' || sat[i].id == 'BEIDOU 11 (C05)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else {
          sat[i].billboard.show = true;
          sat[i].path.show = true;
          sat[i].label.show = true;
        }
      }
    }
    else {
      if (id == "sat_all") {
        sat[i].billboard.show = false;
        sat[i].path.show = false;
        sat[i].label.show = false;
      }
      if (id == "sat_igso") {
        if (sat[i].id.indexOf("IGSO") != -1 || sat[i].id == 'BEIDOU 8 (C08)' || sat[i].id == 'BEIDOU 5 (C06)' || sat[i].id == 'BEIDOU 9 (C09)' || sat[i].id == 'BEIDOU 7 (C07)' || sat[i].id == 'BEIDOU 20 (C18)' || sat[i].id == 'BEIDOU 17 (C31)' || sat[i].id == 'BEIDOU 10 (C10)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
      }
      if (id == "sat_geo") {
        if (sat[i].id.indexOf("G2") != -1 || sat[i].id.indexOf("G1") != -1 || sat[i].id.indexOf("G7") != -1 || sat[i].id.indexOf("G3") != -1 || sat[i].id.indexOf("G8") != -1 || sat[i].id == 'BEIDOU 3 (C01)' || sat[i].id == 'BEIDOU 6 (C04)' || sat[i].id == 'BEIDOU 16 (C02)' || sat[i].id == 'BEIDOU 11 (C05)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
      }
      if (id == "sat_meo") {
        if (sat[i].id.indexOf("IGSO") != -1 || sat[i].id == 'BEIDOU 8 (C08)' || sat[i].id == 'BEIDOU 5 (C06)' || sat[i].id == 'BEIDOU 9 (C09)' || sat[i].id == 'BEIDOU 7 (C07)' || sat[i].id == 'BEIDOU 20 (C18)' || sat[i].id == 'BEIDOU 17 (C31)' || sat[i].id == 'BEIDOU 10 (C10)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else if (sat[i].id.indexOf("G2") != -1 || sat[i].id.indexOf("G1") != -1 || sat[i].id.indexOf("G7") != -1 || sat[i].id.indexOf("G3") != -1 || sat[i].id.indexOf("G8") != -1 || sat[i].id == 'BEIDOU 3 (C01)' || sat[i].id == 'BEIDOU 6 (C04)' || sat[i].id == 'BEIDOU 16 (C02)' || sat[i].id == 'BEIDOU 11 (C05)') {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
        else {
          sat[i].billboard.show = false;
          sat[i].path.show = false;
          sat[i].label.show = false;
        }
      }
    }

  }
}

function picksats() {

  // id = $("input[name='picksats']:checked").val();
  var b2 = document.getElementById("bds_2");
  var b3 = document.getElementById("bds_3");
  var sat_igso = document.getElementsByClassName('sat_igso')
  var sat_geo = document.getElementsByClassName('sat_geo')
  var sat_meo = document.getElementsByClassName('sat_meo')
  var satnumbers=document.getElementById("satnums");
  var allsats=document.getElementsByTagName('li')

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

  satnumbers.value=numscal()
}

function numscal(){
  var sat_igso = document.getElementsByClassName('sat_igso')
  var sat_geo = document.getElementsByClassName('sat_geo')
  var sat_meo = document.getElementsByClassName('sat_meo')
  var b2 = document.getElementById("bds_2");
  var b3 = document.getElementById("bds_3");
  var sat1=document.getElementById('sat_all').children[0].children
  var sat2=document.getElementById('sat_all').children[1].children
  var sat3=document.getElementById('sat_all').children[2].children
  var satnums=0
  var allsats=document.getElementsByTagName('li')
  if(document.getElementById('sat_all').children[0].style.display=='block'){
    for(var i=0;i<sat1.length;i++){
      if (sat1[i].style.display=='block')
      {
        satnums+=1
      }
    }
  }
  if(document.getElementById('sat_all').children[1].style.display=='block'){
    for(var i=0;i<sat2.length;i++){
      if (sat2[i].style.display=='block')
      {
        satnums+=1
      }
    }
  }
  if(document.getElementById('sat_all').children[2].style.display=='block'){
    for(var i=0;i<sat3.length;i++){
      if (sat3[i].style.display=='block')
      {
        satnums+=1
      }
    }
  }
  console.log(satnums)
 return satnums
}

function switchbar(){
  c=document.getElementById('panel')
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