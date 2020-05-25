# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:26:54 2017

@author: broche
"""

import numpy as np
import vtk
from PyMca import PyMcaQt as qt
from time import gmtime, strftime


class VTK_Render_QT(qt.QFrame):
    def __init__(self, parent = None):
        qt.QFrame.__init__(self, parent)
        self.v1 = qt.QVBoxLayout()
        self.renWin =  vtk.vtkRenderWindow()

    @staticmethod
    def exitCheck(obj, event):

        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    @staticmethod
    def image_float_to_int8(vol,minValue,maxValue):
        """
        Format the volume to a 0-255 image uint16
        """

        vol = (255 * (vol - minValue)) / (maxValue - minValue)
        vol = vol.astype(np.uint8)
        vol[vol < 0 ] = 0
        vol[vol > 255 ] = 255

        return vol


    def MarchingCube(self,thresholdValue):

        thresholdValue = float((255.0 * (thresholdValue - self.minValue)) / (self.maxValue - self.minValue))

        threshold = vtk.vtkImageThreshold()
        threshold.SetInputConnection(self.data_importer.GetOutputPort())
        threshold.ThresholdByLower(thresholdValue)  # remove all soft tissue
        threshold.ReplaceInOn()
        threshold.SetInValue(0)  # set all values below 400 to 0
        threshold.ReplaceOutOn()
        threshold.SetOutValue(1)  # set all values above 400 to 1
        threshold.Update()

        self.dmc = vtk.vtkDiscreteMarchingCubes()
        self.dmc.SetInputConnection(threshold.GetOutputPort())
        self.dmc.GenerateValues(1, 1, 1)
        self.dmc.Update()

        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName('./Data/' + strftime("%Y-%m-%d %H:%M:%S", gmtime())+'.stl')
        stlWriter.SetInputConnection(self.dmc.GetOutputPort())
        stlWriter.SetFileTypeToBinary()
        stlWriter.Write()

    def SmoothMesh(self,nbIter,RelaxFactor):

        smoother =  vtk.vtkSmoothPolyDataFilter()
        smoother.SetInputConnection(self.dmc.GetOutputPort())
        smoother.SetNumberOfIterations(nbIter)
        smoother.SetRelaxationFactor(RelaxFactor)#this has little effect on the error!
        self.dmc = vtk.vtkPolyDataNormals()
        self.dmc.SetInputConnection(smoother.GetOutputPort())
        stlWriter = vtk.vtkSTLWriter()

        stlWriter.SetFileName('./Data/' + strftime("%Y-%m-%d %H:%M:%S", gmtime())+'.stl')
        stlWriter.SetFileTypeToBinary()
        stlWriter.SetInputConnection(self.dmc.GetOutputPort())
        stlWriter.Write()

    def init_all_VolumeRendering_component(self, flagMesh):
        self.flagMesh = flagMesh
        self.ren= vtk.vtkRenderer()
        self.renWin.AddRenderer(self.ren)
        self.iren = vtk.vtkXRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)

        self.ren.GetVolumes()

        self.alpha_channel_function = vtk.vtkPiecewiseFunction()
        self.alpha_channel_function.AddPoint(0, 0.0, 0.5, 0.0)
        self.alpha_channel_function.AddPoint(255, 1, 0.5, 0.0)

        self.color_function = vtk.vtkColorTransferFunction()
        self.color_function.AddRGBPoint(0, 0, 0.0, 0.0, 0.5, 0.0)
        self.color_function.AddRGBPoint(255, 1, 1, 1, 0.5, 0.0)

        self.volume_property = vtk.vtkVolumeProperty()
        self.volume_property.SetColor(self.color_function)
        self.volume_property.SetScalarOpacity(self.alpha_channel_function)

        self.data_importer = vtk.vtkImageImport()

        if self.flagMesh :
            self.volume_mapper = vtk.vtkPolyDataMapper()
        else:
            self.volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()

        self.volume = vtk.vtkVolume()

    def import_numpy_array(self, np_array,minValue,maxValue):

        self.minValue = minValue
        self.maxValue = maxValue
        np_array = self.image_float_to_int8(np_array, minValue,maxValue)

        self.shape_data = np_array.shape
        self.data_importer.CopyImportVoidPointer(np_array, np_array.nbytes)
        self.data_importer.SetDataScalarTypeToUnsignedChar()
        self.data_importer.SetNumberOfScalarComponents(1)
        self.data_importer.SetDataExtent(0, self.shape_data[2] - 1, 0, self.shape_data[1] - 1, 0, self.shape_data[0] - 1)
        self.data_importer.SetWholeExtent(0, self.shape_data[2] - 1, 0, self.shape_data[1] - 1, 0, self.shape_data[0] - 1)

    def reset_alpha_channel(self):
        self.alpha_channel_function.RemoveAllPoints()

    def reset_color_channel(self):
        self.color_function.RemoveAllPoints()

    def set_color_channel(self, value, R, G, B, mid = 0.5, sharp = 0.0):
        self.color_function.AddRGBPoint(value*255, R, G, B,mid, sharp)

    def set_alpha_channel(self,value,alpha, mid = 0.5, sharp = 0.0):
        self.alpha_channel_function.AddPoint(value*255, alpha,mid, sharp)

    def set_volume_property(self, shade=True, ambient=0.1, diffuse=0.9, specular=0.2, specular_pw=10.0,
            opacity_unit_dist=0.8919):

        self.volume_property.SetColor(self.color_function)
        self.volume_property.SetScalarOpacity(self.alpha_channel_function)

        if shade:
            self.volume_property.ShadeOn()
        else:
            self.volume_property.ShadeOff()

        self.volume_property.SetAmbient(ambient)
        self.volume_property.SetDiffuse(diffuse)
        self.volume_property.SetSpecular(specular)
        self.volume_property.SetSpecularPower(specular_pw)
        self.volume_property.SetScalarOpacityUnitDistance(opacity_unit_dist)

    def update_mapper(self, blend_mode='Composite'):


        if not self.flagMesh:
            if blend_mode == 'Composite':
                self.volume_mapper.SetBlendModeToComposite()
            elif blend_mode == 'MaxIntensity':
                self.volume_mapper.SetBlendModeToMaximumIntensity()

        self.volume_mapper.RemoveAllInputs()

        if self.flagMesh:
            self.volume_mapper.SetInputConnection(self.dmc.GetOutputPort())
        else:
            self.volume_mapper.SetInputConnection(self.data_importer.GetOutputPort())
            self.volume_mapper.AutoAdjustSampleDistancesOn()
            self.volume_mapper.IntermixIntersectingGeometryOn()
            self.volume.SetMapper(self.volume_mapper)
            self.volume.SetProperty(self.volume_property)


    def add_PolyActor(self):

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.volume_mapper)
        self.ren.AddActor(self.actor)


    def add_volume_to_renderer(self):
        self.ren.AddVolume(self.volume)


    def update_renderer(self, background=[255.0, 255.0, 255.0], sizeW = [1600,1200]):
        self.ren.SetBackground(1,1,1)
        self.renWin.SetSize(sizeW[0],sizeW[1])
        self.renWin.AddObserver("AbortCheckEvent", self.exitCheck)

    def launch_render(self):
        self.setLayout(self.v1)
        self.iren.SetDesiredUpdateRate(25)
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()
        self.close_window()
        del self.renWin, self.iren

    def close_window(self):
        self.renWin.Finalize()
        self.iren.TerminateApp()



    def take_screen_shot(self, file_name):


        WindowToImageFilter = vtk.vtkWindowToImageFilter()

        WindowToImageFilter.SetInput( self.renWin)
        TIFFWriter = vtk.vtkTIFFWriter()
        TIFFWriter.SetInputConnection(WindowToImageFilter.GetOutputPort())
        self.renWin.SetSize(1600, 1200)
        self.ren.Modified()
        self.renWin.Modified()
        self.renWin.Render()
        TIFFWriter.SetFileName(file_name)
        WindowToImageFilter.Modified()
        WindowToImageFilter.Update()

        TIFFWriter.Write()


    def  take_multi_rotation_screen_shot(self, path, angleRot):
        WindowToImageFilter = vtk.vtkWindowToImageFilter()

        WindowToImageFilter.SetInput(self.renWin)
        TIFFWriter = vtk.vtkTIFFWriter()
        TIFFWriter.SetInputConnection(WindowToImageFilter.GetOutputPort())

        self.ren.GetActiveCamera().SetFocalPoint(self.shape_data[2]/2.0,self.shape_data[1]/2.0,1.3*self.shape_data[0])
        self.ren.GetActiveCamera().Elevation(80)
        self.ren.GetActiveCamera().Roll(180)
        self.ren.GetActiveCamera().Zoom(0.7)

        self.renderer.AddActor(self.actor)
        for i in range(0,angleRot):

            WindowToImageFilter.Modified()
            WindowToImageFilter.Update()

            TIFFWriter.SetFileName(path +'%4.4d'%i+'.tiff')
            TIFFWriter.Write()
            self.ren.GetActiveCamera().Azimuth(1)
        self.ren.RemoveVolume(self.volume)
        self.ren.RemoveActor(self.actor)

    def add_arrow_field(self, arrow=[], shaft_reso=24, tip_reso=36):
        if arrow != []:
            for p in range(0,int(len(arrow[:, 0])),4):


                arrow_source = vtk.vtkArrowSource()
                arrow_source.SetShaftResolution(shaft_reso)
                arrow_source.SetTipResolution(tip_reso)

                start_point = [0 for i in range(3)]
                start_point[0] = arrow[p, 2]
                start_point[1] = arrow[p, 1]
                start_point[2] = arrow[p, 0]

                end_point = [0 for i in range(3)]
                end_point[0] = arrow[p, 5]
                end_point[1] = arrow[p, 4]
                end_point[2] = arrow[p, 3]

                normalized_x = [0 for i in range(3)]
                normalized_y = [0 for i in range(3)]
                normalized_z = [0 for i in range(3)]
                normalized_x[0] = end_point[0] - start_point[0]
                normalized_x[1] = end_point[1] - start_point[1]
                normalized_x[2] = end_point[2] - start_point[2]

                # The X axis is a vector from start to end
                math = vtk.vtkMath()
                length = math.Norm(normalized_x)
                if length != 0:
                    math.Normalize(normalized_x)

                    # The Z axis is an arbitrary vector cross X
                    arbitrary = [0 for i in range(3)]
                    arbitrary[0] = 2048
                    arbitrary[1] = 2048
                    arbitrary[2] = 2048
                    math.Cross(normalized_x, arbitrary, normalized_z)
                    math.Normalize(normalized_z)

                    # The Y axis is Z cross X
                    math.Cross(normalized_z, normalized_x, normalized_y)
                    matrix = vtk.vtkMatrix4x4()

                    # Create the direction cosi1, 1, 1ne matrix
                    matrix.Identity()
                    for i in range(3):
                        matrix.SetElement(i, 0, normalized_x[i])
                        matrix.SetElement(i, 1, normalized_y[i])
                        matrix.SetElement(i, 2, normalized_z[i])

                    # Apply the transforms
                    transform = vtk.vtkTransform()
                    transform.Translate(start_point)
                    transform.Concatenate(matrix)
                    transform.Scale(length, length, length)

                    # Transform the polydata
                    transformPD = vtk.vtkTransformPolyDataFilter()
                    transformPD.SetTransform(transform)
                    transformPD.SetInputConnection(arrow_source.GetOutputPort())

                    #Create a mapper and actor for the arrow
                    self.mapper = vtk.vtkPolyDataMapper()
                    self.actor = vtk.vtkActor()

                    arrow_source.SetTipLength(3.0/length)
                    arrow_source.SetTipRadius(1.0/length)
                    arrow_source.SetShaftRadius(0.5/length)

                    self.mapper.SetInputConnection(arrow_source.GetOutputPort())
                    self.actor.SetUserMatrix(transform.GetMatrix())
                    self.actor.GetProperty().SetColor(1,0,0)
                    self.actor.SetMapper(self.mapper)
                    self.ren.AddActor(self.actor)