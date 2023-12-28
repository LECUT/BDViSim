

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMGNhYjhkOS00MGE2LTRkMDctOGZiYS1mZjc4MGQ0YmQyZTMiLCJpZCI6OTYzOTEsImlhdCI6MTY1NDQ5MDE5OH0.KMWej-d39eu-JXzFrpUTrc0rxYr0m5WcAriKMPSnqLs'

var viewer = new Cesium.Viewer('cesiumContainer', {
  selectionIndicator: false,//关闭绿色点击框
  animation: false, //是否显示动画控件
  homeButton: false, //是否显示Home按钮
  fullscreenButton: false, //是否显示全屏按钮
  baseLayerPicker: false, //是否显示图层选择控件
  geocoder: false, //是否显示地名查找控件
  timeline: false, //是否显示时间线控件
  sceneModePicker: false, //是否显示投影方式控件
  navigationHelpButton: false, //是否显示帮助信息控件
  infoBox: false, //是否显示点击要素之后显示的信息
  requestRenderMode: true, //启用请求渲染模式
  scene3DOnly: false, //每个几何实例将只能以3D渲染以节省GPU内存
  sceneMode: 3, //初始场景模式 1 2D模式 2 2D循环模式 3 3D模式  Cesium.SceneMode
  fullscreenElement: document.body, //全屏时渲染的HTML元素 暂时没发现用处
  contextOptions: {
    webgl: {
      alpha: true,
    }
  },
  // vrButton: true
});
// viewer.scene.debugShowFramesPerSecond = true;
this.viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({
  // 影像图

  url: "http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
}))





var satczml = '../static/czml/mainview/satview.czml';
var satdata = new Cesium.CzmlDataSource(satczml);
satdata.load(satczml).then(function () {
  var sat = satdata.entities.values
  // console.log(sat)
  sat[0].label.show = false
  sat[0].path.show = false;
  // sat[0].model.shadows =  false,
  sat[0].model.show = false
})
// viewer.dataSources.add(satdata);


var satczml2 = '../static/czml/mainview/satview2.czml';
var satdata2 = new Cesium.CzmlDataSource(satczml2);
satdata2.load(satczml2).then(function () {
  var sat2 = satdata2.entities.values
  sat2[0].label.show = false
  sat2[0].path.show = false;
  sat2[0].model.show = false

});
// viewer.dataSources.add(satdata2);

var satczml3 = '../static/czml/mainview/satview3.czml';
var satdata3 = new Cesium.CzmlDataSource(satczml3);
satdata3.load(satczml3).then(function () {
  var sat3 = satdata3.entities.values
  sat3[0].label.show = false
  sat3[0].path.show = false;
  sat3[0].model.show = false

});
// viewer.dataSources.add(satdata3);
viewer.clock.shouldAnimate = true;
viewer.clock.multiplier = 300;
// setTimeout(() => {
//   viewer.clock.multiplier = 800;
// }, 10000);
// setTimeout(() => {
//   viewer.clock.multiplier = 500;
// }, 12000);
// setTimeout(() => {
//   viewer.clock.multiplier = 300;
// }, 3000);

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

//设置初始位置为中国
var initialPosition = new Cesium.Cartesian3.fromDegrees(113.42, 10.16, 24000000);
var homeCameraView = {
  destination: initialPosition,
};
setTimeout(() => {
  viewer.scene.camera.flyTo(homeCameraView);


}, 2000);


function switchorbits() {
  var div1 = document.getElementById("loadorbits");
  if (div1.style.display != "block") {

    div1.style.display = "block";

  }
  else {
    div1.style.display = "none";
  }
}

var temp
function upload(input) {

  if (window.FileReader) {
    var file = input.files[0];
    filename = file.name.split(".")[0];
    var reader = new FileReader();
    reader.onload = function () {

      temp = this.result;

      temp = temp.split("\n");


      return temp;
    }
    reader.readAsText(file)
  }
  else {
    alert('error');
  }
}




$("#btnupload").on("click", function () {
  id = document.getElementById('orbits').value;

  var formdata = temp

  var satid = document.getElementById('newselect').value;
  objecttime = document.getElementById('objtime').value
  year = objecttime.slice(0, 4)
  month = objecttime.slice(6, 7)
  day = objecttime.slice(8, 10)



  url = '/' + id
  alert('Loading...')
  
  $.ajax({
    type: "post",
    url: url,//url地址
    contentType: "application/json;charset=UTF-8",
    dataType: "json",
    data: JSON.stringify({ data: formdata, year: year, month: month, day: day }),
    success: function (res) {
      console.log(url)
      if (url == '/TLE') {
        result = res[1]
        result2 = res[0]
        alert("Success")
        newset();
        return result, result2
      }
      if (url == '/Rinex') {
        result3 = res
        alert("Success")
        newset();
        return result3
      }
      if (url == '/SP3') {
        result4 = res
        alert("Success")
        newset();


        return result4
      }
      if (url == '/YUMA') {
        result5 = res
        alert("Success")
        newset();
        return result5
      }





      alert("Success")
      newset();
    }
  });


});

