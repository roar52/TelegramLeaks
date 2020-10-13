import os
import sys

from PySide2 import QtCore, QtWidgets
import multiprocessing
import db
from main_window import Ui_MainWindow


class Win(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Win, self).__init__()
        self.setupUi(self)
        self.ids=[]
        self.db_update.triggered.connect(self.get_file)
        self.NickName_rdr.toggled.connect(self.rdr_toggle)
        self.PhoneNumber_rdr.toggled.connect(self.rdr_toggle)
        self.Surname_rdr.toggled.connect(self.rdr_toggle)
        self.pushButton.clicked.connect(self.search_click)
        self.add_btn.setVisible(False)
        self.add_btn.clicked.connect(self.add_in_db)
        self.create_btn.triggered.connect(self.clear_row)
        self.update_btn.triggered.connect(self.update_in_db)
        self.remove_btn.triggered.connect(self.remove_from_db)
        self.select_page_btn.clicked.connect(self.select_page)
        self.select_page_btn.setEnabled(False)
        self.write_table({},0)

    def get_file(self) -> None:
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл:')
        # self.path_txt.setText(file[0])
        # self.check_btn.setEnabled(True)
        self.parse(file[0])

    def select_page(self):
        self.write_table({},self.comboBox.currentIndex())

    def parse(self,path:str):
        self.setEnabled(False)
        self.data={}
        path_file = path
        if os.path.isfile(path_file) is False:
            self.message_box('Неправильный путь')
            return
        # self.findPath_btn.setEnabled(False)
        # self.check_btn.setEnabled(False)
        # self.pushButton.setEnabled(False)
        size_file = os.path.getsize(path_file)
        ewq = []
        with open(path_file, 'r', encoding='latin-1') as file:
            size = 0
            for i in range(100):
                line = file.readline()
                size += sys.getsizeof(line)

        progress_proc = (size_file / size) * 100
        progress_proc = int(progress_proc) - 1
        print(size_file, size, progress_proc)
        p = QtWidgets.QProgressDialog(str("Load data in database"), "Cancel", 0, progress_proc)
        p.setMinimumDuration(0)
        p.setWindowTitle('plz, wait')
        counter = -1
        db.collection.drop()
        self.comboBox.clear()
        with open(path_file, 'r', encoding='latin-1') as log_file:
            j = 0
            header = ["sys_num", "name", "fname", "phone", "uid", "nik", "wo"]
            for line in log_file:
                p.setValue(j)
                if counter==-1:
                    counter += 1
                    continue
                counter += 1
                j += 1
                QtWidgets.QApplication.processEvents()
                doc = {}
                qwe = line.split('|')
                for n in range(0, len(header)):
                    doc[header[n]] = qwe[n + 1]
                ewq.append(doc)
                if counter%100==0:
                    self.comboBox.addItem(f'{counter//100}')
                if counter == 10000:
                    db.create_many(ewq)
                    ewq = []
                    counter = 0
                if p.wasCanceled():
                    break
        if len(ewq) > 0:
            db.create_many(ewq)
        p.setValue(progress_proc)
        self.write_table({},0)
        self.prekol.setText('')
        self.select_page_btn.setEnabled(True)
        self.setEnabled(True)

    def combobox_count(self,data,multiply):
        k = 0
        j = 0
        info=db.read(data,0,100)
        flag = False
        self.comboBox.clear()
        for i in info:
            flag = False
            j += 1
            if j % 99 == 0:
                k += 1
                self.comboBox.addItem(f"{k}")
                flag = True
        self.comboBox.setCurrentIndex(0)
        if flag:
            pass
        else:
            self.comboBox.addItem("Остаток")
        header = ["sys_num", "name", "fname", "phone", "uid", "nik", "wo"]
        print('1')
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(0)
        row = 0
        print(info)
        result=db.read({},multiply,100)
        for dic in result:
            print('2')
            self.table.insertRow(self.table.rowCount())
            col = 0
            for key, value in dic.items():
                if key == '_id':
                    self.ids.append(value)
                    continue
                kek = QtWidgets.QTableWidgetItem()
                kek.setData(QtCore.Qt.DisplayRole, value)
                print(value)
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
                col += 1
            row += 1
        self.prekol.setText('')
        self.select_page_btn.setEnabled(True)

    def write_table(self,data,multipy):
        header = ["sys_num", "name", "fname", "phone", "uid", "nik", "wo"]
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(0)
        row = 0
        info = db.read(data, multipy, 100)
        for dic in info:
            self.table.insertRow(self.table.rowCount())
            col = 0
            for key, value in dic.items():
                if key == '_id':
                    continue
                kek = QtWidgets.QTableWidgetItem()
                kek.setData(QtCore.Qt.DisplayRole, value)
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
                col += 1
            row += 1

    def search_click(self):
        self.update_btn.setEnabled(False)
        self.add_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.select_page_btn.setEnabled(False)
        if self.NickName_rdr.isChecked():
            self.combobox_count({'nik':self.FInd_txt.toPlainText()},0)
            self.write_table({'nik':self.FInd_txt.toPlainText()},0)
            self.data={'nik':self.FInd_txt.toPlainText()}
        elif self.PhoneNumber_rdr.isChecked():
            self.combobox_count({'phone': self.FInd_txt.toPlainText()},0)
            self.write_table({'phone': self.FInd_txt.toPlainText()}, 0)
            self.data = {'phone': self.FInd_txt.toPlainText()}
        elif self.Surname_rdr.isChecked():
            self.combobox_count({'fname': self.FInd_txt.toPlainText()},0)
            self.write_table({'fname': self.FInd_txt.toPlainText()}, 0)
            self.data = {'fname': self.FInd_txt.toPlainText()}
        self.update_btn.setEnabled(True)
        self.add_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.select_page_btn.setEnabled(True)



    def rdr_toggle(self)->None:
        self.Find_lbl.setText('')
        if self.NickName_rdr.isChecked():
            self.Find_lbl.setText('Введите логин:')
            self.FInd_txt.setText('')
            self.Find_txt.setEnabled(True)
            self.pushButton.setText('Сортировать')
        if self.PhoneNumber_rdr.isChecked():
            self.Find_lbl.setText('Введите телефон:')
            self.FInd_txt.setText('')
            self.Find_txt.setEnabled(True)
            self.button.setText('Сортировать')
            self.FInd_txt.setText('')
        if self.Surname_rdr.isChecked():
            self.Find_lbl.setText('Введите ФИО:')
            self.Find_txt.setEnabled(True)
            self.FInd_txt.setText('')
            self.button.setText('Сортировать')
        self.button.setEnabled(True)

    def clear_row(self):
        self.table.setRowCount(0)
        self.table.setRowCount(1)
        self.add_btn.setVisible(True)

    def add_in_db(self):
        header = ["sys_num", "name", "fname", "phone", "uid", "nik", "wo"]
        data = []
        try:
            for i in range(7):
                data.append(self.table.item(0, i).text())
        except AttributeError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', f'{i + 1}  колонка пустая')
            return 1
        db.create({header[0]:data[0], header[1]:data[1], header[2]:data[2], header[3]:data[3], header[4]:data[4], header[5]:data[5], header[6]:data[6]})
        QtWidgets.QMessageBox.about(self, 'Успешно','Элемент в базе!')
        self.table.setRowCount(0)
        self.add_btn.setVisible(False)

    def remove_from_db(self):
        current_row = self.table.currentRow()
        id = {'_id': self.ids[current_row]}
        if current_row == -1:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Строчка не выбрана')
            return 1
        self.table.removeRow(current_row)
        self.ids.remove(self.ids[current_row])
        db.delete(id)
        QtWidgets.QMessageBox.about(self, 'Успешно', 'Элемент удален!')

    def update_in_db(self):
        header = ["sys_num", "name", "fname", "phone", "uid", "nik", "wo"]
        current_row = self.table.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Строчка не выбрана')
            return 1
        id = {'_id': self.ids[current_row]}
        max = 7
        data = []
        for column in range(max):
            data.append(self.table.item(current_row, column).text())
        db.update(id, {header[0]:data[0], header[1]:data[1], header[2]:data[2], header[3]:data[3], header[4]:data[4], header[5]:data[5], header[6]:data[6]})
        QtWidgets.QMessageBox.about(self, 'Успешно', 'Элемент обновлен!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Win()
    window.show()
    sys.exit(app.exec_())
