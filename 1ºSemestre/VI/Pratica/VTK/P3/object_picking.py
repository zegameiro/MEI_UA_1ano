from vtkmodules.all import *

def render_cone():

    coneSource = vtkConeSource()
    coneSource.SetCenter(0.5, 0.0, 0.5)
    coneSource.SetHeight(2.0)
    coneSource.SetRadius(1.0)
    coneSource.SetResolution(5)

    return coneSource

def render_sphere():
    sphereSource = vtkSphereSource()
    sphereSource.SetCenter(-2.0, 0.0, -2.0)
    sphereSource.SetRadius(2.0)
    sphereSource.SetPhiResolution(10)
    sphereSource.SetThetaResolution(10)

    return sphereSource

def main():
    # Cone setup
    coneSource = render_cone()
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(coneSource.GetOutputPort())
    
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)

    # Sphere setup
    sphereSource = render_sphere()
    sphereMapper = vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
    
    sphereActor = vtkActor()
    sphereActor.SetMapper(sphereMapper)

    # Glyph setup (glyphing the cone onto the sphere)
    glyph = vtkGlyph3D()
    glyph.SetSourceConnection(coneSource.GetOutputPort())  # Cone as the glyph
    glyph.SetInputConnection(sphereSource.GetOutputPort())  # Sphere defines placement
    glyph.SetScaleFactor(0.25)
    glyph.SetVectorModeToUseNormal()
    
    glyphMapper = vtkPolyDataMapper()
    glyphMapper.SetInputConnection(glyph.GetOutputPort())

    glyphActor = vtkActor()
    glyphActor.SetMapper(glyphMapper)

    # Renderer setup
    renderer = vtkRenderer()  
    renderer.AddActor(sphereActor)
    renderer.AddActor(glyphActor) 
    renderer.SetBackground(0.2, 0.3, 0.4)
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName("O B J E C T   P I C K I N G")

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # Picker setup
    pointPicker = vtkPointPicker()
    iren.SetPicker(pointPicker)

    # Sphere for selected point
    selectedSphereSource = vtkSphereSource()
    selectedSphereSource.SetRadius(0.1)

    selectedSphereMapper = vtkPolyDataMapper()
    selectedSphereMapper.SetInputConnection(selectedSphereSource.GetOutputPort())

    selectedSphereActor = vtkActor()
    selectedSphereActor.SetMapper(selectedSphereMapper)
    selectedSphereActor.SetVisibility(False)
    renderer.AddActor(selectedSphereActor)

    def pointer_callback(picker: vtkPointPicker, event):
        pickPosition = picker.GetPickPosition()
        print(f"Picked point coordinates: {pickPosition}")

        # Update the position of the selected sphere
        selectedSphereActor.SetPosition(pickPosition)
        selectedSphereActor.SetVisibility(True)
        selectedSphereActor.GetProperty().SetColor(1.0, 0.0, 0.0)
        renderWindow.Render()

    pointPicker.AddObserver(vtkCommand.EndPickEvent, pointer_callback)

    renderWindow.Render()
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()
