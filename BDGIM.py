import datetime
import math
import numpy as np
# 常量
LAT_POLE = 80.27                  # 北地磁极的纬度 [单位:度]
LON_POLE = -72.58                 # 北地磁极的东经 [单位:度]
Hion_bdgim = 400000.0             # 电离层高度 [单位:m]
EARTH_RADIUS = 6378137.0          # 地球平均半径，用于计算IPP [单位:m]

# 每天初始的MJD，用于确定是否重新计算非广播参数
Init_mjd = 0.0
# Constants
PI = 4.0 * math.atan(1.0)
FREQ1_BDS = 1575420000.0  # 北斗三号B1C频率（赫兹）
BRDPARANUM = 9  # 广播电离层参数的数量
PERIODNUM = 13  # 每个非广播参数的预报周期数
TRISERINUM = PERIODNUM * 2 - 1  # 三角级数的项数
NONBRDNUM = 17  # 非广播一组的数量
MAXGROUP = 12  # 每天12组非广播系数


# Non-Broadcast Ionospheric Parameters Struct
class NonBrdIonData:
    def __init__(self):
        # 球谐函数的度和阶的索引
        self.degOrd = [[0 for _ in range(2)] for _ in range(NONBRDNUM)]
        # 由周期计算得到的欧米伽
        self.omiga = [0.0 for _ in range(PERIODNUM)]
        # 用于存储非广播参数周期表的数组
        self.perdTable = [[0.0 for _ in range(PERIODNUM * 2 - 1)] for _ in range(NONBRDNUM)]
        # 计算日的非广播BDGIM参数
        self.nonBrdCoef = [[0.0 for _ in range(MAXGROUP)] for _ in range(NONBRDNUM)]

# Broadcast Ionospheric Parameters Struct
class BrdIonData:
    def __init__(self):
        self.brdIonCoef = [0.0 for _ in range(BRDPARANUM)]  # The body array for storing the bdgim broadcast parameter
        self.degOrd = [[0 for _ in range(2)] for _ in range(BRDPARANUM)]  # Spheric harmonic function degree and order index for broadcast parameter

class MjdData:
    def __init__(self):
        self.mjd = 0.0
        self.daysec = 0.0
