/*
 * Training Manager
 * a module that updates the heatmap according to sensor readings
 */
import { update_heatmap, update_highest_reading } from "./heatmap.js"

/*
 * Generates values for testing the heatmap
 */
function readingGen(old_reading) {
  var new_reading = 0
  if (old_reading == 200) {
    new_reading = 300
  } else if (old_reading == 300) {
    new_reading = 400
  } else if (old_reading == 400) {                                                             
    new_reading = 500                                                                          
  } else if (old_reading == 500) {                                                             
    new_reading = 600                                                                          
  } else if (old_reading == 600) {                                                             
    new_reading = 700                                                                          
  } else if (old_reading == 700) {                                                             
    new_reading = 800                                                                          
  } else if (old_reading == 800) {                                                             
    new_reading = 900                                                                          
  } else if (old_reading == 900) {                                                             
    new_reading = 200                                                                          
  }                                                                                            
  return new_reading
}

var sensor_value = 200

/*
  // uncomment to periodically change the heatmap
 var interval = setInterval(() => {
   sensor_value = readingGen(sensor_value)
   update_heatmap([sensor_value, sensor_value-100, sensor_value+200, sensor_value+300])
 }, 1000)
 */


let buffer = []
/*
* this function goes through all element in the buffer and displays them regardless of timestamps
*/
function simple_loop() {
    for (var i = 0; i < buffer[0].length; i++) {
      var current_reading = buffer[0].shift() // current reading = next time value
      console.log(current_reading)
     // update_heatmap(current_reading)
    }
}
var max_readings = [0,0,0,0]
// from all files
function fetch_readings() {
  const xHttp = new XMLHttpRequest()
  xHttp.onload = function() {
    buffer = JSON.parse(this.responseText)
	  console.log(buffer)
    var simple_interval = setInterval(() => {
	
    var readings = [0,0,0,0]
    for (var s=0; s < buffer.length; s++) {
	 console.log("readings: ", readings[0], readings[1], readings[2], readings[3])
      if (buffer[s].length > 0) { // buffer has timestamps
	 
         readings[s] = buffer[s].shift()[1]
         if (readings[s] > max_readings[s]) // max readings for each sensor
          max_readings[s] = readings[s]
          console.log("updated max readings: ", max_readings[0], max_readings[1], max_readings[2], max_readings[3])
          document.getElementById("highest-value-sen1").innerHTML = max_readings[0];
          document.getElementById("highest-value-sen2").innerHTML = max_readings[1];
          document.getElementById("highest-value-sen3").innerHTML = max_readings[2];
          document.getElementById("highest-value-sen4").innerHTML = max_readings[3];
      } else {
        clearInterval(simple_interval)
      }
    }
    update_heatmap([readings[0], readings[1], readings[2], readings[3]])
    // update_highest_reading([readings[0], readings[1], readings[2], readings[3]])

    }, 500)
    }
  xHttp.open("GET", "/workout", true) // initialise request
  xHttp.send() // send request
}

fetch_readings()
