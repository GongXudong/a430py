from ctypes import Structure, c_double, c_float


# 初始化参数结构体
class InitializeInfo(Structure):
    _fields_ = [
        ("dLon", c_double),
        ("dLat", c_double),
        ("fAlt", c_float),
        ("fTAS", c_float),
        ("fYaw", c_float),  # 单位：deg
    ]


# 状态结构体
class StateInfo(Structure):
    _fields_ = [
        ("vt", c_double),
        ("alpha", c_double),  # 单位：rad
        ("beta", c_double),  # 单位：rad
        ("phi", c_double),  # 单位：rad
        ("theta", c_double),  # 单位：rad
        ("psi", c_double),  # 单位：rad
        ("p", c_double),  # 单位：rad/s
        ("q", c_double),  # 单位：rad/s
        ("r", c_double),  # 单位：rad/s
        ("h", c_double),
    ]


# 状态输出结构体
class AircraftOutput(Structure):
    _fields_ = [
        ("dLon", c_double),
        ("dLat", c_double),
        ("fAlt", c_float),
        ("fRoll", c_float),  # 单位：deg
        ("fPitch", c_float),  # 单位：deg
        ("fYaw", c_float),  # 单位：deg
        ("fAlpha", c_float),  # 单位：deg
        ("fBeta", c_float),  # 单位：deg
        ("fP", c_float),  # 单位：deg/s
        ("fQ", c_float),  # 单位：deg/s
        ("fR", c_float),  # 单位：deg/s
        ("fVn", c_float),
        ("fVe", c_float),
        ("fVu", c_float),
        ("fAccBx", c_float),
        ("fAccBy", c_float),
        ("fAccBz", c_float),
        ("fTAS", c_float),
        ("fMach", c_float),
        ("fNvn", c_float),
        ("fnpos", c_float),
        ("fepos", c_float),
    ]


# 飞机特征参数
class PlaneConsts(Structure):
    _fields_ = [
        ("S", c_double),
        ("cbar", c_double),
        ("B", c_double),
        ("m", c_double),
        ("Jx", c_double),
        ("Jy", c_double),
        ("Jz", c_double),
        ("Jxz", c_double),
    ]


class AeroCoeffs(Structure):
    _fields_ = [
        ("CL0", c_double),
        ("CLal", c_double),
        ("CLq", c_double),
        ("CLde", c_double),
        ("CD0", c_double),
        ("CDk", c_double),
        ("CDde", c_double),
        ("CDda", c_double),
        ("Cy0", c_double),
        ("Cybe", c_double),
        ("Cyp", c_double),
        ("Cyr", c_double),
        ("Cyda", c_double),
        ("Cl0", c_double),
        ("Clbe", c_double),
        ("Clp", c_double),
        ("Clr", c_double),
        ("Clda", c_double),
        ("Cm0", c_double),
        ("Cmal", c_double),
        ("Cmq", c_double),
        ("Cmde", c_double),
        ("Cn0", c_double),
        ("Cnbe", c_double),
        ("Cnp", c_double),
        ("Cnr", c_double),
        ("Cnda", c_double),
    ]


# 控制输入结构体
class AircraftInput(Structure):
    _fields_ = [
        ("fStickLat", c_float),  # 杆横向位移
        ("fStickLon", c_float),  # 纵向杆位移
        ("fThrottle", c_float),  # 油门杆位移
        ("fRudder", c_float),  # 脚蹬位移
    ]
