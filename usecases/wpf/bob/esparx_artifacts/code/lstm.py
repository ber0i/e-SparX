from torch import nn


class Model(nn.Module):
    def __init__(self, args):

        super().__init__()

        self.lookback_timesteps = args.lookback_timesteps
        self.forecast_timesteps = args.forecast_timesteps
        self.n_hidden_neurons = args.n_hidden_neurons
        self.n_hidden_layers = args.n_hidden_layers
        self.dropout_rate = args.dropout_rate

        self.lstm = nn.LSTM(
            input_size=self.lookback_timesteps * 3 + self.forecast_timesteps * 2,
            hidden_size=self.n_hidden_neurons,
            num_layers=self.n_hidden_layers,
            dropout=self.dropout_rate,
            batch_first=True,
        )
        self.projection = nn.Linear(
            in_features=self.n_hidden_neurons,
            out_features=self.forecast_timesteps,
        )

    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.projection(x)
        return x
