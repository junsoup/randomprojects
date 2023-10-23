import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/0.148.0/three.module.min.js';
import {OrbitControls} from './OrbitControls.js';

// Helper functions
const colorToHex = (color) => {
    const hexadecimal = color.toString(16);
    return hexadecimal.length == 1 ? "0" + hexadecimal : hexadecimal;
}
const RGBtoHex = (red, green, blue) => {
    return "#" + colorToHex(red) + colorToHex(green) + colorToHex(blue);
}

// Renderer setup
const renderer = new THREE.WebGLRenderer({antialias: true, precision: "lowp"});
renderer.setSize( window.innerWidth, window.innerHeight  );
renderer.setPixelRatio( window.devicePixelRatio *1.5);
document.body.appendChild( renderer.domElement );

// Camera setup
const camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 100000 );
// const camera = new THREE.OrthographicCamera( window.innerWidth/-2, window.innerWidth/2, window.innerHeight/2, window.innerHeight/-2, 1, 1000 );

camera.position.set( -300, 200, 300 );
camera.lookAt( 0, 0, 0 );

// Orbit controls setup (mouse)
const controls = new OrbitControls( camera, renderer.domElement );
const scene = new THREE.Scene();

// Simulation setting
var n = 7
var size = Math.floor(200/n);

// Element geometry
const geometry = new THREE.BoxGeometry(size*.7,size*.7,size*.7)
// const geometry = new THREE.IcosahedronGeometry(size*.45, 3)
var cubes = []

// Helper for getting position of element via index
function indextoSpace(i, j, k){
    return [(i-(n/2)+0.25)*size, (j-(n/2)+0.25)*size, (k-(n/2)+0.25)*size]
}

// Create cubes
for(var i = 0; i < n; i++){
    for(var j = 0; j < n; j++){
        for(var k = 0; k < n; k++){
            var r = Math.floor(i/(n-1)*230+15);
            var g = Math.floor(j/(n-1)*230+15);
            var b = Math.floor(k/(n-1)*230+15);
            
            const material = new THREE.MeshBasicMaterial( {color: RGBtoHex(r,g,b),  opacity:.7, transparent:true} );
            var cube = new THREE.Mesh( geometry, material );
            var pos = indextoSpace(i,j,k)
            cube.position.x = pos[0];
            cube.position.y = pos[1];
            cube.position.z = pos[2];
            cubes.push(cube)
            scene.add(cube);
        }
    }
}

// Set element position by time. 
// (alternatively swapping to 0.0 ~ 1.0(or 2PI) param. instead of using .time() may be more "correct")
function cubeWave(){
    var index = 0;
    for(var i = 0; i < n; i++){
        for(var j = 0; j < n; j++){
            for(var k = 0; k < n; k++){
                var pos = indextoSpace(i,j,k);
                let time = Date.now()
                // First const is for frequency, second is for amplitude.
                pos[0] += Math.sin(time*.0015+i)*3
                pos[1] += Math.sin(time*.002+k)*5
                pos[2] += Math.sin(time*.002+j)*1
                cubes[index].position.x = pos[0];
                cubes[index].position.y = pos[1];
                cubes[index].position.z = pos[2];
                index++;
            }
        }
    }
}

// Render loop
// "refresh rate" (seconds)
let renderInterval = 1 / 165;

let renderDelta = 0;
let clock = new THREE.Clock();
let counter = 0;
function animate() {
	let delta = clock.getDelta();
    controls.update();

    // With controlled fps:
	// renderDelta += delta;
    // if(renderDelta > renderInterval){
	// 	if(counter>10){
	// 	   console.log("fps: " + Math.floor(1/renderDelta));
	// 	   counter = 0;
    //    }else{counter++;}
	// 	renderDelta = renderDelta % renderInterval;
    //     renderer.render(scene, camera);
    //     cubeWave();
    // }
    
    // No fps limit (limited to vsync or display's limit):
    if(counter>100){
        console.log("fps: " + Math.floor(1/delta));
        counter = 0;
    }else{counter++;}
    cubeWave();
    renderer.render(scene, camera);


    requestAnimationFrame( animate );
}
animate();