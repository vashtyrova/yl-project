import random
import json
import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

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


def write_msg(user_id, message, key=False):
    if key == False:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048),
                                    'keyboard': keyboard})


# API-token
token = "2effda6686d5e2a99e480df53ea289be412f6e08f3bd431cf6f206689f4fc1e42dbe0121d4c6b918ffc5c"

# Авторизация по токену
vk = vk_api.VkApi(token=token)

# Подключение бот лонгопола
bot_longpoll = VkBotLongPoll(vk, 179315864)

# Старт сессии
print("Server started")

for event in bot_longpoll.listen():

    if event.type == VkBotEventType.GROUP_JOIN:

        obj = event.object
        write_msg(obj.user_id, "Привет! Добро пожаловать! Хочешь узнать поподробнее о наших зонтах? ", True)

    elif event.type == VkBotEventType.GROUP_LEAVE:

        obj = event.object
        write_msg(obj.user_id, "Иди, иди! Мокни без наших крутых зонтов!")

    elif event.type == VkBotEventType.MESSAGE_ALLOW:

        obj = event.object
        write_msg(obj.user_id, "Привет) Спасибо, что разрешил писать тебе! Я помогу тебе выбрать подходящий зонтик и покажу погоду на сегодня ;)", True)
