#!/bin/bash


pip3 install -r requirements.txt
pip3 install -i https://pypi.org/simple/ bitsandbytes

wget -O model-00001-of-00002.safetensors https://huggingface.co/AlphJain/llm/resolve/main/model-00001-of-00002.safetensors?download=true
wget -O model-00002-of-00002.safetensors https://huggingface.co/AlphJain/llm/resolve/main/model-00002-of-00002.safetensors?download=true
wget -O tokenizer.json https://huggingface.co/AlphJain/llm/resolve/main/tokenizer.json?download=true
wget -O tokenizer_config.json https://huggingface.co/AlphJain/llm/resolve/main/tokenizer_config.json?download=true
wget -O tokenizer.model https://huggingface.co/AlphJain/llm/resolve/main/tokenizer.model?download=true
wget -O model.safetensors.index.json https://huggingface.co/AlphJain/llm/resolve/main/model.safetensors.index.json?download=true
wget -O config.json https://huggingface.co/AlphJain/llm/resolve/main/config.json?download=true
wget -O generation_config.json https://huggingface.co/AlphJain/llm/resolve/main/generation_config.json?download=true


mv $PWD/model-00001-of-00002.safetensors $PWD/models/model/model-00001-of-00002.safetensors
mv $PWD/model-00002-of-00002.safetensors $PWD/models/model/model-00002-of-00002.safetensors
mv $PWD/tokenizer.json $PWD/models/tokenizer/tokenizer.json
mv $PWD/tokenizer_config.json $PWD/models/tokenizer/tokenizer_config.json
mv $PWD/tokenizer.model $PWD/models/tokenizer/tokenizer.model
mv $PWD/model.safetensors.index.json $PWD/models/model/model.safetensors.index.json
mv $PWD/config.json $PWD/models/model/config.json
mv $PWD/generation_config.json $PWD/models/model/generation_config.json