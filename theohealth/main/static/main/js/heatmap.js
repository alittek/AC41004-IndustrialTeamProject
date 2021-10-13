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
//grey
var d = new THREE.MeshStandardMaterial({ color: 0xa6a6a6 })

//set the light and camera positions for the secen
light.position.set(0, 0, 1)
camera.position.z = 7
camera.position.y = 17

//orbit Controls
const controls = new OrbitControls(camera, renderer.domElement)
controls.minPolarAngle=controls.maxPolarAngle=1.57079
controls.enablePan = false; //fixes the movment my need to limit it rather than stop it
//zoom distance
controls.minDistance = 22; 
controls.maxDistance = 32;

//addlights
scene.add(light)
scene.add(lightS)

var models = Array(4)
for (let i=0; i < models.length; i++) {
	models[i] = new THREE.Object3D()
}
//create the modles(all included for later use)
var UpperRightLeg = new THREE.Object3D()
var UpperLeftLeg = new THREE.Object3D()
var LowerRightLeg = new THREE.Object3D()
var LowerLeftLeg = new THREE.Object3D()
var RightLeg = new THREE.Object3D()
var LeftLeg = new THREE.Object3D()


function modleload() {

  //Lower left leg

  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    LowerLeftLeg = gltf.scene.children.find((child) => child.name === "LeftHamstring")
    LowerLeftLeg.position.y = 22
    scene.add(LowerLeftLeg);
  })
  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    LowerRightLeg = gltf.scene.children.find((child) => child.name === "LeftQuad")
    LowerRightLeg.position.y = 22
    scene.add(LowerRightLeg);
  })
  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    UpperRightLeg = gltf.scene.children.find((child) => child.name === "RightQuad")
    UpperRightLeg.position.y = 22
    scene.add(UpperRightLeg);
  })
  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    UpperLeftLeg = gltf.scene.children.find((child) => child.name === "RightHamstring")
    UpperLeftLeg.position.y = 22
    scene.add(UpperLeftLeg);
  })
  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    LeftLeg = gltf.scene.children.find((child) => child.name === "LeftLeg")
    LeftLeg.position.y = 22
    LeftLeg.material = d
    scene.add(LeftLeg);
  })
  loader.load('/static/main/3d_models/Leg_Model_1.gltf', function(gltf) {
    RightLeg = gltf.scene.children.find((child) => child.name === "RightLeg")
    RightLeg.position.y = 22
    RightLeg.material = d
    scene.add(RightLeg);
  })
}


var thresholds = [
	{threshold: 0, material: new THREE.MeshStandardMaterial({ color: 0xc8d124 }) },
	{threshold: 300, material: new THREE.MeshStandardMaterial({ color: 0xd1b424 }) },
	{threshold: 500, material: new THREE.MeshStandardMaterial({ color: 0xd18624 }) },
	{threshold: 600, material: new THREE.MeshStandardMaterial({ color: 0xd15e24 }) },
	{threshold: 700, material: new THREE.MeshStandardMaterial({ color: 0xd14424 }) },
	{threshold: 900, material: new THREE.MeshStandardMaterial({ color: 0xc12424 }) },
]
/*
There will be a colourChanger for each limb when the "reading" test data is replaced
currently all limbs change to the same colour because we dont have 4 reading genorators 
I have changed the order for the limbs to better show what the end product will be but they
should be c1 - c6 in order
*/
function colourChanger(readings)
  {
  let t = 0
  for (let r=0; r < 4; r++) {
    t = 0
    for (let i=0; i<thresholds.length; i++) {
	if (readings[r] > thresholds[i].threshold) {
		t = i
	}
    }
    models[r].material = thresholds[t].material
  }
  }

function animate() {
  requestAnimationFrame(animate)
  renderer.render(scene, camera)
}

/*
 * updates the heatmap to the value specified in new_reading
 */
export function update_heatmap(readings) {
  colourChanger(readings)
}

// Set up heatmap
modleload()
requestAnimationFrame(animate)

