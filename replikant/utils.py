# coding: utf-8
import re

import random
import textwrap
import os
import sys

from .getconfig import logger, settings, colors, ptcolors
from shutil import get_terminal_size


def getTermWidth():
    termWidth = get_terminal_size()[0]
    if termWidth < 5:
        logger.warning("Your detected terminal width is: "+str(get_terminal_size()[0]))
        termWidth = 999999999
    return termWidth


termWidth = getTermWidth()


def in_colab():
    """Some terminal codes don't work in a colab notebook."""
    # from https://github.com/tqdm/tqdm/blob/master/tqdm/autonotebook.py
    if settings.getboolean("colab-mode"):
        settings["prompt-toolkit"] = "off"
        return True
    try:
        from IPython import get_ipython
        if (not get_ipython()) or ('IPKernelApp' not in get_ipython().config):  # pragma: no cover
            raise ImportError("console")
        if 'VSCODE_PID' in os.environ:  # pragma: no cover
            raise ImportError("vscode")
    except ImportError:
        if get_terminal_size()[0]==0 or 'google.colab' in sys.modules:
            settings["colab-mode"] = "on"
            settings["prompt-toolkit"] = "off"
            return True
        return False
    else:
        settings["colab-mode"] = "on"
        settings["prompt-toolkit"] = "off"
        return True


def use_ptoolkit():
    return not settings.getboolean("colab-mode") and settings.getboolean('prompt-toolkit')


def clear_lines(n):
    """Clear the last line in the terminal."""
    if in_colab() or settings.getboolean('colab-mode'):
        # this wont work in colab etc
        return
    screen_code = "\033[1A[\033[2K"  # up one line, and clear line
    for _ in range(n):
        print(screen_code, end="\r")


if in_colab():
    logger.warning("Colab mode enabled, disabling line clearing and readline to avoid colab bugs.")
else:
    try:
        if settings.getboolean('prompt-toolkit'):
            from .inline_editor import edit_multiline
            from prompt_toolkit import prompt as ptprompt
            from prompt_toolkit import print_formatted_text
            from prompt_toolkit.styles import Style
            from prompt_toolkit.formatted_text import to_formatted_text, HTML
        else:
            raise ModuleNotFoundError

        logger.info(
            'Python Prompt Toolkit has been imported. This enables a number of editing features but may cause bugs for colab users.')
    except (ImportError, ModuleNotFoundError):
        try:
            settings['prompt-toolkit'] = "off"
            import readline

            logger.info(
                'readline has been imported. This enables a number of editting features but may cause bugs for colab users.')
        except (ImportError, ModuleNotFoundError):
            pass


def pad_text(text, width, sep=' '):
    while len(text) < width:
        text += sep
    return text


