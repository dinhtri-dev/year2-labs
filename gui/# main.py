import os
from pathlib import Path
# main.py — Login: Left image | Right form with top icon (PySide6)
import sys
from pathlib import Path
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QGraphicsView, QGraphicsScene, QComboBox, QFrame
)

# ================== CONFIG (bạn tự đổi) ==================
# Ảnh nền cho panel bên TRÁI
LOGIN_IMAGE_PATH = str(Path(__file__).resolve().parent / 's__500_x_500_px_-removebg-preview.png')
# Icon (dùng cả trên tiêu đề cửa sổ và hiển thị ở đầu panel PHẢI)
ICON_PATH = str(Path(__file__).resolve().parent / 'if-06-harry-potter-colour-sorting-hat-2730319_88134.png')

# Ảnh cho MainWindow phía sau (không bắt buộc; giữ nguyên khung sẵn của bạn)
IMAGE_PATH = str(Path(__file__).resolve().parent / 'dark-hogwarts-castle-bo0tnj2x80cuaejl.jpg')

# ============== Tiện ích: QLabel giữ tỉ lệ ảnh =================
class ScaledImage(QLabel):
    def __init__(self, path: str | None = None, min_size=(360, 260)):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(*min_size)
        self._pix = None
        if path:
            self.set_image(path)

    def set_image(self, path: str):
        pm = QPixmap(path)
        if pm.isNull():
            self.setText("Không tải được ảnh")
            self._pix = None
        else:
            self._pix = pm
            self.setText("")
            self._update_scaled()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_scaled()

    def _update_scaled(self):
        if not self._pix:
            return
        scaled = self._pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled)

# ============== View có pan/zoom (giữ nguyên khung của bạn) ==============
class PanZoomView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHints(self.renderHints() |
                            QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

    def wheelEvent(self, e):
        factor = 1.15 if e.angleDelta().y() > 0 else 1/1.15
        self.scale(factor, factor)

# ================== MAIN WINDOW (không đổi logic) ==================
class MainWindow(QMainWindow):
    def __init__(self, image_path: str):
        super().__init__()
        self.setWindowTitle("Main")
        # đặt icon ứng dụng (khớp với icon login)
        if Path(ICON_PATH).exists():
            self.setWindowIcon(QIcon(ICON_PATH))

        self.scene = QGraphicsScene(self)
        pix = QPixmap(image_path)
        if not pix.isNull():
            self.scene.addPixmap(pix)
            self.scene.setSceneRect(0, 0, pix.width(), pix.height())
        else:
            self.scene.setSceneRect(0, 0, 1280, 720)

        self.view = PanZoomView()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        if not self.scene.itemsBoundingRect().isNull():
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

# ================== LOGIN DIALOG (layout mới) ==================
class LoginDialog(QDialog):
    """
    Layout:
    ┌───────────────────────────────────────────────────────┐
    │ [ẢNH TRÁI (tự nạp)]   |   [ICON]                     │
    │                       |   [Combo Vai trò]            │
    │                       |   [Tài khoản]                │
    │                       |   [Mật khẩu]                 │
    │                       |   [Nút Login]                │
    └───────────────────────────────────────────────────────┘
    """
    def __init__(self, image_path: str | None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập")
        self.setModal(True)
        self.resize(1000, 560)

        # --- đặt icon cửa sổ + dùng lại để hiển thị ở đầu panel phải ---
        self.icon = None
        if Path(ICON_PATH).exists():
            self.icon = QIcon(ICON_PATH)
            self.setWindowIcon(self.icon)

        # ========== Panel TRÁI: ẢNH ==========
        self.leftImage = ScaledImage(image_path, min_size=(420, 320))
        self.leftImage.setStyleSheet("background:#492615; border-radius:12px;")  # nhẹ kiểu ảnh minh hoạ

        # ========== Panel PHẢI: Form + Icon ==========
        right = QWidget()
        rLay = QVBoxLayout(right)
        rLay.setContentsMargins(32, 16, 32, 24)
        rLay.setSpacing(12)

        # Icon preview ở trên
        self.iconLabel = QLabel()
        self.iconLabel.setAlignment(Qt.AlignCenter)
        self.iconLabel.setFixedHeight(120)
        if self.icon:
            self.iconLabel.setPixmap(self.icon.pixmap(QSize(96, 96)))
        rLay.addWidget(self.iconLabel)

        # Combo (giống “Mời chọn” trong ảnh)
        self.role = QComboBox()
        self.role.addItems(["Mời chọn", "Admin", "User", "Guest"])
        self.role.setMinimumHeight(36)
        rLay.addWidget(self.role)

        # Tài khoản & Mật khẩu (giữ vì đây là khung xương dùng lâu dài)
        self.user_edit = QLineEdit()
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Tài khoản:", self.user_edit)
        form.addRow("Mật khẩu:", self.pass_edit)
        rLay.addLayout(form)

        # Nút Login (style nâu như mẫu)
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B4B3A;
                color: #fff;
                border: 0px;
                border-bottom: 4px solid #4b2e22;
                font-weight: 800;
                font-size: 18px;
                padding: 8px 16px;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #8A5441; }
            QPushButton:pressed { border-bottom: 0; margin-top: 4px; }
        """)
        rLay.addSpacing(8)
        rLay.addWidget(self.login_btn)

        rLay.addStretch(1)

        # ========== Ghép TRÁI | PHẢI ==========
        split = QHBoxLayout(self)
        split.setContentsMargins(16, 16, 16, 16)
        split.setSpacing(24)

        # khung trái có bo góc và nền nhẹ
        leftWrap = QWidget()
        lwLay = QVBoxLayout(leftWrap)
        lwLay.setContentsMargins(12, 12, 12, 12)
        lwLay.addWidget(self.leftImage)
        leftWrap.setFixedWidth(520)

        # vạch ngăn mảnh
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)

        split.addWidget(leftWrap, 0)
        split.addWidget(vline)
        split.addWidget(right, 1)

        # ===== Signals =====
        self.login_btn.clicked.connect(self.try_login)
        self.user_edit.returnPressed.connect(self.try_login)
        self.pass_edit.returnPressed.connect(self.try_login)

    def try_login(self):
        # Demo rule: phải chọn vai trò khác "Mời chọn" + nhập user/pass
        if self.role.currentIndex() == 0:
            QMessageBox.information(self, "Chưa chọn vai trò", "Hãy chọn vai trò trước khi đăng nhập.")
            return
        u = self.user_edit.text().strip()
        p = self.pass_edit.text()
        if not u or not p:
            QMessageBox.information(self, "Thiếu thông tin", "Nhập tài khoản và mật khẩu.")
            return

        # Tùy bạn thay bằng xác thực thực tế sau này
        if u == "1" and p == "1":
            self.accept()
        else:
            QMessageBox.warning(self, "Sai thông tin", "Tài khoản hoặc mật khẩu chưa đúng.")

# ================== APP ENTRY ==================
def main():
    app = QApplication.instance() or QApplication(sys.argv)

    # Nếu muốn theme tối -> bỏ comment 2 dòng dưới (layout hiện tại thiết kế nền sáng):
    # import qdarkstyle
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    # đặt icon app cấp toàn cục
    if Path(ICON_PATH).exists():
        app.setWindowIcon(QIcon(ICON_PATH))

    # Bước 1: Login (TRÁI ảnh, PHẢI form + icon)
    login = LoginDialog(LOGIN_IMAGE_PATH)
    if login.exec() == QDialog.Accepted:
        # Bước 2: vào MainWindow (giữ khung pan/zoom của bạn)
        w = MainWindow(IMAGE_PATH)
        w.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
