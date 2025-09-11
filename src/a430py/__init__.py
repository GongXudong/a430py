from gymnasium.envs.registration import register

register(
    id="A430Gym-v0",
    entry_point="a430py.env.a430_gym:A430Gym",
)
