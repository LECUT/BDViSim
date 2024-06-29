from flask import Flask, render_template, request,jsonify
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import datetime
from json import dump
import csv
import math as m
import numpy as np
import pymap3d as pm
import ionex
from scipy.interpolate import interp1d
import datacal
import os
import UEREcal
from scipy.interpolate import RegularGridInterpolator
app = Flask(__name__)


@app.route('/')
def star():
    datacal.orbits_en()
    return render_template('mainviewen.html')
@app.route('/mainviewcn')
def star_en():
    datacal.orbits()
    return render_template('mainview.html')
@app.route('/index')
def index():
    # orbits()
    return render_template('index.html')

@app.route('/kepler', methods=["POST", "GET"])
def kepler():
    return render_template('kepler.html')

@app.route('/orbitcal', methods=["POST", "GET"])
def orbit():
    return render_template('orbitcal.html')

@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/indexen')
def index_en():
    # orbits()
    return render_template('indexen.html')

@app.route('/kepleren', methods=["POST", "GET"])
def kepler_en():
    return render_template('kepleren.html')

@app.route('/orbitcalen', methods=["POST", "GET"])
def orbit_en():
    return render_template('orbitcalen.html')

@app.route('/serviceen')
def service_en():
    return render_template('serviceen.html')

@app.route('/BDSstars', methods=["POST", "GET"])
def vr1():
    return render_template('VRindex.html')

@app.route('/BDSstructure', methods=["POST", "GET"])
def vr2():
    return render_template('SatelliteStructure.html')

@app.route('/BDSpositioning', methods=["POST", "GET"])
def vr3():
    return render_template('PositioningPrinciple.html')

@app.route('/Rinex', methods=["POST", "GET"])
def upload():
    file = request.get_json()
    content = file["data"]

    satellite_info2 = {}
    nfile_lines = content

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
        if (zz == 1):
            obj_time = datetime.datetime(int("20" + str(year)), month, day, hour, minute, 00)
        print(obj_time)

        endtime = datetime.datetime(int("20" + str(year)), month, day, hour, minute, 00)
        satellite_info2['objtime'] = obj_time.isoformat()
        satellite_info2['endtime'] = endtime.isoformat()
        satellite_info2['num'] = zz

    print("Rinex upload success")
    return jsonify(satellite_info2)


@app.route('/SP3', methods=["POST", "GET"])
def upload2():
    print('read SP3')
    file = request.get_json()
    content = file["data"]
    satellite_info3 = {}

    nfile_lines = content
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
        elif (content.startswith('PC')==True):
            satname=str(content[1:4])
            x = float(content[5:19]) * 1000
            y = float(content[19:33]) * 1000
            z = float(content[33:47]) * 1000

            GAP = float(content[47:60])
            satellite_info3[satname][time0] = ['%.12f' % float(x), '%.12f' % float(y), '%.12f' % float(z), GAP, time1]

    print("SP3 success")
    return jsonify(satellite_info3)

@app.route('/YUMA', methods=["POST", "GET"])
def upload4():
    file = request.get_json()
    content = file["data"]
    objyear = file['year']
    objmonth = file['month']
    objday = file['day']
    print(objyear)
    obj_time=datetime.datetime(int(objyear),int(objmonth),int(objday),00,00,00,00)

    def BDS_weekwisToNYR(week, seconds):
        diffrombegin = week * 604800 + seconds
        BDSbegintime = datetime.datetime(2006, 1, 1, 00, 00, 00, 00)
        result = BDSbegintime + datetime.timedelta(seconds=diffrombegin)
        return result

    def BDS_NYRToweekwis(bdsNYR):
        bdsbeginUTC = datetime.datetime(2006, 1, 1, 00, 00, 00, 00)
        timespan = bdsNYR - bdsbeginUTC
        week = int(timespan.days / 7)
        bdsseconds = (timespan.days - week * 7) * 60 * 60 * 24 + timespan.seconds

        return week, bdsseconds

    rr = int((len(content) - 1) / 15)
    sat_data = {}
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

    def yumacal(year, month, day, hour, minute, second, t, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week):
        # 1
        objtime = datetime.datetime(year, month, day, hour, minute, second)
        t_oc = BDS_NYRToweekwis(objtime)[1]
        t = t_oc - (c_gap + c_v * (t_oc - toe))
        if (BDS_NYRToweekwis(objtime)[0] - week) > 0:
            t += 604800
        t_k = t - toe-14

        if t_k > 302400:
            t_k -= 604800
        elif t_k < -302400:
            t_k += 604800
        # 2
        GM = 398600441800000
        GM = 3.9860047e14
        n_0 = m.sqrt(GM) / m.pow(sqrt_A, 3)
        n = n_0
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
        V_k = m.atan2((m.sqrt(1 - (e * e)) * m.sin(E)), (m.cos(E) - e));

        # 6
        u_0 = V_k + w
        r = m.pow(sqrt_A, 2) * (1 - e * m.cos(E))
        # 7
        # if PRN == 'C01' or PRN == 'C02' or PRN == 'C03' or PRN == 'C04' or PRN == 'C05' or PRN == 'C59' or PRN == 'C60' or PRN == 'C61':
        #     i = I_0
        # else:
        #     i = I_0 + 0.3 * m.pi
        i = I_0

        # 8
        x_k = r * m.cos(u_0)
        y_k = r * m.sin(u_0)

        omega_e = 7.292115e-5
        OMEGA_k = OMEGA + (OMEGA_DOT - omega_e) * t_k - omega_e * toe;
        # 9
        # X_k = (x_k * m.cos(OMEGA_k) - y_k * m.cos(i) * m.sin(OMEGA_k))
        # Y_k = (x_k * m.sin(OMEGA_k) + y_k * m.cos(i) * m.cos(OMEGA_k))
        # Z_k = (y_k * m.sin(i))
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
        sat_data['counts'] = xx

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
            # print(time_map2)
            year = time_map['year']
            month = time_map['month']
            day = time_map['day']
            hour = time_map['hour']
            minute = time_map['minute']
            second = time_map['second']

            yumacal(year, month, day, hour, minute, second, t, toe, PRN, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week)
            t += 3600
            t1 += 3600
            xxx += 1
        xx += 1
    print("YUMA success")
    return jsonify(sat_data)


@app.route('/TLE', methods=["POST", "GET"])
def upload5():
    file = request.get_json()
    content = file["data"]
    objyear = file['year']
    objmonth = file['month']
    objday = file['day']
    obj_time = datetime.datetime(int(objyear), int(objmonth), int(objday), 00, 00, 00, 00)
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
        if name.startswith('C') == False:
            name = 'C62'
        line1 = content[j + 1]
        line2 = content[j + 2]
        satellite = twoline2rv(line1, line2, wgs84)

        p_list = []
        for k in range(24):
            next_time2 = obj_time + datetime.timedelta(hours=k)
            next_time3 = obj_time + datetime.timedelta(hours=k) - datetime.timedelta(seconds=18)
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

            # if time_map2['hour'] < 10:
            #     timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + "0" + str(
            #         time_map2['hour']) + "0" + str(time_map2['minute'])
            # else:
            #     timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + str(
            #         time_map2['hour']) + "0" + str(time_map2['minute'])

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
                    'norda': line1[2:8],
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

            satellite_info[name][timeid] = {"time": next_time2.isoformat(),
                                            "x": '%.12f' % float(x),
                                            "y": '%.12f' % float(y),
                                            "z": '%.12f' % float(z),
                                            }
        j += 3

    print("TLE success")
    return jsonify(satellite_info,orbit_info)