# BDGIM非广播系数周期表
NonBrdPara_table = [
    [-0.610000,-0.510000, 0.230000,-0.060000, 0.020000, 0.010000, 0.000000,-0.010000,-0.000000, 0.000000, 0.010000,-0.190000,-0.090000,-0.180000, 0.150000, 1.090000, 0.500000,-0.340000, 0.000000,-0.130000, 0.050000,-0.060000, 0.030000,-0.030000, 0.040000],
    [-1.310000,-0.430000,-0.200000,-0.050000,-0.080000,-0.030000,-0.020000, 0.000000,-0.020000, 0.000000, 0.000000,-0.020000, 0.070000, 0.060000,-0.310000,-0.140000,-0.080000,-0.090000,-0.110000, 0.070000, 0.030000, 0.130000,-0.020000, 0.080000,-0.020000],
    [-2.000000, 0.340000,-0.310000, 0.060000,-0.060000, 0.010000,-0.030000, 0.010000, 0.010000, 0.030000, 0.000000, 0.120000, 0.030000,-0.550000, 0.130000,-0.210000,-0.380000,-1.220000,-0.220000,-0.370000, 0.070000,-0.070000, 0.040000,-0.010000,-0.040000],
    [-0.030000,-0.010000, 0.160000, 0.170000,-0.110000,-0.010000,-0.050000,-0.000000, 0.000000, 0.010000, 0.010000,-0.100000, 0.060000,-0.020000, 0.050000, 0.520000, 0.360000, 0.050000, 0.010000, 0.050000, 0.020000, 0.030000,-0.010000, 0.040000,-0.000000],
    [ 0.150000, 0.170000,-0.030000, 0.150000, 0.150000, 0.050000,-0.010000, 0.010000,-0.010000, 0.020000,-0.000000, 0.060000, 0.090000, 0.090000,-0.090000, 0.270000, 0.140000, 0.150000, 0.020000, 0.060000,-0.010000, 0.020000,-0.030000, 0.010000,-0.010000],
    [-0.480000, 0.020000, 0.020000, 0.000000,-0.140000,-0.030000,-0.070000,-0.000000, 0.010000, 0.010000, 0.000000, 0.000000, 0.010000,-0.080000,-0.030000,-0.000000, 0.040000,-0.290000,-0.030000,-0.110000, 0.030000,-0.050000, 0.020000,-0.020000, 0.000000],
    [-0.400000,-0.060000, 0.040000, 0.110000, 0.010000, 0.050000,-0.030000,-0.010000,-0.000000, 0.000000, 0.000000,-0.020000, 0.020000, 0.000000, 0.060000, 0.110000, 0.000000,-0.170000,-0.010000,-0.070000, 0.020000,-0.050000, 0.010000,-0.020000, 0.010000],
    [ 2.280000, 0.300000, 0.180000,-0.050000, 0.010000,-0.030000,-0.010000,-0.010000,-0.020000,-0.020000,-0.000000,-0.080000, 0.000000, 0.860000,-0.360000, 0.170000, 0.250000, 1.580000, 0.490000, 0.460000,-0.040000, 0.010000, 0.040000,-0.040000, 0.070000],
    [-0.160000, 0.440000, 0.340000,-0.160000, 0.040000,-0.010000, 0.020000, 0.000000, 0.000000, 0.000000, 0.000000,-0.020000,-0.040000,-0.180000, 0.080000, 0.230000, 0.170000,-0.060000,-0.030000,-0.000000,-0.010000, 0.000000, 0.000000, 0.000000, 0.000000],
    [-0.210000,-0.280000, 0.450000, 0.020000,-0.140000,-0.000000,-0.010000, 0.000000, 0.000000, 0.000000, 0.000000,-0.070000,-0.020000,-0.050000, 0.050000, 0.350000, 0.270000,-0.150000,-0.020000,-0.040000,-0.010000, 0.000000, 0.000000, 0.000000, 0.000000],
    [-0.100000,-0.310000, 0.190000, 0.110000,-0.050000,-0.080000, 0.030000, 0.000000, 0.000000, 0.000000, 0.000000, 0.010000,-0.010000,-0.070000, 0.060000,-0.050000,-0.030000, 0.000000, 0.010000, 0.010000, 0.020000, 0.000000, 0.000000, 0.000000, 0.000000],
    [-0.130000,-0.170000,-0.250000, 0.040000, 0.080000,-0.040000,-0.100000, 0.000000, 0.000000, 0.000000, 0.000000, 0.030000, 0.010000, 0.040000,-0.020000, 0.020000,-0.030000, 0.130000, 0.020000, 0.070000, 0.030000, 0.000000, 0.000000, 0.000000, 0.000000],
    [0.210000, 0.040000,-0.120000, 0.120000, 0.080000,-0.000000, 0.010000, 0.000000, 0.000000, 0.000000, 0.000000, 0.150000,-0.100000, 0.140000,-0.050000,-0.600000,-0.320000, 0.280000, 0.040000, 0.090000, 0.020000, 0.000000, 0.000000, 0.000000, 0.000000],
    [0.680000, 0.390000, 0.180000, 0.070000,-0.010000,-0.020000, 0.050000, 0.000000, 0.000000, 0.000000, 0.000000, 0.060000, 0.000000,-0.030000, 0.060000, 0.020000,-0.100000,-0.080000,-0.040000,-0.050000,-0.040000, 0.000000, 0.000000, 0.000000, 0.000000],
    [1.060000,-0.120000, 0.400000, 0.020000, 0.010000,-0.030000,-0.010000, 0.000000, 0.000000, 0.000000, 0.000000,-0.050000,-0.010000, 0.370000,-0.200000, 0.010000, 0.200000, 0.620000, 0.160000, 0.150000,-0.040000, 0.000000, 0.000000, 0.000000, 0.000000],
    [0.000000, 0.120000,-0.090000,-0.140000, 0.110000, 0.000000, 0.040000, 0.000000, 0.000000, 0.000000, 0.000000,-0.030000, 0.020000,-0.110000, 0.040000, 0.270000, 0.100000,-0.010000,-0.020000,-0.010000,-0.010000, 0.000000, 0.000000, 0.000000, 0.000000],
    [-0.120000,-0.000000, 0.210000,-0.140000,-0.120000,-0.030000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,-0.100000, 0.050000,-0.120000, 0.070000, 0.320000, 0.300000,-0.040000,-0.010000, 0.010000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]]
