from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import Dataset
import torch

def train_model(train_dataset, model_name):
   # Check and set device
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

   # Initialize tokenizer and model
   tokenizer = BertTokenizer.from_pretrained(model_name)
   model = BertForSequenceClassification.from_pretrained(
       model_name,
       num_labels=6,
       problem_type="multi_label_classification"
   ).to(device)  # Move model to GPU if available

   def tokenize_function(examples):
       tokenized = tokenizer(examples["comment_text"], truncation=True, padding=True, max_length=128)
       # Add labels
       tokenized['labels'] = [
           [examples['toxic'][i], examples['severe_toxic'][i], examples['obscene'][i],
            examples['threat'][i], examples['insult'][i], examples['identity_hate'][i]]
           for i in range(len(examples['comment_text']))
       ]
       # Convert labels to float tensors and move to GPU if available
       tokenized['labels'] = torch.tensor(tokenized['labels'], dtype=torch.float).to(device)
       return tokenized

   # Convert DataFrame to Hugging Face Dataset
   train_dataset = Dataset.from_pandas(train_dataset)

   # Tokenize the dataset
   tokenized_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=train_dataset.column_names)

   # Data collator
   data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)

   # Training arguments with GPU setting
   training_args = TrainingArguments(
       output_dir='./models',
       num_train_epochs=3,
       per_device_train_batch_size=16,
       per_device_eval_batch_size=64,
       warmup_steps=500,
       weight_decay=0.01,
       logging_dir='./logs',
       no_cuda=False
   )

   # Initialize trainer
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=tokenized_dataset,
       data_collator=data_collator,
   )

   # Train model
   trainer.train()

   return model, tokenizer