function choseback() {
  var div1 = document.getElementById("div1");
  var div2 = document.getElementById("div2");
  var div3 = document.getElementById("div3");
  var div4 = document.getElementById("div4");
  cal.style.display = 'block';
  if (div1.style.display == 'block') {

    l1.style.background = ' rgb(211, 224, 222)';
  }
  if (div1.style.display == 'none') {
    l1.style.background = 'transparent';
  }
  if (div2.style.display == 'block') {
    l2.style.background = ' rgb(211, 224, 222)';
  }
  if (div2.style.display == 'none') {
    l2.style.background = 'transparent';
  }
  if (div3.style.display == 'block') {
    l3.style.background = ' rgb(211, 224, 222)';
  }
  if (div3.style.display == 'none') {
    l3.style.background = 'transparent';
  }
  if (div4.style.display == 'block') {
    l4.style.background = ' rgb(211, 224, 222)';
  }
  if (div4.style.display == 'none') {
    l4.style.background = 'transparent';
  }
}
function showDiv1() {
  var div1 = document.getElementById("div1");
  var div2 = document.getElementById("div2");
  var div3 = document.getElementById("div3");
  var div4 = document.getElementById("div4");
  var div5 = document.getElementById("div5");
  var c1 = document.getElementById("check1");

  if (c1.checked == true) {
    div1.style.display = 'block';
    div2.style.display = 'none';
    div3.style.display = 'none';
    div5.style.display = 'none';
    div4.style.display = 'none';

  }
  choseback();

}
function showDiv2() {
  var div1 = document.getElementById("div1");
  var div2 = document.getElementById("div2");
  var div3 = document.getElementById("div3");
  var div4 = document.getElementById("div4");
  var div5 = document.getElementById("div5");
  var c2 = document.getElementById("check2");
  if (c2.checked == true) {
    div2.style.display = 'block';
    div1.style.display = 'none';
    div3.style.display = 'none';
    div5.style.display = 'none';
    div4.style.display = 'none';
  }
  choseback();
}
function showDiv3() {
  var div1 = document.getElementById("div1");
  var div2 = document.getElementById("div2");
  var div3 = document.getElementById("div3");
  var div4 = document.getElementById("div4");
  var c3 = document.getElementById("check3");
  var div5 = document.getElementById("div5");
  if (c3.checked == true) {
    div3.style.display = 'block';
    div2.style.display = 'none';
    div1.style.display = 'none';
    div4.style.display = 'none';
    div5.style.display = 'none';
  }
  choseback();
}
function showDiv4() {
  var div1 = document.getElementById("div1");
  var div2 = document.getElementById("div2");
  var div3 = document.getElementById("div3");
  var div4 = document.getElementById("div4");
  var c4 = document.getElementById("check4");
  var div5 = document.getElementById("div5");
  if (c4.checked == true) {
    div4.style.display = 'block';
    div3.style.display = 'none';
    div2.style.display = 'none';
    div1.style.display = 'none';
    div5.style.display = 'none';
  }
  choseback();
}


//写文件
var saveAs = saveAs || (function (view) {
  "use strict";
  // IE <10 is explicitly unsupported
  if (typeof view === "undefined" || typeof navigator !== "undefined" && /MSIE [1-9]\./.test(navigator.userAgent)) {
    return;
  }
  var
    doc = view.document
    // only get URL when necessary in case Blob.js hasn't overridden it yet
    , get_URL = function () {
      return view.URL || view.webkitURL || view;
    }
    , save_link = doc.createElementNS("http://www.w3.org/1999/xhtml", "a")
    , can_use_save_link = "download" in save_link
    , click = function (node) {
      var event = new MouseEvent("click");
      node.dispatchEvent(event);
    }
    , is_safari = /constructor/i.test(view.HTMLElement) || view.safari
    , is_chrome_ios = /CriOS\/[\d]+/.test(navigator.userAgent)
    , throw_outside = function (ex) {
      (view.setImmediate || view.setTimeout)(function () {
        throw ex;
      }, 0);
    }
    , force_saveable_type = "application/octet-stream"
    // the Blob API is fundamentally broken as there is no "downloadfinished" event to subscribe to
    , arbitrary_revoke_timeout = 1000 * 40 // in ms
    , revoke = function (file) {
      var revoker = function () {
        if (typeof file === "string") { // file is an object URL
          get_URL().revokeObjectURL(file);
        } else { // file is a File
          file.remove();
        }
      };
      setTimeout(revoker, arbitrary_revoke_timeout);
    }
    , dispatch = function (filesaver, event_types, event) {
      event_types = [].concat(event_types);
      var i = event_types.length;
      while (i--) {
        var listener = filesaver["on" + event_types[i]];
        if (typeof listener === "function") {
          try {
            listener.call(filesaver, event || filesaver);
          } catch (ex) {
            throw_outside(ex);
          }
        }
      }
    }
    , auto_bom = function (blob) {
      // prepend BOM for UTF-8 XML and text/* types (including HTML)
      // note: your browser will automatically convert UTF-16 U+FEFF to EF BB BF
      if (/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) {
        return new Blob([String.fromCharCode(0xFEFF), blob], { type: blob.type });
      }
      return blob;
    }
    , FileSaver = function (blob, name, no_auto_bom) {
      if (!no_auto_bom) {
        blob = auto_bom(blob);
      }
      // First try a.download, then web filesystem, then object URLs
      var
        filesaver = this
        , type = blob.type
        , force = type === force_saveable_type
        , object_url
        , dispatch_all = function () {
          dispatch(filesaver, "writestart progress write writeend".split(" "));
        }
        // on any filesys errors revert to saving with object URLs
        , fs_error = function () {
          if ((is_chrome_ios || (force && is_safari)) && view.FileReader) {
            // Safari doesn't allow downloading of blob urls
            var reader = new FileReader();
            reader.onloadend = function () {
              var url = is_chrome_ios ? reader.result : reader.result.replace(/^data:[^;]*;/, 'data:attachment/file;');
              var popup = view.open(url, '_blank');
              if (!popup) view.location.href = url;
              url = undefined; // release reference before dispatching
              filesaver.readyState = filesaver.DONE;
              dispatch_all();
            };
            reader.readAsDataURL(blob);
            filesaver.readyState = filesaver.INIT;
            return;
          }
          // don't create more object URLs than needed
          if (!object_url) {
            object_url = get_URL().createObjectURL(blob);
          }
          if (force) {
            view.location.href = object_url;
          } else {
            var opened = view.open(object_url, "_blank");
            if (!opened) {
              // Apple does not allow window.open, see https://developer.apple.com/library/safari/documentation/Tools/Conceptual/SafariExtensionGuide/WorkingwithWindowsandTabs/WorkingwithWindowsandTabs.html
              view.location.href = object_url;
            }
          }
          filesaver.readyState = filesaver.DONE;
          dispatch_all();
          revoke(object_url);
        }
        ;
      filesaver.readyState = filesaver.INIT;

      if (can_use_save_link) {
        object_url = get_URL().createObjectURL(blob);
        setTimeout(function () {
          save_link.href = object_url;
          save_link.download = name;
          click(save_link);
          dispatch_all();
          revoke(object_url);
          filesaver.readyState = filesaver.DONE;
        });
        return;
      }

      fs_error();
    }
    , FS_proto = FileSaver.prototype
    , saveAs = function (blob, name, no_auto_bom) {
      return new FileSaver(blob, name || blob.name || "download", no_auto_bom);
    }
    ;
  // IE 10+ (native saveAs)
  if (typeof navigator !== "undefined" && navigator.msSaveOrOpenBlob) {
    return function (blob, name, no_auto_bom) {
      name = name || blob.name || "download";

      if (!no_auto_bom) {
        blob = auto_bom(blob);
      }
      return navigator.msSaveOrOpenBlob(blob, name);
    };
  }

  FS_proto.abort = function () { };
  FS_proto.readyState = FS_proto.INIT = 0;
  FS_proto.WRITING = 1;
  FS_proto.DONE = 2;

  FS_proto.error =
    FS_proto.onwritestart =
    FS_proto.onprogress =
    FS_proto.onwrite =
    FS_proto.onabort =
    FS_proto.onerror =
    FS_proto.onwriteend =
    null;

  return saveAs;
}(
  typeof self !== "undefined" && self
  || typeof window !== "undefined" && window
  || this.content
));
// `self` is undefined in Firefox for Android content script context
// while `this` is nsIContentFrameMessageManager
// with an attribute `content` that corresponds to the window

