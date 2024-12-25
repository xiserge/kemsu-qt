from PyQt5.QtCore import QSettings


def save_settings(width, height):
    settings = QSettings('MyCompany', 'LibrarySystem')
    settings.setValue('window_size', (width, height))


def load_settings():
    settings = QSettings('MyCompany', 'LibrarySystem')
    size = settings.value('window_size', (1024, 768))
    return size
