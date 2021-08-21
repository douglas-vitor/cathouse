from django.shortcuts import render
from django.http import HttpResponse
from ch_app import models

import requests
import json
from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__file__)


def index(req):
	return

def home(req):
	if req.user.is_authenticated:
		if req.POST:
			if req.POST['action'] == 'ON':
				try:
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=Power%20On", timeout=2)
				except:
					pass
			elif req.POST['action'] == 'OFF':
				try:
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=Power%20Off", timeout=2)
				except:
					pass
			elif req.POST['action'] == 'START':
				for rAll in models.R_wifi.objects.filter(type="LUZ"):
					try:
						requests.get("http://" + rAll.ip + "/cm?cmnd=Power%20On", timeout=2)
					except:
						pass
			else:
				pass



		statuslight = {}

		for r in models.R_wifi.objects.filter(type="LUZ"):
			try:
				checkStatus = requests.get("http://" + r.ip + "/cm?cmnd=Power", timeout=2)
				decode = json.loads(checkStatus.content.decode('utf-8'))['POWER']
				statuslight[r.ip] = decode
			except:
				pass

		statustrava = {}

		for t in models.R_wifi.objects.filter(type="TRAVA"):
			try:
				checkStatusTrava = requests.get("http://" + t.ip + "/cm?cmnd=Power", timeout=2)
				decodeTrava = json.loads(checkStatusTrava.content.decode('utf-8'))['POWER']
				statustrava[t.ip] = decodeTrava
			except:
				pass


		luzes = models.R_wifi.objects.filter(type="LUZ")
		travas = models.R_wifi.objects.filter(type="TRAVA")
		cams = models.R_wifi.objects.filter(type="CAM")

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
		mediaTemp = somaTemp / temp_sensores.count()


		return render(req, 'home.html', {'luzes': luzes,
						'travas': travas,
						'cameras': cams,
						'statuslight': statuslight,
						'tempMedia': mediaTemp,
						'statustrava': statustrava})
	else:
		return HttpResponseRedirect("/login")


def temp(req):
	if req.user.is_authenticated:
		temperatura = {}

		for t in models.Sensor_wifi.objects.all():
			try:
				checkTemp = requests.get("http://" + t.ip + "/cm?cmnd=status%208", timeout=2)
				decodeTemp = json.loads(checkTemp.content.decode('utf-8'))['StatusSNS']['DHT11']['Temperature']
				temperatura[t.ip] = decodeTemp
			except:
				pass

		humidade = {}

		for h in models.Sensor_wifi.objects.all():
			try:
				checkHumid = requests.get("http://" + h.ip + "/cm?cmnd=status%208", timeout=2)
				decodeHumid = json.loads(checkHumid.content.decode('utf-8'))['StatusSNS']['DHT11']['Humidity']
				humidade[h.ip] = decodeHumid
			except:
				pass

		sensores = models.Sensor_wifi.objects.all()

		return render(req, 'temp.html', {'sensores': sensores,
						'temperatura': temperatura,
						'humidade': humidade})
	else:
		return HttpResponseRedirect("/login")


def tomada(req):
	if req.user.is_authenticated:
		if req.POST:
			if req.POST['action'] == 'ON':
				try:
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=Power%20On", timeout=2)
				except:
					pass
			elif req.POST['action'] == 'OFF':
				try:
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=Power%20Off", timeout=2)
				except:
					pass
			else:
				pass


		statustomada = {}

		for t in models.R_wifi.objects.filter(type="TOMADA"):
			try:
				checkStatus = requests.get("http://" + t.ip + "/cm?cmnd=Power", timeout=2)
				decode = json.loads(checkStatus.content.decode('utf-8'))['POWER']
				statustomada[t.ip] = decode
			except:
				pass

		tomadas = models.R_wifi.objects.filter(type="TOMADA")

		return render(req, 'tomada.html', {'tomadas': tomadas,
							'statustomada': statustomada})
	else:
		return HttpResponseRedirect("/login")


def camera(req):
	if req.user.is_authenticated:
		return render(req, 'camera.html')
	else:
		return HttpResponseRedirect("/login")


