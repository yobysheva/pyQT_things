import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout, \
    QFileDialog, QPushButton, QComboBox, QLabel, QLineEdit, QHeaderView, QDialog, QMessageBox
import csv
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QSize
from random import randint

import sqlite3

# Возможные темы
pink = [QColor(255, 210, 220), 'background: rgb(255, 190, 200)']
purple = [QColor(255, 220, 250), 'background: rgb(245, 200, 240)']
green = [QColor(205, 240, 205), 'background: rgb(190, 235, 185)']
blue = [QColor(180, 200, 255), 'background: rgb(160, 180, 255)']
yellow = [QColor(250, 255, 100), 'background: rgb(240, 250, 90)']
lightblue = [QColor(176,196,222), 'background: rgb(186,206,232)']

colors = [pink, purple, green, blue, yellow, lightblue]

# Генерируем случайную тему

colour, back_colour = pink

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("films.db")

        self.loadUI()
        self.file = 'films.db.'
        self.loadTable("films", """SELECT * FROM films""")

    # Создаем объекты и соединяем их с соотв. методами
    def loadUI(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.setWindowTitle('Фильмы')
        self.setGeometry(200, 200, 900, 500)

        self.genre_label = QLabel('Жанр', self)

        self.genre_list = QComboBox()
        self.genre_list.addItem('Все')
        self.genre_list.setStyleSheet(back_colour)

        self.year_label = QLabel('Год', self)

        self.year_list = QComboBox()
        self.year_list.addItem('Все')
        self.year_list.setStyleSheet(back_colour)

        self.duration_label = QLabel('Продолжительность', self)

        self.duration_list = QComboBox()
        self.duration_list.addItem('Все')
        self.duration_list.setStyleSheet(back_colour)

        self.name_label = QLabel('Название', self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setStyleSheet(back_colour)
        self.name_edit.setFixedWidth(200)

        self.show_label = QLabel('Результат', self)

        self.show_button = QPushButton('Показать', self)
        self.show_button.setStyleSheet(back_colour)
        self.show_button.clicked.connect(self.load_all)

        self.save_label = QLabel('Изменения', self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.setStyleSheet(back_colour)
        self.save_button.clicked.connect(self.update_table)

        self.add_label = QLabel('Добавить запись', self)

        self.add_button = QPushButton('Ввести значения')
        self.add_button.setStyleSheet(back_colour)
        self.add_button.clicked.connect(self.add_dialog)

        self.delete_label = QLabel('Удалить запись', self)

        self.delete_button = QPushButton('Удалить выбранное')
        self.delete_button.setStyleSheet(back_colour)
        self.delete_button.clicked.connect(self.delete_dialog)

        self.delete_label2 = QLabel('Удалить запись', self)

        self.delete_button2 = QPushButton('Удалить выбранное')
        self.delete_button2.setStyleSheet(back_colour)
        self.delete_button2.clicked.connect(self.delete_dialog)

        self.lay = QHBoxLayout()
        self.table = QTableWidget()
        self.table.cellChanged.connect(self.change_table)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.genre_label)
        self.button_layout.addWidget(self.genre_list)

        self.button_layout.addWidget(self.year_label)
        self.button_layout.addWidget(self.year_list)

        self.button_layout.addWidget(self.duration_label)
        self.button_layout.addWidget(self.duration_list)

        self.button_layout.addWidget(self.name_label)
        self.button_layout.addWidget(self.name_edit)

        self.button_layout.addWidget(self.show_label)
        self.button_layout.addWidget(self.show_button)

        self.button_layout.addWidget(self.save_label)
        self.button_layout.addWidget(self.save_button)

        self.button_layout.addWidget(self.add_label)
        self.button_layout.addWidget(self.add_button)

        self.button_layout.addWidget(self.delete_label)
        self.button_layout.addWidget(self.delete_button)

        self.button_layout.addWidget(self.delete_label2)
        self.button_layout.addWidget(self.delete_button2)

        self.button_layout.addStretch()

        self.lay.addWidget(self.table)
        self.lay.addLayout(self.button_layout)
        self.setLayout(self.lay)

        self.load_lists()

    # Берем значения для выпадающих списков из базы данных
    def load_lists(self):
        cur = self.con.cursor()

        self.years = cur.execute("""SELECT DISTINCT year FROM films ORDER BY year""").fetchall()
        self.year_list.addItems(str(year[0]) for year in self.years)
        self.genre_names = cur.execute("""SELECT title FROM genres""").fetchall()
        self.genre_list.addItems([genre[0] for genre in self.genre_names])
        self.durations = ['>10', '>15', '>30', '>45', '>60', '>75', '>90', '>105', '>120', '>135', '>150', '>165',
                          '>180', '>195', '>205']
        self.duration_list.addItems(self.durations)

        cur.close()

    # Выгружаем данные в таблицу
    def loadTable(self, table_name, request):
        self.table.blockSignals(True)
        cur = self.con.cursor()
        cur.execute("PRAGMA table_info({})".format(table_name))

        title = [column[1] for column in cur.fetchall()]

        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(0)

        for i, row in enumerate(cur.execute(request)):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)

                # item = self.table.item(i, j)
                if j == 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.resizeColumnToContents(1)
        # self.table.update()
        self.table.verticalHeader().hide()

        self.colorRows(colour)
        self.table.blockSignals(False)

        cur.close()

    def load_all(self):
        self.table.blockSignals(True)
        cur = self.con.cursor()

        genre = self.genre_list.currentText()
        print(genre)

        if genre != "Все":
            rq_g = f"(SELECT id FROM genres WHERE title = '{genre}')"
        else:
            rq_g = f"SELECT id FROM genres"

        year = self.year_list.currentText()
        #print(year)

        if year != "Все":
            rq_y = str(year)
        else:
            rq_y = f"SELECT DISTINCT year FROM films"

        duration = self.duration_list.currentText()
        #print(duration)

        if duration != "Все":
            rq_d = f"AND duration {duration}"
        else:
            rq_d = f" "

        name = self.name_edit.text()
        #print(name)

        if name != "Все":
            rq_n = f"AND title like '%{name}%'"
        else:
            rq_n = f" "

        self.loadTable("films",
                       f"""SELECT * FROM films WHERE genre IN ({rq_g}) AND year IN ({rq_y}) {rq_d} {rq_n}""")
        self.table.resizeColumnsToContents()
        self.colorRows(colour)
        self.table.blockSignals(False)
        cur.close()

    def change_table(self, row, colomn):
        try:
            cur = self.con.cursor()

            cur_id = self.table.item(row, 0).text()
            cur_name = self.table.item(row, 1).text()
            cur_year = self.table.item(row, 2).text()
            cur_gen = self.table.item(row, 3).text()
            cur_dur = self.table.item(row, 4).text()
            a = f"""UPDATE films SET title = "{cur_name}", year = {cur_year}, genre = {cur_gen}, duration = {cur_dur} WHERE id = {cur_id}"""
            print(a)
            cur.execute(a)
            cur.close()

        except Exception as e:
            print(e)

    def update_table(self):
        self.load_lists()
        self.con.commit()

    def add_dialog(self):
        try:
            self.dialog1 = QDialog(self)
            self.dialog1.setStyleSheet(back_colour)
            self.dialog1.setWindowTitle("Добавить запись")
            name_label1 = QLabel("Название:")
            name_line_edit1 = QLineEdit()
            name_line_edit1.setStyleSheet("background-color: none;")
            year_label1 = QLabel("Год:")
            year_line_edit1 = QLineEdit()
            year_line_edit1.setStyleSheet("background-color: none;")
            genre_label1 = QLabel("Жанр:")
            genre_line_edit1 = QLineEdit()
            genre_line_edit1.setStyleSheet("background-color: none;")
            duration_label1 = QLabel("Продолжительность:")
            duration_line_edit1 = QLineEdit()
            duration_line_edit1.setStyleSheet("background-color: none;")

            add_button1 = QPushButton("Добавить")
            #add_button1.setStyleSheet("background-color: none;")
            add_button1.clicked.connect(
                lambda: self.add_row(name_line_edit1.text(), year_line_edit1.text(), genre_line_edit1.text(),
                                     duration_line_edit1.text()))

            layout1 = QVBoxLayout()
            layout1.addWidget(name_label1)
            layout1.addWidget(name_line_edit1)
            layout1.addWidget(year_label1)
            layout1.addWidget(year_line_edit1)
            layout1.addWidget(genre_label1)
            layout1.addWidget(genre_line_edit1)
            layout1.addWidget(duration_label1)
            layout1.addWidget(duration_line_edit1)
            layout1.addWidget(add_button1)
            self.dialog1.setLayout(layout1)
            self.dialog1.exec()
        except Exception as e:
            print(e)

    def add_row(self, title1, year1, genre1, duration1):
        try:
            cur = self.con.cursor()
            a = f"""INSERT INTO films(title,year,genre,duration) VALUES("{title1}", {year1}, {genre1}, {duration1}) """
            cur.execute(a)
            self.con.commit()
            cur.close()

            message = QMessageBox()
            message.setWindowTitle("Успешное добавление")
            message.setText("Запись успешно добавлена.")
            message.setStyleSheet(back_colour)
            message.exec()
            self.dialog1.reject()

            self.load_lists()
            self.load_all()

        except Exception as e:
            message = QMessageBox()
            message.setWindowTitle("Не добавлено")
            message.setText("Не удалось добавить запись. Убедитесь, что данные внесены верно.")
            message.setStyleSheet(back_colour)
            message.exec()
            print(e)

    def delete_dialog(self):
        try:
            self.dialog2 = QDialog(self)
            self.dialog2.setStyleSheet(back_colour)
            self.dialog2.setWindowTitle("Добавить запись")
            label1 = QLabel("Вы уверенны, что хотите удалить запись? "
                                 "Восстановить её будет невозможно.")

            delete_button1 = QPushButton("Удалить")
            #add_button1.setStyleSheet("background-color: none;")
            delete_button1.clicked.connect(self.delete_item)

            esc_button1 = QPushButton("Отмена")
            # add_button1.setStyleSheet("background-color: none;")
            esc_button1.clicked.connect(self.dont_delete_item)

            layout1 = QVBoxLayout()
            layout1.addWidget(label1)
            layout1.addWidget(delete_button1)
            layout1.addWidget(esc_button1)
            self.dialog2.setLayout(layout1)
            self.dialog2.exec()

        except Exception as e:
            print(e)

    def dont_delete_item(self):
        self.dialog2.reject()
        message = QMessageBox()
        message.setWindowTitle("Отменя действия")
        message.setText("Запись не удалена.")
        message.setStyleSheet(back_colour)
        message.exec()

    def delete_item(self):
        try:
            current_item = self.table.currentItem()
            if current_item is not None:
                cur = self.con.cursor()
                row = current_item.row()
                item_id = int(self.table.item(row, 0).text())
                cur.execute("DELETE FROM films WHERE id = ?", (item_id,))
                self.con.commit()
                cur.close()

                self.dialog2.reject()
                message = QMessageBox()
                message.setWindowTitle("Успешно")
                message.setText("Успешно удалена запись")
                message.setStyleSheet(back_colour)
                message.exec()

                self.load_all()
                self.load_lists()

            else:
                message = QMessageBox()
                message.setWindowTitle("Ошибка")
                message.setText("Ни одна ячейка не выделена.")
                message.setStyleSheet(back_colour)
                message.exec()

        except Exception as e:
            print(e)

    def colorRows(self, color):
        c = 0
        for row in range(0, self.table.rowCount()):
            if self.table.isRowHidden(row) == False:
                c += 1
                for i in range(self.table.columnCount()):
                    if c % 2 == 1:
                        self.table.item(row, i).setBackground(color)
                    else:
                        self.table.item(row, i).setBackground(QColor(255, 255, 255))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