if (typeof module !== "undefined" && module.exports) {
  module.exports.saveAs = saveAs;
} else if ((typeof define !== "undefined" && define !== null) && (define.amd !== null)) {
  define("FileSaver.js", function () {
    return saveAs;
  });
}



function closeorbit() {

  document.getElementById("orbit_cal").style.display = "none";

}








var satid = "s";


a = $.ajax({
  url: "../static/json/orbit_info.json",//json文件位置，文件名
  type: "GET",//请求方式为get
  dataType: "json", //返回数据格式为json
  async: false,
  success: function (data) {
  }
});
b = $.ajax({
  url: "../static/json/satellite_info.json",//json文件位置，文件名
  type: "GET",//请求方式为get
  dataType: "json", //返回数据格式为json
  async: false,
  success: function (data) {
  }
});
C = $.ajax({
  url: "../static/json/satellite_info2.json",//json文件位置，文件名
  type: "GET",//请求方式为get
  dataType: "json", //返回数据格式为json
  async: false,
  success: function (data) {
  }
});

d = $.ajax({
  url: "../static/json/satellite_info3.json",//json文件位置，文件名
  type: "GET",//请求方式为get
  dataType: "json", //返回数据格式为json
  async: false,
  success: function (data) {
  }
});
e = $.ajax({
  url: "../static/json/satellite_info4.json",//json文件位置，文件名
  type: "GET",//请求方式为get
  dataType: "json", //返回数据格式为json
  async: false,
  success: function (data) {

  }
});

//   var result3=''
//   $.getJSON("../static/json/satellite_info2.json", function (data) {

//     result3=data
// });
result = $.parseJSON(a["responseText"]);
result2 = $.parseJSON(b["responseText"]);
result3 = $.parseJSON(C["responseText"]);
result4 = $.parseJSON(d["responseText"]);
result5 = $.parseJSON(e["responseText"]);

for (var i in result2) {
  if ($.isEmptyObject(result2[i]) == true) {
    delete result2[i]
  }
}
for (var i in result3) {
  if (i == 'num') { continue }
  if ($.isEmptyObject(result3[i]) == true) {
    delete result3[i]
  }
}
for (var i in result4) {
  if ($.isEmptyObject(result4[i]) == true) {
    delete result4[i]
  }
}
for (var i in result5) {
  if ($.isEmptyObject(result5[i]) == true) {
    delete result5[i]
  }
}

var datepick = document.getElementById("datepick")
objtime.value = result3['objtime'].replace("T", " ");
endtime.value = result3['endtime'].replace("T", " ");
datepick.value=result3['objtime'].substring(0, 10)

