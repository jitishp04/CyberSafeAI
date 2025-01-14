# Import necessary modules and classes
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from transformers import BertTokenizer, BertForSequenceClassification, BertTokenizerFast  # Added BertTokenizerFast
import torch
from .models import TextAnalysis
from config.model_manager import ModelManager
from django.core.cache import cache
from backend.config.logger import logger


# Fix the model path to match your actual directory
tokenizer = None
model = None

# Function to load the model and tokenizer
def load_model():
    """Load the model and tokenizer with the current version."""
    global tokenizer, model
    try:
        model_path = ModelManager.get_model_path()
        logger.info(f"Resolved model path: {model_path}")
        
        # Validate model path
        if not os.path.exists(os.path.join(model_path, "config.json")):
            raise FileNotFoundError(f"Model files missing at {model_path}")
        
        # Check cache
        cached_model_path = cache.get("model_path")
        if cached_model_path != model_path:
            logger.info(f"Model path updated. Reloading model from: {model_path}")
            cache.delete("model")
            cache.delete("tokenizer")
            cache.set("model_path", model_path)

        if cache.get('model') is None:
            # Use BertTokenizer instead of BertTokenizerFast
            tokenizer = BertTokenizer.from_pretrained(
                model_path, 
                local_files_only=True,
                use_fast=False  # Explicitly disable fast tokenizer
            )
            
            # Load model with additional parameters to handle large files
            model = BertForSequenceClassification.from_pretrained(
                model_path,
                local_files_only=True,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32,  # Explicitly set dtype
                revision="main"
            )
            
            model.eval()
            cache.set('model', model)
            cache.set('tokenizer', tokenizer)
            logger.info(f"Model loaded successfully from: {model_path}")
        else:
            tokenizer = cache.get('tokenizer')
            model = cache.get('model')
            
        return True

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

# Load initial model
load_model()



# View for the home page
def home(request):
    # Get filter parameters
    filter_type = request.GET.get("filter", "all")
    search_query = request.GET.get("search", "")

    # Base queryset
    analyses = TextAnalysis.objects.all().order_by("-created_at")

    # Apply filters
    if filter_type == "toxic":
        analyses = analyses.filter(toxic=True)
    elif filter_type == "clean":
        analyses = analyses.filter(toxic=False)

    # Apply search
    if search_query:
        analyses = analyses.filter(text__icontains=search_query)

    # Pagination
    paginator = Paginator(analyses, 10)  # Show 10 items per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "moderation/home.html", {
        "analyses": page_obj,
        "total_count": analyses.count(),
        "filter_type": filter_type,
        "search_query": search_query,
    })

# View to analyse text
@csrf_exempt
def analyze_text(request):
    global tokenizer, model

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"})

    text = request.POST.get("text", "").strip()
    if not text:
        return JsonResponse({"error": "No text provided"})

    # Check if we need to reload the model
    current_model_path = ModelManager.get_model_path()
    if model is None or current_model_path != getattr(model, '_model_path', None):
        if not load_model():
            return JsonResponse({"error": "BERT model not loaded properly"})
        # Store the path we loaded from
        model._model_path = current_model_path
    
    try:
        # Split text into words
        words = text.split()
        word_results = []
        highlighted_text = ""

        # Analyze each word individually
        for word in words:
            inputs = tokenizer(
                word,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            # Get predictions for individual word
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                probabilities = torch.sigmoid(logits).squeeze().tolist()
                
                if isinstance(probabilities, float):
                    probabilities = [probabilities]

            # Check if word is toxic, threat, or insult
            labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
            word_flags = {label: False for label in labels}

            for idx, label in enumerate(labels):
                if idx < len(probabilities):
                    probability = float(probabilities[idx])
                    if probability > 0.5:
                        word_flags[label] = True

            if any(word_flags.values()):
                word_results.append({
                    "word": word,
                    **word_flags
                })
                # Highlight toxic words
                highlighted_text += f'<span class="text-red-600 font-bold">{word}</span> '
            else:
                highlighted_text += f"{word} "

            print(f"Flagged words: {word_results}")  # Debugging output

        # Original full text analysis
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits).squeeze().tolist()
            
            if isinstance(probabilities, float):
                probabilities = [probabilities]

        labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
        results = {}

        for idx, label in enumerate(labels):
            if idx < len(probabilities):
                probability = float(probabilities[idx])
                is_toxic = probability > 0.5
                results[label] = {
                    "toxic": is_toxic,
                    "probability": probability
                }
            else:
                results[label] = {
                    "toxic": False,
                    "probability": 0.0
                }

        # Save to database
        analysis = TextAnalysis.objects.create(
            text=text,
            toxic=results["toxic"]["toxic"],
            toxic_probability=results["toxic"]["probability"],
            severe_toxic=results["severe_toxic"]["toxic"],
            severe_toxic_probability=results["severe_toxic"]["probability"],
            obscene=results["obscene"]["toxic"],
            obscene_probability=results["obscene"]["probability"],
            threat=results["threat"]["toxic"],
            threat_probability=results["threat"]["probability"],
            insult=results["insult"]["toxic"],
            insult_probability=results["insult"]["probability"],
            identity_hate=results["identity_hate"]["toxic"],
            identity_hate_probability=results["identity_hate"]["probability"],
        )

        return JsonResponse({
            "success": True,
            "results": results,
            "flagged_words": word_results,
            "highlighted_text": highlighted_text.strip(),
            "text": text,
            "id": analysis.id,
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Error analyzing text: {str(e)}"
        })