from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, precision_recall_fscore_support
import torch

def evaluate_model(model, tokenizer, test_dataset):
    # Get the device model is on
    device = next(model.parameters()).device
    
    model.eval()
    predictions = []
    true_labels = []

    for _, row in test_dataset.iterrows():
        # Move inputs to the same device as model
        inputs_dict = tokenizer(
            row["comment_text"], 
            return_tensors="pt", 
            truncation=True, 
            padding=True
        )
        
        # Move input tensors to GPU
        inputs_dict = {k: v.to(device) for k, v in inputs_dict.items()}

        with torch.no_grad():
            outputs = model(**inputs_dict)
            
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()
        predictions.append(pred)
        true_labels.append(row["label"])

    # Convert lists to numpy arrays for sklearn metrics
    predictions = torch.tensor(predictions).cpu().numpy()
    true_labels = torch.tensor(true_labels).cpu().numpy()

    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, 
        predictions, 
        average="weighted"
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }