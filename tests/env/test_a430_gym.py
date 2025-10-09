import unittest

from a430py.env.a430_gym import A430Gym


class TestA430Gym(unittest.TestCase):
    def test_reset_1(self):
        print("In test reset 1: ")

        self.env = A430Gym()
        obs, info = self.env.reset()

        print(obs)

        self.assertAlmostEqual(obs[6], 0.0)  # fnpos
        self.assertAlmostEqual(obs[7], 0.0)  # fepos

    def test_step_1(self):
        print("In test step 1: ")

        self.env = A430Gym(custom_aircraft_config={"m": 0.5})
        obs, info = self.env.reset()

        # 用于配平的动作
        action = [0.0, -1.998228, 0.0, 0.689030]

        for i in range(60):
            next_obs, reward, terminated, truncated, info = self.env.step(action)
            print(f"step {i}: {next_obs}")

    def test_step_2(self):
        print("In test step 2: ")

        self.env = A430Gym()
        obs, info = self.env.reset()

        # 用于配平的动作
        action = [0.0, -1.998228, 0.0, 0.689030]

        for i in range(60):
            next_obs, reward, terminated, truncated, info = self.env.step(action)

        obs, info = self.env.reset()
        for i in range(60):
            next_obs, reward, terminated, truncated, info = self.env.step(action)
            print(f"step {i}: {next_obs}")

    def test_check_config(self):
        print(f"In test check_config: ")

        self.env = A430Gym(custom_aircraft_config={"m": 0.555})

        self.env.check_config()


if __name__ == "__main__":
    unittest.main()
