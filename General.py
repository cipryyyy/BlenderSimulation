#Libraries
import bpy
import sys
import math

#Data of the simulation
cube = bpy.data.objects["Cube"]
cube.location = [0,0,1]         #Starting position
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
    
    def mul(s, value):
            s.x *= value
            s.y *= value
            s.z *= value
    def add(s, value):
            s.x += value
            s.y += value
            s.z += value
    def toList(s):
        return [s.x,s.y,s.z]

#Forces, velocities and position
Acceleration = Store("Acceleration", 0, 0, 10) #Positive = up, negative = down
Velocity     = Store("Velocity", 10, 0, 0)
Position     = Store("Position", cube.location[0], cube.location[1], cube.location[2])

#Coefficients, 0:min <---> 1:max
viscousity = 0.05       #0: No Viscousity, 1: Really really high viscousity
friction = 0.5         #0:Slides forever, 1: No slide
damping = 0.5          #0:Bounce forever, 1: No bounce

#Video datas
frame = 0        #Starting at frame 0
fps = 24         #Match the project framerate
end = 10         #seconds, project duration

#Loading bar
def loadingBar(current, total):
    percent = (current / total) * 100
    bar_length = 40                    
    bar_filled_length = int(bar_length * (current / total))
    bar = '█' * bar_filled_length + '-' * (bar_length - bar_filled_length) 

    sys.stdout.write(f'\r|{bar}| {percent:.2f}% ({current}/{total}) frame(s)') 
    sys.stdout.flush()

#Main function
def main():
    #Global variables:
    global t, g, frame                          #META
    global Position, Velocity, Acceleration     #PHYSICS
    global damping, friction, viscousity        #ENV
    
    #Update acceleration
    Acceleration.mul(1-viscousity)
      
    #Update velocity
    Velocity.x += (Acceleration.x)/fps
    Velocity.y += (Acceleration.y)/fps
    Velocity.z += g / fps + (Acceleration.z) / fps
    
    #Update position
    Position.x += Velocity.x/fps
    Position.y += Velocity.y/fps
    Position.z += Velocity.z/fps
    
    if Position.z <= 0:      #Ground touch detection
        Position.z = 0
        
        Velocity.x *= (1 - friction)
        Velocity.y *= (1 - friction)
        Velocity.z *= -(1 - damping)
    
    bpy.data.objects["Cube"].location = Position.toList()     #New position
   
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
