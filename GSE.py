import os.path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QSplitter, QTextEdit,
                             QVBoxLayout, QFrame, QToolBar, QCheckBox, QLabel, QSpinBox,
                             QSizePolicy, QFileDialog, QMessageBox)
from PyQt6.QtGui import QAction, QIcon, QImage, QFontMetrics
from PyQt6.QtCore import Qt, QSize
from PyQt6.Qsci import QsciScintilla
import sys
import math
import re
import GSElexer
import DataLoading

TEST_MODE = False

class CustomMainWindow(QMainWindow):  #   QWidget
    def __init__(self):
        super(CustomMainWindow, self).__init__()

        self.app_title = DataLoading.app_title
        self.app_position_x = DataLoading.app_position_x
        self.app_position_y = DataLoading.app_position_y
        self.app_width = DataLoading.app_width
        self.app_height = DataLoading.app_height
        self.ratio_editor1_to_editor2 = DataLoading.ratio_editor1_to_editor2
        self.editor2_font = DataLoading.editor2_font
        self.is_v_guidelines_shown_in_ed1 = DataLoading.is_v_guidelines_shown_in_ed1
        self.is_v_guidelines_shown_in_ed2 = DataLoading.is_v_guidelines_shown_in_ed2
        self.position_guidelines_vertical = DataLoading.position_guidelines_vertical
        self.is_h_guidelines_shown_in_ed1 = DataLoading.is_h_guidelines_shown_in_ed1
        self.is_h_guidelines_shown_in_ed2 = DataLoading.is_h_guidelines_shown_in_ed2
        self.position_guidelines_horizontal = DataLoading.position_guidelines_horizontal
        self.is_margin_numbers_shown_in_ed1 = DataLoading.is_margin_numbers_shown_in_ed1
        self.is_margin_markers_shown_in_ed1 = DataLoading.is_margin_markers_shown_in_ed1
        self.is_margin_numbers_shown_in_ed2 = DataLoading.is_margin_numbers_shown_in_ed2
        self.is_margin_markers_shown_in_ed2 = DataLoading.is_margin_markers_shown_in_ed2

        self.margin1_font = DataLoading.margin1_font
        self.margin1_font_color = DataLoading.margin1_font_color
        self.margin1_numbers_bg = DataLoading.margin1_numbers_bg
        self.margin1_markers_bg = DataLoading.margin1_markers_bg
        self.margin1_number_width = DataLoading.margin1_number_width
        self.guidelines1_color = DataLoading.guidelines1_color

        self.margin2_font = DataLoading.margin2_font
        self.margin2_font_color = DataLoading.margin2_font_color
        self.margin2_numbers_bg = DataLoading.margin2_numbers_bg
        self.margin2_markers_bg = DataLoading.margin2_markers_bg
        self.margin2_number_width = DataLoading.margin2_number_width
        self.guidelines2_color = DataLoading.guidelines2_color

        self.is_spec_linebreaks_shown = DataLoading.is_spec_linebreaks_shown
        self.spec_linebreaks_in_ed2_color_name = DataLoading.spec_linebreaks_in_ed2_color_name
        self.is_text_wrapped = DataLoading.is_text_wrapped
        self.indent_text_wrapped = DataLoading.indent_text_wrapped
        self.is_scrollbars_synchronized = DataLoading.is_scrollbars_synchronized
        self.is_editors_for_notes_shown = DataLoading.is_editors_for_notes_shown
        self.is_toolbar_shown = True         # toolbar at the beginning is always shown
        self.is_toolbar_movable = DataLoading.is_toolbar_movable
        self.position_of_toolbar = DataLoading.position_of_toolbar
        self.is_counter_shown = DataLoading.is_counter_shown
        self.is_app_in_russian = DataLoading.is_app_in_russian

        self.dd_tags_replacement_extended = DataLoading.dd_tags_replacement_extended
        self.pattern_design_tags = '(' + '|'.join(map(re.escape, DataLoading.tp_tags_design_united)) + ')'
        self.pattern_replace = '(' + '|'.join(map(re.escape, DataLoading.dd_tags_replacement_extended.keys())) + ')'
        self.compiled_re_linebreaks = re.compile('|'.join(map(re.escape, DataLoading.tp_tags_linebreak)))
        self.pattern_to_hide_chars_between_tags = DataLoading.pattern_to_hide_chars_between_tags

        self.tp_tags_linebreak_special = DataLoading.tp_tags_linebreak_special
        self.original_text = DataLoading.original_text

        self.splitter_central_ratio = [400, 100]  # vertical proportion between the main editors and fields for notes

        self.ls_obs_spec_linebreaks = []  # list of objects representing horizontal linebreaks
        self.scroll_pos_1_remember = 0    # this variable is used to track moving of the vertical scrollbar in editor 1

        self.dd_markers_in_ed2 = dict()  # create dictionary that keeps symbol markers in the preview window

        # 1. Define the geometry of the main window
        self.setGeometry(self.app_position_x, self.app_position_y, self.app_width, self.app_height)
        self.setWindowTitle(self.app_title if self.app_title else "GameScriptEditor -v1.0")
        self.setWindowIcon(QIcon('images/favicon.png'))

        self.create_menu()
        self.create_toolbar()
        self.create_main_editors_and_layouts()
        self.show_app_and_initialize_its_state()


    def create_menu(self):
        self.main_menu = self.menuBar()

        ### submenu 'File' ###
        self.file_menu = self.main_menu.addMenu("File")

        self.load_action = QAction("Load script from file", self)
        self.load_action.setShortcut("Ctrl+O")
        self.load_action.triggered.connect(self.load_text_from_file)
        self.file_menu.addAction(self.load_action)

        self.save_action = QAction("Save script to file", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_text_to_file)
        self.file_menu.addAction(self.save_action)

        self.file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Alt+F4")
        self.exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(self.exit_action)

        ### submenu 'Guidelines' ###
        self.guidelines_menu = self.main_menu.addMenu("Guidelines")

        self.v_guideline_show_ed1_action = QAction("Show vertical guideline in script editor", self)
        self.v_guideline_show_ed1_action.setCheckable(True)
        self.v_guideline_show_ed1_action.setChecked(self.is_v_guidelines_shown_in_ed1)
        self.v_guideline_show_ed1_action.triggered.connect(self.vert_guidelines_visibility_changed_in_ed1)
        self.guidelines_menu.addAction(self.v_guideline_show_ed1_action)

        self.v_guideline_show_ed2_action = QAction("Show vertical guideline in preview window", self)
        self.v_guideline_show_ed2_action.setCheckable(True)
        self.v_guideline_show_ed2_action.setChecked(self.is_v_guidelines_shown_in_ed2)
        self.v_guideline_show_ed2_action.triggered.connect(self.vert_guidelines_visibility_changed_in_ed2)
        self.guidelines_menu.addAction(self.v_guideline_show_ed2_action)

        self.guidelines_menu.addSeparator()

        self.h_guideline_in_ed1_show_action = QAction("Show horizontal guideline in script editor", self)
        self.h_guideline_in_ed1_show_action.setCheckable(True)
        self.h_guideline_in_ed1_show_action.setChecked(self.is_h_guidelines_shown_in_ed1)
        self.h_guideline_in_ed1_show_action.triggered.connect(self.hor_guideline_visibility_changed_in_ed1)
        self.guidelines_menu.addAction(self.h_guideline_in_ed1_show_action)

        self.h_guideline_in_ed2_show_action = QAction("Show horizontal guideline in preview window", self)
        self.h_guideline_in_ed2_show_action.setCheckable(True)
        self.h_guideline_in_ed2_show_action.setChecked(self.is_h_guidelines_shown_in_ed2)
        self.h_guideline_in_ed2_show_action.triggered.connect(self.hor_guideline_visibility_changed_in_ed2)
        self.guidelines_menu.addAction(self.h_guideline_in_ed2_show_action)

        ### submenu 'Other' ###
        self.other_menu = self.main_menu.addMenu("Other")

        self.toolbar_show_action = QAction("Show toolbar", self)   # at the start of the app the toolbar is always shown
        self.toolbar_show_action.setShortcut("F12")
        self.toolbar_show_action.setCheckable(True)
        self.toolbar_show_action.setChecked(True)
        self.toolbar_show_action.triggered.connect(self.toolbar_visibility_changed)
        self.other_menu.addAction(self.toolbar_show_action)

        self.toolbar_movable_action = QAction("Toolbar is movable", self)
        self.toolbar_movable_action.setCheckable(True)
        self.toolbar_movable_action.setChecked(self.is_toolbar_movable)
        self.toolbar_movable_action.triggered.connect(self.toolbar_movable_action_state_changed)
        self.other_menu.addAction(self.toolbar_movable_action)

        self.counter_of_chars_show_action = QAction("Show counter of characters", self)
        self.counter_of_chars_show_action.setCheckable(True)
        self.counter_of_chars_show_action.setChecked(self.is_counter_shown)
        self.counter_of_chars_show_action.triggered.connect(self.counter_of_chars_visibility_changed)
        self.other_menu.addAction(self.counter_of_chars_show_action)

        self.lang_of_app_change_action = QAction("Сменить язык на русский", self)
        self.lang_of_app_change_action.triggered.connect(self.change_app_lang)
        self.other_menu.addAction(self.lang_of_app_change_action)

        ### submenu 'About' ###
        about_action = QAction("?", self)  # 'Test' button as an item of QMenu
        about_action.triggered.connect(self.fn_about_action)
        self.main_menu.addAction(about_action)

        ### item-command 'Test' ### - it shows button 'Test' to launch some test code snippet
        if TEST_MODE:
            menuSeparator = self.main_menu.addMenu('|')
            menuSeparator.setEnabled(False)

            test_action = QAction("Test", self)
            test_action.triggered.connect(self.fn_test_action)
            self.main_menu.addAction(test_action)


    def create_toolbar(self):
        self.toolbar = QToolBar("ToolBar")       # create a QToolBar
        self.toolbar.setIconSize(QSize(20, 20))  # set icon size
        self.toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea | Qt.ToolBarArea.BottomToolBarArea)
            # This limitation allows user dock the toolbar only to the top and bottom edges.
            # I impose this restriction to keep the further code simpler

        self.addToolBar(self.position_of_toolbar, self.toolbar)

        self.lb_guidelines = QLabel("Guidelines:")
        self.toolbar.addWidget(self.lb_guidelines)

        # create a spinbox for position of vertical guidelines
        self.sb_v_guideline = QSpinBox()
        self.sb_v_guideline.setMaximum(999)
        self.sb_v_guideline.setValue(self.position_guidelines_vertical)
        self.sb_v_guideline.setSingleStep(1)
        self.sb_v_guideline.setFixedWidth(72)
        self.sb_v_guideline.setToolTip("Position of vertical guidelines")
        self.sb_v_guideline.valueChanged.connect(self.sb_v_guideline_valueChanged)
        self.toolbar.addWidget(self.sb_v_guideline)

        # create a spinbox for position of horizontal guidelines
        self.sb_h_guideline = QSpinBox()
        self.sb_h_guideline.setMaximum(999)
        self.sb_h_guideline.setValue(self.position_guidelines_horizontal)
        self.sb_h_guideline.setSingleStep(1)
        self.sb_h_guideline.setFixedWidth(64)
        self.sb_h_guideline.setToolTip("Position of horizontal guidelines")
        self.sb_h_guideline.valueChanged.connect(self.sb_h_guideline_valueChanged)
        self.toolbar.addWidget(self.sb_h_guideline)

        self.toolbar.addSeparator()

        self.lb_margins = QLabel(" Margins: ")
        self.toolbar.addWidget(self.lb_margins)

        self.cb_margin_1n = QCheckBox("1#  ")
        self.cb_margin_1n.setChecked(self.is_margin_numbers_shown_in_ed1)
        self.cb_margin_1n.setToolTip("Show number field in the script editor")
        self.cb_margin_1n.stateChanged.connect(self.cb_margin_1n_stateChanged)
        self.toolbar.addWidget(self.cb_margin_1n)

        self.cb_margin_1m = QCheckBox("1⬣  ")
        self.cb_margin_1m.setChecked(self.is_margin_markers_shown_in_ed1)
        self.cb_margin_1m.setToolTip("Show marker field in the script editor")
        self.cb_margin_1m.stateChanged.connect(self.cb_margin_1m_stateChanged)
        self.toolbar.addWidget(self.cb_margin_1m)

        self.cb_margin_2n = QCheckBox("2#  ")
        self.cb_margin_2n.setChecked(self.is_margin_numbers_shown_in_ed2)
        self.cb_margin_2n.setToolTip("Show number field in the preview window")
        self.cb_margin_2n.stateChanged.connect(self.cb_margin_2n_stateChanged)
        self.toolbar.addWidget(self.cb_margin_2n)

        self.cb_margin_2m = QCheckBox("2⬣  ")
        self.cb_margin_2m.setChecked(self.is_margin_markers_shown_in_ed2)
        self.cb_margin_2m.setToolTip("Show marker field in the preview editor")
        self.cb_margin_2m.stateChanged.connect(self.cb_margin_2m_stateChanged)
        self.toolbar.addWidget(self.cb_margin_2m)

        self.toolbar.addSeparator()

        self.lb_text_wrapping = QLabel("Text wrapping: ")
        self.toolbar.addWidget(self.lb_text_wrapping)

        self.cb_text_wrapping = QCheckBox("🢱")
        self.cb_text_wrapping.setChecked(self.is_text_wrapped)
        self.cb_text_wrapping.setToolTip("Text wrapping")
        self.cb_text_wrapping.stateChanged.connect(self.cb_text_wrapping_stateChanged)
        self.toolbar.addWidget(self.cb_text_wrapping)

        # create a spinbox for position of vertical guidelines
        self.sb_wrap_indent = QSpinBox()
        self.sb_wrap_indent.setMaximum(999)
        self.sb_wrap_indent.setValue(self.indent_text_wrapped)
        self.sb_wrap_indent.setSingleStep(1)
        self.sb_wrap_indent.setFixedWidth(64)
        self.sb_wrap_indent.setToolTip("indentation of text wrapping")
        self.sb_wrap_indent.valueChanged.connect(self.sb_wrap_indent_valueChanged)
        self.toolbar.addWidget(self.sb_wrap_indent)

        self.toolbar.addSeparator()

        self.lb_other = QLabel("Other: ")
        self.toolbar.addWidget(self.lb_other)

        self.cb_spec_linebreaks = QCheckBox("—  ")
        self.cb_spec_linebreaks.setChecked(self.is_spec_linebreaks_shown)
        self.cb_spec_linebreaks.setToolTip("Denote special linebreaks with horizontal lines in the preview window")
        self.cb_spec_linebreaks.stateChanged.connect(self.cb_spec_linebreaks_stateChanged)
        self.toolbar.addWidget(self.cb_spec_linebreaks)

        self.cb_synchronization = QCheckBox("⮅  ")
        self.cb_synchronization.setChecked(self.is_scrollbars_synchronized)
        self.cb_synchronization.setToolTip("Synchronize vertical scrolling")
        self.cb_synchronization.stateChanged.connect(self.cb_synchronization_stateChanged)
        self.toolbar.addWidget(self.cb_synchronization)

        self.cb_temp_notes = QCheckBox("🗒")
        self.cb_temp_notes.setChecked(self.is_editors_for_notes_shown)
        self.cb_temp_notes.setToolTip("Show fields for temporary notes")
        # self.cb_temp_notes.setShortcut("F11")
        self.cb_temp_notes.stateChanged.connect(self.cb_temp_notes_stateChanged)
        self.toolbar.addWidget(self.cb_temp_notes)

        # Create a spacer widget
        tb_spacer = QWidget()
        tb_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.tb_spacer_action = self.toolbar.addWidget(tb_spacer)          # Add spacer to the toolbar

        # Create a label to show counter
        self.lb_char_counter = QLabel("|счётчик:" if self.is_app_in_russian else "|counter:", self)
        self.lb_char_counter.setMinimumWidth(300)
        self.lb_char_counter.setEnabled(False)
        self.lb_char_counter.setToolTip("Counter of characters: number of characters in the script editor window excluding linebreaks (including linebreaks) → similar in the preview window")
        self.lb_char_counter_action = self.toolbar.addWidget(self.lb_char_counter)


    def create_main_editors_and_layouts(self):
        # QScintilla editor 1 setup
        # ------------------------
        self.editor1 = QsciScintilla()         # Make instance of QsciScintilla class
        self.editor1.setUtf8(True)             # Set encoding to UTF-8
        self.editor1.setEolMode(QsciScintilla.EolMode.EolUnix)   # Set EOL character as '\n'

        self.editor1.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByBorder,    # wrap visualization at the end:  WrapFlagNone / WrapFlagByText / WrapFlagByBorder / WrapFlagInMargin
                                        startFlag=QsciScintilla.WrapVisualFlag.WrapFlagNone,    # wrap visualization at the start: WrapFlagNone / WrapFlagByText / WrapFlagInMargin
                                        indent=self.indent_text_wrapped)
        self.editor1.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentFixed)  # indentation mode:  WrapIndentFixed, WrapIndentSame, WrapIndentIndented
        self.editor1.setWrapMode(QsciScintilla.WrapMode.WrapWord if self.is_text_wrapped else QsciScintilla.WrapMode.WrapNone)     # text wrapping: WrapNone / WrapWord / WrapCharacter / WrapWhitespace

        self.editor1.setEdgeMode(QsciScintilla.EdgeMode.EdgeMultipleLines)  # set mode for vertical guideline work
        self.scroll_pos_1_remember = self.editor1.verticalScrollBar().value()

        self.editor1.marginClicked.connect(self.margin_markers_in_ed1_clicked)
        self.editor1.textChanged.connect(self.transpose_text_1to2)

        # Add custom lexer object
        self.lexer1 = GSElexer.GSElexer_text_raw(self.editor1)   # Create a lexer object from custom subclass
        self.editor1.setLexer(self.lexer1)                       # Install the lexer onto the editor

        # Create horizontal guideline for script editor (but don't yet connect it to a central widget)
        self.guideline_hor_in_ed1 = QFrame()                          # place a horizontal guideline in editor 1
        self.guideline_hor_in_ed1.setFrameShape(QFrame.Shape.HLine)   # Set the shape to horizontal line
        self.guideline_hor_in_ed1.setStyleSheet(f"color: {self.guidelines1_color.name()}")   # Change color of the guideline


        # QScintilla editor 2 setup
        # ------------------------
        self.editor2 = QsciScintilla()
        self.editor2.setUtf8(True)             # Set encoding to UTF-8
        self.editor2.setEolMode(QsciScintilla.EolMode.EolUnix)    # set EOL character as '\n'

        self.editor2.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByBorder,    # wrap visualization at the end:  WrapFlagNone / WrapFlagByText / WrapFlagByBorder / WrapFlagInMargin
                                        startFlag=QsciScintilla.WrapVisualFlag.WrapFlagNone,    # wrap visualization at the start: WrapFlagNone / WrapFlagByText / WrapFlagInMargin
                                        indent=self.indent_text_wrapped)
        self.editor2.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentFixed)  # indentation modes:  WrapIndentFixed, WrapIndentSame, WrapIndentIndented
        self.editor2.setWrapMode(QsciScintilla.WrapMode.WrapWord if self.is_text_wrapped else QsciScintilla.WrapMode.WrapNone)     # wrap modes: WrapNone / WrapWord / WrapCharacter / WrapWhitespace

        self.editor2.setEdgeMode(QsciScintilla.EdgeMode.EdgeMultipleLines)  # set mode for vertical guideline work

        self.editor2.marginClicked.connect(self.margin_markers_in_ed2_clicked)

        # Add custom lexer object
        self.lexer2 = GSElexer.GSElexer_text_transformed(self.editor2, editor_with_script=self.editor1)  # pass to the lexer link to the editor with script
        self.editor2.setLexer(self.lexer2)                              # Install the lexer onto the editor

        # Create horizontal guideline for preview windows (but don't yet connect it to a central widget)
        self.guideline_hor_in_ed2 = QFrame()                          # place a horizontal guideline in editor 2
        self.guideline_hor_in_ed2.setFrameShape(QFrame.Shape.HLine)
        self.guideline_hor_in_ed2.setStyleSheet(f"color: {self.guidelines2_color.name()}")


        # set marker set for the marker margin in editor 1
        # ------------------------
        sym_0 = QImage("images/sym_0.png").scaled(QSize(16, 16))
        sym_1 = QImage("images/sym_1.png").scaled(QSize(16, 16))
        sym_2 = QImage("images/sym_2.png").scaled(QSize(16, 16))
        sym_3 = QImage("images/sym_3.png").scaled(QSize(16, 16))
        sym_4 = QImage("images/sym_4.png").scaled(QSize(16, 16))
        sym_5 = QImage("images/sym_5.png").scaled(QSize(16, 16))
        sym_6 = QImage("images/sym_6.png").scaled(QSize(16, 16))
        sym_7 = QImage("images/sym_7.png").scaled(QSize(16, 16))
        for i, sym in enumerate((sym_0, sym_1, sym_2, sym_3, sym_4, sym_5, sym_6, sym_7)):
            self.editor1.markerDefine(sym, i)
            self.editor2.markerDefine(sym, i)


        # Splitter for main editors setup
        # ------------------------
        self.splitter_editors = QSplitter(Qt.Orientation.Horizontal)
        self.splitter_editors.addWidget(self.editor1)
        self.splitter_editors.addWidget(self.editor2)
        self.splitter_editors.setSizes([int(100 * self.ratio_editor1_to_editor2), 100])


        # Text fields for notes and their splitter setup
        # ------------------------
        self.notes_field1 = QTextEdit()
        self.notes_field1.setPlaceholderText("Write here something smart")
        self.notes_field2 = QTextEdit()
        self.notes_field2.setPlaceholderText("And here write something even smarter")
        self.splitter_notes = QSplitter(Qt.Orientation.Horizontal)
        self.splitter_notes.setMinimumHeight(25)        # minimum height of the fields for notes
        self.splitter_notes.addWidget(self.notes_field1)
        self.splitter_notes.addWidget(self.notes_field2)
        self.splitter_notes.setSizes([int(100 * self.ratio_editor1_to_editor2), 100])


        # Layout of widgets
        # ------------------------
        self.splitter_central = QSplitter(Qt.Orientation.Vertical)
        self.splitter_central.addWidget(self.splitter_editors)
        self.splitter_central.addWidget(self.splitter_notes)
        self.splitter_central.setSizes(self.splitter_central_ratio if self.is_editors_for_notes_shown else
                                       [sum(self.splitter_central_ratio), 0])
        self.splitter_central.setStretchFactor(0, 1)   # When a user change the total height of the app window,
        self.splitter_central.setStretchFactor(1, 0)   # only main editors change their height
        self.splitter_central.splitterMoved.connect(self.splitter_central_moved)  # track and handle moving of the splitter

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter_central)


        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)

        # Attach both horizontal guidelines to the central widget
        self.guideline_hor_in_ed1.setParent(self.central_widget)  # Set parent of horizontal guideline 1 to main widget
        self.guideline_hor_in_ed2.setParent(self.central_widget)  # Set parent of horizontal guideline 1 to main widget


        self.setCentralWidget(self.central_widget)



    def show_app_and_initialize_its_state(self):
        self.show()

        # The function allows to configure margins in a QScintilla editor (script editor or preview window)
        def initial_setting_of_margins_in_editor(editor, margin_font, margin_font_color, margin_numbers_bg, is_markers_field_shown=True, margin_markers_bg=None):
            editor.setMarginsFont(margin_font)
            editor.setMarginsForegroundColor(margin_font_color)  # color of text in margins
            editor.setMarginsBackgroundColor(margin_numbers_bg)  # color of background in margins
            editor.setMargins(2)
            editor.setMarginType(1, QsciScintilla.MarginType.SymbolMarginColor)  # this allows to define an arbitrary color to a specific margin
            editor.setMarginBackgroundColor(1, margin_markers_bg)  # background for a single margin, but this function works only in some cases
            editor.setMarginSensitivity(1, True)  # make the symbol margin sensitive to clicks

        # delay redundant variables
        del self.app_title, self.app_position_x, self.app_position_y, self.app_width, self.app_height #, self.original_text  # these variables are not required anymore

        # preview window allow only see text but not edit it
        self.editor2.setReadOnly(True)

        # configure initial states of margins in editors
        initial_setting_of_margins_in_editor(self.editor1, self.margin1_font, self.margin1_font_color, self.margin1_numbers_bg,
                                             margin_markers_bg=self.margin1_markers_bg)   # Initial setting of margins in QScintilla editor 1
        initial_setting_of_margins_in_editor(self.editor2, self.margin2_font, self.margin2_font_color, self.margin2_numbers_bg,
                                             margin_markers_bg=self.margin2_markers_bg)   # Initial setting of margins in QScintilla editor 2

        # configure initial state of vertical guideline in the script editor
        self.is_v_guidelines_shown_in_ed1 = not self.is_v_guidelines_shown_in_ed1
        self.vert_guidelines_visibility_changed_in_ed1()

        # configure initial state of vertical guideline in the preview window
        self.is_v_guidelines_shown_in_ed2 = not self.is_v_guidelines_shown_in_ed2
        self.vert_guidelines_visibility_changed_in_ed2()

        # configure initial state of horizontal guideline in the script editor
        self.is_h_guidelines_shown_in_ed1 = not self.is_h_guidelines_shown_in_ed1
        if self.is_h_guidelines_shown_in_ed1:
            self.splitter_editors.splitterMoved.connect(self.draw_hor_guideline_in_ed1)
            self.splitter_central.splitterMoved.connect(self.draw_hor_guideline_in_ed1)
        self.hor_guideline_visibility_changed_in_ed1()

        # configure initial state of horizontal guideline in the preview window
        self.is_h_guidelines_shown_in_ed2 = not self.is_h_guidelines_shown_in_ed2
        if self.is_h_guidelines_shown_in_ed2:
            self.splitter_editors.splitterMoved.connect(self.draw_hor_guideline_in_ed2)
            self.splitter_central.splitterMoved.connect(self.draw_hor_guideline_in_ed2)
        self.hor_guideline_visibility_changed_in_ed2()

        # set initial visibility of numbers margin in script editor
        self.is_margin_numbers_shown_in_ed1 = not self.is_margin_numbers_shown_in_ed1
        self.cb_margin_1n_stateChanged()

        # set initial visibility of marker margin in script editor
        self.is_margin_markers_shown_in_ed1 = not self.is_margin_markers_shown_in_ed1
        self.cb_margin_1m_stateChanged()

        # set initial visibility of numbers margin in preview window
        self.is_margin_numbers_shown_in_ed2 = not self.is_margin_numbers_shown_in_ed2
        self.cb_margin_2n_stateChanged()

        # set initial mode of text wrapping (in both editors simultaneously)
        self.is_text_wrapped = not self.is_text_wrapped
        self.cb_text_wrapping_stateChanged()

        # set initial mode of synchronization of vertical scrollbars in editors windows
        self.is_scrollbars_synchronized = not self.is_scrollbars_synchronized
        if self.is_counter_shown:
            self.editor1.selectionChanged.connect(self.count_ch_in_selected_text)  # ToDo: think, is that necessary?
        if self.is_scrollbars_synchronized:
            self.editor1.verticalScrollBar().valueChanged.connect(self.synchronize_editors_1to2)
        self.cb_synchronization_stateChanged()

        # set initial state of visibility of counter label
        self.is_counter_shown = not self.is_counter_shown
        if self.is_counter_shown:
            self.editor1.selectionChanged.connect(self.count_ch_in_selected_text)
        self.counter_of_chars_visibility_changed()

        # change language of lettering to Russian is this language is chosen for the app initialization
        if self.is_app_in_russian:
            self.is_app_in_russian = False
            self.change_app_lang()


        self.editor1.setText(self.original_text)  # if to place the text earlier, there will be a micro-bug with the initial state of the text in the script editor
        del self.original_text

        # transpose original text from script editor to preview window according to given rules
        self.transpose_text_1to2()

        # Show horizontal lines for special linebreaks.
        # This block of code has to be executed after function 'transpose_text_1to2' otherwise there will be the bug.
        self.is_spec_linebreaks_shown = not self.is_spec_linebreaks_shown
        if self.is_spec_linebreaks_shown:
            self.splitter_editors.splitterMoved.connect(self.show_lines_for_special_linebreaks)
            self.splitter_central.splitterMoved.connect(self.show_lines_for_special_linebreaks)
            self.editor1.verticalScrollBar().valueChanged.connect(self.show_lines_for_special_linebreaks)
        self.cb_spec_linebreaks_stateChanged()


        # set initial visibility of numbers margin in script editor
        self.is_margin_numbers_shown_in_ed1 = not self.is_margin_numbers_shown_in_ed1
        self.cb_margin_1n_stateChanged()

        if not self.is_toolbar_movable:
            self.is_toolbar_movable = True
            self.toolbar_movable_action_state_changed()


    ######################################
    # Functions associated with menu items
    ######################################
    def load_text_from_file(self):
        if self.is_app_in_russian:
            fname, _ = QFileDialog.getOpenFileName(self, "Открыть файл со скриптом (в кодировке UTF-8)", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        else:
            fname, _ = QFileDialog.getOpenFileName(self, "Open File with Script (in encoding UTF-8)", "", "Text Files (*.txt);;All Files (*)")

        if fname:
            with open(fname, 'r', encoding='utf-8') as fh:
                new_text = fh.read()
                self.editor1.setText(new_text)

            # extract name of file from the full path to the file
            file_name = os.path.splitext(os.path.basename(fname))[0]
            self.setWindowTitle("GSE: " + file_name)


    def save_text_to_file(self):
        suggested_file_name = self.windowTitle()

        if self.is_app_in_russian:
            fname, _ = QFileDialog.getSaveFileName(self, "Сохранить текст в файл (будет использована кодировка UTF-8)", suggested_file_name, "Текстовые файлы (*.txt);;Все файлы (*)")
        else:
            fname, _ = QFileDialog.getSaveFileName(self, "Save Script to File (there will be used encoding UTF-8)", suggested_file_name, "Text Files (*.txt);;All Files (*)")

        if fname:
            text = self.editor1.text()
            with open(fname, 'w', encoding='utf-8') as fh:
                fh.write(text)


    def exit_app(self):
        '''Exit from the application'''
        self.close()


    def vert_guidelines_visibility_changed_in_ed1(self):
        '''Change visibility of vertical guidelines in the script editor. Inner functionality of QScintilla objects is used.'''
        self.is_v_guidelines_shown_in_ed1 = not self.is_v_guidelines_shown_in_ed1
        if self.is_v_guidelines_shown_in_ed1:
            self.editor1.addEdgeColumn(self.position_guidelines_vertical, self.guidelines1_color)  # set new vertical guidelines
        else:
            self.editor1.clearEdgeColumns()  # remove previous vertical guidelines


    def vert_guidelines_visibility_changed_in_ed2(self):
        '''Change visibility of vertical guidelines in the preview window. Inner functionality of QScintilla objects is used.'''
        self.is_v_guidelines_shown_in_ed2 = not self.is_v_guidelines_shown_in_ed2
        if self.is_v_guidelines_shown_in_ed2:
            self.editor2.addEdgeColumn(self.position_guidelines_vertical, self.guidelines2_color)  # set new vertical guidelines
        else:
            self.editor2.clearEdgeColumns()  # remove previous vertical guidelines


    def draw_hor_guideline_in_ed1(self):
        '''Draw horizontal guideline in the script editor.'''
        pos_hor_line_1 = self.editor1.textHeight(1) * self.position_guidelines_horizontal
        if pos_hor_line_1 > self.editor1.height() - 15:
            self.guideline_hor_in_ed1.hide()
        else:
            scrollbar_width_1 = self.editor1.verticalScrollBar().sizeHint().width()
            self.guideline_hor_in_ed1.setGeometry(self.splitter_central.x(), self.splitter_central.y() + pos_hor_line_1,
                                                  self.editor1.width() - scrollbar_width_1, 2)
            self.guideline_hor_in_ed1.show()


    def draw_hor_guideline_in_ed2(self):
        '''Draw horizontal guideline in the preview window.'''
        pos_hor_line_2 = self.editor2.textHeight(1) * self.position_guidelines_horizontal
        if pos_hor_line_2 > self.editor2.height() - 15:
            self.guideline_hor_in_ed2.hide()
        else:
            scrollbar_width_2 = self.editor2.verticalScrollBar().sizeHint().width()
            self.guideline_hor_in_ed2.setGeometry(self.splitter_central.x() + self.editor2.x(), self.splitter_central.y() + pos_hor_line_2,
                                                  self.editor2.width() - scrollbar_width_2, 2)
            self.guideline_hor_in_ed2.show()


    def hor_guideline_visibility_changed_in_ed1(self):
        '''Change visibility of horizontal guideline in the script editor.'''
        self.is_h_guidelines_shown_in_ed1 = not self.is_h_guidelines_shown_in_ed1
        if self.is_h_guidelines_shown_in_ed1:
            self.draw_hor_guideline_in_ed1()
            self.splitter_editors.splitterMoved.connect(self.draw_hor_guideline_in_ed1)  # repaint horizontal guidelines in editors when a user moves jumper in splitter
            self.splitter_central.splitterMoved.connect(self.draw_hor_guideline_in_ed1)
        else:
            self.guideline_hor_in_ed1.hide()
            self.splitter_editors.splitterMoved.disconnect(self.draw_hor_guideline_in_ed1)
            self.splitter_central.splitterMoved.disconnect(self.draw_hor_guideline_in_ed1)


    def hor_guideline_visibility_changed_in_ed2(self):
        '''Change visibility of horizontal guideline in the preview window.'''
        self.is_h_guidelines_shown_in_ed2 = not self.is_h_guidelines_shown_in_ed2
        if self.is_h_guidelines_shown_in_ed2:
            self.draw_hor_guideline_in_ed2()
            self.splitter_editors.splitterMoved.connect(self.draw_hor_guideline_in_ed2)  # repaint horizontal guidelines in editors when a user moves jumper in splitter
            self.splitter_central.splitterMoved.connect(self.draw_hor_guideline_in_ed2)
        else:
            self.guideline_hor_in_ed2.hide()
            self.splitter_editors.splitterMoved.disconnect(self.draw_hor_guideline_in_ed2)
            self.splitter_central.splitterMoved.disconnect(self.draw_hor_guideline_in_ed2)


    def sb_v_guideline_valueChanged(self):
        '''Move the vertical guidelines to the new position.
           If both vertical guidelines are turned off, turn them on.'''
        self.position_guidelines_vertical = self.sb_v_guideline.value()

        if self.is_v_guidelines_shown_in_ed1:
            self.editor1.clearEdgeColumns()   # remove previous vertical guideline
            self.editor1.addEdgeColumn(self.position_guidelines_vertical, self.guidelines1_color)  # set a new vertical guideline
        if self.is_v_guidelines_shown_in_ed2:
            self.editor2.clearEdgeColumns()
            self.editor2.addEdgeColumn(self.position_guidelines_vertical, self.guidelines2_color)
        # if neither of guidelines is shown, turn on their display
        if not self.is_v_guidelines_shown_in_ed1 and not self.is_v_guidelines_shown_in_ed2:
            self.v_guideline_show_ed1_action.setChecked(True)
            self.v_guideline_show_ed2_action.setChecked(True)
            self.vert_guidelines_visibility_changed_in_ed1()
            self.vert_guidelines_visibility_changed_in_ed2()


    def sb_h_guideline_valueChanged(self):
        '''Move the horizontal guidelines to the new position.
           If both horizontal guidelines are turned off, turn them on.'''
        self.position_guidelines_horizontal = self.sb_h_guideline.value()

        if self.is_h_guidelines_shown_in_ed1:
            self.draw_hor_guideline_in_ed1()
        if self.is_h_guidelines_shown_in_ed2:
            self.draw_hor_guideline_in_ed2()
        # if neither of guidelines is shown, turn on their showing
        if not self.is_h_guidelines_shown_in_ed1 and not self.is_h_guidelines_shown_in_ed2:
            self.h_guideline_in_ed1_show_action.setChecked(True)
            self.h_guideline_in_ed2_show_action.setChecked(True)
            self.hor_guideline_visibility_changed_in_ed1()
            self.hor_guideline_visibility_changed_in_ed2()


    def cb_margin_1n_stateChanged(self):
        '''Changed visibility of margin with line numbers in the script editor'''
        self.is_margin_numbers_shown_in_ed1 = not self.is_margin_numbers_shown_in_ed1
        self.editor1.setMarginWidth(0, self.margin1_number_width if self.is_margin_numbers_shown_in_ed1 else 0)


    def cb_margin_1m_stateChanged(self):
        '''Changed visibility of margin with markers in the script editor'''
        self.is_margin_markers_shown_in_ed1 = not self.is_margin_markers_shown_in_ed1
        self.editor1.setMarginWidth(1, 20 if self.is_margin_markers_shown_in_ed1 else 0)


    def cb_margin_2n_stateChanged(self):
        '''Changed visibility of margin with line numbers in the preview window'''
        self.is_margin_numbers_shown_in_ed2 = not self.is_margin_numbers_shown_in_ed2
        self.editor2.setMarginWidth(0, self.margin2_number_width if self.is_margin_numbers_shown_in_ed2 else 0)
        if self.is_spec_linebreaks_shown:
            QApplication.processEvents()  # This command is required to change in the editor take action
                                          # before further processing of the code, otherwise will be a temporary bug
            self.show_lines_for_special_linebreaks()

    def cb_margin_2m_stateChanged(self):
        '''Changed visibility of margin with markers in the script editor'''
        self.is_margin_markers_shown_in_ed2 = not self.is_margin_markers_shown_in_ed2
        self.editor2.setMarginWidth(1, 20 if self.is_margin_markers_shown_in_ed2 else 0)
        if self.is_spec_linebreaks_shown:
            QApplication.processEvents()  # This command is required to change in the editor take action
                                          # before further processing of the code, otherwise will be a temporary bug
            self.show_lines_for_special_linebreaks()

    def cb_spec_linebreaks_stateChanged(self):
        '''Changed mode of denotation of special linebreaks'''
        self.is_spec_linebreaks_shown = not self.is_spec_linebreaks_shown
        if self.is_spec_linebreaks_shown:
            self.show_lines_for_special_linebreaks()
            self.editor2.verticalScrollBar().valueChanged.connect(self.show_lines_for_special_linebreaks)
            self.splitter_editors.splitterMoved.connect(self.show_lines_for_special_linebreaks)
            self.splitter_central.splitterMoved.connect(self.show_lines_for_special_linebreaks)
        else:
            for ob_spec_linebreaks in self.ls_obs_spec_linebreaks:  #hide oll objects represented horizontal lines for special linebreak tags
                ob_spec_linebreaks.hide()
            self.editor2.verticalScrollBar().valueChanged.disconnect(self.show_lines_for_special_linebreaks)
            self.splitter_editors.splitterMoved.disconnect(self.show_lines_for_special_linebreaks)
            self.splitter_central.splitterMoved.disconnect(self.show_lines_for_special_linebreaks)


    def show_lines_for_special_linebreaks(self):

        # step 1: Take text from editor 1, find all linebreaks and determine lines
        # where special linebreaks are located (indexing starts from 1)
        text = self.editor1.text()
        matches_linebreaks = self.compiled_re_linebreaks.finditer(text)
        ls_spec_linebreak_tags_numbers = [i for i, match in enumerate(matches_linebreaks, start=1)
                                          if match.group() in self.tp_tags_linebreak_special]

        # step 2: Determine area that is shown in the preview window at this moment
        first_visible_line = self.editor2.SendScintilla(QsciScintilla.SCI_GETFIRSTVISIBLELINE)
        nmb_lines_on_screen = self.editor2.SendScintilla(QsciScintilla.SCI_LINESONSCREEN)
        last_visible_line = first_visible_line + nmb_lines_on_screen

        uppermost_doc_line = self.editor2.SendScintilla(QsciScintilla.SCI_DOCLINEFROMVISIBLE, first_visible_line)
        lowermost_doc_line = self.editor2.SendScintilla(QsciScintilla.SCI_DOCLINEFROMVISIBLE, last_visible_line)  # The last line that completely shown.

        # step 3: Place horizontal line objects from list 'self.nmb_lines_on_screen' to according positions.
        # If there are not enough line objects in the list, create new ones.
        # If amount of line objects is redundant, hide not used ones.
        c = 0    # counter of visible special linebreaks to process
        single_line_height = self.editor2.textHeight(1)  # height of a single line in the preview window
        scrollbar_width_2 = self.editor2.verticalScrollBar().sizeHint().width()   # width of scroll bar in the preview window
        margin_width_2 = self.editor2.marginWidth(0) + self.editor2.marginWidth(1)  # summary width of both margins in editor 2
        indent_x_drawn_line = self.splitter_central.x() + self.editor2.x() + margin_width_2 + 1  # horizontal indent of the beginning of line drawing

        # length of the line is minimal between space till vertical guideline and width of the preview window
        width_single_character = QFontMetrics(self.editor2_font).horizontalAdvance('A')
        line_width_till_vertical_guideline = width_single_character * self.position_guidelines_vertical
        line_width_from_editor_size = self.editor2.width() - margin_width_2 - scrollbar_width_2 - 2
        width_drawn_line = min(line_width_till_vertical_guideline, line_width_from_editor_size)

        # draw horizontal separators for special line tags one by one
        for tag in ls_spec_linebreak_tags_numbers:
            if tag < uppermost_doc_line:
                continue
            elif tag > lowermost_doc_line:
                break
            else:
                if len(self.ls_obs_spec_linebreaks) <= c:       #↑ If there are not enough line objects in the list, create new ones
                    new_line_obj = QFrame()                         # create a new horizontal separator (horizontal line)
                    new_line_obj.setFrameShape(QFrame.Shape.HLine)  # set the shape to horizontal line
                    new_line_obj.setStyleSheet(f"color: {self.spec_linebreaks_in_ed2_color_name}")   # change color of the separator
                    new_line_obj.setParent(self.central_widget)     # set parent of the new separator to main widget
                    self.ls_obs_spec_linebreaks.append(new_line_obj)  # append the new object to the list of such objects

                indent_y_drawn_line = single_line_height * (self.editor2.SendScintilla(QsciScintilla.SCI_VISIBLEFROMDOCLINE, tag) - first_visible_line)
                self.ls_obs_spec_linebreaks[c].setGeometry(indent_x_drawn_line, self.splitter_central.y() + indent_y_drawn_line, width_drawn_line, 2)
                self.ls_obs_spec_linebreaks[c].show()
                c += 1

        if len(self.ls_obs_spec_linebreaks) > c:                #↑ If amount of line objects is redundant, hide not used ones
            for k in range(c, len(self.ls_obs_spec_linebreaks)):
                self.ls_obs_spec_linebreaks[k].hide()


    def cb_text_wrapping_stateChanged(self):
        '''Changed wrapping mode of text. The change affects the both editors.'''
        # print('set_text_wrapping_mode works')
        self.is_text_wrapped = not self.is_text_wrapped
        if self.is_text_wrapped:
            self.editor1.setWrapMode(QsciScintilla.WrapMode.WrapWord)
            self.editor2.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        else:
            self.editor1.setWrapMode(QsciScintilla.WrapMode.WrapNone)
            self.editor2.setWrapMode(QsciScintilla.WrapMode.WrapNone)

        # if lines for special linebreaks are shown, redraw them
        if self.is_spec_linebreaks_shown:
            QApplication.processEvents()  # This command is required to change of wrap mode in the editor take action
                                          # before further processing of the code, otherwise will be a temporary bug
            self.show_lines_for_special_linebreaks()


    def sb_wrap_indent_valueChanged(self):
        '''Changed text wrapping indent.
           if text wrapping mode if off, turn it on.'''
        self.indent_text_wrapped = self.sb_wrap_indent.value()
        self.editor1.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByBorder, indent=self.indent_text_wrapped)
        self.editor2.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByBorder, indent=self.indent_text_wrapped)
        if not self.is_text_wrapped:
            self.cb_text_wrapping.setChecked(True)


    def cb_synchronization_stateChanged(self):
        # Changed synchronization of vertical scrollbars in editors.
        self.is_scrollbars_synchronized = not self.is_scrollbars_synchronized
        if self.is_scrollbars_synchronized:
            self.scroll_pos_1_remember = self.editor1.verticalScrollBar().value()
            self.editor1.verticalScrollBar().valueChanged.connect(self.synchronize_editors_1to2)
        else:
            self.editor1.verticalScrollBar().valueChanged.disconnect(self.synchronize_editors_1to2)


    def synchronize_editors_1to2(self, value):
        '''Implementation of synchronization of vertical scrolling in editors.'''
        delta = value - self.scroll_pos_1_remember
        self.scroll_pos_1_remember = value
        scroll_pos_2 = self.editor2.verticalScrollBar().value()
        self.editor2.verticalScrollBar().setValue(scroll_pos_2 + delta)


    def counter_of_chars_visibility_changed(self):
        '''Changed visibility of label containing info about number in characters in text / selection.'''
        self.is_counter_shown = not self.is_counter_shown
        if self.is_counter_shown:
            self.lb_char_counter_action.setVisible(True)
            self.editor1.selectionChanged.connect(self.count_ch_in_selected_text)
        else:
            self.lb_char_counter_action.setVisible(False)
            self.editor1.selectionChanged.disconnect(self.count_ch_in_selected_text)


    def change_app_lang(self):
        # .setText("")
        self.is_app_in_russian = not self.is_app_in_russian

        if self.is_app_in_russian:   # if language of the application is Russian
            self.file_menu.setTitle("Файл")
            self.load_action.setText("Загрузить скрипт из файла")
            self.save_action.setText("Сохранить скрипт в файл")
            self.exit_action.setText("Выход")
            self.guidelines_menu.setTitle("Ограничители")
            self.v_guideline_show_ed1_action.setText("Показать вертикальный мягкий ограничитель в редакторе скрипта")
            self.v_guideline_show_ed2_action.setText("Показать вертикальный мягкий ограничитель в окне предосмотра")
            self.h_guideline_in_ed1_show_action.setText("Показать горизонтальный мягкий ограничитель в редакторе скрипта")
            self.h_guideline_in_ed2_show_action.setText("Показать горизонтальный мягкий ограничитель в окне предосмотра")
            self.other_menu.setTitle("Прочее")
            self.toolbar_show_action.setText("Отображать панель инструментов")
            self.toolbar_movable_action.setText("Панель инструментов перемещаема")
            self.counter_of_chars_show_action.setText("Отображать счётчик символов")
            self.lang_of_app_change_action.setText("Change language to English")
            self.toolbar.setWindowTitle("Панель инструментов")
            self.lb_guidelines.setText("Ограничители:")
            self.sb_v_guideline.setToolTip("Позиция вертикального мягкого ограничителя")
            self.sb_h_guideline.setToolTip("Позиция горизонтального мягкого ограничителя")
            self.lb_margins.setText(" Поля: ")
            self.cb_margin_1n.setToolTip("Показать поле с номерами строк в редакторе скрипта")
            self.cb_margin_1m.setToolTip("Показать поле с маркерами в редакторе скрипта")
            self.cb_margin_2n.setToolTip("Показать поле с номерами строк в окне предосмотра")
            self.cb_margin_2m.setToolTip("Показать поле с маркерами в окне предосмотра")
            self.lb_text_wrapping.setText("Перенос текста: ")
            self.cb_text_wrapping.setToolTip("Перенос текста")
            self.sb_wrap_indent.setToolTip("Величина отступа при переносе текста")
            self.lb_other.setText("Прочее: ")
            self.cb_spec_linebreaks.setToolTip("Обозначить теги специального переноса строк горизонтальными линиями в окне предостмотра")
            self.cb_synchronization.setToolTip("Синхронизировать вертикальную прокрутку редактора скрипта и окна предосмотра")
            self.cb_temp_notes.setToolTip("Отобразить поля для временных заметок")
            self.lb_char_counter.setToolTip("Счётчик символов: количество символов в окне редактора скрипта без учёта символов переноса строк (с учётом переноса строк) → аналогично в окне предосмотра")
            self.notes_field1.setPlaceholderText("Сохрани здесь умную заметку на время")
            self.notes_field2.setPlaceholderText("А здесь следующую")
            self.lb_char_counter.setText(f"|счётчик:" + self.lb_char_counter.text().split(':', maxsplit=1)[1])
        else:         # if language of the application is English
            self.file_menu.setTitle("File")
            self.load_action.setText("Load script from file")
            self.save_action.setText("Save script to file")
            self.exit_action.setText("Exit")
            self.guidelines_menu.setTitle("Guidelines")
            self.v_guideline_show_ed1_action.setText("Show vertical guideline in script editor")
            self.v_guideline_show_ed2_action.setText("Show vertical guideline in preview window")
            self.h_guideline_in_ed2_show_action.setText("Show horizontal guideline in script editor")
            self.h_guideline_in_ed2_show_action.setText("Show horizontal guideline in preview window")
            self.other_menu.setTitle("Other")
            self.toolbar_show_action.setText("Show toolbar")
            self.toolbar_movable_action.setText("Toolbar is movable")
            self.counter_of_chars_show_action.setText("Show counter of characters")
            self.lang_of_app_change_action.setText("Сменить язык на русский")
            self.toolbar.setWindowTitle("ToolBar")
            self.lb_guidelines.setText("Guidelines:")
            self.sb_v_guideline.setToolTip("Position of vertical guidelines")
            self.sb_h_guideline.setToolTip("Position of horizontal guidelines")
            self.lb_margins.setText(" Margins: ")
            self.cb_margin_1n.setToolTip("Show number field in the script editor")
            self.cb_margin_1m.setToolTip("Show marker field in the script editor")
            self.cb_margin_2n.setToolTip("Show number field in the preview window")
            self.cb_margin_2m.setToolTip("Show marker field in the preview window")
            self.lb_text_wrapping.setText("Text wrapping: ")
            self.cb_text_wrapping.setToolTip("Text wrapping")
            self.sb_wrap_indent.setToolTip("indentation of text wrapping")
            self.lb_other.setText("Other: ")
            self.cb_spec_linebreaks.setToolTip("Denote special linebreaks with horizontal lines in the preview window")
            self.cb_synchronization.setToolTip("Synchronize vertical scrolling")
            self.cb_temp_notes.setToolTip("Show fields for temporary notes")
            self.lb_char_counter.setToolTip("Counter of characters: number of characters in the script editor window excluding linebreaks (including linebreaks) → similar in the preview window")
            self.notes_field1.setPlaceholderText("Write here something smart")
            self.notes_field2.setPlaceholderText("And here write something even smarter")
            self.lb_char_counter.setText(f"|counter:" + self.lb_char_counter.text().split(':', maxsplit=1)[1])


    def toolbar_visibility_changed(self):
        '''Change visibility of the toolbar.'''
        self.is_toolbar_shown = not self.is_toolbar_shown
        self.toolbar.setVisible(self.is_toolbar_shown)

        # Show/hide horizontal guidelines and lines for special linebreaks
        if self.is_h_guidelines_shown_in_ed1:
            self.draw_hor_guideline_in_ed1()
        if self.is_h_guidelines_shown_in_ed2:
            self.draw_hor_guideline_in_ed2()
        if self.is_spec_linebreaks_shown:
            self.show_lines_for_special_linebreaks()


    def cb_temp_notes_stateChanged(self):
        self.is_editors_for_notes_shown = not self.is_editors_for_notes_shown
        if self.is_editors_for_notes_shown:
            self.splitter_central.setSizes(self.splitter_central_ratio)
        else:
            self.splitter_central.setSizes([sum(self.splitter_central_ratio), 0])

        # Show/hide horizontal guidelines and lines for special linebreaks
        if self.is_h_guidelines_shown_in_ed1:
            self.draw_hor_guideline_in_ed1()
        if self.is_h_guidelines_shown_in_ed2:
            self.draw_hor_guideline_in_ed2()
        if self.is_spec_linebreaks_shown:
            self.show_lines_for_special_linebreaks()


    def toolbar_movable_action_state_changed(self):
        self.is_toolbar_movable = not self.is_toolbar_movable
        self.toolbar.setMovable(self.is_toolbar_movable)


    def fn_about_action(self):
        print('Work')
        msg = QMessageBox(self)

        if self.is_app_in_russian:
            msg.setWindowTitle("О программе")
            msg.setText("GameScriptEditor является специализированным текстовым редактором для работы со скриптами." +\
                        "\n\nv1.0" +\
                        "\nРазработчик: Мальвина Пушкова <lady3mlnm@gmail.com>")
        else:
            msg.setWindowTitle("About the program")
            msg.setText("GameScriptEditor is a specialized text editor for working with scripts." +\
                        "\n\nv1.0" +\
                        "\nDeveloper: Malvina Pushkova <lady3mlnm@gmail.com>")

        msg.exec()


    def fn_test_action(self):
        x = 'Text to show in the note window 2'
        self.notes_field2.setText(x)

        print('fn_test_action works')



    ##################################
    # Functions that are triggered by change of geometry of the main window or splitters
    ##################################

    def resizeEvent(self, event):
        """ Resize correctly horizontal guidelines if user change geometry of the main window"""
        super().resizeEvent(event)
        if self.is_h_guidelines_shown_in_ed1:
            self.draw_hor_guideline_in_ed1()
        if self.is_h_guidelines_shown_in_ed2:
            self.draw_hor_guideline_in_ed2()
        if self.is_spec_linebreaks_shown:
            self.show_lines_for_special_linebreaks()


    def splitter_central_moved(self):
        '''An user change state of the splitter between the major editors of the app and editors for temporary notes'''
        new_splitter_central_ratio = self.splitter_central.sizes()
        height_notes_section = new_splitter_central_ratio[1]

        if height_notes_section:    # if height of the section for notes is not 0, that means that editors for temporary notes are shown
            self.splitter_central_ratio = new_splitter_central_ratio
            if not self.is_editors_for_notes_shown:  # if the app was in mode of hiding of editors for temporary notes, move it to the mode of displaying them
                self.cb_temp_notes.stateChanged.disconnect(self.cb_temp_notes_stateChanged)
                self.cb_temp_notes.setChecked(True)
                self.is_editors_for_notes_shown = True
                self.cb_temp_notes.stateChanged.connect(self.cb_temp_notes_stateChanged)
        else:   # if height of the section for notes is 0, that means that editors for temporary notes are hidden
            if self.is_editors_for_notes_shown:  # if the app was in mode of displaying of editors for temporary notes, turn off this mode
                self.cb_temp_notes.stateChanged.disconnect(self.cb_temp_notes_stateChanged)
                self.cb_temp_notes.setChecked(False)
                self.is_editors_for_notes_shown = False
                self.cb_temp_notes.stateChanged.connect(self.cb_temp_notes_stateChanged)



    ##################################
    # Other functions
    ##################################

    def transpose_text_1to2(self):
        '''The function takes script from the script editor, transforms it according to given rules,
           and places result to the preview window.'''
        position_scroll2 = self.editor2.verticalScrollBar().value()  # save current position of scrollbar in editor 2

        text = self.editor1.text()
        nmb_ch_in_editor1 = len(text)
        nmb_of_linebreaks1 = text.count('\n')

        text = re.sub(self.pattern_to_hide_chars_between_tags, '', text)
        text = re.sub(self.pattern_design_tags, '', text)  # make replacement in text according to given rules
        text = re.sub(self.pattern_replace, lambda match: self.dd_tags_replacement_extended[match.group(0)], text)

        # if margin for markers in the preview window is shown, then store all markers to dictionary,
        # place transformed text to the preview window and restore markers.
        # Otherwise, just restore markers.
        if self.is_margin_markers_shown_in_ed2:
            dd = dict()
            line = 0
            while line >= 0:
                line = self.editor2.markerFindNext(line, 0b11111111)
                if line >= 0:
                    dd[line] = int(math.log2(self.editor2.markersAtLine(line)))
                    line += 1

            self.editor2.setText(text)

            for line, marker in dd.items():
                self.editor2.markerAdd(line, marker)
        else:
            self.editor2.setText(text)

        self.editor2.verticalScrollBar().setSliderPosition(position_scroll2)  # restore position of the scrollbar

        # during operations with text number of lines and their positions can change, so adjust separators for tags of special lines
        if self.is_spec_linebreaks_shown:
            self.show_lines_for_special_linebreaks()

        # count and show number of characters in both editors (excluding and including linebreaks)
        nmb_ch_in_editor2 = len(text)
        nmb_of_linebreaks2 = text.count('\n')

        self.lb_char_counter.setText(f"|{'счётчик' if self.is_app_in_russian else 'counter'}: {nmb_ch_in_editor1 - nmb_of_linebreaks1} ({nmb_ch_in_editor1})  →  {nmb_ch_in_editor2 - nmb_of_linebreaks2} ({nmb_ch_in_editor2})")



    def count_ch_in_selected_text(self):
        '''When a user selected text, the function counts number of selected characters in the raw script and
           in game script after transformation. If nothing is selected, the whole text in processed.'''
        def count_ch(txt):
            nmb_ch_in_editor1 = len(txt)
            nmb_of_linebreaks1 = txt.count('\n')
            txt = re.sub(self.pattern_design_tags, '', txt)  # make replacement in text according to given rules
            txt = re.sub(self.pattern_replace, lambda match: self.dd_tags_replacement_extended[match.group(0)], txt)
            nmb_ch_in_editor2 = len(txt)
            nmb_of_linebreaks2 = txt.count('\n')
            return nmb_ch_in_editor1, nmb_of_linebreaks1, nmb_ch_in_editor2, nmb_of_linebreaks2

        selected_text = self.editor1.selectedText()
        if selected_text == '':
            nmb_ch_in_editor1, nmb_of_linebreaks1, nmb_ch_in_editor2, nmb_of_linebreaks2 = count_ch(self.editor1.text())
            self.lb_char_counter.setText(f"|{'счётчик' if self.is_app_in_russian else 'counter'}: {nmb_ch_in_editor1 - nmb_of_linebreaks1} ({nmb_ch_in_editor1})  →  {nmb_ch_in_editor2 - nmb_of_linebreaks2} ({nmb_ch_in_editor2})")
        else:
            nmb_ch_in_editor1, nmb_of_linebreaks1, nmb_ch_in_editor2, nmb_of_linebreaks2 = count_ch(selected_text)
            self.lb_char_counter.setText(f"|{'выделение' if self.is_app_in_russian else 'selected'}: {nmb_ch_in_editor1 - nmb_of_linebreaks1} ({nmb_ch_in_editor1})  →  {nmb_ch_in_editor2 - nmb_of_linebreaks2} ({nmb_ch_in_editor2})")


    def margin_markers_in_ed1_clicked(self, margin_nr, line_nr, state):
        '''What is happened when a user clicks on the markers margin in the script editor.'''
        current_margin_state = self.editor1.markersAtLine(line_nr)

        if current_margin_state==0:
            marker = 1 if state == Qt.KeyboardModifier.ShiftModifier else \
                     2 if state == Qt.KeyboardModifier.ControlModifier else \
                     3 if state == Qt.KeyboardModifier.AltModifier else \
                     4 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier else \
                     5 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier else \
                     6 if state == Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.AltModifier else \
                     7 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.AltModifier else \
                     0

            self.editor1.markerAdd(line_nr, marker)
        else:
            self.editor1.markerDelete(line_nr, -1)


    def margin_markers_in_ed2_clicked(self, margin_nr, line_nr, state):
        '''What is happened when a user clicks on the markers margin in the script editor.'''
        current_margin_state = self.editor2.markersAtLine(line_nr)

        if current_margin_state==0:
            marker = 1 if state == Qt.KeyboardModifier.ShiftModifier else \
                     2 if state == Qt.KeyboardModifier.ControlModifier else \
                     3 if state == Qt.KeyboardModifier.AltModifier else \
                     4 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier else \
                     5 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier else \
                     6 if state == Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.AltModifier else \
                     7 if state == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.AltModifier else \
                     0

            self.editor2.markerAdd(line_nr, marker)
        else:
            self.editor2.markerDelete(line_nr, -1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myGUI = CustomMainWindow()
    sys.exit(app.exec())