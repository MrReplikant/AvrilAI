from .getconfig import settings, setting_info
from .utils import pad_text

def boolValue(bool):
    return "on" if bool else "off"

def instructions():
    print('\n' +
          'Project Replikant Instructions: \n' +
          '  To do roleplay, use {thing you want to do goes here} followed by a period.\n' +
          '  To speak to the AI, just talk to it as if you were texting someone!\n')
    print('The following commands can be entered for any action:')
    print('  "/revert"                Reverts the last action, allowing you to try a different one.')
    print('  "/quit"                  Quits the conversation and saves')
    print('  "/menu"                  Starts a new conversation and saves your current one')
    print('  "/retry"                 Retries the last action')
    print('  "/restart"               Restarts the AI [WILL ERASE ITS MEMORY, DO NOT DO UNLESS YOURE ABSOLUTELY SURE]')
    print('  "/print"                 Prints a transcript of your conversation (without extra newline formatting)')
    print('  "/alter"                 Edit the last prompt from the AI')
    print('  "/altergen"              Edit the last result from the AI and have it generate the rest')
    print('  "/context"               Edit the AI\'s permanent context paragraph')
    print('  "/remember [SENTENCE]"   Commits something permanently to the AI\'s memory')
    print('  "/memalt"                Let you select and alter a memory entry')
    print('  "/memswap"               Swaps places of two memory entries')
    print('  "/forget"                Opens a menu allowing you to remove permanent memories')
    print('  "/save"                  Saves your conversation to a file in the save directory')
    print('  "/load"                  Loads a conversation from a file in the save directory')
    print('  "/summarize"             Create a new conversation using by summarizing your previous one')
    print('  "/help"                  Prints these instructions again')
    print('  "/set [SETTING] [VALUE]" Sets the specified setting to the specified value.:')
    for k, v in setting_info.items():
        print(pad_text('        ' + k, 27) + v[0] + (" " if v[0] else "") +
              "Default: " + str(v[1]) + " | "
              "Current: " + settings.get(k))
