#!/bin/sh
# ./install.sh
## Install required python packages and downloads resources

# install packages
pip install -r ./requirements.txt

# download spacy language support
python -m spacy download en_core_web_md
python -m spacy download de_core_news_md
python -m spacy download it_core_news_md
python -m spacy download es_core_news_md
python -m spacy download fr_core_news_md
python -m spacy download pt_core_news_md

# Czech morphology annotation
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1836{/czech-morfflex-pdt-161115.zip}
unzip czech-morfflex-pdt-161115.zip
