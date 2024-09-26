Table of Content
## Introduction

This project aims to enhance code completion systems for Python by predicting the next token in Python method code. Leveraging an N-gram model, this approach predicts the likelihood of each possible next token based on the occurrences of token sequences in the training data. 

## Getting Started
### 2.1 Preparation
1. Clone the reposiritory

        git clone https://github.com/afia2023/Course-CSCI680-Afia.git

2. Navigate to the project directory: After cloning, you need to navigate into the project folder

        cd Course-CSCI680-Afia

### 2.2 Install Dependencies
     pip install -r requirements.txt

### 2.3 Run N-gram model 
(1) This script will execute the N-gram model with different sizes of N ranging from 2 to 7. After running models with all the N values, the N-gram model with size 3 (n=3) is observed to perform the best according to the validation set. This best-performing N-gram model is then applied to the test set to evaluate its performance and accuracy on unknown data. The model can also predict the next token in a sequence, specifically for Java methods or functions, by using the token probabilities learned from the training data. The evaluation results, including accuracy and other performance metrics, will help in determining how well the N-gram model generalizes to new data.

     python main3.py

(2) Collecting output serults from output_results5.txt
![alt text](image.png)

### Report

The assignment report is available in the attached file  N-gram(Assignment-1-afia).pdf

### Feature

This project showcases the development and utilization of a probabilistic n-gram language model designed to enhance code completion systems by predicting the next token in Python code sequences. Utilizing a dataset of approximately 32,000 Python method entries, the model learns from the context provided by previous tokens, thus improving the accuracy and efficiency of code writing. Key features of the project include:

Automated Extraction and Processing: Scripts automate the extraction of method code and documentation from multiple GitHub repositories, ensuring a streamlined and scalable setup.
Advanced Data Combination: A specialized script merges extracted data into a comprehensive JSON dataset, ready for analysis.
Robust Model Training and Evaluation: Implements n-gram models varying from 2 to 7 grams, evaluating each for maximum predictive performance using detailed accuracy and statistical metrics.
Practical Application: The best-performing model is made available for immediate use, aiding developers in real-time code prediction and enhancing coding efficiency.






