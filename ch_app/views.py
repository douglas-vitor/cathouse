from django.shortcuts import render
from ch_app import models

import requests
import json
from django.http import HttpResponseRedirect
import logging
from .complements import powerReles
from .complements import allLights
from .complements import statusReles
from .complements import mediaTemp
from .complements import showTemp
from .complements import showHumid
from .complements import createAlarm
from .complements import updateAlarm
from .complements import dellAlarm


logger = logging.getLogger(__file__)


def index(req):
	return

def home(req):
	if req.user.is_authenticated:
		if req.POST:
			try:
				allLights(req.POST['action'])
			except:
				pass
			try:
				powerReles(req.POST['action'], req.POST['ip'])
			except:
				pass

		statuslight = statusReles(type="LUZ")
		statustrava = statusReles(type="TRAVA")

		luzes = models.R_wifi.objects.filter(type="LUZ")
		travas = models.R_wifi.objects.filter(type="TRAVA")
		cams = models.R_wifi.objects.filter(type="CAM")

		mediaTemp()

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
		temperatura = showTemp()
		humidade = showHumid()

		sensores = models.Sensor_wifi.objects.all()

		return render(req, 'temp.html', {'sensores': sensores,
						'temperatura': temperatura,
						'humidade': humidade})
	else:
		return HttpResponseRedirect("/login")


def tomada(req):
	if req.user.is_authenticated:
		if req.POST:
			powerReles(req.POST['action'], req.POST['ip'])

		statustomada = statusReles(type="TOMADA")

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
			createAlarm(
				recThing=req.POST['thing'], 
				recClock=req.POST['clock'], 
				recAction=req.POST['action'], 
				recActive=req.POST['hidden_ativar1'], 
				recRepeat=req.POST['hidden_repetir1'],
				recDom = req.POST.get('dom', '-'),
				recSeg = req.POST.get('seg', '-'),
				recTer = req.POST.get('ter', '-'),
				recQua = req.POST.get('qua', '-'),
				recQui = req.POST.get('qui', '-'),
				recSex = req.POST.get('sex', '-'),
				recSab = req.POST.get('sab', '-')
				)


		alarms = models.Timer.objects.all().exclude(time="na")
		things = models.R_wifi.objects.all()
		return render(req, 'agendamento.html', {'alarms': alarms, 'things': things})
	else:
		return HttpResponseRedirect("/login")


def updatealarm(req, id):
	if req.user.is_authenticated:
		if id:
			updateAlarm(
				recActive=req.POST['hidden_alarm_ativar'],
				recIp=req.POST['ip'],
				recTimer=req.POST['timer'],
				recRepeat=req.POST['hidden_alarm_repetir']
				)
		else:
			pass

		return HttpResponseRedirect("/agendamento")
	else:
		return HttpResponseRedirect("/login")


def dellalarm(req, id):
	if req.user.is_authenticated:
		if id:
			dellAlarm(
				recTime=req.POST['time'],
				recId=req.POST['id'],
				recIp=req.POST['ip'],
				recTimer=req.POST['timer']
			)
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

	
