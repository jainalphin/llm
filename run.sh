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

mkdir models
cd models
mkdir model && mkdir tokenizer
cd ..

mv model-00001-of-00002.safetensors models/model/model-00001-of-00002.safetensors
mv model-00002-of-00002.safetensors models/model/model-00002-of-00002.safetensors
mv tokenizer.json models/tokenizer/tokenizer.json
mv tokenizer_config.json models/tokenizer/tokenizer_config.json
mv tokenizer.model models/tokenizer/tokenizer.model
mv model.safetensors.index.json models/model/model.safetensors.index.json
mv config.json models/model/config.json
mv generation_config.json models/model/generation_config.json