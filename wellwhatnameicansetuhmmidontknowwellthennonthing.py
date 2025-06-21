import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint, QRectF, QTimer
from PyQt5.QtGui import QPainter, QColor, QCursor, QPixmap, QIcon, QRegion, QPainterPath


class FramelessWindow(QWidget):
    def __init__(self, contents="Welcome to the Frameless Window!"):
        super().__init__()
        self.content = contents
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 320)

        # Load logo pixmap
        self.logo = QPixmap("1.png")  # Make sure this file exists!

        # Set app icon from logo
        self.setWindowIcon(QIcon(self.logo))

        # Close button (top-right)
        self.close_btn = QPushButton("X", self)
        self.close_btn.setStyleSheet("""
            background-color: transparent;
            color: white;
            border: none;
            font-weight: bold;
            font-size: 18px;
        """)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)

        # Logo label (top-left)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(self.logo.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setGeometry(10, 10, 40, 40)

        # Text label (centered)
        self.label = QLabel(self.content, self)
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.label.setWordWrap(True)
        self.label.resize(400, 100)

        # Movement & resizing setup
        self.old_pos = None
        self.resizing = False
        self.resize_margin = 10
        self.resize_dir = None

        self.setMouseTracking(True)
        self.update_mask()

    def setContent(self, new_content: str):
        self.content = new_content
        if hasattr(self, 'label') and self.label:
            self.label.setText(self.content)
            self.label.adjustSize()
            # reposition after content update
            self.label.move(self.width() // 2 - self.label.width() // 2,
                            self.logo_label.y() + self.logo_label.height() + 10)

    def update_mask(self):
        radius = 20
        rect = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(30, 30, 30, 220))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def resizeEvent(self, event):
        self.update_mask()
        self.close_btn.move(self.width() - 40, 10)
        self.logo_label.move(10, 10)
        self.label.move((self.width() - self.label.width()) // 2, self.logo_label.y() + self.logo_label.height() + 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            w, h = self.width(), self.height()
            m = self.resize_margin

            # Detect edges/corners
            left, right = pos.x() <= m, pos.x() >= w - m
            top, bottom = pos.y() <= m, pos.y() >= h - m
            self.resize_dir = (
                "top_left" if left and top else
                "top_right" if right and top else
                "bottom_left" if left and bottom else
                "bottom_right" if right and bottom else
                "left" if left else
                "right" if right else
                "top" if top else
                "bottom" if bottom else None
            )

            self.resizing = self.resize_dir is not None
            self.old_pos = event.globalPos()
            self.old_geo = self.geometry()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        w, h = self.width(), self.height()
        m = self.resize_margin

        if self.resizing:
            delta = event.globalPos() - self.old_pos
            geo = self.old_geo
            x, y, width, height = geo.x(), geo.y(), geo.width(), geo.height()
            dx, dy = delta.x(), delta.y()

            if self.resize_dir == "top_left":
                self.setGeometry(x + dx, y + dy, width - dx, height - dy)
            elif self.resize_dir == "top_right":
                self.setGeometry(x, y + dy, width + dx, height - dy)
            elif self.resize_dir == "bottom_left":
                self.setGeometry(x + dx, y, width - dx, height + dy)
            elif self.resize_dir == "bottom_right":
                self.resize(width + dx, height + dy)
            elif self.resize_dir == "left":
                self.setGeometry(x + dx, y, width - dx, height)
            elif self.resize_dir == "right":
                self.resize(width + dx, height)
            elif self.resize_dir == "top":
                self.setGeometry(x, y + dy, width, height - dy)
            elif self.resize_dir == "bottom":
                self.resize(width, height + dy)

        else:
            left, right = pos.x() <= m, pos.x() >= w - m
            top, bottom = pos.y() <= m, pos.y() >= h - m
            if left and top or right and bottom:
                self.setCursor(QCursor(Qt.SizeFDiagCursor))
            elif right and top or left and bottom:
                self.setCursor(QCursor(Qt.SizeBDiagCursor))
            elif left or right:
                self.setCursor(QCursor(Qt.SizeHorCursor))
            elif top or bottom:
                self.setCursor(QCursor(Qt.SizeVerCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

            if event.buttons() == Qt.LeftButton and not self.resizing:
                delta = event.globalPos() - self.old_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resize_dir = None


# You can update this content dynamically later
con = "Welcome to the Frameless Window!\n\nThis is a custom frameless window with rounded corners and a logo."

def main():
    app = QApplication(sys.argv)
    window = FramelessWindow(contents=con)
    window.show()

    # Set new content after 5 seconds (5000 ms)
    QTimer.singleShot(5000, lambda: window.setContent(
        "This content can be updated dynamically!\n\nYou can change it at any time.")
    )

    return app, window

if __name__ == '__main__':
    app, window = main()
    sys.exit(app.exec_())
