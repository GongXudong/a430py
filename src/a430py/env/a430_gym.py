import gymnasium as gym
import numpy as np

from a430py.simulator.a430_sim import A430Simulator


class A430Gym(gym.Env):
    def __init__(
        self,
        initial_lon: float = 120.0,
        initial_lat: float = 30.0,
        initial_alt: float = 10.0,
        initial_tas: float = 8.0,
        initial_yaw: float = 90.0,
        max_steps: int = 100,
        custom_aircraft_config: dict = {},
    ):
        self.initial_lon = initial_lon
        self.initial_lat = initial_lat
        self.initial_alt = initial_alt
        self.initial_tas = initial_tas
        self.initial_yaw = initial_yaw

        self.observation_keys = [
            "fRoll",
            "fPitch",
            "fYaw",
            "fP",
            "fQ",
            "fR",
            "fnpos",
            "fepos",
            "fAlt",  # fAlt乘-1！！！
            "fTAS",
            "fAlpha",
            "fBeta",
        ]

        self.action_keys = [
            "fStickLat",  # 副翼指令
            "fStickLon",  # 升降舵指令
            "fRudder",
            "fThrottle",  # 油门指令
        ]

        self.step_cnt = 0
        self.max_steps = max_steps

        # 1.Define spaces
        ## 1.1 Observation space: vt, phi, theta, psi, alpha, beta, p, q, r, h
        self.observation_space = gym.spaces.Box(
            low=np.array(
                [0.0, -180.0, -90.0, -180.0, -30.0, -30.0, -300.0, -300.0, -300.0, 0.0],
                dtype=np.float32,
            ),
            high=np.array(
                [100.0, 180.0, 90.0, 180.0, 30.0, 30.0, 300.0, 300.0, 300.0, 100.0],
                dtype=np.float32,
            ),
        )
        ## 1.2 Action space: fStickLat, fStickLon, fRudder, fThrottle
        self.action_space = gym.spaces.Box(
            low=np.array(
                [
                    -10.0,
                    -10.0,
                    -10.0,
                    0.0,
                ],
                dtype=np.float32,
            ),
            high=np.array([10.0, 10.0, 10.0, 1.0], dtype=np.float32),
        )

        # 2.Init simulator
        self.simulator = A430Simulator(config=custom_aircraft_config)
        self.simulator.init_plane_model(
            dLon=self.initial_lon,
            dLat=self.initial_lat,
            fAlt=self.initial_alt,
            fTAS=self.initial_tas,
            fYaw=self.initial_yaw,
        )

    def close(self):
        del self.simulator

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)

        self.step_cnt = 0

        obs_dict = self.simulator.reset(
            dLon=self.initial_lon,
            dLat=self.initial_lat,
            fAlt=self.initial_alt,
            fTAS=self.initial_tas,
            fYaw=self.initial_yaw,
        )
        info = {}
        return self.get_observation(obs_dict=obs_dict), info

    def step(self, action):
        obs_dict = self.simulator.step(
            fStickLat=action[0],
            fStickLon=action[1],
            fRudder=action[2],
            fThrottle=action[3],
        )

        self.step_cnt += 1
        reward = 0

        if self.step_cnt >= self.max_steps:
            terminated = True
            truncated = True
        else:
            terminated = False
            truncated = False

        info = {}

        return (
            self.get_observation(obs_dict=obs_dict),
            reward,
            terminated,
            truncated,
            info,
        )

    def get_observation(self, obs_dict: dict) -> np.ndarray:
        return np.array([obs_dict[ky] for ky in self.observation_keys])

    def get_action(self, act_dict: dict) -> np.ndarray:
        return np.array([act_dict[ky] for ky in self.action_keys])

    def check_config(self):
        print(
            f"In python, check config, m = {self.simulator._config['m']}, B = {self.simulator._config['B']}"
        )
        self.simulator.a430_model.check_config(self.simulator.planePtr)
