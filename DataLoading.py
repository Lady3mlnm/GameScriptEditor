##########################################################################
# This module loaded initial state of the app from the file 'settings.ini'
##########################################################################

import configparser
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
import re
from DataStructures import *


def interpret_escaped_string(st):
    return st.encode('raw_unicode_escape').decode('unicode_escape')

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read('settings/settings.ini', encoding='UTF-8')



section_name = 'Application position and size'
t = config[section_name]['title']
app_title = t if (t != 'None') and (t != '') else False

app_position_x = config.getint(section_name, 'x')
app_position_y = config.getint(section_name, 'y')
app_width = config.getint(section_name, 'width')
app_height = config.getint(section_name, 'height')
ratio_editor1_to_editor2 = config.getfloat(section_name, 'proportion of editor 1 to editor 2')



section_name = 'Guidelines'
is_v_guidelines_shown_in_ed1 = config.getboolean(section_name, 'show vertical guideline in script editor')
is_v_guidelines_shown_in_ed2 = config.getboolean(section_name, 'show vertical guideline in preview window')
position_guidelines_vertical = config.getint(section_name, 'position of vertical guidelines, symbols')
is_h_guidelines_shown_in_ed1 = config.getboolean(section_name, 'show horizontal guideline in script editor')
is_h_guidelines_shown_in_ed2 = config.getboolean(section_name, 'show horizontal guidelines in preview window')
position_guidelines_horizontal = config.getint(section_name, 'position of horizontal guidelines, lines')



section_name = 'Settings of script editor'

def load_editor_theme(theme_name):
    config_theme = configparser.ConfigParser()  # Create a ConfigParser object
    config_theme.read(f"themes/{theme_name}.ini", encoding='UTF-8')  # Read the INI file

    section_name = 'Basic font and background'
    editor_font = QFont(config_theme[section_name]['font, name'],
                        config_theme.getint(section_name, 'font, size'),
                        weight=QFont.Weight.Bold if config_theme.getboolean(section_name, 'font, bold') else QFont.Weight.Normal,
                        italic=config_theme.getboolean(section_name, 'font, italic'))
    editor_text_color = QColor(config_theme[section_name]['font, color'])
    editor_bg_color = QColor(config_theme[section_name]['background color'])

    section_name = 'Margins'
    margin_font = QFont(config_theme[section_name]['margin font, name'],
                        config_theme.getint(section_name, 'margin font, size'),
                        weight=QFont.Weight.Bold if config_theme.getboolean(section_name, 'margin font, bold') else QFont.Weight.Normal,
                        italic=config_theme.getboolean(section_name, 'margin font, italic'))
    margin_font_color = QColor(config_theme[section_name]['margin font, color'])
    margin_numbers_bg = QColor(config_theme[section_name]['number margin, background color'])
    margin_markers_bg = QColor(config_theme[section_name]['marker margin, background color'])

    section_name = 'Lines'
    guidelines_color = QColor(config_theme[section_name]['color of vertical and horizontal guidelines'])
    spec_linebreaks_in_ed_color_name = config_theme[section_name]['color of horizontal lines for special linebreaks']

    return editor_font, editor_text_color, editor_bg_color, margin_font, margin_font_color, margin_numbers_bg, margin_markers_bg, guidelines_color, spec_linebreaks_in_ed_color_name

editor1_theme = config[section_name]['theme']
is_margin_numbers_shown_in_ed1 = config.getboolean(section_name, 'show line numbers')
is_margin_markers_shown_in_ed1 = config.getboolean(section_name, 'show margin for markers')

st = config[section_name]['number margin, width']
margin1_number_width = st if (st.startswith('\"') & st.endswith('\"')) or (st.startswith('\'') & st.endswith('\'')) else int(st)

# load settings of the theme for the window of script editing
editor1_font, editor1_text_color, editor1_bg_color, margin1_font, margin1_font_color, margin1_numbers_bg, margin1_markers_bg, guidelines1_color, spec_linebreaks_in_ed1_color_name \
    = load_editor_theme(editor1_theme)



section_name = 'Settings of preview window'
editor2_theme = config[section_name]['theme']
is_margin_numbers_shown_in_ed2 = config.getboolean(section_name, 'show line numbers')

st = config[section_name]['number margin, width']
margin2_number_width = st if (st.startswith('\"') & st.endswith('\"')) or (st.startswith('\'') & st.endswith('\'')) else int(st)

