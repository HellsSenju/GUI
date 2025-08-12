from datetime import datetime
from typing import Optional
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize, Signal, QProcess
from datamatrix import DataMatrix
import sys
from db.db import Database
from db.mongoDB import Database as MongoDB
from utils import get_scaled_pixmap

# from datamatrix import DataMatrix
from utils import get_ip_address


class CustomListItem(QWidget):
    # Создаем сигнал, который будет испускаться при клике
    clicked = Signal()

    def __init__(
        self,
        name: str,
        image_path: str,
        description: str,
        type: int,
        product_code: int,
        place: int,
        children: Optional[list],
        art: str,
    ):
        super().__init__()

        self.setupUi()

        self.label_image.setPixmap(
            get_scaled_pixmap(
                self.label_image.width(), self.label_image.height(), image_path
            )
        )

        self.label_title.setText(f"{name}")
        self.label_desc.setText(f"{description}")

        self.type = type
        self.product_code = product_code
        self.place = place
        self.chldrn = children
        self.art = art

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

        self.db = Database()
        self.mongoDB = MongoDB()
        self.mongoDB.insert_test_data()

        self.setupUi()

        # self.loadListFromMongoDb()

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
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопка переключения
        # self.toggle_button = QPushButton("Открыть сетевые настройки")
        # self.toggle_button.clicked.connect(self.toggle_view)
        # self.main_layout.addWidget(self.toggle_button)

        button_network = QPushButton(self)
        button_network.setText("Открыть сетевые настройки")
        button_network.clicked.connect(self.onNetworkBtnClicked)
        self.main_layout.addWidget(button_network)

        # Создаем Scroll Area (изначально видима)
        self.create_scroll_area()

        # Создаем элементы для режима изображения (изначально скрыты)
        self.image_widget = QWidget()
        layout = QVBoxLayout(self.image_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_datamatrix = QLabel()
        self.label_datamatrix.setAlignment(Qt.AlignCenter)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.showScrollArea)

        layout.addStretch(1)
        layout.addWidget(self.label_datamatrix, 0, Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.back_button, 0, Qt.AlignCenter)
        layout.addStretch(1)

        # Изначальное состояние
        self.showScrollArea()

        # ID label
        self.label_id = QLabel("IP: " + get_ip_address())
        self.label_id.setStyleSheet("color: gray;")
        self.main_layout.addWidget(self.label_id)

    def create_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setAlignment(Qt.AlignTop)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)

        self.scroll_area.setWidget(content_widget)

    def setDatamatrix(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.label_datamatrix.setPixmap(
            pixmap.scaledToWidth(400, Qt.SmoothTransformation)
        )

    def showScrollArea(self):
        self.scroll_area.show()
        self.image_widget.hide()
        # self.toggle_button.setText("Открыть сетевые настройки")
        self.main_layout.insertWidget(1, self.scroll_area)
        self.loadListFromMongoDb()

    def showDatamatrix(self):
        self.scroll_area.hide()
        self.image_widget.show()
        # self.toggle_button.setText("Скрыть сетевые настройки")
        self.main_layout.insertWidget(1, self.image_widget)

    def loadList(self):
        """
        загрузка данных на интерфейс из листа(не используется)
        """
        items_data = [
            {
                "image": "image.png",
                "title": "Item 1 with long text that should wrap properly",
            },
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
            self.grid_layout.addWidget(custom_item, row, col, Qt.AlignmentFlag.AlignTop)
            i += 1

    def loadListFromMongoDb(self):
        # items = self.mongoDB.get_firsts()
        items = self.mongoDB.get_all()
        self.setItemOnLayout(items)

    def setItemOnLayout(
        self, items: list[dict], type: int = 0, product_code: int = 0, place: int = 0
    ):
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
                item.get("description"),
                item.get("type") if item.get("type") else type,
                item.get("product_code") if item.get("product_code") else product_code,
                item.get("place") if item.get("place") else place,
                item.get("children") if item.get("children") else None,
                item.get("art"),
            )

            custom_item.clicked.connect(
                lambda item=custom_item: self.onItemClicked(item)
            )

            self.grid_layout.addWidget(custom_item, row, col, Qt.AlignmentFlag.AlignTop)
            i += 1

    def onNetworkBtnClicked(self):
        print("onNetworkBtnClicked")
        process = QProcess(self)

        # разные команды для разных дистрибутивов
        commands = [
            "nm-connection-editor",  # Стандартный редактор NetworkManager
            "gnome-control-center network",  # Для GNOME
            "kde5-nm-connection-editor",  # Для KDE Plasma
            "systemsettings5 kcm_networkmanagement",  # Альтернатива для KDE
            "xfce4-settings-manager -c network-settings",  # Для XFCE
        ]

        for cmd in commands:
            process.start(cmd.split()[0], cmd.split()[1:])
            if process.waitForStarted(1000):
                break
        else:
            print("Не удалось найти подходящий сетевой менеджер")

    def onItemClicked(self, item: CustomListItem):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if item.chldrn:
            self.setItemOnLayout(
                item.chldrn,
                item.type,
                item.product_code,
                item.place,
            )
        else:
            print("print!!!")
            year = str(datetime.now().year)
            month = str(datetime.now().month)
            serial_pattern = "%06d"

            serial = serial_pattern % 878

            all_datamatrix_code = (
                str(item.product_code)
                + item.art
                + str(item.place)
                + year
                + month
                + serial
            )
            dm = DataMatrix(
                msg=all_datamatrix_code,
                pixel_size=50,
                left_offset=200,
                down_offset=140,
            )

            image_path = f"dm/{all_datamatrix_code}.png"
            dm.drone_datamatrix(image_path, all_datamatrix_code)
            print(all_datamatrix_code, f"complete {878 + 1}/1000")

            self.setDatamatrix(image_path)
            self.showDatamatrix()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
