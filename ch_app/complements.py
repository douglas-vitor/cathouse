import requests
from ch_app import models
import json
import logging

logger = logging.getLogger(__file__)


""""
Funções de complemento para as views
"""

def powerReles(action=None, ip=None):
    if action == 'ON' and len(action) == 2:
        try:
            if len(ip) <= 15 and len(ip) >= 7:
                requests.get("http://" + ip + "/cm?cmnd=Power%20On", timeout=2)
        except:
            return
    elif action == 'OFF' and len(action) == 3:
        try:
            if len(ip) <= 15 and len(ip) >= 7:
                requests.get("http://" + ip + "/cm?cmnd=Power%20Off", timeout=2)
        except:
            return
    else:
        return

def allLights(action=None):
    if action == 'START' and len(action) == 5:
        for rAll in models.R_wifi.objects.filter(type="LUZ"):
            try:
                requests.get("http://" + rAll.ip + "/cm?cmnd=Power%20On", timeout=2)
            except:
                pass
    return

def statusReles(type):
    statustrava = {}
    if len(type) <= 6:
        for t in models.R_wifi.objects.filter(type=type):
            try:
                checkStatusTrava = requests.get("http://" + t.ip + "/cm?cmnd=Power", timeout=2)
                decodeTrava = json.loads(checkStatusTrava.content.decode('utf-8'))['POWER']
                statustrava[t.ip] = decodeTrava
            except:
                pass
    return statustrava

def showTemp():
    temperatura = {}
    for t in models.Sensor_wifi.objects.all():
        try:
            checkTemp = requests.get("http://" + t.ip + "/cm?cmnd=status%208", timeout=2)
            decodeTemp = json.loads(checkTemp.content.decode('utf-8'))['StatusSNS']['DHT11']['Temperature']
            temperatura[t.ip] = decodeTemp
        except:
            pass
    return temperatura

def showHumid():
    humidade = {}
    for h in models.Sensor_wifi.objects.all():
        try:
            checkHumid = requests.get("http://" + h.ip + "/cm?cmnd=status%208", timeout=2)
            decodeHumid = json.loads(checkHumid.content.decode('utf-8'))['StatusSNS']['DHT11']['Humidity']
            humidade[h.ip] = decodeHumid
        except:
            pass
    return humidade

def mediaTemp():
    temp_sensores = models.Sensor_wifi.objects.all()
    somaTemp = 0.0
    for s in temp_sensores:
        try:
            tempstatus = requests.get("http://" + s.ip + "/cm?cmnd=status%208", timeout=2)
            temp_decode = json.loads(tempstatus.content.decode('utf-8'))['StatusSNS']['DHT11']['Temperature']
            currentTemp = temp_decode
            somaTemp += currentTemp
        except:
            pass
    try:
        mediaTemp = somaTemp / temp_sensores.count()
    except:
        mediaTemp = 0
    return mediaTemp

def createAlarm(recThing, 
                recClock, 
                recAction, 
                recActive, 
                recRepeat,
                recDom,
                recSeg,
                recTer,
                recQua,
                recQui,
                recSex,
                recSab):
    if recThing and recClock and recAction and recActive and recRepeat:
        thing = recThing
        clock = recClock
        action = recAction

        dom = recDom
        seg = recSeg
        ter = recTer
        qua = recQua
        qui = recQui
        sex = recSex
        sab = recSab
        days = dom + seg + ter + qua + qui + sex + sab


        if (len(recThing) <= 15 and len(recThing) > 0) and (len(recClock) <= 5 and len(recClock) > 0) and (len(recAction) <= 3 and len(recAction) > 0) and (len(recActive) <= 3 and len(recActive) > 0) and (len(recRepeat) <= 3 and len(recRepeat) > 0) and len(days) == 7:
            pass
        else:
            return

        arm = ''
        repeat = ''
        action = ''
        nameAction = ''
        if recActive == 'yes': arm = 1
        if recActive == 'no': arm = 0

        if recRepeat == 'yes': repeat = 1
        if recRepeat == 'no': repeat = 0

        if recAction == 'on':
            action = 1
            nameAction = 'Ligar'
        if recAction == 'off':
            action = 0
            nameAction = 'Desligar'

        searchTypeOfThing = ''
        searchNameOfThing = ''
        for item in models.R_wifi.objects.filter(rw=recThing):
            searchNameOfThing = item.name.lower()
            if item.type == "LUZ":
                searchTypeOfThing = 'lâmpada'
            else:
                searchTypeOfThing = item.type.lower()

        timerName = ''
        timerCount = 1
        timerCreate = False
        timerUpdate = False
        countTimers = models.Timer.objects.filter(ip=recThing).count()
        countTimerNA = models.Timer.objects.filter(ip=recThing, time='na').count()
        if countTimers == 0:
            timerName = 'timer1'
            timerCreate = True
        elif countTimers > 0 and countTimers <= 10:
            if countTimerNA > 0:
                for seq in range(9):
                    timerName = 'timer' + str(timerCount)
                    if models.Timer.objects.filter(ip=recThing, time='na', name=timerName).count() > 0:
                        timerName = 'timer' + str(timerCount)
                        timerUpdate = True
                        break
                    else:
                        timerCount += 1
            else:
                for s in range(9):
                    timerName = 'timer' + str(timerCount)
                    if models.Timer.objects.filter(ip=recThing, name=timerName).count() == 0:
                        timerName = 'timer' + str(timerCount)
                        timerCreate = True
                        break
                    else:
                        timerCount += 1

        cmd = timerName+'{"Arm":'+str(arm)+',"Enable":'+str(arm)+',"Time":'+"'"+clock+"'"+',"Window":0,"Days":'+days+',"Repeat":'+str(repeat)+',"Output":1,"Action":'+str(action)+'}'
        if timerCreate == True:
            try:
                name_for_user = nameAction + ' ' + searchTypeOfThing + ' ' + searchNameOfThing
                models.Timer.objects.create(arm=arm, time=clock, window="0", days=days, repeat_timer=repeat, output="1", action=action, ip=thing, name=timerName, name_for_user=name_for_user)
            except:
                pass

        if timerUpdate == True:
            try:
                name_for_user = nameAction + ' ' + searchTypeOfThing + ' ' + searchNameOfThing
                models.Timer.objects.filter(ip=recThing, time='na', name=timerName).update(arm=arm, time=clock, window="0", days=days, repeat_timer=repeat, output="1", action=action, ip=thing, name=timerName, name_for_user=name_for_user)
            except:
                pass

        try:
            requests.get("http://" + thing + "/cm?cmnd=" + cmd, timeout=2)
        except:
            pass
    return

