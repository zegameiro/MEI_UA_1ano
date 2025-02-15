from vtkmodules.all import *

def render_main_cone():
    coneSource = vtkConeSource()
    coneSource.SetCenter(0.5, 0.0, 0.5)
    coneSource.SetHeight(2.0)
    coneSource.SetRadius(1.0)
    coneSource.SetResolution(100)

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(coneSource.GetOutputPort())

    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)

    return coneActor

def create_light_with_sphere(renderer, color, position):

    light = vtkLight()
    light.SetColor(color)
    light.SetPosition(position)
    light.SetFocalPoint(0.0, 0.0, 0.0)  # All lights point towards the origin
    renderer.AddLight(light)

    sphereSource = vtkSphereSource()
    sphereSource.SetCenter(position)
    sphereSource.SetRadius(0.5)
    sphereSource.SetPhiResolution(50)
    sphereSource.SetThetaResolution(50)

    sphereMapper = vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtkActor()
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(color)  # Match the light color
    sphereActor.GetProperty().LightingOff()  # Disable lighting for this sphere

    renderer.AddActor(sphereActor)

def main():
    mainSphereActor = render_main_cone()

    renderer = vtkRenderer()
    renderer.SetBackground(0.2, 0.0, 0.4)
    renderer.AddActor(mainSphereActor)

    create_light_with_sphere(renderer, (1, 0, 0), (-5, 0, 0))  # Red light
    create_light_with_sphere(renderer, (0, 1, 0), (0, 0, -5))  # Green light
    create_light_with_sphere(renderer, (0, 0, 1), (5, 0, 0))  # Blue light
    create_light_with_sphere(renderer, (1, 1, 0), (0, 0, 5))  # Yellow light

    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(700, 700)
    renderWindow.SetWindowName("Lights with Spheres")

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == "__main__":
    main()