import sys
from PyQt6 import uic, QtWidgets
import math
#commit2
def calculate_expression(expression):
    try:
        result = eval(expression)
        return result
    except:
        return "Error"

def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact(n - 1)


class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)
        self.setWindowTitle('Калькулятор')
        self.curr = ''
        self.curr_vir = ''
        self.flag = 0
        self.res = ''

        self.lineEdit.setReadOnly(True)
        self.lineEdit.setMaxLength(10)

        # Получаем список кнопок из группы кнопок цифр
        self.buttons = self.cifri.buttons()

        # Проходим по всем кнопкам и связываем их с обработчиком
        for button in self.buttons:
            button.clicked.connect(self.cifra_pushed)

        # Получаем список кнопок из группы кнопок выражений
        self.buttons = self.arifmetics.buttons()

        # Проходим по всем кнопкам и связываем их с обработчиком
        for button in self.buttons:
            button.clicked.connect(self.znak_pushed)

        self.ravno.clicked.connect(self.ravno_pushed)

        self.factorial.clicked.connect(self.factorial_pushed)

        self.sqrt.clicked.connect(self.sqrt_pushed)

        self.clear.clicked.connect(self.clear_pushed)

        self.stepen.clicked.connect(self.stepen_pushed)

    def cifra_pushed(self):
        button = self.sender()
        letter = button.text()

        # Понимаем, какая кнопка была нажата последней
        # В зависимости от состояния индикатора изменяем текущее выражение
        if self.flag == 0:
            self.curr += letter
        elif self.flag == 1:
            self.curr = letter
        elif self.flag == 2:
            self.curr = letter
            self.curr_vir = ''

        # Изменяем выражение, индикатор, выводим выражение на экран
        self.curr_vir += letter
        self.flag = 0

        self.lineEdit.setText(self.curr)


    def znak_pushed(self):
        button = self.sender()
        letter = button.text()

        # Если последним был зажат не знак, то можем нажать на знак
        if self.flag!=1:
            self.flag = 1
            self.curr_vir += letter
        else:
            self.lineEdit.setText('Error')


    def factorial_pushed(self):
        # Если последним был зажат не знак, то можем нажать на знак
        if self.flag!=1:
            self.flag = 1
            self.curr_vir = str(fact(int(calculate_expression(self.curr_vir))))
        else:
            self.lineEdit.setText('Error')


    def sqrt_pushed(self):
        # Если последним был зажат не знак, то можем нажать на знак
        # Считаем корень от неотрицательного числа
        if self.flag != 1:
            self.flag = 1
            number = float(self.curr_vir)
            if number >= 0:
                self.curr_vir = str(math.sqrt(number))
            else:
                self.lineEdit.setText('Error')
        else:
            self.lineEdit.setText('Error')

    def stepen_pushed(self):
        if self.flag != 1:
            self.flag = 1
            self.curr_vir += '**'
        else:
            self.lineEdit.setText('Error')


    def ravno_pushed(self):
        self.res = str(calculate_expression(self.curr_vir))
        self.curr_vir = self.res
        self.flag = 2

        self.lineEdit.setText(self.res)

    def clear_pushed(self):
        self.curr_vir = ''
        self.curr = ''
        self.flag = 0

        self.lineEdit.setText('')


app = QtWidgets.QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
