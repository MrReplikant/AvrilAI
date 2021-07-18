from getconfig import settings, colors, setting_info
from utils import pad_text


def boolValue(bool):
    return "on" if bool else "off"


def instructions():
    print('\n' +
          'Project Replikant Instructions: \n' +
          '  Enter actions starting with a verb ex. "go to the tavern" or "attack the orc."\n' +
          '  To speak enter Me:"(thing you want to say)" followed by (Your AIs name): \n' + 
        'For example: "Me: Hello, Lilith! Lilith:" \n' +
'  To insert your own storyline text into the conversation, enter !(thing you want to insert)')
    print('The following commands can be entered for any action:')
    print('  "/revert"                Reverts the last action allowing you to pick a different action.')
    print('  "/quit"                  Quits the conversation and saves')
    print('  "/menu"                  Starts a new conversation and saves your current one')
    print('  "/retry"                 Retries the last action')
    print('  "/restart"               Restarts the current conversation [WARNING: THIS WILL RESTART YOUR AI AND WIPE ITS MEMORY]')
    print('  "/print"                 Prints a transcript of your conversation (without extra newline formatting)')
    print('  "/alter"                 Edit the last prompt from the AI')
    print('  "/altergen"              Edit the last result from the AI and have it generate the rest')
    print('  "/context"               Edit the conversation\'s permanent context paragraph')
    print('  "/remember [SENTENCE]"   Commits something permanently to the AI\'s memory')
    print('  "/forget"                Opens a menu allowing you to remove permanent memories')
    print('  "/save"                  Saves your conversation to a file in the game\'s save directory')
    print('  "/load"                  Loads a conversation from a file in the game\'s save directory')
    print('  "/summarize"             Create a new conversation using by summarizing your previous one')
    print('  "/help"                  Prints these instructions again')
    print('  "/set [SETTING] [VALUE]" Sets the specified setting to the specified value. {DO NOT ALTER]:')
    for k, v in setting_info.items():
        print(pad_text('        ' + k, 27) + v[0] + (" " if v[0] else "") +
              "Default: " + str(v[1]) + " | "
              "Current: " + settings.get(k))