# BDGIM非广播系数的度/阶表 [ 3/0 3/1 3/-1 3/2 ... 5/2 5/-2 ]
NonBrdPara_degord_table = [
    [3, 0],
    [3, 1],
    [3, -1],
    [3, 2],
    [3, -2],
    [3, 3],
    [3, -3],
    [4, 0],
    [4, 1],
    [4, -1],
    [4, 2],
    [4, -2],
    [5, 0],
    [5, 1],
    [5, -1],
    [5, 2],
    [5, -2]
]
# BDGIM广播系数的度/阶表
BrdPara_degord_table = [
    [0, 0],
    [1, 0],
    [1, 1],
    [1, -1],
    [2, 0],
    [2, 1],
    [2, -1],
    [2, 2],
    [2, -2]
]


def EFLSFL(mjd, lat, lon, geomag, sunframe):
    """
    将地心的纬度/经度转换为地磁或/和太阳固定的纬度/经度

    参数：
        mjd: 计算时刻 [修正儒略日]
        lat: 输入纬度（单位：弧度）
        lon: 输入经度（单位：弧度）
        geomag: 转换为地磁框架（1：是，0：否）
        sunframe: 转换为太阳固定框架（1：是，0：否）

    返回值：
        lat1: 输出纬度（单位：弧度）
        lon1: 输出经度（单位：弧度）
    """
    Bp = LAT_POLE
    Lp = LON_POLE
    sinlon1 = 0.0
    coslon1 = 0.0

    if geomag:
        lat1 = math.asin(math.sin(Bp * math.pi / 180) * math.sin(lat) + math.cos(Bp * math.pi / 180) * math.cos(lat) * math.cos(lon - Lp * math.pi / 180))
        sinlon1 = (math.cos(lat) * math.sin(lon - Lp * math.pi / 180)) / math.cos(lat1)
        coslon1 = -(math.sin(lat) - math.sin(Bp * math.pi / 180) * math.sin(lat1)) / (math.cos(Bp * math.pi / 180) * math.cos(lat1))
        lon1 = math.atan2(sinlon1, coslon1)
    else:
        lat1 = lat
        lon1 = lon

    if sunframe:
        SUNLON = math.pi * (1.0 - 2.0 * (mjd - int(mjd)))
        sinlon2 = math.sin(SUNLON - Lp * math.pi / 180)
        coslon2 = math.sin(Bp * math.pi / 180) * math.cos(SUNLON - Lp * math.pi / 180)
        SUNLON = math.atan2(sinlon2, coslon2)
        lon1 = lon1 - SUNLON
        lon1 = math.atan2(math.sin(lon1), math.cos(lon1))

    return lat1, lon1

