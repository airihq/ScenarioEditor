# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:13:27 2018

@author: AIRI
"""
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore

import sqlite3
import sys
import os.path
import csv
import numpy as np
import ScenarioEditor_options as opt
import json

form_class = uic.loadUiType("./ScenarioEditor.ui")[0]
scenario_DB_path = opt.scenario_DB_path
output_dir = opt.output_dir

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setUI()
        
        # Load DB File
        self.con = sqlite3.connect(scenario_DB_path)
        self.cursor = self.con.cursor()

        # Init Buttons
        self.LoadButton.clicked.connect(self.click_load)
        self.ExitButton.clicked.connect(QCoreApplication.instance().quit)
        self.ExportButton.clicked.connect(self.click_export)
        
        # Event of Left ListWidget
        self.LeftList.itemClicked.connect(self.click_LeftListWidget)
        self.RightList.itemChanged.connect(self.check_RightListWidget)
        # self.RightList.currentRowChanged.connect(self.dragdrop_RightListWidget)

        # init category dict
        self.category_dict = {}
        self.current_category = None

        # self.RightList.dropEvent = self.override_
        
    def setUI(self):
        self.setupUi(self)

    # def dragdrop_RightListWidget(self):
        # print(self.RightList.mimeData())
        # # self.current_category = self.LeftList.currentItem().text()
        # current_dict = self.category_dict[self.current_category]

    def click_load(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        category_list = self.cursor.fetchall()
        category_list = np.array(category_list)[:, 0] # trim 
        
        # init category dict
        for category in category_list:
            # select FileName List
            self.cursor.execute("select FileName from " + category)    
            select_FileName = self.cursor.fetchall()
            select_FileName = np.array(select_FileName)[:, 0]
            
            # select Text List
            self.cursor.execute("select Text from " + category)    
            select_Text = self.cursor.fetchall()
            select_Text = np.array(select_Text)[:, 0]

            # init Check List
            check_list = np.ones(len(select_Text)) * 2 # 2 - checked, 0 - unchecked

            # append category dict
            self.category_dict[category] = {'FileName':select_FileName, 'Text':select_Text, 'Check':check_list}

        # set Left List Widget 
        for i_c, category in enumerate(category_list):
            item = QListWidgetItem(category)
            item.setCheckState(QtCore.Qt.Checked)
            self.LeftList.addItem(item)

        print('Load DB File Complete')
        
    def click_LeftListWidget(self):
        if self.LeftList.currentItem() == None:
            # print('currentItem is None')
            return

        self.current_category = self.LeftList.currentItem().text()
        current_dict = self.category_dict[self.current_category]

        # set right List Widget 
        self.RightList.clear()
        for i_t, text in enumerate(current_dict['Text']):
            item = QListWidgetItem(text)
            if current_dict['Check'][i_t] == 2:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            self.RightList.addItem(item)

    def check_RightListWidget(self, item):
        # chanage Check value in category_dict
        current_row = self.RightList.row(item)
        current_state = item.checkState()
        self.category_dict[self.current_category]['Check'][current_row] = current_state
        # print(self.category_dict[self.current_category]['Check'])

    def click_export(self):
        export_dict = {}
        actionScript_obj = []
        category_obj = []

        # set Categories and ActionScript obj
        for i_list in range(self.LeftList.count()):
            # init 
            dummy_actionScript = {'Name':[], 'Category':''}
            
            # if category item is checked, append checked scripts
            current_category = self.LeftList.item(i_list)
            if current_category.checkState() == 2:
                # set actionScript element
                current_scripts = self.category_dict[current_category.text()]
                selected_scripts = current_scripts['FileName'][current_scripts['Check'] == 2].tolist()
                dummy_actionScript['Name'] = selected_scripts
                dummy_actionScript['Category'] = current_category.text()
                
                # append actionScript element
                actionScript_obj.append(dummy_actionScript)

                # append category_obj element
                category_obj.append(current_category.text())

        export_dict['Categories'] = category_obj
        export_dict['ActionScript'] = actionScript_obj

        # set PlayMode and Layout obj
        if self.DefaultMode_RadioButton.isChecked():
            export_dict['PlayMode'] = 'Interactive'
        else:
            export_dict['PlayMode'] = 'Video'

        if self.VerticalMode_RadioButton.isChecked():
            export_dict['Layout'] = 'Vertical'
        else:
            export_dict['Layout'] = 'Horizontal'

        # print(export_dict)
        with open(output_dir + "/meta.json", "w", encoding='utf-8') as json_file:
            json.dump(export_dict, json_file, ensure_ascii=False)

        print('Export json Complete')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.setWindowTitle('Motion Data Generator')
    myWindow.show()
    app.exec_()
    