@app.route('/resetalt', methods=["POST", "GET"])
def reseta():
    seta=request.form['alt']
    seta=float(seta)
    density=request.form['density']
    exdate=request.form['date']
    density=int(density)
    sat_name=request.form['satname']

    satellite_info3 = {}

    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    print(obj_time)

    date = str(exdate)
    file='./static/sp3/'+date+'.sp3'
    if os.path.exists(file):
        with open(file, 'r') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            nfile_lines = f.readlines()
            f.close()

        for i in range(len(nfile_lines)):
            if (nfile_lines[i].startswith('*') == True):
                start_num = i
                break

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
                t.append(k)
                k = k + 15
            elif (content.startswith('PC') == True and sat_name.find(str(content[1:4]))!=-1):
                satname = str(content[1:4])

                x = float(content[5:19]) * 1000
                y = float(content[19:33]) * 1000
                z = float(content[33:47]) * 1000
                GAP = float(content[47:60])
                satellite_info3[satname][time0] = ['%.12f' % x, '%.12f' % y, '%.12f' % z, GAP, time1]


        B0 = 90
        L0 = 180
        H0 = 0
        s = []
        bd = int(B0 * 2 / density + 1)
        ld = int(L0 * 2 / density + 1)
        stations_B = np.random.random(size=(bd, ld))
        stations_L = np.random.random(size=(bd, ld))
        stations_H = np.random.random(size=(bd, ld))
        for i in range(bd):
            L0 = -180
            for j in range(ld):
                s = [B0, L0, H0]
                stations_B[i][j] = B0
                stations_L[i][j] = L0
                stations_H[i][j] = H0
                L0 = L0 + density
            B0 = B0 - density
        stations = {}
        k = 0
        bdld = int(bd * ld)
        while (k < bdld):
            stations[k] = {}
            k = k + 1
        k = 0
        while (k < bdld):
            for i in range(24):
                obj_time1 = obj_time + datetime.timedelta(hours=i)
                lasttime = str(obj_time1).strip()[0:4] + str(int(str(obj_time1).strip()[5:7])) + str(int(obj_time1.day)) + str(obj_time1).strip()[
                                                                                                                           11:13] + str(
                    obj_time1).strip()[
                                                                                                                                    14:16]
                stations[k][lasttime] = {}
                stations[k][lasttime]['counts'] = 0
                stations[k][lasttime]['Q'] = []
            k = k + 1

        for lasttime in stations[1]:

            for i in range(lines):

                content = nfile_lines[start_num + i]
                if content.find('*') != -1:
                    year = content[3:7]
                    month = content[8:10].replace(' ', '')
                    day = str(int(content[11:13], base=10))
                    hour = content[14:16].replace(' ', '0')
                    minute = content[17:19].replace(' ', '0')
                    time.append(
                        content[3:7] + "-" + content[8:10] + "-" + content[11:13] + "T" + content[14:16] + ":" + content[
                                                                                                                 17:19] + ":" + content[
                                                                                                                                21:31])
                    time0 = year + month + day + hour + minute
                    time1 = year + "-" + month + "-" + day + "T" + hour + ":" + minute

                    t.append(k)
                    k = k + 15
                elif content.startswith('PC') == True and str(time0) == lasttime and sat_name.find(str(content[1:4]))!=-1:
                    satname = str(content[1:4])
                    x = float(content[5:19]) * 1000
                    y = float(content[19:33]) * 1000
                    z = float(content[33:47]) * 1000
                    angle = []
                    h = []
                    dian = 0
                    for row in range(bd):
                        for col in range(ld):
                            blh = [stations_B[row][col] * m.pi / 180, stations_L[row][col] * m.pi / 180, stations_H[row][col] * m.pi / 180]
                            xyz = datacal.blh2xyz(blh)
                            X_k1 = x - (xyz[0])
                            Y_k1 = y - (xyz[1])
                            Z_k1 = z - (xyz[2])
                            altitude = (m.pi / 2 - m.acos((m.cos(stations_B[row][col] * m.pi / 180) * (
                                    m.cos(stations_L[row][col] * m.pi / 180) * X_k1 + m.sin(
                                stations_L[row][col] * m.pi / 180) * Y_k1) + m.sin(
                                stations_B[row][col] * m.pi / 180) * Z_k1) / m.sqrt(
                                X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi
                            h.append(altitude)
                            if (altitude > seta):
                                cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                                cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                                cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                                stations[dian][time0]['counts'] += 1
                                stations[dian][time0]['Q'].append([cosa, cosb, cosr, 1])
                            dian += 1


        for zz in stations:
            for tid in stations[zz]:
                Q = stations[zz][tid]['Q']
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
                stations[zz][tid]['GDOP'] = GDOP
                stations[zz][tid]['PDOP'] = PDOP
                stations[zz][tid]['HDOP'] = HDOP
                stations[zz][tid]['VDOP'] = VDOP
                stations[zz][tid]['TDOP'] = TDOP

        print("success")

        return jsonify(stations)
    else:
        print(file)
        return 'false'

# TLE performance
@app.route('/reset', methods=["POST", "GET"])
def reset():
    seta=request.form['alt']
    seta=float(seta)
    density=request.form['density']
    exdate=request.form['date']
    density=int(density)
    sat_name=request.form['satname']

    satellite_info3 = {}

    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)

    date = str(exdate)
    file="./static/tle/BDSTLE" + date + ".txt"
    if os.path.exists(file):
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()
    else:
        closedate=datacal.closedata(obj_time, './static/tle')
        file="./static/tle/BDSTLE" + closedate + ".txt"
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()
    B0 = 90
    L0 = 180
    H0 = 0
    s = []
    bd = int(B0 * 2 / density + 1)
    ld = int(L0 * 2 / density + 1)

    stations_B = np.random.random(size=(bd, ld))
    stations_L = np.random.random(size=(bd, ld))
    stations_H = np.random.random(size=(bd, ld))
    for i in range(bd):
        L0 = -180
        for j in range(ld):
            s = [B0, L0, H0]
            stations_B[i][j] = B0
            stations_L[i][j] = L0
            stations_H[i][j] = H0
            L0 = L0 + density
        B0 = B0 - density
    stations = {}
    k = 0
    bdld = int(bd * ld)
    while (k < bdld):
        stations[k] = {}
        k = k + 1
    k = 0
    while (k < bdld):
        for i in range(24):
            obj_time1 = obj_time + datetime.timedelta(hours=i)
            lasttime = str(obj_time1).strip()[0:4] + str(int(str(obj_time1).strip()[5:7])) + str(int(obj_time1.day)) + str(obj_time1).strip()[
                                                                                                                       11:13] + str(
                obj_time1).strip()[
                                                                                                                                14:16]
            stations[k][lasttime] = {}
            stations[k][lasttime]['counts'] = 0
            stations[k][lasttime]['Q'] = []
        k = k + 1
    station = {}
    j = 0
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]

        if name.startswith('C') == False:
            name = 'C62'
        if sat_name.find(str(name)) == -1:
            j += 3
            continue
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

            timeid = str(next_time2.year) + str(next_time2.month) + str(next_time2.day) + (next_time2.isoformat())[11:13] + (
                                                                                                                                next_time2.isoformat())[
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
            for row in range(bd):
                for col in range(ld):
                    blh = [stations_B[row][col] * m.pi / 180, stations_L[row][col] * m.pi / 180, stations_H[row][col] * m.pi / 180]
                    xyz = datacal.blh2xyz(blh)
                    X_k1 = x - (xyz[0])
                    Y_k1 = y - (xyz[1])
                    Z_k1 = z - (xyz[2])
                    altitude = (m.pi / 2 - m.acos((m.cos(stations_B[row][col] * m.pi / 180) * (
                            m.cos(stations_L[row][col] * m.pi / 180) * X_k1 + m.sin(
                        stations_L[row][col] * m.pi / 180) * Y_k1) + m.sin(
                        stations_B[row][col] * m.pi / 180) * Z_k1) / m.sqrt(
                        X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi
                    h.append(altitude)
                    if (altitude > seta):
                        cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        stations[dian][timeid]['counts'] += 1
                        stations[dian][timeid]['Q'].append([cosa, cosb, cosr, 1])
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
            stations[z][tid]['GDOP'] = round(GDOP, 2)
            stations[z][tid]['PDOP'] = round(PDOP, 2)
            stations[z][tid]['HDOP'] = round(HDOP, 2)
            stations[z][tid]['VDOP'] = round(VDOP, 2)
            stations[z][tid]['TDOP'] = round(TDOP, 2)
            del stations[z][tid]['Q']
    print("success")
    return jsonify(stations)


#
@app.route('/worldion_igsgim', methods=["POST", "GET"])
def wioncal_IGS():
    exdate = request.form['date']
    resolution = float(request.form['resolution'])  # 获取并转换分辨率参数
    obj_time = datetime.datetime(int(exdate.strip()[0:4]), int(exdate.strip()[5:7]), int(exdate.strip()[8:10]), 0, 0)
    date = str(exdate)
    file_path = f'./static/ion/{date}.{str(obj_time.year)[2:4]}i'
    print(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            ion_info = {}
            try:
                inx = ionex.reader(f)
                t = 0
                for ionex_map in inx:
                    tec = []
                    time = obj_time + datetime.timedelta(hours=t)

                    # 获取原始网格的纬度和经度
                    original_lats = np.linspace(-87.5, 87.5, 71)  # 假设原始数据的纬度步长为2.5°
                    original_lons = np.linspace(-180, 180, 73)  # 假设原始数据的经度步长为5°

                    # 创建插值函数
                    interpolator = RegularGridInterpolator(
                        (original_lats, original_lons),
                        np.array(ionex_map.tec).reshape((71, 73)),  # 假设ionex_map.tec可以被重新形成为71x73的二维数组
                        bounds_error=False,
                        fill_value=None
                    )

                    # 定义新的全球网格，使用 numpy 生成符合 resolution 的网格点
                    lons = np.arange(-180, 180.1, resolution)
                    lats = np.arange(-90, 90.1, resolution)

                    # 遍历网格点，提取电子含量
                    for lat in lats:
                        for lon in lons:
                            tec_value = interpolator((lat, lon))
                            tec.append(float(tec_value))  # 转换为 float 类型

                    t += 1
                    timeid = f"{time.year}{time.month}{time.day}{time.hour:02d}00"
                    ion_info[timeid] = tec

                print("IONEX calculation success")
                # 将 ndarray 转换为列表
                if isinstance(ion_info, np.ndarray):
                    ion_info = ion_info.tolist()
                # print(ion_info)
                return jsonify(ion_info)
            except Exception as e:
                print(f"Error processing IONEX file: {e}")
                return 'Error processing IONEX file', 500
    else:
        print(f"{file_path} open error")
        return 'File not found', 404
import BDGIM
@app.route('/worldion_bdgim', methods=["POST", "GET"])
def global_ioncal():
    # 获取请求中的参数
    exdate = request.form['date']
    resolution = float(request.form['resolution'])  # 空间分辨率，例如：2.5表示2.5度
    obj_time = datetime.datetime(int(exdate.strip()[0:4]), int(exdate.strip()[5:7]), int(exdate.strip()[8:10]), 0, 0)
    date = str(exdate)

    # 检查并读取RINEX文件
    date_str = str(obj_time.date())
    rinexfile = f'./static/Rinex/{date_str}.rx'
    if os.path.exists(rinexfile):
        with open(rinexfile, 'r') as f:
            nfile_lines = f.readlines()
    else:
        # 如果文件不存在，调用函数下载并再次尝试读取
        datacal.rinexget(obj_time)
        if os.path.exists(rinexfile):
            with open(rinexfile, 'r') as f:
                nfile_lines = f.readlines()
        else:
            return 'RINEX file not found', 404

    # 初始化结果数据结构
    ion_info = {}

    # 定义全球网格，使用 numpy 生成符合 resolution 的网格点
    lons = np.arange(-180, 180.1, resolution)
    lats = np.arange(-90, 90.1, resolution)
    print(lons,lats)
    for i in range(97):  # 计算一天内每15分钟的数据，共97个时间点
        caltime = obj_time + datetime.timedelta(minutes=15 * i)
        # 定义非广播电离层参数
        nonBrdData = BDGIM.NonBrdIonData()
        # 定义广播电离层参数
        brdData = BDGIM.BrdIonData()
        # 定义时间参数
        year = caltime.year
        month = caltime.month
        day = caltime.day
        hour = caltime.hour
        minute = caltime.minute
        second = 0

        # 转换时间为MJD
        mjd = BDGIM.UTC2MJD(year, month, day, hour, minute, second)[0]

        # 解析RINEX数据
        brdPara, svid_list = BDGIM.parse_rinex(nfile_lines, caltime)

        # 使用与原始代码相同的格式生成 timeid
        timeid = f"{caltime.year}{caltime.month}{caltime.day}{caltime.hour:02}00"
        ion_info[timeid] = {}
        tec = []
        for lat in lats:
            for lon in lons:

                # 定义站点和卫星的坐标
                staxyz = pm.geodetic2ecef(lat, lon, 0)
                sta_xyz = [staxyz[0], staxyz[1], staxyz[2]]
                upxyz = pm.geodetic2ecef(lat, lon, 20000)
                sat_xyz = [upxyz[0], upxyz[1], upxyz[2]]

                # 调用IonBdsBrdModel函数计算电离层延迟
                ion_delay, vtec = BDGIM.IonBdsBrdModel(nonBrdData, brdData, mjd, sta_xyz, sat_xyz, brdPara)

                # 存储结果
                tec.append(vtec)
                # print('lon:', str(lon), 'lat:', str(lat),'tec:',str(vtec))
        ion_info[timeid] = tec
    return jsonify(ion_info)

@app.route('/linkstar', methods=["POST", "GET"])
def link():
    # seta = request.form['data']
    obj_time=datetime.datetime(2022,9,15)
    with open('./static/tle/BDSTLE2022-09-15.txt', 'r') as f:
        if f == 0:
            print("can not open file")
        else:
            print("success")
        content = f.readlines()
        f.close()
    satellite_info = {}

    orbit_info = {}
    j = 0
    for i in range(64):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info["C" + str(i)] = {}
    begintime=datetime.datetime(2022, 9, 15, 00, 00, 00, 00)
    endtime = datetime.datetime(2022, 9, 16, 00, 00, 00, 00)
    begintime2 = str(datetime.datetime(2022, 9, 15, 8, 00, 00, 00).isoformat())
    endtime2 = str(datetime.datetime(2022, 9, 15, 17, 00, 00, 00).isoformat())
    doc = []
    header = {
        'id': "document",
        "version": "1.0",
        # 'name': name,
        "clock": {
            "currentTime": begintime2,
            "multiplier": 500,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begintime2, endtime2),

        }
    }
    doc.append(header)
    while (j < len(content) - 1):
        name = content[j].strip()
        textname = name[-4:-1]
        if(textname=='C25' or textname=='C23'or textname=='C24'or textname=='C33'or textname=='C34'or textname=='C59'or textname=='C60'or textname=='C61'or textname=='C38'or textname=='C39'or textname=='C26'or textname=='C37'or name=='BEIDOU-3 IGSO-3'):
            if name=='BEIDOU-3 IGSO-3':
                textname='C40'
            line1 = content[j + 1]
            line2 = content[j + 2]
            satellite = twoline2rv(line1, line2, wgs84)

            p_list = []
            for k in range(24*12*2):
                next_time2 = obj_time + datetime.timedelta(minutes=k*5)
                next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
                next_time_str2 = [int(z) for z in next_time_str2]
                time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
                time_map2 = dict(zip(time_key2, next_time_str2))

                if time_map2['hour'] < 10:
                    timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + "0" + str(
                        time_map2['hour']) + "0" + str(time_map2['minute'])
                else:
                    timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + str(
                        time_map2['hour']) + "0" + str(time_map2['minute'])

                position2, velocity2 = satellite.propagate(
                    year=time_map2['year'],
                    month=time_map2['month'],
                    day=time_map2['day'],
                    hour=time_map2['hour'],
                    minute=time_map2['minute'],
                    second=time_map2['second']
                )

                p_list.append(next_time2.isoformat() + '+00:00')
                p_list.append(position2[0] * 1000)
                p_list.append(position2[1] * 1000)
                p_list.append(position2[2] * 1000)

            begintime = str(datetime.datetime(2022, 9, 15, 00, 00, 00, 00).isoformat())


            if (
                    'IGSO' in name or 'BEIDOU 8 (C08)' == name or 'BEIDOU 5 (C06)' == name or 'BEIDOU 9 (C09)' == name or 'BEIDOU 7 (C07)' == name or 'BEIDOU 20 (C18)' == name or 'BEIDOU 17 (C31)' == name or 'BEIDOU 10 (C10)' == name):
                body = {
                    "id": "{}".format(name),
                    "description": '发射日期:20' + line1[9:11] + '年<br/>' +
                                   '轨道类型:IGSO' + '<br/>' +
                                   'NORAD卫星编号:' + line2[2:7] + '<br/>' +
                                   '卫星轨道倾角:' + line2[8:16] + '度' + '<br/>' +
                                   '升交点赤经:' + line2[17:25] + '度' + '<br/>' +
                                   '轨道偏心率:' + line2[26:33] + '<br/>' +
                                   '近地点幅角:' + line2[34:42] + '度' + '<br/>' +
                                   '平近点角:' + line2[43:51] + '度' + '<br/>' +
                                   '每天绕地球飞行圈数:' + line2[52:63] + '<br/>',
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [255, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 8]},
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
                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                        "resolution": 120
                    },
                    "billboard": {
                        "image": "/static/images/hdigso.png",
                        "scale": 0.37
                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": 'INERTIAL',
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)

            elif (
                    'G' in name or 'BEIDOU-2 G4 (C04)' == name or
                    'BEIDOU 3 (C01)' == name or 'BEIDOU 16 (C02)'
                    == name or 'BEIDOU 11 (C05)' == name):
                body = {
                    "id": "{}".format(name),
                    "description": '发射日期:20' + line1[9:11] + '年<br/>' +
                                   '轨道类型:GEO' + '<br/>' +
                                   'NORAD卫星编号:' + line2[2:7] + '<br/>' +
                                   '卫星轨道倾角:' + line2[8:16] + '度' + '<br/>' +
                                   '升交点赤经:' + line2[17:25] + '度' + '<br/>' +
                                   '轨道偏心率:' + line2[26:33] + '<br/>' +
                                   '近地点幅角:' + line2[34:42] + '度' + '<br/>' +
                                   '平近点角:' + line2[43:51] + '度' + '<br/>' +
                                   '每天绕地球飞行圈数:' + line2[52:63] + '<br/>',
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 5]},
                        "fillColor": {"rgba": [213, 255, 0, 255]},
                        "text": textname
                    },
                    "path": {
                        "material": {
                            "polylineOutline": {
                                "color": {
                                    "rgba": [255, 69, 0, 255]
                                },


                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                        "resolution": 120
                    },
                    "billboard": {
                        "image": "/static/images/hdgeo.png",
                        "scale": 0.37,

                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)
            else:

                body = {
                    "id": "{}".format(name),
                    "description": '发射日期:20' + line1[9:11] + '年<br/>' +
                                   '轨道类型:MEO' + '<br/>' +
                                   'NORAD卫星编号:' + line2[2:7] + '<br/>' +
                                   '卫星轨道倾角:' + line2[8:16] + '度' + '<br/>' +
                                   '升交点赤经:' + line2[17:25] + '度' + '<br/>' +
                                   '轨道偏心率:' + line2[26:33] + '<br/>' +
                                   '近地点幅角:' + line2[34:42] + '度' + '<br/>' +
                                   '平近点角:' + line2[43:51] + '度' + '<br/>' +
                                   '每天绕地球飞行圈数:' + line2[52:63] + '<br/>',
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 5]},
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
                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                    },

                    "billboard": {
                        "image": "/static/images/hdmeo.png",
                        "scale": 0.37
                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)


        j = j + 3
    link1 = {
        "id": "Satellite-ground link",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),

        "position": {
            "cartographicDegrees": [116.33333, 39.93333, 0]
        },
        "label": {

            "font": "6pt Lucida Console",
            "outlineWidth": 2,
            "outlineColor": {"rgba": [255, 0, 0, 255]},
            "horizontalOrigin": "LEFT",
            "pixelOffset": {"cartesian2": [12, 0]},
            "fillColor": {"rgba": [213, 255, 0, 255]},
            "text": 'Beijing'
        },
        "billboard": {

            "image": "/static/images/station.png",
            "scale": 0.1
        },
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [128, 0, 0, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","Satellite-ground link#position"
                ]
            }
        }

    }
    doc.append(link1)
    link2 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C38)",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","BEIDOU-3 IGSO-1 (C38)#position"
                ]
            }
        }

    }
    doc.append(link2)
    link3 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C39)",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","BEIDOU-3 IGSO-2 (C39)#position"
                ]
            }
        }

    }
    doc.append(link3)
    link4 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C61)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G3#position"
                ]
            }
        }

    }
    doc.append(link4)
    link5 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C60)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G2#position"
                ]
            }
        }

    }
    doc.append(link5)
    link6 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C59)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G1 (C59)#position"
                ]
            }
        }

    }
    doc.append(link6)
    link66 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C40)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 IGSO-3#position"
                ]
            }
        }

    }
    doc.append(link66)
    link7 = {
        "id": "Different orbit plane inter-satellite link(C26-C33)",
        'class': 'diforbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [255, 140, 0, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M14 (C33)#position"
                ]
            }
        }

    }
    doc.append(link7)
    link8 = {
        "id": "Different orbit plane inter-satellite link(C26-C34)",
        'class':'diforbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [255, 140, 0, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M15 (C34)#position"
                ]
            }
        }

    }
    doc.append(link8)
    link9 = {
        "id": 'Same orbit plane inter-satellite link(C26-C23)',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M9 (C23)#position"
                ]
            }
        }

    }
    doc.append(link9)
    link10 = {
        "id": "Same orbit plane inter-satellite link(C26-C24)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M10 (C24)#position"
                ]
            }
        }

    }
    doc.append(link10)
    link11 = {
        "id": "Same orbit plane inter-satellite link(C26-C25)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M11 (C25)#position"
                ]
            }
        }

    }
    doc.append(link11)
    link12 = {
        "id": "Same orbit plane inter-satellite link(C26-C37)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M18 (C37)#position"
                ]
            }
        }

    }
    doc.append(link12)
    with open("./static/czml/starlink/starlink.czml", 'w') as f:
        dump(doc, f)
    return render_template('linkstar.html')