def IonMapping(type, ipp_elev, sat_elev, Hion):
    """
    计算电离层映射函数值

    参数：
        type: 映射函数类型（0：默认，1：SLM，2：MSLM，3：Klobuchar）
        ipp_elev: IPP的海拔高度 [弧度]
        sat_elev: 卫星仰角 [弧度]
        Hion: 电离层单层高度 [米]

    返回值：
        IMF: 电离层映射函数值
    """
    RE = 6378000.0  # 地球平均半径 [单位：米]

    if Hion < 10:
        Hion = 400000

    if type == 0:
        IMF = 1.0
    elif type == 1:
        # SLM 映射函数
        IMF = 1 / math.sin(ipp_elev)
    elif type == 2:
        # CODE (Schaer) 的 MSLM 映射函数
        IMF = 1 / math.sqrt(1 - (RE * math.sin(0.9782 * (math.pi / 2 - sat_elev)) / (RE + Hion)) ** 2)
    elif type == 3:
        # Klobuchar 映射函数
        IMF = 1 + 16 * ((0.53 - sat_elev / math.pi) ** 3)
    else:
        print("找不到这种类型的映射模型！模型类型为：", type)
        raise ValueError("找不到这种类型的映射模型！")

    return IMF


def Distance(xyz1, xyz2):
    """
    计算两点之间的距离

    参数：
        xyz1: 第一个点的坐标（数组）
        xyz2: 第二个点的坐标（数组）

    返回值：
        两点之间的距离
    """
    return math.sqrt((xyz1[0] - xyz2[0]) ** 2 + (xyz1[1] - xyz2[1]) ** 2 + (xyz1[2] - xyz2[2]) ** 2)


def IPPBLH1(sta, sat, Hion):
    """
    计算 IPP（电离层穿透点）的 XYZ 坐标、纬度、经度和海拔高度

    参数：
        sta: 地面站的 XYZ 坐标（单位：米）
        sat: 卫星的 XYZ 坐标（单位：米）
        Hion: 电离层单层高度（单位：米）

    返回值：
        IPPXYZ: IPP 的 XYZ 坐标（单位：米）
        IPP_B: IPP 的纬度（单位：弧度）
        IPP_L: IPP 的经度（单位：弧度）
        IPP_E: IPP 的海拔高度（单位：弧度）
        sat_ele: 卫星与地面站的仰角（单位：弧度）
    """
    dot = sum(x * x for x in sta)
    if dot < 10e-6:
        return 0
    dot = sum(x * x for x in sat)
    if dot < 10e-6:
        return 0

    DS = Distance(sta, sat)
    R1 = math.sqrt(sta[0] ** 2 + sta[1] ** 2 + sta[2] ** 2)
    R2 = EARTH_RADIUS + Hion
    R3 = math.sqrt(sat[0] ** 2 + sat[1] ** 2 + sat[2] ** 2)
    cos_value = (R1 * R1 + DS * DS - R3 * R3) / (2 * R1 * DS)
    # 确保cos_value在-1到1之间
    cos_value = max(-1, min(1, cos_value))
    zenith = math.pi - math.acos(cos_value)
    sat_ele = math.pi / 2 - zenith

    zenith1 = math.asin(R1 / R2 * math.sin(zenith))
    alpha = zenith - zenith1
    sta_ipp = math.sqrt(R1 * R1 + R2 * R2 - 2 * R1 * R2 * math.cos(alpha))

    IPPXYZ = [
        sta[0] + sta_ipp * (sat[0] - sta[0]) / DS,
        sta[1] + sta_ipp * (sat[1] - sta[1]) / DS,
        sta[2] + sta_ipp * (sat[2] - sta[2]) / DS
    ]

    IPP_L = math.atan2(IPPXYZ[1], IPPXYZ[0])
    IPP_B = math.atan(IPPXYZ[2] / math.sqrt(IPPXYZ[1] ** 2 + IPPXYZ[0] ** 2))
    IPP_E = math.pi / 2.0 - zenith1

    return IPPXYZ, IPP_B, IPP_L, IPP_E, sat_ele


