import vtk
import numpy as np

def pvector(point, data):
    # Create a locator to find the closest point
    points = vtk.vtkPoints()
    points.InsertNextPoint(point[0], point[1], point[2])
    pointsPoly = vtk.vtkPolyData()
    pointsPoly.SetPoints(points)
    probe = vtk.vtkProbeFilter()
    probe.SetInputData(pointsPoly)
    probe.SetSourceData(data)
    probe.Update()
    output = probe.GetOutput().GetPointData().GetArray("vectors").GetTuple3(0)
    return output

def rk4_integration(data, seed, step_size, max_steps):
    # Initialize streamline points
    streamline_points = []

    # Initialize RK4 parameters
    current_point = np.array(seed)
    for _ in range(max_steps):
        # Check if out of bounds
        bounds = data.GetBounds()
        if not all(bounds[2*i] <= current_point[i] <= bounds[2*i + 1] for i in range(3)):
            break
            
        # Forward integration
        k1 = np.array(pvector(current_point, data))
        k2 = np.array(pvector(current_point + step_size / 2 * k1, data))
        k3 = np.array(pvector(current_point + step_size / 2 * k2, data))
        k4 = np.array(pvector(current_point + step_size * k3, data))
        next_point = current_point + step_size / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        
        # Add points to streamline
        streamline_points.append(current_point)

        # Update current point
        current_point = next_point

    return streamline_points

def main():
    # Load vector field data set
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("tornado3d_vector.vti")  # Provide your file name
    reader.Update()
    data = reader.GetOutput()

    # Get user-provided seed location
    seed_input = input("Enter three cordinates separated by spaces: ")
    seed_values = seed_input.split()
    seed_values = [int(val) for val in seed_values]
    seed = np.array(seed_values)  
     
    # Define integration parameters
    step_size = 0.05
    max_steps = 1000

    # Perform RK4 integration
    streamline_forward = rk4_integration(data, seed, step_size, max_steps)
    streamline_backward = rk4_integration(data, seed, -step_size, max_steps)

    # Combine the forward and backward streamlines
    streamline_points = list(reversed(streamline_backward))[:-1] + streamline_forward
    # print(len(streamline_points))
    # Create a vtkPoints object from the streamline points
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    num_points = len(streamline_points)
    for i in range(num_points - 1):
        point = streamline_points[i]
        next_point = streamline_points[i + 1]
        
        points.InsertNextPoint(point)
        
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, i)
        line.GetPointIds().SetId(1, i + 1)
        lines.InsertNextCell(line)

    # Insert the last point
    points.InsertNextPoint(streamline_points[num_points - 1])
        
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    # Write result to file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("streamline_result.vtp")
    writer.SetInputData(polydata)
    writer.Write()

    # # Visualization
    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(polydata)
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(0, 1, 0)  # Green color
    # renderer = vtk.vtkRenderer()
    # renderer.AddActor(actor)
    # renderer.SetBackground(1, 1, 1)  # White background
    # render_window = vtk.vtkRenderWindow()
    # render_window.AddRenderer(renderer)
    # render_window.SetWindowName("Streamline Visualization")  # Set window title
    # interactor = vtk.vtkRenderWindowInteractor()
    # interactor.SetRenderWindow(render_window)
    # interactor.Initialize()
    # interactor.Start()

if __name__ == "__main__":
    main()