is_margin_markers_shown_in_ed2 = config.getboolean(section_name, 'show margin for markers')
is_spec_linebreaks_shown = config.getboolean(section_name, 'denote special linebreaks')
editor2_font, editor2_text_color, editor2_bg_color, margin2_font, margin2_font_color, margin2_numbers_bg, margin2_markers_bg, guidelines2_color, spec_linebreaks_in_ed2_color_name \
    = load_editor_theme(editor2_theme)



section_name = 'Other settings of the application interface'
is_text_wrapped = config.getboolean(section_name, 'text wrapping')
indent_text_wrapped = config.getint(section_name, 'indent used for wrapped lines, symbols')
is_scrollbars_synchronized = config.getboolean(section_name, 'synchronization of vertical scrollbars')
is_editors_for_notes_shown = config.getboolean(section_name, 'open text editors for notes')
is_toolbar_movable = config.getboolean(section_name, 'is toolbar movable')

position_of_toolbar = config[section_name]['position of toolbar']
dd_position = {
    'top'   : Qt.ToolBarArea.TopToolBarArea,
    'bottom': Qt.ToolBarArea.BottomToolBarArea
    # 'left'  : Qt.ToolBarArea.LeftToolBarArea,
    # 'right' : Qt.ToolBarArea.RightToolBarArea,
}
position_of_toolbar = dd_position[position_of_toolbar.lower()]

is_counter_shown = config.getboolean(section_name, 'show counter of characters')

# Language of the app. Only two options are possible now: 'Ru' or, otherwise, 'En'
is_app_in_russian = (config[section_name]['language of application'].capitalize() == 'Ru')



section_name = 'Editor 1: Styles for representation of tags'

# internal mini-function that determine whether a string represent True, False or None
ifn_determine_if_true_false_none = lambda x: True if (x=='True') else False if (x=='False') else None

def extract_ruleReplacement_from_string_simple(st):
    """
    The function transform string representation of simplified ruleReplacement object (without dictionary),
    that is contained in INI-file, to the such object
    """
    regex = r"text_color=(#?\w+), bg_color=(#?\w+), bold=(\w+), italic=(\w+)"  # Regular expression to extract the values
    match = re.search(regex, st)

    text_color = match.group(1)
    text_color = None if text_color == 'None' else QColor(text_color)

    bg_color = match.group(2)
    bg_color = None if bg_color == 'None' else QColor(bg_color)

    bold = match.group(3)
    bold = ifn_determine_if_true_false_none(bold)

    italic = match.group(4)
    italic = ifn_determine_if_true_false_none(italic)

    return ruleReplacement(text_color=text_color, bg_color=bg_color, bold=bold, italic=italic)

editor1_tags_style_replacement = extract_ruleReplacement_from_string_simple( config[section_name]['style of replacement tags'] )
editor1_tags_style_design      = extract_ruleReplacement_from_string_simple( config[section_name]['style of design tags'] )
editor1_tags_style_special     = extract_ruleReplacement_from_string_simple(config[section_name]['style of special tags'])



section_name = 'Special tags'
dd_tags_linebreak_usual = dict()
t = config.getboolean(section_name, 'ignore natural linebreaks in original script')
if t == True:
    dd_tags_linebreak_usual['\n'] = ''

t = config[section_name]['tags for linebreak']
if (t != 'None') and (t != ''):
    t = t.strip('()')
    for tag in t.split(' | '):
        dd_tags_linebreak_usual[tag] = '\n'

t = config[section_name]['tags for special linebreak']
if (t != 'None') and (t != ''):
    t = t.strip('()')
    for tag in t.split(' | '):
        dd_tags_linebreak_usual[tag] = '\n'
    tp_tags_linebreak_special = tuple(t.split(' | '))
else:
    tp_tags_linebreak_special = tuple()

t = config[section_name]['tags to hide digits between them']
tags_to_hide_content = t.strip().split(' | ') if (t != 'None') and (t != '') else []

is_hiding_tags_standard_5d = config.getboolean(section_name, 'hide tags of the pattern <00000>')

t = config[section_name]['additional pattern to hide content']
additional_pattern_to_hide_content = t if (t != 'None') and (t != '') else False



section_name = 'Replacement tags'