def agendamento(req):
	if req.user.is_authenticated:
		if req.POST:
			if req.POST['thing'] and req.POST['clock'] and req.POST['action'] and req.POST['hidden_ativar1'] and req.POST['hidden_repetir1']:
				thing = req.POST['thing']
				clock = req.POST['clock']
				action = req.POST['action']

				dom = req.POST.get('dom', '-')
				seg = req.POST.get('seg', '-')
				ter = req.POST.get('ter', '-')
				qua = req.POST.get('qua', '-')
				qui = req.POST.get('qui', '-')
				sex = req.POST.get('sex', '-')
				sab = req.POST.get('sab', '-')
				days = dom + seg + ter + qua + qui + sex + sab

				arm = ''
				repeat = ''
				action = ''
				nameAction = ''
				if req.POST['hidden_ativar1'] == 'yes': arm = 1
				if req.POST['hidden_ativar1'] == 'no': arm = 0

				if req.POST['hidden_repetir1'] == 'yes': repeat = 1
				if req.POST['hidden_repetir1'] == 'no': repeat = 0

				if req.POST['action'] == 'on':
					action = 1
					nameAction = 'Ligar'
				if req.POST['action'] == 'off':
					action = 0
					nameAction = 'Desligar'

				searchTypeOfThing = ''
				searchNameOfThing = ''
				for item in models.R_wifi.objects.filter(rw=req.POST['thing']):
					searchNameOfThing = item.name.lower()
					if item.type == "LUZ":
						searchTypeOfThing = 'lâmpada'
					else:
						searchTypeOfThing = item.type.lower()

				timerName = ''
				timerCount = 1
				timerCreate = False
				timerUpdate = False
				countTimers = models.Timer.objects.filter(ip=req.POST['thing']).count()
				countTimerNA = models.Timer.objects.filter(ip=req.POST['thing'], time='na').count()
				if countTimers == 0:
					timerName = 'timer1'
					timerCreate = True
				elif countTimers > 0 and countTimers <= 10:
					if countTimerNA > 0:
						for seq in range(9):
							timerName = 'timer' + str(timerCount)
							if models.Timer.objects.filter(ip=req.POST['thing'], time='na', name=timerName).count() > 0:
								timerName = 'timer' + str(timerCount)
								timerUpdate = True
								break
							else:
								timerCount += 1
					else:
						for s in range(9):
							timerName = 'timer' + str(timerCount)
							if models.Timer.objects.filter(ip=req.POST['thing'], name=timerName).count() == 0:
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
						models.Timer.objects.filter(ip=req.POST['thing'], time='na', name=timerName).update(arm=arm, time=clock, window="0", days=days, repeat_timer=repeat, output="1", action=action, ip=thing, name=timerName, name_for_user=name_for_user)
					except:
						pass

				try:
					requests.get("http://" + thing + "/cm?cmnd=" + cmd, timeout=2)
				except:
					pass


		alarms = models.Timer.objects.all().exclude(time="na")
		things = models.R_wifi.objects.all()
		return render(req, 'agendamento.html', {'alarms': alarms, 'things': things})
	else:
		return HttpResponseRedirect("/login")


def updatealarm(req, id):
	if req.user.is_authenticated:
		if id:
			if req.POST['hidden_alarm_ativar'] and req.POST['ip'] and req.POST['timer'] and req.POST['hidden_alarm_repetir']:
				alarm_ativar = ''
				alarm_repeat = ''
				if req.POST['hidden_alarm_ativar'] == 'yes': alarm_ativar = 1
				if req.POST['hidden_alarm_ativar'] == 'no': alarm_ativar = 0
				if req.POST['hidden_alarm_repetir'] == 'yes': alarm_repeat = 1
				if req.POST['hidden_alarm_repetir'] == 'no': alarm_repeat = 0

				alarmBD = models.Timer.objects.filter(ip=req.POST['ip'], name=req.POST['timer'])
				for data in alarmBD:
					cmd = data.name+'{"Arm":'+str(alarm_ativar)+',"Enable":'+str(alarm_ativar)+',"Time":'+"'"+data.time+"'"+',"Window":0,"Days":'+data.days+',"Repeat":'+str(alarm_repeat)+',"Output":1,"Action":'+str(data.action)+'}'

				try:
					models.Timer.objects.filter(ip=req.POST['ip'], name=req.POST['timer']).update(arm=alarm_ativar, repeat_timer=alarm_repeat)
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=" + cmd, timeout=2)
				except:
					pass
		else:
			pass

		return HttpResponseRedirect("/agendamento")
	else:
		return HttpResponseRedirect("/login")


def dellalarm(req, id):
	if req.user.is_authenticated:
		if id:
			if req.POST['time'] and req.POST['id'] and req.POST['ip'] and req.POST['timer']:
				alarmBD = models.Timer.objects.filter(ip=req.POST['ip'], name=req.POST['timer'])
				for data in alarmBD:
					cmd = data.name+'{"Arm":0,"Enable":0,"Time":'+"'"+data.time+"'"+',"Window":0,"Days":'+data.days+',"Repeat":0,"Output":1,"Action":'+str(data.action)+'}'

				try:
					models.Timer.objects.filter(ip=req.POST['ip'], name=req.POST['timer']).update(time='na')
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=" + cmd, timeout=2)
				except:
					pass

		else:
			pass

		return HttpResponseRedirect("/agendamento")
	else:
		return HttpResponseRedirect("/login")


def dimmer(req):
	if req.user.is_authenticated:
		if req.POST:
			if req.POST['ip'] and req.POST['range']:
				try:
					requests.get("http://" + req.POST['ip'] + "/cm?cmnd=Dimmer%20" + req.POST['range'], timeout=2)
				except Exception:
					logger.exception("Não foi possivel se comunicar com o dimmer.")
					pass


		dimmers = models.R_wifi.objects.filter(type2='DIMMER')

		dimmers_percent = {}
		for d in dimmers:
			try:
				checkDimmer = requests.get("http://" + d.ip + "/cm?cmnd=Dimmer", timeout=2)
				decodeDimmer = json.loads(checkDimmer.content.decode('utf-8'))["Dimmer"]
				dimmers_percent[d.ip] = decodeDimmer
			except Exception:
				logger.exception("Chamada para o dimmer falhou.")
				pass

		return render(req, 'dimmer.html', {'dimmers': dimmers, 'current_state': dimmers_percent})
	else:
		return HttpResponseRedirect("/login")


def rgb(req):
	if req.user.is_authenticated:
		rgbs = models.R_wifi.objects.filter(type2='RGB')
		return render(req, 'rgb.html', {'rgbs': rgbs})
	else:
		return HttpResponseRedirect("/login")

	
