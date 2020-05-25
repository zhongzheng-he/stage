# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 10:14:27 2016

@author: broche
"""

import SimpleITK as sitk
import numpy as np


def imageFromNumpyToITK(vol):
    return sitk.GetImageFromArray(vol)

def imageFromITKToNumpy(vol):
    return sitk.GetArrayFromImage(vol)



class Registering():


    def __init__(self, dicPar,ImageStack):

        self.dicPar = dicPar

        self.ImageStack = ImageStack

        self.ImageFixe = []
        self.ImageMoving = []
        self.MaskFixe = []
        self.MaskMoving = []

        """Init registering object """
        self.reg_method = sitk.ImageRegistrationMethod()
        """Init Metric """
        self.initMetric()
        """Optimizer"""
        self.initOptimizer()
        """Interpolator"""
        self.initInterpolator()
        """ Scaling """
        self.initScaling()

        """ Set Inputs"""
        self.setImages()
        self.initIntitialTransform()

    def setImages(self):

        indexFI = int(self.dicPar['Inputs']['FI'])
        indexMI = int(self.dicPar['Inputs']['MI'])
        indexFIM = int(self.dicPar['Inputs']['FIM'])
        indexMIM = int(self.dicPar['Inputs']['MIM'])

        indexIFIT = int(self.dicPar['Inputs']['IFIT'])
        indexIMIT = int(self.dicPar['Inputs']['IMIT'])

        self.ImageFixe = imageFromNumpyToITK(self.ImageStack[indexFI])
        self.ImageMoving = imageFromNumpyToITK(self.ImageStack[indexMI])

        if (indexIFIT  !=0) and (indexIMIT  != 0):
            self.ImageInitFixe = imageFromNumpyToITK(self.ImageStack[indexIFIT-1])
            self.ImageInitMoving =  imageFromNumpyToITK(self.ImageStack[indexIMIT-1])

        if (indexFIM !=0) and (indexMIM  != 0):
            self.MF = imageFromNumpyToITK(self.ImageStack[indexFIM-1])
            self.MM = imageFromNumpyToITK(self.ImageStack[indexMIM-1])


    def initIntitialTransform(self):
        if self.dicPar['Inputs']['InitT'] != "None":
            if self.dicPar['Inputs']['InitT'] == "Geometry":
                self.init_t = sitk.CenteredTransformInitializer(self.ImageInitFixe, self.ImageInitMoving , sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY)
            elif self.dicPar['Inputs']['InitT'] == "Moments" :
                self.init_t = sitk.CenteredTransformInitializer(self.ImageInitFixe, self.ImageInitMoving , sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.MOMENTS)

            self.ImageMoving = sitk.Resample(self.ImageMoving, self.ImageFixe ,self.init_t, self.interpolator, 0.0, self.ImageMoving.GetPixelIDValue())

            if (int(self.dicPar['Inputs']['MIM'])  != 0)  and (int(self.dicPar['Inputs']['FIM']) ==0):
                self.MM = sitk.Resample(self.MM, self.ImageFixe , self.init_t, self.interpolator, 0.0,self.MM.GetPixelIDValue())

        if ( int(self.dicPar['Inputs']['FIM']) !=0) and ( int(self.dicPar['Inputs']['MIM'])  != 0):
            self.reg_method.SetMetricFixedMask(self.MF)
            self.reg_method.SetMetricMovingMask(self.MM)

        x_grid_size = self.dicPar['Grid'][0]
        y_grid_size = self.dicPar['Grid'][0]
        z_grid_size = self.dicPar['Grid'][0]

        grid_physical_spacing = [x_grid_size, y_grid_size, z_grid_size]
        image_physical_size = [size*spacing for size,spacing in zip(self.ImageFixe.GetSize(), self.ImageFixe.GetSpacing())]
        mesh_size = [int(image_size/grid_spacing + 0.5) for image_size,grid_spacing in zip(image_physical_size,grid_physical_spacing)]
        self.initial_transform = sitk.BSplineTransformInitializer(image1 = self.ImageFixe, transformDomainMeshSize = mesh_size, order=3)
        self.reg_method.SetInitialTransform(self.initial_transform)

    def initMetric(self):

        """ Metric """
        if self.dicPar['Metric']['Method'] ==  "Means Squares":
            self.reg_method.SetMetricAsMeanSquares()

        elif self.dicPar['Metric']['Method'] ==  "Correlation":
            self.reg_method.SetMetricAsCorrelation()

        elif self.dicPar['Metric']['Method'] ==  "Demons":
            par1 = float(self.dicPar['Metric']['Par'][0])
            self.reg_method.SetMetricAsDemons(par1)

        elif self.dicPar['Metric']['Method'] ==  "Joint Histogram Mutual Information":
            par1 = int(self.dicPar['Metric']['Par'][0])
            par2 = float(self.dicPar['Metric']['Par'][1])
            self.reg_method.SetMetricAsJointHistogramMutualInformation(par1,par2)

        elif self.dicPar['Metric']['Method'] ==  "Mattes Mutual Information":
            par1 = int(self.dicPar['Metric']['Par'][0])
            self.reg_method.SetMetricAsMattesMutualInformation(par1)
        elif self.dicPar['Metric']['Method'] == "Neighborhood Correlation (ANTs)":
            par1 = int(self.dicPar['Metric']['Par'][0])
            self.reg_method.SetMetricAsANTSNeighborhoodCorrelation (par1)

        if     self.dicPar['Metric']['Sampling']['Method'] != 'None':

            if self.dicPar['Metric']['Sampling']['Method'] != 'Random':
                self.reg_method.SetMetricSamplingStrategy(self.reg_method.RANDOM)
            if self.dicPar['Metric']['Sampling']['Method'] != 'Regular':
                self.reg_method.SetMetricSamplingStrategy(self.reg_method.REGULAR)
            perc = float(self.dicPar['Metric']['Sampling']['Percentage'])
            self.reg_method.SetMetricSamplingPercentage(perc)

        flag_grad_fx_I = int(self.dicPar['Metric']['GradF'])
        flag_grad_mv_I = int(self.dicPar['Metric']['GradM'])

        self.reg_method.SetMetricUseFixedImageGradientFilter(bool(flag_grad_fx_I) )
        self.reg_method.SetMetricUseMovingImageGradientFilter(bool(flag_grad_mv_I))

    def initOptimizer(self):
        """ Optimizer """

        if self.dicPar['Optimizer']['Method'] == "Regular Step Gradient Descent":

            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = float(self.dicPar['Optimizer']['Par'][1])
            par3 = int(self.dicPar['Optimizer']['Par'][2])
            par4 = float(self.dicPar['Optimizer']['Par'][3])
            par5 = float(self.dicPar['Optimizer']['Par'][4])

            if int(self.dicPar['Optimizer']['Par'][5]) == 0 :
                par6 = self.reg_method.Never
            elif int(self.dicPar['Optimizer']['Par'][5]) == 1 :
                par6 = self.reg_method.Once
            elif int(self.dicPar['Optimizer']['Par'][5]) == 2 :
                par6 = self.reg_method.EachIteration

            par7 = float(self.dicPar['Optimizer']['Par'][6])

            self.reg_method.SetOptimizerAsRegularStepGradientDescent(par1,par2, par3, par4, par5, par6, par7)

        elif self.dicPar['Optimizer']['Method'] == "Gradient Descent":

            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = float(self.dicPar['Optimizer']['Par'][2])
            par4 = int(self.dicPar['Optimizer']['Par'][3])

            if int(self.dicPar['Optimizer']['Par'][4]) == 0 :
                par5 = self.reg_method.Never
            elif int(self.dicPar['Optimizer']['Par'][4]) == 1 :
                par5 = self.reg_method.Once
            elif int(self.dicPar['Optimizer']['Par'][4]) == 2 :
                par5 = self.reg_method.EachIteration

            par6 = int(self.dicPar['Optimizer']['Par'][5])
            self.reg_method.SetOptimizerAsGradientDescent(par1,par2, par3, par4, par5, par6)

        elif self.dicPar['Optimizer']['Method'] == "Gradient Descent Line Search":

            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = float(self.dicPar['Optimizer']['Par'][2])
            par4 = int(self.dicPar['Optimizer']['Par'][3])
            par5 =float(self.dicPar['Optimizer']['Par'][4])
            par6 =float(self.dicPar['Optimizer']['Par'][5])
            par7 = float(self.dicPar['Optimizer']['Par'][6])
            par8 = int(self.dicPar['Optimizer']['Par'][7])
            if int(self.dicPar['Optimizer']['Par'][8]) == 0 :
                par9 = self.reg_method.Never
            elif int(self.dicPar['Optimizer']['Par'][8]) == 1 :
                par9 = self.reg_method.Once
            elif int(self.dicPar['Optimizer']['Par'][8]) == 2 :
                par9 = self.reg_method.EachIteration

            par10 = int(self.dicPar['Optimizer']['Par'][9])

            self.reg_method.SetOptimizerAsGradientDescentLineSearch(par1,par2, par3, par4, par5, par6, par7,par8,par9,par10)

        elif self.dicPar['Optimizer']['Method'] == "Conjugate Gradient Line Search":

            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = float(self.dicPar['Optimizer']['Par'][2])
            par4 = int(self.dicPar['Optimizer']['Par'][3])
            par5 =float(self.dicPar['Optimizer']['Par'][4])
            par6 =float(self.dicPar['Optimizer']['Par'][5])
            par7 = float(self.dicPar['Optimizer']['Par'][6])
            par8 = int(self.dicPar['Optimizer']['Par'][7])
            if int(self.dicPar['Optimizer']['Par'][8]) == 0 :
                par9 = self.reg_method.Never
            elif int(self.dicPar['Optimizer']['Par'][8]) == 1 :
                par9 = self.reg_method.Once
            elif int(self.dicPar['Optimizer']['Par'][8]) == 2 :
                par9 = self.reg_method.EachIteration

            par10 = int(self.dicPar['Optimizer']['Par'][9])
            self.reg_method.SetOptimizerAsConjugateGradientLineSearch(par1,par2, par3, par4, par5, par6, par7,par8,par9,par10)

        elif self.dicPar['Optimizer']['Method'] == "Exhaustive":
            par1 = int(self.dicPar['Optimizer']['Par'][1])
            par2 = int(self.dicPar['Optimizer']['Par'][2])
            par3 = int(self.dicPar['Optimizer']['Par'][3])
            par4 = int(self.dicPar['Optimizer']['Par'][4])
            par5 =int(self.dicPar['Optimizer']['Par'][5])
            par6 =int(self.dicPar['Optimizer']['Par'][6])
            par13 = float(self.dicPar['Optimizer']['Par'][0])
            vect1 = [par1,par2,par3,par4,par5,par6]

            self.reg_method.SetOptimizerAsExhaustive(vect1,par13)

        elif self.dicPar['Optimizer']['Method'] == "LBFGSB":
            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = int(self.dicPar['Optimizer']['Par'][2])
            par4 = int(self.dicPar['Optimizer']['Par'][3])
            par5 = float(self.dicPar['Optimizer']['Par'][4])

            self.reg_method.SetOptimizerAsLBFGSB(par1, par2, par3, par4, par5)
        elif self.dicPar['Optimizer']['Method'] == "Powell":
            par1 = int(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = float(self.dicPar['Optimizer']['Par'][2])
            par4 = float(self.dicPar['Optimizer']['Par'][3])
            par5 = float(self.dicPar['Optimizer']['Par'][4])
            self.reg_method.SetOptimizerAsPowell(par1, par2, par3, par4, par5)

        elif self.dicPar['Optimizer']['Method'] == "Amoeba":
            par1 = float(self.dicPar['Optimizer']['Par'][0])
            par2 = int(self.dicPar['Optimizer']['Par'][1])
            par3 = float(self.dicPar['Optimizer']['Par'][2])
            par4 = float(self.dicPar['Optimizer']['Par'][3])
            self.reg_method.SetOptimizerAsAmoeba(par1, par2, par3, par4)

        if self.dicPar['Optimizer']['Method'] != "Exhaustive" or self.dicPar['Optimizer']['Method'] != "LBFGSB":

            if self.dicPar['Optimizer']['MethodScaling'] == "Physical Shift" :

                par1 = int(self.dicPar['Optimizer']['ScalePar'][0])
                par2 = float(self.dicPar['Optimizer']['ScalePar'][1])
                self.reg_method.SetOptimizerScalesFromPhysicalShift(par1,par2)

            elif self.dicPar['Optimizer']['MethodScaling'] == "Jacobian" :
                par1 = int(self.dicPar['Optimizer']['ScalePar'][0])
                self.reg_method.SetOptimizerScalesFromJacobian(par1)

            elif self.dicPar['Optimizer']['MethodScaling'] == "Index Shift" :

                par1 = int(self.dicPar['Optimizer']['ScalePar'][0])
                par2 = float(self.dicPar['Optimizer']['ScalePar'][1])
                self.reg_method.SetOptimizerScalesFromIndexShift(par1,par2)
        elif self.dicPar['Optimizer']['Method'] != "Exhaustive":

            par7 = float(self.dicPar['Optimizer']['Par'][7])
            par8 = float(self.dicPar['Optimizer']['Par'][8])
            par9 = float(self.dicPar['Optimizer']['Par'][9])
            par10 =float(self.dicPar['Optimizer']['Par'][10])
            par11 =float(self.dicPar['Optimizer']['Par'][11])
            par12 = float(self.dicPar['Optimizer']['Par'][12])

            vect2 = [par7,par8,par9,par10,par11,par12]

            self.reg_method.SetOptimizerScales(vect2)

    def initInterpolator(self):

        if self.dicPar['Interpolator'] == "Nearest neighbor":
            self.interpolator = sitk.sitkNearestNeighbor
        elif self.dicPar['Interpolator'] == "Linear Interpolation":
            self.interpolator = sitk.sitkLinear
        elif self.dicPar['Interpolator'] == "BSpline":
            self.interpolator = sitk.sitkBSpline
        elif self.dicPar['Interpolator'] == "Gaussian":
            self.interpolator = sitk.sitkGaussian
        elif self.dicPar['Interpolator'] == "Label Gaussian":
            self.interpolator = sitk.sitkLabelGaussian
        elif self.dicPar['Interpolator'] == "Hamming Windowed Sinc":
            self.interpolator = sitk.sitkHammingWindowedSinc
        elif self.dicPar['Interpolator'] == "Cosine Windowed Sinc":
            self.interpolator = sitk.sitkCosineWindowedSinc
        elif self.dicPar['Interpolator'] == "Welch Windowed Sinc":
            self.interpolator = sitk.sitkWelchWindowedSinc
        elif self.dicPar['Interpolator'] == "Lanczos Windowed Sinc":
            self.interpolator = sitk.sitkLanczosWindowedSinc
        elif self.dicPar['Interpolator'] == "Blackman Windowed Sinc":
            self.interpolator = sitk.sitkBlackmanWindowedSinc

        self.reg_method.SetInterpolator(self.interpolator)

    def initScaling(self):

        vect1 = []
        vect2 = []

        for i in range(0,len(self.dicPar['Scaling'])/2):
            parS = int(self.dicPar['Scaling'][i])
            parSm = int(self.dicPar['Scaling'][i+len(self.dicPar['Scaling'])/2])
            vect1.append(parS)
            vect2.append(parSm)

        self.reg_method.SetShrinkFactorsPerLevel(vect1)
        self.reg_method.SetSmoothingSigmasPerLevel(vect2)

        self.reg_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    def Execute(self):
        self.Final_Transform = self.reg_method.Execute(self.ImageFixe, self.ImageMoving)


    def ApplyTransform(self,ImageIn,FlagRigid):

        ImageITK = imageFromNumpyToITK(ImageIn)

        if FlagRigid:
            ImageITK = sitk.Resample(ImageITK,self.ImageFixe,self.init_t,self.interpolator,0.0,ImageITK.GetPixelIDValue())

        ImageOut = sitk.Resample(ImageITK,self.ImageFixe,self.Final_Transform,self.interpolator,0.0,ImageITK.GetPixelIDValue())


        return np.copy(imageFromITKToNumpy(ImageOut))


    def returnNumpyImage(self):
        self.ImageMovingBef =  imageFromITKToNumpy(self.ImageMoving)
        self.ImageFixedBef =  imageFromITKToNumpy(self.ImageFixe)
        self.ImageMoving = sitk.Resample(self.ImageMoving,self.ImageFixe,self.Final_Transform,self.interpolator,0.0,self.ImageMoving.GetPixelIDValue())
        ImageOut = imageFromITKToNumpy(self.ImageMoving)
        ImageGrid = np.zeros((ImageOut.shape[0],ImageOut.shape[1],ImageOut.shape[2]))

        for i in range(0,ImageOut.shape[0]-1):
            for j in range(0,ImageOut.shape[1]-1):
                for k in range(0,ImageOut.shape[2]-1):
                    if (((i%10)==0) or ((j%10)==0) or ((k%10) == 0)):
                        ImageGrid[i,j,k] = 1.0


        ImageGridITK =  imageFromNumpyToITK(ImageGrid)
        ImageGridITK = sitk.Resample(ImageGridITK,self.ImageFixe,self.Final_Transform,self.interpolator,0.0,ImageGridITK.GetPixelIDValue())
        self.ImageGrid =  imageFromITKToNumpy(ImageGridITK )

        FilterTransform = sitk.TransformToDisplacementFieldFilter()
        FilterTransform.SetReferenceImage(self.ImageFixe)
        self.displacementField = FilterTransform.Execute(self.Final_Transform)
        self.transformOut = imageFromITKToNumpy(self.displacementField)
        self.ImageMoving

        return  ImageOut