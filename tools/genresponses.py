import configparser
import torch
import gc
from random import choice
import json
from random import shuffle
from gpt2generator import GPT2Generator
from numpy.random import beta
from numpy import greater
from numpy import mean
from pathlib import Path
from sys import argv
#from numpy import std
samplesize=1024*16
config = configparser.ConfigParser()
config.read('AB.ini')
A = config['A']
B = config['B']
generalSettings = config['All']
def genResponses(settings, n, name):
    responses = []
    files=list(Path("AB-prompts").iterdir())
    gc.collect()
    torch.cuda.empty_cache()
    generator = GPT2Generator(
            model_path = settings['model-path'],
            dtype = torch.float16,
            max_history_tokens=settings.getint('max-history-tokens')
    )
    generator.top_p_first=settings.getboolean('top-p-first')
    for i in range(n):
        torch.cuda.synchronize()
        gc.collect()
        torch.cuda.empty_cache()
        file = choice(files)
        with file.open() as f:
            prompt=f.read()
        responses.append({
            'name':name,
            'prompt':str(file.resolve()), 
            'output':generator.generate(
                context=prompt,
                temperature=settings.getfloat('temp'),
                top_p = settings.getfloat('top-p'),
                top_k = settings.getint('top-keks'),
                repetition_penalty=settings.getfloat('repetition-penalty'),
                repetition_penalty_slope=settings.getfloat('repetition-slope')
            )
        })
    generator=None
    gc.collect()
    torch.cuda.empty_cache()
    return responses


name = argv[1]
if name == 'A':
    testconfig=A
elif name == 'B':
    testconfig=B
else:
    assert False,'input not A or B'
print(json.dumps(genResponses(testconfig, generalSettings.getint('num-samples'), name)))
