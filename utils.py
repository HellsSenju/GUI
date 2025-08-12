import netifaces
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


def get_ip_address() -> str:
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == "lo":
            continue  # пропускаем loopback интерфейс
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                if "addr" in link:
                    return link["addr"]
    return "127.0.0.1"


def get_scaled_pixmap(width: int, height: int, image_path: str) -> QPixmap:
    """
    Метод возвращает QPixmap с нужным размером
    """
    pixmap = QPixmap(image_path)
    if not pixmap.isNull():
        return pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
