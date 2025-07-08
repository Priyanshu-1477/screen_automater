import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QScrollArea, QFrame, QInputDialog
)
from PyQt5.QtWidgets import QFileDialog
import json
import pyautogui
import time
import threading

from gui.action_dialogs import ActionTypeDialog
from gui.action_dialogs import ClickInputDialog
from gui.action_dialogs import WaitInputDialog
from gui.action_dialogs import TypeInputDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Automator")
        self.setGeometry(300, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stop_flag = False


        # === Top Buttons ===
        self.add_button = QPushButton("+ Add Action")
        self.start_button = QPushButton("▶ Start")
        self.stop_button = QPushButton("⏹ Stop")
        self.save_button = QPushButton("💾 Save Script")
        self.load_button = QPushButton("📂 Load Script")
        

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        self.add_button.clicked.connect(self.open_add_dialog)
        self.start_button.clicked.connect(self.start_execution)
        self.save_button.clicked.connect(self.save_script)
        self.load_button.clicked.connect(self.load_script)
        self.repeat_button = QPushButton("🔁 Repeat Script")
        button_layout.addWidget(self.repeat_button)
        self.repeat_button.clicked.connect(self.ask_repeat_times)




        # === Script Queue Label ===
        queue_label = QLabel("📜 Script Queue:")

        # === Scrollable Queue Area ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.queue_container = QWidget()
        self.queue_layout = QVBoxLayout()
        self.queue_container.setLayout(self.queue_layout)

        self.scroll_area.setWidget(self.queue_container)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(queue_label)
        main_layout.addWidget(self.scroll_area)

        central_widget.setLayout(main_layout)

        self.add_sample_action("🖱️ Click at (320, 450)")
        self.add_sample_action("⌨️ Type 'Hello World'")
        self.add_sample_action("⏱️ Wait: 2 seconds")

    def ask_repeat_times(self):
        count, ok = QInputDialog.getInt(self, "Repeat Script", "How many times to repeat?", min=1, value=1)
        if ok:
            self.repeat_execution(count)

    def repeat_execution(self, times):
        self.stop_flag = False

        def stop_check():
            return self.stop_flag

        actions = self.get_all_actions()
        thread = threading.Thread(target=run_actions, args=(actions, stop_check, times))
        thread.start()

    def load_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # <-- helps show correctly on some Linux setups

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Automation Script",
            "",  # or set to a specific default directory
            "JSON Files (*.json);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    actions = json.load(f)

                # 🧹 Clear old actions
                while self.queue_layout.count():
                    item = self.queue_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

                for action in actions:
                    self.add_sample_action(action)

                print(f"[✅] Script loaded from {file_path}")
            except Exception as e:
                print(f"[❌] Failed to load script: {e}")

    
    def add_sample_action(self, action_text):
        row_layout = QHBoxLayout()

        label = QLabel(action_text)
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("X")

        # === Setup edit/delete functionality ===
        def handle_delete():
            container.deleteLater()

        def handle_edit():
            action_type = ""
            if action_text.startswith("🖱️"):
                dialog = ClickInputDialog()
                if dialog.exec_():
                    x, y = dialog.get_coordinates()
                    label.setText(f"🖱️ Click at ({x}, {y})")

            elif action_text.startswith("⌨️"):
                dialog = TypeInputDialog()
                if dialog.exec_():
                    text = dialog.get_text()
                    label.setText(f"⌨️ Type: {text}")

            elif action_text.startswith("⏱️"):
                dialog = WaitInputDialog()
                if dialog.exec_():
                    sec = dialog.get_seconds()
                    label.setText(f"⏱️ Wait: {sec} seconds")

        edit_button.clicked.connect(handle_edit)
        delete_button.clicked.connect(handle_delete)
        


        row_layout.addWidget(label)
        row_layout.addWidget(edit_button)
        row_layout.addWidget(delete_button)

        container = QWidget()
        container.setLayout(row_layout)

        self.queue_layout.addWidget(container)

    def save_script(self):
    
        actions = self.get_all_actions()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Ensures better behavior on some Linux systems

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Automation Script",
            os.path.expanduser("~"),  # Opens in home directory
            "JSON Files (*.json);;All Files (*)",
            options=options
        )

        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"  # Force .json extension if missing

            try:
                with open(file_path, "w") as f:
                    json.dump(actions, f, indent=2)
                print(f"[✅] Script saved to {file_path}")
            except Exception as e:
                print(f"[❌] Failed to save script: {e}")

    def stop_execution(self):
        self.stop_flag = True
        print("[INFO] Stop requested.")

    def open_add_dialog(self):
        dialog = ActionTypeDialog()
        if dialog.exec_():
            selected = dialog.get_selected_action()
            
            if selected=="click":
                input_dialog = ClickInputDialog()
                if input_dialog.exec_():
                    x, y = input_dialog.get_coordinates()
                    self.add_sample_action(f"🖱️ Click at ({x}, {y})")


                
            elif selected=="type":
                input_dialog = TypeInputDialog()
                if input_dialog.exec_():
                    text = input_dialog.get_text()
                    self.add_sample_action(f"⌨️ Type: '{text}'")

            elif selected=="wait":
                input_dialog = WaitInputDialog()
                if input_dialog.exec_():
                    wait = input_dialog.get_wait()
                    self.add_sample_action(f"⏱️ Wait: {wait} seconds")

    def get_all_actions(self):
        actions= []
        for i in range(self.queue_layout.count()):
            item = self.queue_layout.itemAt(i)
            widget = item.widget()
            if widget:
                layout = widget.layout()
                label = layout.itemAt(0).widget()
                if label:
                    actions.append(label.text())
        return actions

    
    def start_execution(self):
        self.stop_flag = False  # ✅ Reset when starting

        def stop_check():
            return self.stop_flag

        actions = self.get_all_actions()
        thread = threading.Thread(target=run_actions, args=(actions, stop_check))
        thread.start()

