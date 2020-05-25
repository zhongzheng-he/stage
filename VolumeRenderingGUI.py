# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:50:34 2017

@author: broche
"""
from PyMca import PyMcaQt as qt
from TitleAndIcones import TitleAndIcones
import SliderAndLabel
import usefullVTKFunctions as VtkUF
import numpy as np
from LabelEditAndButton import LabelEditAndButton


class VolumeRenderingGUI(qt.QWidget):

    def __init__(self, parent=None,):
        qt.QWidget.__init__(self, parent)

        self.mainLayout = qt.QGridLayout()
        self.frame = VtkUF.VTK_Render_QT()

        nb_row = 9
        width_widget = 350

        self.check_parameters_files()
        self.ImagesList = []
        self.DataList = []
        self.ItemLists = []

        """
        Image To Render
        """
        self.labelIR= qt.QLabel("Volume To Render")
        self.labelIR.setMaximumWidth(width_widget)
        self.comboBoxIR = qt.QComboBox()
        self.comboBoxIR.setMaximumWidth(width_widget)
        self.labelVF= qt.QLabel("Vector Field To Render")
        self.labelVF.setMaximumWidth(width_widget)
        self.comboBoxVF = qt.QComboBox()
        self.comboBoxVF.setMaximumWidth(width_widget)
        self.labelP= qt.QLabel("Plane Image To Render")
        self.labelP.setMaximumWidth(width_widget)
        self.comboBoxP = qt.QComboBox()
        self.comboBoxP.setMaximumWidth(width_widget)
        self.LayoutPlane = qt.QHBoxLayout()

        self.Xplane = LabelEditAndButton(True, "X: ", True, str(0), False)
        self.Xplane.setMaximumWidth(width_widget/3.0)
        self.Yplane = LabelEditAndButton(True, "X: ", True, str(0), False)
        self.Yplane.setMaximumWidth(width_widget/3.0)
        self.Zplane = LabelEditAndButton(True, "Z: ", True, str(0), False)
        self.Zplane.setMaximumWidth(width_widget/3.0)
        self.LayoutPlane.addWidget(self.Xplane)
        self.LayoutPlane.addWidget(self.Yplane)
        self.LayoutPlane.addWidget(self.Zplane)

        self.setImages()
        """------------------------------------
        COLOR TABLE
        -------------------------------------"""

        self.color_TitleAndIcons = TitleAndIcones(True,"Color Table",True, './Icones/save.png','./Icones/saveas.png','./Icones/load.png')
        self.connect(self.color_TitleAndIcons.save,qt.SIGNAL("clicked()"),self._buttonColorSavePushed)
        self.connect(self.color_TitleAndIcons.saveas,qt.SIGNAL("clicked()"),self._buttonColorSaveasPushed)
        self.connect(self.color_TitleAndIcons.load,qt.SIGNAL("clicked()"),self._buttonColorLoadPushed)

        self.colorCoef = qt.QTableWidget(nb_row,6)
        self.colorCoef.verticalHeader().hide()
        self.colorCoef.setColumnWidth(0, 50)
        self.colorCoef.setColumnWidth(1, 50)
        self.colorCoef.setColumnWidth(2, 50)
        self.colorCoef.setColumnWidth(3, 50)
        self.colorCoef.setColumnWidth(4, 70)
        self.colorCoef.setColumnWidth(5, 85)

        for i in range(nb_row):
            self.colorCoef.setRowHeight(i,15)
        self.colorCoef.setMaximumWidth(width_widget)
        self.colorCoef.setHorizontalHeaderLabels(['Value','R','G','B','Midpoint','Sharpness'])
        self.colorCoef.setContentsMargins(-1,0,-1,-1)

        self.fill_colorTable()

        """------------------------------------
        ALPHA TABLE
        -------------------------------------"""

        self.alpha_TitleAndIcons = TitleAndIcones(True,"Alpha Table",True, './Icones/save.png','./Icones/saveas.png','./Icones/load.png')
        self.connect(self.alpha_TitleAndIcons.save,qt.SIGNAL("clicked()"),self._buttonAlphaSavePushed)
        self.connect(self.alpha_TitleAndIcons.saveas,qt.SIGNAL("clicked()"),self._buttonAlphaSaveasPushed)
        self.connect(self.alpha_TitleAndIcons.load,qt.SIGNAL("clicked()"),self._buttonAlphaLoadPushed)

        self.AlphaCoef = qt.QTableWidget(nb_row, 4)
        self.AlphaCoef.verticalHeader().hide()
        self.AlphaCoef.setColumnWidth(0,50)
        self.AlphaCoef.setColumnWidth(1,50)
        self.AlphaCoef.setColumnWidth(2,70)
        self.AlphaCoef.setColumnWidth(3,85)

        for i in range(nb_row):
            self.AlphaCoef.setRowHeight(i,15)
        self.AlphaCoef.setMaximumWidth(width_widget)
        self.AlphaCoef.setHorizontalHeaderLabels(['Value','Alpha','Midpoint','Sharpness'])
        self.AlphaCoef.setContentsMargins(-1,0,-1,-1)

        self.fill_alphaTable()


        """------------------------------------
        PARAMETERS
        -------------------------------------"""

        self.parameters_TitleAndIcons = TitleAndIcones(True,"Volume Parameters",True, './Icones/save.png','./Icones/saveas.png','./Icones/load.png')
        self.connect(self.parameters_TitleAndIcons.save,qt.SIGNAL("clicked()"),self._buttonParaSavePushed)
        self.connect(self.parameters_TitleAndIcons.saveas,qt.SIGNAL("clicked()"),self._buttonParaSaveasPushed)
        self.connect(self.parameters_TitleAndIcons.load,qt.SIGNAL("clicked()"),self._buttonParaLoadPushed)


        self.renderButton = qt.QPushButton("Render")
        self.renderButton.setMaximumWidth(width_widget)


        self.check_box_mesh = qt.QCheckBox("Marching Cube Volume")
        self.ThresholdMC = LabelEditAndButton(True, "Value For Threshold", True, str(0.5), False)

        self.check_smooth = qt.QCheckBox("Smoothing Mesh")
        self.SmoothIterNb = LabelEditAndButton(True, "Smooth Iteration Number :", True, str(10), False)
        self.SmoothRelaxF = LabelEditAndButton(True, "Relaxation Factor :", True, str(0.5), False)

        self.check_box_mesh.setMaximumWidth(width_widget)
        self.ThresholdMC.setMaximumWidth(width_widget)

        self.check_smooth.setMaximumWidth(width_widget)
        self.SmoothIterNb.setMaximumWidth(width_widget)
        self.SmoothRelaxF.setMaximumWidth(width_widget)

        self.checkBox = qt.QCheckBox("Shade")
        self.checkBox.setMaximumWidth(width_widget)

        self.LabelAmb=qt.QLabel("Ambient lighting coefficient")
        self.LabelAmb.setContentsMargins(-1,-1,-1,0)
        self.sliderAmb = SliderAndLabel.SliderAndLabelSpecificScale()
        self.sliderAmb.setMaximumWidth(width_widget)
        self.sliderAmb._setStepPrecision(0.05)
        self.sliderAmb._setRange(0,10.0)
        self.sliderAmb.setContentsMargins(-1,0,-1,-1)

        self.LabelDif=qt.QLabel("Diffuse lighting Coefficient")
        self.LabelDif.setContentsMargins(-1,-1,-1,0)
        self.sliderDif = SliderAndLabel.SliderAndLabelSpecificScale()
        self.sliderDif.setMaximumWidth(width_widget)
        self.sliderDif._setStepPrecision(0.05)
        self.sliderDif._setRange(0,10.0)
        self.sliderDif.setContentsMargins(-1,0,-1,-1)

        self.LabelSpe=qt.QLabel("Specular lighting Coefficient")
        self.LabelSpe.setContentsMargins(-1,-1,-1,0)
        self.sliderSpe = SliderAndLabel.SliderAndLabelSpecificScale()
        self.sliderSpe.setMaximumWidth(width_widget)
        self.sliderSpe._setStepPrecision(0.05)
        self.sliderSpe._setRange(0,10.0)
        self.sliderSpe.setContentsMargins(-1,0,-1,-1)

        self.LabelSpeP=qt.QLabel("Specular power Coefficient")
        self.LabelSpeP.setContentsMargins(-1,-1,-1,0)
        self.sliderSpeP = SliderAndLabel.SliderAndLabelSpecificScale()
        self.sliderSpeP.setMaximumWidth(width_widget)
        self.sliderSpeP._setStepPrecision(0.05)
        self.sliderSpeP._setRange(0,10.0)
        self.sliderSpeP.setContentsMargins(-1,0,-1,-1)


        self.LabelOpa=qt.QLabel("Opacity unit distance")
        self.LabelOpa.setContentsMargins(-1,-1,-1,0)
        self.sliderOpa = SliderAndLabel.SliderAndLabelSpecificScale()
        self.sliderOpa.setMaximumWidth(width_widget)
        self.sliderOpa._setStepPrecision(1)

        self.sliderOpa._setRange(0,1000)
        self.sliderOpa.setContentsMargins(-1,0,-1,-1)

        self.fill_para()


        self.mainLayout.addWidget(self.frame,0,0)

        self.mainLayout.addWidget(self.color_TitleAndIcons,0,1)
        self.mainLayout.addWidget(self.colorCoef,1,1,10,1)

        self.mainLayout.addWidget(self.alpha_TitleAndIcons,12,1)
        self.mainLayout.addWidget(self.AlphaCoef,13,1,10,1)
        self.mainLayout.addWidget(self.labelIR,1,2)
        self.mainLayout.addWidget(self.comboBoxIR,2,2)
        self.mainLayout.addWidget(self.labelVF,3,2)
        self.mainLayout.addWidget(self.comboBoxVF,4,2)
        self.mainLayout.addWidget(self.labelP,5,2)
        self.mainLayout.addWidget(self.comboBoxP,6,2)

        self.mainLayout.addWidget(self.check_box_mesh,7,2)
        self.mainLayout.addWidget(self.ThresholdMC,8,2)

        self.mainLayout.addWidget(self.check_smooth,9,2)
        self.mainLayout.addWidget(self.SmoothIterNb,10,2)
        self.mainLayout.addWidget(self.SmoothRelaxF,11,2)

        self.mainLayout.addLayout(self.LayoutPlane,12,2)
        self.mainLayout.addWidget(self.parameters_TitleAndIcons,13,2)
        self.mainLayout.addWidget(self.checkBox,14,2)
        self.mainLayout.addWidget(self.LabelAmb,15,2)
        self.mainLayout.addWidget(self.sliderAmb,16,2)
        self.mainLayout.addWidget(self.LabelDif,17,2)
        self.mainLayout.addWidget(self.sliderDif,18,2)
        self.mainLayout.addWidget(self.LabelSpe,19,2)
        self.mainLayout.addWidget(self.sliderSpe,20,2)
        self.mainLayout.addWidget(self.LabelSpeP,21,2)
        self.mainLayout.addWidget(self.sliderSpeP,22,2)
        self.mainLayout.addWidget(self.LabelOpa,23,2)
        self.mainLayout.addWidget(self.sliderOpa,24,2)
        self.mainLayout.addWidget(self.renderButton,25,2)

        self.setLayout(self.mainLayout)


        qt.QObject.connect(self.renderButton, qt.SIGNAL("clicked()"), self._render)

    def check_parameters_files(self):
        source_file_color = open('./VTK_parameters/history', "r")
        files_para = source_file_color.readlines()

        if len(files_para) != 3 :
            msgBox = qt.QMessageBox(self)
            msgBox.setText('Missing parameters files in the history')
            msgBox.exec_()
        else:
            matching = [s for s in files_para if ".col" in s]
            if len(str(matching)) != 2:
                self.color_file = str(matching[0]).rstrip('\n')
            else:
                self.color_file = 'empty'
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Missing color file')
                msgBox.exec_()

            matching = [s for s in files_para if ".alp" in s]
            if len(str(matching)) != 2:
                self.alpha_file = str(matching[0]).rstrip('\n')
            else:
                self.alpha_file = 'empty'
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Missing alpha file')
                msgBox.exec_()

            matching = [s for s in files_para if ".pr" in s]
            if len(str(matching)) != 2:
                self.para_file = str(matching[0]).rstrip('\n')
            else:
                self.para_file = 'empty'
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Missing parameters file')
                msgBox.exec_()



    def fill_colorTable(self):
        if self.color_file != 'empty':
            try:
                    source_file_color = open('./VTK_parameters/'+self.color_file, "r")
            except IOError:
                msgBox = qt.QMessageBox(self)
                msgBox.setText('The color file ' + self.color_file + ' does not exist')
                msgBox.exec_()

            all_lines = source_file_color.readlines()

            j = 0
            for line in all_lines:
                line = line.rstrip('\n')
                line = line.split(' ')

                try:
                    line.remove('')
                except:
                    pass

                if len(line) == 4:
                    for i in range(4):
                        Item = qt.QTableWidgetItem()
                        Item.setText(str(line[i]))
                        self.colorCoef.setItem(j,i,Item)
                elif len(line) == 6:
                    for i in range(6):
                        Item = qt.QTableWidgetItem()
                        Item.setText(str(line[i]))
                        self.colorCoef.setItem(j,i,Item)
                j += 1

    def setImages(self):

        self.comboBoxIR.clear()
        self.comboBoxVF.clear()
        self.comboBoxP.clear()

        if self.ImagesList != []:
            self.comboBoxIR.addItems(self.ImagesList)
            self.comboBoxVF.addItem('None')
            self.comboBoxVF.addItems(self.ImagesList)
            self.comboBoxP.addItem('None')
            self.comboBoxP.addItems(self.ImagesList)

    def fill_alphaTable(self):
        if self.alpha_file != 'empty':
            try:
                    source_file_alpha  = open('./VTK_parameters/'+self.alpha_file, "r")
            except IOError:
                msgBox = qt.QMessageBox(self)
                msgBox.setText('The alpha file ' + self.alpha_file + ' does not exist')
                msgBox.exec_()

            all_lines = source_file_alpha.readlines()
            j = 0
            for line in all_lines:

                line = line.rstrip('\n')
                line = line.split(' ')
                try:
                    line.remove('')
                except:
                    pass
                if len(line) == 2:
                    for i in range(2):
                        Item = qt.QTableWidgetItem()
                        Item.setText(str(line[i]))
                        self.AlphaCoef.setItem(j,i,Item)
                elif len(line) == 4:
                    for i in range(4):
                        Item = qt.QTableWidgetItem()

                        Item.setText(str(line[i]))
                        self.AlphaCoef.setItem(j,i,Item)
                j += 1

    def fill_para(self):

        if self.para_file != 'empty':
            try:
                source_file_para  = open('./VTK_parameters/'+self.para_file , "r")

            except IOError:
                msgBox = qt.QMessageBox(self)
                msgBox.setText('The parameters fil : ' + self.para_file + ' does not exist')
                msgBox.exec_()

            line = source_file_para .readlines()[0]
            parameters = line.split(' ')

            if int(parameters[0]) == 2:
                self.checkBox.setChecked(2)
            else:
                self.checkBox.setChecked(0)

            self.sliderAmb._defaultValue(float(parameters[1]))
            self.sliderDif._defaultValue(float(parameters[2]))
            self.sliderSpe._defaultValue(float(parameters[3]))
            self.sliderSpeP._defaultValue(float(parameters[4]))
            self.sliderOpa._defaultValue(float(parameters[5]))
        else:
            self.sliderAmb._defaultValue(1)
            self.sliderDif._defaultValue(1)
            self.sliderSpe._defaultValue(1)
            self.sliderSpeP._defaultValue(1)
            self.sliderOpa._defaultValue(1)


    def _buttonColorSavePushed(self):
        source_file_color = open('./VTK_parameters/history', "r")
        files_para = source_file_color.readlines()
        matching = [s for s in files_para if ".col" in s]

        if len(str(matching)) != 2:
            color_file = str(matching[0]).rstrip('\n')
            if color_file == 'color_rendering_default.col':
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Overwrite the default file is not allowed. Create a new file to save your table')
                msgBox.exec_()
            else:

                colorFileToWrite = open('./VTK_parameters/' + color_file, "w")

                for i in range(10):
                    for j in range(6):
                        try:
                            colorFileToWrite.writelines(self.colorCoef.item(i,j).text()+ ' ')
                        except:
                            if j == 4:
                                colorFileToWrite.writelines('0.5 ')
                            else:
                                colorFileToWrite.writelines('0 ')
                    colorFileToWrite.writelines('\n')

        self.check_parameters_files()

    def _buttonColorSaveasPushed(self):
        newColorFile = str(qt.QFileDialog.getSaveFileName(self, "save our color table", './VTK_parameters/'))
        newColorFile= newColorFile.split('/')[-1]

        if len(newColorFile) != 0:

            source_file_color = open('./VTK_parameters/history', "r")
            files_para = source_file_color.readlines()
            source_file_color = open('./VTK_parameters/history', "w")
            for line in files_para:
                if '.col' in line:
                    source_file_color.writelines(newColorFile+'.col\n')
                else:
                    source_file_color.writelines(line)
            source_file_color.close()
            f= open('./VTK_parameters/'+newColorFile+'.col','w')
            f.close()

        self._buttonColorSavePushed()

    def _buttonColorLoadPushed(self):
        ColFile = str(qt.QFileDialog.getOpenFileName(self, "load our parameters", './VTK_parameters/',str("Color File (*.col)")))
        ColFile= ColFile.split('/')[-1]
        if len(ColFile) != 0 :
            source_file_color = open('./VTK_parameters/history', "r")
            files_para = source_file_color.readlines()
            source_file_color = open('./VTK_parameters/history', "w")
            for line in files_para:

                if '.col' in line:
                    source_file_color.writelines(ColFile+'\n')
                else:
                    source_file_color.writelines(line)
            source_file_color.close()

        self.check_parameters_files()
        self.fill_colorTable()

    def _buttonAlphaSavePushed(self):
        source_file_color = open('./VTK_parameters/history', "r")
        files_para = source_file_color.readlines()
        matching = [s for s in files_para if ".alp" in s]

        if len(str(matching)) != 2:
            alpha_file = str(matching[0]).rstrip('\n')
            if alpha_file == 'alpha_rendering_default.alp':
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Overwrite the default file is not allowed. Create a new file to save your table')
                msgBox.exec_()
            else:

                alphaFileToWrite = open('./VTK_parameters/' + alpha_file, "w")

                for i in range(10):
                    for j in range(4):
                        try:
                            alphaFileToWrite.writelines(self.AlphaCoef.item(i,j).text()+ ' ')
                        except:
                            if j == 4:
                                alphaFileToWrite.writelines('0.5 ')
                            else:
                                alphaFileToWrite.writelines('0 ')
                    alphaFileToWrite.writelines('\n')

        self.check_parameters_files()

    def _buttonAlphaSaveasPushed(self):

        newAlphaFile = str(qt.QFileDialog.getSaveFileName(self, "save our alpha table", './VTK_parameters/'))
        newAlphaFile= newAlphaFile.split('/')[-1]
        if len(newAlphaFile) != 0:
            source_file_color = open('./VTK_parameters/history', "r")
            files_para = source_file_color.readlines()
            source_file_color = open('./VTK_parameters/history', "w")
            for line in files_para:
                if '.alp' in line:
                    source_file_color.writelines(newAlphaFile+'.alp\n')
                else:
                    source_file_color.writelines(line)
            source_file_color.close()
            f= open('./VTK_parameters/'+newAlphaFile+'.alp','w')
            f.close()
        self._buttonAlphaSavePushed()

    def _buttonAlphaLoadPushed(self):
        alphaFile = str(qt.QFileDialog.getOpenFileName(self, "load our parameters", './VTK_parameters/',str("Alpha File (*.alp)")))
        alphaFile= alphaFile.split('/')[-1]
        if len(alphaFile) !=0:
            source_file_alpha = open('./VTK_parameters/history', "r")
            files_para = source_file_alpha.readlines()
            source_file_alpha = open('./VTK_parameters/history', "w")
            for line in files_para:

                if '.alp' in line:
                    source_file_alpha.writelines(alphaFile+'\n')
                else:
                    source_file_alpha.writelines(line)
            source_file_alpha.close()

        self.check_parameters_files()
        self.fill_alphaTable()

    def _buttonParaSavePushed(self):
        source_file_color = open('./VTK_parameters/history', "r")
        files_para = source_file_color.readlines()
        matching = [s for s in files_para if ".pr" in s]

        if len(str(matching)) != 2:
            para_file = str(matching[0]).rstrip('\n')
            if para_file == 'para_rendering_default.pr':
                msgBox = qt.QMessageBox(self)
                msgBox.setText('Overwrite the default file is not allowed. Create a new file to save your table')
                msgBox.exec_()
            else:

                paraFileToWrite = open('./VTK_parameters/' + para_file, "w")
                paraFileToWrite.writelines(str(self.checkBox.checkState()) + ' ')
                paraFileToWrite.writelines(str(self.sliderAmb.value())+ ' ')
                paraFileToWrite.writelines(str(self.sliderDif.value())+ ' ')
                paraFileToWrite.writelines(str(self.sliderSpe.value())+ ' ')
                paraFileToWrite.writelines(str(self.sliderSpe.value())+ ' ')
                paraFileToWrite.writelines(str(self.sliderSpeP.value())+ ' ')
                paraFileToWrite.writelines(str(self.sliderOpa.value()))

        self.check_parameters_files()

    def _buttonParaSaveasPushed(self):

        newParaFile = str(qt.QFileDialog.getSaveFileName(self, "save our parameters", '/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/'))
        newParaFile= newParaFile.split('/')[-1]

        if len(newParaFile) !=0:
            source_file_color = open('/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/history', "r")
            files_para = source_file_color.readlines()
            source_file_color = open('/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/history', "w")
            for line in files_para:
                if '.pr' in line:
                    source_file_color.writelines(newParaFile+'.pr\n')
                else:
                    source_file_color.writelines(line)
            source_file_color.close()
            f= open('./VTK_parameters/'+newParaFile+'.pr','w')
            f.close()
        self._buttonParaSavePushed()

    def _buttonParaLoadPushed(self):
        paraFile = str(qt.QFileDialog.getOpenFileName(self, "load our parameters", '/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/',str("Color File (*.pr)")))
        paraFile= paraFile.split('/')[-1]
        if len(paraFile) != 0:
            source_file_color = open('/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/history', "r")
            files_para = source_file_color.readlines()
            source_file_color = open('/data/id17/broncho/md738/id17/RabbitSegm/Pini_experimental1/VTK_parameters/history', "w")
            for line in files_para:

                if '.pr' in line:
                    source_file_color.writelines(paraFile+'\n')
                else:
                    source_file_color.writelines(line)
            source_file_color.close()


        self.check_parameters_files()
        self.fill_para()

    def _render(self) :

        self.frame = VtkUF.VTK_Render_QT()
        volumeToRender = np.copy(self.DataList[self.comboBoxIR.currentIndex()])
        arrow = np.copy(self.ItemLists[self.comboBoxVF.currentIndex()-1]['Arrows']['Direction2'])

        minValue = np.min(volumeToRender)
        maxValue = np.max(volumeToRender)
        self.flag_mesh = bool(self.check_box_mesh.checkState())

        self.frame.init_all_VolumeRendering_component(self.flag_mesh)


        self.frame.add_arrow_field(arrow)
        self.frame.import_numpy_array(volumeToRender, minValue, maxValue)
        if self.flag_mesh:

            self.frame.MarchingCube(float(self.ThresholdMC.lineEdit.text()))

            if bool(self.check_smooth.checkState()):
                NbIter = int(self.SmoothIterNb.lineEdit.text())
                relaxF= float(self.SmoothRelaxF.lineEdit.text())
                self.frame.SmoothMesh(NbIter,relaxF)

        del volumeToRender

        shade = self.checkBox.checkState()
        ambient = self.sliderAmb.value()
        diffuse = self.sliderDif.value()
        specular = self.sliderSpe.value()
        specular_pw = self.sliderSpeP.value()
        opacity_unit_dist = self.sliderOpa.value()
        self.frame.reset_alpha_channel()
        self.frame.reset_color_channel()
        paraColor = np.zeros(6)
        paraColor[4] = 0.5
        paraColor[5] = 0.0
        for i in range(10):
            for j in range(6):
                try:
                    paraColor[j] = float(self.colorCoef.item(i,j).text())
                except:
                    if j == 4:
                        paraColor[j] = 0.5
                    else:
                        paraColor[j] = 0
            if paraColor[0] != 0 or paraColor[1] != 0:
                paraColor[0]  = ( (paraColor[0] - minValue)) / (maxValue - minValue)
                self.frame.set_color_channel(paraColor[0],paraColor[1], paraColor[2], paraColor[3],paraColor[4],
                                          paraColor[5])

        paraAlpha = np.zeros(4)
        paraAlpha[2] = 0.5
        paraAlpha[3] = 0.0
        for i in range(10):
            for j in range(4):
                try:
                    paraAlpha[j] = float(self.AlphaCoef.item(i,j).text())
                except:
                    if j == 4:
                        paraAlpha[j] = 0.5
                    else:
                        paraAlpha[j] = 0
            if paraAlpha[0] != 0 or paraAlpha[1] != 0:
                paraAlpha[0]  = ((paraAlpha[0] - minValue)) / (maxValue - minValue)
                self.frame.set_alpha_channel(paraAlpha[0],paraAlpha[1], paraAlpha[2], paraAlpha[3])

        self.frame.set_volume_property(shade, ambient, diffuse, specular, specular_pw, opacity_unit_dist)
        self.frame.update_mapper()


        if self.flag_mesh:
            self.frame.add_PolyActor()
        else:
            self.frame.add_volume_to_renderer()

        #self.frame.change_widget_size([2560, 1600])
        self.frame.update_renderer([0.1, 0.1, 0.1])
        #self.frame.show()
        self.frame.launch_render()


    def _snapshot(self):

        self.frame.take_multi_rotation_screen_shot(self.snapshotPath.textEdit, 1)

    def _multiSnapshot(self):
        self.frame.take_multi_rotation_screen_shot(self.snapshotPath.textEdit, 360)
