import random
import json
import requests
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll

# Клавиатура в обычном режиме
keyboard = {
    'one_time': False,
    'buttons': [[{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': 'Прогноз погоды',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '2'}),
            'label': 'Товары',
        },
        'color': 'positive'
    }
    ]]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

# Клавиатура в режиме просмотра товаров
keyboard2 = {
    'one_time': False,
    'buttons': [[{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': 'Посмотреть ещё',
        },
        'color': 'positive'
    }
    ]]
}
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))


def write_msg(user_id, message, key=False):
    if key == False:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048),
                                    'keyboard': keyboard})


# Товары и их смена
def market(lim):
    if lim == 0:
        mes = "Для начала посмотри этот крутой зонт с корюшкой"
        att = 'market-179315864_2083667'
        k = keyboard2
    elif lim == 1:
        mes = "Нет? А как тебе такой вариант?"
        att = 'market-179315864_2083684'
        k = keyboard2
    elif lim == 2:
        mes = "Хорошо. Может быть этот вариант? С таким зонтиком ты точно не заблудишься)"
        att = 'market-179315864_2100866'
        k = keyboard2
    elif lim == 3:
        mes = "Вот этот зонтик с прекрасными архитектурными сооружениями нашего города!"
        att = 'market-179315864_2100859'
        k = keyboard2
    elif lim == 4:
        mes = "Есть и в другом цвете ;)"
        att = 'market-179315864_2083672'
        k = keyboard
    return [mes, att, k]


# Погода
def weather():
    city_id = 498817
    appid = "1666d138d77ad921828b64bc24ca1e45"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'appid': appid, 'lang': 'ru'})
        data = res.json()
        Min = 100
        Max = -100

        # p0 - ключ, для проверки что весь день не что-то из перечисленного ниже
        # p1 - ясно
        # p2 - облачно
        # p3 - дождь / гроза
        # p4 - изморось
        # p5 - снег
        p0, p1, p2, p3, p4, p5 = 0, 0, 0, 0, 0, 0

        c = 0
        while c < 7:
            t = data["list"][c]["main"]
            l = data["list"][c]
            mint = t["temp_min"]
            if mint < Min:
                Min = mint
            maxt = t["temp_max"]
            if maxt > Max:
                Max = maxt

            pog = l["weather"][0]["main"]
            if pog == "Clear":
                p1 += 1
            elif pog == "Cloud":
                p2 += 1
            elif pog == "Rain":
                p3 += 1
            elif pog == "Thunderstorm":
                p3 += 1
            elif pog == "Drizzle":
                p4 += 1
            elif pog == "Snow":
                p5 += 1
            else:
                p0 += 1
            c += 1

        # Распределение, что писать
        if p0 != 7:
            if p1 == 7:
                s = "Сегодня весь день ясно"
            elif p3 == 0 and p4 == 0 and p5 == 0:
                s = "Сегодня будет облачно"
            else:
                if p3 < 3 and p4 < 3 and p5 < 3:
                    if p4 == 0 and p5 == 0:
                        s = "Возможен дождь"
                    elif p3 == 0 and p5 == 0:
                        s = "Возможен мокрый снег"
                    elif p3 == 0 and p4 == 0:
                        s = "Возможен снег"
                    elif p3 == 0:
                        s = "Возможен снег"
                    else:
                        s = "Возможны осадки с выпадением снега"
                else:
                    if p4 == 0 and p5 == 0:
                        s = "Сегодня будет дождь"
                    elif p3 == 0 and p5 == 0:
                        s = "Сегодня будет мокрый снег"
                    elif p3 == 0 and p4 == 0:
                        s = "Сегодня будет снег"
                    elif p3 == 0:
                        s = "Сегодня будет снег"
                    else:
                        s = "Осадки, возможно выпадение снега"
        else:
            s = "Nu vse, pizdec!"       # что ничего

        wres = ("Минимальная температура воздуха: " + str(Min) + "°C" + "\n" + "Максимальная температура воздуха: " + str(Max) + "°C"
                + "\n" + s)
    except Exception as e:
        print("Exception (find):", e)
        pass

    return [wres]


# API-token
token = "2effda6686d5e2a99e480df53ea289be412f6e08f3bd431cf6f206689f4fc1e42dbe0121d4c6b918ffc5c"

# Авторизация по токену
vk = vk_api.VkApi(token=token)

# Подключение лонгпола и бот лонгопола
longpoll = VkLongPoll(vk)
bot_longpoll = VkBotLongPoll(vk, 179315864)

# Старт сессии
print("Server started")


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            if event.text == "Прогноз погоды":
                write_msg(event.user_id, weather()[0])

            elif event.text == "Товары":
                lim = 0
                vk.method('messages.send',
                          {'user_id': event.user_id, 'message': market(lim)[0],
                           'attachment': market(lim)[1], 'random_id': random.randint(0, 2048),
                           'keyboard': market(lim)[2]})

            elif event.text == "Посмотреть ещё":
                lim += 1
                vk.method('messages.send',
                          {'user_id': event.user_id, 'message': market(lim)[0],
                           'attachment': market(lim)[1], 'random_id': random.randint(0, 2048),
                           'keyboard': market(lim)[2]})

            elif event.text == "Привет":
                write_msg(event.user_id, "Привет!", True)

            elif event.text == "Как дела?":
                write_msg(event.user_id, "Хорошо", True)