function newset() {
  // objtime.value = result3['objtime'].replace("T", " ");
  // endtime.value = result3['endtime'].replace("T", " ");
  id = document.getElementById('newselect').value;
  if (!window.result[id]) {



  }
  else {
    n1.value = result[id]['norda'];
    n2.value = result[id]['internationalid'];
    n3.value = result[id]['time'];
    n4.value = result[id]['l1'];
    n5.value = result[id]['l2'];
    n6.value = result[id]['bstar'];
    n7.value = result[id]['Classification'];
    n8.value = result[id]['tlecounts'];

    input3.value = result[id]["Inclination"];
    input4.value = result[id]["Right_Ascension_of_the_Ascending_Node"];
    input5.value = result[id]["Eccentricity"];
    input6.value = result[id]["Argument_of_Perigee"];
    input7.value = result[id]["Mean_Anomaly"];
    input8.value = result[id]["Mean_Motion"];
    n10.value = result[id]['alreadyflys'];
  }


  if (!window.result3[id]) {



  }
  else {
    for (var i = 0; i < result3.num; i++) {
      str = 'in' + i
      if (result3[str].PRN == id) {
        in1.value = result3[str].PRN;
        in2.value = result3[str].epoch.replace("T", " ");
        in3.value = result3[str].a_0;
        in4.value = result3[str].a_1;
        in5.value = result3[str].a_2;
        in6.value = result3[str].IODE;
        in7.value = result3[str].C_rs;
        in8.value = result3[str].sn;
        in9.value = result3[str].M0;
        in10.value = result3[str].C_uc;
        in11.value = result3[str].e;
        in12.value = result3[str].C_us;
        in13.value = result3[str].sqrt_A;
        in14.value = result3[str].TOE;
        in15.value = result3[str].C_ic;
        in16.value = result3[str].OMEGA;
        in17.value = result3[str].C_is;
        in18.value = result3[str].I_0;
        in19.value = result3[str].C_rc;
        in20.value = result3[str].w;
        in21.value = result3[str].OMEGA_DOT;
        in22.value = result3[str].IDOT
        in23.value = result3[str].L2_code
        in24.value = result3[str].PS_week_num
        in25.value = result3[str].L2_P_code
        in26.value = result3[str].wxjd
        in27.value = result3[str].wxjkzt;
        in28.value = result3[str].TGD1
        in29.value = result3[str].TGD2
        in30.value = result3[str].transmission_time
        in31.value = result3[str].IODC;
      }
    }
  }


  if (!window.result5[id]) {



  }
  
  else {
    for (var i = 0; i < result5['counts']['nums']; i++) {
      str = 'sat' + i

      if (result5[str].ID == id.slice(1, 3)) {
        in01.value = result5[str].ID;
        in02.value = result5[str].Health;
        in03.value = result5[str].Eccentricity;
        in04.value = result5[str]["Time_of_Applicability(s)"];
        in05.value = result5[str]["Orbital_Inclination(rad)"];
        in06.value = result5[str]["Rate_of_Right_Ascen(r/s)"];
        in07.value = result5[str]["Right_Ascen_at_Week(rad)"];
        in08.value = result5[str]["SQRT(A)(m_1/2)"];
        in09.value = result5[str]["Argument_of_Perigee(rad)"];
        in010.value = result5[str]["Mean_Anom(rad)"];
        in011.value = result5[str]["Af0(s)"];
        in012.value = result5[str]["Af1(s/s)"];
        in013.value = result5[str].week;
      }
    }
  }

  var tdt = ''
  var tdx = ''
  var tdy = ''
  var tdz = ''
  var tdg = ''
  // sp3text.value = "\t\t\t时间\t\t\t\t\t\t\tX\t\t\t\t\t\t\tY\t\t\t\t\t\t\tZ\t\t\t\t\t钟差\n";
  if(result4=='false')
  {
    td_t1.textContent = "缺少SP3数据"
    td_x1.textContent = ""
    td_y1.textContent = ""
    td_z1.textContent = ""
    td_g1.textContent = ""
    td_time.textContent = ""
    td_x.textContent = ""
    td_y.textContent = ""
    td_z.textContent = ""
    td_g.textContent = ""
  }
  else{
    if (!window.result4[id]) {

      // sp3text.value ="SP3无该颗卫星数据"
      td_t1.textContent = "SP3无该颗卫星数据"
      td_x1.textContent = ""
      td_y1.textContent = ""
      td_z1.textContent = ""
      td_g1.textContent = ""
      td_time.textContent = ""
      td_x.textContent = ""
      td_y.textContent = ""
      td_z.textContent = ""
      td_g.textContent = ""
  
    }
    else {
      td_t1.textContent = "Time"
      td_x1.textContent = "X"
      td_y1.textContent = "Y"
      td_z1.textContent = "Z"
      td_g1.textContent = "Clock bias"
      for (var sp3 in result4[id]) {
        tdt = tdt + result4[id][sp3][4].replace("T", " ") + '\n'
        tdx = tdx + (Number(result4[id][sp3][0])).toFixed(3) + '\n'
        tdy = tdy + (Number(result4[id][sp3][1])).toFixed(3) + '\n'
        tdz = tdz + (Number(result4[id][sp3][2])).toFixed(3) + '\n'
        tdg = tdg + (Number(result4[id][sp3][3])).toFixed(3) + '\n'
        // sp3text.value = sp3text.value + fix(result4[id][sp3][4], 22) +
        //   "\t" + fix((Number(result4[id][sp3][0])/1000).toFixed(6), 22) +
        //   "\t" + fix((Number(result4[id][sp3][1])/1000).toFixed(6), 22) +
        //   "\t" + fix((Number(result4[id][sp3][2])/1000).toFixed(6), 22) +
        //   "\t" + fix(Number(result4[id][sp3][3]).toFixed(6), 22) + "\t"+'\n'
      }
      td_time.textContent = tdt;
      td_x.textContent = tdx;
      td_y.textContent = tdy;
      td_z.textContent = tdz;
      td_g.textContent = tdg;
    }
  }




}





function closeout() {
  var div4 = document.getElementById("div5");
  div5.style.display = 'none';
}


// function openorbit() {

// document.getElementById("orbit_cal").style.display = "block";//显示