def IPPBLH2(lat_u, lon_u, hion, sat_ele, sat_azimuth):
    """
    根据用户的经纬度和卫星的高度角、方位角，计算近似的IPP（电离层穿透点）的纬度、经度和海拔高度

    参数：
        lat_u: 用户的纬度（单位：弧度）
        lon_u: 用户的经度（单位：弧度）
        hion: 电离层单层高度（单位：米）
        sat_ele: 卫星的高度角（单位：弧度）
        sat_azimuth: 卫星的方位角（单位：弧度）

    返回值：
        ipp_b: IPP的纬度（单位：弧度）
        ipp_l: IPP的经度（单位：弧度）
        ipp_e: IPP的海拔高度（单位：弧度）
    """
    phiu = math.pi / 2 - sat_ele - math.asin(EARTH_RADIUS * math.cos(sat_ele) / (EARTH_RADIUS + hion))
    ipp_b = math.asin(math.sin(lat_u) * math.cos(phiu) + math.cos(lat_u) * math.sin(phiu) * math.cos(sat_azimuth))

    temp1 = math.sin(phiu) * math.sin(sat_azimuth) / math.cos(ipp_b)
    temp2 = (math.cos(phiu) - math.sin(lat_u) * math.sin(ipp_b)) / (math.cos(lat_u) * math.cos(ipp_b))

    ipp_l = lon_u + math.atan2(temp1, temp2)
    ipp_e = math.asin(EARTH_RADIUS * math.cos(sat_ele) / (EARTH_RADIUS + hion))

    return ipp_b, ipp_l, ipp_e

def SetNonBrdCoefPeriod(nonBrdData):
    """
    设置BDGIM模型的非广播perdTable的周期项

    参数：
        nonBrdData: BDGIM非广播电离层参数

    返回值：
        无
    """
    year_day = 365.25  # 天
    solar_cycle = 4028.71  # 天
    Moon_Month = 27.0  # 天
    peridday = 0
    m = 0
    period_num = 0

    nonBrdData.omiga[period_num] = 0.0
    period_num += 1
    # 日周期
    nonBrdData.omiga[period_num] = 2 * math.pi
    period_num += 1
    nonBrdData.omiga[period_num] = 2 * math.pi / 0.5
    period_num += 1
    nonBrdData.omiga[period_num] = 2 * math.pi / 0.33
    period_num += 1
    # 半月周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 14.6
    period_num += 1
    # 月周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 27.0
    period_num += 1
    # 三分之一年周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 121.6
    period_num += 1
    # 半年周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 182.51
    period_num += 1
    # 年周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 365.25
    period_num += 1
    # 太阳周期
    nonBrdData.omiga[period_num] = 2 * math.pi / 4028.71
    period_num += 1
    nonBrdData.omiga[period_num] = 2 * math.pi / 2014.35
    period_num += 1
    nonBrdData.omiga[period_num] = 2 * math.pi / 1342.90
    period_num += 1
    nonBrdData.omiga[period_num] = 2 * math.pi / 1007.18

def CalNonBrdCoef(mjd, nonBrdData):
    global Init_mjd
    if mjd >= Init_mjd and (mjd - Init_mjd) < 1.0:
        return 1

    dmjd = 2.0 / 24.0
    igroup = 0

    for tmjd in np.arange(int(mjd), int(mjd) + 1, dmjd):
        for icoef in range(len(nonBrdData.perdTable)):
            coef = 0.0
            ipar = 0
            for n in range(len(nonBrdData.omiga)):
                if nonBrdData.omiga[n] == 0:
                    coef = nonBrdData.perdTable[icoef][ipar]
                    ipar += 1
                else:
                    coef += nonBrdData.perdTable[icoef][ipar] * math.cos(nonBrdData.omiga[n] * (tmjd + dmjd / 2.0))
                    ipar += 1
                    coef += nonBrdData.perdTable[icoef][ipar] * math.sin(nonBrdData.omiga[n] * (tmjd + dmjd / 2.0))
                    ipar += 1
            nonBrdData.nonBrdCoef[icoef][igroup] = coef
        igroup += 1

    Init_mjd = int(mjd)
    return 1

