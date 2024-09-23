from models.layers import MLPLayer
from torch import nn


class Model(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.lookback_timesteps = args.lookback_timesteps
        self.forecast_timesteps = args.forecast_timesteps
        self.d_model = 512
        self.layers = 2
        self.dropout = 0.05
        self.norm_layer = "layer"
        self.activation = "relu"

        # Encoder
        self.mlp = nn.ModuleList(
            [
                MLPLayer(
                    input_size=(
                        self.d_model
                        if i != 0
                        else (self.lookback_timesteps * 3 + self.forecast_timesteps * 2)
                    ),
                    output_size=self.d_model,
                    dropout=self.dropout,
                    activation=self.activation,
                    norm_layer=self.norm_layer,
                )
                for i in range(self.layers)
            ]
        )
        self.projection = nn.Linear(self.d_model, (self.forecast_timesteps), bias=True)

    def forward(self, x):

        # Pass through MLP
        for layer in self.mlp:
            x = layer(x)

        # Project
        output = self.projection(x)

        return output
