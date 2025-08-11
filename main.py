from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,                             
    QScrollArea, 
    QGridLayout, 
    QVBoxLayout, 
    QLabel,
    QFrame,
    QPushButton
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize, Signal, QProcess
from bson import ObjectId
import sys
from db.db import Database
from db.mongoDB import Database as MongoDB
# from datamatrix import DataMatrix
from utils import get_ip_address


class CustomListItem(QWidget):
    # Создаем сигнал, который будет испускаться при клике
    clicked = Signal()


    def __init__(self, 
                 name: str, 
                 image_path: str, 
                 art: str,
                 description: str = "", 
                 product_code: int = 1122,
                 children:list = []):
        super().__init__()
        
        self.setupUi()
      
        # загрузка изображения в label_image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.label_image.width(),
                self.label_image.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label_image.setPixmap(scaled_pixmap)
        
        self.label_title.setText(f"{name}")
        self.label_desc.setText(f"{description}")

        self.product_code = product_code
        self.ch = children
        self.art = art
        print(art)
     
    def setupUi(self):
        """
        Метод настройки внешнего вида CustomListItem
        """
        self.setObjectName("CustomListItem")
        self.setMinimumSize(QSize(280, 334)) 
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        
        self.label_image = QLabel(self)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setMinimumSize(QSize(271, 271))  
        self.verticalLayout.addWidget(self.label_image)
        
        self.label_title = QLabel(self)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.label_title.font()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setWordWrap(True)

        self.label_desc = QLabel(self)
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.label_desc.font()
        font.setPointSize(9)
        self.label_desc.setFont(font)
        self.label_desc.setWordWrap(True)
        
        self.verticalLayout.addWidget(self.label_title)        
        self.verticalLayout.addWidget(self.label_desc)        
        self.verticalLayout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit() 
        
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi()

        self.db = Database()
        self.mongoDB = MongoDB()
        self.mongoDB.insert_test_data()
        
        self.loadListFromMongoDb()
        
    def setupUi(self):
        """
        Метод настройки внешнего вида MainWindow
        """
        # self.setWindowFlags(Qt.FramelessWindowHint) # настройка, чтобы убрать шапку окна
        self.setWindowTitle("GUI")
        self.resize(600, 1024)
        
        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопка открытия настроек сети        
        button_network = QPushButton(self)
        button_network.setText("Открыть сетевые настройки")
        button_network.clicked.connect(self.onNetworkBtnClicked)
        main_layout.addWidget(button_network)
        
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Контейнер для содержимого
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        label_id = QLabel(self)
        label_id.setText(get_ip_address())
        label_id.setStyleSheet("color: gray;")
        main_layout.addWidget(label_id)
        
    def loadList(self):
        """
        загрузка данных на интерфейс из листа(не используется)
        """
        items_data = [
            {"image": "image.png", "title": "Item 1 with long text that should wrap properly"},
            {"image": "image.png", "title": "Item 2"},
            {"image": "image.png", "title": "Item 3"},
            {"image": "image.png", "title": "Item 4"},
            {"image": "image.png", "title": "Item 5"},
            {"image": "image.png", "title": "Item 6"},
            {"image": "image.png", "title": "Item 7"},
            {"image": "image.png", "title": "Item 8"},
            {"image": "image.png", "title": "Item 9"},
            {"image": "image.png", "title": "Item 10"},
        ]
        
        for i, item_data in enumerate(items_data):
            row = i // 2  # 2 колонки
            col = i % 2
            item = CustomListItem(item_data["title"], item_data["image"])
            self.grid_layout.addWidget(item, row, col, Qt.AlignmentFlag.AlignTop)
           
    def loadListFromDB(self):
        """
        загрузка данных на интерфейс из бд постгрес (не используется)
        """
        items = self.db.getData()
        i = 0
        for item in items:
            row = i // 2  
            col = i % 2
            custom_item = CustomListItem(str(item[1]), item[2])
            # Подключаем сигнал clicked к слоту
            custom_item.clicked.connect(lambda item=item: self.onItemClicked(item))
            self.grid_layout.addWidget(
                custom_item, 
                row, 
                col, 
                Qt.AlignmentFlag.AlignTop
            )
            i += 1
            
    def loadListFromMongoDb(self):
        items = self.mongoDB.get_firsts()
        # for item in items:
        #     print(item)
        self.setItemOnLayout(items)

        
    def setItemOnLayout(self, items: list[dict], product_code: int = 0):
        """
        Метод для добавления карточек
        """
        i = 0
        for item in items:
            row = i // 2  
            col = i % 2
            custom_item = CustomListItem(
                item.get("name"), 
                item.get("image_path"), 
                item.get("art"), # считаю, что артикуль уникальный для каждого
                item.get("description"),
                item.get("product_code") if item.get("product_code") else product_code,
                # item.get("children")
                )
            
            custom_item.clicked.connect(
                lambda item=custom_item: self.onItemClicked(item)
            )
            
            self.grid_layout.addWidget(
                custom_item, 
                row, 
                col, 
                Qt.AlignmentFlag.AlignTop
            )
            i += 1   
        
            
    def onNetworkBtnClicked(self):
        print("onNetworkBtnClicked")
        process = QProcess(self)
        
        # разные команды для разных дистрибутивов
        commands = [
            'nm-connection-editor',  # Стандартный редактор NetworkManager
            'gnome-control-center network',  # Для GNOME
            'kde5-nm-connection-editor',  # Для KDE Plasma
            'systemsettings5 kcm_networkmanagement',  # Альтернатива для KDE
            'xfce4-settings-manager -c network-settings'  # Для XFCE
        ]
        
        for cmd in commands:
            process.start(cmd.split()[0], cmd.split()[1:])
            if process.waitForStarted(1000):
                break
        else:
            print("Не удалось найти подходящий сетевой менеджер")  
            

    def onItemClicked(self, list_item: CustomListItem):
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        print(f"listItem.art {list_item.art}")
        item = self.mongoDB.get_by_art(list_item.art)
        
        children = item.get("children")
        # for child in ch:
        #     print(child)
        if children:
            # self.setItemOnLayout(self.mongoDB.get_by_art(item.art), item.product_code)
            self.setItemOnLayout(children, list_item.product_code)
        else:
            print("print!!!")
            print(f"{item.product_code}")
            
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())