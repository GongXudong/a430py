import gc
import platform
from ctypes import CDLL, POINTER, byref, c_double, c_int, c_uint64
from pathlib import Path

import numpy as np

from a430py.simulator.utils.a430_types import (
    AeroCoeffs,
    AircraftInput,
    AircraftOutput,
    InitializeInfo,
    PlaneConsts,
    StateInfo,
)

PROJECT_ROOT_DIR = Path(__file__).parent


class A430Simulator(object):
    def __init__(self, config: dict) -> None:
        self.step_time = 0.01  # 单拍时间，秒
        self.order = 1  # 龙格-库塔的阶数
        self.custom_config = config
        self._config: dict = self.__class__.get_default_config()
        self.output_fields = [
            "dLon",
            "dLat",
            "fAlt",
            "fRoll",
            "fPitch",
            "fYaw",
            "fAlpha",
            "fBeta",
            "fP",
            "fQ",
            "fR",
            "fVn",
            "fVe",
            "fVu",
            "fAccBx",
            "fAccBy",
            "fAccBz",
            "fTAS",
            "fMach",
            "fNvn",
            "fnpos",
            "fepos",
        ]
        self.plane_const_fields = [
            "S",
            "cbar",
            "B",
            "m",
            "Jx",
            "Jy",
            "Jz",
            "Jxz",
        ]
        self.aero_coeff_fields = [
            "CL0",
            "CLal",
            "CLq",
            "CLde",
            "Cy0",
            "Cybe",
            "Cyp",
            "Cyr",
            "Cyda",
            "Cl0",
            "Clbe",
            "Clp",
            "Clr",
            "Clda",
            "Cm0",
            "Cmal",
            "Cmq",
            "Cmde",
            "Cn0",
            "Cnbe",
            "Cnp",
            "Cnr",
            "Cnda",
        ]

        self.initDll()
        self.initArgs()
        self.initDllFuncTypes()

        self.set_config(config=config)

        # self.init_plane_model()

    def initDll(self) -> None:
        """加载dll"""
        osType = platform.system()
        if osType == "Linux":
            dll_path = str(
                PROJECT_ROOT_DIR.parent.parent.parent / "build/liba430plane.so"
            )
        elif osType == "Windows":
            dll_path = str(PROJECT_ROOT_DIR / "libs/a430plane.dll")
        else:
            raise Exception("Unsupported OS, only Linux and Windows are supported!!!")

        self.a430_model = CDLL(dll_path)

    def initArgs(self) -> None:
        """初始化dll定义的部分对象"""
        self.init_info: InitializeInfo = InitializeInfo()
        self.aircraft_input: AircraftInput = AircraftInput()
        self.aircraft_output: AircraftOutput = AircraftOutput()
        self.aircraft_output_delta: AircraftOutput = AircraftOutput()
        self.aircraft_state: StateInfo = StateInfo()

        self.plane_consts: PlaneConsts = PlaneConsts()
        self.aero_coeffs: AeroCoeffs = AeroCoeffs()

        self.plane_consts_for_read: PlaneConsts = PlaneConsts()
        self.aero_coeffs_for_read: AeroCoeffs = AeroCoeffs()

    def initDllFuncTypes(self) -> None:
        """设定dll函数输入输出"""
        self.a430_model.initialize.argtypes = [c_double, c_int, InitializeInfo]
        self.a430_model.initialize.restype = c_uint64

        self.a430_model.initialize2.argtypes = [
            c_double,
            c_int,
            InitializeInfo,
            PlaneConsts,
            AeroCoeffs,
        ]
        self.a430_model.initialize2.restype = c_uint64

        self.a430_model.set_input.argtypes = [c_uint64, AircraftInput]
        self.a430_model.update.argtypes = [c_uint64]
        self.a430_model.get_plane_consts.argtypes = [c_uint64, POINTER(PlaneConsts)]
        self.a430_model.get_aero_coeffs.argtypes = [c_uint64, POINTER(AeroCoeffs)]
        self.a430_model.check_config.argtypes = [c_uint64]
        self.a430_model.get_output.argtypes = [c_uint64, POINTER(AircraftOutput)]
        self.a430_model.get_delta.argtypes = [c_uint64, POINTER(AircraftOutput)]
        self.a430_model.terminate_plane.argtypes = [c_uint64]
        self.a430_model.set_state.argtypes = [c_uint64, StateInfo]

    def init_plane_model(
        self,
        dLon: float = 120.0,
        dLat: float = 30.0,
        fAlt: float = 10.0,
        fTAS: float = 8.0,
        fYaw: float = 90.0,
    ) -> None:
        self.set_init_info(dLon=dLon, dLat=dLat, fAlt=fAlt, fTAS=fTAS, fYaw=fYaw)
        # 创建飞机实例
        self.planePtr = self.a430_model.initialize2(
            self.step_time,
            self.order,
            self.init_info,
            self.plane_consts,
            self.aero_coeffs,
        )

        # if self.custom_config == {}:
        #     # use default parameters
        #     print(f"Init with initialize!!!")
        #     self.planePtr = self.a430_model.initialize(self.step_time, self.order, self.init_info)
        # else:
        #     # use customed parameters
        #     print(f"Init with initialize2!!!")
        #     self.planePtr = self.a430_model.initialize2(self.step_time, self.order, self.init_info, self.plane_consts, self.aero_coeffs)

    def __del__(self) -> None:
        # 飞机销毁
        # print("释放simulator资源...")

        if hasattr(self, "a430_model") and hasattr(self, "planePtr"):
            # print("释放c++指针：planePtr")
            self.a430_model.terminate_plane(self.planePtr)

        if hasattr(self, "a430_model"):
            # print("释放dll：a430_model")
            del self.a430_model

        gc.collect()

    def set_init_info(
        self,
        dLon: float = 120.0,
        dLat: float = 30.0,
        fAlt: float = 10.0,
        fTAS: float = 80.0,
        fYaw: float = 90.0,
    ) -> None:
        """设置飞机初始状态

        Args:
            dLon (float, optional): 初始经度. Defaults to 120..
            dLat (float, optional): 初始纬度. Defaults to 30..
            fAlt (float, optional): 海拔高度. Defaults to 10..
            fTAS (float, optional): 真空速. Defaults to 80..
            fYaw (float, optional): 航向. Defaults to 90..
        """
        self.init_info.dLon = dLon
        self.init_info.dLat = dLat
        self.init_info.fAlt = fAlt
        self.init_info.fTAS = fTAS
        self.init_info.fYaw = fYaw

    def set_aircraft_input(
        self,
        fStickLat: float = 0.0,
        fStickLon: float = 0.0,
        fThrottle: float = 0.0,
        fRudder: float = 0.0,
    ) -> None:
        self.aircraft_input.fStickLat = fStickLat
        self.aircraft_input.fStickLon = fStickLon
        self.aircraft_input.fThrottle = fThrottle
        self.aircraft_input.fRudder = fRudder

        self.a430_model.set_input(self.planePtr, self.aircraft_input)

    def set_aircraft_state(
        self,
        vt: float = 0.0,
        alpha: float = 0.0,
        beta: float = 0.0,
        phi: float = 0.0,
        theta: float = 0.0,
        psi: float = 0.0,
        p: float = 0.0,
        q: float = 0.0,
        r: float = 0.0,
        h: float = 0.0,
    ) -> None:
        self.aircraft_state.vt = vt
        self.aircraft_state.alpha = np.deg2rad(alpha)
        self.aircraft_state.beta = np.deg2rad(beta)
        self.aircraft_state.phi = np.deg2rad(phi)
        self.aircraft_state.theta = np.deg2rad(theta)
        self.aircraft_state.psi = np.deg2rad(psi)
        self.aircraft_state.p = np.deg2rad(p)
        self.aircraft_state.q = np.deg2rad(q)
        self.aircraft_state.r = np.deg2rad(r)
        self.aircraft_state.h = h

        # print(
        #     f"In set_state (python): vt = {vt}, alpha: {alpha}, beta = {beta}, phi = {phi}, theta = {theta}, psi = {psi}, p = {p}, q = {q}, r = {r}, h = {h}"
        # )

        self.a430_model.set_state(self.planePtr, self.aircraft_state)

    def get_aircraft_output(self) -> dict:
        self.a430_model.get_output(self.planePtr, byref(self.aircraft_output))
        return {ky: getattr(self.aircraft_output, ky) for ky in self.output_fields}

    def get_plane_const(self) -> dict:
        self.a430_model.get_plane_consts(
            self.planePtr, byref(self.plane_consts_for_read)
        )
        return {
            ky: getattr(self.plane_consts_for_read, ky)
            for ky in self.plane_const_fields
        }

    def get_aero_coeffs(self) -> dict:
        self.a430_model.get_aero_coeffs(self.planePtr, byref(self.aero_coeffs_for_read))
        return {
            ky: getattr(self.aero_coeffs_for_read, ky) for ky in self.aero_coeff_fields
        }

    @staticmethod
    def get_default_config() -> dict:
        return {
            # plane_const, 8个
            "S": 0.040809,
            "cbar": 0.09781,
            "B": 0.43,
            "m": 0.1,
            "Jx": 0.00400,
            "Jy": 0.00732,
            "Jz": 0.01093,
            "Jxz": 0.00014,
            # aero_coeffs, 27个
            "CL0": 0.2,
            "CLq": 6.898814,
            "CLal": 4.235972,
            "CLde": 0.011006,
            "CD0": 0.04735,
            "CDk": 1.0,
            "CDde": -0.0013,
            "CDda": 0.000149,
            "Cy0": 0.0,
            "Cybe": -0.356799,
            "Cyp": -0.230683,
            "Cyr": 0.378474,
            "Cyda": -0.004417,
            "Cl0": 0.0,
            "Clbe": -0.01363,
            "Clp": -0.340622,
            "Clr": 0.015922,
            "Clda": -0.006115,
            "Cm0": 0.0,
            "Cmal": -0.459587,
            "Cmq": -6.644907,
            "Cmde": -0.021453,
            "Cn0": 0.0,
            "Cnbe": 0.158268,
            "Cnp": 0.110384,
            "Cnr": -0.185416,
            "Cnda": 0.002108,
        }

    def get_config(self) -> dict:
        return self._config

    def set_config(self, config: dict) -> None:
        self.custom_config = config
        self._config.update(config)

        assert set(self.__class__.get_default_config().keys()) <= set(
            self._config.keys()
        ), f"config must contain keys: {self.__class__.get_default_config().keys()}!"

        self.plane_consts.S = self._config["S"]
        self.plane_consts.cbar = self._config["cbar"]
        self.plane_consts.B = self._config["B"]
        self.plane_consts.m = self._config["m"]
        self.plane_consts.Jx = self._config["Jx"]
        self.plane_consts.Jy = self._config["Jy"]
        self.plane_consts.Jz = self._config["Jz"]
        self.plane_consts.Jxz = self._config["Jxz"]

        self.aero_coeffs.CL0 = self._config["CL0"]
        self.aero_coeffs.CLq = self._config["CLq"]
        self.aero_coeffs.CLal = self._config["CLal"]
        self.aero_coeffs.CLde = self._config["CLde"]

        self.aero_coeffs.CD0 = self._config["CD0"]
        self.aero_coeffs.CDk = self._config["CDk"]
        self.aero_coeffs.CDde = self._config["CDde"]
        self.aero_coeffs.CDda = self._config["CDda"]

        self.aero_coeffs.Cy0 = self._config["Cy0"]
        self.aero_coeffs.Cybe = self._config["Cybe"]
        self.aero_coeffs.Cyp = self._config["Cyp"]
        self.aero_coeffs.Cyr = self._config["Cyr"]
        self.aero_coeffs.Cyda = self._config["Cyda"]

        self.aero_coeffs.Cl0 = self._config["Cl0"]
        self.aero_coeffs.Clbe = self._config["Clbe"]
        self.aero_coeffs.Clp = self._config["Clp"]
        self.aero_coeffs.Clr = self._config["Clr"]
        self.aero_coeffs.Clda = self._config["Clda"]

        self.aero_coeffs.Cm0 = self._config["Cm0"]
        self.aero_coeffs.Cmal = self._config["Cmal"]
        self.aero_coeffs.Cmq = self._config["Cmq"]
        self.aero_coeffs.Cmde = self._config["Cmde"]

        self.aero_coeffs.Cn0 = self._config["Cn0"]
        self.aero_coeffs.Cnbe = self._config["Cnbe"]
        self.aero_coeffs.Cnp = self._config["Cnp"]
        self.aero_coeffs.Cnr = self._config["Cnr"]
        self.aero_coeffs.Cnda = self._config["Cnda"]

    def reset(
        self,
        dLon: float = 120.0,
        dLat: float = 30.0,
        fAlt: float = 10.0,
        fTAS: float = 80.0,
        fYaw: float = 90.0,
    ) -> dict:
        if hasattr(self, "a430_model") and hasattr(self, "planePtr"):
            self.a430_model.terminate_plane(self.planePtr)

        self.init_plane_model(dLon=dLon, dLat=dLat, fAlt=fAlt, fTAS=fTAS, fYaw=fYaw)
        return self.get_aircraft_output()

    def step(
        self,
        fStickLat: float = 0.0,
        fStickLon: float = 0.0,
        fThrottle: float = 0.0,
        fRudder: float = 0.0,
    ) -> dict:
        # 设置控制量
        self.set_aircraft_input(
            fStickLat=fStickLat,
            fStickLon=fStickLon,
            fThrottle=fThrottle,
            fRudder=fRudder,
        )
        # 更新飞机状态
        self.a430_model.update(self.planePtr)
        # 读取飞机输出状态
        return self.get_aircraft_output()

    def step_from_customized_observation(
        self,
        obs_vt: float = 0.0,
        obs_alpha: float = 0.0,
        obs_beta: float = 0.0,
        obs_phi: float = 0.0,
        obs_theta: float = 0.0,
        obs_psi: float = 0.0,
        obs_p: float = 0.0,
        obs_q: float = 0.0,
        obs_r: float = 0.0,
        obs_h: float = 0.0,
        act_fStickLat: float = 0.0,
        act_fStickLon: float = 0.0,
        act_fThrottle: float = 0.0,
        act_fRudder: float = 0.0,
        update_times: int = 1,
    ):
        self.reset()
        self.set_aircraft_state(
            vt=obs_vt,
            alpha=obs_alpha,
            beta=obs_beta,
            phi=obs_phi,
            theta=obs_theta,
            psi=obs_psi,
            p=obs_p,
            q=obs_q,
            r=obs_r,
            h=obs_h,
        )
        for _ in range(update_times):
            next_obs = self.step(
                fStickLat=act_fStickLat,
                fStickLon=act_fStickLon,
                fThrottle=act_fThrottle,
                fRudder=act_fRudder,
            )

        return next_obs
