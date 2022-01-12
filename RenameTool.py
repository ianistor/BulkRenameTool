import sys
import glob
import os
from PySide2 import QtCore, QtWidgets, QtGui

VERSION = ("2.0")
CONTACT = "ndrnistor@gmail.com"

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.browseButton = self.createButton("&Schimba folderul...", self.browse)
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        self.addPrefix = self.createButton("Adauga prefix", self.change_prefix)
        self.changeState = self.createButton("Modifica judetul", self.change_state)
        self.changeCity = self.createButton("Modifica orasul", self.change_city)
        self.stateComboBox = self.createComboBox("Alege judetul")
        self.stateComboBox.addItems(["B", "AB", "AR", "AG", "BC", "BH", "BN", "BT", "BR", "BV", "BZ", "CL", "CS", "CJ", "CT", "CV", "DB", "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SJ", "SM", "SB", "SV", "TR", "TM", "TL", "VL", "VS", "VN"])

        global prefix

        directoryLabel = QtWidgets.QLabel("Folder:")
        self.stateLabel = QtWidgets.QLabel("Judetul:")
        self.cityLabel = QtWidgets.QLabel("Orasul:")


        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.setSpacing(10)

        prefixLabel = QtWidgets.QLabel("Prefix:")
        self.prefix_edit = QtWidgets.QLineEdit()
        self.city_edit = QtWidgets.QLineEdit()

        mainLayout.addWidget(directoryLabel, 0, 0)

        mainLayout.addWidget(self.directoryComboBox, 0, 1)
        mainLayout.addWidget(self.browseButton, 0, 2)
        mainLayout.addWidget(prefixLabel, 1,0)
        mainLayout.addWidget(self.prefix_edit, 1,1) # Edit box for prefix
        mainLayout.addWidget(self.addPrefix, 1,2)
        mainLayout.addWidget(self.stateLabel, 2, 0)
        mainLayout.addWidget(self.stateComboBox, 2, 1) # Edit box for state
        mainLayout.addWidget(self.changeState, 2, 2)
        mainLayout.addWidget(self.cityLabel, 3, 0)
        mainLayout.addWidget(self.city_edit, 3, 1)
        mainLayout.addWidget(self.changeCity, 3, 2)

        #  Mainwindow

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 450, 100)
        self.setWindowTitle('RenameTool')
        self.setWindowIcon(QtGui.QIcon('RenameTool.ico'))


        self.show()


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
            QtWidgets.QMessageBox.information(self, 'Gata',"Prefix-ul "+ '"' + prefix + '"' + "a fost adaugat")

    def change_state(self):
        count_state = 0
        state = self.stateComboBox.currentText()
        if state == "Alege judetul":
            QtWidgets.QMessageBox().critical(self, u"Atentie!", u"Nu ai selectat un judet")
        else:
            print(os.getcwd())
            for f in glob.glob("*"):
                new_name = f.split("_")[0] + "_" + f.split("_")[1] + "_" + state.lower() + "_" + f.split("_")[3] + "_" + \
                           f.split("_")[4]
                os.rename(f, new_name)
                count_state += 1
                print(("Renamed" + f + " into " + new_name))
            QtWidgets.QMessageBox().information(self, u"Gata!", state + " a fost adaugat la " + str(count_state) + " fisiere")



    def change_city(self):
        count = 0
        city = self.city_edit.text()
        print (city)
        if len(city) == 0:
            QtWidgets.QMessageBox().critical(self, u"Atentie!", u"Campul pentru oras este gol.")
        else:
            print (os.getcwd())
            for f in glob.glob("*"):
                new_name = f.split("_")[0] + "_" + f.split("_")[1] + "_" + f.split("_")[2] + "_" + city + "_" + f.split("_")[4]
                os.rename(f, new_name)
                count += 1
                print (("Renamed" + f + " into " + new_name))
        QtWidgets.QMessageBox().information(self, u"Gata!", city + " a fost adaugat la " + str(count) + " fisiere")




if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())