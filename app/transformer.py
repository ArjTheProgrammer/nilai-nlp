# from transformers import pipeline
# import json

# classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
# # classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
# # classifier = pipeline(task="text-classification", model="michellejieli/emotion_text_classifier")

# # Example with cleaned text
# text = "People keep looking at me different and I think that they're making fun of me."
# print(json.dumps(classifier(text), indent=2))