import sys
from PyQt5.QtWidgets import QApplication
from App import MyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())