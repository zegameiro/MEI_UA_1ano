###############################################################################
#       						Cone.py
###############################################################################

# This example creates a polygonal model of a Cone e visualize the results in a
# VTK render window.
# The program creates the cone, rotates it 360º and closes
# The pipeline  source -> mapper -> actor -> renderer  is typical
# and can be found in most VTK programs

# Imports

# Import all VTK modules
from vtkmodules.all import *

# Import only needed modules
# import vtkmodules.vtkInteractionStyle
# import vtkmodules.vtkRenderingOpenGL2
# from vtkmodules.vtkFiltersSources import vtkConeSource
# from vtkmodules.vtkRenderingCore import (
#     vtkActor,
#     vtkPolyDataMapper,
#     vtkRenderWindow,
#     vtkRenderWindowInteractor,
#     vtkRenderer
# )


def render_cone():

    # We Create an instance of vtkConeSource and set some of its
    # properties. The instance of vtkConeSource "cone" is part of a
    # visualization pipeline (it is a source process object); it produces data
    # (output type is vtkPolyData) which other filters may process.

    coneSource = vtkConeSource()
    coneSource.SetCenter(0.5, 0.0, 0.5)
    coneSource.SetHeight(2.0)
    coneSource.SetRadius(1.0)
    coneSource.SetResolution(100)

    # We create an instance of vtkPolyDataMapper to map the polygonal data
    # into graphics primitives. We connect the output of the cone source
    # to the input of this mapper.

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(coneSource.GetOutputPort())

    # We create an actor to represent the cone. The actor orchestrates rendering
    # of the mapper's graphics primitives. An actor also refers to properties
    # via a vtkProperty instance, and includes an internal transformation
    # matrix. We set this actor's mapper to be coneMapper which we created
    # above.

    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)

    return coneActor


def render_sphere():
    sphereSource = vtkSphereSource()
    sphereSource.SetCenter(-2.0, 0.0, -2.0)
    sphereSource.SetRadius(2.0)
    sphereSource.SetPhiResolution(100)
    sphereSource.SetThetaResolution(100)

    shereMapper = vtkPolyDataMapper()
    shereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtkActor()
    sphereActor.SetMapper(shereMapper)

    return sphereActor


def render_cylinder():
    cylinderSource = vtkCylinderSource()
    cylinderSource.SetCenter(3.0, 0.0, 3.0)
    cylinderSource.SetRadius(2.0)
    cylinderSource.SetHeight(3.0)
    cylinderSource.SetResolution(100)

    cylinderMapper = vtkPolyDataMapper()
    cylinderMapper.SetInputConnection(cylinderSource.GetOutputPort())

    cylinderActor = vtkActor()
    cylinderActor.SetMapper(cylinderMapper)

    return cylinderActor


def render_cube():
    cubeSource = vtkCubeSource()
    cubeSource.SetCenter(0.0, 3.0, 0.0)
    cubeSource.SetXLength(2.0)
    cubeSource.SetYLength(2.0)
    cubeSource.SetZLength(2.0)

    cubeMapper = vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cubeSource.GetOutputPort())

    cubeActor = vtkActor()
    cubeActor.SetMapper(cubeMapper)

    return cubeActor


def main():
    coneActor = render_cone()
    sphereActor = render_sphere()
    cylinderActor = render_cylinder()
    cubeActor = render_cube()

    # Create the Renderer and assign actors to it. A renderer is like a
    # viewport. It is part or all of a window on the screen and it is
    # responsible for drawing the actors it has.  We also set the background
    # color here.
    ren = vtkRenderer()
    ren.SetBackground(0.2, 0.0, 0.4)
    ren.AddActor(coneActor)
    ren.AddActor(sphereActor)
    ren.AddActor(cylinderActor)
    ren.AddActor(cubeActor)

    ## RENDER INERT CAMERA
    # activeCam = ren.GetActiveCamera()
    # activeCam.SetPosition(10, 10, 10)
    # activeCam.SetViewUp(0, 1, 1)
    ## ORTHOGRAPHIC PROJECTION
    # activeCam.SetParallelProjection(True)

    ## CAMERA
    # cam1 = vtkCamera()
    # cam1.SetPosition(10,10,10)
    # cam1.SetViewUp(0,1,1)
    # ren.SetActiveCamera(cam1)

    ## LIGHT
    # cam1 = ren.GetActiveCamera()
    # light = vtkLight()
    # light.SetColor(1,0,0)
    # light.SetFocalPoint(cam1.GetFocalPoint())
    # light.SetPosition(cam1.GetPosition())
    # ren.AddLight(light)

    ## ACTOR PROPERTIES
    # coneActor.GetProperty().SetColor(0.2, 0.63, 0.79)
    # sphereActor.GetProperty().SetColor(0.0, 1.0, 0.0)
    # cylinderActor.GetProperty().SetColor(0.0, 0.0, 1.0)
    cubeActor.GetProperty().SetColor(1.0, 1.0, 0.0)

    # cubeActor.GetProperty().SetRepresentationToWireframe()

    ## LIGHT 2
    cam1 = ren.GetActiveCamera()
    light_red = vtkLight()
    light_green = vtkLight()
    light_blue = vtkLight()
    light_yellow = vtkLight()
    setColorAtPosition(light_red, (1, 0, 0), (-5, 0, 0))
    setColorAtPosition(light_green, (0, 1, 0), (0, 0, -5))
    setColorAtPosition(light_blue, (0, 0, 1), (5, 0, 0))
    setColorAtPosition(light_yellow, (1, 1, 0), (0, 0, 5))

    ren.AddLight(light_red)
    ren.AddLight(light_green)
    ren.AddLight(light_blue)
    ren.AddLight(light_yellow)

    # Finally we create the render window which will show up on the screen.
    # We put our renderer into the render window using AddRenderer. We also
    # set the size to be 300 pixels by 300.

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(700, 700)

    renWin.SetWindowName("geometric forms")

    """ # Now we loop over 360 degrees and render the cone each time.
    for i in range(0,360):
        # render the image
        renWin.Render()
        # rotate the active camera by one degree
        ren.GetActiveCamera().Azimuth(1)
 """

    # Adds a render window interactor to the cone example to
    # enable user interaction (e.g. to rotate the scene)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


def setColorAtPosition(light, color, position):
    light.SetColor(color)
    light.SetPosition(position)


if __name__ == "__main__":
    main()
