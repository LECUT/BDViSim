from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import datetime
from json import dump
import math as m
import numpy as np
import pymap3d as pm
import ionex
import os
import urllib.request
from wget import download
from gzip import GzipFile
def dops(az, el, elmin,P):
    """ calculate DOP from az/el """
    nm = az.shape[0]
    H = np.zeros((nm, 4))
    n = 0
    for i in range(nm):
        if el[i] < elmin:
            continue
        cel = m.cos(el[i])
        sel = m.sin(el[i])
        H[n, 0] = cel*m.sin(az[i])
        H[n, 1] = cel*m.cos(az[i])
        H[n, 2] = sel
        H[n, 3] = 1
        n += 1
    if n < 4:
        return None
    Qinv = np.linalg.inv(H.T @ P @ H)
    dop = np.diag(Qinv)
    hdop = dop[0]+dop[1]
    vdop = dop[2]
    pdop = hdop+vdop
    gdop = pdop+dop[3]
    dop = np.sqrt(np.array([gdop, pdop, hdop, vdop]))
    return dop
def dops_accuracy(az, el, elmin,P):
    """ calculate DOP from az/el """
    nm = az.shape[0]
    H = np.zeros((nm, 4))
    n = 0
    for i in range(nm):
        if el[i] < elmin:
            continue
        cel = m.cos(el[i])
        sel = m.sin(el[i])
        H[n, 0] = cel*m.sin(az[i])
        H[n, 1] = cel*m.cos(az[i])
        H[n, 2] = sel
        H[n, 3] = 1
        n += 1
    if n < 4:
        return None
    Qinv = np.linalg.inv(H.T @ P @ H)
    dop = np.diag(Qinv)
    hdop = dop[0]+dop[1]
    vdop = dop[2]
    pdop = hdop+vdop
    gdop = pdop+dop[3]
    dop = np.sqrt(np.array([gdop, pdop, hdop, vdop]))
    return dop
def sp3un_gz(file_name):
    f_name = file_name.replace(".gz", ".sp3")
    g_file = GzipFile(file_name)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()
def lagrange(x, w):
    M = len(x)
    p = 0.0
    for j in range(M):
        pt = w[j]
        for k in range(M):
            if k == j:
                continue
            fac = x[j] - x[k]
            pt *= np.poly1d([1.0, -x[k]]) / fac
        p += pt
    return p

def blh2xyz(blh):
    a = 6378137.0
    f = 1.0 / 298.257223563
    e = m.sqrt(2 * f - f * f);
    e2 = 0.00669437999013
    lat = blh[0]
    lon = blh[1]
    height = blh[2]
    slat = np.sin(lat)
    clat = np.cos(lat)
    slon = np.sin(lon)
    clon = np.cos(lon)
    t2lat = (np.tan(lat)) * (np.tan(lat))
    tmp = 1 - e * e
    tmpden = np.sqrt(1 + tmp * t2lat)
    tmp2 = np.sqrt(1 - e * e * slat * slat)
    N = a / tmp2
    x = (N + height) * clat * clon
    y = (N + height) * clat * slon
    z = (a * tmp * slat) / tmp2 + height * slat
    return [x, y, z]

def XYZ_to_LLA(X, Y, Z):
    a = 6378137.0
    b = 6356752.314245
    ea = np.sqrt((a ** 2 - b ** 2) / a ** 2)
    eb = np.sqrt((a ** 2 - b ** 2) / b ** 2)
    p = np.sqrt(X ** 2 + Y ** 2)
    theta = np.arctan2(Z * a, p * b)
    longitude = np.arctan2(Y, X)
    latitude = np.arctan2(Z + eb ** 2 * b * np.sin(theta) ** 3, p - ea ** 2 * a * np.cos(theta) ** 3)
    N = a / np.sqrt(1 - ea ** 2 * np.sin(latitude) ** 2)
    altitude = p / np.cos(latitude) - N
    return np.array([np.degrees(latitude), np.degrees(longitude), altitude])

def BDS_weekwisToNYR(week, seconds):
    diffrombegin = week * 604800 + seconds
    BDSbegintime = datetime.datetime(2006, 1, 1, 00, 00, 00, 00)
    result = BDSbegintime + datetime.timedelta(seconds=diffrombegin)
    return result

def date2doy(date):
    date_base = datetime.datetime(date.year,1,1)
    doy = (date - date_base).days + 1
    return doy

def BDS_NYRToweekwis(bdsNYR):
    bdsbeginUTC = datetime.datetime(2006, 1, 1, 00, 00, 00, 00)
    timespan = bdsNYR - bdsbeginUTC
    week = int(timespan.days / 7)
    bdsseconds = (timespan.days - week * 7) * 60 * 60 * 24 + timespan.seconds
    return week, bdsseconds

def calculate_gps_week(date):
    gps_epoch = datetime.datetime(1980, 1, 6)
    days_since_gps_epoch = (date.date() - gps_epoch.date()).days
    gps_week = days_since_gps_epoch // 7
    return gps_week

# YUMA
def yumacal(content, obj_time,chosen):
    rr = int((len(content) - 1) / 15)
    sat_data = {}
    sat_data['counts'] = {'nums':rr,}
    for i in range(rr):
        sat = {}
        for j in range(15):
            data_content = content[j + i * 15]
            if j == 1:
                sat["ID"] = data_content[28:30]
            if j == 2:
                sat["Health"] = data_content[28:31]
            if j == 3:
                sat["Eccentricity"] = float(data_content[27:])
            if j == 4:
                sat["Time_of_Applicability(s)"] = float(data_content[27:])
            if j == 5:
                sat["Orbital_Inclination(rad)"] = float(data_content[27:])
            if j == 6:
                sat["Rate_of_Right_Ascen(r/s)"] = float(data_content[27:])
            if j == 7:
                sat["SQRT(A)(m_1/2)"] = float(data_content[27:])
            if j == 8:
                sat["Right_Ascen_at_Week(rad)"] = float(data_content[27:])
            if j == 9:
                sat["Argument_of_Perigee(rad)"] = float(data_content[27:])
            if j == 10:
                sat["Mean_Anom(rad)"] = float(data_content[27:])
            if j == 11:
                sat["Af0(s)"] = float(data_content[27:])
            if j == 12:
                sat["Af1(s/s)"] = float(data_content[27:])
            if j == 13:
                sat["week"] = float(data_content[27:])
        sat_data["sat" + str(i)] = sat
    xx = 0
    xxx = 1
    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            sat_data["C" + str(i)] = {}

    def yumacal(year, month, day, hour, minute, second, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v,chosen):
        # 1t_k
        if chosen=='t':
            objtime = datetime.datetime(year, month, day, hour, minute, second)
            t_oc = BDS_NYRToweekwis(objtime)[1]
            t = t_oc - (c_gap + c_v * (t_oc - toe))
            if (BDS_NYRToweekwis(objtime)[0]-week)>0:
                t+=604800
            t_k = t - toe-14
        elif chosen=="c":
            objtime = datetime.datetime(year, month, day, hour, minute, second)
            t_oc = BDS_NYRToweekwis(objtime)[1]
            t = t_oc - (c_gap + c_v * (t_oc - toe))
            t_k = t - toe-14

            if t_k > 302400:
                t_k -= 604800
            elif t_k < -302400:
                t_k += 604800

        GM = 3.9860047e14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0
        M_k = M0 + n * t_k
        E = 0;
        E1 = 1;
        count = 0;
        while abs(E1 - E) > 1e-12:
            count = count + 1
            E1 = E;
            E = M_k + e * m.sin(E);
            if count > 1e8:
                print("Not convergent!")
                break

        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e));

        u_0 = V_k + w

        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E))
        if chosen=="c":
            i = I_0
        elif chosen=="t":
            if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
                i = I_0
            else:
                i=I_0+0.3*m.pi


        # 9
        x_k = r * m.cos(u_0)
        y_k = r * m.sin(u_0)
        # 10
        omega_e = 7.292115e-5
        OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * toe;
        # 11
        #old file
        if chosen=="c":
            if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
                OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * toe;
                X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
                Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
                Z_k1 = (y_k * m.sin(i))
                X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(-(5 * m.pi / 180)) + Z_k1 * m.sin(
                    omega_e * t_k) * m.sin(-(5 * m.pi / 180))
                Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
                    -(5 * m.pi / 180)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(-(5 * m.pi / 180))
                Z_k = -(Y_k1 * m.sin(-(5 * m.pi / 180))) + Z_k1 * m.cos(-(5 * m.pi / 180))

            else:
                X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
                Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
                Z_k = (y_k * m.sin(i))
        # new file
        elif chosen=="t":
            X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k = (y_k * m.sin(i))
        if (hour < 10):
            hour = "0" + str(hour)
        if (minute < 10):
            minute = "0" + str(minute)
        epoch = BDS_weekwisToNYR(week, t_oc).isoformat()
        timeid = str(year) + str(month) + str(day) + str(hour) + str(minute)
        sat_data[PRN][timeid] = {"PRN": PRN,
                                 "epoch": epoch,
                                 "n": n,
                                 "M_k": M_k,
                                 "E": E,
                                 "V_k": V_k,
                                 "u_0": u_0,
                                 "x_ky_k": '(' + str(x_k) + ',' + str(y_k) + ')',
                                 "OMEGA_k": OMEGA_k,
                                 "X_k": '%.12f' % X_k,
                                 "Y_k": '%.12f' % Y_k,
                                 "Z_k": '%.12f' % Z_k,

                                 }

    for i in range(rr):
        PRN = "C" + sat_data["sat" + str(i)]["ID"]
        sqrt_A = sat_data["sat" + str(i)]["SQRT(A)(m_1/2)"]
        M0 = sat_data["sat" + str(i)]["Mean_Anom(rad)"]
        e = sat_data["sat" + str(i)]["Eccentricity"]
        w = sat_data["sat" + str(i)]["Argument_of_Perigee(rad)"]
        I_0 = sat_data["sat" + str(i)]["Orbital_Inclination(rad)"]
        OMEGA_DOT = sat_data["sat" + str(i)]["Rate_of_Right_Ascen(r/s)"]
        OMEGA = sat_data["sat" + str(i)]["Right_Ascen_at_Week(rad)"]
        c_gap = sat_data["sat" + str(i)]["Af0(s)"]
        c_v = sat_data["sat" + str(i)]["Af1(s/s)"]
        week = sat_data["sat" + str(i)]["week"]
        health = sat_data["sat" + str(i)]["Health"]
        toe = sat_data["sat" + str(i)]["Time_of_Applicability(s)"]
        t1 = 0
        t = toe
        sat_data['out' + str(xx)] = {}
        xxx = 1
        for j in range(24):
            next_time = obj_time + datetime.timedelta(hours=j)
            next_time_str = next_time.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str = [int(z) for z in next_time_str]
            time_key = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map = dict(zip(time_key, next_time_str))
            year = time_map['year']
            month = time_map['month']
            day = time_map['day']
            hour = time_map['hour']
            minute = time_map['minute']
            second = time_map['second']
            yumacal(year, month, day, hour, minute, second, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v,chosen)
            xxx += 1
        xx += 1
        endtime = next_time.isoformat()

    with open('./static/json/satellite_info4.json', 'w') as f:
        dump(sat_data, f)
