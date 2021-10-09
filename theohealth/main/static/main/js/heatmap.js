//import needed threejs libs
import * as THREE from 'https://cdn.skypack.dev/three@0.133.0'
import { OrbitControls } from 'https://cdn.skypack.dev/pin/three@v0.133.0-mRqtjW5H6POaf81d9bnr/mode=imports/unoptimized/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'https://cdn.skypack.dev/pin/three@v0.133.0-mRqtjW5H6POaf81d9bnr/mode=imports/unoptimized/examples/jsm/loaders/GLTFLoader.js'

//create secen and check its all added
var scene = new THREE.Scene()
scene.background = new THREE.Color('white')

var camera = new THREE.PerspectiveCamera(100, innerWidth / innerHeight, 0.1, 1000)
var canvas = document.getElementById("heatmap-canvas")
var renderer = new THREE.WebGLRenderer({antialias : true})

//light (change so it lights the back side or moves with camera???)
var light = new THREE.AmbientLight(0xffffff, 0.5)
var lightS = new THREE.DirectionalLight(0xffffff, 0.7)

//make sure secen fits the window
renderer.setSize(innerWidth*0.7, innerHeight*0.7)
renderer.setPixelRatio(devicePixelRatio)
// document.body.appendChild(renderer.domElement)
document.getElementById("heatmap").appendChild(renderer.domElement)


//Model loader and mesh
var loader = new GLTFLoader()
//var mesh = new THREE.Mesh(loader, material)
var reading = 200 // this will need to be the function that gets the readings (mkae a place holder)

//Material libary, c1 = low  c6 = high (more can be added if needed 6 was a good test range)
var c1 = new THREE.MeshStandardMaterial({ color: 0xc8d124 })
var c2 = new THREE.MeshStandardMaterial({ color: 0xd1b424 })
var c3 = new THREE.MeshStandardMaterial({ color: 0xd18624 })
var c4 = new THREE.MeshStandardMaterial({ color: 0xd15e24 })
var c5 = new THREE.MeshStandardMaterial({ color: 0xd14424 })
var c6 = new THREE.MeshStandardMaterial({ color: 0xd12424 })

//set the light and camera positions for the secen
light.position.set(0, 0, 1)
camera.position.z = 7
camera.position.y = 0

//orbit Controls
const controls = new OrbitControls(camera, renderer.domElement)
controls.minPolarAngle=controls.maxPolarAngle=1.57079
controls.enablePan = false; //fixes the movment my need to limit it rather than stop it
//zoom distance
controls.minDistance = 4; 
controls.maxDistance = 8;

//addlights
scene.add(light)
scene.add(lightS)

//create the modles(all included for later use)
var UpperRightLeg = new THREE.Object3D()
var UpperLeftLeg = new THREE.Object3D()
var LowerRightLeg = new THREE.Object3D()
var LowerLeftLeg = new THREE.Object3D()

function modleload() {
  //Lower left leg
  loader.load('/static/main/3d_models/LowerL.gltf', function(gltf) {
    LowerLeftLeg = gltf.scene.children.find((child) => child.name === "LowerLeft")
    LowerLeftLeg.position.y = -3
    scene.add(LowerLeftLeg);
  })
  loader.load('/static/main/3d_models/LowerR.gltf', function(gltf) {
    LowerRightLeg = gltf.scene.children.find((child) => child.name === "LowerRight")
    LowerRightLeg.position.y = -3
    scene.add(LowerRightLeg);
  })
  loader.load('/static/main/3d_models/UpplerL.gltf', function(gltf) {
    UpperRightLeg = gltf.scene.children.find((child) => child.name === "UpperLeft")
    UpperRightLeg.position.y = -3
    scene.add(UpperRightLeg);
  })
  loader.load('/static/main/3d_models/UpperR.gltf', function(gltf) {
    UpperLeftLeg = gltf.scene.children.find((child) => child.name === "UpperRight")
    UpperLeftLeg.position.y = -3
    scene.add(UpperLeftLeg);
  })
}


var thresholds = [
	{threshold: 100, mesh: new THREE.MeshStandardMaterial({ color: 0xc8d124 }) },
	{threshold: 150, mesh: new THREE.MeshStandardMaterial({ color: 0xd1b424 }) },
	{threshold: 200, mesh: new THREE.MeshStandardMaterial({ color: 0xd18624 }) },
	{threshold: 250, mesh: new THREE.MeshStandardMaterial({ color: 0xd15e24 }) },
	{threshold: 300, mesh: new THREE.MeshStandardMaterial({ color: 0xd14424 }) },
	{threshold: 350, mesh: new THREE.MeshStandardMaterial({ color: 0xc8d124 }) },
]
/*
There will be a colourChanger for each limb when the "reading" test data is replaced
currently all limbs change to the same colour because we dont have 4 reading genorators 
I have changed the order for the limbs to better show what the end product will be but they
should be c1 - c6 in order
*/
function colourChanger()
  {
    console.log(reading)
   switch(reading) {
    case 300 : {LowerLeftLeg.material = c3, LowerRightLeg.material = c1, UpperLeftLeg.material = c2, UpperRightLeg.material = c1}
    break
    case 500 : {LowerLeftLeg.material = c3, LowerRightLeg.material = c4, UpperLeftLeg.material = c2, UpperRightLeg.material = c2}
    break
    case 600 : {LowerLeftLeg.material = c4, LowerRightLeg.material = c4, UpperLeftLeg.material = c2, UpperRightLeg.material = c1}
    break
    case 700 : {LowerLeftLeg.material = c2, LowerRightLeg.material = c4, UpperLeftLeg.material = c1, UpperRightLeg.material = c3}
    break
    case 800 : {LowerLeftLeg.material = c6, LowerRightLeg.material = c5, UpperLeftLeg.material = c3, UpperRightLeg.material = c3}
    break
    case 900 : {LowerLeftLeg.material = c5, LowerRightLeg.material = c6, UpperLeftLeg.material = c2, UpperRightLeg.material = c1}
    break
   }
  }

//load modles
modleload()

function animate() {
  requestAnimationFrame(animate)
  renderer.render(scene, camera)
}

/*
 * updates the heatmap to the value specified in new_reading
 */
export function update_heatmap(new_reading) {
  requestAnimationFrame(animate)
  reading = new_reading
  colourChanger()
}

