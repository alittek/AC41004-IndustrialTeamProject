//import needed threejs libs
import * as THREE from 'https://cdn.skypack.dev/three@0.133.0'
import { OrbitControls } from 'https://cdn.skypack.dev/pin/three@v0.133.0-mRqtjW5H6POaf81d9bnr/mode=imports/unoptimized/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'https://cdn.skypack.dev/pin/three@v0.133.0-mRqtjW5H6POaf81d9bnr/mode=imports/unoptimized/examples/jsm/loaders/GLTFLoader.js'

//create secen and check its all added
var scene = new THREE.Scene()
scene.background = new THREE.Color('white')

var camera = new THREE.PerspectiveCamera(100, innerWidth / innerHeight, 0.1, 1000)
var canvas = document.getElementById("heatmap-canvas")
var renderer = new THREE.WebGLRenderer()

//light (change so it lights the back side or moves with camera???)
var light = new THREE.AmbientLight(0xffffff, 0.5)
var lightS = new THREE.DirectionalLight(0xffffff, 0.7)

//make sure secen fits the window
renderer.setSize(innerWidth, innerHeight)
renderer.setPixelRatio(devicePixelRatio)
// document.body.appendChild(renderer.domElement)
document.getElementById("heatmap").appendChild(renderer.domElement)


//Model loader and mesh
var loader = new GLTFLoader()
//var mesh = new THREE.Mesh(loader, material)
var reading = 200 // this will need to be the function that gets the readings (mkae a place holder)

//three place holder materials for testing(more to be added or possibly dynamic colours ???)
var HighUseage = new THREE.MeshStandardMaterial({ color: 0xc91c1c })
var MedUseage = new THREE.MeshStandardMaterial({ color: 0xcf871b })
var LowUseage = new THREE.MeshStandardMaterial({ color: 0xd6d01e })

//set the light and camera positions for the secen
light.position.set(0, 0, 1)
camera.position.z = 8
camera.position.y = 2

//orbit Controls(fix these to much freedom ??)
const controls = new OrbitControls(camera, renderer.domElement)
controls.minPolarAngle=controls.maxPolarAngle=1.57079
controls.enablePan = false; //fixes the movment my need to limit it rather than stop it
//zoom distance
controls.minDistance = 4; 
controls.maxDistance = 8;

//addlights
scene.add(light)
scene.add(lightS)

function modleload() {
  //Lower left leg
  loader.load('/static/main/3d_models/LowerL.gltf', function(gltf) {
    var lowerlMesh = gltf.scene.children.find((child) => child.name === "LowerLeft")
    lowerlMesh.position.y = -3
    
    addLleftmesh(lowerlMesh);

  })
}

function addLleftmesh(lowerlMesh) {
  var lower_left_leg = lowerlMesh.clone(true);
/*
  var colours = [
    [200, 0xd6d01e],
    [600, 0xcf871b],
    [900, 0xc91c1c]
  ]
*/
  if (reading == 200) {
    lower_left_leg.material = new THREE.MeshStandardMaterial({ color: 0xd6d01e })
    scene.remove(lower_left_leg)
    scene.add(lower_left_leg)
  } else if (reading == 600) {
    lower_left_leg.material = new THREE.MeshStandardMaterial({ color: 0xcf871b })
    scene.remove(lower_left_leg)
    scene.add(lower_left_leg)
  } else if (reading == 900) {
    lower_left_leg.material = new THREE.MeshStandardMaterial({ color: 0xc91c1c })
    scene.remove(lower_left_leg)
    scene.add(lower_left_leg)
  }

}

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
 // modleload()
}