def yumacal2(content, obj_time,chosen,tstep):
    rr = int((len(content) - 1) / 15)
    sat_data = {}
    sat_data['counts'] = {'nums':rr,}
    for i in range(rr):
        sat = {}
        for j in range(15):
            data_content = content[j + i * 15]
            if j == 1:
                sat["ID"] = data_content[28:30]
            if j == 2:
                sat["Health"] = data_content[28:31]
            if j == 3:
                sat["Eccentricity"] = float(data_content[27:])
            if j == 4:
                sat["Time_of_Applicability(s)"] = float(data_content[27:])
            if j == 5:
                sat["Orbital_Inclination(rad)"] = float(data_content[27:])
            if j == 6:
                sat["Rate_of_Right_Ascen(r/s)"] = float(data_content[27:])
            if j == 7:
                sat["SQRT(A)(m_1/2)"] = float(data_content[27:])
            if j == 8:
                sat["Right_Ascen_at_Week(rad)"] = float(data_content[27:])
            if j == 9:
                sat["Argument_of_Perigee(rad)"] = float(data_content[27:])
            if j == 10:
                sat["Mean_Anom(rad)"] = float(data_content[27:])
            if j == 11:
                sat["Af0(s)"] = float(data_content[27:])
            if j == 12:
                sat["Af1(s/s)"] = float(data_content[27:])
            if j == 13:
                sat["week"] = float(data_content[27:])
        sat_data["sat" + str(i)] = sat
    xx = 0
    xxx = 1
    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            sat_data["C" + str(i)] = {}

    def yumacal(year, month, day, hour, minute, second, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v,chosen):
        # 1t_k
        if chosen=='t':
            objtime = datetime.datetime(year, month, day, hour, minute, second)
            t_oc = BDS_NYRToweekwis(objtime)[1]
            t = t_oc - (c_gap + c_v * (t_oc - toe))
            if (BDS_NYRToweekwis(objtime)[0]-week)>0:
                t+=604800
            t_k = t - toe-14
        elif chosen=="c":
            objtime = datetime.datetime(year, month, day, hour, minute, second)
            t_oc = BDS_NYRToweekwis(objtime)[1]
            t = t_oc - (c_gap + c_v * (t_oc - toe))
            t_k = t - toe-14

            if t_k > 302400:
                t_k -= 604800
            elif t_k < -302400:
                t_k += 604800

        GM = 3.9860047e14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0
        M_k = M0 + n * t_k
        E = 0;
        E1 = 1;
        count = 0;
        while abs(E1 - E) > 1e-12:
            count = count + 1
            E1 = E;
            E = M_k + e * m.sin(E);
            if count > 1e8:
                print("Not convergent!")
                break

        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e));

        u_0 = V_k + w

        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E))
        if chosen=="c":
            i = I_0
        elif chosen=="t":
            if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
                i = I_0
            else:
                i=I_0+0.3*m.pi


        # 9
        x_k = r * m.cos(u_0)
        y_k = r * m.sin(u_0)
        # 10
        omega_e = 7.292115e-5
        OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * toe;
        # 11
        if chosen=="c":
            if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
                OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * toe;
                X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
                Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
                Z_k1 = (y_k * m.sin(i))
                X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(-(5 * m.pi / 180)) + Z_k1 * m.sin(
                    omega_e * t_k) * m.sin(-(5 * m.pi / 180))
                Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
                    -(5 * m.pi / 180)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(-(5 * m.pi / 180))
                Z_k = -(Y_k1 * m.sin(-(5 * m.pi / 180))) + Z_k1 * m.cos(-(5 * m.pi / 180))

            else:
                X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
                Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
                Z_k = (y_k * m.sin(i))
        elif chosen=="t":
            X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k = (y_k * m.sin(i))
        if (hour < 10):
            hour = "0" + str(hour)
        if (minute < 10):
            minute = "0" + str(minute)
        epoch = BDS_weekwisToNYR(week, t_oc).isoformat()
        # print(epoch)
        timeid = str(year) + str(month) + str(day) + str(hour) + str(minute)
        sat_data[PRN][timeid] = {"PRN": PRN,
                                 "epoch": epoch,
                                 "n": n,
                                 "M_k": M_k,
                                 "E": E,
                                 "V_k": V_k,
                                 "u_0": u_0,
                                 "x_ky_k": '(' + str(x_k) + ',' + str(y_k) + ')',
                                 "OMEGA_k": OMEGA_k,
                                 "X_k": '%.12f' % X_k,
                                 "Y_k": '%.12f' % Y_k,
                                 "Z_k": '%.12f' % Z_k,

                                 }
    for i in range(rr):
        PRN = "C" + sat_data["sat" + str(i)]["ID"]
        sqrt_A = sat_data["sat" + str(i)]["SQRT(A)(m_1/2)"]
        M0 = sat_data["sat" + str(i)]["Mean_Anom(rad)"]
        e = sat_data["sat" + str(i)]["Eccentricity"]
        w = sat_data["sat" + str(i)]["Argument_of_Perigee(rad)"]
        I_0 = sat_data["sat" + str(i)]["Orbital_Inclination(rad)"]
        OMEGA_DOT = sat_data["sat" + str(i)]["Rate_of_Right_Ascen(r/s)"]
        OMEGA = sat_data["sat" + str(i)]["Right_Ascen_at_Week(rad)"]
        c_gap = sat_data["sat" + str(i)]["Af0(s)"]
        c_v = sat_data["sat" + str(i)]["Af1(s/s)"]
        week = sat_data["sat" + str(i)]["week"]
        health = sat_data["sat" + str(i)]["Health"]
        toe = sat_data["sat" + str(i)]["Time_of_Applicability(s)"]
        t1 = 0
        t = toe
        sat_data['out' + str(xx)] = {}
        xxx = 1
        for j in range(24):
            next_time = obj_time + datetime.timedelta(hours=j)
            for st in range(int(60 / tstep)):
                next_time_str = next_time.strftime('%Y %m %d %H %M %S').split(' ')
                next_time_str = [int(z) for z in next_time_str]
                time_key = ['year', 'month', 'day', 'hour', 'minute', 'second']
                time_map = dict(zip(time_key, next_time_str))
                year = time_map['year']
                month = time_map['month']
                day = time_map['day']
                hour = time_map['hour']
                minute = time_map['minute']
                second = time_map['second']
                yumacal(year, month, day, hour, minute, second, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v,chosen)
                xxx += 1
                next_time = next_time + datetime.timedelta(minutes=tstep)
        xx += 1
        endtime = next_time.isoformat()
    return sat_data

