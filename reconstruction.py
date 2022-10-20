# %%
import vtk

# %%
# dicom_dir = '../Database/2EFVJVCN-Osso' #path to dcom image folder
#dicom_dir = '../Database/CQ500-CT-412/CQ500CT412 CQ500CT412/Unknown Study/CT 0.625mm/'
#dicom_dir = '../Database/2EFVJVCN-HighIntensity-FFA-d2-q1'
dicom_dir = '../Database/2EFVJVCN-Temp'
#dicom_dir = '../Database/2EFVJVCN'


# %%
if dicom_dir == '../Database/2EFVJVCN':
    iso_value = 200
else:
    iso_value = 0

# %%
'''
A class holding colors and their names. 
'''
colors = vtk.vtkNamedColors()

if iso_value is None and dicom_dir is not None:
    print('An ISO value is needed.')

volume = vtk.vtkImageData()
if dicom_dir is None:
    pass

else:
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_dir)
    reader.Update()
    volume.DeepCopy(reader.GetOutput())

surface = vtk.vtkMarchingCubes()
surface.SetInputData(volume)
surface.ComputeNormalsOn()
surface.SetValue(0, iso_value)

renderer = vtk.vtkRenderer()
renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName('MarchingCubes')

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

renderer.AddActor(actor)

render_window.Render()
interactor.Start()