def BrdCoefGroupIndex(mjd, nonBrdData):
    global Init_mjd
    igroup = -1

    # 计算BDGIM模型的非广播参数
    if mjd < Init_mjd or mjd > Init_mjd + 1.0:
        CalNonBrdCoef(mjd, nonBrdData)

    # 设置sh系数组时间间隔
    dmjd = 2.0 / 24.0
    tmjd = float(int(Init_mjd))

    while tmjd < int(Init_mjd) + 1:
        if mjd >= tmjd and mjd < tmjd + dmjd:
            igroup += 1
            break
        else:
            igroup += 1
        tmjd += dmjd

    if igroup > 11:
        igroup = -1

    return igroup

def VtecBrdSH(nonBrdData, brdData, mjd, ipp_b, ipp_l):
    vtec_brd = 0.0
    vtec_A0 = 0.0
    vtec = 0.0

    # 获取BDGIM模型会话组
    igroup = BrdCoefGroupIndex(mjd, nonBrdData)

    if igroup == -1:
        return 0

    ipp_b1 = ipp_b
    ipp_l1 = ipp_l

    # 计算广播系数的VTEC
    for ipar in range(BRDPARANUM):
        if brdData.degOrd[ipar][1] > brdData.degOrd[ipar][0]:
            return 0
        vtec_brd += brdData.brdIonCoef[ipar] * ASLEFU(ipp_b1, ipp_l1, brdData.degOrd[ipar][0], brdData.degOrd[ipar][1])

    # 计算非广播系数的VTEC
    for ipar in range(NONBRDNUM):
        if nonBrdData.degOrd[ipar][1] > nonBrdData.degOrd[ipar][0]:
            return 0
        vtec_A0 += nonBrdData.nonBrdCoef[ipar][igroup] * ASLEFU(ipp_b1, ipp_l1, nonBrdData.degOrd[ipar][0], nonBrdData.degOrd[ipar][1])

    vtec = vtec_brd + vtec_A0

    if brdData.brdIonCoef[0] > 35.0:
        vtec = max(brdData.brdIonCoef[0] / 10.0, vtec)
    elif brdData.brdIonCoef[0] > 20.0:
        vtec = max(brdData.brdIonCoef[0] / 8.0, vtec)
    elif brdData.brdIonCoef[0] > 12.0:
        vtec = max(brdData.brdIonCoef[0] / 6.0, vtec)
    else:
        vtec = max(brdData.brdIonCoef[0] / 4.0, vtec)
    return vtec
def ASLEFU(XLAT, XLON, INN, IMM):
    """
    计算归一化勒让德多项式

    参数：
        XLAT：纬度（Latitude）
        XLON：经度（Longitude）
        INN：阶数（Degree）
        IMM：次数（Order）

    返回值：
        result：归一化勒让德多项式的计算结果
    """
    NN = abs(INN)
    MM = abs(IMM)
    XX = 0.0
    PMM = 1.0
    FACT = 1.0
    SOMX2 = 0.0
    COEF = 0.0
    PMMP1 = 0.0
    PLL = 0.0
    KDELTA = 0.0
    FACTN = 0.0
    result = 0.0

    # 计算关联的勒让德多项式
    if INN >= 0:
        XX = math.sin(XLAT)
    else:
        XX = math.cos(XLAT)

    if MM > 0:
        SOMX2 = math.sqrt((1.0 - XX) * (1.0 + XX))
        FACT = 1.0
        for II in range(1, MM + 1):
            PMM *= FACT * SOMX2
            FACT += 2.0

    if NN == MM:
        COEF = PMM
    else:
        PMMP1 = XX * (2 * MM + 1) * PMM
        if NN == MM + 1:
            COEF = PMMP1
        else:
            for LL in range(MM + 2, NN + 1):
                PLL = (XX * (2 * LL - 1) * PMMP1 - (LL + MM - 1) * PMM) / (LL - MM)
                PMM = PMMP1
                PMMP1 = PLL
            COEF = PLL

    # 计算归一化因子和（归一化）系数
    if MM == 0:
        KDELTA = 1.0
    else:
        KDELTA = 0.0

    FACTN = math.sqrt(2.0 * (2.0 * NN + 1.0) / (1.0 + KDELTA) * FAKULT(NN - MM) / FAKULT(NN + MM))

    if IMM >= 0:
        result = FACTN * COEF * math.cos(MM * XLON)
    else:
        result = FACTN * COEF * math.sin(MM * XLON)

    return result
