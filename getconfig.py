import configparser
import logging

config = configparser.ConfigParser()
config.read("config.ini")
settings = config["Settings"]

colorschemefile = settings["color-scheme"]
colorconfig = configparser.ConfigParser()
colorconfig.read(colorschemefile)
ptcolors = colorconfig["Colors"]

colorschemefile = settings["backup-color-scheme"]
colorconfig = configparser.ConfigParser()
colorconfig.read(colorschemefile)
colors = colorconfig["Colors"]

logger = logging.getLogger(__name__)
logLevel = settings.getint("log-level")
oneLevelUp = 20

# I don't know if this will work before loading the transformers module?
# silence transformers outputs when loading model
logging.getLogger("transformers.tokenization_utils").setLevel(logLevel + oneLevelUp)
logging.getLogger("transformers.modeling_utils").setLevel(logLevel + oneLevelUp)
logging.getLogger("transformers.configuration_utils").setLevel(logLevel + oneLevelUp)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logLevel + oneLevelUp,
)
logger.setLevel(logLevel)

"""
Settings descriptions and their default values keyed by their name.
These settings, their descriptions, and their defaults appear in the settings menu and the /help prompt.
"""
setting_info = {
    "temp":             ["Higher values make the AI more random.", 0.4],
    "rep-pen":          ["Controls how repetitive the AI is allowed to be.", 1.2],
    "text-wrap-width":  ["Maximum width of lines printed by computer.", 80],
    "console-bell":     ["Beep after AI generates text.", "on"],
    "top-keks":         ["Number of words the AI can randomly choose.", 20],
    "action-sugg":      ["How many actions to generate; 0 is off.", 4],
    "action-d20":       ["Makes actions difficult.", "on"],
    "action-temp":      ["How random the suggested actions are.", 1],
    "prompt-toolkit":   ["Whether or not to use the prompt_toolkit library.", "on"],
    "autosave":         ["Whether or not to save after every action.", "on"],
    "generate-num":     ["Approximate number of words to generate.", 60],
    "top-p":            ["Changes number of words nucleus sampled by the AI.", 0.9],
    "log-level":        ["Development log level. <30 is for developers.", 30],
}


