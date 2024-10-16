import os
import sys

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread
from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtWidgets import (QGridLayout, QPushButton, QWidget, QApplication, QLabel, QSpinBox, QListWidget,
                               QListWidgetItem, QFileDialog, QMessageBox, QProgressBar)
from functools import lru_cache

from api_pdf import ConvertImage


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Worker(QtCore.QObject):
    image_converted = QtCore.Signal(object, bool)
    finished = QtCore.Signal()

    def __init__(self, image_to_convert, images_path_to_convert, size, new_folder_path):
        super().__init__()
        self.image_to_convert = image_to_convert
        self.images_path_to_convert = images_path_to_convert
        self.size = size
        self.new_folder_path = new_folder_path

    def convert_images(self):
        for index, image_lw_item in enumerate(self.image_to_convert):
            if not image_lw_item.processed:
                image_path = self.images_path_to_convert[index]
                image = ConvertImage(path=image_path, folder_path=self.new_folder_path)
                succes = image.save_image(upscale_factor=self.size)
                self.image_converted.emit(image_lw_item, succes)

        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Img to PDF")
        self.resize(350, 450)
        self.setup_ui()

        icon_path = resource_path("./_img/icon.png")
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.modify()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_layouts(self):
        self.main_layout = QGridLayout(self)

    def create_widgets(self):
        self.lbl_fileOK = QLabel()
        self.lw_files = QListWidget()
        self.lbl_placeholder = QLabel("Drag and drop your files here")
        self.lbl_size = QLabel("Modify Size (%):")
        self.spn_size = QSpinBox()
        self.btn_convert = QPushButton("Convert to PDF")
        self.prg_bar = QProgressBar()

    def modify(self):
        # StyleSheet
        self.lbl_fileOK.setStyleSheet(f"""
                font-family: cursive;
                font-size: 12px;
                font-weight: bold;
            """)

        self.lw_files.setStyleSheet(f"""
                QListWidget{{
                    background: rgb(250, 250, 250);
                    
                    border: 2px solid rgb(248, 138, 94);
                    border-radius: 10px;
                    padding: 0.5em;
                    
                    font-size: 12px;
                    font-weight: bold;
                    }}
                    
                QListWidget::item {{
                    padding: 2px;
                    }}
                    
                QListWidget::item:hover {{
                    background: rgb(251, 235, 210);
                    border-radius: 5px;
                    }}
                
                QListView::item:selected {{
                    color: black;
                    border-radius: 5px;
                    background : rgb(251, 235, 210);
                    }}
            """)

        self.lbl_placeholder.setStyleSheet(f"""
                font-family: cursive;
                font-size: 16px;
            """)

        self.lbl_size.setStyleSheet(f"""
                font-family: cursive;
                font-size: 12px;
                font-weight: bold;
            """)

        self.spn_size.setStyleSheet(f"""
                QSpinBox {{
                    font-size: 13px;
                    font-weight: bold;
                }}
                
                QSpinBox::down-button{{
                    subcontrol-position: top left; 
                    height: 20;
                    width: 25;
                }}
                QSpinBox::up-button{{
                    subcontrol-position: top right; 
                    height: 20;
                    width: 25;
                }}
            """)

        self.btn_convert.setStyleSheet(f"""
            QPushButton {{     
                        background: rgb(250, 250, 250);
                                   
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: rgb(248, 138, 94);
                        
                        font-size: 15px;
                        font-weight: bold;
                    }}
            QPushButton:pressed {{
                                background-color: rgb(248, 138, 94);
                                border-style: inset;
                                border-width: 0px;
                            }}
            """)

        self.prg_bar.setStyleSheet(f"""
                QProgressBar {{
                    font-size: 15px;
                    font-weight: bold;
                    border: 2px solid rgb(29, 150, 162);
                    border-radius: 10px;
                }}
                
                QProgressBar::chunk {{
                    background-color: #1FE6C0;
                    width: 15px;
                    border-radius: 5px;
                    text-align: center;
                    margin: 0.5px;
                }}
            """)

        # Alignment
        self.lbl_fileOK.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_size.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spn_size.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.prg_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Range
        self.spn_size.setRange(50, 150)
        self.spn_size.setValue(100)

        # Others
        self.lbl_fileOK.setText('Supported file types are<br> '
                                '<span style="color: #F4561D;">.png</span> / '
                                '<span style="color: #F4561D;">.jpg</span> / '
                                '<span style="color: #F4561D;">.bmp</span>')
        self.prg_bar.setVisible(False)
        self.lw_files.setSelectionMode(QListWidget.ExtendedSelection)
        self.lw_files.setAlternatingRowColors(True)
        self.setAcceptDrops(True)
        self.update_placeholder()

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_fileOK, 0, 0, 1, 2)
        self.main_layout.addWidget(self.lw_files, 1, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_placeholder, 1, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_size, 3, 0, 1, 1)
        self.main_layout.addWidget(self.spn_size, 3, 1, 1, 1)
        self.main_layout.addWidget(self.btn_convert, 4, 0, 1, 2)
        self.main_layout.addWidget(self.prg_bar, 5, 0, 1, 2)

    def setup_connections(self):
        self.btn_convert.clicked.connect(self.convert_image)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Delete), self.lw_files, self.delete_selected_items)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Backspace), self.lw_files, self.delete_selected_items)

    ###############################################################
    def convert_image(self):
        size = self.spn_size.value() / 100.0
        dialog = QFileDialog()
        new_folder_path = dialog.getExistingDirectory(None, "Select the folder where the image will be saved")

        lw_items = []
        file_urls = []
        for index in range(self.lw_files.count()):
            item_index = self.lw_files.item(index)
            lw_items.append(item_index)
            file_url = item_index.data(QtCore.Qt.ItemDataRole.UserRole)
            file_urls.append(file_url)

        image_to_convert = []
        for lw_item in lw_items:
            if not lw_item.processed:
                image_to_convert.append(1)

        if not image_to_convert:
            msg_box = QMessageBox.warning(None, "Info", "All images have already been converted")
            msg_box.exec_()
            return False

        self.thread = QThread(self)
        self.worker = Worker(image_to_convert=lw_items,
                             images_path_to_convert=file_urls,
                             size=size,
                             new_folder_path=new_folder_path)

        self.worker.moveToThread(self.thread)
        self.worker.image_converted.connect(self.image_converted)
        self.thread.started.connect(self.worker.convert_images)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

        self.prg_bar.setVisible(True)
        self.prg_bar.setRange(1, len(image_to_convert))
        self.prg_bar.show()

    def image_converted(self, lw_item, success):
        if success:
            lw_item.setIcon(self.img_checked())
            lw_item.processed = True
            self.prg_bar.setValue(self.prg_bar.value() + 1)

    def delete_selected_items(self):
        for lw_item in self.lw_files.selectedItems():
            row = self.lw_files.row(lw_item)
            self.lw_files.takeItem(row)

        if self.lw_files.count() == 0:
            self.prg_bar.reset()
            self.prg_bar.setVisible(False)

        self.update_placeholder()

    def add_file(self, url_name, url_file):
        items = []
        for index in range(self.lw_files.count()):
            item_text = self.lw_files.item(index).text()
            items.append(item_text)

        if url_name not in items:
            lw_item = QListWidgetItem(url_name)
            lw_item.setIcon(self.img_unchecked())
            lw_item.processed = False
            lw_item.setData(QtCore.Qt.ItemDataRole.UserRole, url_file)
            self.lw_files.addItem(lw_item)

        self.update_placeholder()

    def update_placeholder(self):
        if self.lw_files.count() == 0:
            self.lbl_placeholder.setVisible(True)
        else:
            self.lbl_placeholder.setVisible(False)

    ###############################################################
    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        pass

    def enterEvent(self, event):
        event.accept()

    def leaveEvent(self, event):
        pass

    def dropEvent(self, event):
        event.accept()

        for url in event.mimeData().urls():
            file_url = url.toLocalFile()
            file_name = url.toLocalFile().split("/")[-1]
            self.add_file(url_name=file_name, url_file=file_url)

    ###############################################################

    @lru_cache(maxsize=2)
    def img_checked(self):
        return QtGui.QIcon(resource_path("_img/checked.png"))

    @lru_cache(maxsize=2)
    def img_unchecked(self):
        return QtGui.QIcon(resource_path("_img/unchecked.png"))


app = QApplication()
win = MainWindow()
win.show()
app.exec()
