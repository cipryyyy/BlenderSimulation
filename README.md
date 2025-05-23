# Blender is Physics

A Python library of scripts for simulating basic physics in Blender 3D. Just paste it into the Text Editor inside Blender and hit "Run Script".

## Available Simulations

* `General`: Simulates free movement of the default cube with basic damping, friction, and viscosity effects.
* `FreeFall`: Free fall of an object (default = cube), with terminal velocity calculation.
* `PID`: Simulate a PID controller with the cube, allowing dynamic tuning of `k_p`, `k_i`, and `k_d` to reach defined setpoints over time.

## imitations & Future Improvements
* Currently supports only translation, rotation physics will be added in the future.
* Friction and viscosity are simplified and not physically accurate.
* Momentum, Inertia and other simulations will be added.
* Edit the scripts to support additional objects beyond the default cube.
