# 🩺 Diagno: Medical Symptom Diagnostic Chatbot


## 🧠 Overview
Diagno is an advanced machine learning model designed to analyze user-inputted symptoms in natural language (RNN) and predict the top 4 potential diseases based on the similarity. 

## 🚀 Features
- Natural Language Input – Accepts free-text symptom descriptions.
- Top 4 Disease Predictions – Ranked by relevance percentages.
- Comprehensive Output – Provides a general description, symptom list, and treatment info for each disease.
- Similarity Scoring – Percentage scores for how closely symptoms match each predicted disease.
 
## ⚙️ How It Works
- The user enters their symptoms as text.
- Diagno processes the input using natural language processing techniques to extract and interpret symptoms.
- The model use RNN to matches the extracted symptoms against a trained disease database.
- Diagno returns the top 4 potential diseases and their corresponding similarity percentages.
- Diagno also show the general descriptions, symptom, and treatment for each disease.


## 💾 Datasets & Models
Due to GitHub’s file size limits, large files are hosted on Google Drive:

- [augmented_disease_dataset.csv](https://drive.google.com/file/d/12AqEcHYaqaRC3UBXSK2KY0mNdYwpFRSL/view?usp=drive_link)
- [preprocessed_augmented_disease_dataset.csv](https://drive.google.com/file/d/1andxggEAGof6QPGfodhtlKMOzA53vv8r/view?usp=drive_link)


## 🧰 Prerequisites
To use Diagno, ensure you have the following prerequisites installed:
- python
- tensorflow
- numpy
- pandas
- nltk
- tkinter
- json
- pickle
- re
- subprocess
- matplotlib
- seaborn
- textwrap
- pathlib

To run Diagno (model_production), these are the additional prerequisites:
- sklearn
- collections
- time
- joblib

## 💻 How to Run the UI

Follow the steps below to run the Medical Symptom Diagnostic Chatbot UI:

### 1. Download the Project Files
Download all the source code files and place them in a single folder.

### 2. Download the Datasets
Download the required datasets from the provided [Google Drive link]([#datasets--models]) and place them in the appropriate directory.

### 3. Navigate to the Project Directory
Open a terminal in Visual Studio Code (or any terminal of your choice) and navigate to the project folder using the following command:
```bash 
cd /path/to/your/Medical-Symptom-Diagnostic-Chatbot-main
```

> 📝 Note: Replace `/path/to/your/Medical-Symptom-Diagnostic-Chatbot-main` with the actual path to the project directory on your computer.

### 4. Install Dependencies
   Install all the prerequisites and dependencies.

### 5. Run the Application
To start the chatbot UI, run main.py
run the following command:
```bash
python main.py 
```

Limitations:
- Not a Replacement for Professional Diagnosis: Diagno is a tool to assist users and is not a substitute for medical advice from licensed healthcare professionals.
- Langauge support: Currently only support input text in english only.
- Complex Cases: May struggle with rare diseases or symptoms not well-represented in the training data.
- Loading time: While model predict the user input instantly, UI take a fair amount of time to load.

Source code:
- Dicoding.com, Learn Machine Learning Development Bootcamp, Sentiment Analysis Project


Thank you for using Diagno! Together, we can make health insights more accessible.
