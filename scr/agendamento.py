# -*- coding: utf-8 -*-

import datetime,time,requests
import RPi.GPIO as GPIO
from config import Config
from pi.leitura_tag import ler

def reles(acesso):
    try:
        if acesso == 1: #liga tudo
            print('acesso 1')
            GPIO.output(pino_rele_1,0)
            GPIO.output(pino_rele_2,0)
        elif acesso == 0: # liga lampada
            print('acesso 0')
            GPIO.output(pino_rele_1,0)
            GPIO.output(pino_rele_2,1)
        elif acesso == 3: #desliga tudo
            print('acesso 3')
            GPIO.output(pino_rele_1,1)
            GPIO.output(pino_rele_2,1)
    except Exception as e:
        raise e


def time_atual():
    data = datetime.datetime.today()

    data_atual = str(data.year) + '-' + str(data.month) + '-' + str(data.day)

    hora_atual = str(data.hour) + ':' + str(data.minute)

    return data_atual,hora_atual

def enviar_feedback(agendamento):
    try:
        payload ={
            'cadastro': 0,
            'id_agendamento' : agendamento 
        }
        requests.post(conf.HOST + '/email/',json=payload)
    except Exception as e:
        raise e

pino_rele_1 = 12 # pino rele 1
pino_rele_2 = 16 # pino rele 2


#GPIO.setmode(10)
GPIO.setup(pino_rele_1, GPIO.OUT)
GPIO.setup(pino_rele_2, GPIO.OUT)

conf = Config()

print('setando rele 0')

reles(3)

print('iniciando leitura agendamento')

while True:
    try:
        tag,_ = ler()

        response = requests.get(conf.HOST + '/tag/agendamento/' + str(tag))  # pegar agendamento
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
            enviar_feedback(agendamento['id_agendamento'])

        elif not agendamento['acesso'] and agendamento['data'] == data_atual and agendamento['hora'] == hora_atual:
            print('acesso 0')
            while agendamento['hora_final'] == hora_atual:
                reles(0)
                time.sleep(60)
                _,hora_atual = time_atual()
            reles(3)
            enviar_feedback(agendamento['id_agendamento'])

        else:
            raise 'erro ao liberar acesso'

    except Exception as e:
        GPIO.cleanup()
        print(e)
