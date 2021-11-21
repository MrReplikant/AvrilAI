# AIDungeon2
## Clover Edition

A fork of AIDungeon2 with numerous improvements. Now supporting GPT-Neo.

![img](images/retro1.jpg)
![img](images/retro2.jpg)
![img](images/retro3.jpg)
![img](images/original-screenshot.png)

Also take a look at [AIDungeonPastes](https://aidungeonpastes.github.io/AID2-Art/) for some drawn gameplay examples.



## Features
------------------------

* GPT-Neo support
* Complete rewrite of the user interface
  * Colored text
  * Suggested actions
  * Console bell dings when the AI finishes
  * Much improved prompt selection
  * Ability to save custom prompts
* Half precision floating point using significantly less GPU memory
* Repetition Penalty to reduce AI looping behavior
* A much larger library of fan made starting prompts
* Challenge added with your actions not always succeeding
* A simple config file
* Lots of changes to story history sampling/truncation to hopefully stay on track with longer games
* Eventually hope to improve the AI itself, but this will take some time

## Install instructions
------------------------

Officially we only support local installs. We encourage and recommend installing and running the game locally. However since the beginning most people have been playing it for free on Google's servers through their Colab platform. Allegedly it requires no effort to get started. Try [this link](https://colab.research.google.com/drive/1kYVhVeE6z4sUyyKDVxLGrzI4OTV43eEa) and go to the [4chan threads](https://boards.4chan.org/search#/aidungeon%20OR%20%22ai%20dungeon%22) for help and info.

To play with GPU acceleration, you need an Nvidia GPU, although some anons claim to have gotten it working with an AMD with ROCm in Linux. The original "XL" 1558M parameter model requires at least 4GB of VRAM. Smaller models may consume much less. On CPU, response times vary from about a minute on the XL GPT-2 1558M model, which is slow but usable, to about 6 minutes on GPT-Neo.

After any of the following install steps, you must get one of the models.

### Windows 10 install

1. Download this repo. Github has a green download button to the top right that looks like: `[⤓ Code]`. Click it, select "Download Zip", then unzip it to a folder. Or you can use the git command `git clone --depth=1 "https://github.com/cloveranon/Clover-Edition/"` if you have git installed. 
2. Go to your Clover Edition folder.
3. Run `install.bat` and follow the on-screen instructions.

#### Windows troubleshooting

- Users have reported that some anti-virus (specifically Kaspersky) isn't happy with the install.bat script. Please whitelist or temporarily disable anti-virus when installing.
- You can partially uninstall by deleting the `venv/` folder, and fully uninstall by just deleting the entire Clover Edition folder.

### Windows 7+ install

1. Visit [the repo for the Clover Edition installer project](https://github.com/AIDungeonWiXAnon/AID2-Installer-Project/releases/latest) and download the latest executable.
2. Navigate to your folder for your downloads
3. Run the executable (`Clover.Edition.Installer.exe`) and follow on-screen prompts.

### Linux install

1. Install [Python](https://www.python.org/downloads/) or use your package manager (e.g. `sudo apt-get install python3` or `sudo yum install python3` or something).
2. Download this repo. Github has a green download button to the top right that looks like: `[⤓ Code]`. Click it, select "Download Zip", then unzip it to a folder. Or you can use the git command `git clone --depth=1 "https://github.com/cloveranon/Clover-Edition/"` if you have git installed.
3. Go to your Clover Edition folder.
4. Run `sh install.sh` and follow the on-screen instructions.

### OS-agnostic manual install

1. Install [Python](https://www.python.org/downloads/). The installer should install `pip` and it should add it to your `PATH` automatically. Make sure you have the relevant options selected if the installer gives you any options.
2. Download this repo. Github has a green download button to the top right that looks like: `[⤓ Code]`. Click it, select "Download Zip", then unzip it to a folder. Or you can use the git command `git clone --depth=1 "https://github.com/cloveranon/Clover-Edition/"` if you have git installed. 
3. Open a command line or terminal and go to your Clover Edition folder.
4. Run: `pip --no-cache-dir install -r requirements/requirements.txt`
5. Install PyTorch (you must do one of the following):
    - If you're using an Nvidia GPU with CUDA, run: `pip install -r requirements/cuda_requirements.txt`
    - If you're planning on just using your CPU, run: `pip install -r requirements/cpu_requirements.txt`


## Models

You can have multiple models installed, but you need at least one.

| Model Name | Model Type | Parameters | File Size | RAM | VRAM | Links  |
|---|---|---|---|---|---|---|
| finetuneanon's horni - light novel | GPT-Neo | 2.7 billion | 5 GB | 8 GB | 8 GB | [[mega](https://mega.nz/file/rQcWCTZR#tCx3Ztf_PMe6OtfgI95KweFT5fFTcMm7Nx9Jly_0wpg)] [[gdrive](https://drive.google.com/file/d/1M1JY459RBIgLghtWDRDXlD4Z5DAjjMwg/view?usp=sharing)] [[torrent](https://tinyurl.com/pytorch-gptneo-horni)]  |
| finetuneanon's horni | GPT-Neo | 2.7 billion | 5 GB | 8 GB | 8 GB | [[mega](https://mega.nz/file/6BNykLJb#B6gxK3TnCKBpeOF1DJMXwaLc_gcTcqMS0Lhzr1SeJmc)] [[gdrive](https://drive.google.com/file/d/1-Jj_hlyNCQxuSnK7FFBXREGnRSMI5MoF/view?usp=sharing)] [[torrent](https://tinyurl.com/pytorch-gptneo-horni)](same as above) |
| EleutherAI | GPT-Neo | 2.7 billion | 10 GB | 12 GB | 8 GB | [[huggingface](https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/main)] * |
| Original Clover Edition | GPT-2 | 1.56 billion | 6 GB | 12 GB | 5 GB | [[torrent](tinyurl.com/pytorch-gpt2-model)] |
| Collection of 4 models | GPT-2 | 774 million | 3 GB ea | 8 GB | 4 GB | [[mega](https://mega.nz/folder/4e5kRCIB#v7q0ItVjhhGcIqfZOZy9yA)] |

\* For EleutherAI's GPT-Neo-2.7B, Download only `pytorch_model.bin` and make sure it's named that, put it into a new folder named `gpt-neo-2.7b` (see below for the structure), then copy `config.json`, `merges.txt`, and `vocab.json` from one of finetuneanon's models and put them in the same folder.

16-Bit models are half the size, and load 20 times faster (probably because they run out of RAM and hit the swap space). I found the original AID2 model (`pytorch-gpt2-xl-aid2-v5`) took 12.6 minutes to load, while the 16 bit version took 37 seconds.

Once downloaded, your model folder should look like this:
```
    ./models
    └── <MODEL-NAME>
        ├── config.json
        ├── merges.txt
        ├── pytorch_model.bin
        └── vocab.json
```

## Playing

- Windows 10: double-click `play.bat`
- Windows 7+: `python launch.py`
- Linux: `bash play.sh`
- OS-agnostic install: `python launch.py`


## Color support on Windows

Install [Windows Terminal](https://aka.ms/terminal) (recommended), [cmder](https://cmder.net/), or [hyper](https://hyper.is/), and use that as your terminal. If you installed Clover Edition with `install.bat`, you might already have Windows Terminal installed.


## Datasets and fine-tuning the AI
---------------

I threw together a quick page of some tips [here](DATASETS.md). I plan to throw any links to interesting datasets or guides for training and fine-tuning the AI there. Please send me anything interesting.

Fine-tuning is not currently a push button thing and requires some minimal technical ability. Most people are using the program gpt-simple. You may have more luck with the much more advanced [Huggingface-Transformers](https://github.com/huggingface/transformers) program that we use to power Clover-Edition. [This](https://huggingface.co/transformers/examples.html#language-model-fine-tuning) seems to be their documentation on fine-tuning.

## Converting Tensorflow model to PyTorch
----------------

I have made the [convert_gpt2_model.py](convert_gpt2_model.py) script an idiot proof simple way of quickly converting tensorflow models to PyTorch models. Just run it on the folder containing a tensorflow model and you will get a PyTorch model. You can use the --full flag to get a full 32bit model, but do try 16bit models as they will be potentially half the size for the same accuracy.

See the [test-models.py](test-models.py) script to test the accuracy of 16 bit mode if you doubt the chad 16BIT models. My tests were well within expectations:

![img](images/16bitvs32bit.png)


## Community
------------------------

See that github issues page? Post any questions, requests, or problems there if you are willing to create a github account. Unless MicroAndSoft deletes us.
Otherwise see:

* **Website**: [4chan Discussion](https://boards.4chan.org/search#/aidungeon%20OR%20%22ai%20dungeon%22)
* **Email**: cloveranon@nuke.africa


## Contributing
------------------------
Contributions are more than welcome. You can fork the thing and send a  [pull request](https://help.github.com/articles/using-pull-requests/) from your fork.

![cry.](images/cry.png)


## PyTorch Model magnet links (for reference)
------------------------

GPT-Neo, finetuneanon's horni and horni-ln:
```
magnet:?xt=urn:btih:31d956ff4a248dcf914b1b7e474cbac02d70d6a4&dn=gtp-neo-horni
```

GPT-2, AIDungeon2 Clover Edition (16-bit):
```
magnet:?xt=urn:btih:9c774c51bac64e5bffd481187b86e834839b4141&dn=model%5Fv5%5Fpytorch%5F16bit&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.pomf.se%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce
```

GPT-2, AIDungeon2 Clover Edition (32-bit):
```
magnet:?xt=urn:btih:17dcfe3d12849db04a3f64070489e6ff5fc6f63f&dn=model_v5_pytorch&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2fopen.stealth.si%3a80%2fannounce&tr=udp%3a%2f%2fp4p.arenabg.com%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.coppersurfer.tk%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.cyberia.is%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me%3a6969%2fannounce&tr=udp%3a%2f%2f9.rarbg.me%3a2710%2fannounce&tr=udp%3a%2f%2ftracker3.itzmx.com%3a6961%2fannounce
```
