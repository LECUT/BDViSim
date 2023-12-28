class GlobeRotate {
    constructor(viewer) {
        this._viewer = viewer;
    }

    // 根据国际天体参考系计算旋转矩阵
    _icrf() {
        if (this._viewer.scene.mode !== Cesium.SceneMode.SCENE3D) {
            return ture;
        }
        console.log(this._viewer.camera.position);
        let icrfToFixed = Cesium.Transforms.computeIcrfToFixedMatrix(this._viewer.clock.currentTime);
        if (icrfToFixed) {
            let camera = this._viewer.camera;
            let offset = Cesium.Cartesian3.clone(camera.position);
            let transform = Cesium.Matrix4.fromRotationTranslation(icrfToFixed);
            // 偏移相机，否则会场景旋转而地球不转
            camera.lookAtTransform(transform, offset);
        }
    }

    // 绑定事件
    _bindEvent() {
    	// 转动的速度设置
        this._viewer.clock.multiplier = 15 * 1000;
        // 初始化为单位矩阵
        this._viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
        this._viewer.scene.postUpdate.addEventListener(this._icrf, this);
    }

    // 解除绑定
    _unbindEvent() {
        this._viewer.clock.multiplier = 1;
        this._viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
        this._viewer.scene.postUpdate.removeEventListener(this._icrf, this);
    }

    // 开始旋转
    start() {
        this._viewer.clock.shouldAnimate = true;
        this._unbindEvent();
        this._bindEvent();
        return this;
    }

    // 停止旋转
    stop() {
        this._unbindEvent();
        return this;
    }
}
