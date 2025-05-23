#Libraries
import bpy
import statistics
import sys
import time

#DATA
cube = bpy.data.objects["Cube"]
cube.location = [0,0,0]    #Startinf position at 0, 0, 25
mass = 1                    #cube mass, for force calculation
t = 0                          #time start at 0
a = -9.81                      #gravity
desiredHeight = 10           #desired height,  only positive

fz = 0
vz = 0
z = cube.location[2]

#Coefficient in case of ground touch
friction = 0.05        #0:Slides forever, 1: No slide
damping = 0.5         #0:Bounce forever, 1:No bounce

#Video data
frame = 0       #Starting at frame 0
fps = 24        #Match the project framerate
end = 30 #seconds, project duration

#PID values
integral = 0
oldError = 0

#Loading bar
def loadingBar(current, total):
    percent = (current / total) * 100
    bar_length = 40                         #Length of loading bar
    bar_filled_length = int(bar_length * (current / total))
    bar = '█' * bar_filled_length + '-' * (bar_length - bar_filled_length)    #To display

    sys.stdout.write(f'\r|{bar}| {percent:.2f}% ({current}/{total}) frame(s)')   #stdout to use single line
    sys.stdout.flush()

#force controller
def PID(z, z_desired, minVAL, maxVAL):
    global integral
    global oldError
    
    kp = 2.2                      #GAIN
    ki = 0.8                    #INTERGRAL
    kd = 2                      #DERIVATIVE
    e = z_desired-z           #ERROR
    dt = 1/fps    #TIME DIFFERENCE
    
    integral += e * dt
    derivative = (e-oldError)/dt
    
    Ogain = e * kp
    Oint = ki * integral
    Oder = kd * derivative
    
    Out = Ogain + Oint + Oder
    
    if Out < minVAL:
        Out = minVAL
    oldError = e
    return (min(Out, maxVAL))

#Main function
def runner():
    global t, frame, z, vz, fz    #call global vars
    
    vz = vz + a / fps + (fz/mass) / fps
    
    z = z + vz / fps
    
    if z <= 0:      #if it touches ground
        z = 0
        vz = -vz * (1 - damping)        #bounce will be smaller and smaller
    
    bpy.data.objects["Cube"].location = [0,0,z]     #set new position
        
    fz = PID(z, desiredHeight, 0.10, 20)
    
    # Go to next frame and update values
    cube.keyframe_insert(data_path = "location", frame = frame)     #Save posititon
    bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_current + 1)
    frame += 1
    t += 1/fps  #Increment time and frame
    
    if frame >= (end * fps):    #If simulation is done
        print("\n=== Simulation ended ===")
        return None
    
    loadingBar(frame, round(end * fps - 1))     #display progress bar
    return 1/fps            #Wait for next call

#Print data
print("\n\n\n=== Simulation started ===")
cube.animation_data_clear()           #Delete previous keyframes, it looks messy
bpy.data.scenes["Scene"].frame_end = round(end * fps - 1)   #Set end
bpy.data.scenes['Scene'].frame_set(0)                           #Frame 0
bpy.app.timers.register(runner)                                 #Call function
