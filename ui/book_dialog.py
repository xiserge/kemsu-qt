from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox, QFormLayout, QLineEdit, QPushButton, QDialog, QLabel

from database.db import get_book


class BookDialog(QDialog):
    def __init__(self, parent=None, book_id=None):
        super().__init__(parent)
        self.book_id = book_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Изменение книги')
        layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.author_input = QLineEdit(self)
        self.image_input = QLineEdit(self)

        self.btn_browse_image = QPushButton('Выбрать картинку', self)
        self.btn_browse_image.clicked.connect(self.browseImage)

        self.preview_label = QLabel(self)

        if self.book_id:
            book = get_book(self.book_id)

            self.title_input.setText(str(book[0]))
            self.author_input.setText(str(book[1]))
            self.image_preview(image_data=book[3])

        layout.addRow('Название:', self.title_input)
        layout.addRow('Автор:', self.author_input)
        layout.addRow('Картинка:', self.image_input)
        layout.addRow('', self.preview_label)
        layout.addWidget(self.btn_browse_image)

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
