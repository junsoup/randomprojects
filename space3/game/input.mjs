class Input{
    constructor(controls){
        //private
        var accel = 0.1;
        var keys = {};
        var domElement = document.body;
        connect();

        function keyDown(event) {
            keys[event.code] = true;
            if(event.code == "KeyW"){
                accel = accel*1.1;
            }
            // if(accel >= 50){
            //     accel = 50;
            // }
        };
        function keyUp(event){
            keys[event.code] = false;
            if(event.code == "KeyW")
                accel = 0.3;
        }
        function connect() {
			domElement.ownerDocument.addEventListener("keydown", keyDown, false);
			domElement.ownerDocument.addEventListener("keyup", keyUp, false);
            domElement.ownerDocument.addEventListener("click",
            function () {
                controls.lock();
            }, false);
		};
        //public
        this.controlTick = function(){

            if(keys['KeyW'])
                controls.moveForward(accel);
            if(keys['KeyA'])
                controls.moveRight(-accel);
            if(keys['KeyS'])
                controls.moveForward(-accel);
            if(keys['KeyD'])
                controls.moveRight(accel);
            if(keys['Space'])
                controls.moveUp(-accel);
            if(keys['ShiftLeft'])
                controls.moveUp(accel);
            // if(keys['KeyE'])
            //     controls.changeCamera(.01);
        }
    }
}
export{ Input };
