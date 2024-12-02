import os
import pathlib
from datetime import timedelta

from commonpower.control.configs.algorithms import SB3MetaConfig, SB3PPOConfig
from commonpower.control.controllers import RLControllerSB3
from commonpower.control.runners import SingleAgentTrainer
from commonpower.control.safety_layer.penalties import DistanceDependingPenalty
from commonpower.control.safety_layer.safety_layers import ActionProjectionSafetyLayer
from commonpower.control.wrappers import SingleAgentWrapper
from commonpower.core import System
from stable_baselines3 import PPO


def setup_controller(
    forecast_horizon: timedelta,
    control_horizon: timedelta,
    control_sample_time: timedelta,
    total_training_steps: int,
    rl_model_weights_path: pathlib.Path,
    sys: System,
):

    if os.path.exists(f"{rl_model_weights_path}.zip"):
        # load pretrained if existing
        print("Model weights found. Loading pretrained agent.")
        agent = RLControllerSB3(
            name="agent",
            safety_layer=ActionProjectionSafetyLayer(
                penalty=DistanceDependingPenalty(penalty_factor=0.001)
            ),
            pretrained_policy_path=rl_model_weights_path,
        )
    else:
        agent = RLControllerSB3(
            name="agent",
            safety_layer=ActionProjectionSafetyLayer(
                penalty=DistanceDependingPenalty(penalty_factor=0.001)
            ),
        )

    # specify a seed for the random number generator used during training
    training_seed = 42

    # set up configuration for the PPO algorithm
    alg_config = SB3MetaConfig(
        total_steps=total_training_steps,
        seed=training_seed,
        algorithm=PPO,
        penalty_factor=0.001,
        algorithm_config=SB3PPOConfig(
            n_steps=24 * 6,  # 24 hours before parameter update
            learning_rate=0.0008,
            batch_size=24,  # -> 6 batches per day
            policy_kwargs=dict(log_std_init=-2),
        ),  # default hyperparameters for PPO
    )

    runner = SingleAgentTrainer(
        sys=sys,
        global_controller=agent,
        wrapper=SingleAgentWrapper,
        alg_config=alg_config,
        forecast_horizon=forecast_horizon,
        control_horizon=control_horizon,
        dt=control_sample_time,
        save_path=rl_model_weights_path,
        seed=alg_config.seed,
    )

    return agent, alg_config, runner
