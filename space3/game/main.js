
import * as THREE from 'three';
// import {WebGPUNodes} from 'three/nodes/WebGPUNodes.js'
import defaultExport  from 'three/addons/renderers/webgpu/WebGPURenderer.js'
import { PointerLockControls } from './PointerLockControls.mjs';
import { Input } from './input.mjs';
import { World } from './world.mjs';


//scene
const scene = new THREE.Scene();

//camera
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.01, Number.MAX_SAFE_INTEGER );


//rederer
const renderer = new THREE.WebGLRenderer({antialias: true, precision: "lowp"});
renderer.setSize( window.innerWidth, window.innerHeight );

//canvas
const canvas = renderer.domElement;
document.body.appendChild( canvas );

//event listeners
window.addEventListener( 'resize', onWindowResize, false );
function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

//Objects
const controls = new PointerLockControls(camera, canvas);
const input = new Input(controls);
const world = new World(scene, camera);

//frame timers
let gameDelta = 0;
let renderDelta = 0;

//game ticks per second, render ticks per second
let gameInterval = 1 / 60;
let renderInterval = 1 / 165;
//FPS timer
let clock = new THREE.Clock();
let counter = 0;

//run method
function animate() {
    //frame timers
	let delta = clock.getDelta();
	gameDelta += delta;
	renderDelta += delta;

    //game loop
    if(gameDelta > gameInterval){
		gameDelta = gameDelta % gameInterval;
        if(controls.isLocked){
            input.controlTick();
        }
        //game updates{
        world.tick();
    }

    //render loop
	if(renderDelta > renderInterval){
		if(counter>10){
		   console.log("fps: " + Math.floor(1/renderDelta, "Scene size: ",scene.children.length));
		   counter = 0;
       }else{counter++;}
		renderDelta = renderDelta % renderInterval;
        //render scene{
        renderer.render(scene, camera);
        //}
    }
    requestAnimationFrame(animate);
};
animate();
