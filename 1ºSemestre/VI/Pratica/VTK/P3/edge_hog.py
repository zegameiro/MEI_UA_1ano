from vtkmodules.all import *

def main():

    # Coordinates for the vertices
    coords = [[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 1]]

    # Vectors associated with each vertex
    vectors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]

    # Scalars associated with each vertex
    scalars = [0.1, 0.3, 0.5, 0.8]

    ugrid = vtkUnstructuredGrid()
    points = vtkPoints()

    # Insert points into vtkPoints
    for i, coord in enumerate(coords):
        points.InsertPoint(i, coord)

    # Create cells as VTK_VERTEX
    for i in range(len(coords)):  # Create one cell for each vertex
        ugrid.InsertNextCell(VTK_VERTEX, 1, [i])

    # Assign points to the unstructured grid
    ugrid.SetPoints(points)

    # Create vtkFloatArray for vectors
    vecData = vtkFloatArray()
    vecData.SetNumberOfComponents(3)
    vecData.SetName("Vectors")

    # Add vectors to the vtkFloatArray
    for vec in vectors:
        vecData.InsertNextTuple3(*vec)

    # Associate the vectors with the points
    ugrid.GetPointData().SetVectors(vecData)

    # Create vtkFloatArray for scalars
    scalarData = vtkFloatArray()
    scalarData.SetNumberOfComponents(1)
    scalarData.SetName("Scalars")

    # Add scalars to the vtkFloatArray
    for scalar in scalars:
        scalarData.InsertNextValue(scalar)

    # Associate the scalars with the points
    ugrid.GetPointData().SetScalars(scalarData)

    #################################
    # Hedgehog Representation
    hedgehog = vtkHedgeHog()
    hedgehog.SetInputData(ugrid)
    hedgehog.SetScaleFactor(0.3)

    # Create a mapper for HedgeHog
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(hedgehog.GetOutputPort())

    # Set scalar range for coloring the line segments
    mapper.SetScalarRange(0.1, 0.8)

    hedgehog_actor = vtkActor()
    hedgehog_actor.SetMapper(mapper)

    #################################
    # Renderer setup
    renderer = vtkRenderer()
    renderer.SetBackground(0.8, 0.8, 0.8)
    renderer.AddActor(hedgehog_actor)

    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName("V E C T O R S  W I T H  H E D G E H O G")

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    #################################
    # Start the interaction
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()