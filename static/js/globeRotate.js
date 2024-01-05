class GlobeRotate {
    constructor(viewer) {
        this._viewer = viewer;
    }


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

            camera.lookAtTransform(transform, offset);
        }
    }


    _bindEvent() {

        this._viewer.clock.multiplier = 15 * 1000;

        this._viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
        this._viewer.scene.postUpdate.addEventListener(this._icrf, this);
    }


    _unbindEvent() {
        this._viewer.clock.multiplier = 1;
        this._viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
        this._viewer.scene.postUpdate.removeEventListener(this._icrf, this);
    }


    start() {
        this._viewer.clock.shouldAnimate = true;
        this._unbindEvent();
        this._bindEvent();
        return this;
    }


    stop() {
        this._unbindEvent();
        return this;
    }
}
