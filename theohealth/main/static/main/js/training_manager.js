/*
 * Training Manager
 * a module that updates the heatmap according to sensor readings
 */
import { update_heatmap } from "./heatmap.js"

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

update_heatmap(200)


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
 * highest_reading()
 * 
 * finds and displays the highest reading from a workout
 */
function get_highest_reading() {
  var max_reading = 0
  var current_reading = 0

  for (var i = 0; i < buffer[0].length; i++) {
    current_reading = buffer[0].shift() // current reading = next time value
    if (max_reading < current_reading) {
      max_reading = current_reading
      console.log(max_reading)
    }
    else {
      console.log(max_reading)
    }    
  }

}

// from all files
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
