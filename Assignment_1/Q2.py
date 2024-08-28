
import vtk

def create_color_transfer_function():
    """
    Create and define the color transfer function.
    """
    color_tf = vtk.vtkColorTransferFunction()
    color_points = {
        -4931.54: (0.0, 1.0, 1.0),
        -2508.95: (0.0, 0.0, 1.0),
        -1873.9: (0.0, 0.0, 0.5),
        -1027.16: (1.0, 0.0, 0.0),
        -298.031: (1.0, 0.4, 0.0),
        2594.97: (1.0, 1.0, 0.0)
    }
    for value, color in color_points.items():
        color_tf.AddRGBPoint(value, *color)
    return color_tf

def create_opacity_transfer_function():
    """
    Create and define the opacity transfer function.
    """
    opacity_tf = vtk.vtkPiecewiseFunction()
    opacity_points = {
        -4931.54: 1.0,
        101.815: 0.002,
        2594.97: 0.0
    }
    for value, opacity in opacity_points.items():
        opacity_tf.AddPoint(value, opacity)
    return opacity_tf

def create_volume_property(enable_phong_shading=False):
    """
    Create volume property with optional Phong shading.
    """
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(create_color_transfer_function())
    volume_property.SetScalarOpacity(create_opacity_transfer_function())
    
    if enable_phong_shading:
        volume_property.ShadeOn()
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    
    return volume_property

def create_outline_actor(reader):
    """
    Create outline actor.
    """
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(0, 0, 0)
    
    return outline_actor

def create_volume(reader, use_phong_shading):
    """
    Create volume with optional Phong shading.
    """
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)

    if use_phong_shading.lower() == "yes":
        volume.SetProperty(create_volume_property(enable_phong_shading=True))
    else:
        volume.SetProperty(create_volume_property())

    return volume

def setup_rendering():
    """
    Setup rendering components.
    """
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)  # Set background color to white

    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)

    return renderer, render_window

def initialize_interactor(render_window):
    """
    Initialize interactor.
    """
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    interactor.Start()

def main():
    """
    Main function to run the program.
    """
    # Load 3D data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("Data/Isabel_3D.vti")  # Update with your data file name
    reader.Update()

    # Take user input for Phong shading
    use_phong_shading = input("Do you want to enable Phong shading? (yes/no): ")

    # Create volume
    volume = create_volume(reader, use_phong_shading)

    # Create renderer and add volume and outline actor
    renderer, render_window = setup_rendering()
    renderer.AddVolume(volume)
    renderer.AddActor(create_outline_actor(reader))

    # Initialize interactor
    initialize_interactor(render_window)

if __name__ == "__main__":
    main()