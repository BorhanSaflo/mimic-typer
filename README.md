# Mimic Typer

![mimic-typer-demo](https://github.com/BorhanSaflo/mimic-typer/assets/60056206/69666c6d-3ef4-4c4c-969c-c7f85466ca2e)

Mimic Typer is a Python-based GUI application that simulates typing in any text field outside the application. It's built using `Tkinter` for the graphical interface and utilizes libraries like `pyautogui` and `keyboard` for controlling keyboard events. This application is particularly useful for software demonstrations or presentations, where you can pre-write the text you want to be typed and then use the application to simulate typing in the currently active text field. You can also use it for testing inputs or text fields in software applications.

## Installation

To run Mimic Typer, you'll need Python installed along with Tkinter and the other dependencies.

### Installing Python

You can install Python from [here](https://www.python.org/downloads/).

### Installing Tkinter

Tkinter is a Python library that is used for creating GUI applications. It comes pre-installed with Python on Windows and macOS, but you'll need to install it separately on Linux. You can install it by running the following command in the terminal:

```bash
sudo apt-get install python3-tk
```

### Installing Dependencies

Once you have Python installed, you can install the dependencies by running the following command in the project directory:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the program by running `python mimic-typer.py` in the project directory.
2. Enter the text you want to be typed automatically in the text area.
3. Use the options in the right panel to set customize the typing behavior.
4. To start typing, press `Ctrl+Shift+/`. The program will then simulate typing in the currently active text field outside the application.
5. Press `Ctrl+Shift+/` again to stop typing.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
