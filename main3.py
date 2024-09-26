import pickle
import sys
import logging
import re
import json
from collections import defaultdict, Counter

# Setting logging level to INFO to avoid printing warnings
logging.basicConfig(level=logging.INFO)

# Define a regular function to replace lambda
def counter_defaultdict():
    return defaultdict(Counter)

# Load the dataset
def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return None
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None

# Improved tokenizer using regex
def tokenize(method):
    return re.findall(r'[A-Za-z_]\w*|\S', method)

# Function to build an N-gram model
def build_ngram_model(methods, N):
    model = defaultdict(counter_defaultdict)
    for method in methods:
        tokens = ['<start>'] * (N-1) + tokenize(method) + ['<end>']
        for i in range(len(tokens) - N + 1):
            prefix = tuple(tokens[i:i+N-1])
            token = tokens[i+N-1]

            # Reset the Counter without logging
            if not isinstance(model[prefix], Counter):
                model[prefix] = Counter()

            model[prefix][token] += 1  # Safely increment the token count

    return model

# Predict the next token
def predict_next_token(model, prefix):
    if prefix in model:
        return max(model[prefix].items(), key=lambda item: item[1], default=('Unknown', 0))
    return ('Unknown', 0)

# Evaluate the model by predicting one token at a time and show only the first 10 results
def evaluate_model_single_token(model, test_methods, N, show_first_n=10, file=None):
    correct = 0
    total = 0
    results_to_show = []  # Store first 10 results

    # Process 100 inputs from the test set automatically
    for method in test_methods[:100]:  # Automatically take the first 100 test inputs
        tokens = ['<start>'] * (N-1) + tokenize(method) + ['<end>']
        for i in range(len(tokens) - N + 1):
            prefix = tuple(tokens[i:i+N-1])
            actual = tokens[i+N-1]

            # Predict the next token using the model
            predicted, _ = predict_next_token(model, prefix)

            # Compare predicted token with actual token
            if predicted == actual:
                correct += 1  # Count if prediction is correct
            total += 1  # Increment total number of predictions

            # Store the first 10 predictions for display
            if len(results_to_show) < show_first_n:
                results_to_show.append((prefix, predicted, actual))

    # Write the results to both the console and the file
    print("\nShowing first 10 token predictions and their actual matches:")
    if file:
        file.write("\nShowing first 10 token predictions and their actual matches:\n")
    
    for result in results_to_show:
        prefix, predicted, actual = result
        console_output = f"Prefix: {prefix}, Predicted: {predicted}, Actual: {actual}"
        print(console_output)
        
        if file:
            file.write(console_output + '\n')

    # Calculate and return accuracy
    accuracy = correct / total
    accuracy_message = f"\nAccuracy: {accuracy:.4f}\n"
    print(accuracy_message)
    
    if file:
        file.write(accuracy_message)

    return correct / total

# Function to save the model to a file
def save_model(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {filename}")

# Main function to train multiple models, save the best one, and save the output
def main():
    methods = load_data('Dataset_methods.json')
    if methods is None:
        return  # Exit if data could not be loaded

    # Use the full dataset for training, validation, and testing
    train_set = methods[:-200]        # Training set (everything except the last 200)
    validation_set = methods[-200:-100]  # Validation set (next 100)
    test_set = methods[-100:]         # Test set (last 100)

    max_n = 7  # Increase size to 7-gram
    accuracies = {}

    # Open the output file for writing
    with open('output_results5.txt', 'w') as output_file:
        # Train and evaluate models for different values of N (2-gram to max_n-gram)
        for N in range(2, max_n + 1):  # Train models from 2-gram to 7-gram
            model = build_ngram_model(train_set, N)  # Train the model using the training set
            accuracy = evaluate_model_single_token(model, validation_set, N, show_first_n=0)  # Evaluate on validation set
            accuracies[N] = accuracy
            logging.info(f"Accuracy of {N}-gram model on validation set: {accuracy:.4f}")
            # Write validation accuracies to the file
            output_file.write(f"Accuracy of {N}-gram model on validation set: {accuracy:.4f}\n")

        # Select the best-performing model based on accuracy on the validation set
        best_n = max(accuracies, key=lambda x: accuracies[x])
        best_model = build_ngram_model(train_set, best_n)
        logging.info(f"The best performing model is the {best_n}-gram with accuracy {accuracies[best_n]:.4f}")

        # Write the best performing model to the file
        output_file.write(f"\nThe best performing model is the {best_n}-gram model with accuracy {accuracies[best_n]:.4f}\n")
        output_file.write("\nPredicting tokens for 100 input test tasks:\n")

        # Save the best-performing model to a file
        save_model(best_model, f'best_model_{best_n}_gram.pkl')

        # Now use the best model for the 100-input token prediction task (test set)
        print(f"\nUsing the {best_n}-gram model for the 100 input test task...\n")
        evaluate_model_single_token(best_model, test_set, best_n, show_first_n=10, file=output_file)

if __name__ == '__main__':
    main()
