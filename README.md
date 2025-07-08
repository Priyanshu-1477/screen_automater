# 🎯 Screen Automator

**Screen Automator** is a powerful desktop app that lets you automate mouse clicks, keyboard typing, and wait commands — all through a simple and intuitive GUI.  
Built with **Python + PyQt5**, it’s perfect for automating repetitive tasks, demos, form filling, testing, and more.

---

## 🚀 Features

- ✅ Add actions: Click, Type, Wait
- 🔁 Repeat the full automation multiple times
- 📜 Script queue with scrollable preview
- 💾 Save/load automation scripts as `.json`
- ⏹ Emergency stop (press `Ctrl + Alt + S`)
- 🧠 Fully threaded — no freezing during automation
- 🔧 Modular and extensible

---

## 📸 Screenshots

> *(Add screenshots later here)*

```
📜 Script Queue:
-----------------------
🖱️ Click at (100, 200)       [Edit] [X]
⌨️ Type: "Hello World"       [Edit] [X]
⏱️ Wait: 2 seconds           [Edit] [X]
```

---

## 🛠️ Tech Stack

| Tech        | Purpose                     |
|-------------|------------------------------|
| `PyQt5`     | GUI toolkit                  |
| `pyautogui` | Automation (mouse, keyboard) |
| `pynput`    | Global hotkey listener       |
| `threading` | Smooth background execution  |
| `json`      | Script save/load             |

---

## 💻 Installation

> Make sure you have Python 3.8+ installed.

```bash
git clone https://github.com/your-username/screen-automator.git
cd screen-automator
pip install -r requirements.txt
python3 main.py
```

---

## 🧪 Usage

1. Launch the app
2. Click **+ Add Action**
3. Choose `Click`, `Type`, or `Wait`
4. Click ▶ **Start** to begin automation
5. Click ⏹ or press `Ctrl + Alt + S` to stop anytime
6. Use 💾 **Save Script** / 📂 **Load Script** to reuse your actions
7. 🔁 Use "Repeat Script" to repeat the whole flow multiple times

---

## 📂 Save/Load Format

Scripts are saved as `.json` files with a list of your actions.  
You can reuse, share, or edit them manually if needed.

---

## 🚧 Roadmap

- [ ] 🔄 Drag-and-drop reordering
- [ ] 📷 Record live clicks/keystrokes
- [ ] 🌐 Export to `.exe` / `.AppImage`
- [ ] 🎛️ Command-line mode: `screen-automator run script.json`
- [ ] 🧠 Conditions, loops, variables

---

## 📄 License

MIT License © [Priyanshu Raj](https://github.com/Priyanshu-1477)

---
