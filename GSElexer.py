from PyQt6.QtGui import QFont
from PyQt6.Qsci import *
import re
from DataLoading import (global_rules_replacement, global_rules_design, tags_to_hide_content, tp_tags_design_open, tp_tags_design_close, tp_tags_replacement,
                         tp_tags_service, tp_tags_replacement_extended, tp_tags_design_united, dd_tags_replacement, dd_tags_replacement_extended,
                         editor1_font, editor1_text_color, editor1_bg_color,
                         editor1_tags_style_special, editor1_tags_style_replacement, editor1_tags_style_design,
                         editor2_font, editor2_text_color, editor2_bg_color,
                         pattern_to_hide_chars_between_tags)

pattern_style = '(' + pattern_to_hide_chars_between_tags + '|' + \
                '|'.join(map(re.escape, tp_tags_service + tp_tags_design_open + tp_tags_design_close + tp_tags_replacement)) + ')'


class GSElexer_text_raw(QsciLexerCustom):

    def __init__(self, parent):
        super(GSElexer_text_raw, self).__init__(parent)
        self.text_font = editor1_font
        self.text_color = editor1_text_color
        self.bg_color = editor1_bg_color

        # Default text settings
        self.setDefaultFont(self.text_font)
        self.setDefaultColor(self.text_color)
        self.setDefaultPaper(self.bg_color)

        # Initialize fonts per style
        self.setFont(self.text_font, 0)

        # Initialize text colors per style
        self.setColor(self.text_color, 0)

        # Initialize background (paper) colors per style
        self.setPaper(self.bg_color, 0)

        for i, style in enumerate((editor1_tags_style_special,
                                   editor1_tags_style_replacement,
                                   editor1_tags_style_replacement,
                                   editor1_tags_style_design), start=1):
            self.setFont(QFont(self.text_font.family(),
                               self.text_font.pointSize(),
                               weight=self.text_font.weight() if style.bold is None else QFont.Weight.Bold if style.bold else QFont.Weight.Normal,
                               italic=style.italic if style.italic is not None else self.text_font.italic()), i)
            self.setColor(style.text_color if style.text_color is not None else self.text_color, i)
            self.setPaper(style.bg_color if style.bg_color is not None else self.bg_color, i)


    def language(self):   # name of the language
        return "Custom_GSE_text_raw"


    def description(self, style):   # descriptive name for a given style
        if style>=0 and style<=3:
            return "myStyle_" + str(style)
        return ""


    def styleText(self, start, end):   # Called everytime the editors text has changed
        # 1. Initialize the styling procedure
        self.startStyling(0)  # self.startStyling(start)

        # 2. Slice out a part from the text
        text = self.parent().text()  #[start:end]   # get text from the editor (as understand, QsciScintilla-object)

        # 3. Tokenize the text
        token_list = re.split(pattern_style, text)
        token_list = [ (token, len(bytearray(token, "utf-8"))) for token in token_list]
        # -> 'token_list' is a list of tuples: (token_name, token_len)

        # 4. Style the text in a loop
        # use: self.setStyling(number_of_chars, style_nr)
        for token in token_list:
            if token[0] in tp_tags_service:
                self.setStyling(token[1], 1)
            elif token[0] in tp_tags_replacement:
                self.setStyling(token[1], 2)
            elif token[0] in tp_tags_design_united:
                self.setStyling(token[1], 3)
            elif re.fullmatch(pattern_to_hide_chars_between_tags, token[0]) is not None:
                self.setStyling(token[1], 1)
            else:
                self.setStyling(token[1], 0)    # default style

        # Make sure that number of characters in the text is the same as in the 'token_list', so that the internal counter is in sync
        # sum_1 = len(bytearray(text, "utf-8"))
        # sum_2 = sum(token[1] for token in token_list)
        # print(f"{sum_1} vs {sum_2}")
        # print(token_list)
        # print()


