##########################################################################
# This module contains basic structures used in other parts of the app
##########################################################################


from collections import namedtuple

ruleReplacement = namedtuple('ruleReplacement',
                             ['dd_replacement', 'text_color', 'bg_color', 'bold', 'italic'],
                             defaults=[None, None, None, None, None])

ruleDesign = namedtuple('ruleDesign',
                        ['tag_open', 'tag_close', 'text_color', 'bg_color', 'bold', 'italic'],
                        defaults=[None, None, None, None, None, None])