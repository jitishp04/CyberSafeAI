## AI Model Folder

This folder is dedicated to the **AI model** that performs content analysis. It includes the logic for training the model, inference (making predictions), data preprocessing, and model serving.

### Folder structure:
#### 1. Test file:
- **/test/test_preprocessing.py**: Test if the data loads
  
#### 2. Utility files:
- **/utils**: Utility files for each step of the ML pipeline
  - **/combine_data.py**: Combine previous data with new user data
  - **/data_loader.py**: Load data as DataFrames
  - **/data_preprocessing.py**: Preprocess text to lowercase all characters, remove non-alphabetical characters, etc.
  - **/data_splitter.py**: Split the data for training and testing 
  - **/evaluation.py**: Evaluate the new trained model returns: accuracy, precision, recall, f1
  - **/logger.py**: Log all steps of the ML pipeline
  - **/model_save.py**: Versioning and saving the model to backend
  - **/training.py**: Trains the model, and tokenize's the data 

#### 3. Configuration file:
- **config.py**: Configuration file with information such as pre-trained model used, batch size, learning rate, etc.

#### 4. AI model training file:
- **train.py**: Main file that calls the utilities step by step to run the ML pipeline

### Purpose:
The **AI model** folder is responsible for the core content analysis functionality. It includes everything from dataset preparation to training a model that can detect toxicity and unethical language in text.