@app.route('/linkstaren', methods=["POST", "GET"])
def linken():
    obj_time=datetime.datetime(2022,9,15)
    with open('./static/tle/BDSTLE2022-09-15.txt', 'r') as f:
        if f == 0:
            print("can not open file")
        else:
            print("success")
        content = f.readlines()
        f.close()
    satellite_info = {}

    orbit_info = {}
    j = 0
    for i in range(64):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info["C" + str(i)] = {}
    begintime=datetime.datetime(2022, 9, 15, 00, 00, 00, 00)
    endtime = datetime.datetime(2022, 9, 16, 00, 00, 00, 00)
    begintime2 = str(datetime.datetime(2022, 9, 15, 8, 00, 00, 00).isoformat())
    endtime2 = str(datetime.datetime(2022, 9, 15, 17, 00, 00, 00).isoformat())
    doc = []

    header = {
        'id': "document",
        "version": "1.0",
        "clock": {
            "currentTime": begintime2,
            "multiplier": 500,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begintime2, endtime2),

        }
    }
    doc.append(header)
    while (j < len(content) - 1):
        name = content[j].strip()
        textname = name[-4:-1]
        if(textname=='C25' or textname=='C23'or textname=='C24'or textname=='C33'or textname=='C34'or textname=='C59'or textname=='C60'or textname=='C61'or textname=='C38'or textname=='C39'or textname=='C26'or textname=='C37'or name=='BEIDOU-3 IGSO-3'):
            if name=='BEIDOU-3 IGSO-3':
                textname='C40'
            line1 = content[j + 1]
            line2 = content[j + 2]
            satellite = twoline2rv(line1, line2, wgs84)

            p_list = []
            for k in range(24*12*2):
                next_time2 = obj_time + datetime.timedelta(minutes=k*5)
                next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
                next_time_str2 = [int(z) for z in next_time_str2]
                time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
                time_map2 = dict(zip(time_key2, next_time_str2))

                if time_map2['hour'] < 10:
                    timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + "0" + str(
                        time_map2['hour']) + "0" + str(time_map2['minute'])
                else:
                    timeid = str(time_map2['year']) + str(time_map2['month']) + str(time_map2['day']) + str(
                        time_map2['hour']) + "0" + str(time_map2['minute'])

                position2, velocity2 = satellite.propagate(
                    year=time_map2['year'],
                    month=time_map2['month'],
                    day=time_map2['day'],
                    hour=time_map2['hour'],
                    minute=time_map2['minute'],
                    second=time_map2['second']
                )

                p_list.append(next_time2.isoformat() + '+00:00')
                p_list.append(position2[0] * 1000)
                p_list.append(position2[1] * 1000)
                p_list.append(position2[2] * 1000)

            # filename = "./static/czml/starlink/{}starlink.czml".format(name)
            begintime = str(datetime.datetime(2022, 9, 15, 00, 00, 00, 00).isoformat())


            if (
                    'IGSO' in name or 'BEIDOU 8 (C08)' == name or 'BEIDOU 5 (C06)' == name or 'BEIDOU 9 (C09)' == name or 'BEIDOU 7 (C07)' == name or 'BEIDOU 20 (C18)' == name or 'BEIDOU 17 (C31)' == name or 'BEIDOU 10 (C10)' == name):
                body = {
                    "id": "{}".format(name),
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [255, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 8]},
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
                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                        "resolution": 120
                    },
                    "billboard": {
                        "image": "/static/images/hdigso.png",
                        "scale": 0.37
                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": 'INERTIAL',
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)

            elif (
                    'G' in name or 'BEIDOU-2 G4 (C04)' == name or
                    'BEIDOU 3 (C01)' == name or 'BEIDOU 16 (C02)'
                    == name or 'BEIDOU 11 (C05)' == name):
                body = {
                    "id": "{}".format(name),
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 5]},
                        "fillColor": {"rgba": [213, 255, 0, 255]},
                        "text": textname
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

                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                        "resolution": 120
                    },
                    "billboard": {
                        "image": "/static/images/hdgeo.png",
                        "scale": 0.37,

                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)
            else:

                body = {
                    "id": "{}".format(name),
                    "description": '发射日期:20' + line1[9:11] + '年<br/>' +
                                   '轨道类型:MEO' + '<br/>' +
                                   'NORAD卫星编号:' + line2[2:7] + '<br/>' +
                                   '卫星轨道倾角:' + line2[8:16] + '度' + '<br/>' +
                                   '升交点赤经:' + line2[17:25] + '度' + '<br/>' +
                                   '轨道偏心率:' + line2[26:33] + '<br/>' +
                                   '近地点幅角:' + line2[34:42] + '度' + '<br/>' +
                                   '平近点角:' + line2[43:51] + '度' + '<br/>' +
                                   '每天绕地球飞行圈数:' + line2[52:63] + '<br/>',
                    "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 5]},
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
                                "outlineWidth": 2
                            }
                        },
                        "width": 3,
                    },

                    "billboard": {
                        "image": "/static/images/hdmeo.png",
                        "scale": 0.37
                    },
                "model": {
                    "gltf": "/static/models/satellite.glb",
                    "scale": 8,
                    "minimumPixelSize": 0,
                    'maxmumPixelSize': 100,

                },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begintime,
                        "cartesian": p_list
                    }
                }
                doc.append(body)


        j = j + 3
    link1 = {
        "id": "Satellite-ground link",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),

        "position": {
            "cartographicDegrees": [116.33333, 39.93333, 0]
        },
        "label": {

            "font": "6pt Lucida Console",
            "outlineWidth": 2,
            "outlineColor": {"rgba": [255, 0, 0, 255]},
            "horizontalOrigin": "LEFT",
            "pixelOffset": {"cartesian2": [12, 0]},
            "fillColor": {"rgba": [213, 255, 0, 255]},
            "text": 'Beijing'
        },
        "billboard": {

            "image": "/static/images/station.png",
            "scale": 0.1
        },
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [128, 0, 0, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","Satellite-ground link#position"
                ]
            }
        }

    }
    doc.append(link1)
    link2 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C38)",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","BEIDOU-3 IGSO-1 (C38)#position"
                ]
            }
        }

    }
    doc.append(link2)
    link3 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C39)",
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material" : {
                "polylineGlow" : {
                    "color" : {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower" : 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position","BEIDOU-3 IGSO-2 (C39)#position"
                ]
            }
        }

    }
    doc.append(link3)
    link4 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C61)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G3#position"
                ]
            }
        }

    }
    doc.append(link4)
    link5 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C60)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G2#position"
                ]
            }
        }

    }
    doc.append(link5)
    link6 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C59)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba" : [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 G1 (C59)#position"
                ]
            }
        }

    }
    doc.append(link6)
    link66 = {
        "id": "High-middle orbit plane inter-satellite link(C26-C40)",
        'class': 'high_mid',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 0, 255, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 IGSO-3#position"
                ]
            }
        }

    }
    doc.append(link66)
    link7 = {
        "id": "Different orbit plane inter-satellite link(C26-C33)",
        'class': 'diforbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [255, 140, 0, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M14 (C33)#position"
                ]
            }
        }

    }
    doc.append(link7)
    link8 = {
        "id": "Different orbit plane inter-satellite link(C26-C34)",
        'class':'diforbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [255, 140, 0, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M15 (C34)#position"
                ]
            }
        }

    }
    doc.append(link8)
    link9 = {
        "id": 'Same orbit plane inter-satellite link(C26-C23)',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M9 (C23)#position"
                ]
            }
        }

    }
    doc.append(link9)
    link10 = {
        "id": "Same orbit plane inter-satellite link(C26-C24)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width" : 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M10 (C24)#position"
                ]
            }
        }

    }
    doc.append(link10)
    link11 = {
        "id": "Same orbit plane inter-satellite link(C26-C25)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M11 (C25)#position"
                ]
            }
        }

    }
    doc.append(link11)
    link12 = {
        "id": "Same orbit plane inter-satellite link(C26-C37)",
        'class': 'sameorbits',
        "availability": '{}/{}'.format(begintime, next_time2.isoformat()),
        "polyline": {
            "material": {
                "polylineGlow": {
                    "color": {
                        "rgba": [0, 255, 128, 255]
                    },
                    "glowPower": 0.2
                }
            },
            "width": 8,
            "arcType": "NONE",
            "positions": {
                "references": [
                    "BEIDOU-3 M12 (C26)#position", "BEIDOU-3 M18 (C37)#position"
                ]
            }
        }

    }
    doc.append(link12)
    with open("./static/czml/starlink/starlink.czml", 'w') as f:
        dump(doc, f)
    return render_template('linkstaren.html')