def updateAlarm(recActive, recIp, recTimer, recRepeat):
    if recActive and recIp and recTimer and recRepeat:
        alarm_ativar = ''
        alarm_repeat = ''
        if recActive == 'yes': alarm_ativar = 1
        if recActive == 'no': alarm_ativar = 0
        if recRepeat == 'yes': alarm_repeat = 1
        if recRepeat == 'no': alarm_repeat = 0

        if len(recIp) <= 15 and len(recIp) >= 7:
            pass
        else:
            return

        alarmBD = models.Timer.objects.filter(ip=recIp, name=recTimer)
        for data in alarmBD:
            cmd = data.name+'{"Arm":'+str(alarm_ativar)+',"Enable":'+str(alarm_ativar)+',"Time":'+"'"+data.time+"'"+',"Window":0,"Days":'+data.days+',"Repeat":'+str(alarm_repeat)+',"Output":1,"Action":'+str(data.action)+'}'

        try:
            models.Timer.objects.filter(ip=recIp, name=recTimer).update(arm=alarm_ativar, repeat_timer=alarm_repeat)
            requests.get("http://" + recIp + "/cm?cmnd=" + cmd, timeout=2)
        except:
            pass
        return
    return

def dellAlarm(recTime, recId, recIp, recTimer):
    if recTime and recId and recIp and recTimer:
        if len(recIp) <= 15 and len(recIp) >= 7:
            pass
        else:
            return
        alarmBD = models.Timer.objects.filter(ip=recIp, name=recTimer)
        for data in alarmBD:
            cmd = data.name+'{"Arm":0,"Enable":0,"Time":'+"'"+data.time+"'"+',"Window":0,"Days":'+data.days+',"Repeat":0,"Output":1,"Action":'+str(data.action)+'}'

        try:
            models.Timer.objects.filter(ip=recIp, name=recTimer).update(time='na')
            requests.get("http://" + recIp + "/cm?cmnd=" + cmd, timeout=2)
        except:
            pass
    return

def powerDimmer(setRange=None, ip=None):
    if ip and setRange and len(ip) <= 15 and len(ip) >= 7 and int(setRange) >= 0 and int(setRange) <= 100:
        try:
            requests.get("http://" + ip + "/cm?cmnd=Dimmer%20" + setRange, timeout=2)
        except Exception:
            logger.exception("Não foi possivel se comunicar com o dimmer.")
            return

    return

def statusPercentDimmer():
    dimmers_percent = {}
    for d in models.R_wifi.objects.filter(type2='DIMMER'):
        try:
            checkDimmer = requests.get("http://" + d.ip + "/cm?cmnd=Dimmer", timeout=2)
            decodeDimmer = json.loads(checkDimmer.content.decode('utf-8'))["Dimmer"]
            dimmers_percent[d.ip] = decodeDimmer
        except Exception:
            logger.exception("Chamada para o dimmer falhou.")
            pass

    return dimmers_percent

def statusRGB():
    rgbs_status = {}
    for rgb in models.R_wifi.objects.filter(type2='RGB'):
        try:
            checkRgb = request.get("http://" + rgb.ip + "/json/state", timeout=2)
            #decodeRgb = json.loads(checkRgb.content.decode('utf-8'))
            rgbs_status[rgb.ip] = checkRgb
            
        except:
            pass
    
    return rgbs_status

