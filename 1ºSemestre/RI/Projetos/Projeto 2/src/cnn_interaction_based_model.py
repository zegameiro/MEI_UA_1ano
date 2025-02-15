import torch
import torch.nn as nn 
import torch.nn.functional as F

class CNNInteractionBasedModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        self.vocab_size = vocab_size

        # Embedding layer
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=300, padding_idx=0, max_norm=1)

        # Convolutional layer
        self.conv = nn.Conv2d(in_channels=1, out_channels=100, kernel_size=(3, 3))

        # Fully connected layer
        self.fc = nn.Linear(100, 1)

        # Activation layer
        self.activation = nn.ReLU()

        # Sigmoid for probabilistic output
        self.sigmoid = nn.Sigmoid()

    def forward(self, query: list[int], document: list[int]) -> float:

        # Convert query and documents IDs into embeddings
        query_embed = self.embedding(query)
        document_embed = self.embedding(document)

        # Create interaction matrix
        interaction_matrix = torch.bmm(query_embed, document_embed.transpose(1, 2))

        # Add a channel dimension for convolution
        interaction_matrix = interaction_matrix.unsqueeze(1)

        # Apply convolution
        conv_output = self.conv(interaction_matrix)
        conv_output = self.activation(conv_output)

        # Apply max pooling
        pooled_output = F.max_pool2d(conv_output, kernel_size=conv_output.size()[2:])
        pooled_output = pooled_output.squeeze()

        # Apply fully connected layer
        logits = self.fc(pooled_output)

        # Convert logits to probabilities
        prob = self.sigmoid(logits)

        return prob