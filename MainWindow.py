# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:26:20 2016

@author: broche
"""
import sys
from PyMca import PyMcaQt as qt
from Frame import Frame

class MyMainWindow(qt.QMainWindow) :
    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.mainWidget = Frame()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Pini3_Alpha ')
        self._buildMenu()

    def _buildMenu(self) :
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        loadAction = qt.QAction('&Load Slice Image', self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.setStatusTip('Open 3D Images')
        qt.QObject.connect(loadAction, qt.SIGNAL("triggered()"), self.mainWidget._load)
        fileMenu.addAction(loadAction)
        
        loadActionF = qt.QAction('&Load Folders Image', self)
        loadActionF.setStatusTip('Open 3D Images')
        qt.QObject.connect(loadActionF, qt.SIGNAL("triggered()"), self.mainWidget._loadFolders)
        fileMenu.addAction(loadActionF)


        loadDicomAction = qt.QAction('&Load Dicom/Mat File', self)
        loadDicomAction.setStatusTip('Load Dicom/Mat File')
        qt.QObject.connect(loadDicomAction, qt.SIGNAL("triggered()"), self.mainWidget._loadDicom)
        fileMenu.addAction(loadDicomAction)
        
        loadSTLAction = qt.QAction('&Load STL file as Image', self)
        loadSTLAction.setStatusTip('Load STL File')
        qt.QObject.connect(loadSTLAction, qt.SIGNAL("triggered()"), self.mainWidget._loadSTL)
        fileMenu.addAction(loadSTLAction)
        
        saveAction = qt.QAction( '&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save ')
        qt.QObject.connect(saveAction, qt.SIGNAL("triggered()"), self.mainWidget._save)
        fileMenu.addAction(saveAction)

        exitAction = qt.QAction(qt.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qt.qApp.quit)
        fileMenu.addAction(exitAction)

        ProcessMenu = menubar.addMenu('&Image Processing')

        FormatingMenu = ProcessMenu.addMenu('&Image Format')
        cropAction = qt.QAction('&Crop', self)
        cropAction.setStatusTip('Crop Volume')
        qt.QObject.connect(cropAction , qt.SIGNAL("triggered()"), self.mainWidget._crop )
        FormatingMenu.addAction(cropAction)
        
        fillAction = qt.QAction('&Fill', self)
        fillAction.setStatusTip('Fill Volume')
        qt.QObject.connect(fillAction , qt.SIGNAL("triggered()"), self.mainWidget._fill )
        FormatingMenu.addAction(fillAction)

        resampleAction = qt.QAction('&Resample', self)
        qt.QObject.connect(resampleAction , qt.SIGNAL("triggered()"), self.mainWidget._resample_GUI )
        FormatingMenu.addAction(resampleAction)

        equalizeAction = qt.QAction('&Equalize', self)
        equalizeAction.setStatusTip('Equalize Slices using 1 or 2 uniform zone')
        qt.QObject.connect(equalizeAction, qt.SIGNAL("triggered()"), self.mainWidget._equalize)
        FormatingMenu.addAction(equalizeAction)

        equalizeHistoAction = qt.QAction('&Equalize Histogram', self)
        equalizeHistoAction.setStatusTip('Put the 2 Main Modes of the histogram to a specific Value')
        qt.QObject.connect(equalizeHistoAction, qt.SIGNAL("triggered()"), self.mainWidget._equalizeHisto)
        FormatingMenu.addAction(equalizeHistoAction)

        mozaicAction = qt.QAction('&Mozaic', self)
        mozaicAction.setStatusTip('Make a Mozaic Stack')
        qt.QObject.connect(mozaicAction, qt.SIGNAL("triggered()"), self.mainWidget._mozaicGUI)
        FormatingMenu.addAction(mozaicAction)

        stackAction = qt.QAction('&Stack Images', self)
        stackAction.setStatusTip('Stack Images Together')
        qt.QObject.connect(stackAction, qt.SIGNAL("triggered()"), self.mainWidget._stack_GUI)
        FormatingMenu.addAction(stackAction)

        destackAction = qt.QAction('&Destack Images', self)
        destackAction.setStatusTip('Destack Images Together')
        qt.QObject.connect(destackAction, qt.SIGNAL("triggered()"), self.mainWidget._destack_GUI)
        FormatingMenu.addAction(destackAction)

        AnalyseMenu = ProcessMenu.addMenu('&Analyse')
        analyseAction = qt.QAction('&Analyse Distribution In ROI', self)
        qt.QObject.connect(analyseAction, qt.SIGNAL("triggered()"), self.mainWidget._analysisROIGUI)
        AnalyseMenu.addAction(analyseAction)
        
        analyseLineAction = qt.QAction('&Read Pixels Line', self)
        qt.QObject.connect( analyseLineAction, qt.SIGNAL("triggered()"), self.mainWidget._followLineGUI)
        AnalyseMenu.addAction( analyseLineAction)
        
        analyseMaxLineAction = qt.QAction('&Follow Max Value', self)
        qt.QObject.connect( analyseMaxLineAction, qt.SIGNAL("triggered()"), self.mainWidget._followMaxLineGUI)
        AnalyseMenu.addAction( analyseMaxLineAction)

        histoAction = qt.QAction('&Compute Histogram', self)
        qt.QObject.connect(histoAction, qt.SIGNAL("triggered()"), self.mainWidget._histoGUI)
        AnalyseMenu.addAction(histoAction)

        fftcorrelationAction = qt.QAction('&Cross FFT Correlation', self)
        qt.QObject.connect(fftcorrelationAction, qt.SIGNAL("triggered()"), self.mainWidget._FFTCORGUI)
        AnalyseMenu.addAction(fftcorrelationAction)

        mutualInformationAction = qt.QAction('&Mutual Information In Between Stack', self)
        qt.QObject.connect(mutualInformationAction, qt.SIGNAL("triggered()"), self.mainWidget._MIGUI)
        AnalyseMenu.addAction(mutualInformationAction)

        ratioVolMaskAction = qt.QAction('&Local Volume Ratio Mask', self)
        qt.QObject.connect(ratioVolMaskAction, qt.SIGNAL("triggered()"), self.mainWidget._RatioVolMaskGUI)
        AnalyseMenu.addAction(ratioVolMaskAction )

        ratioMaskAction = qt.QAction('&Local Ratio Mask 2D', self)
        qt.QObject.connect(ratioMaskAction, qt.SIGNAL("triggered()"), self.mainWidget._RatioMaskGUI)
        AnalyseMenu.addAction(ratioMaskAction )

        SelectionMenu = ProcessMenu.addMenu('&Selection')
        smoothAction = qt.QAction('&Smooth Contours', self)
        qt.QObject.connect(smoothAction, qt.SIGNAL("triggered()"), self.mainWidget._smoothContours)
        SelectionMenu.addAction(smoothAction)

        interpolateAction = qt.QAction('&Interpolate Contours', self)
        qt.QObject.connect(interpolateAction, qt.SIGNAL("triggered()"), self.mainWidget._interpolateContourGUI)
        SelectionMenu.addAction(interpolateAction)
        
        interpolateMAction = qt.QAction('&Interpolate Mask', self)
        qt.QObject.connect(interpolateMAction, qt.SIGNAL("triggered()"), self.mainWidget._interpolateMaskGUI)
        SelectionMenu.addAction(interpolateMAction)
        
        fftcorrelationAction = qt.QAction('&Cross FFT Correlation', self)
        qt.QObject.connect(fftcorrelationAction, qt.SIGNAL("triggered()"), self.mainWidget._FFTCORGUI)
        AnalyseMenu.addAction(fftcorrelationAction)
        
        SegmentationMenu = ProcessMenu.addMenu('&Segmentation')

        segment_contour_Action = qt.QAction('&Segmentation From Contour', self)
        segment_contour_Action.setStatusTip('Segmentation From Contour')
        qt.QObject.connect(segment_contour_Action, qt.SIGNAL("triggered()"), self.mainWidget._segFromContour)
        SegmentationMenu.addAction(segment_contour_Action)

        segment_th_Action = qt.QAction('&Threshold ', self)
        segment_th_Action.setStatusTip('3D Region Growing')
        qt.QObject.connect(segment_th_Action, qt.SIGNAL("triggered()"), self.mainWidget._th_segmentation_GUI)
        SegmentationMenu.addAction(segment_th_Action)

        segment_rg_Action = qt.QAction('&3D Region Growing Threathold', self)
        segment_rg_Action.setStatusTip('3D Region Growing')
        qt.QObject.connect(segment_rg_Action, qt.SIGNAL("triggered()"), self.mainWidget._rg_segmentation_GUI)
        SegmentationMenu.addAction(segment_rg_Action)

        segment_rgc_Action = qt.QAction('&3D Region Growing Confidence', self)
        segment_rgc_Action.setStatusTip('3D Region Growing')
        qt.QObject.connect(segment_rgc_Action, qt.SIGNAL("triggered()"), self.mainWidget._rgc_segmentation_GUI)
        SegmentationMenu.addAction(segment_rgc_Action)

        segment_fm_Action = qt.QAction('&Fast Marching', self)
        segment_fm_Action.setStatusTip('Fast Marching Segmentation')
        qt.QObject.connect(segment_fm_Action, qt.SIGNAL("triggered()"), self.mainWidget._fm_segmentation_GUI)
        SegmentationMenu.addAction(segment_fm_Action)

        segment_sd_Action = qt.QAction('&Shape Detection Level Set', self)
        segment_sd_Action.setStatusTip('Shape Detection Level Set')
        qt.QObject.connect(segment_sd_Action, qt.SIGNAL("triggered()"), self.mainWidget._sd_segmentation_GUI)
        SegmentationMenu.addAction(segment_sd_Action)

        segment_geo_Action = qt.QAction('&Geodesic  Level Set', self)
        segment_geo_Action.setStatusTip('Geodesic Level Set')
        qt.QObject.connect(segment_geo_Action, qt.SIGNAL("triggered()"), self.mainWidget._geo_segmentation_GUI)
        SegmentationMenu.addAction(segment_geo_Action)

        segment_wh_Action = qt.QAction('&Watershed', self)
        segment_wh_Action.setStatusTip('Watershed')
        qt.QObject.connect(segment_wh_Action, qt.SIGNAL("triggered()"), self.mainWidget._wh_segmentation_GUI)
        SegmentationMenu.addAction(segment_wh_Action)

        EdgeDetectionMenu = ProcessMenu.addMenu('&Edge Detection')

        edge_GradientRGau_Action = qt.QAction('&Gradient Recursive Gaussian ', self)
        edge_GradientRGau_Action.setStatusTip('Gradient Recursive Gaussian ')
        qt.QObject.connect(edge_GradientRGau_Action, qt.SIGNAL("triggered()"), self.mainWidget.edge_GradGauss_GUI)
        EdgeDetectionMenu.addAction(edge_GradientRGau_Action)

        edge_Canny_Action = qt.QAction('&Canny Edge', self)
        edge_Canny_Action.setStatusTip('Canny Edge')
        qt.QObject.connect(edge_Canny_Action, qt.SIGNAL("triggered()"), self.mainWidget.edge_Canny_GUI)
        EdgeDetectionMenu.addAction(edge_Canny_Action)

        Zero_Crossing_Action = qt.QAction('&Zero Crossing Edge', self)
        Zero_Crossing_Action.setStatusTip('Zero Crossing Edge')
        qt.QObject.connect(Zero_Crossing_Action, qt.SIGNAL("triggered()"), self.mainWidget.zero_Crossing_GUI)
        EdgeDetectionMenu.addAction(Zero_Crossing_Action)

        FilterMenu = ProcessMenu.addMenu('&Filter')

        filter_ani_diff_Action = qt.QAction('&Anisotropic Diffusion', self)
        filter_ani_diff_Action.setStatusTip('Anisotropic Diffusion')
        qt.QObject.connect(filter_ani_diff_Action, qt.SIGNAL("triggered()"), self.mainWidget.filter_anidiff_GUI)
        FilterMenu.addAction(filter_ani_diff_Action)

        filter_recursiveGauss_Action = qt.QAction('&Recursive Gaussian', self)
        filter_recursiveGauss_Action.setStatusTip('Recursive Gaussian')
        qt.QObject.connect(filter_recursiveGauss_Action, qt.SIGNAL("triggered()"), self.mainWidget.filter_recursiveGauss_GUI)
        FilterMenu.addAction(filter_recursiveGauss_Action)

        filter_median_Action = qt.QAction('&Median ', self)
        filter_median_Action.setStatusTip('Median Filter')
        qt.QObject.connect(filter_median_Action, qt.SIGNAL("triggered()"), self.mainWidget.filter_median_GUI)
        FilterMenu.addAction(filter_median_Action)

        filter_sigmo_Action = qt.QAction('&Sigmoid Contrast ', self)
        filter_sigmo_Action.setStatusTip('Sigmoid Mapping  ')
        qt.QObject.connect(filter_sigmo_Action, qt.SIGNAL("triggered()"), self.mainWidget.filter_Sigmo_GUI)
        FilterMenu.addAction(filter_sigmo_Action)

        filter_wv_Action = qt.QAction('&Wavelet Filtering', self)
        filter_wv_Action.setStatusTip('Wavelet Filtering')
        qt.QObject.connect(filter_wv_Action, qt.SIGNAL("triggered()"), self.mainWidget.filter_WL_GUI)
        FilterMenu.addAction(filter_wv_Action)

        mathAction = qt.QAction( '&Math', self)
        mathAction.setStatusTip('Volume Simple Math Calculation')
        qt.QObject.connect(mathAction, qt.SIGNAL("triggered()"), self.mainWidget._math_GUI)
        ProcessMenu.addAction(mathAction)

        ImageRegisteringMenu = ProcessMenu.addMenu('&Image Registration')
        registrationAction = qt.QAction(qt.QIcon('morpho.png'), '&Elastic Registration', self)
        qt.QObject.connect(registrationAction, qt.SIGNAL("triggered()"), self.mainWidget._registration_GUI)
        ImageRegisteringMenu.addAction(registrationAction)

        morphoAction = qt.QAction(qt.QIcon('morpho.png'), '&Morphologic Operation', self)
        morphoAction.setStatusTip('Volume Morph Operation')
        qt.QObject.connect(morphoAction, qt.SIGNAL("triggered()"), self.mainWidget._morpho_GUI)
        ProcessMenu.addAction(morphoAction)

        PreProcessCTMenu = menubar.addMenu('&Pre-processCT')
        ring_algo1_Action = qt.QAction('&Ring Algo1', self)
        ring_algo1_Action.setStatusTip('Ring Algo1')
        qt.QObject.connect(ring_algo1_Action, qt.SIGNAL("triggered()"), self.mainWidget.correct_ring1_GUI)
        PreProcessCTMenu.addAction(ring_algo1_Action)

        flat_field_Action = qt.QAction('&Flat Field Correction', self)
        qt.QObject.connect(flat_field_Action, qt.SIGNAL("triggered()"), self.mainWidget.correct_ff_GUI)
        PreProcessCTMenu.addAction(flat_field_Action)

        StudyMenu = menubar.addMenu('&Study')
        venti_Action = qt.QAction('&Ventilation Map', self)
        venti_Action.setStatusTip('Compute Ventilation Map')
        qt.QObject.connect(venti_Action, qt.SIGNAL("triggered()"), self.mainWidget.study_venti_GUI)
        StudyMenu.addAction(venti_Action)

        density_Action = qt.QAction('&Density Change', self)
        density_Action.setStatusTip('Compute Density Change')
        qt.QObject.connect(density_Action, qt.SIGNAL("triggered()"), self.mainWidget.study_density_GUI)
        StudyMenu.addAction(density_Action)

        macroMenu = menubar.addMenu('&Macros')

        macro2_Action = qt.QAction('&CHU Registration Analysis', self)
        macro2_Action.setStatusTip('CHU Registration Analysis')
        qt.QObject.connect(macro2_Action, qt.SIGNAL("triggered()"), self.mainWidget.macro2_GUI)
        macroMenu.addAction(macro2_Action)
        
        macro3_Action = qt.QAction('&CHU Heart Analysis', self)
        macro3_Action.setStatusTip('CHU Heart Segmentation')
        qt.QObject.connect(macro3_Action, qt.SIGNAL("triggered()"), self.mainWidget.macro3_GUI)
        macroMenu.addAction(macro3_Action)
        
        macro5_Action = qt.QAction('&CHU Lung Blood Volume', self)
        macro5_Action.setStatusTip('CHU Lung Blood Volume')
        qt.QObject.connect(macro5_Action, qt.SIGNAL("triggered()"), self.mainWidget.macro5_GUI)
        macroMenu.addAction(macro5_Action)
        
        macro4_Action = qt.QAction('&Bronchi Study', self)
        macro4_Action.setStatusTip('Bronchi Study')
        qt.QObject.connect(macro4_Action, qt.SIGNAL("triggered()"), self.mainWidget.macro4_GUI)
        macroMenu.addAction(macro4_Action)
        
        macro1_Action = qt.QAction('&Image Analysis Diffusion', self)
        macro1_Action.setStatusTip('Concentration Analysis Diffusion Study')
        qt.QObject.connect(macro1_Action, qt.SIGNAL("triggered()"), self.mainWidget.macro1_GUI)
        macroMenu .addAction(macro1_Action)




if __name__ == "__main__":

    app = qt.QApplication(["-display"])
    foo = MyMainWindow()
    foo.resize(400, 400)
    foo.show()
    sys.exit(app.exec_())
