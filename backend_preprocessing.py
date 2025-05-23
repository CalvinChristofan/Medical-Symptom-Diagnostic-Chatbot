import tensorflow as tf
import numpy as np
import pickle
import json
import pandas as pd
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

DF_PATH = "scraping_disease_information_backend.csv"
MODEL_PATH = "best_model_predict_diseases.keras"
MAPPING_PATH = "mapping.pkl"
TOKENIZER_PATH = "tokenizer_disease.json"


def loadDf():
    df = pd.read_csv(DF_PATH)
    return df

def loadModel():
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

def loadMapping():
    with open(MAPPING_PATH, 'rb') as f:
        mapping = pickle.load(f)
    return mapping

def loadTokenizer():
    with open(TOKENIZER_PATH, "r") as file: 
        tokenizer_json = file.read()  
    tokenizer_config = json.loads(tokenizer_json)  
    tokenizer = tokenizer_from_json(tokenizer_config)  
    return tokenizer
    
# Preprocessing Functions
def cleaningText(text):
    text = re.sub(r'[0-9]+', '', text) 
    text = re.sub(r"(\w)'(\w)", r"\1 \2", text)
    text = re.sub(r'[^\w\s]', '', text)

    text = text.replace('\n', ' ') 
    text = text.strip(' ') 
    return text   

def casefoldingText(text): 
    text = text.lower()
    return text

def tokenizingText(text): 
    text = word_tokenize(text)
    return text

def deletedfrequentWord(text):
    words_to_remove = {"sometimes","experience","experiencing","symptoms", 
                       "frequent", "feel", "felt","feeling", "suffer", 
                       "notice", "detect", "perceive", "indication"
                       "occasionally","usually","often","always","irregularly"
                       "periodically", "discountinuously", "rarely", "frequently"
                       "started","today","day","yesterday","monday","tuesday","wednesday"
                       "thursday","friday","saturday","sunday","last","dawn","morning"
                       "afternoon","evening","night","midnight","thank","since"}
    
    filtered_text = [word for word in text if word not in words_to_remove]
    
    return filtered_text

def filteringText(text): 
    listStopwords1 = set(stopwords.words('english')) 
    filtered = [txt for txt in text if txt not in listStopwords1] 
    return ' '.join(filtered) 

def lemmatizeText(text):
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    lemmatized_text = ' '.join(lemmatized_words)
    
    return lemmatized_text


# Preprocessing Input Pipeline
def preprocess_input(user_input): 
    tokenizer = loadTokenizer()
    text_clean = cleaningText(user_input)
    text_casefoldingText = casefoldingText(text_clean)
    text_tokenizingText = tokenizingText(text_casefoldingText)
    text_deletedfrequentWord = deletedfrequentWord(text_tokenizingText)
    text_stopword = filteringText(text_deletedfrequentWord)
    text_lemmatizing = lemmatizeText(text_stopword)
    testing_seq = tokenizer.texts_to_sequences([text_lemmatizing])  
    testing_seq_padded = pad_sequences(testing_seq, maxlen=35, padding='post')
    
    return testing_seq_padded


# Predict with model pipeline (return in form of Json file)
def predict(preprocess_input):
    model = loadModel()
    mapping = loadMapping()
    df = loadDf()
    
    model_output = model.predict(preprocess_input)
    single_output = model_output[0]
    single_output = single_output / np.sum(single_output) 

    # Get the top 4 indices and probabilities
    top_4_indices = np.argsort(single_output)[-4:][::-1]  
    top_4_probs = single_output[top_4_indices]         
    top_4_percentages = top_4_probs * 100   
    
    json_file = {}
    i = 0 
    
    for disease in top_4_indices :
        disease_detail = {}
        disease_detail["similarity"] = str(top_4_percentages[i])
        disease_name = mapping.get(disease)
        disease_index = df.index[df["name"] == disease_name]
        disease_index = list(disease_index)[0]
        disease_detail["description"] = df['General Description'][disease_index]
        disease_detail["solution"] = df['Treatment'][disease_index]
        disease_detail['symptoms'] = df['Symptoms'][disease_index]
        json_file[disease_name] = disease_detail
        i+=1
    
    print(json_file)
    return json_file