def extract_ruleReplacement_from_st(st):
    """
    The function transform string representation of a ruleReplacement object, that is contained in INI-file, to the such object
    """
    regex = r"{(.*)} - text_color=(#?\w+), bg_color=(#?\w+), bold=(\w+), italic=(\w+)"  # Regular expression to extract the values
    match = re.search(regex, st)

    dd_st = match.group(1)
    dd = {}
    for pair in dd_st.split(' | '):
        k, v = pair.split(' : ')
        dd[interpret_escaped_string(k)] = interpret_escaped_string(v)

    text_color = match.group(2)
    text_color = None if text_color == 'None' else QColor(text_color)

    bg_color = match.group(3)
    bg_color = None if bg_color == 'None' else QColor(bg_color)

    bold = match.group(4)
    bold = ifn_determine_if_true_false_none(bold)

    italic = match.group(5)
    italic = ifn_determine_if_true_false_none(italic)

    return ruleReplacement(dd, text_color=text_color, bg_color=bg_color, bold=bold, italic=italic)

global_rules_replacement = []
for _, v in config.items(section_name):
    global_rules_replacement.append(extract_ruleReplacement_from_st(v))



section_name = 'Design tags'

def extract_ruleDesign_from_st(st):
    """
    The function transform string representation of a ruleDesign object, that is contained in INI-file, to the such object
    """
    regex = r"\((.*) \| (.*)\) - text_color=(#?\w+), bg_color=(#?\w+), bold=(\w+), italic=(\w+)"  # Regular expression to extract the values
    match = re.search(regex, st)

    tag_open = interpret_escaped_string(match.group(1))

    tag_close = interpret_escaped_string(match.group(2))

    text_color = match.group(3)
    text_color = None if text_color == 'None' else QColor(text_color)

    bg_color = match.group(4)
    bg_color = None if bg_color == 'None' else QColor(bg_color)

    bold = match.group(5)
    bold = ifn_determine_if_true_false_none(bold)

    italic = match.group(6)
    italic = ifn_determine_if_true_false_none(italic)

    return ruleDesign(tag_open, tag_close, text_color=text_color, bg_color=bg_color, bold=bold, italic=italic)

global_rules_design = []
for _, v in config.items(section_name):
    global_rules_design.append(extract_ruleDesign_from_st(v))



section_name = 'Text loaded during loading'
name_of_file_with_text = config[section_name]['name of file with text']
name_of_file_with_text = name_of_file_with_text.strip("\'\"")
if (name_of_file_with_text != 'None') and (name_of_file_with_text != ''):
    with open(f"settings/{name_of_file_with_text}", 'r', encoding='UTF-8') as fh:
        original_text = fh.read()  #.replace("\n","\r\n")
else:
    original_text = ''



### Creation of additional data structures to facilitate further calculations
#-----------------------------------------
dd_tags_replacement = {k:v for rule in global_rules_replacement
                           for k, v in rule.dd_replacement.items()}

dd_tags_replacement_extended = {**dd_tags_linebreak_usual, **dd_tags_replacement}

tp_tags_service = tuple(dd_tags_linebreak_usual.keys())
# tp_tags_linebreak_special is created above

tp_tags_replacement = tuple(k for rule in global_rules_replacement
                              for k in rule.dd_replacement.keys())

tp_tags_replacement_extended = tp_tags_replacement + tp_tags_service

tp_tags_design_open = tuple(rule.tag_open for rule in global_rules_design)
tp_tags_design_close = tuple(rule.tag_close for rule in global_rules_design)
tp_tags_design_united = tp_tags_design_open + tp_tags_design_close

# tuple of tags that encode linebreak in raw script: tags of linebreaks + '\n' if it is not removed
tp_tags_linebreak = tuple(k for k, v in dd_tags_linebreak_usual.items() if v == '\n')
if '\n' not in dd_tags_linebreak_usual.keys():
    tp_tags_linebreak = ('\n', *tp_tags_linebreak)


if tags_to_hide_content:
    pattern_to_hide_chars_between_tags = tags_to_hide_content[0] + r"\d*?" + tags_to_hide_content[1]  # add r"(?s)"+... for multiline mode
else:
    pattern_to_hide_chars_between_tags = ''

if is_hiding_tags_standard_5d:
    if pattern_to_hide_chars_between_tags:
        pattern_to_hide_chars_between_tags += '|<\d{5}>'
    else:
        pattern_to_hide_chars_between_tags = '<\d{5}>'

if additional_pattern_to_hide_content:
    if pattern_to_hide_chars_between_tags:
        pattern_to_hide_chars_between_tags += '|' + additional_pattern_to_hide_content
    else:
        pattern_to_hide_chars_between_tags = additional_pattern_to_hide_content


# remove unnecessary further variables
del is_hiding_tags_standard_5d, additional_pattern_to_hide_content
