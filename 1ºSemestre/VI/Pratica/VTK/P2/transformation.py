from vtkmodules.all import *

def render_plane():
    plane = vtkPlaneSource()
  	
    # Definition of the transformation (a translation)
    MyTransform = vtkTransform()
    MyTransform.Translate(0,0,-1)

    # Filter definition
    MyFilter = vtkTransformPolyDataFilter()

    # Tranform end vtkPolydata input to the filter
    MyFilter.SetTransform(MyTransform)
    MyFilter.SetInputData(plane.GetOutput())

    planeMapper = vtkPolyDataMapper()
    planeMapper.SetInputConnection(MyFilter.GetOutputPort())

    planeActor = vtkActor()
    planeActor.SetMapper( planeMapper )

    return planeActor

def main():
    planeActor = render_plane()

    ren = vtkRenderer()
    ren.AddActor(planeActor)
    ren.SetBackground(0.1, 0.2, 0.3)

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(600, 600)
    renWin.SetWindowName("T R A N S F O R M A T I O N S")

    # Adds a render window interactor to the cone example to
    # enable user interaction (e.g. to rotate the scene)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()