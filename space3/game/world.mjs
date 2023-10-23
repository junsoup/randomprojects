import * as THREE from 'three';

function createPathStrings(filename) {
  const basePath = "./textures/";
  const baseFilename = basePath + filename;
  const fileType = ".png";
  const sides = ["ft", "bk", "up", "dn", "rt", "lf"];
  const pathStings = sides.map(side => {
    return baseFilename + "_" + side + fileType;
  });
  return pathStings;
}
let skyboxImage = "bg";

function createMaterialArray(filename) {
  const skyboxImagepaths = createPathStrings(filename);
  const materialArray = skyboxImagepaths.map(image => {
    let texture = new THREE.TextureLoader().load(image);
    return new THREE.MeshBasicMaterial({ map: texture, side: THREE.BackSide, depthWrite: false});
  });
  return materialArray;
}
const skyboxGeo = new THREE.BoxGeometry(50,50 ,50);
const materialArray = createMaterialArray(skyboxImage);
const skybox = new THREE.Mesh(skyboxGeo, materialArray);

const light = new THREE.PointLight( 0xffcc88 ,500000000000000,0,2);
const ambientLight = new THREE.AmbientLight(0x212122);
const lightHelper = new THREE.PointLightHelper(light);

const starGeometry = new THREE.IcosahedronGeometry();
const starMaterial = new THREE.MeshStandardMaterial({color:0xffffff});
const star = new THREE.Mesh(starGeometry, starMaterial);

const sunGeometry = new THREE.IcosahedronGeometry(1392700,0);
const sunMaterial = new THREE.MeshBasicMaterial({color:0xffaa33});
const sun = new THREE.Mesh(sunGeometry, sunMaterial);

sun.position.set(13000000,0,0);
light.position.set(13000000,0,0);

//0: always render
//else: max view distancec
const objects = [];
objects.push(light);
objects.push(ambientLight);
objects.push(lightHelper);
objects.push(sun);

class World{
    constructor(scene,camera){
        var counter = 0;
        scene.add(skybox);
        scene.add(camera);
        for (var i = 0; i < objects.length; i++)
            scene.add(objects[i]);
        this.tick = function(){
            camera.getWorldPosition(skybox.position);
        }
    }
}
export {World}
