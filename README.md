

# BlenderSimulation
### How to use it
Just use the default cube and run the script for the simulation, easy as that

## Variables
8 . **cube.location**: Modify the starting point with coordinates [*x*, *y*, *z*]

9 . **mass**: Weight of the object

10 . **a**: Acceleration of gravity 

15 . **xbalancer**: If *True*, *fx* will be adjusted to reach that location

16 . **ybalancer**: If *True*, *fy* will be adjusted to reach that location

17 . **zbalancer**: If *True*, *fz* will be adjusted to reach that location

21 .  **vx**, **vy**, **vz**: Initial velocities

25 . **fx**, **fy**, **fz**: Forces 

36 . **friction**: Slows down the block if it touches the ground

37 . **damping**: Slows down the bounces if it touches the ground

41 .  **fps**: Framerate of the project

42 . **end**: Duration of the simulation, in seconds

## Functions
* **loadingBar**

Give an update about the frames simulated

* **Status**

Print all the main datas of the project about the object

* **controlForce**

Updates the value of the given force

* **runner**

The main function, called every 1/24 seconds to update the cube location in the project and saves the keyframe

### Notes

* *Status* and *loadingBar* looks awful together, if one is active, the other one will be disabled
* It works like the *rigid body constraint*, rotations still aren't implemented
