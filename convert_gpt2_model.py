# coding=utf-8
# Copyright 2018 The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Convert OpenAI GPT checkpoint."""

import argparse



def convert_gpt2_checkpoint_to_pytorch(gpt2_checkpoint_path, full, gpt2_config_file, pytorch_dump_folder_path):
    #putting requirements here so users can see usage info before it errors out on missing modules
    from io import open
    from shutil import copyfile
    import logging
    logging.basicConfig(level=logging.INFO)
    from pathlib import Path
    import torch
    #WEIGHTS_NAME = "pytorch_model.bin"
    #CONFIG_NAME = "config.json"
    from transformers import (
        CONFIG_NAME,
        WEIGHTS_NAME,
        GPT2Config,
        GPT2Model,
        load_tf_weights_in_gpt2,
    )
    gpt2_checkpoint_path=Path(gpt2_checkpoint_path)
    print(gpt2_checkpoint_path.name)

    if pytorch_dump_folder_path=='':
        prefix = '32BIT-' if full else '16BIT-'
        pytorch_dump_folder_path='pytorch-'+prefix+gpt2_checkpoint_path.name
    pytorch_dump_folder_path=Path(pytorch_dump_folder_path)


    pytorch_dump_folder_path.mkdir(exist_ok=True)

    # Construct model
    if gpt2_config_file == "":
        #This doesn't seem to work. We will use the hparams.json file that seems to be included in 
        #config = GPT2Config()
        gpt2_config_file = gpt2_checkpoint_path/'hparams.json'

    config = GPT2Config.from_json_file(gpt2_config_file)
    model = GPT2Model(config)

    # Load weights from numpy
    load_tf_weights_in_gpt2(model, config, gpt2_checkpoint_path)
    if not full:
        model.half()

    # Save pytorch-model
    pytorch_weights_dump_path = pytorch_dump_folder_path/WEIGHTS_NAME
    pytorch_config_dump_path = pytorch_dump_folder_path/CONFIG_NAME
    print("Save PyTorch model to {}".format(str(pytorch_weights_dump_path)))

    torch.save(model.state_dict(), pytorch_weights_dump_path)

    print("Save configuration file to: "+str(pytorch_config_dump_path))
    with pytorch_config_dump_path.open("w", encoding="utf-8") as f:
        f.write(config.to_json_string())

    copyfile(gpt2_checkpoint_path/'vocab.bpe', pytorch_dump_folder_path/'merges.txt')
    copyfile(gpt2_checkpoint_path/'encoder.json', pytorch_dump_folder_path/'vocab.json')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    ## Required parameters
    parser.add_argument(
        "gpt2_checkpoint_path",
        type=str,
        help="Path to the TensorFlow checkpoint path.",
    )
    parser.add_argument(
        "--pytorch_dump_folder_path",
        default='',
        type=str,
        required=False,
        help="Path to the output PyTorch model.\n"
        "By default creates a new path based on the input path with pytorch-XXBIT- prefix",
    )
    parser.add_argument(
        "--gpt2_config_file",
        default="",
        type=str,
        help="An optional config json file corresponding to the pre-trained OpenAI model. \n"
        "This specifies the model architecture.\n"
        "Uses the hparams.json file if it exists. If that doesn't work see\n"
        "https://github.com/huggingface/transformers/blob/17ea43cf98/transformers/configuration_gpt2.py#L29\n"
        "for config files for several different gpt2 models"
    )
    parser.add_argument(
            "--full",
            action='store_true',
            help="Stores full 32 bit floating point instead of the default reduction to 16bit floating point."
    )
    args = parser.parse_args()
    convert_gpt2_checkpoint_to_pytorch(
        args.gpt2_checkpoint_path, args.full, args.gpt2_config_file, args.pytorch_dump_folder_path
    )


"""
download aidungeon2 v5 model from this torrent or elsewhere
-  magnet:?xt=urn:btih:b343b83b35bff774dab13e0281ce13b3daf37d3e&dn=model_v5&tr=udp%3a%2f%2ftracker.coppersurfer.tk%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.leechers-paradise.org%3a6969%2fannounce
The original AIDungeon2 stored the model as this directory: generator/gpt2/models/model_v5
For usage and useful information type:
python convert_gpt2_model.py --help
huggingface has many of these files available if you lose them. E.g. you can get a merges.txt and vocab.json file from these urls compatible with the original model:
https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-xl-merges.txt
https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-xl-vocab.json
"""
