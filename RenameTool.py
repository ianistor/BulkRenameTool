import sys
import re
import glob
import os
from PySide2 import QtCore, QtWidgets, QtGui

VERSION = ("2.0")
CONTACT = "ndrnistor@gmail.com"

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.browseButton = self.createButton("&Browse working folder...", self.browse)
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        self.addPrefix = self.createButton("Add prefix", self.change_prefix)
        self.changeState = self.createButton("Change state", self.change_state)
        self.changeCity = self.createButton("Change city", self.change_city)
        self.stateComboBox = self.createComboBox("Pick your state")
        self.stateComboBox.addItems(["B", "AB", "AR", "AG", "BC", "BH", "BN", "BT", "BR", "BV", "BZ", "CL", "CS", "CJ", "CT", "CV", "DB", "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SJ", "SM", "SB", "SV", "TR", "TM", "TL", "VL", "VS", "VN"])

        global prefix

        directoryLabel = QtWidgets.QLabel("Folder:")
        self.stateLabel = QtWidgets.QLabel("State:")
        self.cityLabel = QtWidgets.QLabel("City:")


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
        """
        Changes working folder
        :return:
        """
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
        """
        Function for faster Combo box creation (more clean than anything else really)
        :param text:
        :return:
        """
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Preferred)
        return comboBox

    def createButton(self, text, member):
        """
        Function for faster button creation (more clean than anything else really)
        :param text:
        :param member:
        :return:
        """
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createLineEdit(self, text=""):
        """
        Function for faster edit box creation (more clean than anything else really)
        :param text:
        :return:
        """
        boxEdit = QtWidgets.QLineEdit(text)
        return boxEdit


    def change_prefix(self):
        """
        Function to modify prefix of all files in a folder (for safety reasons I've limited it to .tif, .jpeg, .jpg only)
        This should be written more nicely when I have time, but for now, not touching what works :)
        """        
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
            QtWidgets.QMessageBox.information(self, 'Done',"Prefix: "+ '"' + prefix + '"' + "was added")

    def change_state(self):
        """
        Renames the 3rd _ group (which in this case equals the state)
        """
        count_state = 0
        state = self.stateComboBox.currentText()
        if state == "Pick State":
            QtWidgets.QMessageBox().critical(self, u"Error!", u"No state was selected")
            return
        else:
            print(os.getcwd())
            for f in glob.glob("*"):
                new_state_names = []
                splitting_state = re.split('([_])', f)
                new_state_name = splitting_state[:4]
                end_name = splitting_state[5:]
                new_state_names.extend(new_state_name)
                new_state_names.extend(state.lower())
                new_state_names.extend(end_name)
                name_string = ''.join(map(str, new_state_names))
                print(name_string)
                os.rename(f, name_string)
                count_state += 1
                print(("Renamed -> " + f + " into ->  " + name_string))
            QtWidgets.QMessageBox().information(self, u"Done!", state + " was added to " + str(count_state) + " files")



    def change_city(self):
        """
        Renames the 4th _ group (which in this case equals the city)
        :return:
        """

        count = 0
        city = self.city_edit.text()
        print (city)
        if len(city) == 0:
            QtWidgets.QMessageBox().critical(self, u"Error!", u"City field is empty, please edit")
            return
        else:
            print (os.getcwd())
            for f in glob.glob("*"):
                new_name_list = []
                splitting_city = re.split('([_])', f)
                new_name = splitting_city[:6]
                end_name = splitting_city[7:]
                new_name_list.extend(new_name)
                new_name_list.extend(city.lower())
                new_name_list.extend(end_name)
                name_string = ''.join(map(str, new_name_list))
                print (name_string)
                os.rename(f, name_string)
                count += 1
                print (("Renamed ->  " + f + " into -> " + str(name_string)))
        QtWidgets.QMessageBox().information(self, u"Done!", city + " was added to  " + str(count) + " files")



if __name__ == '__main__':

    import sys
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    window = Window()
    window.show()
    sys.exit(app.exec_())
