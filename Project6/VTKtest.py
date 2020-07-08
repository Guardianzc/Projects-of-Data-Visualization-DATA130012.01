import vtk
import os
import sys
import nibabel as nib


def volumeRender():
    # Create the standard renderer, render window and interactor.
    ren1 = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create the reader for the data.
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName('./image/ironProt.vtk')

    # Create transfer mapping scalar value to opacity.
    volumeOpacity = vtk.vtkPiecewiseFunction()
    volumeOpacity.AddPoint(50, 0)
    volumeOpacity.AddPoint(150, 0.4)
    volumeOpacity.AddPoint(200, 0.7)
    volumeOpacity.AddPoint(255, 1)

    # Create transfer mapping scalar value to color.
    volumeColor = vtk.vtkColorTransferFunction()

    volumeColor.AddRGBPoint(0.0, 25.0, 25.0, 25.0)
    volumeColor.AddRGBPoint(64.0, 100.0, 100.0, 100.0)
    volumeColor.AddRGBPoint(128.0, 150.0, 150.0, 150.0)
    volumeColor.AddRGBPoint(192.0, 200.0, 200.0, 200.0)
    # The property describes how the data will look.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeOpacity)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    # The mapper / ray cast function know how to render the data.
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    colors = vtk.vtkNamedColors()

    ren1.AddVolume(volume)
    ren1.SetBackground(colors.GetColor3d("White"))
    ren1.GetActiveCamera().Azimuth(0)
    ren1.GetActiveCamera().Elevation(15)
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()

    renWin.SetSize(600, 600)
    renWin.Render()

    iren.Start()

def isosurfaceRendering():
    # source->filter(MC算法)->mapper->actor->render->renderwindow->interactor   
    # load the nii data
    img1 = nib.load('./image/image_lr.nii.gz')
    img1_data = img1.get_data()
    dims = img1.shape
    spacing = (img1.header['pixdim'][1], img1.header['pixdim'][2], img1.header['pixdim'][3])
    image = vtk.vtkImageData()
    image.SetDimensions( dims[0], dims[1], dims[2])
    image.SetOrigin(0,0,0)

    if vtk.VTK_MAJOR_VERSION <= 5:
       image.SetNumberOfScalarComponents(1)
       image.SetScalarTypeToDouble()
    else:
       image.AllocateScalars(vtk.VTK_DOUBLE, 1)
    
    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                scalardata = img1_data[x][y][z]
                image.SetScalarComponentFromDouble(x, y, z, 0, scalardata)

    # filter -- Marching Cubes
    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(image)
    Extractor.SetValue(0, 150)
    # Smoothing (can be remove)
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(Extractor.GetOutputPort())
    smoother.SetNumberOfIterations(500)
    
    # filter -- remove the old unit
    Stripper = vtk.vtkStripper()
    #Stripper.SetInputConnection(Extractor.GetOutputPort())
    Stripper.SetInputConnection(smoother.GetOutputPort())

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(Stripper.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # set the color
    actor.GetProperty().SetDiffuseColor(1, 1, 0)
    actor.GetProperty().SetOpacity(0.8)
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)
    mapper.ScalarVisibilityOff()

    # define the render
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)
    renderer.AddActor(actor)

    # define the renderwindow
    rewin = vtk.vtkRenderWindow()
    
        
    # show the data
    rewin.AddRenderer(renderer)
    rewin.SetSize(250, 250)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(rewin)
    interactor.Initialize()
    rewin.Render()
    interactor.Start()

if __name__ == '__main__':
    os.chdir(sys.path[0])
    volumeRender()
    isosurfaceRendering()