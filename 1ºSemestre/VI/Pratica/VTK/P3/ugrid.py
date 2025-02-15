from vtkmodules.all import *

def main():

    # Coordinates for the vertices
    coords = [[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 1]]
    
    #################################
    # VTKUnstructuredGrid Definition
    Ugrid = vtkUnstructuredGrid()
    points = vtkPoints()
    
    # Insert points into vtkPoints
    for i, coord in enumerate(coords):
        points.InsertPoint(i, coord)
    
    # Create cells as VTK_VERTEX
    for i in range(len(coords)):  # Create one cell for each vertex
        Ugrid.InsertNextCell(VTK_VERTEX, 1, [i])
    
    # Assign points to the unstructured grid
    Ugrid.SetPoints(points)
    
    # Mapper and actor
    UGridMapper = vtkDataSetMapper()
    UGridMapper.SetInputData(Ugrid)

    UGridActor = vtkActor()
    UGridActor.SetMapper(UGridMapper)

    # Modify actor properties
    UGridActor.GetProperty().SetColor(1, 0, 0)  # Red color
    UGridActor.GetProperty().SetPointSize(5)    # Set point size

    # Creation of renderer, render window, and interactor
    ren1 = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetWindowName("U N S T R U C T U R E D   G R I D")

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add actor to the renderer and set background color
    ren1.AddActor(UGridActor)
    ren1.SetBackground(0.8, 0.8, 0.8)  # Light gray background

    # Render and start interaction
    renWin.Render()
    iren.Start()

if __name__ == '__main__':
    main()