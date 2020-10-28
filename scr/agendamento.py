# -*- coding: utf-8 -*-

import datetime,time,requests
from time import process_time
import RPi.GPIO as GPIO
from config import Config
from pi.leitura_tag import ler

def reles(acesso):
    try:
        if acesso:
            GPIO.output(pino_rele_1,1)
            GPIO.output(pino_rele_2,1)
        elif not acesso:
            GPIO.output(pino_rele_1,1)
            GPIO.output(pino_rele_2,0)
        elif acesso == 3:
            GPIO.output(pino_rele_1,0)
            GPIO.output(pino_rele_2,0)
    except Exception as e:
        raise e


def time_atual():
    data = datetime.datetime.today()

    data_atual = str(data.year) + '-' + str(data.month) + '-' + str(data.day)

    hora_atual = str(data.hour) + ':' + str(data.minute)

    return data_atual,hora_atual

def enviar_feedback(tag):
    try:
        requests.post(conf.HOST + '/feedback/' + tag)
    except Exception as e:
        raise e

pino_rele_1 = 20 # pino rele 1
pino_rele_2 = 21 # pino rele 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(pino_rele_1, GPIO.OUT)
GPIO.setup(pino_rele_2, GPIO.OUT)

conf = Config()

reles(3)

while True:
    try:
        tag,_ = ler()

        response = requests.get(conf.HOST + '/tag/agendamento/' + tag)  # pegar agendamento
        agendamento = response.json()
        print(agendamento)

        data_atual,hora_atual  = time_atual()

        if agendamento['acesso'] and agendamento['data'] == data_atual and agendamento['hora'] == hora_atual:
            print('acesso 1')
            while agendamento['hora_final'] == hora_atual:
                reles(1)
                time.sleep(60)
                _,hora_atual = time_atual()
            reles(3)
            enviar_feedback(tag)

        elif not agendamento['acesso'] and agendamento['data'] == data_atual and agendamento['hora'] == hora_atual:
            print('acesso 0')
            while agendamento['hora_final'] == hora_atual:
                reles(0)
                time.sleep(60)
                _,hora_atual = time_atual()
            reles(3)
            enviar_feedback(tag)

        else:
            raise 'erro ao liberar acesso'

    except Exception as e:
        GPIO.cleanup()
        print(e)