from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox, QFormLayout, QDialog


class DeleteConfirmDialog(QDialog):
    def __init__(self, parent=None, book_id=None):
        super().__init__(parent)
        self.book_id = book_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Подтверждение удаления книги')
        layout = QFormLayout()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setAcceptDrops(True)

        self.setLayout(layout)

    def browseImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выбери картинку', '', 'Images (*.png *.jpg *.bmp *.jpeg)')
        if file_path:
            self.image_input.setText(file_path)
            self.image_preview(file_path=file_path)

    def getBookData(self):
        return self.title_input.text(), self.author_input.text(), self.image_input.text()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.image_input.setText(file_path)
            self.image_preview(file_path=file_path)

    def image_preview(self, file_path=None, image_data=None):
        pixmap = QPixmap()
        if file_path:
            pixmap.load(file_path)
        if image_data:
            pixmap.loadFromData(image_data)
        if not pixmap.isNull():
            self.preview_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            self.preview_label.show()
        else:
            self.preview_label.hide()
