from vtkmodules.all import *

def render_cube_face(textureFile, rotation, translation):
    planeSource = vtkPlaneSource()
    planeSource.SetCenter(0, 0, 0)
    planeSource.SetResolution(100, 100)

    # Apply the rotation and translation
    transform = vtkTransform()
    transform.RotateWXYZ(rotation[0], rotation[1], rotation[2], rotation[3])
    transform.Translate(translation)
    
    filter = vtkTransformPolyDataFilter()
    filter.SetTransform(transform)
    filter.SetInputConnection(planeSource.GetOutputPort())

    planeMapper = vtkPolyDataMapper()
    planeMapper.SetInputConnection(filter.GetOutputPort())

    # Apply the texture
    jpegReader = vtkJPEGReader()
    jpegReader.SetFileName(textureFile)
    jpegReader.Update()

    texture = vtkTexture()
    texture.SetInputConnection(jpegReader.GetOutputPort())

    # Apply everything to the actor
    planeActor = vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetTexture(texture)

    return planeActor

def main():
    # Create the cube faces
    # ROTATION: [angle, x, y, z]
    # TRANSLATION: [x, y, z]
    face1 = render_cube_face("./images/Im1.jpg", [90, 0, 1, 0], [0, 0, 0.5])
    face2 = render_cube_face("./images/Im2.jpg", [90, 0, 1, 0], [0, 0, -0.5])
    face3 = render_cube_face("./images/Im3.jpg", [0, 0, 0, 1], [0, 0, 0.5])
    face4 = render_cube_face("./images/Im4.jpg", [90, 0, 0, 1], [0, 0, -0.5])
    face5 = render_cube_face("./images/Im5.jpg", [90, 1, 0, 0], [0, 0, 0.5])
    face6 = render_cube_face("./images/Im6.jpg", [90, 1 , 0, 0], [0,0 , -0.5])

    # Create the renderer
    ren = vtkRenderer()
    ren.AddActor(face1)
    ren.AddActor(face2)
    ren.AddActor(face3)
    ren.AddActor(face4)
    ren.AddActor(face5)
    ren.AddActor(face6)

    ren.SetBackground(0.1, 0.2, 0.3)

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(600, 600)
    renWin.SetWindowName("T E X T U R E S")

    # Adds a render window interactor to the cone example to
    # enable user interaction (e.g. to rotate the scene)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()