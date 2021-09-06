#!/usr/bin/python
import linuxcnc, hal, time

lube = hal.component("lube")
lube.newpin("fault", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("fault2", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("run", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("delay", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("machine_status", hal.HAL_BIT, hal.HAL_IN)
lube.newpin("spindle_status", hal.HAL_BIT, hal.HAL_IN)
lube.newpin("pressuresw_floatsw", hal.HAL_BIT, hal.HAL_IN)
lube.newpin("reset", hal.HAL_BIT, hal.HAL_IN)
lube.ready()

#initialize variables
lube['run'], lube['fault'] = 0, 0
try:
    while 1:
        time.sleep(0.5)
        lube['delay'] = 0
        #1. machine needs to be on
        #2. spindle needs to be running like in a g-code program
        #3. there should be no pump faults
        if(lube['machine_status'] and lube['spindle_status'] and not lube['fault']):
            if(lube['pressuresw_floatsw']):
				lube['fault2'] = 1;
            lube['run'] = 1;
            time.sleep(10) #run pump for 10s
            if(lube['pressuresw_floatsw']):
                lube['fault2'] = 0;
                time.sleep(50) #continue running pump for an additional 50s
                lube['run'] = 0;
                lube['delay'] = 1; #show that pump is resting
                time.sleep(720) #let the pump rest for 720s (12 min)            
            else:
                lube['run'] = 0; #shut off pump immediately
                lube['fault'] = 1; #there is a fault if input 14 becomes active (fluid low or a big leak somewhere)
                 
        #gives user to ability to reset the fault after fluid was filled or leak was fixed
        if(lube['reset']):
            lube['fault'] = 0;
            lube['reset'] = 0; #reset the reset!

except KeyboardInterrupt:
    raise SystemExit

