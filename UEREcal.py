import numpy as np
from numpy.linalg import norm, inv
# 计算星历方差

def uraindex(value):
    import numpy as np
    ura_eph = np.array([2.4, 3.4, 4.85, 6.85, 9.65, 13.65, 24.0, 48.0, 96.0, 192.0, 384.0, 768.0, 1536.0, 3072.0, 6144.0, 0.0])
    for i in range(15):
        if ura_eph[i] >= value:
            ind = i
            return ind

def var_uraeph(ura):
    STD_GAL_NAPA = 500.0
    ura_value = np.array([2.4, 3.4, 4.85, 6.85, 9.65, 13.65, 24.0, 48.0, 96.0, 192.0, 384.0, 768.0, 1536.0, 3072.0, 6144.0])
    ura = ura
    if ura < 0 or ura > 15:
        vars = 6144**2
    else:
        vars = ura_value[ura]**2
    return vars

def get_Vars(sva_data):
    sva = uraindex(sva_data)
    Vars = var_uraeph(int(sva))
    return Vars


# 计算TGD方差
def get_Vmea():
    ERR_CBIAS = 0.3
    Vmea = (ERR_CBIAS)**2
    return Vmea

#计算对流层和电离层方差
class gtime_t():
    """ class to define the time """

    def __init__(self, time=0, sec=0.0):
        self.time = time
        self.sec = sec

def epoch2time(ep):
    """ calculate time from epoch """
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    time = gtime_t()
    year = int(ep[0])
    mon = int(ep[1])
    day = int(ep[2])

    if year < 1970 or year > 2099 or mon < 1 or mon > 12:
        return time
    days = (year-1970)*365+(year-1969)//4+doy[mon-1]+day-2
    if year % 4 == 0 and mon >= 3:
        days += 1
    sec = int(ep[5])
    time.time = days*86400+int(ep[3])*3600+int(ep[4])*60+sec
    time.sec = ep[5]-sec
    return time

def time2gpst(t):
    """ convert to gps-time from time """
    gpst0 = [1980, 1, 6, 0, 0, 0]
    t0 = epoch2time(gpst0)
    sec = t.time-t0.time
    week = int(sec/(86400*7))
    tow = sec-week*86400*7+t.sec
    return week, tow

def ionmodel(t, pos, az, el, ion=None):
    """ klobuchar model of ionosphere delay estimation """
    ion_default = np.array([ # /* 2004/1/1 */
        0.1118E-07, -0.7451E-08, -0.5961E-07, 0.1192E-06,
        0.1167E+06, -0.2294E+06, -0.1311E+06, 0.1049E+07])

    if pos[2] < -1E3 or el <= 0:
        return 0.0

    ion = ion_default

    psi = 0.0137 / (el / np.pi + 0.11) - 0.022
    phi = pos[0] / np.pi + psi * np.cos(az)
    phi = np.max((-0.416, np.min((0.416, phi))))
    lam = pos[1]/np.pi + psi * np.sin(az) / np.cos(phi * np.pi)
    phi += 0.064 * np.cos((lam - 1.617) * np.pi)
    _, tow = time2gpst(t)
    tt = 43200.0 * lam + tow  # local time
    tt -= np.floor(tt / 86400) * 86400
    f = 1.0 + 16.0 * np.power(0.53 - el/np.pi, 3.0)  # slant factor

    h = [1, phi, phi**2, phi**3]
    amp = np.dot(h, ion[0:4])
    per = np.dot(h, ion[4:8])
    amp = max(amp, 0)
    per = max(per, 72000.0)
    x = 2.0 * np.pi * (tt - 50400.0) / per
    if np.abs(x) < 1.57:
        v = 5e-9 + amp * (1.0 + x * x * (-0.5 + x * x / 24.0))
    else:
        v = 5e-9
    diono = 299792458.0 * f * v
    return diono


def get_ion_trp_var(time, pos, az, el, ion_gps):
    ion = 1
    trop = 1
    if ion == 0:
        dion_var = 5**2
    elif ion == 1:
        dion = ionmodel(time, pos, az, el, ion_gps)
        dion_var = (0.5*dion)**2
    # tropospheric correction
    if trop == 0:
        dtrop_var = 3**2
    elif trop == 1:
        dtrop_var = (0.3/(np.sin(el) + 0.01))**2
    return dion_var, dtrop_var


# 计算多路径和噪声方差
def get_VARr(el):
    """ variation of measurement """
    s_el = np.sin(el)
    if s_el <= 0.0:
        return 0.0
    a = 0.3
    b = 0.3
    VARr = a**2 + (b / s_el)**2
    return VARr

def get_UERE(time, pos, az, el, ion_gps, sva_data):
    Vars = get_Vars(sva_data)
    VARr = get_VARr(el)
    dion_var, dtrop_var = get_ion_trp_var(time, pos, az, el, ion_gps)
    Vmea = get_Vmea()
    UERE = VARr + Vars + dion_var + dtrop_var + Vmea
    return np.sqrt(UERE)