def FAKULT(N):
    """
    计算N的阶乘

    参数：
        N：整数

    返回值：
        FAK：N的阶乘
    """
    FAK = 1.0
    if N <= 1:
        return FAK
    for I in range(2, N + 1):
        FAK *= I
    return FAK


def IonBdsBrdModel(nonBrdData, brdData, mjd, sta_xyz, sat_xyz, brdPara):
    """
    使用BDGIM电离层模型获取B1C频率下的斜电离层延迟

    参数：
        nonBrdData: BDGIM非广播电离层参数
        brdData: BDGIM广播电离层参数
        mjd: 当前时刻的修正儒略日
        sta_xyz: 站点的x、y、z坐标
        sat_xyz: 卫星的x、y、z坐标
        brdPara: 广播电离层参数（包括9个参数模型）

    返回值：
        ion_delay: B1C频率下的电离层延迟（单位：米）
    """
    ipp_xyz = [0.0, 0.0, 0.0]
    ipp_b, ipp_l, ipp_e = 0.0, 0.0, 0.0
    geomag_b, geomag_l = 0.0, 0.0
    sat_ele = 0.0
    vtec = 0.0

    # 设置基本参数：周期、度/序、角速度、非广播参数
    for num in range(NONBRDNUM):
        nonBrdData.degOrd[num][0] = NonBrdPara_degord_table[num][0]
        nonBrdData.degOrd[num][1] = NonBrdPara_degord_table[num][1]

        for j in range(TRISERINUM):
            nonBrdData.perdTable[num][j] = NonBrdPara_table[num][j]

    for i in range(BRDPARANUM):
        brdData.degOrd[i][0] = BrdPara_degord_table[i][0]
        brdData.degOrd[i][1] = BrdPara_degord_table[i][1]

        brdData.brdIonCoef[i] = brdPara[i]

    SetNonBrdCoefPeriod(nonBrdData)

    # 计算IPP信息
    IPPXYZ, ipp_b, ipp_l, ipp_e, sat_ele=IPPBLH1(sta_xyz, sat_xyz, Hion_bdgim)

    # 将地固坐标转换为太阳固定和地磁坐标
    geomag_b,geomag_l=EFLSFL(mjd, ipp_b, ipp_l, 1, 1)

    # 计算映射因子
    mf = IonMapping(2, ipp_e, sat_ele, Hion_bdgim)
    # 计算垂直电离层TEC
    vtec=VtecBrdSH(nonBrdData, brdData, mjd, geomag_b, geomag_l)
    # print(vtec)
    # 计算延迟转换系数
    K = 40.3e16 / (1.0 * pow(FREQ1_BDS, 2))

    # 计算B1C频率下的电离层延迟
    ion_delay = mf * K * vtec

    return ion_delay,vtec




def UTC2MJD(year, month, day, hour, minute, second):
    hourn = hour + minute / 60.0 + second / 3600.0

    if month <= 2:
        year -= 1
        month += 12

    m_julindate = int(365.25 * year) + int(30.6001 * (month + 1)) + day + hourn / 24.0 + 1720981.5

    mjd = m_julindate - 2400000.5
    daysec = hour * 3600.0 + minute * 60.0 + second

    if daysec == 86400.0:
        daysec = 0.0

    return mjd, daysec

import re


