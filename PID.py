#Libraries
import bpy
import sys
import math

#Data of the simulation
cube = bpy.data.objects["Cube"]
cube.location = [0,0,0]         #Starting position at 0, 0, 0
mass = 1                        #cube mass
t = 0                           #time start at 0
g = -9.81                       #gravity

#Class to elegantly store datas
class Store:                     
    def __init__(s, name="Random", x=0, y=0, z=0):
        s.name = name
        s.x = x
        s.y = y
        s.z = z
    def __str__(s):                                     #DEBUG
        return(f"{s.name} data: {s.x}, {s.y}, {s.z}")
    def toList(s):
        return [s.x,s.y,s.z]

#Forces, velocities and position
Force    = Store("Force", 0, 0, 0)
Velocity = Store("Velocity", 0, 0, 0)
Position = Store("Position", cube.location[0], cube.location[1], cube.location[2])

#Coefficients
friction = 0.05        #0:Slides forever, 1: No slide
damping = 0.5          #0:Bounce forever, 1:No bounce

#Video datas
frame = 0       #Starting at frame 0
fps = 24        #Match the project framerate
end = 30        #seconds, project duration

#PID values
PIDsim = True
Setpoint = Store("Setpoint", 0, 0, 10)            #Setpoint to reach
Integral = Store("Integral", 0, 0, 0)             #Integral, for integrative gain
OldError = Store("Old Error", 0, 0, 0)            #oldError, for derivative gain

#Loading bar
def loadingBar(current, total):
    percent = (current / total) * 100
    bar_length = 40                    
    bar_filled_length = int(bar_length * (current / total))
    bar = '█' * bar_filled_length + '-' * (bar_length - bar_filled_length) 

    sys.stdout.write(f'\r|{bar}| {percent:.2f}% ({current}/{total}) frame(s)') 
    sys.stdout.flush()

#PID controller
def PID(position, setpoint, integral, old_error, minVAL, maxVAL):
    #PARAMETERS, 2.2, 0.8, 2 are kinda good
    kp = 2.2                    #Proportional
    ki = 0.8                    #Integral
    kd = 2                      #Derivative
    
    #Infos about past, present and future
    e = setpoint-position       #Error between output and setpoint
    dt = 1/fps                  #Delta of the time
    integral += e * dt              #Update the integral
    derivative = (e-old_error)/dt    #Calculate the derivative
    
    #Calculate the values
    pOUT = kp * e
    iOUT = ki * integral
    dOUT = kd * derivative
    
    Out = pOUT + iOUT + dOUT   #TOTAL

    if abs(Out) < minVAL:             #If the output is less than the minimum, return the minimum
        try:
            Out = minVAL * (Out/abs(Out))
        except ZeroDivisionError:
            pass
    if Out > 0:                         #Return limited by the max output
        return min(Out, maxVAL), integral, e
    return max(Out, -maxVAL), integral, e

#Main function
def main():
    #Global variables:
    global t, g, frame                  #META
    global Position, Velocity, Force    #PHYSICS
    global damping, friction            #GROUND
    global Setpoint, Integral, OldError #PID
    
    #UPDATE the cube status
    Velocity.x += (Force.x/mass)/fps
    Velocity.y += (Force.y/mass)/fps
    Velocity.z += g / fps + (Force.z/mass) / fps
    
    Position.x += Velocity.x/fps
    Position.y += Velocity.y/fps
    Position.z += Velocity.z/fps
    
    if Position.z <= 0:      #Bounce detection
        Position.z = 0
        Velocity.z = -Velocity.z * (1 - damping)
    
    bpy.data.objects["Cube"].location = Position.toList()     #New position
        
    #PID simulator
    if PIDsim:    
        Force.x, Integral.x, OldError.x = PID(Position.x, Setpoint.x, Integral.x, OldError.x, 0.10, 20)
        Force.y, Integral.y, OldError.y = PID(Position.y, Setpoint.y, Integral.y, OldError.y, 0.10, 20)
        Force.z, Integral.z, OldError.z = PID(Position.z, Setpoint.z, Integral.z, OldError.z, 0.10, 20)
    
    #Insert the keyframe and go to the next frame
    cube.keyframe_insert(data_path = "location", frame = frame)     #Save posititon
    bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_current + 1)
    frame += 1
    t += 1/fps  #Increment time and frame
    
    if frame >= (end * fps):    #If simulation is done
        print("\n=== Simulation ended ===")
        return None
    
    loadingBar(frame, round(end * fps - 1))     #display progress bar
    return 1/fps                                #Wait for next call

if __name__== "__main__":
    print("\n\n\n=== Simulation started ===")
    cube.animation_data_clear()                                   #Delete old keyframes
    bpy.data.scenes["Scene"].frame_end = round(end * fps - 1)     #Set the end
    bpy.data.scenes['Scene'].frame_set(0)                         #Go to frame 0
    bpy.app.timers.register(main)                                 #Call main function
