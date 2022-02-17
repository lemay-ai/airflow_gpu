"""
Inference script.

Can be expanded to include an inference switch-gate.
You can also load different models based on different 
inference activities.

"""

# Load all necessary libraries
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
tqdm().pandas()

import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

import sys, getopt



class Inference:
    

    def __init__(self):
        """
        Initialize the class and assign device.
        """
        if torch.cuda.is_available():
            dev = "cuda:0"
        else:
            dev = "cpu"
        device = torch.device(dev)
        torch.cuda.set_device(0)

        self.dev = dev


    def run_en_fr(self, data_path: str):

        """
        Translate data from English to French.
        
        """
        

        print("Running EN to FR Translation...")

        def batch(iterable, n=1):
            """
            Batching function for sentence groups.
            """
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]


        # load tokenizer and model.
        # Note: This will re-download the model every time this container is started.
        # TODO: The reader should load locally saved models.
        tokenizer         = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
        translation_model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-fr").to('cuda')

        # load specific data
        df = pd.read_csv(data_path)

        statements = df["Phrase"].tolist()

        translatedResults = []
        BATCH_SIZE = 50


        for batch_text_list in tqdm(batch(statements, BATCH_SIZE),total=len(statements)/BATCH_SIZE):
            translated = translation_model.generate(**tokenizer.prepare_seq2seq_batch(batch_text_list, return_tensors="pt").to('cuda'))

            results = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
            for item in results:
                translatedResults.append(item)

        df["translation"] = translatedResults

        df.to_csv("/data/output.csv")


        print("Translation complete.")
        

def main(argv):
    """
    Main argument parser function.
    Official entrypoint.
    """

    # Assuming English to French translation
    category = 'en_fr'


    # TODO: Add your own parameters and functions.
    # For this demo, we'll go straight to the EN/FR case.
    try:
        opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
        print('main_inference.py -t <type>')

        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main_inference.py -t <type> ')


        elif opt in ("-t", "--type"):
            category = arg



    # Run the target function - assumes no parameters were passed.
    inf = Inference()
    inf.run_en_fr('/data/train_full_sentences.csv')





if __name__ == "__main__":
    """
    Program entry point.
    """
    main(sys.argv[1:])
