from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QRadioButton,
    QPushButton, QButtonGroup, QLineEdit,
    QLabel
)

class ActionTypeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose Action Type")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.click_radio = QRadioButton("Click at coordinates (x,y)")
        self.type_radio = QRadioButton("Type text _______")
        self.wait_radio = QRadioButton("Wait for ...")

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.click_radio)
        self.button_group.addButton(self.type_radio)
        self.button_group.addButton(self.wait_radio)

        layout.addWidget(self.click_radio)
        layout.addWidget(self.type_radio)
        layout.addWidget(self.wait_radio)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.accept)

        layout.addWidget(self.next_button)
        self.setLayout(layout)

    def get_selected_action(self):
        if self.click_radio.isChecked():
            return "click"
        elif self.type_radio.isChecked():
            return "type"
        elif self.wait_radio.isChecked():
            return "wait"
        else:
            return None
    
class ClickInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click Action Details")
        self.setFixedSize(300,150)

        layout = QVBoxLayout()
        self.input_x = QLineEdit()
        self.input_y = QLineEdit()

        self.input_x.setPlaceholderText("value of x")
        self.input_y.setPlaceholderText("value of y")

        layout.addWidget(QLabel("Enter x-coordinate:"))
        layout.addWidget(self.input_x)
        layout.addWidget(QLabel("Enter y-coordinate:"))
        layout.addWidget(self.input_y)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def get_coordinates(self):
        return self.input_x.text(), self.input_y.text()
    
class TypeInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Type Action Details")
        self.setFixedSize(300,150)

        layout = QVBoxLayout()
        self.input_text = QLineEdit()
        
        self.input_text.setPlaceholderText("type the task")

        layout.addWidget(QLabel("Enter the text here:"))
        layout.addWidget(self.input_text)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def get_text(self):
        return self.input_text.text()
    
class WaitInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wait Action Details")
        self.setFixedSize(300,150)

        layout = QVBoxLayout()
        self.input_wait = QLineEdit()

        self.input_wait.setPlaceholderText("waiting time ...")

        layout.addWidget(QLabel("Enter time to wait:"))
        layout.addWidget(self.input_wait)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def get_wait(self):
        return self.input_wait.text() 

    