import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

from database.db import create_db, update_book, get_books, add_book_with_image, remove_book
from settings import save_settings, load_settings
from ui.book_dialog import BookDialog


class LibrarySystem(QWidget):
    def __init__(self):
        super().__init__()
        create_db()
        self.initUI()
        self.showBooks()

    def initUI(self):
        self.setWindowTitle('Библиотечная система')
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget(self)
        layout.addWidget(self.tableWidget)

        self.btn_add_book = QPushButton('Добавить книгу', self)
        self.btn_add_book.clicked.connect(self.openAddBookDialog)
        layout.addWidget(self.btn_add_book)

        self.btn_edit_book = QPushButton('Редактировать книгу', self)
        self.btn_edit_book.clicked.connect(self.openEditBookDialog)
        layout.addWidget(self.btn_edit_book)

        self.loadSettings()

        self.setLayout(layout)
        self.show()

    def showBooks(self):
        books = get_books()
        self.tableWidget.setRowCount(len(books))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Автор', 'Изображение', 'Удаление'])

        for row, book in enumerate(books):
            for i in range(3):
                self.tableWidget.setItem(row, i, QTableWidgetItem(str(book[i])))
                self.tableWidget.item(row, i).setFlags(self.tableWidget.item(row, i).flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(book[i])))

            image_item = QTableWidgetItem()
            if book[3]:  # Если есть бинарные данные изображения
                image_data = book[3]
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                icon = QIcon(pixmap)
                image_item.setIcon(icon)
            self.tableWidget.setItem(row, 3, image_item)  # Image
            # Кнопка удаления
            delete_button = QPushButton('Удалить')
            delete_button.clicked.connect(
                lambda checked, row=row: self.deleteBook(row))  # Связываем с функцией удаления
            self.tableWidget.setCellWidget(row, 4, delete_button)  # Размещаем кнопку в последней колонке

    def openAddBookDialog(self):
        dialog = BookDialog(self)
        if dialog.exec_():
            title, author, image_path = dialog.getBookData()
            add_book_with_image(title, author, image_path)
            self.showBooks()  # Refresh the book list after adding

    def openEditBookDialog(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            book_id = self.tableWidget.item(selected_row, 0).text()
            dialog = BookDialog(self, book_id)
            if dialog.exec_():
                title, author, image_path = dialog.getBookData()
                update_book(book_id, title, author, image_path)
                self.showBooks()  # Refresh the book list after editing

    def loadSettings(self):
        (width, height) = load_settings()
        self.resize(width, height)

    def closeEvent(self, event):
        save_settings(self.width(), self.height())

    def deleteBook(self, row):
        book_id = self.tableWidget.item(row, 0).text()
        reply = QMessageBox.question(self, 'Подтверждение удаления',
                                     f'Вы уверены, что хотите удалить эту книгу?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            remove_book(book_id)
            self.showBooks()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LibrarySystem()
    sys.exit(app.exec_())
