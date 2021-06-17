# Question Classification in German - Evaluation of GottBERT-based approach

## Installation of Requirements
You need to have a Python 3.x version and pip already installed. 

Create a virtual environment where you'll install all the requirements:
```bash
apt-get update
apt-get install python-virtualenv
virtualenv question-classifier-german-venv
```
Activate the environment:
- on Windows:
    ```bash
    .\question-classifier-german-venv\Scripts\activate
    ```
- on Linux:
    ```bash
    source question-classifier-german-venv/bin/activate
    ```
After the activation of the virtual environment install the requirements:
```bash
pip install -U requests transformers[torch] setuptools wheel spacy
```
Also the first time you run the code, the gottbert model will be automatically downloaded.

Apart from the above, you will also need a tool we created in order to find if a sentence contains question words or question syntax. Please find more details about how to install and run this tool in the folder qcg-sentence-analyzer.

## Run the evaluation
In the *Data* folder there is a csv file that contains all the utterances of Dortmund corpus after a preprocessing and cleanup step. You can directly use this data to run your experiments. 

The pipeline.py file inside *Code* takes the aforementioned csv file and executes all the required steps in order to make predictions about the punctuation of the utterances and also convert those predictions from punctuation symbols to labels such as 'question', 'EOS', 'other'. This information is stored in another csv file inside the *Data* folder which can then be processed as a spreadsheet to extract statistics about the performance of the model. Apart from this file, some intermediate files are also stored in order that you will be able to run only a part of the code for subsequent experiments.

Inside the *Spreadsheets* folder you can find the spreadsheet we worked on, where you can see several experiments we made in order to come to some conclusions about this gottbert-based approach.