for (var prn in result3) {
  for (var i = 0; i < newselect.options.length; i++) {
    var z = 0
    if (prn != newselect.options[i].value) {
      continue
    }
    z = 1
    break
  }
  if (z == 0 && prn.indexOf('C') != -1) { document.getElementById("newselect").options.add(new Option(prn, prn)); }
  if (prn == 'C62') { break }
}
for (var prn in result2) {
  for (var i = 0; i < newselect.options.length; i++) {
    var z = 0
    if (prn != newselect.options[i].value) {
      continue
    }
    z = 1
    break
  }
  if (z == 0 && prn.indexOf('C') != -1) { document.getElementById("newselect").options.add(new Option(prn, prn)); }
  if (prn == 'C62') { break }
}
for (var prn in result4) {
  for (var i = 0; i < newselect.options.length; i++) {
    var z = 0
    if (prn != newselect.options[i].value) {
      continue
    }
    z = 1
    break
  }
  if (z == 0 && prn.indexOf('C') != -1) { document.getElementById("newselect").options.add(new Option(prn, prn)); }
  if (prn == 'C62') { break }
}
for (var prn in result5) {
  for (var i = 0; i < newselect.options.length; i++) {
    var z = 0
    if (prn != newselect.options[i].value) {
      continue
    }
    z = 1
    break
  }
  if (z == 0 && prn.indexOf('C') != -1) { document.getElementById("newselect").options.add(new Option(prn, prn)); }
  if (prn == 'C62') { break }
}
newset();
// }
function neworbitcal() {

  var c1 = document.getElementById("check1");
  var c2 = document.getElementById("check2");
  var c3 = document.getElementById("check3");
  var c4 = document.getElementById("check4");

  id = document.getElementById('newselect').value;


  timelist = [];
  data_x1 = [];
  data_x2 = [];
  data_x3 = [];
  data_x4 = [];
  data_y1 = [];
  data_y2 = [];
  data_y3 = [];
  data_y4 = [];
  data_z1 = [];
  data_z2 = [];
  data_z3 = [];
  data_z4 = [];

  text1.value = "";
  ii = 26;
  jj = 0

  var tstep=$('#tstep').val()
  for (var i = 0; i <(((60/tstep))*24+1); i++) {


    objecttime = document.getElementById('objtime').value
    year = objecttime.slice(0, 4)
    month = Math.floor(objecttime.slice(5, 7))
    day = objecttime.slice(8, 10)
    day = Math.floor(day)
    let timedate = new Date(year, month, day)
    timedate.setMinutes(timedate.getMinutes()+(tstep*(i-1)))
    var chour=timedate.getHours()
    var cminutes=timedate.getMinutes()
    if(chour<10){
      chour='0'+chour
    }
    if(cminutes<10){
      cminutes='0'+cminutes
    }
    timeid = year + month + day + chour + cminutes

    if (i == 0) {
      text1.value = fix("Time", 12);
      if (c1.checked == true) {
        text1.value = text1.value + fix("X(TLE)", 22)  + fix("Y(TLE)", 16)  + fix("Z(TLE)", 16) ;
        if (c4.checked == true) {
          text1.value = text1.value + fix("X(YUMA)", 17)  + fix("Y(YUMA)", 16)  + fix("Z(YUMA)", 16) ;
        }
        if (c2.checked == true) {
          text1.value = text1.value + fix("X(Rinex)", 17)  + fix("Y(Rinex)", 16)  + fix("Z(Rinex)", 16) ;
        }
        if (c3.checked == true) {
          text1.value = text1.value + fix("X(SP3)", 15)  + fix("Y(SP3)", 16)  + fix("Z(SP3)", 16) ;
        }
  
      }
      else{
        if (c4.checked == true) {
          text1.value = text1.value + fix("X(YUMA)", 22)  + fix("Y(YUMA)", 16)  + fix("Z(YUMA)", 16) ;
          if (c2.checked == true) {
            text1.value = text1.value + fix("X(Rinex)", 17)  + fix("Y(Rinex)", 16)  + fix("Z(Rinex)", 16) ;
          }
          if (c3.checked == true) {
            text1.value = text1.value + fix("X(SP3)", 15)  + fix("Y(SP3)", 16)  + fix("Z(SP3)", 16) ;
          }
        }
        else{
          if (c2.checked == true) {
            text1.value = text1.value + fix("X(Rinex)", 22)  + fix("Y(Rinex)", 16)  + fix("Z(Rinex)", 16) ;
            if (c3.checked == true) {
              text1.value = text1.value + fix("X(SP3)", 15)  + fix("Y(SP3)", 16)  + fix("Z(SP3)", 16) ;
            }
          }
          else{
            if (c3.checked == true) {
              text1.value = text1.value + fix("X(SP3)", 22)  + fix("Y(SP3)", 16)  + fix("Z(SP3)", 16) ;
            }
          }
        }

      }

    }
    else {
      if (c2.checked == true) {


        if (!window.result3[id][timeid]) {
          // alert("Rinex中无匹配数据")
          break;
        }
        else {

          timelist.push(result3[id][timeid]["epoch"].slice(11, 16));
          text1.value = text1.value + fix(result3[id][timeid]["epoch"].replace("T", " "), 20) + "\t";
          if (c1.checked == true) {
            if (!window.result2[id][timeid]) {

              alert("No match data in the TLE file")
              break
            }

            data_x1.push(result2[id][timeid]["x"]);
            data_y1.push(result2[id][timeid]["y"]);
            data_z1.push(result2[id][timeid]["z"]);
            text1.value = text1.value +
              fix(parseFloat(result2[id][timeid]["x"]).toFixed(3), 12) + "\t" +
              fix(parseFloat(result2[id][timeid]["y"]).toFixed(3), 12) + "\t"
              + fix(parseFloat(result2[id][timeid]["z"]).toFixed(3), 12) + '\t';
          }
          if (c4.checked == true) {

            if (!window.result5[id][timeid]) {

              alert("No match data in the YUMA file")
              break
            }

            data_x4.push(result5[id][timeid].X_k);
            data_y4.push(result5[id][timeid].Y_k);
            data_z4.push(result5[id][timeid].Z_k);
            text1.value = text1.value + fix(parseFloat(result5[id][timeid].X_k).toFixed(3), 12) + "\t" +
              fix(parseFloat(result5[id][timeid].Y_k).toFixed(3), 12) + "\t" +
              fix(parseFloat(result5[id][timeid].Z_k).toFixed(3), 12)+ "\t";
          }
          
          data_x2.push(result3[id][timeid]['X_k']);
          data_y2.push(result3[id][timeid]['Y_k']);
          data_z2.push(result3[id][timeid]['Z_k']);
          text1.value = text1.value +
            fix(parseFloat(result3[id][timeid]['X_k']).toFixed(3), 12) + '\t' +
            fix(parseFloat(result3[id][timeid]['Y_k']).toFixed(3), 12) + '\t' +
            fix(parseFloat(result3[id][timeid]['Z_k']).toFixed(3), 12) + "\t";
          if (c3.checked == true) {
            if (!window.result4[id]||!window.result4[id][timeid]) {
              modal.innerHTML = 'No match data in the SP3 file';
              // alert("SP3无匹配数据")
              document.body.style.pointerEvents = 'auto';     
              confirmBtn.textContent = 'Confirm';
              confirmBtn.addEventListener('click', onConfirm);
              modal.appendChild(confirmBtn);
              break
            }
            data_x3.push(result4[id][timeid][0]);
            data_y3.push(result4[id][timeid][1]);
            data_z3.push(result4[id][timeid][2]);
            text1.value = text1.value + fix(parseFloat(result4[id][timeid][0]).toFixed(3), 12) + '\t' +
              fix(parseFloat(result4[id][timeid][1]).toFixed(3), 12) + '\t' +
              fix(parseFloat(result4[id][timeid][2]).toFixed(3), 12) 


          }


        }

      }
      else {


        if (c1.checked == true) {
          if (!window.result2[id][timeid]) {

            alert("No match data in the TLE file")
            break
          }
          if (timelist.length == i - 1) {

            timelist.push(result2[id][timeid]["time"].slice(11, 16));

          }
          text1.value = text1.value + fix(result2[id][timeid]["time"].replace("T", " "), 20) + "\t";
          data_x1.push(result2[id][timeid].x);
          data_y1.push(result2[id][timeid].y);
          data_z1.push(result2[id][timeid].z);
          text1.value = text1.value +
            fix(parseFloat(result2[id][timeid].x).toFixed(3), 12) + "\t" + fix(parseFloat(result2[id][timeid].y).toFixed(3), 12) + "\t"
            + fix(parseFloat(result2[id][timeid].z).toFixed(3), 12) + '\t';
        }
        if (c4.checked == true) {
          if (!window.result5[id][timeid]) {

            alert("No match data in the YUMA file")
            break
          }

          if (timelist.length == i - 1) {

            timelist.push(result4[id][timeid][4].slice(11, 16));
            text1.value = text1.value + fix(result5[id][timeid]['epoch'].replace("T", " "), 20) + "\t";
          }
          data_x4.push(result5[id][timeid].X_k);
          data_y4.push(result5[id][timeid].Y_k);
          data_z4.push(result5[id][timeid].Z_k);
          text1.value = text1.value + fix(parseFloat(result5[id][timeid].X_k).toFixed(3), 12) + "\t" +
            fix(parseFloat(result5[id][timeid].Y_k).toFixed(3), 12) + "\t" +
            fix(parseFloat(result5[id][timeid].Z_k).toFixed(3), 12)+ "\t";
        }

        if (c3.checked == true) {

          if (!window.result4[id][timeid]) {

            alert("No match data in the SP3 file")
            break
          }
          if (!window.result4[id][timeid]) {
            console.log(result4)
            console.log(timeid)
            alert("No match data in the SP3 file")
            break
          }
          if (timelist.length == i - 1) {

            timelist.push(result4[id][timeid][4].slice(11, 16));

          }
          if (c1.checked != true) {
            text1.value = text1.value + fix(result4[id][timeid][4].replace("T", " "), 20) + "\t";
          }
          data_x3.push(result4[id][timeid][0]);
          data_y3.push(result4[id][timeid][1]);
          data_z3.push(result4[id][timeid][2]);
          text1.value = text1.value + fix(parseFloat(result4[id][timeid][0]).toFixed(3), 12) + '\t' +
            fix(parseFloat(result4[id][timeid][1]).toFixed(3), 12) + '\t' +
            fix(parseFloat(result4[id][timeid][2]).toFixed(3), 12) 

        }

      }
    }


    text1.value = text1.value + '\n';
  }
  // < !--计算差值-->
  gap_x1 = [];
  gap_x2 = [];
  gap_x3 = [];
  gap_y1 = [];
  gap_y2 = [];
  gap_y3 = [];
  gap_z1 = [];
  gap_z2 = [];
  gap_z3 = [];

  
  for (var z = 0; z < data_x1.length; z++) {
    gap_x1[z] = ((data_x1[z] - data_x3[z]) / 1000).toFixed(2);
    gap_y1[z] = ((data_y1[z] - data_y3[z]) / 1000).toFixed(2);
    gap_z1[z] =( (data_z1[z] - data_z3[z]) / 1000).toFixed(2);

  }
  for (var z = 0; z < data_x2.length; z++) {
    gap_x2[z] = (data_x2[z] - data_x3[z]).toFixed(2);
    gap_y2[z] = (data_y2[z] - data_y3[z]).toFixed(2);
    gap_z2[z] = (data_z2[z] - data_z3[z]).toFixed(2);
  }
  for (var z = 0; z < data_x3.length; z++) {
    gap_x3[z] = ((data_x4[z] - data_x3[z]) / 1000).toFixed(2);
    gap_y3[z] = ((data_y4[z] - data_y3[z]) / 1000).toFixed(2);
    gap_z3[z] = ((data_z4[z] - data_z3[z]) / 1000).toFixed(2);
  }
  x1_rms=calculateRMS(gap_x1).toFixed(2);
  y1_rms=calculateRMS(gap_y1).toFixed(2);
  z1_rms=calculateRMS(gap_z1).toFixed(2);
  x2_rms=calculateRMS(gap_x2).toFixed(2);
  y2_rms=calculateRMS(gap_y2).toFixed(2);
  z2_rms=calculateRMS(gap_z2).toFixed(2);
  x3_rms=calculateRMS(gap_x3).toFixed(2);
  y3_rms=calculateRMS(gap_y3).toFixed(2);
  z3_rms=calculateRMS(gap_z3).toFixed(2);

  paintchart();
}
function fix(num, length) {
  return ('' + num).length < length ? ((new Array(length + 1)).join(' ') + num).slice(-length) : '' + num;
}
function downresult() {
  savecontent = [];
  savecontent.push(text1.value)
  alert(savecontent);
  var file = new File(
    savecontent,
    "result.txt",
    { type: "text/plain;charset=utf-8" }
  );
  saveAs(file);
}


