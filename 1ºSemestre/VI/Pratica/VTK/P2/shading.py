from vtkmodules.all import *

def render_sphere():
    sphereSource = vtkSphereSource()
    sphereSource.SetCenter(0, 0, 0)
    sphereSource.SetRadius(2.0)
    sphereSource.SetPhiResolution(10)
    sphereSource.SetThetaResolution(10)

    shereMapper = vtkPolyDataMapper()
    shereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtkActor()
    sphereActor.SetMapper(shereMapper)

    return sphereActor

def main ():
    sphereActor1 = render_sphere()
    sphereActor2 = render_sphere()
    sphereActor2.GetProperty().SetInterpolationToFlat()
    sphereActor3 = render_sphere()
    sphereActor3.GetProperty().SetInterpolationToGouraud()
    sphereActor4 = render_sphere()
    sphereActor4.GetProperty().SetInterpolationToPhong()

    ren = vtkRenderer()
    ren.AddActor(sphereActor1)
    ren.SetBackground(0.8, 0.3, 0.3)  # Light red
    ren.SetViewport(0, 0.5, 0.5, 1)

    ren2 = vtkRenderer()
    ren2.AddActor(sphereActor2)
    ren2.SetBackground(0.3, 0.8, 0.3)  # Light green
    ren2.SetViewport(0.5, 0.5, 1, 1)
    ren2.GetActiveCamera().Azimuth(90)
    ren2.GetActiveCamera().SetPosition(0, 10, 8)

    ren3 = vtkRenderer()
    ren3.AddActor(sphereActor3)
    ren3.SetBackground(0.3, 0.3, 0.8)  # Light blue
    ren3.SetViewport(0, 0, 0.5, 0.5)
    ren3.GetActiveCamera().Azimuth(180)
    ren3.GetActiveCamera().SetPosition(0, 10, 8)

    ren4 = vtkRenderer()
    ren4.AddActor(sphereActor4)
    ren4.SetBackground(0.8, 0.8, 0.3)  # Light yellow
    ren4.SetViewport(0.5, 0, 1, 0.5)
    ren4.GetActiveCamera().Azimuth(270)
    ren4.GetActiveCamera().SetPosition(0, 10, 8)

    
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.AddRenderer(ren2)
    renWin.AddRenderer(ren3)
    renWin.AddRenderer(ren4)

    renWin.SetSize(600, 600)
    renWin.SetWindowName('S H A D I N G')

    
    # # Adds a render window interactor to the cone example to
    # # enable user interaction (e.g. to rotate the scene)
    # iren = vtkRenderWindowInteractor()
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # iren.Start()

    # Now we loop over 360 degrees and render the cone each time.
    for i in range(0,360):
        # render the image
        renWin.Render()
        # rotate the active camera by one degree
        ren.GetActiveCamera().Azimuth(1)
        ren2.GetActiveCamera().Azimuth(1)
        ren3.GetActiveCamera().Azimuth(1)
        ren4.GetActiveCamera().Azimuth(1)

if __name__ == '__main__':
    main()