@app.route('/SP3paint', methods=["POST", "GET"])
def SP3paint():
    alt=float(request.form['alt'])
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    height = float(request.form['height'])
    exdate=request.form['date']
    sat_name=request.form['satname']

    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    timeid = str(obj_time.year)+str(obj_time.month)+str(obj_time.day)+'0000'
    date = str(exdate)
    pickp=request.form['pickp']
    file='./static/sp3/'+date+'.sp3'

    if os.path.exists(file):
        with open(file, 'r') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            nfile_lines = f.readlines()
            f.close()
    else:
        datacal.sp3get2(obj_time)
        if os.path.exists(file):
            with open(file, 'r') as f:
                nfile_lines = f.readlines()
                f.close()
        else:
            print(file)
            return 'false'

    satellite_info3 = {}
    station = {}
    for i in range(len(nfile_lines)):
        if (nfile_lines[i].startswith('*') == True):
            start_num = i
            break
    t = []
    time = []
    lines = len(nfile_lines) - start_num
    k = 0
    for i in range(80):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            satellite_info3["C" + str(i)] = {}

    start = 0
    n = 0
    for i in range(lines):
        content = nfile_lines[start_num + i]
        if content.find('*') != -1 and int(content[17:19]) in [0,15,30,45]:

            if (n == 290):
                break

            year = int(content[3:7])
            month = int(content[8:10])
            day = int(content[11:13])
            hour = int(content[14:16])
            minute = int(content[17:19])

            time = datetime.datetime(year, month, day, hour, minute)

            time0 = str(year) + str(month) + str(day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]
            # print(time.isoformat(),' ',time0)
            time1 = time.isoformat()
            if (time0 == timeid):
                start = 1
            if (start == 1):
                n += 1
                station[time0] = {}
                station[time0]['counts'] = 0
                station[time0]['Q'] = []
                station[time0]['P'] = []
                station[time0]['uereP'] = []
                station[time0]['visibility'] = {}
                station[time0]['time'] = time.isoformat()
                station[time0]['az'] = []
                station[time0]['el'] = []

            t.append(k)
            k = k + 15


        elif content.startswith('PC') == True and start == 1 and sat_name.find(str(content[1:4])) != -1:
            satname = str(content[1:4])
            x = float(content[5:19]) * 1000
            y = float(content[19:33]) * 1000
            z = float(content[33:47]) * 1000
            blh = [lat, lon, height]
            xyz = pm.geodetic2ecef(blh[0],blh[1],blh[2])
            X_k1 = x - (xyz[0])

            Y_k1 = y - (xyz[1])
            Z_k1 = z - (xyz[2])
            altitude = (m.pi / 2 - m.acos((m.cos(lat * m.pi / 180) * (
                    m.cos(lon * m.pi / 180) * X_k1 + m.sin(
                lon * m.pi / 180) * Y_k1) + m.sin(
                lat * m.pi / 180) * Z_k1) / m.sqrt(
                X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi

            azi_angle = m.atan2((-m.sin(lon * m.pi / 180) * X_k1) + m.cos(lon * m.pi / 180) * Y_k1,
                                (-m.sin(lat * m.pi / 180)) * (m.cos(lon * m.pi / 180) * X_k1 + m.sin(lon * m.pi / 180) * Y_k1) + m.cos(
                                    lat * m.pi / 180) * Z_k1) * 180 / m.pi
            if (altitude > alt):
                cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                station[time0]['counts'] += 1
                station[time0]['Q'].append([cosa, cosb, cosr, 1])
                station[time0]['az'].append(m.radians(azi_angle))
                station[time0]['el'].append(m.radians(altitude))
                if (
                        satname == 'C01' or satname == 'C02' or satname == 'C03' or satname == 'C04' or satname == 'C05' or satname == 'C06' or satname == 'C07' or satname == 'C08' or satname == 'C09' or satname == 'C10' or satname == 'C11' or satname == 'C12' or satname == 'C13' or satname == 'C14' or satname == 'C16'):
                    uerep=1.04


                elif satname == 'C31' or satname == 'C56' or satname == 'C57' or satname == 'C58':
                    uerep = 0.73
                else:
                    # station[timeid]['uereP'].append(1/((0.4) * (0.4)))
                    uerep = 0.4
                uerep = 4
                if (pickp == 'unit'):
                    var = 1
                    station[time0]['P'].append(1 /(var*var))
                    station[time0]['uereP'].append(1 /(uerep*uerep))
                if (pickp == 's_el'):
                    a = 0.3
                    b = 0.5
                    s_el = np.sin(m.radians(altitude))
                    var = a + b / (s_el**2)
                    station[time0]['P'].append((1 /(var)))
                    station[time0]['uereP'].append((1/((uerep) * (uerep)))*(1 /(var)))
                station[time0]['visibility'][satname] = altitude, azi_angle
                station[time0]['visibility'][satname] = round(altitude, 2), round(azi_angle, 2)

    for tid in station:
        if (station[tid]['counts'] < 4):
            station[tid]['GDOP'] = None
            station[tid]['PDOP'] = None
            station[tid]['HDOP'] = None
            station[tid]['VDOP'] = None
            station[tid]['TDOP'] = None
            station[tid]['Position'] = None
            station[tid]['Vertical'] = None
            station[tid]['Horizontal'] = None
        else:
            Q = station[tid]['Q']
            Qt = np.transpose(Q)
            #权阵计算
            P = np.diag(station[tid]['P'])
            # print(P)

            QX=np.dot(Qt, P)
            QX=np.dot(QX, Q)
            QX = np.linalg.inv(QX)
            tr = QX.diagonal()

            # QXX = np.delete(QX, 3, axis=0)
            # QXX = np.delete(QXX, 3, axis=1)
            # QQ=np.dot(H, QXX)
            # QQ=np.dot(QQ, Ht)
            # tr3=QQ.diagonal()
            # error=UERE*DOP
            uereP = np.diag(station[tid]['uereP'])
            QX2 = np.dot(Qt, uereP)
            QX2 = np.dot(QX2, Q)
            QX2 = np.linalg.inv(QX2)
            tr2 = QX2.diagonal()

            if ((tr[0] + tr[1] + tr[2] + tr[3]) < 0):
                GDOP = 0
            else:
                GDOP = m.sqrt(tr[0] + tr[1] + tr[2] + tr[3])
            if ((tr[0] + tr[1] + tr[2]) < 0):
                PDOP = 0
            else:
                PDOP = m.sqrt(tr[0] + tr[1] + tr[2])
                Position = m.sqrt(tr2[0] + tr2[1] + tr2[2])
            if ((tr[0] + tr[1]) < 0):
                HDOP = 0
            else:
                HDOP = m.sqrt(tr[0] + tr[1])
                Horizontal = m.sqrt(tr2[0] + tr2[1])
            if ((tr[2]) < 0):
                VDOP = 0
            else:
                VDOP = m.sqrt(tr[2])
                Vertical = m.sqrt(tr2[2])
            if ((tr[3]) < 0):
                TDOP = 0
            else:
                TDOP = m.sqrt(tr[3])
            # station[tid]['GDOP'] = GDOP
            # station[tid]['PDOP'] = PDOP
            # station[tid]['HDOP'] = HDOP
            # station[tid]['VDOP'] = VDOP
            # station[tid]['TDOP'] = TDOP
            # station[tid]['Vertical'] = Vertical
            # station[tid]['Horizontal'] = Horizontal
            # station[tid]['Position'] = Position

            az=np.array(station[tid]['az'])
            el=np.array(station[tid]['el'])

            dops = datacal.dops(az, el, m.radians(alt), P)
            dops_accuracy = datacal.dops_accuracy(az, el, m.radians(alt), uereP)
            del station[tid]['Q']
            del station[tid]['P']
            del station[tid]['uereP']
            station[tid]['GDOP'] = round(dops[0], 2)
            station[tid]['PDOP'] = round(dops[1], 2)
            station[tid]['HDOP'] = round(dops[2], 2)
            station[tid]['VDOP'] = round(dops[3], 2)
            station[tid]['TDOP'] = round(TDOP, 2)
            station[tid]['Vertical'] = round(dops_accuracy[3], 2)
            station[tid]['Horizontal'] = round(dops_accuracy[2], 2)
            station[tid]['Position'] = round(dops_accuracy[1], 2)

    print(station)
    print("success")
    # print(sat2)
    return jsonify(station)

@app.route('/TLEpaint', methods=["POST", "GET"])
def TLEpaint():

    alt=float(request.form['alt'])
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    height = float(request.form['height'])
    print(lat,lon)
    exdate=request.form['date']
    sat_name=request.form['satname']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    timeid = str(obj_time.year)+str(obj_time.month)+str(obj_time.day)+'0000'
    date = str(exdate)
    pickp=request.form['pickp']


    file="./static/tle/BDSTLE" + date + ".txt"
    if os.path.exists(file):
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()
    else:
        closedate=datacal.closedata(obj_time, './static/tle')
        file="./static/tle/BDSTLE" + closedate + ".txt"
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()


    station = {}
    for t in range(96):
        time = obj_time + datetime.timedelta(minutes=t * 15)

        time0 = str(time.year) + str(time.month) + str(time.day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]
        station[time0] = {}
        station[time0]['counts'] = 0
        station[time0]['Q'] = []
        station[time0]['P'] = []
        station[time0]['uereP'] = []
        station[time0]['visibility'] = {}
        station[time0]['time'] = time.isoformat()
        station[time0]['az']=[]
        station[time0]['el']=[]

    j = 0
    # for i in range(64):
    #     if (i != 0):
    #         if (i < 10):
    #             i = "0" + str(i)
    #         satellite_info["C" + str(i)] = {}
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]

        if name.startswith('C') == False:
            name = 'C62'
        if sat_name.find(str(name)) == -1:
            j += 3
            continue
        # print(name+'1')
        line1 = content[j + 1]
        line2 = content[j + 2]
        satellite = twoline2rv(line1, line2, wgs84)

        p_list = []
        for k in range(96):
            next_time2 = obj_time + datetime.timedelta(minutes=k * 15)
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
            blh = [lat, lon, height]
            xyz = datacal.blh2xyz(blh)
            xyz2=pm.geodetic2ecef(blh[0],blh[1],blh[2])


            X_k1 = x - (xyz2[0])
            Y_k1 = y - (xyz2[1])
            Z_k1 = z - (xyz2[2])
            # dxyz=[X_k1,Y_k1,Z_k1]
            # H = [[-m.sin(m.radians(lon)), m.cos(m.radians(lon)), 0],
            #      [-m.sin(m.radians(lat)) * m.cos(m.radians(lon)), -m.sin(m.radians(lat)) * m.sin(m.radians(lon)), m.cos(m.radians(lat))],
            #      [m.cos(m.radians(lat)) * m.cos(m.radians(lon)), m.cos(m.radians(lat)) * m.sin(m.radians(lon)), m.sin(m.radians(lat))]]
            # enu=np.dot(H,dxyz)
            # X_k1=enu[0]
            # Y_k1=enu[1]
            # Z_k1=enu[2]
            altitude = (m.pi / 2 - m.acos((m.cos(m.radians(lat)) * (
                    m.cos(m.radians(lon)) * X_k1 + m.sin(
                m.radians(lon)) * Y_k1) + m.sin(
                m.radians(lat)) * Z_k1) / m.sqrt(
                X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)))
            altitude=np.rad2deg(altitude)

            azi_angle = m.atan2((-m.sin(m.radians(lon)) * X_k1) + m.cos(m.radians(lon)) * Y_k1,
                                (-m.sin(m.radians(lat))) * (m.cos(m.radians(lon)) * X_k1 + m.sin(m.radians(lon)) * Y_k1) + m.cos(
                                    m.radians(lat)) * Z_k1)
            azi_angle = np.rad2deg(azi_angle)
            if (altitude> alt):
                cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                station[timeid]['counts'] += 1
                station[timeid]['Q'].append([cosa, cosb, cosr, 1])
                station[timeid]['az'].append(m.radians(azi_angle))
                station[timeid]['el'].append(m.radians(altitude))
                if (
                        name == 'C01' or name == 'C02' or name == 'C03' or name == 'C04' or name == 'C05' or name == 'C06' or name == 'C07' or name == 'C08' or name == 'C09' or name == 'C10' or name == 'C11' or name == 'C12' or name == 'C13' or name == 'C14' or name == 'C16'):
                    # station[timeid]['uereP'].append(1/((1.04) * (1.04)))
                    uerep=1.04
                elif name=='C31'or name == 'C56'or name == 'C57'or name == 'C58':
                    uerep = 0.73
                else:
                    # station[timeid]['uereP'].append(1/((0.4) * (0.4)))
                    uerep = 0.4
                uerep=4
                if(pickp=='unit'):
                    var = 1
                    station[timeid]['P'].append(1 /(var*var))
                    station[timeid]['uereP'].append(1 /(uerep*uerep))
                if(pickp=='s_el'):
                    a = 0.003
                    b = 0.09
                    s_el = np.sin(m.radians(altitude))
                    var = a + b / (s_el**2)
                    station[timeid]['P'].append((1 /(var)))
                    station[timeid]['uereP'].append((1/((uerep) * (uerep)))*(1 /(var)))
                # if(pickp=='c_el'):
                #     a = 1.5
                #     b = 1
                #     var = a + b*m.cos(m.radians(altitude))
                #     station[timeid]['P'].append((1 /(var))*(1/((uerep) * (uerep))))
                # if(pickp=='exp'):
                #     a = 0.04
                #     b = 0.23
                #     var = (a + b * m.exp(-m.radians(altitude) / np.deg2rad(33.1))) ** 2
                #     station[timeid]['P'].append((1/(var))*(1/((uerep) * (uerep))))
                station[timeid]['visibility'][name] = altitude, azi_angle
                station[timeid]['visibility'][name] = round(altitude, 2), round(azi_angle, 2)
        j += 3

    for tid in station:
        if (station[tid]['counts'] < 4):
            station[tid]['GDOP'] = None
            station[tid]['PDOP'] = None
            station[tid]['HDOP'] = None
            station[tid]['VDOP'] = None
            station[tid]['TDOP'] = None
            station[tid]['Position'] = None
            station[tid]['Vertical'] = None
            station[tid]['Horizontal'] = None
        else:
            # H=[[-m.sin(m.radians(lon)),m.cos(m.radians(lon)),0],[-m.sin(m.radians(lat))*m.cos(m.radians(lon)),-m.sin(m.radians(lat))*m.sin(m.radians(lon)),m.cos(m.radians(lat))],[m.cos(m.radians(lat))*m.cos(m.radians(lon)),m.cos(m.radians(lat))*m.sin(m.radians(lon)),m.sin(m.radians(lat))]]
            #
            # Ht=np.transpose(H)

            Q = station[tid]['Q']
            Qt = np.transpose(Q)
            #权阵计算
            P = np.diag(station[tid]['P'])
            # print(P)

            QX=np.dot(Qt, P)
            QX=np.dot(QX, Q)
            QX = np.linalg.inv(QX)
            tr = QX.diagonal()

            # QXX = np.delete(QX, 3, axis=0)
            # QXX = np.delete(QXX, 3, axis=1)
            # QQ=np.dot(H, QXX)
            # QQ=np.dot(QQ, Ht)
            # tr3=QQ.diagonal()
            # error=UERE*DOP
            uereP = np.diag(station[tid]['uereP'])
            QX2 = np.dot(Qt, uereP)
            QX2 = np.dot(QX2, Q)
            QX2 = np.linalg.inv(QX2)
            tr2 = QX2.diagonal()

            if ((tr[0] + tr[1] + tr[2] + tr[3]) < 0):
                GDOP = 0
            else:
                GDOP = m.sqrt(tr[0] + tr[1] + tr[2] + tr[3])
            if ((tr[0] + tr[1] + tr[2]) < 0):
                PDOP = 0
            else:
                PDOP = m.sqrt(tr[0] + tr[1] + tr[2])
                Position = m.sqrt(tr2[0] + tr2[1] + tr2[2])
            if ((tr[0] + tr[1]) < 0):
                HDOP = 0
            else:
                HDOP = m.sqrt(tr[0] + tr[1])
                Horizontal = m.sqrt(tr2[0] + tr2[1])
            if ((tr[2]) < 0):
                VDOP = 0
            else:
                VDOP = m.sqrt(tr[2])
                Vertical = m.sqrt(tr2[2])
            if ((tr[3]) < 0):
                TDOP = 0
            else:
                TDOP = m.sqrt(tr[3])
            # station[tid]['GDOP'] = GDOP
            # station[tid]['PDOP'] = PDOP
            # station[tid]['HDOP'] = HDOP
            # station[tid]['VDOP'] = VDOP
            # station[tid]['TDOP'] = TDOP
            # station[tid]['Vertical'] = Vertical
            # station[tid]['Horizontal'] = Horizontal
            # station[tid]['Position'] = Position

            az=np.array(station[tid]['az'])
            el=np.array(station[tid]['el'])

            dops = datacal.dops(az, el, m.radians(alt), P)
            dops_accuracy = datacal.dops_accuracy(az, el, m.radians(alt), uereP)
            del station[tid]['Q']
            del station[tid]['P']
            del station[tid]['uereP']
            station[tid]['GDOP'] = round(dops[0], 2)
            station[tid]['PDOP'] = round(dops[1], 2)
            station[tid]['HDOP'] = round(dops[2], 2)
            station[tid]['VDOP'] = round(dops[3], 2)
            station[tid]['TDOP'] = round(TDOP, 2)
            station[tid]['Vertical'] = round(dops_accuracy[3], 2)
            station[tid]['Horizontal'] = round(dops_accuracy[2], 2)
            station[tid]['Position'] = round(dops_accuracy[1], 2)
    print("计算完毕")
    # print(station)
    return jsonify(station)
@app.route('/YUMApaint', methods=["POST", "GET"])
def YUMApaint():

    alt=float(request.form['alt'])
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    height = float(request.form['height'])
    print(lat,lon)
    exdate=request.form['date']
    sat_name=request.form['satname']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    timeid = str(obj_time.year)+str(obj_time.month)+str(obj_time.day)+'0000'
    date = str(exdate)
    pickp=request.form['pickp']

    yumafile1 = './static/YUMA/' + date + '-c.alc'
    yumafile2 = './static/YUMA/' + date + '-t.alc'
    if os.path.exists(yumafile1):
        print('打开C')
        with open(yumafile1, 'r') as f:
            content = f.readlines()
            satinfo = datacal.yumacal2(content, obj_time,'c', 15)
            f.close()
    elif os.path.exists(yumafile2):
        print('打开T')
        with open(yumafile2, 'r') as f:
            content = f.readlines()
            satinfo = datacal.yumacal2(content, obj_time,'t', 15)
            f.close()
    else:
        datacal.yumaget(obj_time)
        if os.path.exists(yumafile1):
            with open(yumafile1, 'r') as f:
                content = f.readlines()
                satinfo = datacal.yumacal2(content, obj_time,'c', 15)
                f.close()
        elif os.path.exists(yumafile2):
            with open(yumafile2, 'r') as f:
                content = f.readlines()
                satinfo = datacal.yumacal2(content, obj_time,'t', 15)
                f.close()
        else:

            closedate = datacal.closedata2(obj_time, './static/YUMA')
            yumafile = "./static/YUMA/" + closedate + "-t.alc"
            print(yumafile)
            with open(yumafile, 'r') as f:
                content = f.readlines()
                satinfo = datacal.yumacal2(content, obj_time,'t', 15)
                f.close()



    station = {}
    for t in range(96):
        time = obj_time + datetime.timedelta(minutes=t * 15)

        time0 = str(time.year) + str(time.month) + str(time.day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]
        station[time0] = {}
        station[time0]['counts'] = 0
        station[time0]['Q'] = []
        station[time0]['P'] = []
        station[time0]['uereP'] = []
        station[time0]['visibility'] = {}
        station[time0]['time'] = time.isoformat()
        station[time0]['az'] = []
        station[time0]['el'] = []

    for name in satinfo:
        if sat_name.find(str(name)) == -1:
            continue
        for timeid in satinfo[name]:

            x = float(satinfo[name][timeid]['X_k'])
            y = float(satinfo[name][timeid]['Y_k'])
            z = float(satinfo[name][timeid]['Z_k'])
            blh = [lat, lon, height]
            blh2 = [np.radians(lat), np.radians(lon), height]
            xyz2 = pm.geodetic2ecef(blh[0], blh[1], blh[2])
            X_k1 = x - (xyz2[0])
            Y_k1 = y - (xyz2[1])
            Z_k1 = z - (xyz2[2])

            altitude = (m.pi / 2 - m.acos((m.cos(m.radians(lat)) * (
                    m.cos(m.radians(lon)) * X_k1 + m.sin(
                m.radians(lon)) * Y_k1) + m.sin(
                m.radians(lat)) * Z_k1) / m.sqrt(
                X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)))
            altitude = np.rad2deg(altitude)

            azi_angle = m.atan2((-m.sin(m.radians(lon)) * X_k1) + m.cos(m.radians(lon)) * Y_k1,
                                (-m.sin(m.radians(lat))) * (m.cos(m.radians(lon)) * X_k1 + m.sin(m.radians(lon)) * Y_k1) + m.cos(
                                    m.radians(lat)) * Z_k1)
            azi_angle = np.rad2deg(azi_angle)
            if (altitude > alt):
                cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                # sv_accu = satinfo[name][timeid]['sv_accu']
                # eptime = satinfo[name][timeid]['time']
                # eptime = [eptime.year, eptime.month, eptime.day, eptime.hour, eptime.minute, eptime.second]
                # gtime = UEREcal.epoch2time(eptime)
                # az = np.radians(azi_angle)
                # el = np.radians(altitude)
                # uerep = UEREcal.get_UERE(gtime, blh2, az, el, None, sv_accu)
                if (
                        name == 'C01' or name == 'C02' or name == 'C03' or name == 'C04' or name == 'C05' or name == 'C06' or name == 'C07' or name == 'C08' or name == 'C09' or name == 'C10' or name == 'C11' or name == 'C12' or name == 'C13' or name == 'C14' or name == 'C16'):
                    # station[timeid]['uereP'].append(1/((1.04) * (1.04)))
                    uerep=1.04
                elif name=='C31'or name == 'C56'or name == 'C57'or name == 'C58':
                    uerep = 0.73
                else:
                    # station[timeid]['uereP'].append(1/((0.4) * (0.4)))
                    uerep = 0.4
                uerep=4
                # print(uerep)
                # print(name,eptime,uerep,az,el,blh2)
                station[timeid]['counts'] += 1
                station[timeid]['Q'].append([cosa, cosb, cosr, 1])
                station[timeid]['az'].append(round(m.radians(azi_angle), 2))
                station[timeid]['el'].append(round(m.radians(altitude), 2))

                # ****
                # EL.append(altitude)
                # AZ.append(azi_angle)
                # timear.append(eptime)
                # *****

                if (pickp == 'unit'):
                    var = 1
                    station[timeid]['P'].append(1 / (var * var))
                    station[timeid]['uereP'].append(1 / (uerep * uerep))
                if (pickp == 's_el'):
                    a = 0.003
                    b = 0.09
                    s_el = np.sin(m.radians(altitude))
                    var = a + b / (s_el ** 2)
                    station[timeid]['P'].append((1 / (var)))
                    station[timeid]['uereP'].append((1 / ((uerep) * (uerep))) * (1 / (var)))
                station[timeid]['visibility'][name] = round(altitude, 2), round(azi_angle, 2)

    for tid in station:
        if (station[tid]['counts'] < 4):
            station[tid]['GDOP'] = None
            station[tid]['PDOP'] = None
            station[tid]['HDOP'] = None
            station[tid]['VDOP'] = None
            station[tid]['TDOP'] = None
            station[tid]['Position'] = None
            station[tid]['Vertical'] = None
            station[tid]['Horizontal'] = None
        else:
            Q = station[tid]['Q']
            Qt = np.transpose(Q)
            P = np.diag(station[tid]['P'])
            QX = np.dot(Qt, P)
            QX = np.dot(QX, Q)
            QX = np.linalg.inv(QX)
            tr = QX.diagonal()

            uereP = np.diag(station[tid]['uereP'])
            QX2 = np.dot(Qt, uereP)
            QX2 = np.dot(QX2, Q)
            QX2 = np.linalg.inv(QX2)
            tr2 = QX2.diagonal()

            if ((tr[3]) < 0):
                TDOP = 0
            else:
                TDOP = m.sqrt(tr[3])
            az = np.array(station[tid]['az'])
            el = np.array(station[tid]['el'])
            dops = datacal.dops(az, el, m.radians(alt), P)
            dops_accuracy = datacal.dops_accuracy(az, el, m.radians(alt), uereP)
            del station[tid]['Q']
            del station[tid]['P']
            del station[tid]['uereP']
            station[tid]['GDOP'] = round(dops[0], 2)
            station[tid]['PDOP'] = round(dops[1], 2)
            station[tid]['HDOP'] = round(dops[2], 2)
            station[tid]['VDOP'] = round(dops[3], 2)
            station[tid]['TDOP'] = round(TDOP, 2)
            station[tid]['Vertical'] = round(dops_accuracy[3], 2)
            station[tid]['Horizontal'] = round(dops_accuracy[2], 2)
            station[tid]['Position'] = round(dops_accuracy[1], 2)

            # *****
            # GDOP.append(round(dops[0], 2))
            # PDOP.append(round(dops[1], 2))
            # HDOP.append(round(dops[2], 2))
            # VDOP.append(round(dops[3], 2))
            # TDOP1.append(round(TDOP,2))
            # VER.append(round(dops_accuracy[3],2))
            # HOR.append(round(dops_accuracy[2],2))
            # POS.append(round(dops_accuracy[1],2))
    # *******
    # CNT=[]
    # for tid in station:
    #     CNT.append(station[tid]['counts'])
    # data = { 'GDOP': GDOP, 'HDOP': HDOP,'PDOP':PDOP,'VDOP': VDOP,'TDOP': TDOP1,'VER': VER,'HOR': HOR,'POS': POS,'COUNTS':CNT}
    # df = pd.DataFrame(data)
    # df.to_csv('data.csv', index=False)

    # ****
    print("success")

    return jsonify(station)
@app.route('/rinexpaint', methods=["POST", "GET"])
def rinexpaint():
    # ****
    # EL= []
    # AZ=[]
    # HDOP=[]
    # TDOP1=[]
    # VDOP=[]
    # PDOP=[]
    # GDOP=[]
    # VER=[]
    # HOR=[]
    # POS=[]
    # timear=[]
    # *******
    alt=float(request.form['alt'])
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    height = float(request.form['height'])

    print(lat,lon,height)
    exdate=request.form['date']
    sat_name=request.form['satname']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    date = str(exdate)
    pickp=request.form['pickp']

    file='./static/Rinex/' + date + '.rx'
    if os.path.exists(file):
        with open(file, 'r') as f:
            nfile_lines = f.readlines()
            f.close()
        satinfo = datacal.rinexcal2(nfile_lines, obj_time, 15)

        station = {}
        for t in range(96):
            time = obj_time + datetime.timedelta(minutes=t * 15)

            time0 = str(time.year) + str(time.month) + str(time.day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]
            station[time0] = {}
            station[time0]['counts'] = 0
            station[time0]['Q'] = []
            station[time0]['P'] = []
            station[time0]['uereP'] = []
            station[time0]['visibility'] = {}
            station[time0]['time'] = time.isoformat()
            station[time0]['az']=[]
            station[time0]['el']=[]


        for name in satinfo:
            if sat_name.find(str(name)) == -1:
                continue
            for timeid in satinfo[name]:

                x = float(satinfo[name][timeid]['X_k'])
                y = float(satinfo[name][timeid]['Y_k'])
                z = float(satinfo[name][timeid]['Z_k'])
                blh = [lat, lon, height]
                blh2=[np.radians(lat),np.radians(lon),height]
                xyz = datacal.blh2xyz(blh)
                xyz2=pm.geodetic2ecef(blh[0],blh[1],blh[2])
                X_k1 = x - (xyz2[0])
                Y_k1 = y - (xyz2[1])
                Z_k1 = z - (xyz2[2])

                altitude = (m.pi / 2 - m.acos((m.cos(m.radians(lat)) * (
                        m.cos(m.radians(lon)) * X_k1 + m.sin(
                    m.radians(lon)) * Y_k1) + m.sin(
                    m.radians(lat)) * Z_k1) / m.sqrt(
                    X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)))
                altitude=np.rad2deg(altitude)

                azi_angle = m.atan2((-m.sin(m.radians(lon)) * X_k1) + m.cos(m.radians(lon)) * Y_k1,
                                    (-m.sin(m.radians(lat))) * (m.cos(m.radians(lon)) * X_k1 + m.sin(m.radians(lon)) * Y_k1) + m.cos(
                                        m.radians(lat)) * Z_k1)
                azi_angle = np.rad2deg(azi_angle)
                if (altitude> alt):
                    cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                    cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                    cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                    sv_accu=satinfo[name][timeid]['sv_accu']
                    eptime=satinfo[name][timeid]['time']
                    eptime=[eptime.year,eptime.month,eptime.day,eptime.hour,eptime.minute,eptime.second]
                    gtime=UEREcal.epoch2time(eptime)
                    az=np.radians(azi_angle)
                    el=np.radians(altitude)
                    uerep=UEREcal.get_UERE(gtime,blh2,az,el,None,sv_accu)
                    print(uerep)
                    # print(name,eptime,uerep,az,el,blh2)
                    station[timeid]['counts'] += 1
                    station[timeid]['Q'].append([cosa, cosb, cosr, 1])
                    station[timeid]['az'].append(round(m.radians(azi_angle),2))
                    station[timeid]['el'].append(round(m.radians(altitude),2))

                    # ****
                    # EL.append(altitude)
                    # AZ.append(azi_angle)
                    # timear.append(eptime)
                    # *****

                    if(pickp=='unit'):
                        var = 1
                        station[timeid]['P'].append(1 /(var*var))
                        station[timeid]['uereP'].append(1 /(uerep*uerep))
                    if(pickp=='s_el'):
                        a = 0.003
                        b = 0.09
                        s_el = np.sin(m.radians(altitude))
                        var = a + b / (s_el**2)
                        station[timeid]['P'].append((1 /(var)))
                        station[timeid]['uereP'].append((1/((uerep) * (uerep)))*(1 /(var)))
                    station[timeid]['visibility'][name] = round(altitude,2), round(azi_angle,2)


        for tid in station:
            if (station[tid]['counts'] < 4):
                station[tid]['GDOP'] = None
                station[tid]['PDOP'] = None
                station[tid]['HDOP'] = None
                station[tid]['VDOP'] = None
                station[tid]['TDOP'] = None
                station[tid]['Position'] = None
                station[tid]['Vertical'] = None
                station[tid]['Horizontal'] = None
            else:
                Q = station[tid]['Q']
                Qt = np.transpose(Q)
                P = np.diag(station[tid]['P'])
                QX=np.dot(Qt, P)
                QX=np.dot(QX, Q)
                QX = np.linalg.inv(QX)
                tr = QX.diagonal()

                uereP = np.diag(station[tid]['uereP'])
                QX2 = np.dot(Qt, uereP)
                QX2 = np.dot(QX2, Q)
                QX2 = np.linalg.inv(QX2)
                tr2 = QX2.diagonal()

                if ((tr[3]) < 0):
                    TDOP = 0
                else:
                    TDOP = m.sqrt(tr[3])
                az=np.array(station[tid]['az'])
                el=np.array(station[tid]['el'])
                dops = datacal.dops(az, el, m.radians(alt), P)
                dops_accuracy = datacal.dops_accuracy(az, el, m.radians(alt), uereP)
                del station[tid]['Q']
                del station[tid]['P']
                del station[tid]['uereP']
                station[tid]['GDOP'] = round(dops[0], 2)
                station[tid]['PDOP'] = round(dops[1],2)
                station[tid]['HDOP'] = round(dops[2],2)
                station[tid]['VDOP'] = round(dops[3],2)
                station[tid]['TDOP'] = round(TDOP,2)
                station[tid]['Vertical'] = round(dops_accuracy[3],2)
                station[tid]['Horizontal'] = round(dops_accuracy[2],2)
                station[tid]['Position'] = round(dops_accuracy[1],2)

                # *****
                # GDOP.append(round(dops[0], 2))
                # PDOP.append(round(dops[1], 2))
                # HDOP.append(round(dops[2], 2))
                # VDOP.append(round(dops[3], 2))
                # TDOP1.append(round(TDOP,2))
                # VER.append(round(dops_accuracy[3],2))
                # HOR.append(round(dops_accuracy[2],2))
                # POS.append(round(dops_accuracy[1],2))
        # *******
        # CNT=[]
        # for tid in station:
        #     CNT.append(station[tid]['counts'])
        # data = { 'GDOP': GDOP, 'HDOP': HDOP,'PDOP':PDOP,'VDOP': VDOP,'TDOP': TDOP1,'VER': VER,'HOR': HOR,'POS': POS,'COUNTS':CNT}
        # df = pd.DataFrame(data)
        # df.to_csv('data.csv', index=False)

        # ****
        print("success")

        return jsonify(station)
    else:
        datacal.rinexget(obj_time)
        if os.path.exists(file):
            with open(file, 'r') as f:
                nfile_lines = f.readlines()
                f.close()
            satinfo = datacal.rinexcal2(nfile_lines, obj_time, 15)

            station = {}
            for t in range(96):
                time = obj_time + datetime.timedelta(minutes=t * 15)

                time0 = str(time.year) + str(time.month) + str(time.day) + (time.isoformat())[11:13] + (time.isoformat())[14:16]
                station[time0] = {}
                station[time0]['counts'] = 0
                station[time0]['Q'] = []
                station[time0]['P'] = []
                station[time0]['uereP'] = []
                station[time0]['visibility'] = {}
                station[time0]['time'] = time.isoformat()
                station[time0]['az'] = []
                station[time0]['el'] = []

            for name in satinfo:
                if sat_name.find(str(name)) == -1:
                    continue
                for timeid in satinfo[name]:

                    x = float(satinfo[name][timeid]['X_k'])
                    y = float(satinfo[name][timeid]['Y_k'])
                    z = float(satinfo[name][timeid]['Z_k'])
                    blh = [lat, lon, height]
                    blh2 = [np.radians(lat), np.radians(lon), height]
                    xyz = datacal.blh2xyz(blh)
                    xyz2 = pm.geodetic2ecef(blh[0], blh[1], blh[2])
                    X_k1 = x - (xyz2[0])
                    Y_k1 = y - (xyz2[1])
                    Z_k1 = z - (xyz2[2])

                    altitude = (m.pi / 2 - m.acos((m.cos(m.radians(lat)) * (
                            m.cos(m.radians(lon)) * X_k1 + m.sin(
                        m.radians(lon)) * Y_k1) + m.sin(
                        m.radians(lat)) * Z_k1) / m.sqrt(
                        X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)))
                    altitude = np.rad2deg(altitude)

                    azi_angle = m.atan2((-m.sin(m.radians(lon)) * X_k1) + m.cos(m.radians(lon)) * Y_k1,
                                        (-m.sin(m.radians(lat))) * (m.cos(m.radians(lon)) * X_k1 + m.sin(m.radians(lon)) * Y_k1) + m.cos(
                                            m.radians(lat)) * Z_k1)
                    azi_angle = np.rad2deg(azi_angle)
                    if (altitude > alt):
                        cosa = X_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosb = Y_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        cosr = Z_k1 / m.sqrt(X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1)
                        sv_accu = satinfo[name][timeid]['sv_accu']
                        eptime = satinfo[name][timeid]['time']
                        eptime = [eptime.year, eptime.month, eptime.day, eptime.hour, eptime.minute, eptime.second]
                        gtime = UEREcal.epoch2time(eptime)
                        az = np.radians(azi_angle)
                        el = np.radians(altitude)
                        uerep = UEREcal.get_UERE(gtime, blh2, az, el, None, sv_accu)
                        # print(name,eptime,uerep,az,el,blh2)
                        station[timeid]['counts'] += 1
                        station[timeid]['Q'].append([cosa, cosb, cosr, 1])
                        station[timeid]['az'].append(round(m.radians(azi_angle), 2))
                        station[timeid]['el'].append(round(m.radians(altitude), 2))

                        # ****
                        # EL.append(altitude)
                        # AZ.append(azi_angle)
                        # timear.append(eptime)
                        # *****

                        if (pickp == 'unit'):
                            var = 1
                            station[timeid]['P'].append(1 / (var * var))
                            station[timeid]['uereP'].append(1 / (uerep * uerep))
                        if (pickp == 's_el'):
                            a = 0.003
                            b = 0.09
                            s_el = np.sin(m.radians(altitude))
                            var = a + b / (s_el ** 2)
                            station[timeid]['P'].append((1 / (var)))
                            station[timeid]['uereP'].append((1 / ((uerep) * (uerep))) * (1 / (var)))
                        station[timeid]['visibility'][name] = round(altitude, 2), round(azi_angle, 2)

            for tid in station:
                if (station[tid]['counts'] < 4):
                    station[tid]['GDOP'] = None
                    station[tid]['PDOP'] = None
                    station[tid]['HDOP'] = None
                    station[tid]['VDOP'] = None
                    station[tid]['TDOP'] = None
                    station[tid]['Position'] = None
                    station[tid]['Vertical'] = None
                    station[tid]['Horizontal'] = None
                else:
                    Q = station[tid]['Q']
                    Qt = np.transpose(Q)
                    P = np.diag(station[tid]['P'])
                    QX = np.dot(Qt, P)
                    QX = np.dot(QX, Q)
                    QX = np.linalg.inv(QX)
                    tr = QX.diagonal()

                    uereP = np.diag(station[tid]['uereP'])
                    QX2 = np.dot(Qt, uereP)
                    QX2 = np.dot(QX2, Q)
                    QX2 = np.linalg.inv(QX2)
                    tr2 = QX2.diagonal()

                    if ((tr[3]) < 0):
                        TDOP = 0
                    else:
                        TDOP = m.sqrt(tr[3])
                    az = np.array(station[tid]['az'])
                    el = np.array(station[tid]['el'])
                    dops = datacal.dops(az, el, m.radians(alt), P)
                    dops_accuracy = datacal.dops_accuracy(az, el, m.radians(alt), uereP)
                    del station[tid]['Q']
                    del station[tid]['P']
                    del station[tid]['uereP']
                    station[tid]['GDOP'] = round(dops[0], 2)
                    station[tid]['PDOP'] = round(dops[1], 2)
                    station[tid]['HDOP'] = round(dops[2], 2)
                    station[tid]['VDOP'] = round(dops[3], 2)
                    station[tid]['TDOP'] = round(TDOP, 2)
                    station[tid]['Vertical'] = round(dops_accuracy[3], 2)
                    station[tid]['Horizontal'] = round(dops_accuracy[2], 2)
                    station[tid]['Position'] = round(dops_accuracy[1], 2)

                    # *****
                    # GDOP.append(round(dops[0], 2))
                    # PDOP.append(round(dops[1], 2))
                    # HDOP.append(round(dops[2], 2))
                    # VDOP.append(round(dops[3], 2))
                    # TDOP1.append(round(TDOP,2))
                    # VER.append(round(dops_accuracy[3],2))
                    # HOR.append(round(dops_accuracy[2],2))
                    # POS.append(round(dops_accuracy[1],2))
            # *******
            # CNT=[]
            # for tid in station:
            #     CNT.append(station[tid]['counts'])
            # data = { 'GDOP': GDOP, 'HDOP': HDOP,'PDOP':PDOP,'VDOP': VDOP,'TDOP': TDOP1,'VER': VER,'HOR': HOR,'POS': POS,'COUNTS':CNT}
            # df = pd.DataFrame(data)
            # df.to_csv('data.csv', index=False)

            # ****
            print("success")

            return jsonify(station)
        else:
            return 'false'
# IGS VTEC
@app.route('/siteion_igsgim', methods=["POST", "GET"])
def ioncal_igsgim():
    ion_info={}
    tec=[]
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    # print('lon',lon,int((lon + 180) / 5) )
    # print('lat',lat,int(((87.5 - lat) / 2.5)) )
    p = int(int((lon + 180) / 5) + int(((87.5 - lat) / 2.5)) * 73)
    # print('p',p)
    exdate=request.form['date']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    timeid = str(obj_time.year)+str(obj_time.month)+str(obj_time.day)+'0000'
    date = str(exdate)
    filename = './static/ion/' + date + '.' + str(obj_time.year)[2:4] + 'i'
    if os.path.exists(filename):
        with open(filename) as file:
            inx = ionex.reader(file)
            x = []
            y = []
            t = 0

            for ionex_map in inx:
                x.append(t)
                y.append(ionex_map.tec[p])
                # print(ionex_map.tec[p-1],ionex_map.tec[p],ionex_map.tec[p+1])
                t += 4
                ion_info['height']=str(ionex_map.height).strip('\n')[12:15]
            a = interp1d(x, y, kind='cubic')
            for i in range(97):
                tec.append(float(a(i)))
            ion_info['tec']=tec
            file.close()
        print(ion_info)
        return jsonify(ion_info)
    else:
        datacal.ionexget(obj_time)
        if os.path.exists(filename):
            with open(filename) as file:
                inx = ionex.reader(file)
                x = []
                y = []
                t = 0

                for ionex_map in inx:
                    x.append(t)
                    y.append(ionex_map.tec[p])
                    t += 4
                    ion_info['height'] = str(ionex_map.height).strip('\n')[12:15]
                a = interp1d(x, y, kind='cubic')
                for i in range(97):
                    tec.append(float(a(i)))
                ion_info['tec'] = tec
                file.close()
            print(ion_info)
            return jsonify(ion_info)
        else:
            return 'false'

@app.route('/siteion_bdgim', methods=["POST", "GET"])
def ioncal_bdgim():
    ion_info={}
    tec=[]
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    p = int((lon + 180) / 5 + ((87.5 - lat) / 2.5) * 73)
    print(p)
    exdate=request.form['date']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    timeid = str(obj_time.year)+str(obj_time.month)+str(obj_time.day)+'0000'
    date = str(exdate)
    filename = './static/ion/' + date + '.' + str(obj_time.year)[2:4] + 'i'

    x = []
    y = []
    t = 0
    # 提取日期部分
    date = str(obj_time.date())
    nfile_lines=[]
    rinexfile = './static/Rinex/' + date + '.rx'
    if os.path.exists(rinexfile):
        with open(rinexfile, 'r') as f:
            nfile_lines = f.readlines()
            f.close()
    else:
        datacal.rinexget(obj_time)
        if os.path.exists(rinexfile):
            with open(rinexfile, 'r') as f:
                nfile_lines = f.readlines()
                f.close()
        else:
            rinexdata = 'false'
    for i in range(97):
        caltime=obj_time+datetime.timedelta(minutes=15*i)
        # print(caltime)
        import BDGIM
        # 定义非广播电离层参数
        nonBrdData = BDGIM.NonBrdIonData()
        # 定义广播电离层参数
        brdData = BDGIM.BrdIonData()

        # 定义时间参数
        year = caltime.year
        month = caltime.month
        day = caltime.day
        hour =caltime.hour
        minute = caltime.minute
        second = 0

        # 转换时间为MJD
        mjd = BDGIM.UTC2MJD(year, month, day, hour, minute, second)[0]
        # 定义站点和卫星的坐标
        staxyz = pm.geodetic2ecef(lat, lon, 0)
        sta_xyz = [staxyz[0], staxyz[1], staxyz[2]]
        upxyz = pm.geodetic2ecef(lat, lon, 20000)
        sat_xyz = [upxyz[0], upxyz[1], upxyz[2]]
        # 定义广播电离层参数****
        # 解析数据
        brdPara, svid_list = BDGIM.parse_rinex(nfile_lines, caltime)
        # print('定义广播电离层参数:',brdPara)
        # 定义广播电离层参数****


        # 调用IonBdsBrdModel函数计算电离层延迟
        ion_delay, vtec = BDGIM.IonBdsBrdModel(nonBrdData, brdData, mjd, sta_xyz, sat_xyz, brdPara)

        # 打印结果
        # print("B1C频率下的电离层延迟：", ion_delay, "米")
        # print('垂直电子含量：', vtec)
        tec.append(vtec)
    ion_info['tec'] = tec
    print(ion_info)
    return jsonify(ion_info)


@app.route('/keplercal', methods=["POST", "GET"])
def keplercal():

    obj_time = datetime.datetime(2022, 9, 15,00,00,00)
    sattype = 1
    e = float(request.form['e'])
    toe = 345600.0000
    I_0 = np.radians(float(request.form['I_0']))
    OMEGA_DOT = -4.7787704835E-009
    sqrt_A = float(request.form['sqrt_A'])
    OMEGA = np.radians(float(request.form['OMEGA']))
    w = np.radians(float(request.form['w']))
    week = 871
    M0 = np.radians(float(request.form['M0']))
    c_gap = 6.5470254049E-004
    c_v = 4.4104275787E-011
    position_list=[]
    if(sqrt_A >7500):
        k=40
    elif(sqrt_A >6800):
        k=34
    elif (sqrt_A > 6340):
        k = 27
    elif (sqrt_A > 5700):
        k = 23
    else:
        k=19
    negative = 'false'
    positive = 'false'
    bpos=[]
    truepos=[]
    for j in range(k* 4):
        next_time = obj_time + datetime.timedelta(minutes=j * 20)-datetime.timedelta(hours=8)
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
        xyz=datacal.Kepcal(year, month, day, hour, minute, second, toe, sattype, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v)
        XYZ=pm.ecef2eci(xyz[0],xyz[1],xyz[2],next_time)
        # BLH=pm.eci2geodetic(xyz[0],xyz[1],xyz[2],next_time)
        BLH=datacal.XYZ_to_LLA(XYZ[0],XYZ[1],XYZ[2])

        if (day==14 and hour==23 and minute==40):
            truepos=[float(BLH[0]),float(BLH[1]),float(BLH[2])]





        if(BLH[0]<0):
            positive = 'false'
            negative='true'
        elif (BLH[0] > 0):
            positive = 'true'
            # print(BLH)
        if(negative=='true'and positive == 'true'):
            negative = 'false'
            if abs(oldblh[0]) < abs(BLH[0]):
                acendpos=[float(oldblh[0]),float(oldblh[1]),float(oldblh[2])]
            else:
                acendpos = [float(oldblh[0]),float(oldblh[1]),float(oldblh[2])]

        # pm.geodetic2ecef(blh[0], blh[1], blh[2])
        position_list.append(next_time.isoformat() + '+00:00')
        position_list.append(float(XYZ[0]))
        position_list.append(float(XYZ[1]))
        position_list.append(float(XYZ[2]))
        oldblh=BLH
        if(j==0):
            lon0=float(BLH[1])
            bposset = 'True'
        if abs(float(BLH[1]) - lon0)<4 and j>10 and bposset == 'True':
            bposset='False'
        if bposset == 'True':
            bpos.append(float(XYZ[0]))
            bpos.append(float(XYZ[1]))
            bpos.append(float(XYZ[2]))
    end=str(next_time.isoformat())
    doc = []
    # 定义头部
    begin2 = str(datetime.datetime(2022, 9, 15, 00, 00, 00, 00).isoformat())
    begin3 = str(datetime.datetime(2022, 9, 15, 7, 40, 00, 00).isoformat())
    end2=str((datetime.datetime(2022, 9, 15, 00, 00, 00, 00) + datetime.timedelta(hours=24)).isoformat())

    header = {
        'id': "document",
        "version": "1.0",
        "clock": {
            "currentTime": begin3,
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begin2, end2),

        }
    }
    doc.append(header)
    body = {
        "id": 'orbit',
        "availability": '{}/{}'.format(begin2, end),
        "label": {
            "font": "10pt Lucida Console",
            "horizontalOrigin": "LEFT",
            "pixelOffset": {"cartesian2": [-20, -25]},
            "fillColor": {"rgba": [0, 255, 255, 255]},
            "text": '卫星',
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
                    "outlineWidth": 1
                }
            },
            "width": 3,
            "resolution": 120
        },
        # "model": {
        #     "gltf": "/static/models/satellite.glb",
        #     "scale": 20,
        #     "minimumPixelSize": 200,
        #     'maxmumPixelSize': 400,
        #
        # },
        "billboard": {

            "image": "/static/images/hdigso.png",
            "scale": 0.37,

        #     "pixelOffset": {
        #         "cartesian2": [-20, 20]
        # }
        },

        "position": {
            "referenceFrame": 'FIXED',
            "interpolationDegree": 5,
            "interpolationAlgorithm": "LAGRANGE",
            "epoch": begin2,
            "cartesian": position_list
        },
        "polygon": {
            "positions": {
                "interpolationDegree": 5,
                "interpolationAlgorithm": "LAGRANGE",
                "cartesian": bpos
            },
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [26, 98, 167, 120]
                    }
                }
            },
            # "extrudedHeight": 0,
            "perPositionHeight": True,
            # "outline": True,
            # "outlineColor": {
            #     "rgba": [255, 0, 255, 255]
            # }
        }
    }

    doc.append(body)

    with open("./static/czml/keplerorbit2.czml", 'w') as f:
        dump(doc, f)
    return jsonify([doc,acendpos,truepos])