from pynput import keyboard

# Track pressed keys
pressed_keys = set()
stop_requested = False

def on_press(key):
    global stop_requested
    pressed_keys.add(key)

    if (
        keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys
    ) and (
        keyboard.Key.alt_l in pressed_keys or keyboard.Key.alt_r in pressed_keys
    ) and (
        key == keyboard.KeyCode.from_char('s')
    ):
        stop_requested = True
        print("[EMERGENCY] Ctrl + Alt + S detected — stopping automation.")

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()






def run_actions(actions, stop_check, repeat_count=1):
    import pyautogui
    import time

    print(f"[INFO] Automation will start in 3 seconds... Repeating {repeat_count} time(s).")
    time.sleep(3)

    for cycle in range(repeat_count):
        if stop_check() or stop_requested:
            print(f"[⏹] Stopped before starting cycle {cycle + 1}")
            break

        print(f"[🔁] Starting cycle {cycle + 1} of {repeat_count}")

        for action in actions:
            if stop_check() or stop_requested:
                print(f"[⏹] Stopped during cycle {cycle + 1}")
                return

            if action.startswith("🖱️ Click at"):
                coords = action.split("(")[1].split(")")[0]
                x, y = map(int, coords.split(","))
                pyautogui.moveTo(x, y)
                pyautogui.click()
                time.sleep(0.5)

            elif action.startswith("⌨️ Type:"):
                text = action.split("Type:")[1].strip().strip("'\"")
                pyautogui.write(text, interval=0.05)

            elif action.startswith("⏱️ Wait:"):
                seconds = action.split(":")[1].strip().split()[0]
                try:
                    total = float(seconds)
                    elapsed = 0.0
                    while elapsed < total:
                        if stop_check() or stop_requested:
                            print(f"[⏹] Stopped during wait in cycle {cycle + 1}")
                            return
                        time.sleep(0.1)
                        elapsed += 0.1
                except ValueError:
                    print(f"[ERROR] Invalid wait time: {seconds}")


if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
