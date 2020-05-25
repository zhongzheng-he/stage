# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:26:20 2016

@author: broche
"""

import pickle
import os
from PyMca import PyMcaQt as qt

from LabelEditAndButton import LabelEditAndButton


class RegisteringOption(qt.QWidget):

    def __init__(self, ImagesList, parent=None,):
        qt.QWidget.__init__(self, parent)

        self.mainLayout = qt.QGridLayout()
        self.ImagesList = ImagesList

        self.dicPar = {'Grid':[0,0,0],'Inputs':{},'Outputs':{},'Metric':{}, 'Optimizer':{}, 'Interpolator':{}, 'Scaling':[0,0,0,0,0,0,0,0]}
        self.dicPar['Outputs']['Save'] = []
        self.dicPar['Outputs']['Display'] = []
        self.flag_dicUp = False

        self.tabWidget = qt.QTabWidget()
        self.tabInput = qt.QWidget()
        self.tabMetric = qt.QWidget()
        self.tabOptimizer = qt.QWidget()
        self.tabInterpolator = qt.QWidget()
        self.tabScaling = qt.QWidget()
        self.tabOutput = qt.QWidget()

        self.setWindowTitle('Elastic Registration Option')

        """ Inputs Tabs """
        self.layoutInput = qt.QGridLayout()

        self.labelFI = qt.QLabel("Fixed Image")
        self.comboBoxFI = qt.QComboBox()
        self.labelMI = qt.QLabel("Moving Image")
        self.comboBoxMI = qt.QComboBox()

        self.labelFIM = qt.QLabel("Fixed Image Mask")
        self.comboBoxFIM = qt.QComboBox()
        self.labelMIM = qt.QLabel("Moving Image Mask")
        self.comboBoxMIM = qt.QComboBox()

        self.labelIFIT = qt.QLabel("Fixed Image For Inital Tranform")
        self.comboBoxIFIT = qt.QComboBox()
        self.labelIMIT= qt.QLabel("Moving Image For Inital Tranform")
        self.comboBoxIMIT= qt.QComboBox()

        self.initTransform = qt.QCheckBox("Initiate With Rigid Transform")
        self.initTranformC = qt.QComboBox()
        self.initTranformC.addItem("Geometry")
        self.initTranformC.addItem("Moments")
        self.initTranformC.setDisabled(1)

        self.labelGrid = qt.QLabel("Grid Size [x,y,z]")

        self.layoutGrid = qt.QHBoxLayout()
        self.SizeX =  LabelEditAndButton(True,"", True, str(40), False)
        self.SizeY =  LabelEditAndButton(True,"", True, str(40), False)
        self.SizeZ=  LabelEditAndButton(True,"", True, str(40), False)

        self.layoutGrid.addWidget(self.SizeX)
        self.layoutGrid.addWidget(self.SizeY)
        self.layoutGrid.addWidget(self.SizeZ)

        self.layoutInput.addWidget(self.labelFI,0,0)
        self.layoutInput.addWidget(self.labelMI,0,1)
        self.layoutInput.addWidget(self.comboBoxFI ,1,0)
        self.layoutInput.addWidget(self.comboBoxMI ,1,1)
        self.layoutInput.addWidget(self.labelFIM ,2,0)
        self.layoutInput.addWidget(self.labelMIM,2,1)
        self.layoutInput.addWidget(self.comboBoxFIM ,3,0)
        self.layoutInput.addWidget(self.comboBoxMIM ,3,1)
        self.layoutInput.addWidget(self.labelIFIT,4,0)
        self.layoutInput.addWidget(self.labelIMIT,4,1)
        self.layoutInput.addWidget(self.comboBoxIFIT ,5,0)
        self.layoutInput.addWidget(self.comboBoxIMIT ,5,1)
        self.layoutInput.addWidget(self.initTransform ,6,0)
        self.layoutInput.addWidget(self.initTranformC ,6,1)
        self.layoutInput.addWidget(self.labelGrid ,7,0)
        self.layoutInput.addLayout(self.layoutGrid ,8,0)
        self.tabInput.setLayout(self.layoutInput)

        """ Metric """
        self.layoutMetric = qt.QGridLayout()

        self.labelMetric = qt.QLabel("Calculate Metric as :")
        self.comboBoxMetric = qt.QComboBox()
        self.comboBoxMetric.addItem("Means Squares")
        self.comboBoxMetric.addItem("Correlation")
        self.comboBoxMetric.addItem("Demons")
        self.comboBoxMetric.addItem("Joint Histogram Mutual Information")
        self.comboBoxMetric.addItem("Mattes Mutual Information")
        self.comboBoxMetric.addItem("Neighborhood Correlation (ANTs)")

        self.DemonsIntensityDiff = LabelEditAndButton(True, "Intensity Difference: ", True, str(0.001), False)
        self.DemonsIntensityDiff.hide()

        self.HMutalInfoBins = LabelEditAndButton(True, "Number of Bins: ", True, str(20), False)
        self.HMutalInfoVar = LabelEditAndButton(True, " Variance For Joint Probability Density Function Smoothing : ", True, str(1.5), False)
        self.HMutalInfoBins.hide()
        self.HMutalInfoVar.hide()

        self.MatesMutalInfoBins = LabelEditAndButton(True, "Number of Bins: ", True, str(50), False)
        self.MatesMutalInfoBins.hide()

        self.NeigCorrRadius = LabelEditAndButton(True, "Radius: ", True, str(50), False)
        self.NeigCorrRadius.hide()

        self.labelMetricSam = qt.QLabel("Sampling Strategy")
        self.comboBoxMetricSamp = qt.QComboBox()
        self.comboBoxMetricSamp.addItem("None")
        self.comboBoxMetricSamp.addItem("Regular")
        self.comboBoxMetricSamp.addItem("Random")
        self.metricSamplingPerc = LabelEditAndButton(True, "Sampling Percentage: ", True, str(0.01), False)
        self.metricSamplingPerc.setDisabled(1)

        self.checkBoxesGrad= qt.QHBoxLayout()
        self.checkBoxGradientF = qt.QCheckBox("Fixed Image Gradient Filter")
        self.checkBoxGradientM = qt.QCheckBox("Moving Image Gradient Filter")

        self.checkBoxesGrad.addWidget(self.checkBoxGradientF)
        self.checkBoxesGrad.addWidget(self.checkBoxGradientM)

        self.layoutMetric.addWidget(self.labelMetric)
        self.layoutMetric.addWidget(self.comboBoxMetric)
        self.layoutMetric.addWidget(self.DemonsIntensityDiff)
        self.layoutMetric.addWidget(self.HMutalInfoBins)
        self.layoutMetric.addWidget(self.HMutalInfoVar)
        self.layoutMetric.addWidget(self.MatesMutalInfoBins)
        self.layoutMetric.addWidget(self.NeigCorrRadius)
        self.layoutMetric.addWidget(self.labelMetricSam)
        self.layoutMetric.addWidget(self.comboBoxMetricSamp)
        self.layoutMetric.addWidget(self.metricSamplingPerc)
        self.layoutMetric.addLayout(self.checkBoxesGrad,10,0)
        self.tabMetric.setLayout(self.layoutMetric)

        """ Optimizer """

        self.layoutOptimizer = qt.QGridLayout()
        self.labelOptimizer = qt.QLabel("Calculate Optimizer as :")
        self.comboBoxOptimizer = qt.QComboBox()
        self.comboBoxOptimizer.addItem("Regular Step Gradient Descent")
        self.comboBoxOptimizer.addItem("Gradient Descent")
        self.comboBoxOptimizer.addItem("Gradient Descent Line Search")
        self.comboBoxOptimizer.addItem("Conjugate Gradient Line Search")
        self.comboBoxOptimizer.addItem("Exhaustive")
        self.comboBoxOptimizer.addItem("LBFGSB")
        self.comboBoxOptimizer.addItem("Powell")
        self.comboBoxOptimizer.addItem("Amoeba")

        self.list_w_GradientDescentRS = []
        self.GDRS_learningRate = LabelEditAndButton(True, "Learning Rate: ", True, str(1.0), False)
        self.GDRS_minStep = LabelEditAndButton(True, "Min Step: ", True, str(0.1), False)
        self.GDRS_nbIter = LabelEditAndButton(True, "Number of Iterations: ", True, str(10), False)
        self.GDRS_relaxationFactor = LabelEditAndButton(True, "Relaxation Factor: ", True, str(0.5), False)
        self.GDRS_gradMagnitudeTo = LabelEditAndButton(True, "Gradient Magnitude Tolerance: ", True, str(0.0001), False)
        self.GDRS_learnRate = qt.QLabel("Estimate Learning Rate")
        self.GDRS_comboBoxEstiLearningRate = qt.QComboBox()
        self.GDRS_comboBoxEstiLearningRate.addItem("Never")
        self.GDRS_comboBoxEstiLearningRate.addItem("Once")
        self.GDRS_comboBoxEstiLearningRate.addItem("EachIteration")
        self.GDRS_maxStepSize = LabelEditAndButton(True, "Maximun Step Size ", True, str(0.0), False)
        self.GDRS_maxStepSize.setDisabled(1)

        self.list_w_GradientDescentRS.append(self.GDRS_learningRate)
        self.list_w_GradientDescentRS.append(self.GDRS_minStep)
        self.list_w_GradientDescentRS.append(self.GDRS_nbIter)
        self.list_w_GradientDescentRS.append(self.GDRS_relaxationFactor)
        self.list_w_GradientDescentRS.append(self.GDRS_gradMagnitudeTo)
        self.list_w_GradientDescentRS.append(self.GDRS_learnRate)
        self.list_w_GradientDescentRS.append(self.GDRS_comboBoxEstiLearningRate)
        self.list_w_GradientDescentRS.append(self.GDRS_maxStepSize)

        self.list_w_GradientDescent = []
        self.GD_learningRate = LabelEditAndButton(True, "Learning Rate: ", True, str(1.0), False)
        self.GD_nbIter = LabelEditAndButton(True, "Number of Iterations: ", True, str(10), False)
        self.GD_minValue = LabelEditAndButton(True, "Convergence Minimum Value: ", True, str(0.0000001), False)
        self.GD_windowSize = LabelEditAndButton(True, "Convergence Window Size: ", True, str(10), False)
        self.GD_learnRate = qt.QLabel("Estimate Learning Rate")
        self.GD_comboBoxEstiLearningRate = qt.QComboBox()
        self.GD_comboBoxEstiLearningRate.addItem("Never")
        self.GD_comboBoxEstiLearningRate.addItem("Once")
        self.GD_comboBoxEstiLearningRate.addItem("EachIteration")
        self.GD_maxStepSize = LabelEditAndButton(True, "Maximun Step Size ", True, str(0.0), False)
        self.GD_maxStepSize.setDisabled(1)

        self.list_w_GradientDescent.append(self.GD_learningRate)
        self.list_w_GradientDescent.append(self.GD_nbIter)
        self.list_w_GradientDescent.append(self.GD_minValue)
        self.list_w_GradientDescent.append(self.GD_windowSize)
        self.list_w_GradientDescent.append(self.GD_learnRate)
        self.list_w_GradientDescent.append(self.GD_comboBoxEstiLearningRate)
        self.list_w_GradientDescent.append(self.GD_maxStepSize)

        self.list_w_GradientDescentLS = []
        self.GDLS_learningRate = LabelEditAndButton(True, "Learning Rate: ", True, str(1.0), False)
        self.GDLS_nbIter= LabelEditAndButton(True, "Number of Iterations ", True, str(100), False)
        self.GDLS_minValue = LabelEditAndButton(True, "Convergence Minimum Value: ", True, str(0.0000001), False)
        self.GDLS_windowSize = LabelEditAndButton(True, "Convergence Window Size: ", True, str(10), False)
        self.GDLS_lowerLimit = LabelEditAndButton(True, "Line Search Lower Limit: ", True, str(0.2), False)
        self.GDLS_upperLimit = LabelEditAndButton(True, "Line Search Upper Limit: ", True, str(1.0), False)
        self.GDLS_espilon = LabelEditAndButton(True, "Line Search Epsilon: ", True, str(0.01), False)
        self.GDLS_lineMaxIter = LabelEditAndButton(True, "Line Search Maximum Iteration ", True, str(20), False)
        self.GDLS_learnRate = qt.QLabel("Estimate Learning Rate")
        self.GDLS_comboBoxEstiLearningRate = qt.QComboBox()
        self.GDLS_comboBoxEstiLearningRate.addItem("Never")
        self.GDLS_comboBoxEstiLearningRate.addItem("Once")
        self.GDLS_comboBoxEstiLearningRate.addItem("EachIteration")
        self.GDLS_maxStepSize = LabelEditAndButton(True, "Maximun Step Size ", True, str(0.0), False)

        self.list_w_GradientDescentLS.append(self.GDLS_learningRate)
        self.list_w_GradientDescentLS.append(self.GDLS_nbIter)
        self.list_w_GradientDescentLS.append(self.GDLS_minValue)
        self.list_w_GradientDescentLS.append(self.GDLS_windowSize)
        self.list_w_GradientDescentLS.append(self.GDLS_lowerLimit )
        self.list_w_GradientDescentLS.append(self.GDLS_upperLimit )
        self.list_w_GradientDescentLS.append(self.GDLS_espilon )
        self.list_w_GradientDescentLS.append(self.GDLS_lineMaxIter)
        self.list_w_GradientDescentLS.append(self.GDLS_learnRate )
        self.list_w_GradientDescentLS.append(self.GDLS_comboBoxEstiLearningRate )
        self.list_w_GradientDescentLS.append(self.GDLS_maxStepSize )

        self.list_w_GradientCLS= []
        self.GCLS_learningRate = LabelEditAndButton(True, "Learning Rate: ", True, str(1.0), False)
        self.GCLS_nbIter= LabelEditAndButton(True, "Number of Iterations ", True, str(100), False)
        self.GCLS_minValue = LabelEditAndButton(True, "Convergence Minimum Value: ", True, str(0.0000001), False)
        self.GCLS_windowSize = LabelEditAndButton(True, "Convergence Window Size: ", True, str(10), False)
        self.GCLS_lowerLimit = LabelEditAndButton(True, "Line Search Lower Limit: ", True, str(0.0), False)
        self.GCLS_upperLimit = LabelEditAndButton(True, "Line Search Upper Limit: ", True, str(5.0), False)
        self.GCLS_espilon = LabelEditAndButton(True, "Line Search Epsilon: ", True, str(0.01), False)
        self.GCLS_lineMaxIter = LabelEditAndButton(True, "Line Search Maximum Iteration ", True, str(20), False)
        self.GCLS_learnRate = qt.QLabel("Estimate Learning Rate")
        self.GCLS_comboBoxEstiLearningRate = qt.QComboBox()
        self.GCLS_comboBoxEstiLearningRate.addItem("Never")
        self.GCLS_comboBoxEstiLearningRate.addItem("Once")
        self.GCLS_comboBoxEstiLearningRate.addItem("EachIteration")
        self.GCLS_maxStepSize = LabelEditAndButton(True, "Maximun Step Size ", True, str(0.0), False)

        self.list_w_GradientCLS.append(self.GCLS_learningRate)
        self.list_w_GradientCLS.append(self.GCLS_nbIter)
        self.list_w_GradientCLS.append(self.GCLS_minValue)
        self.list_w_GradientCLS.append(self.GCLS_windowSize)
        self.list_w_GradientCLS.append(self.GCLS_lowerLimit )
        self.list_w_GradientCLS.append(self.GCLS_upperLimit )
        self.list_w_GradientCLS.append(self.GCLS_espilon )
        self.list_w_GradientCLS.append(self.GCLS_lineMaxIter)
        self.list_w_GradientCLS.append(self.GCLS_learnRate )
        self.list_w_GradientCLS.append(self.GCLS_comboBoxEstiLearningRate )
        self.list_w_GradientCLS.append(self.GCLS_maxStepSize )

        self.list_w_Exhau = []
        self.Exhau_stepLength = LabelEditAndButton(True, "Learning Rate: ", True, str(1.0), False)
        self.Exhau_vector = qt.QTableWidget()
        self.Exhau_vector.setRowCount(2)
        self.Exhau_vector.setColumnCount(6)
        self.Exhau_vector.setItem(0,0,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(0,1,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(0,2,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(0,3,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(0,4,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(0,5,qt.QTableWidgetItem("0.0"))
        self.Exhau_vector.setItem(1,0,qt.QTableWidgetItem("1.0"))
        self.Exhau_vector.setItem(1,1,qt.QTableWidgetItem("1.0"))
        self.Exhau_vector.setItem(1,2,qt.QTableWidgetItem("1.0"))
        self.Exhau_vector.setItem(1,3,qt.QTableWidgetItem("1.0"))
        self.Exhau_vector.setItem(1,4,qt.QTableWidgetItem("1.0"))
        self.Exhau_vector.setItem(1,5,qt.QTableWidgetItem("1.0"))

        self.list_w_Exhau.append(self.Exhau_stepLength)
        self.list_w_Exhau.append(self.Exhau_vector)

        self.list_w_LBFGSB= []
        self.LBFGSB_gradConv = LabelEditAndButton(True, "Gradient Convergence Tolerance: ", True, str(0.00001), False)
        self.LBFGSB_nbIter = LabelEditAndButton(True, "Number of Iterations: ", True, str(500), False)
        self.LBFGSB_MaxNbCorrection = LabelEditAndButton(True, "Max Number Of Corrections: ", True, str(5), False)
        self.LBFGSB_MaxNbFuncEval = LabelEditAndButton(True, "Max number Of Function Evaluations: ", True, str(2000), False)
        self.LBFGSB_CostFunc = LabelEditAndButton(True, "Cost Function Convergence Factor: ", True, str(10000000), False)

        self.list_w_LBFGSB.append(self.LBFGSB_gradConv)
        self.list_w_LBFGSB.append(self.LBFGSB_nbIter)
        self.list_w_LBFGSB.append(self.LBFGSB_MaxNbCorrection)
        self.list_w_LBFGSB.append(self.LBFGSB_MaxNbFuncEval)
        self.list_w_LBFGSB.append(self.LBFGSB_CostFunc)

        self.list_w_powell = []
        self.powell_nbIter = LabelEditAndButton(True, "Number of Iterations: ", True, str(100), False)
        self.powell_nbIterLine = LabelEditAndButton(True, "Max Line Iterations: ", True, str(100), False)
        self.powell_stepLength = LabelEditAndButton(True, "Step Length: ", True, str(1.0), False)
        self.powell_stepTolerance = LabelEditAndButton(True, "Step Tolerance: ", True, str(0.0000001), False)
        self.powell_valueTolerance = LabelEditAndButton(True, "Value Tolerance: ", True, str(0.0000001), False)

        self.list_w_powell.append(self.powell_nbIter)
        self.list_w_powell.append(self.powell_nbIterLine)
        self.list_w_powell.append(self.powell_stepLength)
        self.list_w_powell.append(self.powell_stepTolerance)
        self.list_w_powell.append(self.powell_valueTolerance)

        self.list_w_amoeba = []
        self.amoeba_sDelta = LabelEditAndButton(True, "Simplex Delta: ", True, str(1.0), False)
        self.amoeba_nbIter = LabelEditAndButton(True, "Number of Iterations: ", True, str(100), False)
        self.amoeba_convTolPar = LabelEditAndButton(True, "Parameters Convergence Tolerance: ", True, str(0.000000001), False)
        self.amoeba_convTolFun = LabelEditAndButton(True, "Function Convergence Tolerance: ", True, str(0.00001), False)

        self.list_w_amoeba.append(self.amoeba_sDelta)
        self.list_w_amoeba.append(self.amoeba_nbIter)
        self.list_w_amoeba.append(self.amoeba_convTolPar)
        self.list_w_amoeba.append(self.amoeba_convTolFun)

        self.labelOptimizerScale = qt.QLabel("Calculate Optimizer Scale From :")
        self.comboBoxOptimizerS = qt.QComboBox()
        self.comboBoxOptimizerS.addItem('Index Shift')
        self.comboBoxOptimizerS.addItem('Jacobian')
        self.comboBoxOptimizerS.addItem('Physical Shift')

        self.list_w_indexShift = []
        self.idxshift_radius = LabelEditAndButton(True, "Central Region Radius: ", True, str(5), False)
        self.idxshift_small_Para_Var = LabelEditAndButton(True, "Small Parameter Variation: ", True, str(0.01), False)
        self.list_w_indexShift.append(self.idxshift_radius)
        self.list_w_indexShift.append(self.idxshift_small_Para_Var)

        self.jac_radius = LabelEditAndButton(True, "Central Region Radius: ", True, str(5), False)

        self.list_w_PhysicalShift = []
        self.phshift_radius = LabelEditAndButton(True, "Central Region Radius: ", True, str(5), False)
        self.phshift_small_Para_Var = LabelEditAndButton(True, "Small Parameter Variation: ", True, str(0.01), False)
        self.list_w_PhysicalShift.append(self.phshift_radius)
        self.list_w_PhysicalShift.append(self.phshift_small_Para_Var)

        self.layoutOptimizer.addWidget(self.labelOptimizer)
        self.layoutOptimizer.addWidget(self.comboBoxOptimizer)

        for w in self.list_w_GradientDescentRS:
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_GradientDescent:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_GradientDescentLS:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_GradientCLS:
            w.hide()
            self.layoutOptimizer.addWidget(w)
        for w in    self.list_w_Exhau:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_LBFGSB:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_powell:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        for w in self.list_w_amoeba :
            w.hide()
            self.layoutOptimizer.addWidget(w)

        self.layoutOptimizer.addWidget(self.labelOptimizerScale)
        self.layoutOptimizer.addWidget(self.comboBoxOptimizerS)

        for w in self.list_w_indexShift:
            w.show()
            self.layoutOptimizer.addWidget(w)

        self.jac_radius.hide()
        self.layoutOptimizer.addWidget(self.jac_radius)

        for w in self.list_w_PhysicalShift:
            w.hide()
            self.layoutOptimizer.addWidget(w)

        self.tabOptimizer.setLayout(self.layoutOptimizer)


        """Interpolator Tabs """
        
        self.layoutInterpolator = qt.QHBoxLayout()

        self.labelIter = qt.QLabel("Interpolator as:")
        self.comboBoxInterpo = qt.QComboBox()
        self.comboBoxInterpo.addItem("Nearest neighbor")
        self.comboBoxInterpo.addItem("Linear Interpolation")
        self.comboBoxInterpo.addItem("BSpline")
        self.comboBoxInterpo.addItem("Gaussian")
        self.comboBoxInterpo.addItem("Label Gaussian")
        self.comboBoxInterpo.addItem("Hamming Windowed Sinc")
        self.comboBoxInterpo.addItem("Cosine Windowed Sinc")
        self.comboBoxInterpo.addItem("Welch Windowed Sinc")
        self.comboBoxInterpo.addItem("Lanczos Windowed Sinc")
        self.comboBoxInterpo.addItem("Blackman Windowed Sinc")

        self.layoutInterpolator.addWidget(self.labelIter)
        self.layoutInterpolator.addWidget(self.comboBoxInterpo)

        self.tabInterpolator.setLayout(self.layoutInterpolator)

        """Scaling Tabs """
        
        self.layoutScaling = qt.QGridLayout()
        self.layoutShrink = qt.QHBoxLayout()
        self.labelShrink = qt.QLabel("Shrink Factors Per Level:")

        self.ShrinkEdit1 =  LabelEditAndButton(True,"", True, str(5), False)
        self.ShrinkEdit2 =  LabelEditAndButton(True,"", True, str(5), False)
        self.ShrinkEdit3 =  LabelEditAndButton(True,"", True, str(5), False)
        self.ShrinkEdit4 =  LabelEditAndButton(True,"", True, str(5), False)

        self.layoutShrink.addWidget(self.ShrinkEdit1)
        self.layoutShrink.addWidget(self.ShrinkEdit2)
        self.layoutShrink.addWidget(self.ShrinkEdit3)
        self.layoutShrink.addWidget(self.ShrinkEdit4)

        self.layoutScaling.addWidget(self.labelShrink )
        self.layoutScaling.addLayout(self.layoutShrink,1,0)

        self.layoutSmooth = qt.QHBoxLayout()
        self.labelSmooth = qt.QLabel("Smoothing Factors Per Level:")

        self.SmoothEdit1 =  LabelEditAndButton(True,"", True, str(5), False)
        self.SmoothEdit2 =  LabelEditAndButton(True,"", True, str(5), False)
        self.SmoothEdit3 =  LabelEditAndButton(True,"", True, str(5), False)
        self.SmoothEdit4 =  LabelEditAndButton(True,"", True, str(5), False)

        self.layoutSmooth.addWidget(self.SmoothEdit1)
        self.layoutSmooth.addWidget(self.SmoothEdit2)
        self.layoutSmooth.addWidget(self.SmoothEdit3)
        self.layoutSmooth.addWidget(self.SmoothEdit4)

        self.layoutScaling.addWidget(self.labelSmooth )
        self.layoutScaling.addLayout(self.layoutSmooth,3,0)
        self.tabScaling.setLayout(self.layoutScaling)

        """Outputs Tabs """

        self.layoutOutputs = qt.QGridLayout()
        self.labelDisplay = qt.QLabel("Display:")

        self.layoutDisplay = qt.QHBoxLayout()
        self.checkBxInfo = qt.QCheckBox("General Infos")
        self.checkBxImages = qt.QCheckBox("Images Overlay")
        self.checkBxMetric = qt.QCheckBox("Metric Curve")
        self.checkBxTransformImage = qt.QCheckBox("Transform")
        self.layoutDisplay.addWidget(self.checkBxInfo )
        self.layoutDisplay.addWidget(self.checkBxImages )
        self.layoutDisplay.addWidget(self.checkBxMetric )
        self.layoutDisplay.addWidget(self.checkBxTransformImage)

        self.labelSaving = qt.QLabel("Saving:")
        self.layoutSaving = qt.QHBoxLayout()
        self.checkBxImages2 = qt.QCheckBox("Images")
        self.checkBxMetric2 = qt.QCheckBox("Metric Curve")
        self.checkBxTransformImage2 = qt.QCheckBox("Transform")
        self.layoutSaving .addWidget(self.checkBxImages2 )
        self.layoutSaving .addWidget(self.checkBxMetric2 )
        self.layoutSaving .addWidget(self.checkBxTransformImage2)

        self.outputsSampling = LabelEditAndButton(True,"Outputs Sampling (x Iterations)", True, str(5), False)

        self.layoutOutputs.addWidget(self.labelDisplay)
        self.layoutOutputs.addLayout(self.layoutDisplay,1,0)
        self.layoutOutputs.addWidget(self.labelSaving)
        self.layoutOutputs.addLayout(self.layoutSaving,3,0)
        self.layoutOutputs.addWidget(self.outputsSampling)
        self.tabOutput.setLayout(self.layoutOutputs)

        """Signals """

        qt.QObject.connect(self.initTransform, qt.SIGNAL("stateChanged(int)"), self.EnableInitTransform)
        qt.QObject.connect(self.comboBoxFI, qt.SIGNAL("currentIndexChanged(int)"), self.FIChanged)
        qt.QObject.connect(self.comboBoxMI, qt.SIGNAL("currentIndexChanged(int)"), self.MIChanged)
        qt.QObject.connect(self.comboBoxFIM, qt.SIGNAL("currentIndexChanged(int)"), self.FIMChanged)
        qt.QObject.connect(self.comboBoxMIM, qt.SIGNAL("currentIndexChanged(int)"), self.MIMChanged)
        qt.QObject.connect(self.comboBoxIFIT, qt.SIGNAL("currentIndexChanged(int)"), self.IFITChanged)
        qt.QObject.connect(self.comboBoxIMIT, qt.SIGNAL("currentIndexChanged(int)"), self.IMITChanged)
        qt.QObject.connect(self.initTranformC, qt.SIGNAL("currentIndexChanged(int)"), self.initTChanged)
        qt.QObject.connect(self.SizeX.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SizeXChanged)
        qt.QObject.connect(self.SizeY.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SizeYChanged)
        qt.QObject.connect(self.SizeZ.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SizeZChanged)

        qt.QObject.connect(self.comboBoxMetric, qt.SIGNAL("currentIndexChanged(int)"), self._MetricChanged)
        qt.QObject.connect(self.DemonsIntensityDiff.lineEdit, qt.SIGNAL("textChanged(QString)"), self._DmIntensChanged)
        qt.QObject.connect(self.HMutalInfoBins.lineEdit, qt.SIGNAL("textChanged(QString)"), self._HMInfoBinsChanged)
        qt.QObject.connect(self.HMutalInfoVar.lineEdit, qt.SIGNAL("textChanged(QString)"), self._HMInfoVarChanged)
        qt.QObject.connect(self.MatesMutalInfoBins.lineEdit, qt.SIGNAL("textChanged(QString)"), self._MatesBinsChanged)
        qt.QObject.connect(self.NeigCorrRadius.lineEdit, qt.SIGNAL("textChanged(QString)"), self._NeigRadiusChanged)
        qt.QObject.connect(self.comboBoxMetricSamp, qt.SIGNAL("currentIndexChanged(int)"), self._MetricSampChanged)
        qt.QObject.connect(self.metricSamplingPerc.lineEdit, qt.SIGNAL("textChanged(QString)"), self._MetricSampValueChanged)
        qt.QObject.connect(self.checkBoxGradientF , qt.SIGNAL("stateChanged(int)"), self.GradientFMetricChanged)
        qt.QObject.connect(self.checkBoxGradientM , qt.SIGNAL("stateChanged(int)"), self.GradientMMetricChanged)

        qt.QObject.connect(self.comboBoxInterpo, qt.SIGNAL("currentIndexChanged(int)"), self._InterpolatorChanged)

        qt.QObject.connect(self.comboBoxOptimizerS, qt.SIGNAL("currentIndexChanged(int)"), self._OptimizerChangedS)
        qt.QObject.connect(self.comboBoxOptimizer, qt.SIGNAL("currentIndexChanged(int)"), self._OptimizerChanged)

        qt.QObject.connect(self.GDRS_learningRate.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_learningRateChanged)
        qt.QObject.connect(self.GDRS_minStep.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_minStepChanged)
        qt.QObject.connect(self.GDRS_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_nbIterChanged)
        qt.QObject.connect(self.GDRS_relaxationFactor.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_relaxationFactorChanged)
        qt.QObject.connect(self.GDRS_gradMagnitudeTo.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_gradMagnitudeToChanged)
        qt.QObject.connect(self.GDRS_maxStepSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDRS_maxStepSizeChanged)
        qt.QObject.connect(self.GDRS_comboBoxEstiLearningRate, qt.SIGNAL("currentIndexChanged(int)"), self.GDRS_EstiLearningRateChanged)


        qt.QObject.connect(self.GD_learningRate.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GD_learningRateChanged)
        qt.QObject.connect(self.GD_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GD_nbIterChanged)
        qt.QObject.connect(self.GD_minValue.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GD_minValueChanged)
        qt.QObject.connect(self.GD_windowSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GD_windowSizeChanged)
        qt.QObject.connect(self.GD_maxStepSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GD_maxStepSizeChanged)
        qt.QObject.connect(self.GD_comboBoxEstiLearningRate, qt.SIGNAL("currentIndexChanged(int)"), self.GD_EstiLearningRateChanged)


        qt.QObject.connect(self.GDLS_learningRate.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_learningRateChanged)
        qt.QObject.connect(self.GDLS_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_nbIterChanged)
        qt.QObject.connect(self.GDLS_minValue.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_minValueChanged)
        qt.QObject.connect(self.GDLS_windowSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_windowSizeChanged)
        qt.QObject.connect(self.GDLS_lowerLimit.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_lowerLimitChanged)
        qt.QObject.connect(self.GDLS_upperLimit.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_upperLimitChanged)
        qt.QObject.connect(self.GDLS_espilon.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_espilonChanged)
        qt.QObject.connect(self.GDLS_lineMaxIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_lineMaxIterChanged)
        qt.QObject.connect(self.GDLS_maxStepSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GDLS_maxStepSizeChanged)
        qt.QObject.connect(self.GDLS_comboBoxEstiLearningRate, qt.SIGNAL("currentIndexChanged(int)"), self.GDLS_EstiLearningRateChanged)

        qt.QObject.connect(self.GCLS_learningRate.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_learningRateChanged)
        qt.QObject.connect(self.GCLS_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_nbIterChanged)
        qt.QObject.connect(self.GCLS_minValue.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_minValueChanged)
        qt.QObject.connect(self.GCLS_windowSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_windowSizeChanged)
        qt.QObject.connect(self.GCLS_lowerLimit.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_lowerLimitChanged)
        qt.QObject.connect(self.GCLS_upperLimit.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_upperLimitChanged)
        qt.QObject.connect(self.GCLS_espilon.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_espilonChanged)
        qt.QObject.connect(self.GCLS_lineMaxIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_lineMaxIterChanged)
        qt.QObject.connect(self.GCLS_maxStepSize.lineEdit, qt.SIGNAL("textChanged(QString)"), self.GCLS_maxStepSizeChanged)
        qt.QObject.connect(self.GCLS_comboBoxEstiLearningRate, qt.SIGNAL("currentIndexChanged(int)"), self.GCLS_EstiLearningRateChanged)

        qt.QObject.connect(self.Exhau_stepLength.lineEdit, qt.SIGNAL("textChanged(QString)"),self.Exhau_stepLengthChanged)
        qt.QObject.connect(self.Exhau_vector,qt.SIGNAL("cellChanged(int,int)"),self.ExhauVectorChanged)
        qt.QObject.connect(self.LBFGSB_gradConv.lineEdit, qt.SIGNAL("textChanged(QString)"), self.LBFGSB_gradConvChanged)
        qt.QObject.connect(self.LBFGSB_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.LBFGSB_nbIterChanged)
        qt.QObject.connect(self.LBFGSB_MaxNbCorrection.lineEdit, qt.SIGNAL("textChanged(QString)"), self.LBFGSB_MaxNbCorrectionChanged)
        qt.QObject.connect(self.LBFGSB_MaxNbFuncEval.lineEdit, qt.SIGNAL("textChanged(QString)"), self.LBFGSB_MaxNbFuncEvalChanged)
        qt.QObject.connect(self.LBFGSB_CostFunc.lineEdit, qt.SIGNAL("textChanged(QString)"), self.LBFGSB_CostFuncChanged)

        qt.QObject.connect(self.powell_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.powell_nbIterChanged)
        qt.QObject.connect(self.powell_nbIterLine.lineEdit, qt.SIGNAL("textChanged(QString)"), self.powell_nbIterLineChanged)
        qt.QObject.connect(self.powell_stepLength.lineEdit, qt.SIGNAL("textChanged(QString)"), self.powell_stepLengthChanged)
        qt.QObject.connect(self.powell_stepTolerance.lineEdit, qt.SIGNAL("textChanged(QString)"), self.powell_stepToleranceChanged)
        qt.QObject.connect(self.powell_valueTolerance.lineEdit, qt.SIGNAL("textChanged(QString)"), self.powell_valueToleranceChanged)

        qt.QObject.connect(self.amoeba_sDelta.lineEdit, qt.SIGNAL("textChanged(QString)"), self.amoeba_sDeltaChanged)
        qt.QObject.connect(self.amoeba_nbIter.lineEdit, qt.SIGNAL("textChanged(QString)"), self.amoeba_nbIterChanged)
        qt.QObject.connect(self.amoeba_convTolPar.lineEdit, qt.SIGNAL("textChanged(QString)"), self.amoeba_convTolParChanged)
        qt.QObject.connect(self.amoeba_convTolFun.lineEdit, qt.SIGNAL("textChanged(QString)"), self.amoeba_convTolFunChanged)

        qt.QObject.connect(self.idxshift_radius.lineEdit, qt.SIGNAL("textChanged(QString)"), self.idxshift_radiusChanged)
        qt.QObject.connect(self.idxshift_small_Para_Var.lineEdit, qt.SIGNAL("textChanged(QString)"), self.idxshift_small_Para_VarChanged)
        qt.QObject.connect(self.jac_radius.lineEdit, qt.SIGNAL("textChanged(QString)"), self.jac_radiusChanged)
        qt.QObject.connect(self.phshift_radius.lineEdit, qt.SIGNAL("textChanged(QString)"), self.phshift_radiusChanged)
        qt.QObject.connect(self.phshift_small_Para_Var.lineEdit, qt.SIGNAL("textChanged(QString)"), self.phshift_small_Para_VarChanged)

        qt.QObject.connect(self.ShrinkEdit1.lineEdit, qt.SIGNAL("textChanged(QString)"), self.ShrinkEdit1Changed)
        qt.QObject.connect(self.ShrinkEdit2.lineEdit, qt.SIGNAL("textChanged(QString)"), self.ShrinkEdit2Changed)
        qt.QObject.connect(self.ShrinkEdit3.lineEdit, qt.SIGNAL("textChanged(QString)"), self.ShrinkEdit3Changed)
        qt.QObject.connect(self.ShrinkEdit4.lineEdit, qt.SIGNAL("textChanged(QString)"), self.ShrinkEdit4Changed)
        qt.QObject.connect(self.SmoothEdit1.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SmoothEdit1Changed)
        qt.QObject.connect(self.SmoothEdit2.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SmoothEdit2Changed)
        qt.QObject.connect(self.SmoothEdit3.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SmoothEdit3Changed)
        qt.QObject.connect(self.SmoothEdit4.lineEdit, qt.SIGNAL("textChanged(QString)"), self.SmoothEdit4Changed)

        qt.QObject.connect(self.checkBxInfo  , qt.SIGNAL("stateChanged(int)"), self.checkBxInfoChanged)
        qt.QObject.connect(self.checkBxImages  , qt.SIGNAL("stateChanged(int)"), self.checkBxImagesChanged)
        qt.QObject.connect(self.checkBxMetric  , qt.SIGNAL("stateChanged(int)"), self.checkBxMetricChanged)
        qt.QObject.connect(self.checkBxTransformImage , qt.SIGNAL("stateChanged(int)"), self.checkBxTransformImageChanged)

        qt.QObject.connect(self.checkBxImages2  , qt.SIGNAL("stateChanged(int)"), self.checkBxImages2Changed)
        qt.QObject.connect(self.checkBxMetric2  , qt.SIGNAL("stateChanged(int)"), self.checkBxMetric2Changed)
        qt.QObject.connect(self.checkBxTransformImage2 , qt.SIGNAL("stateChanged(int)"), self.checkBxTransformImage2Changed)
        qt.QObject.connect(self.outputsSampling.lineEdit, qt.SIGNAL("textChanged(QString)"), self.outputsSamplingChanged)


        """Final """

        self.tabWidget.addTab(self.tabInput,"Inputs/Initialisation")
        self.tabWidget.addTab(self.tabMetric,"Metric")
        self.tabWidget.addTab(self.tabOptimizer,"Optimizer")
        self.tabWidget.addTab(self.tabInterpolator,"Interpolator")
        self.tabWidget.addTab(self.tabScaling,"Scaling")
        self.tabWidget.addTab(self.tabOutput,"Outputs")

        self.buttonLayout= qt.QHBoxLayout()
        self.startRegistering = qt.QPushButton("GO !")

        qt.QObject.connect(self.startRegistering, qt.SIGNAL("clicked()"), self.startRegisteringChanged)
        self.buttonLayout.addWidget(self.startRegistering)

        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addLayout(self.buttonLayout,1,0)

        self.setLayout(self.mainLayout)

        self.restoreValues()

        self.flag_dicUp = True

    def GDRS_learningRateChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.GDRS_learningRate.lineEdit.text())

    def GDRS_minStepChanged(self):
        self.dicPar['Optimizer']['Par'][1] = float(self.GDRS_minStep.lineEdit.text())

    def GDRS_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][2] = int(self.GDRS_nbIter.lineEdit.text())

    def GDRS_relaxationFactorChanged(self):
        self.dicPar['Optimizer']['Par'][3] = float(self.GDRS_relaxationFactor.lineEdit.text())

    def GDRS_gradMagnitudeToChanged(self):
        self.dicPar['Optimizer']['Par'][4] = float(self.GDRS_gradMagnitudeTo.lineEdit.text())

    def GDRS_maxStepSizeChanged(self):
        self.dicPar['Optimizer']['Par'][6] = float(self.GDRS_maxStepSize.lineEdit.text())

    def GDRS_EstiLearningRateChanged(self):

        if self.GDRS_comboBoxEstiLearningRate.currentIndex() == 0:
            self.dicPar['Optimizer']['Par'][5] = 0.0
            self.GDRS_maxStepSize.setDisabled(1)
        elif self.GDRS_comboBoxEstiLearningRate.currentIndex() == 1:
            self.dicPar['Optimizer']['Par'][5] = 1.0
            self.GDRS_maxStepSize.setEnabled(1)
        elif self.GDRS_comboBoxEstiLearningRate.currentIndex() == 2:
            self.dicPar['Optimizer']['Par'][5] = 2.0
            self.GDRS_maxStepSize.setEnabled(1)

    def GD_learningRateChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.GD_learningRate.lineEdit.text())

    def GD_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][1] = int(self.GD_nbIter.lineEdit.text())

    def GD_minValueChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.GD_minValue.lineEdit.text())

    def GD_windowSizeChanged(self):
        self.dicPar['Optimizer']['Par'][3] = int(self.GD_windowSize.lineEdit.text())

    def GD_maxStepSizeChanged(self):
        self.dicPar['Optimizer']['Par'][5] = float(self.GD_maxStepSize.lineEdit.text())

    def GD_EstiLearningRateChanged(self):

        if self.GD_comboBoxEstiLearningRate.currentIndex() == 0:
            self.dicPar['Optimizer']['Par'][4] = 0.0
            self.GD_maxStepSize.setDisabled(1)
        elif self.GD_comboBoxEstiLearningRate.currentIndex() == 1:
            self.dicPar['Optimizer']['Par'][4] = 1.0
            self.GD_maxStepSize.setEnabled(1)
        elif self.GD_comboBoxEstiLearningRate.currentIndex() == 2:
            self.dicPar['Optimizer']['Par'][4] = 2.0
            self.GD_maxStepSize.setEnabled(1)

    def GDLS_learningRateChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.GDLS_learningRate.lineEdit.text())

    def GDLS_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][1] = int(self.GDLS_nbIter.lineEdit.text())

    def GDLS_minValueChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.GDLS_minValue.lineEdit.text())

    def GDLS_windowSizeChanged(self):
        self.dicPar['Optimizer']['Par'][3] = int(self.GDLS_windowSize.lineEdit.text())

    def GDLS_lowerLimitChanged(self):
        self.dicPar['Optimizer']['Par'][4] = float(self.GDLS_lowerLimit.lineEdit.text())

    def GDLS_upperLimitChanged(self):
        self.dicPar['Optimizer']['Par'][5] = float(self.GDLS_upperLimit.lineEdit.text())

    def GDLS_espilonChanged(self):
        self.dicPar['Optimizer']['Par'][6] = float(self.GDLS_espilon.lineEdit.text())

    def GDLS_lineMaxIterChanged(self):
        self.dicPar['Optimizer']['Par'][7] = float(self.GDLS_lineMaxIter.lineEdit.text())

    def GDLS_maxStepSizeChanged(self):
        self.dicPar['Optimizer']['Par'][9] = float(self.GDLS_maxStepSize.lineEdit.text())

    def GDLS_EstiLearningRateChanged(self):

        if self.GDLS_comboBoxEstiLearningRate.currentIndex() == 0:
            self.dicPar['Optimizer']['Par'][8] = 0.0
            self.GDLS_maxStepSize.setDisabled(1)
        elif self.GDLS_comboBoxEstiLearningRate.currentIndex() == 1:
            self.dicPar['Optimizer']['Par'][8] = 1.0
            self.GDLS_maxStepSize.setEnabled(1)
        elif self.GDLS_comboBoxEstiLearningRate.currentIndex() == 2:
            self.dicPar['Optimizer']['Par'][8] = 2.0
            self.GDLS_maxStepSize.setEnabled(1)

    def GCLS_learningRateChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.GCLS_learningRate.lineEdit.text())

    def GCLS_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][1] = int(self.GCLS_nbIter.lineEdit.text())

    def GCLS_minValueChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.GCLS_minValue.lineEdit.text())
        
    def GCLS_windowSizeChanged(self):
        self.dicPar['Optimizer']['Par'][3] = int(self.GCLS_windowSize.lineEdit.text())

    def GCLS_lowerLimitChanged(self):
        self.dicPar['Optimizer']['Par'][4] = float(self.GCLS_lowerLimit.lineEdit.text())

    def GCLS_upperLimitChanged(self):
        self.dicPar['Optimizer']['Par'][5] = float(self.GCLS_upperLimit.lineEdit.text())

    def GCLS_espilonChanged(self):
        self.dicPar['Optimizer']['Par'][6] = float(self.GCLS_espilon.lineEdit.text())

    def GCLS_lineMaxIterChanged(self):
        self.dicPar['Optimizer']['Par'][7] = float(self.GCLS_lineMaxIter.lineEdit.text())

    def GCLS_maxStepSizeChanged(self):
        self.dicPar['Optimizer']['Par'][9] = float(self.GCLS_maxStepSize.lineEdit.text())

    def GCLS_EstiLearningRateChanged(self):

        if self.GCLS_comboBoxEstiLearningRate.currentIndex() == 0:
            self.dicPar['Optimizer']['Par'][8] = 0.0
            self.GCLS_maxStepSize.setDisabled(1)
        elif self.GCLS_comboBoxEstiLearningRate.currentIndex() == 1:
            self.dicPar['Optimizer']['Par'][8] = 1.0
            self.GCLS_maxStepSize.setEnabled(1)
        elif self.GCLS_comboBoxEstiLearningRate.currentIndex() == 2:
            self.dicPar['Optimizer']['Par'][8] = 2.0
            self.GCLS_maxStepSize.setEnabled(1)

    def Exhau_stepLengthChanged(self):

        self.dicPar['Optimizer']['Par'][0] = float(self.Exhau_stepLength.lineEdit.text())

    def  ExhauVectorChanged(self,line,row):

        index = (line*6)+(row+1)
        self.dicPar['Optimizer']['Par'][index] = float(self.Exhau_vector.item(line,row).text())

    def LBFGSB_gradConvChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.LBFGSB_gradConv.lineEdit.text())
    def LBFGSB_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][1] = float(self.LBFGSB_nbIter.lineEdit.text())
    def LBFGSB_MaxNbCorrectionChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.LBFGSB_MaxNbCorrection.lineEdit.text())
    def LBFGSB_MaxNbFuncEvalChanged(self):
        self.dicPar['Optimizer']['Par'][3] = float(self.LBFGSB_MaxNbFuncEval.lineEdit.text())
    def LBFGSB_CostFuncChanged(self):
        self.dicPar['Optimizer']['Par'][4] = float(self.LBFGSB_CostFunc.lineEdit.text())


    def powell_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.powell_nbIter.lineEdit.text())
    def powell_nbIterLineChanged(self):
        self.dicPar['Optimizer']['Par'][1] = float(self.powell_nbIterLine.lineEdit.text())
    def powell_stepLengthChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.powell_stepLength.lineEdit.text())
    def powell_stepToleranceChanged(self):
        self.dicPar['Optimizer']['Par'][3] = float(self.powell_stepTolerance.lineEdit.text())
    def powell_valueToleranceChanged(self):
        self.dicPar['Optimizer']['Par'][4] = float(self.powell_valueTolerance.lineEdit.text())


    def amoeba_sDeltaChanged(self):
        self.dicPar['Optimizer']['Par'][0] = float(self.amoeba_sDelta.lineEdit.text())
    def amoeba_nbIterChanged(self):
        self.dicPar['Optimizer']['Par'][1] = float(self.amoeba_nbIter.lineEdit.text())
    def amoeba_convTolParChanged(self):
        self.dicPar['Optimizer']['Par'][2] = float(self.amoeba_convTolPar.lineEdit.text())
    def amoeba_convTolFunChanged(self):
        self.dicPar['Optimizer']['Par'][3] = float(self.amoeba_convTolFun.lineEdit.text())

    def     idxshift_radiusChanged(self):
        self.dicPar['Optimizer']['ScalePar'][0] = float(self.idxshift_radius.lineEdit.text())

    def     jac_radiusChanged(self):
        self.dicPar['Optimizer']['ScalePar'][0] = float(self.jac_radius.lineEdit.text())

    def    phshift_radiusChanged(self):
        self.dicPar['Optimizer']['ScalePar'][0] = float(self.phshift_radius.lineEdit.text())

    def     idxshift_small_Para_VarChanged(self):
        self.dicPar['Optimizer']['ScalePar'][1] = float(self.idxshift_small_Para_Var.lineEdit.text())

    def    phshift_small_Para_VarChanged(self):
        self.dicPar['Optimizer']['ScalePar'][1] = float(self.phshift_small_Para_Var.lineEdit.text())


    def SizeXChanged(self):
        self.dicPar['Grid'][0] = float(self.SizeX.lineEdit.text())
    def SizeYChanged(self):
        self.dicPar['Grid'][1] = float(self.SizeY.lineEdit.text())

    def SizeZChanged(self):
        self.dicPar['Grid'][2] = float(self.SizeZ.lineEdit.text())

    def ShrinkEdit1Changed(self):
        self.dicPar['Scaling'][0] = float(self.ShrinkEdit1.lineEdit.text())
    def ShrinkEdit2Changed(self):
        self.dicPar['Scaling'][1] = float(self.ShrinkEdit2.lineEdit.text())
    def ShrinkEdit3Changed(self):
        self.dicPar['Scaling'][2] = float(self.ShrinkEdit3.lineEdit.text())
    def ShrinkEdit4Changed(self):
        self.dicPar['Scaling'][3] = float(self.ShrinkEdit4.lineEdit.text())

    def SmoothEdit1Changed(self):
        self.dicPar['Scaling'][4] = float(self.SmoothEdit1.lineEdit.text())
    def SmoothEdit2Changed(self):
        self.dicPar['Scaling'][5] = float(self.SmoothEdit2.lineEdit.text())
    def SmoothEdit3Changed(self):
        self.dicPar['Scaling'][6] = float(self.SmoothEdit3.lineEdit.text())
    def SmoothEdit4Changed(self):
        self.dicPar['Scaling'][7] = float(self.SmoothEdit4.lineEdit.text())

    def _MetricSampValueChanged(self):
        self.dicPar['Metric']['Sampling']['Percentage'] = float(self.metricSamplingPerc.lineEdit.text())

    def _NeigRadiusChanged(self):
        self.dicPar['Metric']['Par'] = [float(self.NeigCorrRadius.lineEdit.text())]

    def _MatesBinsChanged(self):
        self.dicPar['Metric']['Par'] = [int(self.MatesMutalInfoBins.lineEdit.text())]

    def _HMInfoBinsChanged(self):
        self.dicPar['Metric']['Par'][0] = int(self.HMutalInfoBins.lineEdit.text())

    def _HMInfoVarChanged(self):
        self.dicPar['Metric']['Par'][1] = float(self.HMutalInfoVar.lineEdit.text())

    def _DmIntensChanged(self):
        self.dicPar['Metric']['Par'] = [float(self.DemonsIntensityDiff.lineEdit.text())]

    def GradientFMetricChanged(self):
        if self.checkBoxGradientF.checkState() == 2.0:
            self.dicPar['Metric']['GradF'] = 1
        else:

            self.dicPar['Metric']['GradF'] = 0


    def GradientMMetricChanged(self):
        if self.checkBoxGradientM.checkState() == 2.0:
            self.dicPar['Metric']['GradM'] = 1
        else:
            self.dicPar['Metric']['GradM'] =0

    def checkBxInfoChanged(self):
        if self.checkBxInfo.checkState() == 2.0:
            if not('Info' in self.dicPar['Outputs']['Display']):
                self.dicPar['Outputs']['Display'].append("Info")
        else:
            i = self.dicPar['Outputs']['Display'].index("Info")
            del self.dicPar['Outputs']['Display'][i]

    def checkBxImagesChanged(self):
        if self.checkBxImages.checkState() == 2.0:
            if not("Image"in self.dicPar['Outputs']['Display']):
                self.dicPar['Outputs']['Display'].append("Image")
        else:
            i = self.dicPar['Outputs']['Display'].index("Image")
            del self.dicPar['Outputs']['Display'][i]

    def checkBxMetricChanged(self):
        if self.checkBxMetric.checkState() == 2.0:
            if not("Metric"in self.dicPar['Outputs']['Display']):
                self.dicPar['Outputs']['Display'].append("Metric")
        else:
            i = self.dicPar['Outputs']['Display'].index("Metric")
            del self.dicPar['Outputs']['Display'][i]

    def checkBxTransformImageChanged(self):
        if self.checkBxTransformImage.checkState() == 2.0:
            if not("Transform" in self.dicPar['Outputs']['Display']):
                self.dicPar['Outputs']['Display'].append("Transform")
        else:
            i = self.dicPar['Outputs']['Display'].index("Transform")
            del self.dicPar['Outputs']['Display'][i]

    def checkBxMetric2Changed(self):

        if self.checkBxMetric2.checkState() == 2.0:
            if not("Metric" in self.dicPar['Outputs']['Save']):
                self.dicPar['Outputs']['Save'].append("Metric")
        else:
            i = self.dicPar['Outputs']['Save'].index('Metric')
            del self.dicPar['Outputs']['Save'][i]

    def checkBxImages2Changed(self):
        if self.checkBxImages2.checkState() == 2.0:
            if not("Image" in self.dicPar['Outputs']['Save']):
                self.dicPar['Outputs']['Save'].append("Image")
        else:
            i = self.dicPar['Outputs']['Save'].index('Image')
            del self.dicPar['Outputs']['Save'][i]
 

    def checkBxTransformImage2Changed(self):
        if self.checkBxTransformImage2.checkState() == 2.0:
            if not("Transform" in self.dicPar['Outputs']['Save']):
                self.dicPar['Outputs']['Save'].append("Transform")
        else:
            i = self.dicPar['Outputs']['Save'].index('Transform')
            del self.dicPar['Outputs']['Save'][i]

    def outputsSamplingChanged(self):
        self.dicPar['Outputs']['Sampling'] = float(self.outputsSampling.lineEdit.text())

    def closeEvent(self,event):
        quit_msg = "Do you want to Save ?"
        reply = qt.QMessageBox.question(self, 'Message',  quit_msg, qt.QMessageBox.Yes, qt.QMessageBox.No)

        if reply == qt.QMessageBox.Yes:
            self.save_dic()

    def startRegisteringChanged(self):
        self.save_dic()

    def save_dic(self):
        with open('./Data/DicR.pkl', 'wb') as f:
            pickle.dump(self.dicPar, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self ):
        with open('./Data/DicR.pkl', 'rb') as f:
            self.dicPar = pickle.load(f)

    def restoreValues(self):
        if os.path.exists('./Data/DicR.pkl'):
            self.load_obj()
            self.setImages()

            if  self.dicPar['Inputs']['InitT']  != "None":

                self.initTransform.setCheckState(2)

                if self.dicPar['Inputs']['InitT'] == "Geometry":
                    self.initTranformC.setCurrentIndex(0)

                elif self.dicPar['Inputs']['InitT'] == "Moments":
                    self.initTranformC.setCurrentIndex(1)
            else:
                self.initTransform.setCheckState(0)

            if self.dicPar['Metric']['Method'] == "Means Squares":
                self.comboBoxMetric.setCurrentIndex(0)
            elif self.dicPar['Metric']['Method'] == "Correlation":
                self.comboBoxMetric.setCurrentIndex(1)
            elif self.dicPar['Metric']['Method'] == "Demons":
                self.comboBoxMetric.setCurrentIndex(2)
                self.DemonsIntensityDiff.changeLineEdit(str(self.dicPar['Metric']['Par'][0]))
            elif self.dicPar['Metric']['Method'] == "Joint Histogram Mutual Information":
                self.comboBoxMetric.setCurrentIndex(3)
                self.HMutalInfoBins.changeLineEdit(str(self.dicPar['Metric']['Par'][0]))
                self.HMutalInfoVar.changeLineEdit(str(self.dicPar['Metric']['Par'][1]))
            elif self.dicPar['Metric']['Method'] == "Mattes Mutual Information":
                self.comboBoxMetric.setCurrentIndex(4)
                self.MatesMutalInfoBins.changeLineEdit(str(self.dicPar['Metric']['Par'][0]))
            elif self.dicPar['Metric']['Method'] == "Neighborhood Correlation (ANTs)":
                self.comboBoxMetric.setCurrentIndex(5)
                self.NeigCorrRadius.changeLineEdit(str(self.dicPar['Metric']['Par'][0]))

            if self.dicPar['Metric']['Sampling']['Method'] == "None":
                self.comboBoxMetricSamp.setCurrentIndex(0)
            elif self.dicPar['Metric']['Sampling']['Method'] == "Regular":
                self.comboBoxMetricSamp.setCurrentIndex(1)
                self.metricSamplingPerc.changeLineEdit(str(self.dicPar['Metric']['Sampling']['Percentage']))

            elif self.dicPar['Metric']['Sampling']['Method'] == "Random":
                self.comboBoxMetricSamp.setCurrentIndex(2)
                self.metricSamplingPerc.changeLineEdit(str(self.dicPar['Metric']['Sampling']['Percentage']))

            if self.dicPar['Metric']['GradM'] == 0:
                 self.checkBoxGradientM.setCheckState(0)
            else:
                 self.checkBoxGradientM.setCheckState(2)

            if self.dicPar['Metric']['GradF'] == 0:
                 self.checkBoxGradientF.setCheckState(0)
            else:
                 self.checkBoxGradientF.setCheckState(2)

            if self.dicPar['Optimizer']['Method'] == "Regular Step Gradient Descent":
                self.comboBoxOptimizer.setCurrentIndex(0)
                self.GDRS_learningRate.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.GDRS_minStep.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.GDRS_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.GDRS_relaxationFactor.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.GDRS_gradMagnitudeTo.changeLineEdit(str(self.dicPar['Optimizer']['Par'][4]))
                self.GDRS_comboBoxEstiLearningRate.setCurrentIndex(self.dicPar['Optimizer']['Par'][5])
                self.GDRS_maxStepSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][6]))

            elif self.dicPar['Optimizer']['Method'] == "Gradient Descent":
                self.comboBoxOptimizer.setCurrentIndex(1)

                self.GD_learningRate.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.GD_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.GD_minValue.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.GD_windowSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.GD_comboBoxEstiLearningRate.setCurrentIndex(self.dicPar['Optimizer']['Par'][4])
                self.GD_maxStepSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][5]))

            elif self.dicPar['Optimizer']['Method'] == "Gradient Descent Line Search":
                self.comboBoxOptimizer.setCurrentIndex(2)
                self.GDLS_learningRate.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.GDLS_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.GDLS_minValue.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.GDLS_windowSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.GDLS_lowerLimit.changeLineEdit(str(self.dicPar['Optimizer']['Par'][4]))
                self.GDLS_upperLimit.changeLineEdit(str(self.dicPar['Optimizer']['Par'][5]))
                self.GDLS_espilon.changeLineEdit(str(self.dicPar['Optimizer']['Par'][6]))
                self.GDLS_lineMaxIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][7]))
                self.GDLS_comboBoxEstiLearningRate.setCurrentIndex(self.dicPar['Optimizer']['Par'][8])
                self.GDLS_maxStepSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][9]))

            elif self.dicPar['Optimizer']['Method'] == "Conjugate Gradient Line Search":
                self.comboBoxOptimizer.setCurrentIndex(3)

                self.GCLS_learningRate.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.GCLS_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.GCLS_minValue.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.GCLS_windowSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.GCLS_lowerLimit.changeLineEdit(str(self.dicPar['Optimizer']['Par'][4]))
                self.GCLS_upperLimit.changeLineEdit(str(self.dicPar['Optimizer']['Par'][5]))
                self.GCLS_espilon.changeLineEdit(str(self.dicPar['Optimizer']['Par'][6]))
                self.GCLS_lineMaxIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][7]))
                self.GCLS_comboBoxEstiLearningRate.setCurrentIndex(self.dicPar['Optimizer']['Par'][8])
                self.GCLS_maxStepSize.changeLineEdit(str(self.dicPar['Optimizer']['Par'][9]))

            elif self.dicPar['Optimizer']['Method'] == "Exhaustive":
                self.comboBoxOptimizer.setCurrentIndex(4)
                self.Exhau_stepLength.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.Exhau_vector.setItem(0,0,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][1])))
                self.Exhau_vector.setItem(0,1,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][2])))
                self.Exhau_vector.setItem(0,2,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][3])))
                self.Exhau_vector.setItem(0,3,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][4])))
                self.Exhau_vector.setItem(0,4,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][5])))
                self.Exhau_vector.setItem(0,5,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][6])))
                self.Exhau_vector.setItem(1,0,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][7])))
                self.Exhau_vector.setItem(1,1,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][8])))
                self.Exhau_vector.setItem(1,2,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][9])))
                self.Exhau_vector.setItem(1,3,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][10])))
                self.Exhau_vector.setItem(1,4,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][11])))
                self.Exhau_vector.setItem(1,5,qt.QTableWidgetItem(str(self.dicPar['Optimizer']['Par'][12])))

            elif self.dicPar['Optimizer']['Method'] == "LBFGSB":
                self.comboBoxOptimizer.setCurrentIndex(5)
                self.LBFGSB_gradConv.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.LBFGSB_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.LBFGSB_MaxNbCorrection.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.LBFGSB_MaxNbFuncEval.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.LBFGSB_CostFunc.changeLineEdit(str(self.dicPar['Optimizer']['Par'][4]))

            elif self.dicPar['Optimizer']['Method'] == "Powell":
                self.comboBoxOptimizer.setCurrentIndex(6)
                self.powell_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][0]))
                self.powell_nbIterLine.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.powell_stepLength.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.powell_stepTolerance.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))
                self.powell_valueTolerance.changeLineEdit(str(self.dicPar['Optimizer']['Par'][4]))

            elif self.dicPar['Optimizer']['Method'] == "Amoeba":
                self.comboBoxOptimizer.setCurrentIndex(7)
                self.amoeba_sDelta.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][0]))
                self.amoeba_nbIter.changeLineEdit(str(self.dicPar['Optimizer']['Par'][1]))
                self.amoeba_convTolPar.changeLineEdit(str(self.dicPar['Optimizer']['Par'][2]))
                self.amoeba_convTolFun.changeLineEdit(str(self.dicPar['Optimizer']['Par'][3]))

            if self.dicPar['Optimizer']['MethodScaling'] == 'Index Shift':
                self.comboBoxOptimizerS.setCurrentIndex(0)
                self.idxshift_radius.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][0]))
                self.idxshift_small_Para_Var.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][1]))

            elif self.dicPar['Optimizer']['MethodScaling'] == 'Jacobian':
                self.comboBoxOptimizerS.setCurrentIndex(1)
                self.jac_radius.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][0]))

            elif self.dicPar['Optimizer']['MethodScaling'] == 'Physical Shift':
                self.comboBoxOptimizerS.setCurrentIndex(2)
                self.phshift_radius.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][0]))
                self.phshift_small_Para_Var.changeLineEdit(str(self.dicPar['Optimizer']['ScalePar'][1]))

            if self.dicPar['Interpolator'] == "Nearest neighbor":
                self.comboBoxInterpo.setCurrentIndex(0)
            elif self.dicPar['Interpolator'] == "Linear Interpolation" :
                self.comboBoxInterpo.setCurrentIndex(1)
            elif self.dicPar['Interpolator'] == "BSpline":
                self.comboBoxInterpo.setCurrentIndex(2)
            elif self.dicPar['Interpolator'] == "Gaussian":
                self.comboBoxInterpo.setCurrentIndex(3)
            elif self.dicPar['Interpolator'] == "Label Gaussian":
                self.comboBoxInterpo.setCurrentIndex(4)
            elif self.dicPar['Interpolator'] == "Hamming Windowed Sinc":
                self.comboBoxInterpo.setCurrentIndex(5)
            elif self.dicPar['Interpolator'] == "Cosine Windowed Sinc":
                self.comboBoxInterpo.setCurrentIndex(6)
            elif self.dicPar['Interpolator'] == "Welch Windowed Sinc":
                self.comboBoxInterpo.setCurrentIndex(7)
            elif self.dicPar['Interpolator'] == "Lanczos Windowed Sinc":
                self.comboBoxInterpo.setCurrentIndex(8)
            elif self.dicPar['Interpolator'] == "Blackman Windowed Sinc":
                self.comboBoxInterpo.setCurrentIndex(9)


            self.SizeX.changeLineEdit(str(self.dicPar['Grid'][0]))
            self.SizeY.changeLineEdit(str(self.dicPar['Grid'][1]))
            self.SizeZ.changeLineEdit(str(self.dicPar['Grid'][2]))
            self.ShrinkEdit1.changeLineEdit(str(self.dicPar['Scaling'][0]))
            self.ShrinkEdit2.changeLineEdit(str(self.dicPar['Scaling'][1]))
            self.ShrinkEdit3.changeLineEdit(str(self.dicPar['Scaling'][2]))
            self.ShrinkEdit4.changeLineEdit(str(self.dicPar['Scaling'][3]))
            self.SmoothEdit1.changeLineEdit(str(self.dicPar['Scaling'][4]))
            self.SmoothEdit2.changeLineEdit(str(self.dicPar['Scaling'][5]))
            self.SmoothEdit3.changeLineEdit(str(self.dicPar['Scaling'][6]))
            self.SmoothEdit4.changeLineEdit(str(self.dicPar['Scaling'][7]))

            if ("Info" in self.dicPar['Outputs']['Display']):
                 self.checkBxInfo.setCheckState(2)
            else:
                 self.checkBoxGradientM.setCheckState(0)

            if ("Image" in self.dicPar['Outputs']['Display']):
                self.checkBxImages.setCheckState(2)
            else:
                self.checkBxImages.setCheckState(0)

            if ("Metric" in self.dicPar['Outputs']['Display']):
                self.checkBxMetric.setCheckState(2)
            else:
                self.checkBxMetric.setCheckState(0)

            if ("Transform" in self.dicPar['Outputs']['Display']):
                self.checkBxTransformImage.setCheckState(2)
            else:
                self.checkBxTransformImage.setCheckState(0)

            if ("Metric" in self.dicPar['Outputs']['Save']):
                self.checkBxMetric2.setCheckState(2)
            else:
                self.checkBxMetric2.setCheckState(0)


            if ("Image" in self.dicPar['Outputs']['Save']):
                self.checkBxImages2.setCheckState(2)
            else:
                self.checkBxImages2.setCheckState(0)

            if ("Transform" in self.dicPar['Outputs']['Save']):
                self.checkBxTransformImage2.setCheckState(2)
            else:
                self.checkBxTransformImage2.setCheckState(0)


            self.outputsSampling.changeLineEdit(str(self.dicPar['Outputs']['Sampling']))


        else:
            self.setImages()


    def     IFITChanged(self):
        self.dicPar['Inputs']['IFIT'] = self.comboBoxIFIT.currentIndex()

    def     IMITChanged(self):
        self.dicPar['Inputs']['IMIT'] = self.comboBoxIMIT.currentIndex()

    def     FIChanged(self):
        self.dicPar['Inputs']['FI'] = self.comboBoxFI.currentIndex()


    def     MIChanged(self):
        self.dicPar['Inputs']['MI'] = self.comboBoxMI.currentIndex()

    def     FIMChanged(self):
        self.dicPar['Inputs']['FIM'] = self.comboBoxFIM.currentIndex()

    def     MIMChanged(self):
        self.dicPar['Inputs']['MIM'] = self.comboBoxMIM.currentIndex()

    def     initTChanged(self):
        self.dicPar['Inputs']['InitT'] = self.initTranformC.currentText()

    def EnableInitTransform(self):
        if self.initTransform.checkState() == 2:
            self.initTranformC.setEnabled(1)
            if self.flag_dicUp:
                self.dicPar['Inputs']['InitT'] = self.initTranformC.currentText()

        else:
            self.initTranformC.setDisabled(1)
            if self.flag_dicUp:
                self.dicPar['Inputs']['InitT'] = "None"


    def _MetricSampChanged(self):

        if self.flag_dicUp:
            self.dicPar['Metric']['Sampling'] = {'Method': self.comboBoxMetricSamp.currentText(),'Percentage': float(self.metricSamplingPerc.lineEdit.text())}
        if self.comboBoxMetricSamp.currentText() == "None":
            self.metricSamplingPerc.setDisabled(1)
        else:
            self.metricSamplingPerc.setEnabled(1)



    def setImages(self):


        if self.ImagesList != []:
            self.comboBoxFI.addItems(self.ImagesList)
            self.comboBoxMI.addItems(self.ImagesList)
            self.comboBoxFIM.addItem('None')
            self.comboBoxFIM.addItems(self.ImagesList)
            self.comboBoxMIM.addItem('None')
            self.comboBoxMIM.addItems(self.ImagesList)
            self.comboBoxIFIT.addItem('None')
            self.comboBoxIFIT.addItems(self.ImagesList)
            self.comboBoxIMIT.addItem('None')
            self.comboBoxIMIT.addItems(self.ImagesList)

    def _MetricChanged(self):
        if self.comboBoxMetric.currentText() == "Means Squares" :

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Means Squares"
                self.dicPar['Metric']['Par'] = []

            self.DemonsIntensityDiff.hide()
            self.HMutalInfoBins.hide()
            self.HMutalInfoVar.hide()
            self.MatesMutalInfoBins.hide()
            self.NeigCorrRadius.hide()

        elif self.comboBoxMetric.currentText() == "Correlation":

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Correlation"
                self.dicPar['Metric']['Par'] = []

            self.DemonsIntensityDiff.hide()
            self.HMutalInfoBins.hide()
            self.HMutalInfoVar.hide()
            self.MatesMutalInfoBins.hide()
            self.NeigCorrRadius.hide()

        elif self.comboBoxMetric.currentText() == "Demons":

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Demons"
                self.dicPar['Metric']['Par'] = [float(self.DemonsIntensityDiff.lineEdit.text())]

            self.DemonsIntensityDiff.show()
            self.HMutalInfoBins.hide()
            self.HMutalInfoVar.hide()
            self.MatesMutalInfoBins.hide()
            self.NeigCorrRadius.hide()

        elif self.comboBoxMetric.currentText() == "Joint Histogram Mutual Information":

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Joint Histogram Mutual Information"
                self.dicPar['Metric']['Par'] = [int(self.HMutalInfoBins.lineEdit.text()),float(self.HMutalInfoVar.lineEdit.text())]

            self.DemonsIntensityDiff.hide()
            self.HMutalInfoBins.show()
            self.HMutalInfoVar.show()
            self.MatesMutalInfoBins.hide()
            self.NeigCorrRadius.hide()

        elif self.comboBoxMetric.currentText() == "Mattes Mutual Information":

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Mattes Mutual Information"
                self.dicPar['Metric']['Par'] = [int(self.MatesMutalInfoBins.lineEdit.text())]

            self.DemonsIntensityDiff.hide()
            self.HMutalInfoBins.hide()
            self.HMutalInfoVar.hide()
            self.MatesMutalInfoBins.show()
            self.NeigCorrRadius.hide()

        elif self.comboBoxMetric.currentText() == "Neighborhood Correlation (ANTs)":

            if self.flag_dicUp:
                self.dicPar['Metric']['Method'] = "Neighborhood Correlation (ANTs)"
                self.dicPar['Metric']['Par'] = [float(self.NeigCorrRadius.lineEdit.text())]

            self.DemonsIntensityDiff.hide()
            self.HMutalInfoBins.hide()
            self.HMutalInfoVar.hide()
            self.MatesMutalInfoBins.hide()
            self.NeigCorrRadius.show()

    def _OptimizerChanged(self):

        if self.comboBoxOptimizer.currentText() == "Regular Step Gradient Descent":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Regular Step Gradient Descent"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.GDRS_learningRate.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = float(self.GDRS_minStep.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = int(self.GDRS_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = float(self.GDRS_relaxationFactor.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = float(self.GDRS_gradMagnitudeTo.lineEdit.text())
                self.dicPar['Optimizer']['Par'][5] = self.GDRS_comboBoxEstiLearningRate.currentIndex()
                self.dicPar['Optimizer']['Par'][6] = float(self.GDRS_maxStepSize.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.show()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Gradient Descent":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Gradient Descent"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.GD_learningRate.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = int(self.GD_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.GD_minValue.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = int(self.GD_windowSize.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = self.GD_comboBoxEstiLearningRate.currentIndex()
                self.dicPar['Optimizer']['Par'][5] = float(self.GD_maxStepSize.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.show()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Gradient Descent Line Search":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Gradient Descent Line Search"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0,0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.GDLS_learningRate.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = int(self.GDLS_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.GDLS_minValue.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = int(self.GDLS_windowSize.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = float(self.GDLS_lowerLimit.lineEdit.text())
                self.dicPar['Optimizer']['Par'][5] = float(self.GDLS_upperLimit.lineEdit.text())
                self.dicPar['Optimizer']['Par'][6] = float(self.GDLS_espilon.lineEdit.text())
                self.dicPar['Optimizer']['Par'][7] = int(self.GDLS_lineMaxIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][8] = self.GDLS_comboBoxEstiLearningRate.currentIndex()
                self.dicPar['Optimizer']['Par'][9] = float(self.GDLS_maxStepSize.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.show()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Conjugate Gradient Line Search":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Conjugate Gradient Line Search"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0,0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.GCLS_learningRate.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = int(self.GCLS_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.GCLS_minValue.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = int(self.GCLS_windowSize.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = float(self.GCLS_lowerLimit.lineEdit.text())
                self.dicPar['Optimizer']['Par'][5] = float(self.GCLS_upperLimit.lineEdit.text())
                self.dicPar['Optimizer']['Par'][6] = float(self.GCLS_espilon.lineEdit.text())
                self.dicPar['Optimizer']['Par'][7] = int(self.GDLS_lineMaxIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][8] = self.GDLS_comboBoxEstiLearningRate.currentIndex()
                self.dicPar['Optimizer']['Par'][9] = float(self.GDLS_maxStepSize.lineEdit.text())


            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.show()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Exhaustive":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Exhaustive"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.Exhau_stepLength.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = float(self.Exhau_vector.item(0,0).text())
                self.dicPar['Optimizer']['Par'][2] = float(self.Exhau_vector.item(0,1).text())
                self.dicPar['Optimizer']['Par'][3] = float(self.Exhau_vector.item(0,2).text())
                self.dicPar['Optimizer']['Par'][4] = float(self.Exhau_vector.item(0,3).text())
                self.dicPar['Optimizer']['Par'][5] = float(self.Exhau_vector.item(0,4).text())
                self.dicPar['Optimizer']['Par'][6] = float(self.Exhau_vector.item(0,5).text())
                self.dicPar['Optimizer']['Par'][7] = float(self.Exhau_vector.item(1,0).text())
                self.dicPar['Optimizer']['Par'][8] = float(self.Exhau_vector.item(1,1).text())
                self.dicPar['Optimizer']['Par'][9] = float(self.Exhau_vector.item(1,2).text())
                self.dicPar['Optimizer']['Par'][10] = float(self.Exhau_vector.item(1,3).text())
                self.dicPar['Optimizer']['Par'][11] = float(self.Exhau_vector.item(1,4).text())
                self.dicPar['Optimizer']['Par'][12] = float(self.Exhau_vector.item(1,5).text())

            self.comboBoxOptimizerS.setDisabled(1)
            for w in self.list_w_indexShift:
                w.setDisabled(1)
            for w in self.list_w_PhysicalShift:
                w.setDisabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.show()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "LBFGSB":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "LBFGSB"
                self.dicPar['Optimizer']['Par']=[0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.LBFGSB_gradConv.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = float(self.LBFGSB_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.LBFGSB_MaxNbCorrection.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = float(self.LBFGSB_MaxNbFuncEval.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = float(self.LBFGSB_CostFunc.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.show()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Powell":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Powell"

                self.dicPar['Optimizer']['Par']=[0,0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.powell_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = float(self.powell_nbIterLine.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.powell_stepLength.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = float(self.powell_stepTolerance.lineEdit.text())
                self.dicPar['Optimizer']['Par'][4] = float(self.powell_valueTolerance.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.show()
            for w in self.list_w_amoeba:
                w.hide()
        elif self.comboBoxOptimizer.currentText() == "Amoeba":

            if self.flag_dicUp:
                self.dicPar['Optimizer']['Method'] = "Amoeba"
                self.dicPar['Optimizer']['Par']=[0,0,0,0]
                self.dicPar['Optimizer']['Par'][0] = float(self.amoeba_sDelta.lineEdit.text())
                self.dicPar['Optimizer']['Par'][1] = float(self.amoeba_nbIter.lineEdit.text())
                self.dicPar['Optimizer']['Par'][2] = float(self.amoeba_convTolPar.lineEdit.text())
                self.dicPar['Optimizer']['Par'][3] = float(self.amoeba_convTolFun.lineEdit.text())

            self.comboBoxOptimizerS.setEnabled(1)
            for w in self.list_w_indexShift:
                w.setEnabled(1)
            for w in self.list_w_PhysicalShift:
                w.setEnabled(1)

            for w in self.list_w_GradientDescentRS:
                w.hide()
            for w in self.list_w_GradientDescent:
                w.hide()
            for w in self.list_w_GradientDescentLS:
                w.hide()
            for w in self.list_w_GradientCLS:
                w.hide()
            for w in self.list_w_Exhau:
                w.hide()
            for w in self.list_w_LBFGSB:
                w.hide()
            for w in self.list_w_powell:
                w.hide()
            for w in self.list_w_amoeba:
                w.show()


    def _OptimizerChangedS(self):

        if self.comboBoxOptimizerS.currentText() == 'Index Shift':
            if self.flag_dicUp:
                self.dicPar['Optimizer']['MethodScaling'] =  'Index Shift'
                self.dicPar['Optimizer']['ScalePar']=[0,0]
                self.dicPar['Optimizer']['ScalePar'][0] = float(self.idxshift_radius.lineEdit.text())
                self.dicPar['Optimizer']['ScalePar'][1] = float(self.idxshift_small_Para_Var.lineEdit.text())

            for w in self.list_w_indexShift:
                w.show()
            self.jac_radius.hide()
            for w in self.list_w_PhysicalShift:
                w.hide()

        elif self.comboBoxOptimizerS.currentText() == 'Jacobian':
            self.dicPar['Optimizer']['MethodScaling'] =  'Jacobian'
            self.dicPar['Optimizer']['ScalePar']=[0]
            self.dicPar['Optimizer']['ScalePar'][0] = float(self.jac_radius.lineEdit.text())


            for w in self.list_w_indexShift:
                w.hide()
            self.jac_radius.show()
            for w in self.list_w_PhysicalShift:
                w.hide()

        elif self.comboBoxOptimizerS.currentText() == 'Physical Shift':
            self.dicPar['Optimizer']['MethodScaling'] =  'Physical Shift'
            self.dicPar['Optimizer']['ScalePar']=[0,0]
            self.dicPar['Optimizer']['ScalePar'][0] = float(self.phshift_radius.lineEdit.text())
            self.dicPar['Optimizer']['ScalePar'][1] = float(self.phshift_small_Para_Var.lineEdit.text())

            for w in self.list_w_indexShift:
                w.hide()
            self.jac_radius.hide()
            for w in self.list_w_PhysicalShift:
                w.show()

    def _InterpolatorChanged(self):

        if self.comboBoxInterpo.currentText() == "Nearest neighbor":
            self.dicPar['Interpolator'] =  "Nearest neighbor"
        elif self.comboBoxInterpo.currentText() == "Linear Interpolation" :
            self.dicPar['Interpolator'] =  "Linear Interpolation"
        elif self.comboBoxInterpo.currentText() == "BSpline":
            self.dicPar['Interpolator'] =  "BSpline"
        elif self.comboBoxInterpo.currentText() == "Gaussian":
            self.dicPar['Interpolator'] =  "Gaussian"
        elif self.comboBoxInterpo.currentText() == "Label Gaussian":
            self.dicPar['Interpolator'] =  "Label Gaussian"
        elif self.comboBoxInterpo.currentText() == "Hamming Windowed Sinc":
            self.dicPar['Interpolator'] =   "Hamming Windowed Sinc"
        elif self.comboBoxInterpo.currentText() == "Cosine Windowed Sinc":
            self.dicPar['Interpolator'] =  "Cosine Windowed Sinc"
        elif self.comboBoxInterpo.currentText() == "Welch Windowed Sinc":
            self.dicPar['Interpolator'] =  "Welch Windowed Sinc"
        elif self.comboBoxInterpo.currentText() == "Lanczos Windowed Sinc":
            self.dicPar['Interpolator'] =  "Lanczos Windowed Sinc"
        elif self.comboBoxInterpo.currentText() == "Blackman Windowed Sinc":
            self.dicPar['Interpolator'] = "Blackman Windowed Sinc"