@app.route('/keplercalen', methods=["POST", "GET"])
def keplercalen():
    obj_time = datetime.datetime(2022, 9, 15,00,00,00)
    sattype = 1
    e = float(request.form['e'])
    toe = 345600.0000
    I_0 = np.radians(float(request.form['I_0']))
    OMEGA_DOT = -4.7787704835E-009
    sqrt_A = float(request.form['sqrt_A'])
    OMEGA = np.radians(float(request.form['OMEGA']))
    w = np.radians(float(request.form['w']))
    week = 871
    M0 = np.radians(float(request.form['M0']))
    c_gap = 6.5470254049E-004
    c_v = 4.4104275787E-011
    position_list=[]
    if(sqrt_A >7500):
        k=40
    elif(sqrt_A >6800):
        k=34
    elif (sqrt_A > 6340):
        k = 27
    elif (sqrt_A > 5700):
        k = 23
    else:
        k=19
    negative = 'false'
    positive = 'false'
    for j in range(k* 4):
        next_time = obj_time + datetime.timedelta(minutes=j * 20)-datetime.timedelta(hours=8)
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
        xyz=datacal.Kepcal(year, month, day, hour, minute, second, toe, sattype, sqrt_A, M0, e, w, I_0, OMEGA_DOT, OMEGA, week, c_gap, c_v)
        XYZ=pm.ecef2eci(xyz[0],xyz[1],xyz[2],next_time)
        BLH=pm.eci2geodetic(xyz[0],xyz[1],xyz[2],next_time)
        print(BLH)
        if(BLH[0]<0):
            positive = 'false'
            negative='true'
        elif (BLH[0] > 0):
            positive = 'true'
            # print(BLH)
        if(negative=='true'and positive == 'true'):
            print('stop')
            negative = 'false'
            # closest_to_zero(a, b)
            if abs(oldblh[0]) < abs(BLH[0]):
                print(oldblh)
                acendpos=[float(oldblh[0]),float(oldblh[1]),float(oldblh[2])]
            else:
                print(BLH)
                acendpos = [float(oldblh[0]),float(oldblh[1]),float(oldblh[2])]
        # pm.geodetic2ecef(blh[0], blh[1], blh[2])
        position_list.append(next_time.isoformat() + '+00:00')
        position_list.append(float(XYZ[0]))
        position_list.append(float(XYZ[1]))
        position_list.append(float(XYZ[2]))
        oldblh=BLH
    end=str(next_time.isoformat())
    doc = []
    begin2 = str(datetime.datetime(2022, 9, 15, 00, 00, 00, 00).isoformat())
    begin3 = str(datetime.datetime(2022, 9, 15, 7, 40, 00, 00).isoformat())
    end2=str((datetime.datetime(2022, 9, 15, 00, 00, 00, 00) + datetime.timedelta(hours=24)).isoformat())
    header = {
        'id': "document",
        "version": "1.0",
        "clock": {
            "currentTime": begin3,
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begin2, end2),

        }
    }
    doc.append(header)
    body = {
        "id": 'Kepler orbit',
        "availability": '{}/{}'.format(begin2, end),
        "label": {
            "font": "10pt Lucida Console",
            "horizontalOrigin": "LEFT",
            "pixelOffset": {"cartesian2": [-20, -25]},
            "fillColor": {"rgba": [0, 255, 255, 255]},
            "text": 'satellite',
        },
        "path": {
            "material": {
                "polylineOutline": {
                    "color": {
                        "rgba": [0, 0, 255, 255]
                    },
                    "outlineColor": {
                        "rgba": [0, 0, 0, 255]
                    },
                    "outlineWidth": 1
                }
            },
            "width": 3,
            "resolution": 120
        },
        # "model": {
        #     "gltf": "/static/models/satellite.glb",
        #     "scale": 20,
        #     "minimumPixelSize": 200,
        #     'maxmumPixelSize': 400,
        #
        # },
        "billboard": {
            "image": "/static/images/hdigso.png",
            "scale": 0.37,

        #     "pixelOffset": {
        #         "cartesian2": [-20, 20]
        # }
        },
        "position": {
            "referenceFrame": 'INERTIAL',
            "interpolationDegree": 5,
            "interpolationAlgorithm": "LAGRANGE",
            "epoch": begin2,
            "cartesian": position_list
        }
    }
    doc.append(body)
    return jsonify([doc,acendpos])

