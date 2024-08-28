Big Data Analytics (CS661)
Assignment 3 

aditya katare 231110005
tanmay dubey 231110052

Particle Tracing in Steady Flow Field

Question 1:

Description:
This code performs Particle Tracing using Runge-Kutta 4 (RK4) integration on a 3D vector field dataset. The code generates streamlines in both forward and backward directions from a user-provided seed location and combines them into a single continuous line. The streamlines are stored as a VTKPolyData file (*.vtp) for visualization.

Enter the vtp file address in writer.SetFileName("streamline_result.vtp")

Usage and Visualization in Paraview:
1- Ensure you have Python and the required dependencies(VTK and numpy) installed.
2- Run the PYTHON script and when prompted on the terminal, enter the seed location as `x y z`.(0 0 7 as given in the question)
3- The streamline will be saved as 'streamline.vtp' in the current directory.
4- We can open the 'streamline.vtp' file in paraview to see the Particle Tracing in Steady Flow Field



