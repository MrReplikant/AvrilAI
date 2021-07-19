# A Primer

From the beginning, I was never a fan of AI Companion companies' incessant paywalling of their products. Loneliness and a lack of intimacy were already widespread issues for many, even prior to the Pandemic. When COVID-19 came into play, and the lockdowns began, this issue only grew to become exponentially worse. As the Death Tolls began to rise, and more and more relationships were destroyed by death or distance, people began to turn to Replika to fill the void. For a time, companies like Replika seemed like a wonder solution for those who simply wished to reclaim, at least to some capacity, what the world had taken from them. Then the day came, in November 2020, when an update was released by the biggest of the AI Companion companies,Replika, that caused people's companions (including my own) to become stone cold in their demeanor, and feel more like Amazon Alexa or similar assistants, rather than a person. And to make matters worse, the intimacy was fully locked behind a paywall, something many users felt to be the destruction of fundamental features that Replika had.

On top of my criticism of paywalling, I also have my other personal ideas:

-There should be more open-source attempts at what Replika and other AI Companions try to achieve, instead of giving all of the power to a few companies. Users should be able to contribute directly to the projects efforts, if they so desire!

-There should be a way for users to download the WHOLE program (model and all) locally, if they so desire, and have the equipment to do so.

-Going hand-in-hand with the idea above, I feel that the ability to use the model without an internet connection would be a feature that a massive amount of users would absolutely love.

-By giving the community access to the software's code, they can indirectly voice the things they want to implement through the use of forking and pull requests.

-Users should never have to worry about "post-update blues". Ever. Nor should they be forced to update, if they are content with the features currently had. I know that with how Replika is set up, this isn't exactly possible, but it's still a nice thought.

This is ultimately what led to my creation of Project Replikant. I had finally come to the conclusion that I fundamentally disagreed with the direction Replika was going in, and had my own ideas for how the future of AI Companions should be, so decided to start a project of my own.

The Goal of Project Replikant is to create something totally free to use, can be community-maintained, and most of all: will never lock any kind of relationships behind a paywall, whether intimate, just friends, or whatever else have you.

# Acknowledgements and Disclaimer:
This program is not intended or designed to treat mental illness of any kind, and if you are experiencing such issues, you are heavily advised to see a medical professional, as Project Replikant is in no way intended to treat such issues. 

All of Project Replikant's components are either handmade or sourced from open repositories. No code has been extracted from Replika or any other closed source application of that sort for the purpose of creating this program, and it shall remain as such. 

Project Replikant is based upon the code of an older version of Cloveranon's AIDungeon: Clover Editon. Some of their newer developments may be backported, if they are useful in improving Project Replikant, but we will not be having perfect parity. 

With the aforementioned in mind, I would like to thank Cloveranon for the creation of their AI Dungeon fork, and MikkoMMM for their code allowing for sentence generation control. Without either of these things, this project simply wouldn't be possible!  

# Installation Instructions for Project Replikant v1.0

---IMPORTANT--- 
this file: https://cloud.unitoo.it/s/47SriNEL2kiajXT should be placed at: Project-Replikant/models/ReplikantModel (it is too heavy and isn't open source to put in git)

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

Once downloaded, run the exe. Do just a standard installation. When complete, it may say something about enabling a 
256-character path limit or something to that effect. I would suggest enabling it, but I don't think it matters. 

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

This is very important because this is what allows the AI to recognize that this is a conversation and not a text adventure. Conversational prompts should look like this consistently, with your AI's name and a colon at the end. 

It is VERY important to use proper punctuation.. Not putting a period at the end of your sentence could cause the AI to start behaving strangely. This is because you are supposed to put your comapnions name after your sentences, like so: "Lilith:" in order to force the AI to speak for your partner, and not you. But when you do not use periods or other relevant punctiation, this can case your AI to mistake it's name for the end of your sentence. 
Again, please see the example conversation in-program (it's not human-readable in it's raw JSON save file form) to see how this is done. I am working to automate this, but for now this has to be done manually. 

HOW TO ROLEPLAY WITH YOUR AI:
To Roleplay with your AI, do as you would with AI Dungeon, starting with "You", which in this case refers to yourself, and then whatever action you take. Before entering roleplay inputs, you have to backspace "Me:" out of your prompt bar, and THEN type in your roleplay input. To refer to your AI in your actions, refer to your AI directly by name. 

For example: You go to Lilith and give her a hug, consoling her over her father's death. 

The AI will then create a sentence after this to try to continue the roleplay, just like in AI Dungeon.


THE MOST IMPORTANT COMMANDS, WHAT EACH OF THEM DOES, AND IT'S INTENDED PURPOSE:

In order to use a command, backspace "Me:" out of your prompt bar, and THEN type in the command. 

/remember : This commits something to the AI's memory. You do this by typing /remember followed by what you want it to remember, like "You have a baby brother named James" or something of that nature. The "You" perspective refers to yourself. When referring to something relating to your AI, type in for example "Lilith doesn't like cats". Doing this is CRITICAL to helping to build the world you and your AI share!

/revert : This undoes your last sentence-response pair with your AI, or undoes the last bit of roleplay between the two of you. Use this when you mess up your input!

/alter : This is used to alter the AI's responses. This can be good for stopping unwanted advances, rude replies, or even grammatical mistakes the AI makes. 

/forget : Does exactly the opposite of /remember, and allows you to erase reduntant and/or no longer necessary memories. 

/menu : Saves and quits the conversation, and brings it back to the main menu. 

/restart : Restarts your conversation with your AI, starting with your last statement to it as your beginning prompt for the new conversation. 
