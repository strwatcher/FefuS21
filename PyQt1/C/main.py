import sys
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


PRODUCTS = [["Баскет", "240", "./resources/324188775_m650.webp"],
            ["Лимонад Черешня", "89", "./resources/cherry.webp"],
            ["Милкшейк Банан", "59", "./resources/banana_milkshake.webp"],
            ["Мороженое банановое", "70", "./resources/banan_icecream.webp"],
            ["Баскет острый", "320", "./resources/busket_spicy.webp"],
            ["Картошка по деревенски", "60", "./resources/pot1.webp"],
            ["Донат карамельный", "74", "./resources/don.webp"],
            ["Айс Кофе", "89", "./resources/ice.webp"],
            ["ЛанчБаскет 5 за 300", "300", "./resources/lunch.webp"],
            ["Шефбургер Джуниор", "99", "./resources/sch.webp"],
            ["Сырные подушечки", "69", "./resources/cheese.webp"]]


class Box:
    def __init__(self):
        self._shop_box = list()

    def drop_product(self, product):
        self._shop_box.append(product)

    def catch_product(self, product):
        self._shop_box.remove(product)

    def take_all(self):
        return self._shop_box[:]

    def print_all(self):
        for product in self._shop_box:
            print(product.name, product.quantity)


class Product:
    def __init__(self, name, cost, img_src):
        self._name = name
        self._cost = cost
        self._img_src = img_src
        self._quantity = 0

    @property
    def name(self):
        return self._name

    @property
    def quantity(self):
        return self._quantity

    @property
    def cost(self):
        return self._cost

    @property
    def img_src(self):
        return self._img_src

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity


class ProductView:
    def __init__(self, product, parent, checkbox_flag=True):
        self._widget = QWidget()
        self._name = QLabel(product.name)
        self._cost = QLabel(product.cost)
        pixmap = QPixmap(product.img_src)
        self._img = QLabel()
        self._img.setPixmap(pixmap)
        self.cf = checkbox_flag
        self.checkbox = QCheckBox()
        self._parent = parent
        self._product = product
        self.setup_ui()

    def setup_ui(self):
        product_layout = QVBoxLayout()
        self.widget.setStyleSheet("background: white;"
                                  "border: black solid 1px;"
                                  "border-radius: 10px;"
                                  "margin: 10%;")

        if self.cf:
            adder = partial(self._parent.adder, self.product)
            self.checkbox.clicked.connect(adder)
            product_layout.addWidget(self.checkbox)

        product_layout.addWidget(self._img, alignment=Qt.AlignHCenter)
        product_layout.addWidget(self._name, alignment=Qt.AlignHCenter)
        product_layout.addWidget(self._cost, alignment=Qt.AlignHCenter)
        self.widget.setLayout(product_layout)

    @property
    def widget(self):
        return self._widget

    @property
    def product(self):
        return self._product


class MenuWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.box = Box()
        self.parent = parent
        self.scroll = QScrollArea()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        menu_widget = QWidget()
        layout = QGridLayout()
        row, column = 0, 0
        for product in PRODUCTS:
            cur_product_widget = ProductView(Product(*product), self).widget
            layout.addWidget(cur_product_widget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
        button = QPushButton("Сделать заказ")
        button.clicked.connect(self.parent.go_to_cheque)
        menu_widget.setLayout(layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(menu_widget)

        main_layout.addWidget(self.scroll)
        main_layout.addWidget(button)

        self.setLayout(main_layout)

    def adder(self, product):
        if self.sender().isChecked():
            i, ok_pressed = QInputDialog.getInt(self, "Количество", "Выберите количество порций")
            if ok_pressed and i > 0:
                product.quantity = i
                self.sender().setText(str(i))
                self.box.drop_product(product)
            else:
                self.sender().setChecked(False)
        else:
            self.box.catch_product(product)


class ChequeWindow(QWidget):
    def __init__(self, box):
        super().__init__()
        self.box = box
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        cheque = QWidget()
        layout = QVBoxLayout()
        final_cost = 0
        for product in self.box.take_all():
            for i in range(product.quantity):
                cur_product_widget = ProductView(product, self, False).widget
                layout.addWidget(cur_product_widget)
                final_cost += int(product.cost)
        total_cost = QLabel("Общая стоимость: {}".format(final_cost))
        total_cost.setStyleSheet("font-size: 30px;")
        layout.addWidget(total_cost)

        cheque.setLayout(layout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(cheque)

        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.menu = MenuWindow(self)
        self.cheque = ChequeWindow(Box())

        self.stack = QStackedWidget()
        self.stack.addWidget(self.menu)
        self.stack.setCurrentWidget(self.menu)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def go_to_cheque(self):
        if len(self.menu.box.take_all()) == 0:
            return
        self.cheque = ChequeWindow(self.menu.box)
        self.cheque.show()
        self.stack.addWidget(self.cheque)
        self.stack.setCurrentWidget(self.cheque)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