def parse_rinex(lines, target_time):
    brdPara = []
    svid_list = []
    time_points = [chr(i) for i in range(ord('a'), ord('x') + 1)]
    time_data = {tp: [] for tp in time_points}

    # 将时间转换为小时
    target_hour = target_time.hour

    # 找到对应的字母
    if 0 <= target_hour < 24:
        target_time_point = time_points[target_hour]
    else:
        raise ValueError("时间超出范围，应该在0-23小时之间。")

    for line in lines:
        if line.startswith("BDS1") or line.startswith("BDS2") or line.startswith("BDS3"):
            parts = re.split(r'\s+', line.strip())
            try:
                time_point = parts[4]
                params = [float(parts[1]), float(parts[2]), float(parts[3])]
                svid = parts[5]
                time_data[time_point].append((params, svid))
            except (ValueError, IndexError):
                continue

    # 如果目标时间段有数据，直接返回
    if time_data[target_time_point]:
        for params, svid in time_data[target_time_point]:
            brdPara.extend(params)
            svid_list.append(svid)
    else:
        # 寻找最近的时间段数据
        target_index = time_points.index(target_time_point)
        left_index = target_index - 1
        right_index = target_index + 1

        while left_index >= 0 or right_index < len(time_points):
            if left_index >= 0 and time_data[time_points[left_index]]:
                for params, svid in time_data[time_points[left_index]]:
                    brdPara.extend(params)
                    svid_list.append(svid)
                break

            if right_index < len(time_points) and time_data[time_points[right_index]]:
                for params, svid in time_data[time_points[right_index]]:
                    brdPara.extend(params)
                    svid_list.append(svid)
                break

            left_index -= 1
            right_index += 1

    return brdPara, svid_list
def main():
    # 定义非广播电离层参数
    nonBrdData = NonBrdIonData()
    # 定义广播电离层参数
    brdData = BrdIonData()

    # 定义时间参数
    year = 2024
    month = 3
    day = 2
    hour = 6
    minute = 0
    second = 0

    # 转换时间为MJD
    mjd = UTC2MJD(year, month, day, hour, minute, second)[0]
    import datacal
    import pymap3d as pm
    # 定义站点和卫星的坐标
    staxyz = pm.geodetic2ecef(39, 116, 0)
    sta_xyz = [staxyz[0], staxyz[1], staxyz[2]]
    upxyz=pm.geodetic2ecef(39, 116,20000)
    sat_xyz = [upxyz[0], upxyz[1], upxyz[2]]
    sat_xyz = [    16633.662763  ,22327.657972  , 1842.783519]  # c23 00:00
    sat_xyz = [13939.137148  , 9195.581927,  22341.441527]  # c46 06:00
    # 定义广播电离层参数
    brdPara = [31.38, -0.3750 , 11,
               10.87,-12.12, 1.25,
               0 ,1.5 , 1.375]
    obj_time=datetime.datetime(year, month, day, hour, minute, second)
    # 提取日期部分
    date=str(obj_time.date())
    # print(date)
    import os
    rinexfile = './static/Rinex/' + date + '.rx'
    if os.path.exists(rinexfile):
        with open(rinexfile, 'r') as f:
            nfile_lines = f.readlines()
            # print(nfile_lines)

            # 解析数据
            brdPara, svid_list = parse_rinex(nfile_lines, obj_time)
            print("brdPara:", brdPara)
            print("SVID list:", svid_list)
            f.close()

        # rinexdata=datacal.rinexcal3(nfile_lines, obj_time,15)

    else:
        datacal.rinexget(obj_time)
        if os.path.exists(rinexfile):
            with open(rinexfile, 'r') as f:
                nfile_lines = f.readlines()
                brdPara, svid_list = parse_rinex(nfile_lines, obj_time)
                f.close()
            # rinexdata = datacal.rinexcal3(nfile_lines, obj_time, tstep)
        else:
            rinexdata='false'

    # 调用IonBdsBrdModel函数计算电离层延迟
    ion_delay,vtec = IonBdsBrdModel(nonBrdData, brdData, mjd, sta_xyz, sat_xyz, brdPara)

    # 打印结果
    print("B1C频率下的电离层延迟：", ion_delay, "米")
    print('垂直电子含量：',vtec)

# 调用主函数
if __name__ == "__main__":
    main()