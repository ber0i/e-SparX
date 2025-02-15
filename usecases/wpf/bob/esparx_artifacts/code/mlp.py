import torch.nn.functional as F
from torch import nn


class MLPLayer(nn.Module):
    def __init__(
        self,
        input_size,
        output_size,
        dropout,
        activation,
        norm_layer,
    ):
        super().__init__()

        self.hidden = nn.Linear(input_size, output_size)
        if norm_layer == "layer":
            self.norm = nn.LayerNorm(output_size)
        elif norm_layer == "batch":
            self.norm = nn.BatchNorm1d(output_size)
        else:
            self.norm = None
        self.activation = F.relu if activation == "relu" else F.leaky_relu
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.hidden(x)
        x = self.norm(x) if self.norm is not None else x
        x = self.dropout(self.activation(x))

        return x


class Model(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.lookback_timesteps = args.lookback_timesteps
        self.forecast_timesteps = args.forecast_timesteps
        self.n_hidden_neurons = args.n_hidden_neurons
        self.n_hidden_layers = args.n_hidden_layers
        self.dropout_rate = args.dropout_rate
        self.norm_layer = args.norm_layer
        self.activation = args.activation

        # Encoder
        self.mlp = nn.ModuleList(
            [
                MLPLayer(
                    input_size=(
                        self.n_hidden_neurons
                        if i != 0
                        else (self.lookback_timesteps * 3 + self.forecast_timesteps * 2)
                    ),
                    output_size=self.n_hidden_neurons,
                    dropout=self.dropout_rate,
                    activation=self.activation,
                    norm_layer=self.norm_layer,
                )
                for i in range(self.n_hidden_layers)
            ]
        )
        self.projection = nn.Linear(
            self.n_hidden_neurons, (self.forecast_timesteps), bias=True
        )

    def forward(self, x):

        # Pass through MLP
        for layer in self.mlp:
            x = layer(x)

        # Project
        output = self.projection(x)

        return output
