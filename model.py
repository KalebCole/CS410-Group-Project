from transformers import AutoModel, AdamW, get_cosine_schedule_with_warmup, RobertaConfig
import torch.nn as nn
import math
import torch.nn.functional as F
import torch
import pytorch_lightning as pl

class Java_Code_Classifier(pl.LightningModule):

    def __init__(self, config: dict, pretrained=True):
        super().__init__()
        self.config = config
        if pretrained: # Load a pre-trained model from Hugging Face
            self.pretrained_model = AutoModel.from_pretrained(config['model_name'], return_dict=True)
        else: # Load a model configuration without pre-trained weights
            model_config = RobertaConfig()
            self.pretrained_model = AutoModel.from_config(model_config)
        self.hidden = torch.nn.Linear(self.pretrained_model.config.hidden_size, self.pretrained_model.config.hidden_size)
        self.classifier = torch.nn.Linear(self.pretrained_model.config.hidden_size, self.config['n_labels'])
        torch.nn.init.xavier_uniform_(self.classifier.weight)
        self.loss_func = nn.BCEWithLogitsLoss(reduction='mean')
        self.dropout = nn.Dropout()  # randomly turns several nodes on or off for training

    def forward(self, input_ids, attention_mask, labels=None):
        # roberta layer
        output = self.pretrained_model(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = torch.mean(output.last_hidden_state, 1)
        # final logits
        pooled_output = self.dropout(pooled_output)
        pooled_output = self.hidden(pooled_output)
        pooled_output = F.relu(pooled_output)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        # calculate loss
        loss = 0
        if labels is not None:
            loss = self.loss_func(logits.view(-1, self.config['n_labels']), labels.view(-1, self.config['n_labels']))
        return {'loss': loss, 'logits': logits}

    def training_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        self.log("train loss ", loss, prog_bar=True, logger=True)
        return {"loss": loss, "predictions": outputs, "labels": batch["labels"]}

    def validation_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        self.log("validation loss ", loss, prog_bar=True, logger=True)
        return {"val_loss": loss, "predictions": outputs, "labels": batch["labels"]}

    def predict_step(self, batch, batch_index):
        loss, outputs = self(**batch)
        return outputs

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.config['lr'], weight_decay=self.config['weight_decay'])
        total_steps = self.config['train_size'] / self.config['batch_size']
        warmup_steps = math.floor(total_steps * self.config['warmup'])
        scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps)
        return [optimizer], [scheduler]

def load_model(config, checkpoint_path):
    model = Java_Code_Classifier(config, pretrained=False)  # Initialize the model architecture
    model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')))  # Load your checkpoint
    model.eval()  # Set the model to evaluation mode
    return model

