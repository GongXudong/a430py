from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from a430py.simulator.a430_sim import A430Simulator

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent


def test_init_simulator_from_default_config():
    print("In test trajectory 2 with plane initialized with default configs: ")

    sim = A430Simulator(config={})

    sim.init_plane_model(
        dLon=120,
        dLat=30,
        fAlt=10,
        fTAS=8,
        fYaw=90,
    )

    for i in range(60):
        next_state = sim.step(
            fStickLat=0.0,
            fStickLon=-1.998228,
            fThrottle=0.689030,
            fRudder=0,
        )


def test_init_simulator_from_customized_config():
    print("In test trajectory 3 with plane initialized with customized configs: ")
    custom_config = {
        "m": 0.543,
        "Jx": 1.5,
        "CLal": 3.0,
        "Cnbe": 2.0,
        "Cybe": 2.0,
    }
    sim = A430Simulator(config=custom_config)

    sim.init_plane_model(
        dLon=120,
        dLat=30,
        fAlt=10,
        fTAS=8,
        fYaw=90,
    )

    config_read_from_sim = {
        **sim.get_plane_const(),
        **sim.get_aero_coeffs(),
    }
    print(config_read_from_sim)

    for ky in custom_config.keys():
        print(
            f"check config {ky}, {custom_config[ky]}, {sim.get_config()[ky]}, {config_read_from_sim[ky]}"
        )
        assert custom_config[ky] == sim.get_config()[ky] == config_read_from_sim[ky]

    for i in range(60):
        next_state = sim.step(
            fStickLat=0.0,
            fStickLon=-1.998228,
            fThrottle=0.689030,
            fRudder=0,
        )


def test_reset_simulator():
    print("In test reset 1: ")
    custom_config = {
        "m": 0.123,
    }
    sim = A430Simulator(config=custom_config)
    print(f"check config: m = {sim.get_config()['m']}")

    sim.init_plane_model(
        dLon=120,
        dLat=30,
        fAlt=10,
        fTAS=8,
        fYaw=90,
    )

    for i in range(60):
        next_state = sim.step(
            fStickLat=0.0,
            fStickLon=-1.998228,
            fThrottle=0.689030,
            fRudder=0,
        )

    sim.reset(
        dLon=120,
        dLat=30,
        fAlt=10,
        fTAS=90,
        fYaw=90,
    )

    for i in range(60):
        next_state = sim.step(
            fStickLat=0.0,
            fStickLon=-1.998228,
            fThrottle=0.689030,
            fRudder=0,
        )


@pytest.mark.parametrize(
    "csv_path, eps",
    [
        (PROJECT_ROOT_DIR / "tests/simulator/trajectories/down_up_trace.csv", 1e-7),
    ],
)
def test_simulator_single_step(csv_path: Path, eps: float):
    print("In test single step 1: ")
    # 测试 state, action -> next_state

    sim = A430Simulator(config={})

    sim.reset(
        dLon=120,
        dLat=30,
        fAlt=10,
        fTAS=8,
        fYaw=90,
    )

    obs_df = pd.read_csv(csv_path)

    for index, row in obs_df.iterrows():
        if index + 1 < obs_df.shape[0]:
            print(f"step = {index}")

            sim.reset()

            sim.set_aircraft_state(
                vt=row["fTAS"],
                alpha=row["fAlpha"],
                beta=row["fBeta"],
                phi=row["fRoll"],
                theta=row["fPitch"],
                psi=row["fYaw"],
                p=row["fP"],
                q=row["fQ"],
                r=row["fR"],
                h=row["fAlt"],
            )

            print(f"\nobs: {sim.get_aircraft_output()}")

            for i in range(2):
                next_obs = sim.step(
                    fStickLat=row["fStickLat"],
                    fStickLon=row["fStickLon"],
                    fThrottle=row["fThrottle"],
                    fRudder=row["fRudder"],
                )

                print(f"\nnext_obs: {next_obs}")

            assert np.allclose(
                next_obs["fTAS"], obs_df.iloc[index + 1]["fTAS"], atol=eps
            )
            assert np.allclose(
                next_obs["fAlpha"], obs_df.iloc[index + 1]["fAlpha"], atol=eps
            )
            assert np.allclose(
                next_obs["fBeta"], obs_df.iloc[index + 1]["fBeta"], atol=eps
            )
            assert np.allclose(
                next_obs["fRoll"], obs_df.iloc[index + 1]["fRoll"], atol=eps
            )
            assert np.allclose(
                next_obs["fPitch"], obs_df.iloc[index + 1]["fPitch"], atol=eps
            )
            assert np.allclose(
                next_obs["fYaw"], obs_df.iloc[index + 1]["fYaw"], atol=eps
            )
            assert np.allclose(next_obs["fP"], obs_df.iloc[index + 1]["fP"], atol=eps)
            assert np.allclose(next_obs["fQ"], obs_df.iloc[index + 1]["fQ"], atol=eps)
            assert np.allclose(next_obs["fR"], obs_df.iloc[index + 1]["fR"], atol=eps)
            assert np.allclose(
                next_obs["fAlt"], obs_df.iloc[index + 1]["fAlt"], atol=eps
            )
            assert np.allclose(
                obs_df.iloc[index]["fnpos"] + next_obs["fnpos"],
                obs_df.iloc[index + 1]["fnpos"],
                atol=eps,
            )
            assert np.allclose(
                obs_df.iloc[index]["fepos"] + next_obs["fepos"],
                obs_df.iloc[index + 1]["fepos"],
                atol=eps,
            )


if __name__ == "__main__":
    test_init_simulator_from_customized_config()
    test_reset_simulator()
