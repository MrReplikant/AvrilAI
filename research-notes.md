After digging up the GutenBerg Dialogue Dataset repo, and downloading the trained models created based upon it, I have realized that 125M GPT-2 is simply too small
for use with Project Replikant, at least when trained in such matter seen in the Gutenberg models. 

I am currently training yet another iteration of my experimental model, GPT-R, and this time, I am utilizing a parameter that has not been utilized before. This is 
the "noise" parameter, found in Neil Shepperd's GPT-2 training program. It is normally used to regularize against typos. But, I am hoping that it will also allow 
GPT-R to have more fluid conversational ability. Time will ultimately tell. 

8/7/21 
The Noise parameter has definitely been of incredible help. So much so that I have managed to train a decent model in only 1,000 training steps. However, there is an optimal threshold past of which causes the training to make the model spew gibberish. Will be researching this further.

An ongoing challenge remains that I still need quite a lot of training data. This shortage has proven to be crippling to the project, as it is quite difficult to train the model in emotional situations when there are none such data available. I have pleaded many times with the users and followers to help me, but as of now it seems my cries have fallen upon deaf ears. Or, perhaps, they are having just as much trouble as I am. It could easily be either. 
