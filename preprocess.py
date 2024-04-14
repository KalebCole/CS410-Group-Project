from transformers import AutoTokenizer

def preprocess_code(code, tokenizer_name='roberta-base', max_length=512):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tokens = tokenizer.encode_plus(code, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt")
    return tokens["input_ids"], tokens["attention_mask"]