class GSElexer_text_transformed(QsciLexerCustom):

    def __init__(self, parent, editor_with_script):
        super(GSElexer_text_transformed, self).__init__(parent)
        self.text_font = editor2_font
        self.text_color = editor2_text_color
        self.bg_color = editor2_bg_color
        self.editor_with_script = editor_with_script

        # Default text settings
        self.setDefaultFont(self.text_font)
        self.setDefaultColor(self.text_color)
        self.setDefaultPaper(self.bg_color)

        # Initialize fonts per style
        self.setFont(self.text_font, 0)

        # Initialize text colors per style
        self.setColor(self.text_color, 0)  # Style 0: black   # assign an attribute to style 0

        # Initialize background (paper) colors per style
        self.setPaper(self.bg_color, 0)  # Style 0: white

        self.dd_tag_to_style = {k: -1 for k in tp_tags_service}

        for i, rule in enumerate(global_rules_replacement, start = 1):
            self.setFont(QFont(self.text_font.family(),
                               self.text_font.pointSize(),
                               weight=self.text_font.weight() if rule.bold is None else QFont.Weight.Bold if rule.bold else QFont.Weight.Normal,
                               italic=rule.italic if rule.italic is not None else self.text_font.italic()), i)
            self.setColor(rule.text_color if rule.text_color is not None else self.text_color, i)
            self.setPaper(rule.bg_color if rule.bg_color is not None else self.bg_color, i)

            tags = rule.dd_replacement.keys()
            for tag in tags:
                self.dd_tag_to_style[tag] = i

        for i, rule in enumerate(global_rules_design, start = i+1):
            self.setFont(QFont(self.text_font.family(),
                               self.text_font.pointSize(),
                               weight=self.text_font.weight() if rule.bold is None else QFont.Weight.Bold if rule.bold else QFont.Weight.Normal,
                               italic=rule.italic if rule.italic is not None else self.text_font.italic()), i)
            self.setColor(rule.text_color if rule.text_color is not None else self.text_color, i)
            self.setPaper(rule.bg_color if rule.bg_color is not None else self.bg_color, i)
            self.dd_tag_to_style[rule.tag_open] = i


    def language(self):   # name of the language
        return "Custom_GSE_text_transformed"


    def description(self, style):   # descriptive name for a given style
        nmb_of_spec_styles = len(tp_tags_replacement) + len(tp_tags_design_open)
        if style >= 0 and style <= nmb_of_spec_styles:
            return "myStyle_" + str(style)
        return ""

    def styleText(self, start, end):   # Called everytime the editors text has changed
        # 1. Initialize the styling procedure
        self.startStyling(0)  # self.startStyling(start)

        # 2. Slice out a part from the text
        # text_transformed = self.parent().text()  #[start:end]   # get text from the editor (as understand, QsciScintilla-object)
        text_original = self.editor_with_script.text() #.editor1.text()

        # 3. Tokenize the text
        token_list = re.split(pattern_style, text_original)

        token_list = [ (token, len(bytearray(dd_tags_replacement_extended[token], "utf-8")) if token in tp_tags_replacement_extended else \
                               0 if token in tp_tags_design_united else \
                               len(bytearray(token, "utf-8")))
                                   for token in token_list]
        # -> 'token_list' is a list of tuples: (token_name, token_len)

        # 4. Style the text in a loop
        # use: self.setStyling(number_of_chars, style_nr)
        current_style = 0
        for token in token_list:
            tag = token[0]
            if tag in tp_tags_service:
                self.setStyling(token[1], 0)
            elif tag in tp_tags_replacement:
                self.setStyling(token[1], self.dd_tag_to_style[tag])
            elif tag in tp_tags_design_open:
                current_style = self.dd_tag_to_style[tag]
                continue
            elif tag in tp_tags_design_close:
                current_style = 0
                continue
            elif re.fullmatch(pattern_to_hide_chars_between_tags, tag) is not None:
                current_style = 0
                continue
            else:
                self.setStyling(token[1], current_style)    # default style