from torch import optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from tqdm import tqdm
from transformers import BertForSequenceClassification, AutoModelForSequenceClassification

import torch

class Trainer:

    def __init__(
        self,
        model: AutoModelForSequenceClassification,
        train_dataset: Dataset,
        batch_size: int = 32,
        lr: float = 2e-5,
        epochs: int = 3,
        adam_epsilon=1e-8
    ):
        """
            Trainer for Neural Reranker.
            :param model: The bert model that will be trained.
            :param train_dataset: Training dataset.
            :param val_dataset: Validation dataset.
            :param batch_size: Batch size for training.
            :param lr: Learning rate.
            :param epochs: Number of training epochs.
        """
        
        self.model = model
        
        # Data Loaders
        collate_fn = self.build_collate_fn()
        self.train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr, eps=adam_epsilon)
        self.epochs = epochs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.best_loss = float("inf")

    def train(self):

        for epoch in range(self.epochs):
            print(f"Epoch {epoch + 1}")
            self.model.train()
            total_loss = 0

            for batch in tqdm(self.train_dataloader):
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["label"].float().to(self.device)

                # Zero out any previously accumulated gradients
                self.optimizer.zero_grad()

                # Forward pass
                outputs = self.model(input_ids, token_type_ids=None, attention_mask=attention_mask, labels=labels)

                loss = outputs.loss
                total_loss += loss.item()
                loss.backward()

                self.optimizer.step()

            avg_loss = total_loss / len(self.train_dataloader)
            print(f"Epoch {epoch + 1}/{self.epochs}, Loss: {avg_loss:.4f}")
            
            if avg_loss < self.best_loss:
                self.best_loss = avg_loss
                torch.save(self.model.state_dict(), "best_model.pth")
                print(f"Best model saved with validation loss: {avg_loss:.4f}")

    def build_collate_fn(self):
        def collate_fn(batch):
            input_ids = []
            attention_mask = []
            labels = []
            
            for sample in batch:
                input_ids.append(sample["input_ids"])
                attention_mask.append(sample["attention_mask"])
                labels.append(sample["label"])

            input_ids = pad_sequence(input_ids, batch_first=True, padding_value=0)
            attention_mask = pad_sequence(attention_mask, batch_first=True, padding_value=0)
            labels = torch.tensor(labels, dtype=torch.long)  # Use float for regression

            return {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "label": labels
            }
        
        return collate_fn