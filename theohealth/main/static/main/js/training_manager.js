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


