#Libraries
import bpy
import statistics
import sys

#DATA
cube = bpy.data.objects["Cube"]     #OBJECT, default cube <3
cube.location = [-4,9,25]    #Startinf position at 0, 0, 25
mass = 1                    #cube mass, for force calculation
t = 0                          #time start at 0, obv
a = -9.81                      #gravity
desiredPosx = -20           #desired position
desiredPosy = -40           #desired position
desiredHeight = 100           #desired height,  only positive
xbalancer = True                 #simulate force on z axis and stabilize the block
ybalancer = True                 #simulate force on z axis and stabilize the block
zbalancer = True                 #simulate force on z axis and stabilize the block
verbose = False             #Print on blender terminal, if false, progress bar
      
#Initial velocities
vx = 0
vy = 0
vz = 0

#Active forces
fx = 0
fy = 0
fz = 0

#Initial location
x = cube.location[0]
y = cube.location[1]
z = cube.location[2]

#Coefficient in case of ground touch
friction = 0.05        #0:Slides forever, 1: No slide
damping = 0.5         #0:Bounce forever, 1:No bounce

#Video data
frame = 0       #Starting at frame 0
fps = 24        #Match the project framerate
end = 30 #seconds, project duration

#Loading bar
def loadingBar(current, total):
    percent = (current / total) * 100
    bar_length = 40                         #Length of loading bar
    bar_filled_length = int(bar_length * (current / total))
    bar = '█' * bar_filled_length + '-' * (bar_length - bar_filled_length)    #To display

    sys.stdout.write(f'\r|{bar}| {percent:.2f}% ({current}/{total}) frame(s)')   #stdout to use single line
    sys.stdout.flush()

#Print function
def status(time, frame, lX, lY, lZ, vX, vY, vZ, force):
    print(f"{frame}", end=" [")                           #time info
    print(str(format(time, ".2f"))+ "s]:", end = "\t")
    
    print(format(lX, ".3f"), "m", end = ", ")       #position info
    print(format(lY, ".3f"), "m", end = ", ")
    print(format(lZ, ".3f"), "m", end = "\t")
    
    print(format(vX, ".3f"), "m/s", end = ", ")     #velocity info
    print(format(vY, ".3f"), "m/s", end = ", ")
    print(format(vZ, ".3f"), "m/s", end = "\t")
    
    print(format(force[0], ".3f"), end = ", ")                 #force info
    print(format(force[1], ".3f"), end = ", ")                 #force info
    print(format(force[2], ".3f"))                              #force info

#force controller
def controlForce(fz, vz, z, z_desired, m, g=0, max_step=100.0, tolerance=0.1, damping_factor=0.8):
    
    #Boring physics

    position_error = z_desired - z
    gravity_force = m * g

    if abs(position_error) < tolerance:
        if abs(vz) < 0.05:
            return gravity_force if g > 0 else 0
        else:
            fz += (gravity_force - fz) * damping_factor
            return fz

    step = max_step * (1 - min(abs(position_error) / 100, 1))

    if position_error > tolerance:
        fz += step * (position_error / abs(z_desired))
    elif position_error < -tolerance:
        fz -= step * (abs(position_error) / abs(z_desired))

    if vz > 0:
        fz -= step * (vz / 10)
    elif vz < 0:
        fz += step * (abs(vz) / 10)

    if g == 0:
        if abs(position_error) < tolerance * 5:
            fz -= damping_factor * vz
    else:
        if abs(position_error) < tolerance * 5:
            fz -= damping_factor * vz

    if abs(position_error) < tolerance * 2:
        return gravity_force if g > 0 else 0

    return max(fz, gravity_force - 10)

#Main function
def runner():
    global t, frame, x, y, z, vx, vy, vz, fx, fy, fz    #call global vars
    
    vx = vx + (fx/mass) / fps           #physics of the object
    vy = vy + (fy/mass) / fps
    vz = vz + a / fps + (fz/mass) / fps
    
    x = x + vx / fps
    y = y + vy / fps
    z = z + vz / fps
    
    if z <= 0:      #if it touches ground
        z = 0
        vx = vx * (1 - friction)        #x and y are slowed down
        vy = vy * (1 - friction)
        vz = -vz * (1 - damping)        #bounce will be smaller and smaller
    
    bpy.data.objects["Cube"].location = [x,y,z]     #set new position
    
    #Force simulation
    if xbalancer:
        fx = controlForce(fx, vx, x, desiredPosx, mass)
    if ybalancer:
        fy = controlForce(fy, vy, y, desiredPosy, mass)
    if zbalancer:
        fz = controlForce(fz, vz, z, desiredHeight, mass, a)
    #If disabled, block will bounce, nothing else
    #Else it will be stabilized at desiredHeight
    
    # Go to next frame and update values
    cube.keyframe_insert(data_path = "location", frame = frame)     #Save posititon
    bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_current + 1)
    frame += 1
    t += 1/fps  #Increment time and frame
    if verbose:
        status(t, frame, x, y, z, vx, vy, vz, [fx,fy,fz])   #print status
    
    if frame >= (end * fps):    #If simulation is done
        print("\n=== Simulation ended ===")
        return None         #Done
    if not verbose:
        loadingBar(frame, round(end * fps - 1))     #display progress bar
    return 1/fps            #Wait for next call

#Print data
print("\n\n\n=== Simulation started ===")
cube.animation_data_clear()           #Delete previous keyframes, it looks messy
bpy.data.scenes["Scene"].frame_end = round(end * fps - 1)   #Set end
bpy.data.scenes['Scene'].frame_set(0)                           #Frame 0
bpy.app.timers.register(runner)                                 #Call function
