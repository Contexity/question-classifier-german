# Installation

## Install Anaconda 
Install Anaconda from https://docs.anaconda.com/anaconda/install/ based on your operation system.
OR

Install curl if you don't have it
<pre>
sudo apt-get install curl
</pre>
Switch to the /tmp directory and use curl to download the installer using your command terminal:
<pre>
cd /tmp
curl –O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
</pre>
Verify data integrity of the installer
<pre>
sha256sum Anaconda3-2019.03-Linux-x86_64.sh
</pre>
Run the Anaconda script and after it finishes activate the installation
<pre>
bash Anaconda3-2019.03-Linux-x86_64.sh
source ~/.bashrc
</pre>

## Open Anaconda and create a new environment
- On Windows open a terminal called "Anaconda3"
- On Linux use the terminal

On both systems run:
<pre>
conda create --name nlp_server python=3.7
</pre>
to create the environment and install a python version.

## Activate env and install dependencies
To activate the above environment run: 
<pre>
conda activate nlp_server
</pre>

Install connexion
<pre>
pip install connexion
</pre>

Install openapi-generator
<pre>
pip install openapi-generator-cli # openapi generator for python
								  # needs Java installed, install from https://adoptopenjdk.net/ (currently desired version: 11LTS)
</pre>

Install spacy and download medium-sized language models (here, english and german)
<pre>
conda install -c conda-forge spacy
python -m spacy download en_core_web_md
python -m spacy download de_core_news_md
</pre>

Install other libraries
<pre>
conda install -c conda-forge textacy
conda install -c conda-forge conllu
pip install -r requirements.txt
</pre>

## Usage
From the current folder run:
<pre>
python -m openapi_server
</pre>
and open your browser to http://localhost:8080/ui/