def rinexcal(nfile_lines,obj_time):
    satellite_info2 = {}

    def start_num():
        for i in range(len(nfile_lines)):
            if nfile_lines[i].find('END OF HEADER') != -1:
                start_num = i + 1
        return start_num

    print('start line' + str(start_num()))
    n_dic_list = []
    n_data_lines_nums = int((len(nfile_lines) - start_num()) / 8)

    for j in range(n_data_lines_nums):
        n_dic = {}
        for i in range(8):
            data_content = nfile_lines[start_num() + 8 * j + i]
            n_dic['数据组数'] = j + 1
            if i == 0:
                n_dic['卫星PRN号'] = str(data_content.strip('\n')[0:3].strip(' '))
                n_dic['历元'] = data_content.strip('\n')[3:23]
                n_dic['卫星钟偏差(s)'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(
                        ' '))  # 利用字符串切片功能来进行字符串的修改
                n_dic['卫星钟漂移(s/s)'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['卫星钟漂移速度(s/s*s)'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 1:
                n_dic['IODE'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rs'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['n'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['M0'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 2:
                n_dic['C_uc'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['e'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['C_us'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['sqrt_A'] = float(
                    (data_content.strip('\n')[62:80][0:-4] + 'e' + data_content.strip('\n')[62:80][-3:]).strip(' '))
            if i == 3:
                n_dic['TEO'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_ic'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['OMEGA'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['C_is'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 4:
                n_dic['I_0'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rc'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['w'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['OMEGA_DOT'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 5:
                n_dic['IDOT'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['L2_code'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['PS_week_num'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['L2_P_code'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 6:
                n_dic['卫星精度(m)'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['卫星健康状态'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['TGD1'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['TGD2'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 7:
                n_dic['信号发射时刻'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['IODC'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
        if n_dic['卫星PRN号'].startswith('C') == False:
            continue
        n_dic_list.append(n_dic)

    outlist = []
    zz = 0

    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info2["C" + str(i)] = {}

    def CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                    sqrt_A,
                    TOE, C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1):
        # 1
        GM = 3.986004418e+14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0 + δn

        # 2
        UT = hour + (minute / 60.0) + (second / 3600);
        if year >= 80:
            if year == 80 and month == 1 and day < 6:
                year = year + 2000
            else:
                year = year + 1900
        else:
            year = year + 2000
        if month <= 2:
            year = year - 1
            month = month + 12
        JD = (365.25 * year) + int(30.6001 * (month + 1)) + day + UT / 24 + 1720981.5;
        WN = int((JD - 2444244.5) / 7);
        t_oc = (JD - 2444244.5 - 7.0 * WN) * 24 * 3600.0 - 14;
        if t1 is None:
            t_k = 0
        else:
            δt = a_0 + a_1 * (t1 - TOE) + a_2 * (t1 - TOE) * (t1 - TOE)
            t = t1 - δt
            t_k = t - TOE-14

        # 3
        M_k = M0 + n * t_k

        # 4
        E = 0;
        E1 = 1;
        count = 0;
        while abs(E1 - E) > 1e-12:
            count = count + 1
            E1 = E;
            E = M_k + e * m.sin(E);
            if count > 1e8:
                print("Not convergent!")
                break

        # 5
        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e))

        # 6
        u_0 = V_k + w

        # 7
        δu = C_uc * m.cos(2 * u_0) + C_us * m.sin(2 * u_0)
        δr = C_rc * m.cos(2 * u_0) + C_rs * m.sin(2 * u_0)
        δi = C_ic * m.cos(2 * u_0) + C_is * m.sin(2 * u_0)

        # 8
        u = u_0 + δu
        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E)) + δr
        i = I_0 + δi + IDOT * (t_k);

        # 9
        x_k = r * m.cos(u)
        y_k = r * m.sin(u)
        omega_e = 7.2921150e-5
        if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
            # 10
            OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * TOE;

            # 11
            X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k1 = (y_k * m.sin(i))
            X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(-(5 * m.pi / 180)) + Z_k1 * m.sin(
                omega_e * t_k) * m.sin(-(5 * m.pi / 180))
            Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
                -(5 * m.pi / 180)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(-(5 * m.pi / 180))
            Z_k = -(Y_k1 * m.sin(-(5 * m.pi / 180))) + Z_k1 * m.cos(-(5 * m.pi / 180))

        else:

            OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * TOE;

            # 11
            X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k = (y_k * m.sin(i))


        if month > 12:
            year = year + 1
            month = month - 12

        if hour < 10:
            hour = '0' + str(hour)
        if minute < 10:
            minute = '0' + str(minute)
        if second < 10:
            second = '0' + str(second)
        # if month < 10:
        #     month = '0' + str(month)
        name = str(year) + str(month) + str(day) + str(hour) + str(minute)
        satellite_info2['ymd'] = str(year) + str(month) + str(day)
        epochtime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        # print(epochtime.isoformat())
        satellite_info2[PRN][name] = {"PRN": PRN,
                                      "epoch": epochtime.isoformat(),
                                      # "n": n,
                                      # "t_k": t_k,
                                      # "M_k": M_k,
                                      # "E": E,
                                      # "V_k": V_k,
                                      # "u_0": u_0,
                                      # "SDGZX": '(' + str(δu) + ',' + str(δr) + ',' + str(δi) + ')',
                                      # "SG": '(' + str(u) + ',' + str(r) + ',' + str(i) + ')',
                                      # "x_ky_k": '(' + str(x_k) + ',' + str(y_k) + ')',
                                      # "OMEGA_k": OMEGA_k,
                                      "X_k": '%.12f' % X_k,
                                      "Y_k": '%.12f' % Y_k,
                                      "Z_k": '%.12f' % Z_k,
                                      }


    for row in n_dic_list:
        PRN = str(row["卫星PRN号"])
        TIME = row["历元"]
        year = int(TIME.strip('\n')[3:5])
        month = int(TIME.strip('\n')[6:8])
        day = int(TIME.strip('\n')[8:12])
        hour = int(TIME.strip('\n')[12:15])
        minute = int(TIME.strip('\n')[16:18])
        second = float(TIME.strip('\n')[18:20])
        a_0 = float(row["卫星钟偏差(s)"])
        a_1 = float(row["卫星钟漂移(s/s)"])
        a_2 = float(row["卫星钟漂移速度(s/s*s)"])
        IODE = float(row["IODE"])
        C_rs = float(row["C_rs"])
        δn = float(row["n"])
        M0 = float(row["M0"])
        C_uc = float(row["C_uc"])
        e = float(row["e"])
        C_us = float(row["C_us"])
        sqrt_A = float(row["sqrt_A"])
        TOE = float(row["TEO"])
        C_ic = float(row["C_ic"])
        OMEGA = float(row["OMEGA"])
        C_is = float(row["C_is"])
        I_0 = float(row["I_0"])
        C_rc = float(row["C_rc"])
        w = float(row["w"])
        OMEGA_DOT = float(row["OMEGA_DOT"])
        IDOT = float(row["IDOT"])
        L2_code = float(row["L2_code"])
        PS_week_num = float(row["PS_week_num"])
        L2_P_code = float(row["L2_P_code"])
        wxjd = float(row["卫星精度(m)"])
        wxjkzt = float(row["卫星健康状态"])
        TGD1 = float(row["TGD1"])
        TGD2 = float(row["TGD2"])
        transT = float(row["信号发射时刻"])
        IODC = float(row["IODC"])
        t1 = TOE
        epochtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, int(second))
        satellite_info2['in' + str(zz)] = {"PRN": PRN,
                                           "epoch": epochtime.isoformat(),
                                           "a_0": a_0,
                                           "a_1": a_1,
                                           "a_2": a_2,
                                           "IODE": IODE,
                                           "C_rs": C_rs,
                                           "sn": δn,
                                           "M0": M0,
                                           "C_uc": C_uc,
                                           "e": e,
                                           "C_us": C_us,
                                           "sqrt_A": sqrt_A,
                                           "TOE": TOE,
                                           "C_ic": C_ic,
                                           "OMEGA": OMEGA,
                                           "C_is": C_is,
                                           "I_0": I_0,
                                           "C_rc": C_rc,
                                           "w": w,

                                           "OMEGA_DOT": OMEGA_DOT,
                                           "IDOT": IDOT,
                                           "L2_code": L2_code,
                                           "PS_week_num": PS_week_num,
                                           "L2_P_code": L2_P_code,
                                           "wxjd": wxjd,
                                           "wxjkzt": wxjkzt,
                                           "TGD1": TGD1,
                                           "TGD2": TGD2,

                                           "transmission_time": transT,
                                           "IODC": IODC

                                           }
        CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                    sqrt_A, TOE,
                    C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1)
        zz = zz + 1
        satellite_info2['num'] = zz
        endtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, 00)
        satellite_info2['objtime'] = obj_time.isoformat()
        satellite_info2['endtime'] = endtime.isoformat()


    with open('./static/json/satellite_info2.json', 'w') as f:
        dump(satellite_info2, f)

def rinexcal2(nfile_lines,obj_time,tstep):
    satellite_info2 = {}
    def start_num():
        for i in range(len(nfile_lines)):
            if nfile_lines[i].find('END OF HEADER') != -1:
                start_num = i + 1
        return start_num

    print('start line' + str(start_num()))

    n_dic_list = []
    n_data_lines_nums = int((len(nfile_lines) - start_num()) / 8)
    for i in range(63):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info2["C" + str(i)] = {}

    def CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                    sqrt_A,
                    TOE, C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1,sv_accu):
        # 1
        GM = 3.986004418e+14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0 + δn

        # 2
        if t1 is None:
            t_k = 0
        else:
            δt = a_0 + a_1 * (t1 - TOE) + a_2 * (t1 - TOE) * (t1 - TOE)
            t = t1 - δt
            t_k = t - TOE-14

        # 3
        M_k = M0 + n * t_k

        # 4
        E = 0;
        E1 = 1;
        count = 0;
        while abs(E1 - E) > 1e-12:
            count = count + 1
            E1 = E;
            E = M_k + e * m.sin(E);
            if count > 1e8:
                print("计算偏近点角时未收敛！")
                break

        # 5
        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e))

        # 6
        u_0 = V_k + w

        # 7
        δu = C_uc * m.cos(2 * u_0) + C_us * m.sin(2 * u_0)
        δr = C_rc * m.cos(2 * u_0) + C_rs * m.sin(2 * u_0)
        δi = C_ic * m.cos(2 * u_0) + C_is * m.sin(2 * u_0)

        # 8
        u = u_0 + δu
        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E)) + δr
        i = I_0 + δi + IDOT * (t_k);

        # 9
        x_k = r * m.cos(u)
        y_k = r * m.sin(u)
        omega_e = 7.2921150e-5
        if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
            # 10
            OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * TOE;

            # 11
            X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k1 = (y_k * m.sin(i))
            X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(-(5 * m.pi / 180)) + Z_k1 * m.sin(
                omega_e * t_k) * m.sin(-(5 * m.pi / 180))
            Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
                -(5 * m.pi / 180)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(-(5 * m.pi / 180))
            Z_k = -(Y_k1 * m.sin(-(5 * m.pi / 180))) + Z_k1 * m.cos(-(5 * m.pi / 180))

        else:
            # 10
            OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * TOE;

            # 11
            X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k = (y_k * m.sin(i))

        minute=int(minute+(t1-TOE)/60)
        if hour < 10:
            hour = '0' + str(hour)
        if minute < 10:
            minute = '0' + str(minute)
        if second < 10:
            second = '0' + str(second)
        # if month < 10:
        #     month = '0' + str(month)
        name = '20'+str(year) + str(month) + str(day) + str(hour) + str(minute)
        satellite_info2['ymd'] = str(year) + str(month) + str(day)
        epochtime = datetime.datetime(int(2000+year), int(month), int(day), int(hour), int(minute))
        # print(epochtime.isoformat())
        satellite_info2[PRN][name] = {
                                      "X_k": '%.12f' % X_k,
                                      "Y_k": '%.12f' % Y_k,
                                      "Z_k": '%.12f' % Z_k,
                                      "sv_accu": sv_accu,
                                      "time":epochtime
                                      }
    for j in range(n_data_lines_nums):
        n_dic = {}
        for i in range(8):
            data_content = nfile_lines[start_num() + 8 * j + i]
            n_dic['数据组数'] = j + 1
            if i == 0:
                n_dic['卫星PRN号'] = str(data_content.strip('\n')[0:3].strip(' '))
                n_dic['历元'] = data_content.strip('\n')[3:23]
                n_dic['卫星钟偏差(s)'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(
                        ' '))
                n_dic['卫星钟漂移(s/s)'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['卫星钟漂移速度(s/s*s)'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 1:
                n_dic['IODE'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rs'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['n'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['M0'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 2:
                n_dic['C_uc'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['e'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['C_us'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['sqrt_A'] = float(
                    (data_content.strip('\n')[62:80][0:-4] + 'e' + data_content.strip('\n')[62:80][-3:]).strip(' '))
            if i == 3:
                n_dic['TEO'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_ic'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['OMEGA'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['C_is'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 4:
                n_dic['I_0'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rc'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['w'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['OMEGA_DOT'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 5:
                n_dic['IDOT'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['L2_code'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['PS_week_num'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['L2_P_code'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 6:
                n_dic['sv_accu'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['卫星健康状态'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['TGD1'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['TGD2'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 7:
                n_dic['信号发射时刻'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['IODC'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
        if n_dic['卫星PRN号'].startswith('C') == False:
            continue
        n_dic_list.append(n_dic)
        PRN = str(n_dic["卫星PRN号"])
        TIME = n_dic["历元"]
        year = int(TIME.strip('\n')[3:5])
        month = int(TIME.strip('\n')[6:8])
        day = int(TIME.strip('\n')[8:12])
        hour = int(TIME.strip('\n')[12:15])
        minute = int(TIME.strip('\n')[16:18])
        second = float(TIME.strip('\n')[18:20])
        a_0 = float(n_dic["卫星钟偏差(s)"])
        a_1 = float(n_dic["卫星钟漂移(s/s)"])
        a_2 = float(n_dic["卫星钟漂移速度(s/s*s)"])
        C_rs = float(n_dic["C_rs"])
        δn = float(n_dic["n"])
        M0 = float(n_dic["M0"])
        C_uc = float(n_dic["C_uc"])
        e = float(n_dic["e"])
        C_us = float(n_dic["C_us"])
        sqrt_A = float(n_dic["sqrt_A"])
        TOE = float(n_dic["TEO"])
        C_ic = float(n_dic["C_ic"])
        OMEGA = float(n_dic["OMEGA"])
        C_is = float(n_dic["C_is"])
        I_0 = float(n_dic["I_0"])
        C_rc = float(n_dic["C_rc"])
        w = float(n_dic["w"])
        OMEGA_DOT = float(n_dic["OMEGA_DOT"])
        IDOT = float(n_dic["IDOT"])
        sv_accu = n_dic['sv_accu']
        for number in range(int(60 / tstep)):
            t1 = TOE + number * tstep * 60
            CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                        sqrt_A, TOE,
                        C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1, sv_accu)

            endtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, 00)
            satellite_info2['objtime'] = obj_time.isoformat()
            satellite_info2['endtime'] = endtime.isoformat()

    return satellite_info2
def rinexcal3(nfile_lines,obj_time,tstep):
    satellite_info2 = {}

    def start_num():
        for i in range(len(nfile_lines)):
            if nfile_lines[i].find('END OF HEADER') != -1:
                start_num = i + 1
        return start_num

    print('strat line' + str(start_num()))
    n_dic_list = []
    n_data_lines_nums = int((len(nfile_lines) - start_num()) / 8)

    for j in range(n_data_lines_nums):
        n_dic = {}
        for i in range(8):
            data_content = nfile_lines[start_num() + 8 * j + i]
            n_dic['数据组数'] = j + 1
            if i == 0 and 'C' not in str(data_content.strip('\n')[0:3].strip(' ')):
                break
            if i == 0:
                n_dic['卫星PRN号'] = str(data_content.strip('\n')[0:3].strip(' '))
                n_dic['历元'] = data_content.strip('\n')[3:23]
                n_dic['卫星钟偏差(s)'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(
                        ' '))
                n_dic['卫星钟漂移(s/s)'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['卫星钟漂移速度(s/s*s)'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 1:
                n_dic['IODE'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rs'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['n'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['M0'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 2:
                n_dic['C_uc'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['e'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['C_us'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['sqrt_A'] = float(
                    (data_content.strip('\n')[62:80][0:-4] + 'e' + data_content.strip('\n')[62:80][-3:]).strip(' '))
            if i == 3:
                n_dic['TEO'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_ic'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['OMEGA'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['C_is'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))

            if i == 4:
                n_dic['I_0'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['C_rc'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['w'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['OMEGA_DOT'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 5:
                n_dic['IDOT'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['L2_code'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['PS_week_num'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                if (data_content.strip('\n')[61:80]) != '':
                    n_dic['L2_P_code'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
                else:
                    n_dic['L2_P_code']=''
            if i == 6:
                n_dic['卫星精度(m)'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['卫星健康状态'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))
                n_dic['TGD1'] = float(
                    (data_content.strip('\n')[42:61][0:-4] + 'e' + data_content.strip('\n')[42:61][-3:]).strip(' '))
                n_dic['TGD2'] = float(
                    (data_content.strip('\n')[61:80][0:-4] + 'e' + data_content.strip('\n')[61:80][-3:]).strip(' '))
            if i == 7:
                n_dic['信号发射时刻'] = float(
                    (data_content.strip('\n')[4:23][0:-4] + 'e' + data_content.strip('\n')[4:23][-3:]).strip(' '))
                n_dic['IODC'] = float(
                    (data_content.strip('\n')[23:42][0:-4] + 'e' + data_content.strip('\n')[23:42][-3:]).strip(' '))

        n_dic_list.append(n_dic)

    outlist = []
    zz = 0

    for i in range(64):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info2["C" + str(i)] = {}

    def CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                    sqrt_A,
                    TOE, C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1):
        # 1
        GM = 3.986004418e+14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0 + δn

        # 2
        UT = hour + (minute / 60.0) + (second / 3600);
        if year >= 80:
            if year == 80 and month == 1 and day < 6:
                year = year + 2000
            else:
                year = year + 1900
        else:
            year = year + 2000
        if month <= 2:
            year = year - 1
            month = month + 12

        JD = (365.25 * year) + int(30.6001 * (month + 1)) + day + UT / 24 + 1720981.5;
        WN = int((JD - 2444244.5) / 7);
        t_oc = (JD - 2444244.5 - 7.0 * WN) * 24 * 3600.0 - 14;
        if t1 is None:
            t_k = 0
        else:
            δt = a_0 + a_1 * (t1 - TOE) + a_2 * (t1 - TOE) * (t1 - TOE)

            t = t1 - δt

            t_k = t - TOE-14

        # 3
        M_k = M0 + n * t_k

        # 4
        E = 0;
        E1 = 1;
        count = 0;
        while abs(E1 - E) > 1e-12:
            count = count + 1
            E1 = E;
            E = M_k + e * m.sin(E);
            if count > 1e8:
                print("Not convergent!")
                break

        # 5
        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e))

        # 6
        u_0 = V_k + w

        # 7
        δu = C_uc * m.cos(2 * u_0) + C_us * m.sin(2 * u_0)
        δr = C_rc * m.cos(2 * u_0) + C_rs * m.sin(2 * u_0)
        δi = C_ic * m.cos(2 * u_0) + C_is * m.sin(2 * u_0)

        # 8
        u = u_0 + δu
        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E)) + δr
        i = I_0 + δi + IDOT * (t_k);

        # 9
        x_k = r * m.cos(u)
        y_k = r * m.sin(u)
        omega_e = 7.2921150e-5
        if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61' or PRN == 'C62':
            # 10
            OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * TOE;

            # 11
            X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k1 = (y_k * m.sin(i))
            X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(m.radians(-5)) + Z_k1 * m.sin(
                omega_e * t_k) * m.sin(m.radians(-5))
            Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
                m.radians(-5)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(m.radians(-5))
            Z_k = -(Y_k1 * m.sin(m.radians(-5))) + Z_k1 * m.cos(-(5 * m.pi / 180))

        else:
            # 10

            OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * TOE;

            # 11
            X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
            Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
            Z_k = (y_k * m.sin(i))


        if month > 12:
            year = year + 1
            month = month - 12

        if hour < 10:
            hour = '0' + str(hour)
        if minute < 10:
            minute = '0' + str(minute)
        if second < 10:
            second = '0' + str(second)

        name = str(year) + str(month) + str(day) + str(hour) + str(minute)
        satellite_info2['ymd'] = str(year) + str(month) + str(day)
        epochtime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        satellite_info2[PRN][name] = {"PRN": PRN,
                                      "epoch": epochtime.isoformat(),
                                      # "n": n,
                                      # "t_k": t_k,
                                      # "M_k": M_k,
                                      # "E": E,
                                      # "V_k": V_k,
                                      # "u_0": u_0,
                                      # "SDGZX": '(' + str(δu) + ',' + str(δr) + ',' + str(δi) + ')',
                                      # "SG": '(' + str(u) + ',' + str(r) + ',' + str(i) + ')',
                                      # "x_ky_k": '(' + str(x_k) + ',' + str(y_k) + ')',
                                      # "OMEGA_k": OMEGA_k,
                                      "X_k": '%.12f' % X_k,
                                      "Y_k": '%.12f' % Y_k,
                                      "Z_k": '%.12f' % Z_k,
                                      }


    for row in n_dic_list:
        PRN = str(row["卫星PRN号"])
        TIME = row["历元"]
        year = int(TIME.strip('\n')[3:5])
        month = int(TIME.strip('\n')[6:8])
        day = int(TIME.strip('\n')[8:12])
        hour = int(TIME.strip('\n')[12:15])
        minute = int(TIME.strip('\n')[16:18])
        second = float(TIME.strip('\n')[18:20])
        a_0 = float(row["卫星钟偏差(s)"])
        a_1 = float(row["卫星钟漂移(s/s)"])
        a_2 = float(row["卫星钟漂移速度(s/s*s)"])
        IODE = float(row["IODE"])
        C_rs = float(row["C_rs"])
        δn = float(row["n"])
        M0 = float(row["M0"])
        C_uc = float(row["C_uc"])
        e = float(row["e"])
        C_us = float(row["C_us"])
        sqrt_A = float(row["sqrt_A"])
        TOE = float(row["TEO"])
        C_ic = float(row["C_ic"])
        OMEGA = float(row["OMEGA"])
        C_is = float(row["C_is"])
        I_0 = float(row["I_0"])
        C_rc = float(row["C_rc"])
        w = float(row["w"])
        OMEGA_DOT = float(row["OMEGA_DOT"])
        IDOT = float(row["IDOT"])
        L2_code = float(row["L2_code"])
        PS_week_num = float(row["PS_week_num"])
        if row["L2_P_code"] != '':
            L2_P_code = float(row["L2_P_code"])
        else:
            L2_P_code=''

        wxjd = float(row["卫星精度(m)"])
        wxjkzt = float(row["卫星健康状态"])
        TGD1 = float(row["TGD1"])
        TGD2 = float(row["TGD2"])
        transT = float(row["信号发射时刻"])
        IODC = float(row["IODC"])
        t1 = TOE
        epochtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, int(second))
        satellite_info2['in' + str(zz)] = {"PRN": PRN,
                                           "epoch": epochtime.isoformat(),
                                           "a_0": a_0,
                                           "a_1": a_1,
                                           "a_2": a_2,
                                           "IODE": IODE,
                                           "C_rs": C_rs,
                                           "sn": δn,
                                           "M0": M0,
                                           "C_uc": C_uc,
                                           "e": e,
                                           "C_us": C_us,
                                           "sqrt_A": sqrt_A,
                                           "TOE": TOE,
                                           "C_ic": C_ic,
                                           "OMEGA": OMEGA,
                                           "C_is": C_is,
                                           "I_0": I_0,
                                           "C_rc": C_rc,
                                           "w": w,

                                           "OMEGA_DOT": OMEGA_DOT,
                                           "IDOT": IDOT,
                                           "L2_code": L2_code,
                                           "PS_week_num": PS_week_num,
                                           "L2_P_code": L2_P_code,
                                           "wxjd": wxjd,
                                           "wxjkzt": wxjkzt,
                                           #
                                           "TGD1": TGD1,
                                           "TGD2": TGD2,

                                           "transmission_time": transT,
                                           "IODC": IODC

                                           }
        zz = zz + 1
        satellite_info2['num'] = zz
        for number in range(int(60 / tstep)):
            t1 = TOE + number * tstep * 60
            minute=number * tstep
            CulLocation(PRN, year, month, day, hour, minute, second, a_0, a_1, a_2, IDOT, C_rs, δn, M0, C_uc, e, C_us,
                        sqrt_A, TOE,
                        C_ic, OMEGA, C_is, I_0, C_rc, w, OMEGA_DOT, t1)
            endtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, 00)
            satellite_info2['objtime'] = obj_time.isoformat()
            satellite_info2['endtime'] = endtime.isoformat()

    return satellite_info2
def sp3cal(nfile_lines, obj_time):
    satellite_info3 = {}
    for i in range(len(nfile_lines)):
        if (nfile_lines[i].startswith('*') == True):
            start_num = i
            break
    print(start_num)

    t = []
    time = []
    lines = len(nfile_lines) - start_num
    k = 0
    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info3["C" + str(i)] = {}

    for i in range(lines):
        content = nfile_lines[start_num + i]
        year = content[3:7]
        month = content[8:10].replace(' ', '')
        day = content[11:13].replace(' ', '')
        hour = content[14:16].replace(' ', '0')
        second = content[17:19].replace(' ', '0')
        if content.find('*') != -1:
            time.append(
                content[3:7] + "-" + content[8:10] + "-" + content[11:13] + "T" + content[14:16] + ":" + content[
                                                                                                         17:19] + ":" + content[
                                                                                                                        21:31])
            time0 = year + month + day + hour + second
            time1 = year + "-" + month + "-" + day + "T" + hour + ":" + second + ":" + content[21:31]
            time2=datetime.datetime(int(year),int(month),int(day),int(hour),int(second))
            time1=time2.isoformat()
            t.append(k)
            k = k + 15
        elif (content.startswith('PC') == True):
            satname = str(content[1:4])
            x = float(content[5:19]) * 1000
            y = float(content[19:33]) * 1000
            z = float(content[33:47]) * 1000
            GAP = float(content[47:60])
            satellite_info3[satname][time0] = ['%.12f' % x, '%.12f' % y, '%.12f' % z, GAP, time1]

    with open('./static/json/satellite_info3.json', 'w') as f:
        dump(satellite_info3, f)

def sp3cal2(nfile_lines, obj_time):
    satellite_info3 = {}
    # print(nfile_lines)
    for i in range(len(nfile_lines)):
        if (nfile_lines[i].startswith('*') == True):
            start_num = i
            break
    # start_num = 32
    print(start_num)

    t = []
    time = []
    lines = len(nfile_lines) - start_num
    k = 0
    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info3["C" + str(i)] = {}

    for i in range(lines):
        content = nfile_lines[start_num + i]
        year = content[3:7]
        month = content[8:10].replace(' ', '')
        day = content[11:13].replace(' ', '')
        hour = content[14:16].replace(' ', '0')
        second = content[17:19].replace(' ', '0')
        if content.find('*') != -1:
            time.append(
                content[3:7] + "-" + content[8:10] + "-" + content[11:13] + "T" + content[14:16] + ":" + content[
                                                                                                         17:19] + ":" + content[
                                                                                                                        21:31])
            time0 = year + month + day + hour + second
            time1 = year + "-" + month + "-" + day + "T" + hour + ":" + second + ":" + content[21:31]
            time2=datetime.datetime(int(year),int(month),int(day),int(hour),int(second))
            time1=time2.isoformat()
            t.append(k)
            k = k + 15
        elif (content.startswith('PC') == True):
            satname = str(content[1:4])
            x = float(content[5:19]) * 1000
            y = float(content[19:33]) * 1000
            z = float(content[33:47]) * 1000
            GAP = float(content[47:60])
            satellite_info3[satname][time0] = ['%.12f' % x, '%.12f' % y, '%.12f' % z, GAP, time1]

    return satellite_info3
def ioncal(nfile_lines, obj_time):
    ion_info={}
    inx = ionex.reader(nfile_lines)
    t = 0
    for ionex_map in inx:
        tec = []
        time=obj_time+datetime.timedelta(hours=t)
        k=0
        kk=1
        for p in range(2482):
            tec.append(ionex_map.tec[k+kk*73])
            while k==73:
                k=0
                kk+=2
            k+=1
        t+=1
        timeid=str(time.year)+str(time.month)+str(time.day)+str(time.isoformat().strip()[11:13])+'00'
        ion_info[timeid] = tec
    with open('./static/json/ion_info.json', 'w') as f:
        dump(ion_info, f)
def ioncal2(nfile_lines, obj_time):
    ion_info={}
    inx = ionex.reader(nfile_lines)
    t = 0
    for ionex_map in inx:
        tec = []
        time=obj_time+datetime.timedelta(hours=t)
        k=0
        kk=1
        for p in range(2482):
            tec.append(ionex_map.tec[k+kk*73])
            while k==73:
                k=0
                kk+=2
            k+=1
        t+=1
        timeid=str(time.year)+str(time.month)+str(time.day)+str(time.isoformat().strip()[11:13])+'00'
        ion_info[timeid] = tec

    return ion_info

def tlecal(content, obj_time):
    satellite_info = {}
    orbit_info = {}
    j = 0
    for i in range(64):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info["C" + str(i)] = {}
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]
        if name.startswith('C')==False:
            name='C62'
        line1 = content[j + 1]
        line2 = content[j + 2]
        # 调用sgp4算法计算星历每个时刻的位置
        satellite = twoline2rv(line1, line2, wgs84)
        p_list = []
        for k in range(24):
            next_time2 = obj_time + datetime.timedelta(hours=k)
            next_time3= obj_time + datetime.timedelta(hours=k)-datetime.timedelta(seconds=18)
            # print(next_time3)
            next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str2 = [int(z) for z in next_time_str2]
            time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map2 = dict(zip(time_key2, next_time_str2))

            next_time_str3 = next_time3.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str3 = [int(z) for z in next_time_str3]
            time_key3 = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map3 = dict(zip(time_key3, next_time_str3))
            # 调用sgp4库的propagate函数计算对应时刻的位置
            if time_map2['hour'] < 10:
                timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + "0" + str(
                    time_map2['hour']) + "0" + str(time_map2['minute'])
            else:
                timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + str(
                    time_map2['hour']) + "0" + str(time_map2['minute'])
            # print(time_map3)
            position2, velocity2 = satellite.propagate(
                year=time_map3['year'],
                month=time_map3['month'],
                day=time_map3['day'],
                hour=time_map3['hour'],
                minute=time_map3['minute'],
                second=time_map3['second']
            )
            x, y, z = pm.eci2ecef(position2[0] * 1000, position2[1] * 1000, position2[2] * 1000, next_time3)
            # x,y,z=position2[0] * 1000, position2[1] * 1000, position2[2] * 1000
            orbit_info.update({
                name: {
                    'norda': line1[2:7],
                    'Classification': line1[7:8],
                    'internationalid': line1[9:17],
                    'time': line1[18:32],
                    'l1': line1[33:43],
                    'l2': line1[44:52],
                    'bstar': line1[53:61],
                    'orbittype': line1[62:63],
                    'tlecounts': line1[64:68],
                    'Inclination': line2[8:16],
                    'Right Ascension of the Ascending Node'.replace(' ', '_'): line2[17:25],
                    'Eccentricity': line2[26:33],
                    'Argument of Perigee'.replace(' ', '_'): line2[34: 42],
                    'Mean Anomaly'.replace(' ', '_'): line2[43:51],
                    'Mean Motion'.replace(' ', '_'): line2[52:63],
                    'alreadyflys': line2[63:68],
                    'gap': 1
                }
            })
            if name.startswith('C'):
                satellite_info[name][timeid] = {"time": next_time2.isoformat(),
                                                "x": '%.12f' % float(x),
                                                "y": '%.12f' % float(y),
                                                "z": '%.12f' % float(z),
                                                }

        j += 3

    with open('./static/json/satellite_info.json', 'w') as f:
        dump(satellite_info, f)
    with open('./static/json/orbit_info.json', 'w') as f:
        dump(orbit_info, f)

def tlecal3(content, obj_time,tstep):
    satellite_info = {}
    orbit_info = {}
    j = 0
    for i in range(64):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info["C" + str(i)] = {}
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]
        if name.startswith('C')==False:
            name='C62'
        line1 = content[j + 1]
        line2 = content[j + 2]
        # 调用sgp4算法计算星历每个时刻的位置
        satellite = twoline2rv(line1, line2, wgs84)
        p_list = []
        for k in range(24):
            next_time2 = obj_time + datetime.timedelta(hours=k)
            next_time3 = obj_time + datetime.timedelta(hours=k) - datetime.timedelta(seconds=18)
            print(next_time3)
            # print(next_time2)
            for st in range(int(60/tstep)):

                next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
                next_time_str2 = [int(z) for z in next_time_str2]
                time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
                time_map2 = dict(zip(time_key2, next_time_str2))
                # 调用sgp4库的propagate函数计算对应时刻的位置
                timeid = str(next_time2.year) + str(next_time2.month) + str(next_time2.day) + (next_time2.isoformat())[11:13] + (
                                                                                                                                    next_time2.isoformat())[
                                                                                                                                14:16]

                next_time_str3 = next_time3.strftime('%Y %m %d %H %M %S').split(' ')
                next_time_str3 = [int(z) for z in next_time_str3]
                time_key3 = ['year', 'month', 'day', 'hour', 'minute', 'second']
                time_map3 = dict(zip(time_key3, next_time_str3))
                print(time_map2)
                print(time_map3)
                position2, velocity2 = satellite.propagate(
                    year=time_map3['year'],
                    month=time_map3['month'],
                    day=time_map3['day'],
                    hour=time_map3['hour'],
                    minute=time_map3['minute'],
                    second=time_map3['second']
                )
                x, y, z = pm.eci2ecef(position2[0] * 1000, position2[1] * 1000, position2[2] * 1000, next_time3)

                orbit_info.update({
                    name: {
                        'norda': line1[2:7],
                        'Classification': line1[7:8],
                        'internationalid': line1[9:17],
                        'time': line1[18:32],
                        'l1': line1[33:43],
                        'l2': line1[44:52],
                        'bstar': line1[53:61],
                        'orbittype': line1[62:63],
                        'tlecounts': line1[64:68],
                        'Inclination': line2[8:16],
                        'Right Ascension of the Ascending Node'.replace(' ', '_'): line2[17:25],
                        'Eccentricity': line2[26:33],
                        'Argument of Perigee'.replace(' ', '_'): line2[34: 42],
                        'Mean Anomaly'.replace(' ', '_'): line2[43:51],
                        'Mean Motion'.replace(' ', '_'): line2[52:63],
                        'alreadyflys': line2[63:68],
                        'gap': 1
                    }
                })
                if name.startswith('C'):
                    satellite_info[name][timeid] = {"time": next_time2.isoformat(),
                                                    "x": '%.12f' % float(x),
                                                    "y": '%.12f' % float(y),
                                                    "z": '%.12f' % float(z),
                                                    }
                next_time2 = next_time2 + datetime.timedelta(minutes=tstep)
                next_time3 = next_time3 + datetime.timedelta(minutes=tstep)
        j += 3
    return satellite_info,orbit_info


def tlecal2(content, obj_time):
    B0 = 90
    L0 = 180
    H0 = 0
    s = []
    stations_B = np.random.random(size=(37, 73))
    stations_L = np.random.random(size=(37, 73))
    stations_H = np.random.random(size=(37, 73))
    for i in range(37):
        L0 = -180
        for j in range(73):
            s = [B0, L0, H0]
            stations_B[i][j] = B0
            stations_L[i][j] = L0
            stations_H[i][j] = H0
            L0 = L0 + 5
        B0 = B0 - 5
    stations = {}
    k = 0

    while (k < 2701):
        stations[k] = {}
        for t in range(24):
            time = obj_time + datetime.timedelta(hours=t)
            time0 = str(time.year) + str(time.month) + str(time.day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]

            stations[k][time0] = {}
            stations[k][time0]['counts'] = 0
            stations[k][time0]['Q'] = []
            stations[k][time0]['P'] = []
            stations[k][time0]['az'] = []
            stations[k][time0]['el'] = []
        k = k + 1
    j = 0
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]

        if name.startswith('C') == False:
            name = 'C62'
        line1 = content[j + 1]
        line2 = content[j + 2]
        satellite = twoline2rv(line1, line2, wgs84)

        p_list = []
        for k in range(24):
            next_time2 = obj_time + datetime.timedelta(hours=k)
            next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str2 = [int(z) for z in next_time_str2]
            time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map2 = dict(zip(time_key2, next_time_str2))
            timeid = str(next_time2.year) + str(next_time2.month) + str(next_time2.day) + (next_time2.isoformat())[11:13] + (next_time2.isoformat())[
                                                                                                                            14:16]

            position2, velocity2 = satellite.propagate(
                year=time_map2['year'],
                month=time_map2['month'],
                day=time_map2['day'],
                hour=time_map2['hour'],
                minute=time_map2['minute'],
                second=time_map2['second']
            )
            x, y, z = pm.eci2ecef(position2[0] * 1000, position2[1] * 1000, position2[2] * 1000, next_time2)
            x = float(x)
            y = float(y)
            z = float(z)
            angle = []
            h = []
            dian = 0
            for row in range(37):
                for col in range(73):
                    blh = [stations_B[row][col] * m.pi / 180, stations_L[row][col] * m.pi / 180, stations_H[row][col] * m.pi / 180]

                    xyz = pm.geodetic2ecef(blh[0], blh[1], blh[2])
                    X_k1 = x - (xyz[0])
                    Y_k1 = y - (xyz[1])
                    Z_k1 = z - (xyz[2])


                    azi_angle = m.atan2((-m.sin(m.radians(stations_L[row][col])) * X_k1) + m.cos(m.radians(stations_L[row][col])) * Y_k1,
                                        (-m.sin(m.radians(stations_B[row][col]))) * (m.cos(m.radians(stations_L[row][col])) * X_k1 + m.sin(m.radians(stations_L[row][col])) * Y_k1) + m.cos(
                                            m.radians(stations_B[row][col])) * Z_k1)
                    azi_angle = np.rad2deg(azi_angle)
                    altitude = (m.pi / 2 - m.acos((m.cos(stations_B[row][col] * m.pi / 180) * (
                            m.cos(stations_L[row][col] * m.pi / 180) * X_k1 + m.sin(
                        stations_L[row][col] * m.pi / 180) * Y_k1) + m.sin(
                        stations_B[row][col] * m.pi / 180) * Z_k1) / m.sqrt(
                        X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi
                    h.append(altitude)
                    if (altitude > 5):
                        cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        stations[dian][timeid]['counts'] += 1
                        stations[dian][timeid]['Q'].append([cosa, cosb, cosr, 1])
                        stations[dian][timeid]['az'].append(m.radians(azi_angle))
                        stations[dian][timeid]['el'].append(m.radians(altitude))
                        stations[dian][timeid]['P'].append(1)
                    dian += 1
        j += 3
    for z in stations:
        for tid in stations[z]:
            Q = stations[z][tid]['Q']
            if len(Q) < 4:
                continue
            Qt = np.transpose(Q)
            QX = np.dot(Qt, Q)
            QX = np.linalg.inv(QX)
            tr = QX.diagonal()
            if ((tr[0] + tr[1] + tr[2] + tr[3]) < 0):
                GDOP = 0
            else:
                GDOP = m.sqrt(tr[0] + tr[1] + tr[2] + tr[3])
            if ((tr[0] + tr[1] + tr[2]) < 0):
                PDOP = 0
            else:
                PDOP = m.sqrt(tr[0] + tr[1] + tr[2])
            if ((tr[0] + tr[1]) < 0):
                HDOP = 0
            else:
                HDOP = m.sqrt(tr[0] + tr[1])
            if ((tr[2]) < 0):
                VDOP = 0
            else:
                VDOP = m.sqrt(tr[2])
            if ((tr[3]) < 0):
                TDOP = 0
            else:
                TDOP = m.sqrt(tr[3])
            P = np.diag(stations[z][tid]['P'])
            az = np.array(stations[z][tid]['az'])
            el = np.array(stations[z][tid]['el'])
            dopsdata = dops(az, el, m.radians(5), P)
            stations[z][tid]['GDOP'] = round(dopsdata[0], 2)
            stations[z][tid]['PDOP'] = round(dopsdata[1], 2)
            stations[z][tid]['HDOP'] = round(dopsdata[2], 2)
            stations[z][tid]['VDOP'] = round(dopsdata[3], 2)
            stations[z][tid]['TDOP'] = round(TDOP, 2)
            # stations[z][tid]['GDOP'] = round(GDOP, 2)
            # stations[z][tid]['PDOP'] = round(PDOP, 2)
            # stations[z][tid]['HDOP'] = round(HDOP, 2)
            # stations[z][tid]['VDOP'] = round(VDOP, 2)
            # stations[z][tid]['TDOP'] = round(TDOP, 2)

            del stations[z][tid]['Q']
            del stations[z][tid]['P']
            del stations[z][tid]['az']
            del stations[z][tid]['el']
    stations['objtime'] = obj_time.isoformat()
    print("TLE performance success")
    with open('./static/json/stations.json', 'w') as f:
        dump(stations, f)


def Kepcal(year, month, day, hour, minute, second, toe, sattype, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v):
    # 1
    objtime = datetime.datetime(year, month, day, hour, minute, second)
    t_oc = BDS_NYRToweekwis(objtime)[1]
    t = t_oc - (c_gap + c_v * (t_oc - toe))
    t_k = t - toe

    if t_k > 302400:
        t_k -= 604800
    elif t_k < -302400:
        t_k += 604800

    GM = 398600441800000
    GM = 3.9860047e14
    n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
    n = n_0

    M_k = M0 + n * t_k

    E = 0;
    E1 = 1;
    count = 0;
    while abs(E1 - E) > 1e-12:
        count = count + 1
        E1 = E;
        E = M_k + e * m.sin(E);
        if count > 1e8:
            print("Not convergent!")
            break

    V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e));

    u_0 = V_k + w

    r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E))
    i = I_0

    # 9
    x_k = r * m.cos(u_0)
    y_k = r * m.sin(u_0)
    # 10
    omega_e = 7.292115e-5
    OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * toe;

    # 11
    if sattype==0:
        OMEGA_k = OMEGA + OMEGA_DOT * t_k - omega_e * toe;
        X_k1 = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
        Y_k1 = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
        Z_k1 = (y_k * m.sin(i))
        X_k = X_k1 * m.cos(omega_e * t_k) + Y_k1 * m.sin(omega_e * t_k) * m.cos(-(5 * m.pi / 180)) + Z_k1 * m.sin(
            omega_e * t_k) * m.sin(-(5 * m.pi / 180))
        Y_k = -(X_k1 * m.sin(omega_e * t_k)) + Y_k1 * m.cos(omega_e * t_k) * m.cos(
            -(5 * m.pi / 180)) + Z_k1 * m.cos(omega_e * t_k) * m.sin(-(5 * m.pi / 180))
        Z_k = -(Y_k1 * m.sin(-(5 * m.pi / 180))) + Z_k1 * m.cos(-(5 * m.pi / 180))

    else:
        X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
        Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
        Z_k = (y_k * m.sin(i))

    return X_k,Y_k,Z_k




def orbits():
    date = datetime.datetime.now()
    closedate = closedata(date, './static/tle')
    file = "./static/tle/BDSTLE" + closedate + ".txt"
    print(file)
    with open(file, 'rt') as f:
        if f == 0:
            print("can not open file")
        else:
            print("success")
        content = f.readlines()  #
        f.close()
    j = 0
    doc = []
    # define header
    begin2 = str((datetime.datetime.now()).isoformat())
    end2 = str((datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat())
    header = {
        'id': "document",
        "version": "1.0",
        # 'name': name,
        "clock": {
            # "currentTime": begin2,
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begin2, end2),

        }
    }
    doc.append(header)
    while (j < len(content) - 1):
        name = content[j].strip()

        textname = name[-4:-1]
        # print(name.startswith('C'))
        # if textname.startswith('C') == False:
        #     textname = 'C62'
        #     # break
        if name=='BEIDOU-3 G4':
            textname = 'C62'
        if name=='BEIDOU-3 M25':
            textname = 'C63'
            break
        # if name=='BEIDOU-3 M26':
        #     textname = 'C64'
        # print(name)
        line1 = content[j + 1]
        line2 = content[j + 2]
        # gap = 1. / float(line2[52:63]) * 24 * 60 * 60 / 360
        satellite = twoline2rv(line1, line2, wgs84)
        now_time = datetime.datetime.now() - datetime.timedelta(hours=8)
        next_time = datetime.datetime.now()
        position_list = []
        position_list2 = []
        # nums = 500
        for i in range(180):
            next_time = now_time + datetime.timedelta(minutes=15 * (i))
            next_time_str = next_time.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str = [int(v) for v in next_time_str]
            time_key = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map = dict(zip(time_key, next_time_str))
            position, velocity = satellite.propagate(
                year=time_map['year'],
                month=time_map['month'],
                day=time_map['day'],
                hour=time_map['hour'],
                minute=time_map['minute'],
                second=time_map['second']
            )
            position_list.append(next_time.isoformat() + '+00:00')
            position_list.append(position[0] * 1000)
            position_list.append(position[1] * 1000)
            position_list.append(position[2] * 1000)

            position_list2.append(next_time.isoformat() + '+00:00')
            position_list2.append(XYZ_to_LLA(position[0] * 1000, position[1] * 1000, position[2] * 1000)[1])
            position_list2.append(XYZ_to_LLA(position[0] * 1000, position[1] * 1000, position[2] * 1000)[0])
            position_list2.append(0)

        begin = str(now_time.isoformat())
        end = str((next_time).isoformat())

        if (
                textname == 'C06' or textname == 'C07' or textname == 'C08' or textname == 'C09' or textname == 'C10' or textname == 'C13' or textname == 'C16' or textname == 'C31' or textname == 'C38' or textname == 'C39' or textname == 'C40' or textname == 'C56'):
            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">发射日期:</span>20' + line1[9:11] + '年<br/>' +
                               '<span style="color:yellow">轨道类型:</span>IGSO' + '<br/>' +
                               '<span style="color:yellow">NORAD卫星编号:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">卫星轨道倾角:</span>' + line2[8:16] + '度' + '<br/>' +
                               '<span style="color:yellow">升交点赤经:</span>' + line2[17:25] + '度' + '<br/>' +
                               '<span style="color:yellow">轨道偏心率:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">近地点幅角:</span>' + line2[34:42] + '度' + '<br/>' +
                               '<span style="color:yellow">平近点角:</span>' + line2[43:51] + '度' + '<br/>' +
                               '<span style="color:yellow">每天绕地球飞行圈数:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [255, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 14]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname,
                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [255, 0, 255, 255]
                            },
                            # "outlineColor": {
                            #     "rgba": [0, 0, 0, 255]
                            # },
                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "model": {
                    "gltf": "/static/models/IGSO.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,
                    "color": {
                        "rgba": [255, 0, 0, 128]
            },
            "colorBlendMode": "BLEND"

                },
                "orientation": {
                    "unitQuaternion": [-0.5, 0.2, 0.1, 0.5]
                },
                "billboard": {
                    "image": "/static/images/hdigso.png",
                    "scale": 0.37
                },
                "position": {
                    "referenceFrame": 'INERTIAL',
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)

        elif (
                textname == 'C01' or textname == 'C02' or textname == 'C03' or textname == 'C04' or textname == 'C05' or textname == 'C59' or textname == 'C60' or textname == 'C61' or textname == 'C62'):
            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">发射日期:</span>20' + line1[9:11] + '年<br/>' +
                               '<span style="color:yellow">轨道类型:</span>GEO' + '<br/>' +
                               '<span style="color:yellow">NORAD卫星编号:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">卫星轨道倾角:</span>' + line2[8:16] + '度' + '<br/>' +
                               '<span style="color:yellow">升交点赤经:</span>' + line2[17:25] + '度' + '<br/>' +
                               '<span style="color:yellow">轨道偏心率:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">近地点幅角:</span>' + line2[34:42] + '度' + '<br/>' +
                               '<span style="color:yellow">平近点角:</span>' + line2[43:51] + '度' + '<br/>' +
                               '<span style="color:yellow">每天绕地球飞行圈数:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [0, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 12]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname
                },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [255, 69, 0, 255]
                            },
                            # "outlineColor": {
                            #     "rgba": [0, 0, 0, 255]
                            # },

                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "billboard": {
                    "image": "/static/images/hdgeo.png",
                    "scale": 0.37,

                },
                "position": {
                    "referenceFrame": "INERTIAL",
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)
        else:

            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">发射日期:</span>20' + line1[9:11] + '年<br/>' +
                               '<span style="color:yellow">轨道类型:</span>MEO' + '<br/>' +
                               '<span style="color:yellow">NORAD卫星编号:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">卫星轨道倾角:</span>' + line2[8:16] + '度' + '<br/>' +
                               '<span style="color:yellow">升交点赤经:</span>' + line2[17:25] + '度' + '<br/>' +
                               '<span style="color:yellow">轨道偏心率:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">近地点幅角:</span>' + line2[34:42] + '度' + '<br/>' +
                               '<span style="color:yellow">平近点角:</span>' + line2[43:51] + '度' + '<br/>' +
                               '<span style="color:yellow">每天绕地球飞行圈数:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [0, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 12]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname
                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [0, 255, 255, 255]
                            },
                            # "outlineColor": {
                            #     "rgba": [0, 0, 0, 255]
                            # },
                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "model": {
                    "gltf": "/static/models/MEO.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                "billboard": {
                    "image": "/static/images/hdmeo.png",
                    "scale": 0.37
                },
                "position": {
                    "referenceFrame": "INERTIAL",
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)
        body2 = {
            "id": "{}points".format(textname),
            "availability": '{}/{}'.format(begin, end),

            "position": {
                "referenceFrame": 'INERTIAL',
                "interpolationDegree": 5,
                "interpolationAlgorithm": "LAGRANGE",
                "epoch": begin,
                "cartographicDegrees": position_list2,

            },
            "point": {
                "color": {
                    "rgba": [255, 255, 255, 128]
                },
                "outlineColor": {
                    "rgba": [255, 0, 0, 128]
                },
                "outlineWidth": 3,
                'show': 'false',
                "pixelSize": 4,
                'show': 'false',
            },
            "polyline": {
                "width": 1,
                'show': 'false',
                "material": {
                    "polylineDash": {
                        "color": {
                            "rgba": [255, 255, 255, 128]
                        }
                    }
                },
                "arcType": "NONE",
                "positions": {
                    "references": [
                        "{}".format(textname) + "#position", "{}points".format(textname) + "#position"
                    ]
                }
            }

        }
        doc.append(body2)

        j = j + 3
    with open("./static/czml/stellites.czml", 'w') as f:
        dump(doc, f)
    print('czmlsuccess')


def orbits_en():
    date = datetime.datetime.now()
    closedate = closedata(date, './static/tle')
    file = "./static/tle/BDSTLE" + closedate + ".txt"
    print(file)
    with open(file, 'rt') as f:
        if f == 0:
            print("can not open file")
        else:
            print("success")
        content = f.readlines()
        f.close()
    j = 0
    doc = []
    # define header
    begin2 = str((datetime.datetime.now()).isoformat())
    end2 = str((datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat())
    header = {
        'id': "document",
        "version": "1.0",
        # 'name': name,
        "clock": {
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begin2, end2),

        }
    }
    doc.append(header)
    while (j < len(content) - 1):
        name = content[j].strip()

        textname = name[-4:-1]
        # print(name.startswith('C'))
        # if textname.startswith('C') == False:
        #     textname = 'C62'
        #     # break
        if name=='BEIDOU-3 G4':
            textname = 'C62'
        if name=='BEIDOU-3 M25':
            textname = 'C63'
            break
        # print(name)
        line1 = content[j + 1]
        line2 = content[j + 2]
        # gap = 1. / float(line2[52:63]) * 24 * 60 * 60 / 360
        satellite = twoline2rv(line1, line2, wgs84)
        now_time = datetime.datetime.now() - datetime.timedelta(hours=8)
        next_time = datetime.datetime.now()
        position_list = []
        position_list2 = []
        # nums = 500
        for i in range(180):
            next_time = now_time + datetime.timedelta(minutes=15 * (i))
            next_time_str = next_time.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str = [int(v) for v in next_time_str]
            time_key = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map = dict(zip(time_key, next_time_str))
            position, velocity = satellite.propagate(
                year=time_map['year'],
                month=time_map['month'],
                day=time_map['day'],
                hour=time_map['hour'],
                minute=time_map['minute'],
                second=time_map['second']
            )
            position_list.append(next_time.isoformat() + '+00:00')
            position_list.append(position[0] * 1000)
            position_list.append(position[1] * 1000)
            position_list.append(position[2] * 1000)

            position_list2.append(next_time.isoformat() + '+00:00')
            position_list2.append(XYZ_to_LLA(position[0] * 1000, position[1] * 1000, position[2] * 1000)[1])
            position_list2.append(XYZ_to_LLA(position[0] * 1000, position[1] * 1000, position[2] * 1000)[0])
            position_list2.append(0)

        begin = str(now_time.isoformat())
        end = str((next_time).isoformat())


        if (
                textname == 'C06' or textname == 'C07' or textname == 'C08' or textname == 'C09' or textname == 'C10' or textname == 'C13' or textname == 'C16' or textname == 'C31' or textname == 'C38' or textname == 'C39' or textname == 'C40' or textname == 'C56'):
            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">Launch date:</span>20' + line1[9:11] + '<br/>' +
                               '<span style="color:yellow">Orbit type:</span>IGSO' + '<br/>' +
                               '<span style="color:yellow">NORAD ID:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">Inclination:</span>' + line2[8:16]  + '<br/>' +
                               '<span style="color:yellow">Right ascension of ascending node:</span>' + line2[17:25]  + '<br/>' +
                               '<span style="color:yellow">Eccentricity:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">Argument of perigee:</span>' + line2[34:42] + '<br/>' +
                               '<span style="color:yellow">Mean anomaly:</span>' + line2[43:51]  + '<br/>' +
                               '<span style="color:yellow">Mean motion:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [255, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 14]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname,
                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [255, 0, 255, 255]
                            },
                            # "outlineColor": {
                            #     "rgba": [0, 0, 0, 255]
                            # },
                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                "billboard": {

                    "image": "/static/images/hdigso.png",
                    "scale": 0.37
                },
                "position": {
                    "referenceFrame": 'INERTIAL',
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)

        elif (
                textname == 'C01' or textname == 'C02' or textname == 'C03' or textname == 'C04' or textname == 'C05' or textname == 'C59' or textname == 'C60' or textname == 'C61' or textname == 'C62'):
            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">Launch date:</span>20' + line1[9:11] + '<br/>' +
                               '<span style="color:yellow">Orbit type:</span>GEO' + '<br/>' +
                               '<span style="color:yellow">NORAD ID:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">Inclination:</span>' + line2[8:16]  + '<br/>' +
                               '<span style="color:yellow">Right ascension of ascending node:</span>' + line2[17:25]  + '<br/>' +
                               '<span style="color:yellow">Eccentricity:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">Argument of perigee:</span>' + line2[34:42]  + '<br/>' +
                               '<span style="color:yellow">Mean anomaly:</span>' + line2[43:51]  + '<br/>' +
                               '<span style="color:yellow">Mean motion:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [0, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 12]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname
                },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [255, 69, 0, 255]
                            },
                            # "outlineColor": {
                            #     "rgba": [0, 0, 0, 255]
                            # },

                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "billboard": {
                    "image": "/static/images/hdgeo.png",
                    "scale": 0.37,

                },
                "position": {
                    "referenceFrame": "INERTIAL",
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)
        else:

            body = {
                "id": "{}".format(textname),
                "description": '<span style="color:yellow">Launch date:</span>20' + line1[9:11] + '<br/>' +
                               '<span style="color:yellow">Orbit type:</span>MEO' + '<br/>' +
                               '<span style="color:yellow">NORAD ID:</span>' + line2[2:7] + '<br/>' +
                               '<span style="color:yellow">Inclination:</span>' + line2[8:16] + '<br/>' +
                               '<span style="color:yellow">Right ascension of ascending node:</span>' + line2[17:25]  + '<br/>' +
                               '<span style="color:yellow">Eccentricity:</span>' + line2[26:33] + '<br/>' +
                               '<span style="color:yellow">Argument of perigee:</span>' + line2[34:42]  + '<br/>' +
                               '<span style="color:yellow">Mean anomaly:</span>' + line2[43:51]  + '<br/>' +
                               '<span style="color:yellow">Mean motion:</span>' + line2[52:63] + '<br/>',
                "availability": '{}/{}'.format(begin, end),
                "label": {
                    "font": "6pt Lucida Console",
                    "outlineWidth": 2,
                    "outlineColor": {"rgba": [0, 0, 0, 255]},
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {"cartesian2": [20, 12]},
                    "fillColor": {"rgba": [213, 255, 0, 255]},
                    "text": textname
                },
                "path": {
                    "material": {
                        "polylineOutline": {
                            "color": {
                                "rgba": [0, 255, 255, 255]
                            },
                            "outlineColor": {
                                "rgba": [0, 0, 0, 255]
                            },
                            "outlineWidth": 0.5
                        }
                    },
                    "width": 2,
                    "resolution": 360
                },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                "billboard": {
                    "image": "/static/images/hdmeo.png",
                    "scale": 0.37
                },
                "position": {
                    "referenceFrame": "INERTIAL",
                    "interpolationDegree": 5,
                    "interpolationAlgorithm": "LAGRANGE",
                    "epoch": begin,
                    "cartesian": position_list
                }
            }
            doc.append(body)
        body2 = {
            "id": "{}points".format(textname),
            "availability": '{}/{}'.format(begin, end),

            "position": {
                "referenceFrame": 'INERTIAL',
                "interpolationDegree": 5,
                "interpolationAlgorithm": "LAGRANGE",
                "epoch": begin,
                "cartographicDegrees": position_list2,

            },
            "point": {
                "color": {
                    "rgba": [255, 255, 255, 128]
                },
                "outlineColor": {
                    "rgba": [255, 0, 0, 128]
                },
                "outlineWidth": 3,
                'show': 'false',
                "pixelSize": 4,
                'show': 'false',
            },
            "polyline": {
                "width": 1,
                'show': 'false',
                "material": {
                    "polylineDash": {
                        "color": {
                            "rgba": [255, 255, 255, 128]
                        }
                    }
                },
                "arcType": "NONE",
                "positions": {
                    "references": [
                        "{}".format(textname) + "#position", "{}points".format(textname) + "#position"
                    ]
                }
            }

        }
        doc.append(body2)

        j = j + 3
    with open("./static/czml/stellites3.czml", 'w') as f:
        dump(doc, f)
    print('czmlsuccess')
def closedata(obj_time,objpath):
    all_dates=[]
    folder_path = objpath
    all_files = os.listdir(folder_path)
    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            date_str = file_name[6:-4]
            all_dates.append(date_str)
    closest_date = None
    closest_delta = None

    for date in all_dates:
        current_delta = abs(obj_time - datetime.datetime.strptime(date, '%Y-%m-%d'))
        if closest_delta is None or current_delta < closest_delta:
            closest_date = date
            closest_delta = current_delta

    print(f"Closest available date is {closest_date}")
    return closest_date
def rinexget(obj_time):
    NYR=obj_time
    days=(NYR-datetime.datetime(NYR.year,1,1)).days+1
    if days<100 and days>=10:
        days='0'+str(days)
    if days<10:
        days='00'+str(days)
    urllist=["ftp://pub:tarc@ftp2.csno-tarc.cn/brdc/"+str(NYR.year)+"/hour"+str(days)+"0."+str(NYR.year)[2:4]+"b"]
    target_name=[]
    target_name.append('./static/Rinex/' + str(NYR.isoformat().strip()[0:10]) + '.rx')
    for file in target_name:
        if os.path.exists(file):
            os.remove(file)
    opener = urllib.request.build_opener()
    for i in range(1):
        try:
            opener.open(urllist[i])
            download(urllist[i], out=target_name[i])
            print(urllist[i] + 'success')

        except urllib.error.HTTPError:
            print(urllist[i] + '=error')
            # time.sleep(2)
        except urllib.error.URLError:
            print(urllist[i] + '=error')
            # time.sleep(2)

def yumaget(obj_time):
    NYR=obj_time
    days=(NYR-datetime.datetime(NYR.year,1,1)).days+1
    print(NYR)
    print(days)
    if days<100 and days>=10:
        days='0'+str(days)
    if days<10:
        days='00'+str(days)
    urllist=["ftp://pub:tarc@ftp2.csno-tarc.cn/almanac/"+str(NYR.year)+"/conv"+str(days)+"0."+str(NYR.year)[2:4]+"alc"]
    urllist2=["ftp://pub:tarc@ftp2.csno-tarc.cn/almanac/"+str(NYR.year)+"/tarc"+str(days)+"0."+str(NYR.year)[2:4]+"alc"]
    target_name=[]
    target_name.append('./static/YUMA/' + str(NYR.isoformat().strip()[0:10]) + '-c.alc')
    target_name2=[]
    target_name2.append('./static/YUMA/' + str(NYR.isoformat().strip()[0:10]) + '-t.alc')
    for file in target_name:
        if os.path.exists(file):
            os.remove(file)
    for file2 in target_name2:
        if os.path.exists(file2):
            os.remove(file2)
    opener = urllib.request.build_opener()
    for i in range(1):
        try:
            opener.open(urllist[i])
            download(urllist[i], out=target_name[i])
            print(urllist[i] + 'success')

        except urllib.error.HTTPError:
            print(urllist[i] + '=error')
            # time.sleep(2)
        except urllib.error.URLError:
            print(urllist[i] + '=error')
            # time.sleep(2)
    for i in range(1):
        try:
            opener.open(urllist2[i])
            download(urllist2[i], out=target_name2[i])
            print(urllist2[i] + 'success')

        except urllib.error.HTTPError:
            print(urllist2[i] + '=error')
            # time.sleep(2)
        except urllib.error.URLError:
            print(urllist2[i] + '=error')
            # time.sleep(2)

def sp3get2(obj_time):
    target_name = []

    for i in range(1):
        date=obj_time-datetime.timedelta(days=i)
        gps_week = calculate_gps_week(date)
        doy=date2doy(date)
        if doy < 100 and doy >= 10:
            doy = '0' + str(doy)
        if doy < 10:
            doy = '00' + str(doy)
        url1 = 'ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/' + str(gps_week) +'/WUM0MGXULT_' + str(date.year) +str(doy)+'0000_01D_05M_ORB' + '.SP3.gz'
        url2 = 'ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/' + str(gps_week) + '/WUM0MGXULT_' + str(date.year) + str(
            doy) + '0100_01D_05M_ORB' + '.SP3.gz'
        try:
            if os.path.exists('./static/sp3/' + str((date).isoformat().strip()[0:10]) + '.gz'):
                os.remove('./static/sp3/' + str((date).isoformat().strip()[0:10]) + '.gz')
            urllib.request.urlretrieve(url1, r'./static/sp3/' + str((date).isoformat().strip()[0:10]) + '.gz',)
            # my_ftp.download_file(r'./static/sp3/' + str((date).isoformat().strip()[0:10]) + '.gz', url1)
            target_name.append('./static/sp3/' + str((date).isoformat().strip()[0:10]) + '.gz')
            print(url1 + 'success')
        except urllib.error.HTTPError:
            print(url1 + ' http error')
        except urllib.error.URLError:
            print(url1 + ' url error')
    for file in target_name:
        if file.endswith('gz'):
            try:
                sp3un_gz(file)
                os.remove(file)
            except FileNotFoundError:
                continue
    print('sp3 success')
