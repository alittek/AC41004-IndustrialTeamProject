/*
 * Training Manager
 * a module that updates the heatmap according to sensor readings
 */
import { update_heatmap } from "./heatmap.js"

var sensor_value = 200
var buffer = []

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

/**
 * update()
 * 
 * function which takes in sensor readings with thier associated
 * timestamps and updates the currently displayed value 30 times a second
 */
function update() {
  var isBufferInPast = new Boolean(true) // variable used to return true if the timestamp in the buffer is behind the reference point
  var reference_point = 0 // initialising the reference point for where the browser currently is in real time
  Initial_Reference_point = buffer[0][0]  // inital reference point is set to be the time of the first timestamp in the buffer
  var timer // timer that tracks the time that has surpassed since the initial reference point - need to figure out how to implement time elapsed
  reference_point = initial_reference_point + timer // set the reference point to be the time elapsed since the initial reference point

  while (isBufferInPast == true) {  // check if the buffer is before the reference point and if it is then move on to the next value
    if (buffer[0][0] < reference_point) {
      isBufferInPast = true
    }
    else {
      break
    }

    Reference_point = Reference_point + timer() // update reference point
    buffer[0].shift()  // delete item at the top of the buffer so that the next item can be read in
  }
  
  new_reading = buffer[0][1]  // set the value at the most recent timestamp to be the new reading
  return new_reading  // return new_reading
}

/**
 * get_highest_reading()
 * 
 * finds and displays the highest reading from a workout
 */
function get_highest_reading() {
  var max_reading = 0   // stores the highest reading from the sensor
  var current_reading = 0   // stores the current reading from the buffer

  for (var i = 0; i < buffer[0].length; i++) {   // loop through each item in the buffer
    current_reading = buffer[0].shift()   // current reading = next time value
    if (max_reading < current_reading) {  // check if the current reading is higher than the highest reading
      max_reading = current_reading   // set the current reading as the new highest reading
      console.log(max_reading)  // send the max reading to the console
    }
    else {
      console.log(max_reading)  // send the max reading to the console
    }    
  }

}

/*
 * sends an AJAX request to /workout to get sensor readings and then periodically updates these
 */
function fetch_readings() {
  const xHttp = new XMLHttpRequest()
  xHttp.onload = function() {
    buffer = JSON.parse(this.responseText)
	  console.log(buffer)
    var simple_interval = setInterval(() => {
	
    var readings = Array(4)
    for (var s=0; s < buffer.length; s++) {
      if (buffer[s].length > 0) { // buffer has timestamps
	 
         readings[s] = buffer[s].shift()[1]
      } else {
        clearInterval(simple_interval)
      }
    }
    update_heatmap([readings[0], readings[1], readings[2], readings[3]])

    }, 500)
    }
  xHttp.open("GET", "/workout", true) // initialise request
  xHttp.send() // send request
}

fetch_readings()