def format_input(text):
    """
    Formats the text for purposes of storage.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_result(text):
    """
    Formats the result text from the AI to be more human-readable.
    """
    text = re.sub(r"\n{3,}", "<br>", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"<br>", "\n", text)
    text = re.sub(r"(\"[.!?]) ([A-Z])", "\\1\n\n\\2", text)
    text = re.sub(r"([^\"][.!?]) \"", "\\1\n\n\"", text)
    text = re.sub(r"([\".!?]) \"", "\\1\n\"", text)
    return text.strip()


def end_sentence(text):
    if text[-1] not in [".", "?", "!"]:
        text = text + "."
    return text


def select_file(p, e, d=0):
    """
    Selects a file from a specific path matching a specific extension.
    p: The current path (and subdirectories) to choose from.
    e: The extension to filter based on.
    d: The path depth. Used for knowing when to go back or when to abort a file selection. Do not set this yourself.
    """
    if p.is_dir():
        t_dirs = sorted([x for x in p.iterdir() if x.is_dir()])
        t_files = sorted([x for x in p.iterdir() if x.is_file() and x.name.endswith(e)])
        files = t_dirs + t_files
        list_items(
            ["(Random)"] +
            [f.name[:-len(e)] if f.is_file() else f.name + "/" for f in files] +
            ["(Cancel)" if d == 0 else "(Back)"],
            "menu"
        )
        count = len(files) + 1
        i = input_number(count)
        if i == 0:
            try:
                i = random.randrange(1, count-1)
            except ValueError:
                i = 1
        if i == count:
            if d == 0:
                output("Action cancelled. ", "message")
                return None
            else:
                return select_file(p.parent, e, d-1)
        else:
            return select_file(files[i-1], e, d+1)
    else:
        return p


def fill_text(text, width):
    texts = text.split('\n')
    for i in range(0, len(texts)):
        texts[i] = textwrap.fill(
            texts[i],
            width,
            replace_whitespace=False,
            drop_whitespace=False
        )
    return '\n'.join(texts)


# ECMA-48 set graphics codes for the curious. Check out "man console_codes"
def output(text1, col1=None,
           text2=None, col2=None,
           wrap=True,
           beg=None, end='\n', sep=' ',
           rem_beg_spaces=True):
    print('', end=beg)
    ptoolkit = use_ptoolkit() and ptcolors['displaymethod'] == "prompt-toolkit"

    if wrap:
        width = settings.getint("text-wrap-width")
        width = 999999999 if width < 2 else width
        width = min(width, termWidth)
        wtext = text1 + '\u200D' + sep + '\u200D' + text2 if text2 is not None else text1
        wtext = fill_text(wtext, width)
        wtext = re.sub(r"\n[ \t]+", "\n", wtext) if rem_beg_spaces else wtext
        wtext = wtext.split('\u200D')
        text1 = wtext[0]
        if text2 is not None:
            sep = wtext[1]
            text2 = ' '.join(wtext[2:])

    if ptoolkit:
        col1 = ptcolors[col1] if col1 and ptcolors[col1] else ""
        col2 = ptcolors[col2] if col2 and ptcolors[col2] else ""
        print_formatted_text(to_formatted_text(text1, col1), end='')
        if text2:
            print_formatted_text(to_formatted_text(sep), end='')
            print_formatted_text(to_formatted_text(text2, col2), end='')
        print('', end=end)

    else:
        col1 = colors[col1] if col1 and colors[col1] and colors[col1][0].isdigit() else None
        col2 = colors[col2] if col2 and colors[col2] and colors[col2][0].isdigit() else None

        clb1 = "\x1B[{}m".format(col1) if col1 else ""
        clb2 = "\x1B[{}m".format(col2) if col2 else ""
        cle1 = "\x1B[0m" if col1 else ""
        cle2 = "\x1B[0m" if col2 else ""
        text1 = clb1 + text1 + cle1
        if text2 is not None:
            text2 = clb2 + text2 + cle2
            print(text1, end='')
            print(sep, end='')
            print(text2, end=end)
        else:
            print(text1, end=end)

    linecount = 1
    if beg:
        linecount += beg.count('\n')
    if text1:
        linecount += text1.count('\n')
    if end:
        linecount += end.count('\n')
    if text2:
        linecount += text2.count('\n')
        if sep:
            linecount += sep.count('\n')
    return linecount


def input_bool(prompt, col1="default", default: bool = False):
    val = input_line(prompt, col1).strip().lower()
    if not val or val[0] not in "yn":
        return default
    return val[0] == "y"

def input_line(str, col1="default", default=""):
    if use_ptoolkit() and ptcolors['displaymethod'] == "prompt-toolkit":
        col1 = ptcolors[col1] if col1 and ptcolors[col1] else ""
        val = ptprompt(to_formatted_text(str, col1), default=default)
    else:
        clb1 = "\x1B[{}m".format(colors[col1]) if col1 and colors[col1] and colors[col1][0].isdigit() else ""
        cle1 = "\x1B[0m" if col1 and colors[col1] and colors[col1][0].isdigit() else ""
        val = input(clb1 + str + cle1)
        print("\x1B[0m", end="")
    return val


def input_number(max_choice, default=0):
    # Inputs an integer from 0 to max_choice (inclusive)
    if default == -1:
        default = max_choice
    bell()
    print()
    val = input_line(f"Enter a number from above (default {default}):", "selection-prompt")
    if not val:
        return default
    elif not re.match("^\d+$", val) or 0 > int(val) or int(val) > max_choice:
        output("Invalid choice. ", "error")
        return input_number(max_choice)
    else:
        return int(val)


def bell():
    if settings.getboolean("console-bell"):
        print("\x07", end="")


alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|ca|gg|tv|co|net|org|io|gov)"


def sentence_split(text):
    """Splits a paragraph of text into a list of sentences within the text."""
    text = " " + text + "  "
    text = text.replace("...","<3elp><stop>")
    text = text.replace("..","<2elp><stop>")
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace(".<stop>\"", ".\"<stop>")
    text = text.replace("?<stop>\"", "?\"<stop>")
    text = text.replace("!<stop>\"", "!\"<stop>")
    text = text.replace("<3elp><stop>\"", "<3elp>\"<stop>")
    text = text.replace("<2elp><stop>\"", "<2elp>\"<stop>")
    text = text.replace("<prd>",".")
    text = text.replace("<3elp>","...")
    text = text.replace("<2elp>","..")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences[-1] == "":
        sentences = sentences[:-1]
    return sentences


def list_items(items, col='menu', start=0, end=None, wrap=False):
    """Lists a generic list of items, numbered, starting from the number passed to start. If end is not None,
    an additional element will be added with its name as the value """
    i = start
    digits = len(str(len(items)-1))
    for s in items:
        output(str(i).rjust(digits) + ") " + s, col, end='', wrap=wrap)
        i += 1
    if end is not None:
        output('', end=end, wrap=wrap)


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]


def _get_prefix(first_string ,second_string):
    if not first_string or not second_string:
        return ""
    if first_string == second_string:
        return first_string
    maximum_length = min(len(first_string), len(second_string))
    for i in range(0, maximum_length):
        if not first_string[i] == second_string[i]:
            return first_string[0:i]
    return first_string[0:maximum_length]


def get_similarity(first_string, second_string, scaling=0.1):
    first_string_length = len(first_string)
    second_string_length = len(second_string)
    a_matches = [False] * first_string_length
    b_matches = [False] * second_string_length
    matches = 0
    transpositions = 0
    jaro_distance = 0.0

    if first_string_length == 0 or second_string_length == 0:
        return 1.0

    maximum_matching_distance = (max(first_string_length, second_string_length) // 2) - 1
    if maximum_matching_distance < 0:
        maximum_matching_distance = 0

    for i in range (first_string_length):
        start = max(0, i - maximum_matching_distance)
        end = min(i + maximum_matching_distance + 1, second_string_length)
        for x in range (start, end):
            if b_matches[x]:
                continue
            if first_string[i] != second_string[x]:
                continue
            a_matches[i] = True
            b_matches[x] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(first_string_length):
        if not a_matches[i]:
            continue
        while not b_matches[k]:
            k += 1
        if first_string[i] != second_string[k]:
            transpositions += 1
        k += 1

    jaro_distance = ((matches / first_string_length) +
                    (matches / second_string_length) +
                    ((matches - transpositions / 2) / matches)) / 3.0
    prefix = min(len(_get_prefix(first_string, second_string)), 4)

    # Round to 2 places of percision to match pyjarowinkler formatting
    return round((jaro_distance + prefix * scaling * (1.0 - jaro_distance)) * 100.0) / 100.0


def get_num_options(num):

    while True:
        choice = input("Enter the number of your choice: ")
        try:
            result = int(choice)
            if result >= 0 and result < num:
                return result
            else:
                print("Error invalid choice. ")
        except ValueError:
            print("Error invalid choice. ")


def player_died(text):
    """
    TODO: Add in more sophisticated NLP, maybe a custom classifier
    trained on hand-labelled data that classifies second-person
    statements as resulting in death or not.
    """
    lower_text = text.lower()
    you_dead_regexps = [
        "you('re| are) (dead|killed|slain|no more|nonexistent)",
        "you (die|pass away|perish|suffocate|drown|bleed out)",
        "you('ve| have) (died|perished|suffocated|drowned|been (killed|slain))",
        "you (\w* )?(yourself )?to death",
        "you (\w* )*(collapse|bleed out|chok(e|ed|ing)|drown|dissolve) (\w* )*and (die(|d)|pass away|cease to exist|(\w* )+killed)",
    ]
    return any(re.search(regexp, lower_text) for regexp in you_dead_regexps)


def player_won(text):
    lower_text = text.lower()
    won_phrases = [
        "you ((\w* )*and |)live happily ever after",
        "you ((\w* )*and |)live (forever|eternally|for eternity)",
        "you ((\w* )*and |)(are|become|turn into) ((a|now) )?(deity|god|immortal)",
        "you ((\w* )*and |)((go|get) (in)?to|arrive (at|in)) (heaven|paradise)",
        "you ((\w* )*and |)celebrate your (victory|triumph)",
        "you ((\w* )*and |)retire",
    ]
    return any(re.search(regexp, lower_text) for regexp in won_phrases)


def cut_trailing_quotes(text):
    num_quotes = text.count('"')
    if num_quotes % 2 == 0:
        return text
    else:
        final_ind = text.rfind('"')
        return text[:final_ind]


def split_first_sentence(text):
    first_period = text.find(".")
    first_exclamation = text.find("!")

    if first_exclamation < first_period and first_exclamation > 0:
        split_point = first_exclamation + 1
    elif first_period > 0:
        split_point = first_period + 1
    else:
        split_point = text[0:20]

    return text[0:split_point], text[split_point:]


def cut_trailing_action(text):
    lines = text.split("\n")
    last_line = lines[-1]
    if (
        "you ask" in last_line
        or "You ask" in last_line
        or "you say" in last_line
        or "You say" in last_line
    ) and len(lines) > 1:
        text = "\n".join(lines[0:-1])
    return text


def clean_suggested_action(result_raw, min_length=4):
    result_cleaned = standardize_punctuation(result_raw)
    result_cleaned = cut_trailing_sentence(result_cleaned, allow_action=True)
    # The generations actions carry on into the next prompt, so lets remove the prompt
    results = result_cleaned.split("\n")
    results = [s.strip() for s in results]
    results = [s for s in results if len(s) > min_length]
    # Sometimes actions are generated with leading > ! . or ?. Likely the model trying to finish the prompt or start an action.
    result = results[0].strip().lstrip(" >!.?") if len(results) else ""
    # result = cut_trailing_quotes(result)
    logger.debug(
        "full suggested action '%r'. Cropped: '%r'. Split '%r'",
        result_raw,
        result,
        results,
    )
    # Often actions are cropped with sentance fragments, lets remove. Or we could just turn up config_act["generate-number"]
    result = first_to_second_person(result)
    # Sometimes the suggestion start with "You" we will add that on later anyway so remove it here
    # result = re.sub("^ ?[Yy]ou try to ?", "", result)
    # result = re.sub("^ ?[Yy]ou start to ?", "", result)
    # result = re.sub("^ ?[Yy]ou ", "", result)
    logger.debug("suggested action after cleaning `%r`", result)
    return result


def fix_trailing_quotes(text):
    num_quotes = text.count('"')
    if num_quotes % 2 == 0:
        return text
    else:
        return text + '"'


def cut_trailing_sentence(text, allow_action=False):
    text = standardize_punctuation(text)
    last_punc = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
    if last_punc <= 0:
        last_punc = len(text) - 1
    et_token = text.find("<")
    if et_token > 0:
        last_punc = min(last_punc, et_token - 1)
    # elif et_token == 0:
    #     last_punc = min(last_punc, et_token)
    if allow_action:
        act_token = text.find(">")
        if act_token > 0:
            last_punc = min(last_punc, act_token - 1)
        # elif act_token == 0:
        #     last_punc = min(last_punc, act_token)
    text = text[: last_punc + 1]
    text = fix_trailing_quotes(text)
    if allow_action:
        text = cut_trailing_action(text)
    return text


def replace_outside_quotes(text, current_word, repl_word):
    text = standardize_punctuation(text)
    reg_expr = re.compile(current_word + '(?=([^"]*"[^"]*")*[^"]*$)')
    output = reg_expr.sub(repl_word, text)
    return output


def is_first_person(text):
    count = 0
    for pair in first_to_second_mappings:
        variations = mapping_variation_pairs(pair)
        for variation in variations:
            reg_expr = re.compile(variation[0] + '(?=([^"]*"[^"]*")*[^"]*$)')
            matches = re.findall(reg_expr, text)
            count += len(matches)

    if count > 3:
        return True
    else:
        return False


def is_second_person(text):
    count = 0
    for pair in second_to_first_mappings:
        variations = mapping_variation_pairs(pair)
        for variation in variations:
            reg_expr = re.compile(variation[0] + '(?=([^"]*"[^"]*")*[^"]*$)')
            matches = re.findall(reg_expr, text)
            count += len(matches)

    if count > 3:
        return True
    else:
        return False


def capitalize(word):
    return word[0].upper() + word[1:]


def mapping_variation_pairs(mapping):
    mapping_list = []
    mapping_list.append((" " + mapping[0] + " ", " " + mapping[1] + " "))
    mapping_list.append(
        (" " + capitalize(mapping[0]) + " ", " " + capitalize(mapping[1]) + " ")
    )

    # Change you it's before a punctuation
    if mapping[0] == "you":
        mapping = ("you", "me")
    mapping_list.append((" " + mapping[0] + ",", " " + mapping[1] + ","))
    mapping_list.append((" " + mapping[0] + "\?", " " + mapping[1] + "\?"))
    mapping_list.append((" " + mapping[0] + "\!", " " + mapping[1] + "\!"))
    mapping_list.append((" " + mapping[0] + "\.", " " + mapping[1] + "."))

    return mapping_list


first_to_second_mappings = [
    ("I'm", "you're"),
    ("i'm", "you're"),
    ("Im", "you're"),
    ("im", "you're"),
    ("Ive", "you've"),
    ("ive", "you've"),
    ("I am", "you are"),
    ("i am", "you are"),
    ("wasn't I", "weren't you"),
    ("I", "you"),
    ("I'd", "you'd"),
    ("i", "you"),
    ("I've", "you've"),
    ("was I", "were you"),
    ("am I", "are you"),
    ("was i", "were you"),
    ("am i", "are you"),
    ("wasn't I", "weren't you"),
    ("I", "you"),
    ("i", "you"),
    ("I'd", "you'd"),
    ("i'd", "you'd"),
    ("I've", "you've"),
    ("i've", "you've"),
    ("I was", "you were"),
    ("i was", "you were"),
    ("my", "your"),
    ("we", "you"),
    ("we're", "you're"),
    ("mine", "yours"),
    ("me", "you"),
    ("us", "you"),
    ("our", "your"),
    ("I'll", "you'll"),
    ("i'll", "you'll"),
    ("myself", "yourself"),
]

second_to_first_mappings = [
    ("you're", "I'm"),
    ("your", "my"),
    ("you are", "I am"),
    ("you were", "I was"),
    ("are you", "am I"),
    ("you", "I"),
    ("you", "me"),
    ("you'll", "I'll"),
    ("yourself", "myself"),
    ("you've", "I've"),
]


def capitalize_helper(string):
    string_list = list(string)
    string_list[0] = string_list[0].upper()
    return "".join(string_list)


def capitalize_first_letters(text):
    first_letters_regex = re.compile(r"((?<=[\.\?!]\s)(\w+)|(^\w+))")

    def cap(match):
        return capitalize_helper(match.group())

    result = first_letters_regex.sub(cap, text)
    return result


def standardize_punctuation(text):
    text = text.replace("’", "'")
    text = text.replace("`", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text


def first_to_second_person(text):
    text = " " + text
    text = standardize_punctuation(text)
    if text[-1] not in [".", "?", "!"]:
        text += "."
    for pair in first_to_second_mappings:
        variations = mapping_variation_pairs(pair)
        for variation in variations:
            text = replace_outside_quotes(text, variation[0], variation[1])
    return text


def second_to_first_person(text):
    text = " " + text
    text = standardize_punctuation(text)
    if text[-1] not in [".", "?", "!"]:
        text += "."
    for pair in second_to_first_mappings:
        variations = mapping_variation_pairs(pair)
        for variation in variations:
            text = replace_outside_quotes(text, variation[0], variation[1])
    return text
