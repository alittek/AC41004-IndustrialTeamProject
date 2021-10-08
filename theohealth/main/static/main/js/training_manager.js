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
  
  // buffer which contains all the sensor readings with associated timestamps
  const buffer = [
    [2021-09-30T10:27:53.047Z, 46],
    [2021-09-30T10:27:53.558Z, 254],
    [2021-09-30T10:27:54.581Z, 670]
  ]

  // get the current time
  var date = new Date()
  var currentTime = date.getFullYear() + '-' + (date.getMonth()+1) + '-' + date.getDate() + 'T' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + '.' + date.getMilliseconds() + 'z'

  // set the reference point for where the browser currently is in real time
  var reference_point = currentTime + Date(2021-09-30T10:27:53.047Z)

  for (let i = 0; i < time.now; i++) {  //for every second
    while (isBufferInPast(buffer[[n]], reference_point) == true) {  // check if the buffer is before the reference point and if it is then move on to the next value
      n += 1  // go to the next value
    }
    new_reading = buffer[[n]]
    // return new_reading
  }
  return new_reading
}

/**
 * isBufferInPast()
 * 
 * function which checks if the most recent 
 */
function isBufferInPast(buffer, reference_point) {
  if (buffer[[]] < reference_point) {
    return true
  }
  return false
}