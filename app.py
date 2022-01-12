import sys
import glob
import os
from PySide2 import QtCore, QtWidgets, QtGui

VERSION = ("2.0")
CONTACT = "ndrnistor@gmail.com"

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.browseButton = self.createButton("&Browse...", self.browse)
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        self.addPrefix = self.createButton("Add prefix", self.change_prefix)

        global prefix

        directoryLabel = QtWidgets.QLabel("Working Folder:")


        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.setSpacing(10)

        prefixLabel = QtWidgets.QLabel("Prefix:")
        self.prefix_edit = QtWidgets.QLineEdit()

        mainLayout.addWidget(directoryLabel, 0, 0)
        mainLayout.addWidget(self.directoryComboBox, 0, 1)
        mainLayout.addWidget(self.browseButton, 0, 2)
        mainLayout.addWidget(prefixLabel, 1,0)
        mainLayout.addWidget(self.prefix_edit, 1,1)
        mainLayout.addWidget(self.addPrefix, 1,2)

        #  Mainwindow

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 450, 100)
        self.setWindowTitle('Name Changer')
        self.setWindowIcon(QtGui.QIcon('AddPrefix.ico'))


        self.show()

    # def on_about_action(self):
    #     QtWidgets.QMessageBox.information(self, 'About', 'Version %s' % VERSION)

    def browse(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files",
                QtCore.QDir.currentPath())
        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))

        os.chdir(directory)
        print ("Folder chosen:",directory)
        return directory

    def createComboBox(self, text=""):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Preferred)
        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createLineEdit(self, text=""):
        boxEdit = QtWidgets.QLineEdit(text)
        return boxEdit

    def change_prefix(self):
        prefix = self.prefix_edit.text()
        print (prefix)
        if len(prefix) == 0:
            QtWidgets.QMessageBox().critical(self, u"Caution!", u"Prefix field is empty, will not continue.")
        else:
            for f in glob.glob("*.tif"):
                if f.startswith(prefix):
                    print (f + " was skipped since it already has prefix")
                    continue
                fix_prefix = prefix + f
                print (fix_prefix)
                os.rename(f, fix_prefix)
            for f in glob.glob("*.jpeg"):
                if f.startswith(prefix):
                    print (f + " was skipped since it already has prefix")
                    continue
                fix_prefix = prefix + f
                print (fix_prefix)
                os.rename(f, fix_prefix)
            for f in glob.glob("*.jpg"):
                if f.startswith(prefix):
                    print (f + " was skipped since it already has prefix")
                    continue
                fix_prefix = prefix + f
                print (fix_prefix)
                os.rename(f, fix_prefix)
            QtWidgets.QMessageBox.information(self, 'Done', "Prefix has been added")


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())