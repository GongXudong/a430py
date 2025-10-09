import numpy as np

from a430py.env.a430_gym import A430Gym


def test_reset_1():
    print("In test reset 1: ")

    env = A430Gym()
    obs, info = env.reset()

    print(obs)

    assert np.allclose(obs[6], 0.0)  # fnpos
    assert np.allclose(obs[7], 0.0)  # fepos


def test_step_1():
    print("In test step 1: ")

    env = A430Gym(custom_aircraft_config={"m": 0.5})
    obs, info = env.reset()

    # 用于配平的动作
    action = [0.0, -1.998228, 0.0, 0.689030]

    for i in range(60):
        next_obs, reward, terminated, truncated, info = env.step(action)
        # print(f"step {i}: {next_obs}")


def test_step_2():
    print("In test step 2: ")

    env = A430Gym()
    obs, info = env.reset()

    # 用于配平的动作
    action = [0.0, -1.998228, 0.0, 0.689030]

    for i in range(60):
        next_obs, reward, terminated, truncated, info = env.step(action)

    obs, info = env.reset()
    for i in range(60):
        next_obs, reward, terminated, truncated, info = env.step(action)
        # print(f"step {i}: {next_obs}")


def test_check_config():
    print(f"In test check_config: ")

    env = A430Gym(custom_aircraft_config={"m": 0.555, "B": 0.6})

    env.check_config()


if __name__ == "__main__":
    test_check_config()
