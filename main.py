import sys
from PyQt5.QtWidgets import QApplication
from App import MyApp

def main():
    try:
        app = QApplication(sys.argv)
        window = MyApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    main()
