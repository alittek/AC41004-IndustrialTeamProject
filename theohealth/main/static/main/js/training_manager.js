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

 // uncomment to periodically change the heatmap
var interval = setInterval(() => {
  sensor_value = readingGen(sensor_value)
  update_heatmap(sensor_value)
}, 1000)



// --- SCOTT'S CODE BELOW ---



/**
 * update()
 * 
 * function which takes in sensor readings with thier associated
 * timestamps and updates the currently displayed value 30 times a second
 */
function update() {
  const buffer = [  // buffer which contains all the sensor readings with associated timestamps
    [2021-09-30T10:27:53.047Z, 46],
    [2021-09-30T10:27:53.558Z, 254],
    [2021-09-30T10:27:54.581Z, 670]
  ]

  var isBufferInPast = new Boolean(false)

  var reference_point = 0 // initialising the reference point for where the browser currently is in real time

  // inital reference point is set to be the time of the first timestamp in the buffer
  Initial_Reference_point = buffer[0][0]  // set this to be 10 seconds before the first time in buffer

  setTimeout // timer that tracks the time that has surpassed since the initial reference point
  
  reference_point = initial_reference_point + TimeR() // set the reference point to be 

  for (let i = 0; i < time.now; i++) {  //for every second
    while (isBufferInPast(buffer[[n]], reference_point) == true) {  // check if the buffer is before the reference point and if it is then move on to the next value
      n += 1  // go to the next value
    }
    new_reading = buffer[[n]]
    // return new_reading
  }
  return new_reading
}