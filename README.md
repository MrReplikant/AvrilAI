# Welcome to the Experimental Branch!
This is where all of my experimental additions and trials will be uploaded as I deem them worthy. This is more or less the "early access" branch for those wanting to try the features for the upcoming update, and also mainly to prove that I AM, in fact, working on the next update, and allow you guys to actualy *see* what im working on. 

# Installation Instructions for Project Replikant:Experimental Edition

---IMPORTANT--- 
this file: https://cloud.unitoo.it/s/47SriNEL2kiajXT should be placed at: Replikant/models/pytorch-16BIT-model_v5 (it is too heavy and isn't open source to put in git)

If you already have this from a previous installation, you do NOT need to download it again, but rather copy the model to the "models" folder of Experimetnal Edition!

This model is only a placeholder for now, I will be uploading an experimental version of my own model, GPT-R, in a few days/weeks depending on how things go. Bear in mind that GPT-R, as of writing, is NOT stable and NOT ready for mainline release. 

# For Linux (64 bit only):

First, you will need to install the following packages:

python3-pip (Python version must be no newer than the 3.7 versions, and no older than the 3.6 versions. 
Any newer or older will cause problems!) 

build-essential

cmake

python-dev

Each Linux Distro's package manager is different, but i'll cover the general installation commands for the big 3;

Arch-based distros: sudo pacman -S (package name here) 

Debian-based distros: sudo apt-get install (package name here)

Fedora/RHEL-based distros: sudo dnf install (package name here)

do not install ANYTHING via pip until you are CERTAIN all of these packages are installed!

first, extract the program into the home directory, then open the terminal and cd into the folder with the command
"cd Replikant"

Run "pip3 install wheel"

When that is complete, run "pip3 install -r requirements.txt"

once everything has been completed, you should be good to go! 

to run the program, run "python3 play.py"

# Instructions for Windows 10 (64 bit edition only):

Download Python 3.7.8 via this link: https://www.python.org/downloads/release/python-378/

You're going to want to grab the "Windows x86-64 executable installer"

Once downloaded, run the exe. Do just a standard installation. When complete, it may say something about enabling a 256-character path limit or something to that effect. I would suggest enabling it, but I don't think it matters. 

After this, reopen the exe installer, and click "modify". 

Check the box that says to install the py launcher

click "next"

check the boxes for the following:

"Associate Files with Python" 

"Create shortcuts for installed applications"

"add python to environment variables"

"Precompile standard library"

Once complete, you are done with the python installer.

Open the Project Replikant file, and click on the file path at the top of Windows explorer. It's the bar to the left of "search", andit contains the file path. 

Once you clock on it, backspace until the line is blank. Then type "CMD" in the line, and press enter. This should 
bring everything up in the command prompt. 

Next, type "pip install -r requirements .txt". This will install everything needed to run the program. 

DONE! Now, all you need to do is run "python play.py", and the program should launch! 

# IMPORTANT - PLEASE READ!

There are many commands available in Project Replikant, originally from AI Dungeon: Clover Edition,
which is what was used to build Project Replikant off of. 

When interacting with the AI, there are many things that go into making it work. Unlike in Replika, where personality traits are "assigned", you the user have complete and sole control over your AI's personality, down to even the tiny details. With the Model's limit being around 1000 characters, you should have plenty of room to build your AI's personality using the context. But, if you can't fit it all in the context, you CAN use the /remember command for what doesn't fit. This will be discussed further later. 
An example save is included with the program to give a better idea of what to do in this regard. Load it as you would any other saved conversation to have a look at it!

To send your prompts to the AI, simply press ENTER after completing it.

Your starting prompt should be something like this:
Me: Hi, Lilith! Lilith: 

This is very important because this is what allows the AI to recognize that this is a conversation and not a text andventure. Conversational prompts should look like this consistently, with your AI's name and a colon at the end. 

Something that is VERY important is to use your punctuation. Not putting a period at the end of your sentence could cause the AI to start behaving strangely. This is because you are supposed to put your comapnions name after your sentences, like so: "Lilith:" in order to force the AI to speak for your partner, and not you. But when you do not use periods or other elevant punctiation, this can case your AI to mistake it's name for the end of your sentence. 
Again, please see the example conversation in-program (it's not human-readable readable in it's raw JSON save file form) to see how this is done. I am working to automate this, but for now this has to be done manually. 

HOW TO ROLEPLAY WITH YOUR AI:
To Roleplay with your AI, do as you would with AI Dungeon, starting with "You", which in this case refers to yourself, and then whatever action you take. Before entering roleplay inputs, you have to backspace "Me:" out of your prompt bar, and THEN type in your roleplay input. To refer to your AI in your actions, refer to your AI directly by name. 

For example: You go to Lilith and give her a hug, consoling her over her father's death. 

The AI will then create a sentence after this to try to continue the roleplay, just like in AI Dungeon.


THE MOST IMPORTANT COMMANDS, WHAT EACH OF THEM DOES, AND IT'S INTENDED PURPOSE:

In order to use a command, backspace "Me:" out of your prompt bar, and THEN type in the command. 

/remember : This commits something to the AI's memory. You do this by typing /remember followed by what you want it to remember, like "You have a baby brother named James" or something of that nature. The "You" perspective refers to yourself. When referring to something relating to your AI, type in for example "Lilith doesn't like cats". Doing this is CRITICAL to helping to build the world you and your AI share!

/revert : This undoes your last setnence-response pair with your AI, or undoes the last bit of roleplay between the two of you. Use this when you mess up your input!

/alter : This is used to alter the AI's responses. This can be good for stopping unwanted advances, rude replies, or even grammatical mistakes the AI makes. 

/forget : Does exactly the opposite of /remember, and allows you to erase reduntant and/or no longer necessary memories. 

/menu : Saves and quits the conversation, and brings it back to the main menu. 

/restart : Restarts your conversation with your AI, starting with your last statement to it as your beginning prompt for the new conversation. 