function paintchart() {
  var tstep = $('#tstep').val();
  var myChart4 = echarts.init(document.getElementById('gap_chart1'));
  var myChart5 = echarts.init(document.getElementById('gap_chart2'));
  var myChart6 = echarts.init(document.getElementById('gap_chart3'));

  objecttime = document.getElementById('objtime').value
  year = objecttime.slice(0, 4)
  month = objecttime.slice(5, 7)
  day = objecttime.slice(8, 10)

  paintime = year + "-" + month + "-" + day
  for (var z = 0; z < data_x1.length; z++) {
    data_x1[z] = data_x1[z] / 1000
    data_y1[z] = data_x1[z] / 1000
    data_z1[z] = data_x1[z] / 1000
  }
  for (var z = 0; z < data_x2.length; z++) {
    data_x2[z] = data_x2[z] / 1000
    data_y2[z] = data_x2[z] / 1000
    data_z2[z] = data_x2[z] / 1000
  }
  for (var z = 0; z < data_x3.length; z++) {
    data_x3[z] = data_x3[z] / 1000
    data_y3[z] = data_x3[z] / 1000
    data_z3[z] = data_x3[z] / 1000
  }
  for (var z = 0; z < data_x4.length; z++) {
    data_x4[z] = data_x4[z] / 1000
    data_y4[z] = data_x4[z] / 1000
    data_z4[z] = data_x4[z] / 1000
  }

  var option4 = {
    title: {
      text: paintime,
      x: 'center',
      y: 'top',
      top: 20,
      textStyle: {
        color: 'black',
        fontStyle: 'normal',
        fontWeight: 'bold',
        fontSize: 18,
      },
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      orient: 'vertical', 
      align: 'left',
      right:'70px',
      y: '10px',
      backgroundColor: 'rgba(0,0,0,0)',
      borderColor: '#ccc',
      borderWidth: 0,
      padding: 0, 
      itemGap: 2,
      itemWidth: 20,
      itemHeight: 10, 
      textStyle: {
        color: 'black'
      },
      formatter: function (legendName) {
        if(legendName=='dx'){
          var objectname='RMS_X='+x2_rms
        }
        if(legendName=='dy'){
          var objectname='RMS_Y='+y2_rms
        }
        if(legendName=='dz'){
          var objectname='RMS_Z='+z2_rms
        }

        
        return objectname 
      },
    },
    xAxis: {

      name: 'Time',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      axisLabel: {
        color: 'black',
        interval: (60/tstep)*2-1
      },
      axisLine: {

        lineStyle: {
          color: 'black', 
        },
      },
      data: timelist
    },
    yAxis: {
      name: 'Error[m]',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
          // color: 'black',
        }
      },
      axisLine: {
        lineStyle: {
          color: 'black', 
        },
      },
      axisLabel: {
        color: 'black',
      }
    },
    series: [{
      showSymbol: false,
      name: 'dx',
      type: 'line',
      color: "red",
      data: gap_x2
    },
    {
      showSymbol: false,
      name: 'dy',
      type: 'line',
      color: "green",
      data: gap_y2
    },
    {
      showSymbol: false,
      name: 'dz',
      color: "blue",
      type: 'line',
      data: gap_z2
    }
    ],


  };
  var option5 = {
    title: {
      text: paintime,
      x: 'center',
      y: 'top',
      top: 20,
      textStyle: {
        color: 'black',
        fontStyle: 'normal',
        fontWeight: 'bold',
        fontSize: 18
      },
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      orient: 'vertical',
      align: 'left',
      right:'70px',
      y: '10px',
      backgroundColor: 'rgba(0,0,0,0)',
      borderColor: '#ccc',
      borderWidth: 0,
      padding: 0,
      itemGap: 2,
      itemWidth: 20,
      itemHeight: 10,
      textStyle: {
        color: 'black'
      },
      formatter: function (legendName) {
        if(legendName=='dx'){
          var objectname='RMS_X='+x3_rms
        }
        if(legendName=='dy'){
          var objectname='RMS_Y='+y3_rms
        }
        if(legendName=='dz'){
          var objectname='RMS_Z='+z3_rms
        }

        
        return objectname 
      },
    },
    xAxis: {

      name: 'Time',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      axisLine: {
        lineStyle: {
          color: 'black',
        },
      },
      axisLabel: {
        color: 'black',
        interval: (60/tstep)*2-1
      },
      data: timelist
    },
    yAxis: {
      name: 'Error[km]',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
        }
      },
      axisLine: {
        lineStyle: {
          color: 'black', 
        },
      },
      axisLabel: {
        color: 'black',
      }
    },
    series: [{
      showSymbol: false,
      name: 'dx',
      type: 'line',
      color: "red",
      data: gap_x3
    },
    {
      showSymbol: false,
      name: 'dy',
      type: 'line',
      color: "green",
      data: gap_y3
    },
    {
      showSymbol: false,
      name: 'dz',
      type: 'line',
      color: "blue",
      data: gap_z3
    }
    ]
  };
  var option6 = {
    title: {
      text: paintime,
      x: 'center',
      y: 'top',
      top: 20,
      textStyle: {
        color: 'black',
        fontStyle: 'normal',
        fontWeight: 'bold',
        fontSize: 18
      },
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      orient: 'vertical',
      align: 'left',
      right:'70px',
      y: '10px',
      backgroundColor: 'rgba(0,0,0,0)',
      borderColor: '#ccc',
      borderWidth: 0,
      padding: 0,
      itemGap: 2, 
      itemWidth: 20,
      itemHeight: 10,
      textStyle: {
        color: 'black'
      },
      formatter: function (legendName) {
        if(legendName=='dx'){
          var objectname='RMS_X='+x1_rms
        }
        if(legendName=='dy'){
          var objectname='RMS_Y='+y1_rms
        }
        if(legendName=='dz'){
          var objectname='RMS_Z='+z1_rms
        }
        
        return objectname 
      },
    },
    xAxis: {

      name: 'Time',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      axisLine: {
        lineStyle: {
          color: 'black',
        },
      },
      axisLabel: {
        color: 'black',
        interval: (60/tstep)*2-1
      },
      data: timelist

    },
    yAxis: {
      name: 'Error[km]',
      nameLocation: "center",
      nameTextStyle: {
        fontSize: 16,
        padding: 10,
        color: 'black'
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
        }
      },
      axisLine: {
        lineStyle: {
          color: 'black',
        },
      },
      axisLabel: {
        color: 'black',
      }
    },
    series: [{
      showSymbol: false,
      name: 'dx',
      type: 'line',
      color: "red",
      data: gap_x1
    },
    {
      showSymbol: false,
      name: 'dy',
      type: 'line',
      color: "green",
      data: gap_y1
    },
    {
      showSymbol: false,
      name: 'dz',
      type: 'line',
      color: "blue",
      data: gap_z1
    }
    ]
  };

  myChart4.setOption(option4);
  myChart5.setOption(option5);
  myChart6.setOption(option6);

}
// < !--对比图-->
function show2() {
  id = $("input[name='b']:checked").val();
  if (id == 'chart_x') {
    chart_x.style.display = 'block';
    chart_y.style.display = 'none';
    chart_z.style.display = 'none';
  }
  if (id == 'chart_y') {
    chart_y.style.display = 'block';
    chart_x.style.display = 'none';
    chart_z.style.display = 'none';
  }
  if (id == 'chart_z') {
    chart_z.style.display = 'block';
    chart_x.style.display = 'none';
    chart_y.style.display = 'none';
  }

}
// < !--结果选项-->
function show1() {
  id = $("input[name='a']:checked").val();
  dt=document.getElementById('downtext')
  dc=document.getElementById('btndownchart')
  if (id == 'text1') {
    text1.style.display = 'block';
    dt.style.display = 'block';
    dc.style.display = 'none';
    // chart1.style.display = 'none';
    chart2.style.display = 'none';
    // chart3.style.display = 'none';
  }

  if (id == 'chart2') {
    chart2.style.display = 'block';
    text1.style.display = 'none';
    dc.style.display = 'block';
    dt.style.display = 'none';
    // chart1.style.display = 'none';
    // chart3.style.display = 'none';
  }


}
// < !--差值图-->
function show3() {
  id = $("input[name='c']:checked").val();
  if (id == 'gap_chart1') {
    gap_chart1.style.display = 'block';
    gap_chart2.style.display = 'none';
    gap_chart3.style.display = 'none';
  }
  if (id == 'gap_chart2') {
    gap_chart2.style.display = 'block';
    gap_chart1.style.display = 'none';
    gap_chart3.style.display = 'none';
  }
  if (id == 'gap_chart3') {
    gap_chart3.style.display = 'block';
    gap_chart1.style.display = 'none';
    gap_chart2.style.display = 'none';
  }
}
function jiequ() {
  if (document.getElementById('gap_chart1').style.display == 'block') {
    var obj = '#gap_chart1'
  }
  else if (document.getElementById('gap_chart2').style.display == 'block') {
    var obj = '#gap_chart2'
  }
  else if (document.getElementById('gap_chart3').style.display == 'block') {
    var obj = '#gap_chart3'
  }
  else {
    alert('no pictrue')
  }

  html2canvas($(obj), {
    backgroundColor: '#ffffff',
    height: ($("#contbox").outerHeight()) * 10,
    width: ($("#contbox").outerWidth()) * 10,
    scale: 10,
    logging: true,
    foreignObjectRendering: true,
    useCORS: true,
    onrendered: function (canvas) {
      var img = convertCanvasToImage(canvas);
      download(img.src)
    }
  });

}
// function jiequ() {
//   if(document.getElementById('gap_chart1').style.display=='block'){
//     var obj='#gap_chart1'
//     var select=1
//   }
//   else if(document.getElementById('gap_chart2').style.display=='block'){
//     var obj='#gap_chart2'
//     var select=2
//   }
//   else if(document.getElementById('gap_chart3').style.display=='block'){
//     var obj='#gap_chart3'
//     var select=3
//   }
//   else{
//     alert('no pictrue')
//   }
//   document.getElementById('downchart').style.display='block'
//   paintdownchart('downchart',select)
//   // html2canvas($(obj), {
//   //     backgroundColor:'#ffffff',
//   //     height: ($("#contbox").outerHeight())*10,
//   //     width: ($("#contbox").outerWidth())*10,
//   //     scale: 10,
//   //     logging:true,
//   //     foreignObjectRendering: true,
//   //     useCORS: true,
//   //     onrendered: function (canvas) {
//   //         var img = convertCanvasToImage(canvas);
//   //         download(img.src)
//   //     }
//   // });

