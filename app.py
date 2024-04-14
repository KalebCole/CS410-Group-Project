from model import Java_Code_Classifier 
from flask import Flask, request, jsonify
from model import load_model
from preprocess import preprocess_code
import torch

app = Flask(__name__)

# Configuration for your model
config = {
    'model_name': 'distilroberta-base',  # Update as needed
    'n_labels': 2  # Update based on your model's configuration
}
# At the start of your Flask app, after defining your config
model = Java_Code_Classifier(config, pretrained=False)
model.eval()  # Set the model to evaluation mode if not training


def run_model_on_code(code_snippet):
    # Preprocess the code snippet to get input_ids and attention_mask
    input_ids, attention_mask = preprocess_code(code_snippet)
    
    # Ensure the input tensors are moved to the same device as the model
    input_ids = input_ids.to(model.device)
    attention_mask = attention_mask.to(model.device)

    # Run the model
    with torch.no_grad():
        output = model(input_ids, attention_mask)
        
        # Assuming your model returns logits and you want to convert these to probabilities
        # This step is optional and depends on your model's output and how you want to interpret it
        probabilities = torch.softmax(output['logits'], dim=-1)
        predictions = torch.argmax(probabilities, dim=-1)

        return probabilities, predictions


@app.route('/predict', methods=['POST'])
def predict():
    print("Request received")
    data = request.json
    print(data)
    code = data.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    input_ids, attention_mask = preprocess_code(code)

    with torch.no_grad():
        output = model(input_ids=input_ids, attention_mask=attention_mask)  # Implicit forward call
        probabilities = torch.softmax(output['logits'], dim=-1)
        predictions = torch.argmax(probabilities, dim=-1)

    response_data = {'predictions': predictions.tolist(), 'probabilities': probabilities.tolist()}
    print("Response:", response_data)
    return jsonify(response_data)


def test():
    model_checkpoint_path = None
    # model_checkpoint_path = r'Models\epoch=9-step=10.ckpt'
    if model_checkpoint_path is not None:
        model = load_model(config, model_checkpoint_path)
    else:
        model = Java_Code_Classifier(config, pretrained=False)
        model.eval()  # Set the model to evaluation mode
    code_snippet = "public static void main(String[] args) { System.out.println('Hello, World!'); }"
    probabilities, predictions = run_model_on_code(code_snippet)
    print("Probabilities:", probabilities)
    print("Predictions:", predictions)
    
if __name__ == '__main__':
    # test()
    app.run(debug=True)