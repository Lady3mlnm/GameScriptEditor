GameScriptEditor is a specialized text editor for working with scripts _(for example, game scripts)_. The editor has several unique features that simplify working with scripts that are not available in usual text editors.

The main feature of the editor is the preview window, which allows you to see in real time how original text will be transformed into game text according to set of rules. The editor greatly simplifies the work of text alignment.

In this version, the initial state of the editor is customized and text transformation rules are defined by modifying the ```settings.ini``` file in the folder ```settings```. You can change the themes or create your own through the contents of the folder ```themes```. The markers used can be changed via the folder ```images```.

The editor has English and Russian interfaces.

Screenshot of the application and illustration of some ways of tags transformations _(not all)_ superimposed on it:
![screenshot of the application](description%20and%20scheme/screenshot%20GSE%20v1_0.png)

![screenshot of the application with several arrows that illustrate some ways of transformation](description%20and%20scheme/screenshot%20GSE%20v1_0%20with%20arrows.png)

If the program starts working slowly, try to disable the marker field in the preview window and the character counter.

The program is created in the programming language [Python v3.9](https://www.python.org/) using [PyQt6 v6.8.0](https://www.riverbankcomputing.com/software/pyqt/) and [QScintilla v2.14.1](https://qscintilla.com) in the [PyCharm](https://www.jetbrains.com/pycharm/) development environment. Using a downgraded version of Python is due to the need for compatibility with PyQt and QScintilla.

This repository contains only the code. You can download the compiled application from the [Google Drive](https://drive.google.com/drive/folders/1dm2ofi04wq0MlFdrGhH5xWs_8QowMka2).