// }
//绘制显示图片
function convertCanvasToImage(canvas) {
  var image = new Image();

  image.src = canvas.toDataURL("image/png"); //生成图片地址
  return image;
}
//生成canvas元素
function convertImageToCanvas(image, startX, startY, width, height) {
  var canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  canvas.getContext("2d").drawImage(image, startX, startY, width, height, 0, 0, width, height);//在这调整图片中内容的显示（大小,放大缩小,位置等）
  return canvas;
}// 另存为图片
function download(src) {


  var $a = $("<a></a>").attr("href", src).attr("download",
    "图像.png");
  $a[0].click();
}

// 获取颜色选择器元素
var colorPicker = document.getElementById("colorPicker");

// 获取目标容器元素
var chart2 = document.getElementById("chart2");

// 监听颜色选择器的变化事件
colorPicker.addEventListener("change", function () {
  // 获取选择的颜色值
  var color = colorPicker.value;

  // 将颜色应用于目标容器的背景颜色
  chart2.style.backgroundColor = color;
});
function calculateRMS(numbers) {
  // 计算平方和
  const squareSum = numbers.reduce((sum, num) => sum + num * num, 0);

  // 计算均方根并返回
  const rms = Math.sqrt(squareSum / numbers.length);
  return rms;
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

let isDone = false;
const calcBtn = document.getElementById('cal');
const modal = document.getElementById('modal');
let confirmBtn = document.createElement('button');
let stepsetvalue=false
let timesetvalue=false
calcBtn.addEventListener('click', () => {
  isDone = false;
  modal.innerHTML = 'Calculating...';
  modal.showModal();
  document.body.style.pointerEvents = 'none';

  var date = $('#datepick').val();
  var tstep = $('#tstep').val();
  if (stepsetvalue==false&&timesetvalue==false) {
    neworbitcal()
    newset();
    if(modal.innerHTML=='Calculating...'){
      isDone = true;
      modal.innerHTML = 'Success';
      document.body.style.pointerEvents = 'auto';     
      confirmBtn.textContent = 'Confirm';
      confirmBtn.addEventListener('click', onConfirm);
      modal.appendChild(confirmBtn);

    }

  }
  else {
    var url = '/calorbits'

    $.post(url, { 'date': date, 'tstep':tstep }, function (res) {

      console.log(res)
      // rinexdata
      result3 = res[0];
      // sp3data
      result4=res[1]
      // yuamdata
      result5=res[2]
      // tledata
      result=res[3][1]
      result2=res[3][0]

      if(modal.innerHTML=='Calculating...'){
        content='Success'
        content1=''
        isDone = true;
        if(result3=='false')
        {
          content1+='\tNo Rinex file'
        }
        if(result4=='false')
        {
          content1+='\tNo SP3 file'
        }
        if(result5=='false')
        {
          content1+='\tNo YUMA file'
        }
        modal.innerHTML = content+content1
        document.body.style.pointerEvents = 'auto';     
        confirmBtn.textContent = 'Confirm';
        confirmBtn.addEventListener('click', onConfirm);
        modal.appendChild(confirmBtn);
        newset();

        neworbitcal()
      }
    })

    timesetvalue=false
    stepsetvalue=false
  }
  
});
function onConfirm() {
  modal.close();
  modal.removeChild(confirmBtn);
}

function timeset()
{
  timesetvalue=true
  var datepick = document.getElementById("datepick").value
  objtime.value=datepick+' 00:00'
  endtime.value=datepick+' 23:00'
}
function stepset(){
  stepsetvalue=true
}
let dateInput = document.querySelector('input[type="date"]');
let today = new Date().toISOString().slice(0, 10); 
dateInput.setAttribute('max', today);