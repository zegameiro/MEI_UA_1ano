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
    sphereSource.SetPhiResolution(30)
    sphereSource.SetThetaResolution(30)

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
    renderWindow.SetWindowName("G L Y P H I N G")

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    renderWindow.Render()
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()