@app.route('/satnumsv', methods=["POST", "GET"])
def satnumsview():
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    alt=float(request.form['alt'])
    stationname=str(request.form['name'])

    exdate=request.form['date']
    sat_name=request.form['satname']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    date = str(exdate)
    file='./static/sp3/'+date+'.sp3'

    if os.path.exists(file):
        with open(file, 'r') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            nfile_lines = f.readlines()
            f.close()
        sat_info = {}
        station = {}
        for i in range(len(nfile_lines)):
            if (nfile_lines[i].startswith('*') == True):
                start_num = i
                break
        lines = len(nfile_lines) - start_num
        for i in range(80):
            if (i != 0):
                if (i < 10):
                    i = "0" + str(i)
                sat_info["C" + str(i)] = {}
                sat_info["C" + str(i)]['plist'] = []
                sat_info["C" + str(i)]['begintime'] = []
                sat_info["C" + str(i)]['endtime'] = []
                sat_info["C" + str(i)]['start'] = 0
                sat_info["C" + str(i)]['end'] = 0
        startcount = 0
        for i in range(lines):
            content = nfile_lines[start_num + i]
            if content.find('*') != -1:
                year = int(content[3:7])
                month = int(content[8:10])
                day = int(content[11:13])
                hour = int(content[14:16])
                minute = int(content[17:19])
                time = datetime.datetime(year, month, day, hour, minute)
                czmltime = time - datetime.timedelta(hours=8)
                timeid = str(time.isoformat())
                station[timeid] = {}
                station[timeid]['counts'] = 0
                if(timeid==obj_time.isoformat()):
                    startcount += 1
                    starttime = czmltime.isoformat()
                lasttime = time.isoformat()
                lasttime2=(time+datetime.timedelta(minutes=15)).isoformat()
            elif (content.startswith('PC') == True and startcount != 0 and sat_name.find(str(content[1:4]))!=-1):
                satname = str(content[1:4])
                x = float(content[5:19]) * 1000
                y = float(content[19:33]) * 1000
                z = float(content[33:47]) * 1000
                X, Y, Z = pm.ecef2eci(x, y, z, czmltime)
                sat_info[satname]['plist'].append(czmltime.isoformat() + '+00:00')
                sat_info[satname]['plist'].append(float(X))
                sat_info[satname]['plist'].append(float(Y))
                sat_info[satname]['plist'].append(float(Z))
                blh = [lat, lon, 0]
                xyz = datacal.blh2xyz(blh)
                X_k1 = x - (xyz[0])
                Y_k1 = y - (xyz[1])
                Z_k1 = z - (xyz[2])
                altitude = (m.pi / 2 - m.acos((m.cos(lat * m.pi / 180) * (
                        m.cos(lon * m.pi / 180) * X_k1 + m.sin(
                    lon * m.pi / 180) * Y_k1) + m.sin(
                    lat * m.pi / 180) * Z_k1) / m.sqrt(
                    X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi
                if (altitude > alt):
                    station[timeid]['counts'] += 1
                    sat_info[satname]['start'] += 1
                    sat_info[satname]['end'] = 0
                    if (sat_info[satname]['start'] == 1):
                        sat_info[satname]['begintime'].append(time.isoformat())
                else:
                    sat_info[satname]['start'] = 0
                    sat_info[satname]['end'] += 1
                    if (sat_info[satname]['end'] == 1 and sat_info[satname]['begintime'] !=[]):
                        sat_info[satname]['endtime'].append((time-datetime.timedelta(minutes=15)).isoformat())

        doc = []
        begin = starttime+ '+00:00'
        end = lasttime2
        header = {
            'id': "document",
            "version": "1.0",
            # 'name': name,
            "clock": {
                "multiplier": 900,
                "range": "LOOP_STOP",
                "step": "SYSTEM_CLOCK_MULTIPLIER",
                "interval": '{}/{}'.format(begin, end),

            }
        }
        doc.append(header)
        stationczml = {
            "id": stationname,
            "name": stationname,
            "billboard": {
                "image": {"uri": "../static/images/station.png"},
                "scale": 0.1
            },
            "position": {
                "cartographicDegrees": [lon, lat, 0]
            },
        }
        doc.append(stationczml)


        bg={}
        eg={}

        for sat in sat_info:
            if(sat_info[sat]['begintime']!=[]):
                bg[sat] = sat_info[sat]['begintime']
                eg[sat]=  sat_info[sat]['endtime']


        for sat in sat_info:
            if (len(sat_info[sat]['plist']) != 0):
                if (
                        # IGSO
                        sat == 'C07' or sat == 'C08' or sat == 'C09' or sat == 'C10' or sat == 'C13' or sat == 'C06' or sat == 'C16' or sat == 'C31' or sat == 'C18' or sat == 'C39' or sat == 'C40' or sat == 'C38'):
                    body = {
                        "id": "{}".format(sat),

                        "availability": '{}/{}'.format(begin, end),
                        "path": {
                            "material": {
                                "polylineOutline": {
                                    "color": {
                                        "rgba": [255, 0, 255, 255]
                                    },
                                    # "outlineColor": {
                                    #     "rgba": [0, 0, 0, 255]
                                    # },
                                    "outlineWidth": 2
                                }
                            },
                            "width": 3,
                            "resolution": 120
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
                            "cartesian": sat_info[sat]['plist']
                        }
                    }
                    doc.append(body)
                # GEO
                elif (sat == 'C04' or sat == 'C05' or sat == 'C02' or sat == 'C03' or sat == 'C01' or sat == 'C60' or sat == 'C61' or sat == 'C59'):
                    body = {
                        "id": "{}".format(sat),
                        "availability": '{}/{}'.format(begin, end),

                        "path": {
                            "material": {
                                "polylineOutline": {
                                    "color": {
                                        "rgba": [255, 69, 0, 255]
                                    },
                                    # "outlineColor": {
                                    #     "rgba": [0, 0, 0, 255]
                                    # },
                                    "outlineWidth": 2
                                }
                            },
                            "width": 3,
                            "resolution": 120
                        },
                        "billboard": {
                            "image": "/static/images/hdmeo.png",
                            "scale": 0.37,

                        },
                        "position": {
                            "referenceFrame": "INERTIAL",
                            "interpolationDegree": 5,
                            "interpolationAlgorithm": "LAGRANGE",
                            "epoch": begin,
                            "cartesian": sat_info[sat]['plist']
                        }
                    }
                    doc.append(body)
                else:

                    body = {
                        "id": "{}".format(sat),
                        "availability": '{}/{}'.format(begin, end),
                        "path": {
                            "material": {
                                "polylineOutline": {
                                    "color": {
                                        "rgba": [0, 255, 255, 255]
                                    },
                                    "outlineWidth": 2
                                }
                            },
                            "width": 3,
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
                            "cartesian": sat_info[sat]['plist']
                        }
                    }
                    doc.append(body)

                for i in range(len(sat_info[sat]['begintime'])):
                    gap1 = sat_info[sat]['begintime'][i]
                    if ( i>=len(sat_info[sat]['endtime'])):
                        gap2 = lasttime
                    else:
                        gap2 = sat_info[sat]['endtime'][i]
                    timegap = '{}/{}'.format(gap1, gap2)
                    link = {
                        "id": "{}link".format(sat) + str(i),
                        "availability": timegap,
                        "polyline": {
                            "material": {
                                "polylineGlow": {
                                    "color": {
                                        "rgba": [0, 0, 255, 255]
                                    },
                                    "glowPower": 0.2
                                }
                            },
                            "width": 8,
                            "arcType": "NONE",
                            "positions": {
                                "references": [
                                    sat + "#position", stationname + "#position"
                                ]
                            }
                        }

                    }
                    doc.append(link)
        counts = []
        counts.append(station)
        return jsonify([doc, station])
    else:
        print(file)
        return 'false'

@app.route('/satnumsv2', methods=["POST", "GET"])
def satnumsview2():
    lon=float(request.form['lon'])
    lat = float(request.form['lat'])
    alt=float(request.form['alt'])
    height = float(request.form['height'])
    stationname=str(request.form['name'])
    exdate=request.form['date']
    sat_name=request.form['satname']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    date = str(exdate)
    file = "./static/tle/BDSTLE" + date + ".txt"
    if os.path.exists(file):
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()
    else:
        closedate=datacal.closedata(obj_time, './static/tle')
        file="./static/tle/BDSTLE" + closedate + ".txt"
        with open(file, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()
            f.close()
    sat_info = {}
    station = {}

    for i in range(63):
        if (i != 0):
            if (i < 10):
                i = "0" + str(i)
            sat_info["C" + str(i)] = {}
            sat_info["C" + str(i)]['plist'] = []
            sat_info["C" + str(i)]['begintime'] = []
            sat_info["C" + str(i)]['endtime'] = []
            sat_info["C" + str(i)]['start'] = 0
            sat_info["C" + str(i)]['end'] = 0
    j = 0
    while (j < len(content) - 1):
        name = content[j].strip()
        name = name[-4:-1]

        # if name.startswith('C') == False:
        #     name = 'C62'
        if name=='BEIDOU-3 G4':
            name = 'C62'
        if name=='BEIDOU-3 M25':
            name = 'C63'
            break
        if sat_name.find(str(name)) == -1:
            j += 3
            continue
        line1 = content[j + 1]
        line2 = content[j + 2]
        satellite = twoline2rv(line1, line2, wgs84)
        p_list = []
        for k in range(96):
            next_time2 = obj_time + datetime.timedelta(minutes=k * 15)
            next_time_str2 = next_time2.strftime('%Y %m %d %H %M %S').split(' ')
            next_time_str2 = [int(z) for z in next_time_str2]
            time_key2 = ['year', 'month', 'day', 'hour', 'minute', 'second']
            time_map2 = dict(zip(time_key2, next_time_str2))
            czmltime = next_time2 - datetime.timedelta(hours=8)
            timeid = str(next_time2.isoformat())
            station[timeid] = {}
            station[timeid]['counts'] = 0
            lasttime = next_time2.isoformat()
            lasttime2 = (next_time2 + datetime.timedelta(minutes=15)).isoformat()

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

            X, Y, Z = pm.ecef2eci(x, y, z, czmltime)
            sat_info[name]['plist'].append(czmltime.isoformat() + '+00:00')
            sat_info[name]['plist'].append(float(X))
            sat_info[name]['plist'].append(float(Y))
            sat_info[name]['plist'].append(float(Z))
            blh = [lat, lon, height]
            xyz = pm.geodetic2ecef(blh[0],blh[1],blh[2])
            X_k1 = x - (xyz[0])
            Y_k1 = y - (xyz[1])
            Z_k1 = z - (xyz[2])
            altitude = (m.pi / 2 - m.acos((m.cos(lat * m.pi / 180) * (
                    m.cos(lon * m.pi / 180) * X_k1 + m.sin(
                lon * m.pi / 180) * Y_k1) + m.sin(
                lat * m.pi / 180) * Z_k1) / m.sqrt(
                X_k1 * X_k1 + Y_k1 * Y_k1 + Z_k1 * Z_k1))) * 180 / m.pi
            if (altitude > alt):
                station[timeid]['counts'] += 1

                sat_info[name]['start'] += 1
                sat_info[name]['end'] = 0
                if (sat_info[name]['start'] == 1):
                    sat_info[name]['begintime'].append(next_time2.isoformat())
            else:

                sat_info[name]['start'] = 0
                sat_info[name]['end'] += 1

                if (sat_info[name]['end'] == 1 and sat_info[name]['begintime'] != []):
                    sat_info[name]['endtime'].append((next_time2 - datetime.timedelta(minutes=15)).isoformat())
        j += 3

    doc = []
    starttime = (obj_time - datetime.timedelta(hours=8)).isoformat()
    lasttime2 = (obj_time + datetime.timedelta(minutes=15*96)).isoformat()
    begin = starttime + '+00:00'
    end = lasttime2
    header = {
        'id': "document",
        "version": "1.0",
        "clock": {
            "multiplier": 900,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "interval": '{}/{}'.format(begin, end),

        }
    }
    doc.append(header)
    stationczml = {
        "id": stationname,
        "name": stationname,
        "label": {

            "font": "6pt Lucida Console",
            "outlineWidth": 2,
            "outlineColor": {"rgba": [255, 0, 0, 255]},
            "horizontalOrigin": "LEFT",
            "pixelOffset": {"cartesian2": [12, 0]},
            "fillColor": {"rgba": [213, 255, 0, 255]},
            "text": stationname
        },
        "billboard": {
            "image": {"uri": "../static/images/station.png"},
            "scale": 0.1
        },
        # "model": {
        #     "gltf": "/static/models/ground_satellite_station_i.glb",
        #     "scale": 8,
        #     "minimumPixelSize": 0,
        #     'maxmumPixelSize': 100,
        #
        # },
        "position": {
            "cartographicDegrees": [lon, lat, 0]
        },
    }
    doc.append(stationczml)

    bg = {}
    eg = {}

    for sat in sat_info:
        if (sat_info[sat]['begintime'] != []):
            bg[sat] = sat_info[sat]['begintime']
            eg[sat] = sat_info[sat]['endtime']


    for sat in sat_info:
        if (len(sat_info[sat]['plist']) != 0):
            if (
                    # IGSO
                    sat == 'C07' or sat == 'C08' or sat == 'C09' or sat == 'C10' or sat == 'C13' or sat == 'C06' or sat == 'C16' or sat == 'C31' or sat == 'C18' or sat == 'C39' or sat == 'C40' or sat == 'C38'or sat == 'C56'):
                body = {
                    "id": "{}".format(sat),

                    "availability": '{}/{}'.format(begin, end),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [255, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 14]},
                        "fillColor": {"rgba": [213, 255, 0, 255]},
                        "text": sat,
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
                    # "model": {
                    #     "gltf": "/static/models/satellite.glb",
                    #     "scale": 8,
                    #     "minimumPixelSize": 0,
                    #     'maxmumPixelSize': 100,
                    #
                    # },
                    "billboard": {
                        "image": "/static/images/hdigso.png",
                        "scale": 0.37
                    },
                    "position": {
                        "referenceFrame": 'INERTIAL',
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begin,
                        "cartesian": sat_info[sat]['plist']
                    }
                }
                doc.append(body)
            # GEO
            elif (
                    sat == 'C04' or sat == 'C05' or sat == 'C02' or sat == 'C03' or sat == 'C01' or sat == 'C60' or sat == 'C61' or sat == 'C59' or sat == 'C62'):
                body = {
                    "id": "{}".format(sat),
                    "availability": '{}/{}'.format(begin, end),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 12]},
                        "fillColor": {"rgba": [213, 255, 0, 255]},
                        "text": sat
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
                        "image": "/static/images/hdmeo.png",
                        "scale": 0.37,

                    },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begin,
                        "cartesian": sat_info[sat]['plist']
                    }
                }
                doc.append(body)
            else:

                body = {
                    "id": "{}".format(sat),
                    "availability": '{}/{}'.format(begin, end),
                    "label": {
                        "font": "6pt Lucida Console",
                        "outlineWidth": 2,
                        "outlineColor": {"rgba": [0, 0, 0, 255]},
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {"cartesian2": [20, 12]},
                        "fillColor": {"rgba": [213, 255, 0, 255]},
                        "text": sat
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
                    "billboard": {
                        "image": "/static/images/hdmeo.png",
                        "scale": 0.37
                    },
                    "position": {
                        "referenceFrame": "INERTIAL",
                        "interpolationDegree": 5,
                        "interpolationAlgorithm": "LAGRANGE",
                        "epoch": begin,
                        "cartesian": sat_info[sat]['plist']
                    }
                }
                doc.append(body)

            for i in range(len(sat_info[sat]['begintime'])):
                gap1 = sat_info[sat]['begintime'][i]
                if (i >= len(sat_info[sat]['endtime'])):
                    gap2 = lasttime
                else:
                    gap2 = sat_info[sat]['endtime'][i]
                timegap = '{}/{}'.format(gap1, gap2)
                link = {
                    "id": "{}link".format(sat) + str(i),
                    "availability": timegap,
                    "polyline": {
                        "material": {
                            "polylineGlow": {
                                "color": {
                                    "rgba": [0, 0, 255, 255]
                                },
                                "glowPower": 0.2
                            }
                        },
                        "width": 8,
                        "arcType": "NONE",
                        "positions": {
                            "references": [
                                sat + "#position", stationname + "#position"
                            ]
                        }
                    }

                }
                doc.append(link)
    counts = []
    counts.append(station)
    return jsonify([doc, station])
@app.route('/calorbits', methods=["POST", "GET"])
def calorbit():

    exdate=request.form['date']
    obj_time=datetime.datetime(int(exdate.strip()[0:4]),int(exdate.strip()[5:7]),int(exdate.strip()[8:10]),0,0)
    date = str(exdate)
    tstep=int(request.form['tstep'])

    print(date)
    print(tstep)
    # Rinex ***
    rinexfile = './static/Rinex/' + date + '.rx'
    if os.path.exists(rinexfile):
        with open(rinexfile, 'r') as f:
            nfile_lines = f.readlines()
            f.close()
        rinexdata=datacal.rinexcal3(nfile_lines, obj_time,tstep)
    else:
        datacal.rinexget(obj_time)
        if os.path.exists(rinexfile):
            with open(rinexfile, 'r') as f:
                nfile_lines = f.readlines()
                f.close()
            rinexdata = datacal.rinexcal3(nfile_lines, obj_time, tstep)
        else:
            rinexdata='false'
    # Rinex ***
    # SP3 ***
    sp3file = './static/sp3/' + date + '.sp3'
    if os.path.exists(sp3file):
        with open(sp3file, 'r') as f:
            nfile_lines = f.readlines()
            f.close()
        sp3data=datacal.sp3cal2(nfile_lines,obj_time)
    else:
        datacal.sp3get2(obj_time)
        if os.path.exists(sp3file):
            with open(sp3file, 'r') as f:
                nfile_lines = f.readlines()
                f.close()
            sp3data = datacal.sp3cal2(nfile_lines, obj_time)
        else:
            sp3data='false'
    # SP3 ***
    # Yuma ***
    yumafile1 = './static/YUMA/' + date + '-c.alc'
    yumafile2 = './static/YUMA/' + date + '-t.alc'
    if os.path.exists(yumafile1):
        print('打开C')
        with open(yumafile1, 'r') as f:
            content = f.readlines()
            f.close()
        yumadate=datacal.yumacal2(content, obj_time,"c",tstep)
    elif os.path.exists(yumafile2):
        print('打开T')
        with open(yumafile2, 'r') as f:
            content = f.readlines()
            f.close()
        yumadate=datacal.yumacal2(content, obj_time,'t',tstep)
    else:
        datacal.yumaget(obj_time)
        if os.path.exists(yumafile1):
            with open(yumafile1, 'r') as f:
                content = f.readlines()
                f.close()
            yumadate = datacal.yumacal2(content, obj_time, "c", tstep)
        elif os.path.exists(yumafile2):
            with open(yumafile2, 'r') as f:
                content = f.readlines()
                f.close()
            yumadate = datacal.yumacal2(content, obj_time, 't', tstep)
        else:
            yumadate = 'false'
    # Yuma ***
    # TLE ***
    tlefile='./static/tle/BDSTLE'+date+'.txt'
    if os.path.exists(tlefile):
        with open(tlefile, 'r') as f:
            content = f.readlines()  
            f.close()
        tledata=datacal.tlecal3(content,obj_time,tstep)
    else:
        closedate=datacal.closedata(obj_time, './static/tle')
        tlefile="./static/tle/BDSTLE" + closedate + ".txt"
        with open(tlefile, 'rt') as f:
            if f == 0:
                print("can not open file")
            else:
                print("success")
            content = f.readlines()  
            f.close()
        tledata = datacal.tlecal3(content, obj_time, tstep)
        # tledata='false'
    # TLE ***
    return jsonify([rinexdata,sp3data,yumadate,tledata])
if __name__ == '__main__':
    # app.run()
    app.run(app.run(host='0.0.0.0',port=83))