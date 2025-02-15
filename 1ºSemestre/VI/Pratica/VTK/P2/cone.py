###############################################################################
#       						Cone.py
###############################################################################

# This example creates a polygonal model of a Cone e visualize the results in a
# VTK render window.
# The program creates the cone, rotates it 360º and closes
# The pipeline  source -> mapper -> actor -> renderer  is typical 
# and can be found in most VTK programs
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

##############################
# Callback for the interaction
##############################
class vtkMyCallback(object):
    def __init__(self, renderer):
        self.ren = renderer

    def __call__(self, caller, ev):
        # Just do this to demonstrate who called callback and the event that triggered it.
        print(caller.GetClassName(), 'Event Id:', ev)
        # Now print the camera position.
        print("Camera Position: %f, %f, %f" % (self.ren.GetActiveCamera().GetPosition()[0],self.ren.GetActiveCamera().GetPosition()[1],self.ren.GetActiveCamera().GetPosition()[2]))
    
    # Callback for the interaction


def render_cone_p1():

    # We Create an instance of vtkConeSource and set some of its
    # properties. The instance of vtkConeSource "cone" is part of a
    # visualization pipeline (it is a source process object); it produces data
    # (output type is vtkPolyData) which other filters may process.

    coneSource = vtkConeSource()
    coneSource.SetCenter(0, 0, 0)
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

def render_cones():

    # We Create an instance of vtkConeSource and set some of its
    # properties. The instance of vtkConeSource "cone" is part of a
    # visualization pipeline (it is a source process object); it produces data
    # (output type is vtkPolyData) which other filters may process.
    
    coneSource = vtkConeSource()
    
    # We create an instance of vtkPolyDataMapper to map the polygonal data
    # into graphics primitives. We connect the output of the cone source 
    # to the input of this mapper.
  
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection( coneSource.GetOutputPort() )

    # We create an actor to represent the cone. The actor orchestrates rendering
    # of the mapper's graphics primitives. An actor also refers to properties
    # via a vtkProperty instance, and includes an internal transformation
    # matrix. We set this actor's mapper to be coneMapper which we created
    # above.
  
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(0.2, 0.63, 0.79)
    coneActor.GetProperty().SetDiffuse(0.7)
    coneActor.GetProperty().SetSpecular(0.4)
    coneActor.GetProperty().SetSpecularPower(20)
    coneActor.GetProperty().SetOpacity(0.5)

    #Create a property and directly manipulate it. Assign it to the second actor.

    property = vtkProperty()
    property.SetColor(1.0, 0.3882, 0.2784)
    property.SetDiffuse(0.7)
    property.SetSpecular(0.4)
    property.SetSpecularPower(20)
    property.SetOpacity(0.5)

    # Create a second actor and a property. The property is directly
    # manipulated and then assigned to the actor. In this way, a single
    # property can be shared among many actors. Note also that we use the
    # same mapper as the first actor did. This way we avoid duplicating
    # geometry, which may save lots of memory if the geoemtry is large.
    coneActor2 = vtkActor()
    coneActor2.SetMapper(coneMapper)
    coneActor2.SetPosition(0, 2, 0)
    coneActor2.SetProperty(property)

    return coneActor, coneActor2


def main():

    # Create the cone and assign it to the renderer
    coneActor_p1 = render_cone_p1()
    coneActor, coneActor2 = render_cones()

    # Create the Renderer and assign actors to it. A renderer is like a
    # viewport. It is part or all of a window on the screen and it is
    # responsible for drawing the actors it has.  We also set the background
    # color here.
    ren = vtkRenderer()
    ren.AddActor( coneActor )
    ren.AddActor( coneActor2 )
    ren.SetBackground(0.1, 0.2, 0.4 )
    ren.SetViewport(0, 0, 0.5, 1)

    ren2 = vtkRenderer()
    ren2.AddActor( coneActor_p1 )
    ren2.SetBackground(0.2, 0.3, 0.4)
    ren2.SetViewport(0.5, 0, 1, 1)
    ren2.GetActiveCamera().Azimuth(90)
    ren2.GetActiveCamera().SetPosition(10, 0, 0)

    ################################################################
    # Here is where we setup the observer, we do a new and ren1 
    mo1 = vtkMyCallback(ren2)
    ren2.AddObserver(vtkCommand.EndEvent,mo1)
    ################################################################
    
    # Finally we create the render window which will show up on the screen.
    # We put our renderer into the render window using AddRenderer. We also
    # set the size to be 300 pixels by 300.
    
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.AddRenderer(ren2)

    renWin.SetSize(600, 300)
    renWin.SetWindowName('Cone')

    
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


if __name__ == '__main__':
    main()