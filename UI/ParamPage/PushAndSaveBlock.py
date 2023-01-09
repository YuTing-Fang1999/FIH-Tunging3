from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox
)
from PyQt5.QtCore import QThread, pyqtSignal
import xml.etree.ElementTree as ET
from time import sleep
import os
import shutil

from myPackage.func import mkdir

class CaptureWorker(QThread):
    set_btn_enable_signal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.saved_path = "./"
        self.capture = None

    def run(self):
        self.set_btn_enable_signal.emit(False)
        self.capture.capture(path=self.saved_path)
        self.set_btn_enable_signal.emit(True)

class PushWorker(QThread):
    set_btn_enable_signal = pyqtSignal(bool)
    capture_signal = pyqtSignal()
    push_to_camera_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.is_capture = False

    def run(self):
        self.set_btn_enable_signal.emit(False)
        self.push_to_camera_signal.emit()
        for i in range(10):
            print(i)
            sleep(1)
        if self.is_capture:
            self.capture_signal.emit()
        else:
            self.set_btn_enable_signal.emit(True)

class PushAndSaveBlock(QWidget):
    alert_info_signal = pyqtSignal(str, str)
    get_and_set_param_value_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_UI()
        self.setup_controller()
        

    def setup_UI(self):
        self.push_worker = PushWorker()
        self.capture_worker = CaptureWorker()

        VLayout = QVBoxLayout(self)

        title_wraper = QHBoxLayout()
        label_title = QLabel("Push and Save")
        label_title.setStyleSheet("background-color:rgb(72, 72, 72);")
        title_wraper.addWidget(label_title)
        VLayout.addLayout(title_wraper)

        gridLayout = QGridLayout()

        label = QLabel("資料夾名稱")
        label.setToolTip("要存入的資料夾名稱")
        gridLayout.addWidget(label, 0, 0)

        self.lineEdits_dir_name = QLineEdit()
        gridLayout.addWidget(self.lineEdits_dir_name, 0, 1)

        label = QLabel("圖片檔名")
        label.setToolTip("要存入的圖片檔名")
        gridLayout.addWidget(label, 1, 0)

        self.lineEdits_img_name = QLineEdit()
        gridLayout.addWidget(self.lineEdits_img_name, 1, 1)

        VLayout.addLayout(gridLayout)

        self.btn_set_to_xml = QPushButton("寫入")
        VLayout.addWidget(self.btn_set_to_xml)

        self.btn_push_phone = QPushButton("推到手機")
        VLayout.addWidget(self.btn_push_phone)

        self.btn_capture = QPushButton("拍照")
        VLayout.addWidget(self.btn_capture)

        self.btn_push_phone_capture = QPushButton("寫入 + 推到手機 + 拍照")
        VLayout.addWidget(self.btn_push_phone_capture)
        

    def setup_controller(self):
        self.btn_set_to_xml.clicked.connect(self.get_and_set_param_value_signal.emit)
        self.btn_push_phone.clicked.connect(lambda: self.push_phone(is_capture=False, is_set_to_xml=False))
        self.btn_push_phone_capture.clicked.connect(lambda: self.push_phone(is_capture=True, is_set_to_xml=True))
        self.btn_capture.clicked.connect(self.do_capture)
        self.push_worker.capture_signal.connect(self.capture_worker.start)
        self.push_worker.set_btn_enable_signal.connect(self.btn_enable)
        self.capture_worker.set_btn_enable_signal.connect(self.btn_enable)

    def set_data(self):
        dir_name = self.lineEdits_dir_name.text()
        img_name = self.lineEdits_img_name.text()

        if dir_name=="": dir_name="."
        mkdir(dir_name)

        self.capture_worker.saved_path = "{}/{}".format(dir_name, img_name)

    # def set_to_xml(self):
    #     param_value = self.ui.parameter_setting_page.param_modify_block.get_param_value()

    #     config = self.config[self.data["page_root"]][self.data["page_key"]]
    #     block_data = self.data[self.data["page_root"]][self.data["page_key"]]
        
    #     # param
    #     self.tuning.platform = self.data["platform"]
    #     # config
    #     self.tuning.rule = config["rule"]
    #     self.tuning.xml_node = config["xml_node"]
    #     self.tuning.expand = config["expand"]
    #     self.tuning.data_node = config["data_node"]

    #     self.tuning.xml_path = self.data['xml_path']+config["file_path"]
    #     self.trigger_selector.set_data()
    #     self.tuning.trigger_idx = self.data["trigger_idx"]
    #     self.tuning.param_names = config['param_names']
    #     self.tuning.key = self.data["page_key"]

    #     self.logger.signal.emit('set {} trigger_idx={} param to xml {}, '.format(self.data["page_key"], self.tuning.trigger_idx, config["file_path"]))
    #     self.tuning.setParamToXML(param_value)

    def push_phone(self, is_capture, is_set_to_xml):
        if is_capture:
            self.set_data()
            path = self.capture_worker.saved_path
            if os.path.exists(path+".jpg"):
                self.alert_info_signal.emit("檔名重複", "檔名\n"+path+".jpg\n已存在，請重新命名")
                return
        if is_set_to_xml:
            self.get_and_set_param_value_signal.emit()

        self.push_worker.is_capture = is_capture
        self.push_worker.start()

    def btn_enable(self, b):
        self.btn_set_to_xml.setEnabled(b)
        self.btn_capture.setEnabled(b)
        self.btn_push_phone.setEnabled(b)
        self.btn_push_phone_capture.setEnabled(b)

    def do_capture(self):
        print("PushAndSaveBlock do_capture")
        self.set_data()
        path = self.capture_worker.saved_path
        if os.path.exists(path+".jpg"):
            self.alert_info_signal.emit("檔名重複", "檔名\n"+path+".jpg\n已存在，請重新命名")
            return
        self.capture_worker.start()
        # self.ui.capture.capture(path=path, focus_time = 3, save_time = 0.5, capture_num = 1)


