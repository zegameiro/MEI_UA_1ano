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
    # Glyph Representation
    cone_source = vtkConeSource()
    cone_source.SetHeight(0.4)
    cone_source.SetRadius(0.2)
    cone_source.SetResolution(5)

    glyph = vtkGlyph3D()
    glyph.SetSourceConnection(cone_source.GetOutputPort())
    glyph.SetInputData(ugrid)
    glyph.SetVectorModeToUseVector() # Orient cones by the vector data
    glyph.SetScaleFactor(0.5) # Set the overall scaling factor for glyphs

    glyph_mapper = vtkPolyDataMapper()
    glyph_mapper.SetInputConnection(glyph.GetOutputPort())

    glyph_mapper.SetScalarRange(0.1, 0.8)

    glyph_actor = vtkActor()
    glyph_actor.SetMapper(glyph_mapper)

    #################################
    # Renderer setup
    renderer = vtkRenderer()
    renderer.SetBackground(0.8, 0.8, 0.8)
    renderer.AddActor(glyph_actor)

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(600, 600)
    render_window.SetWindowName("S C A L A R   A S S O C I A T I O N S   &   V E C T O R S   O N   G R I D S")

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(render_window)

    #################################
    # Render and interaction
    render_window.Render()
    iren.Start()

if __name__ == '__main__':
    main()