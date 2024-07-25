from telethon import TelegramClient, events
from telegram import Bot
import asyncio
import os
import pandas as pd
from openai import OpenAI
import json

clientAI = OpenAI(api_key='<<API_KEY>>', base_url="https://api.deepinfra.com/v1/openai")

def generate_response_from_api(prompt: str):
    response = clientAI.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7,
        max_tokens=5
    )
    if response.choices:
        return response.choices[0].message.content

    return None


API_ID = '<<API_ID>>'
API_HASH = '<<API_HASH>>'
BOT_TOKEN = '<<BOT_TOKEN>>'
NAMES_IDS = ['@mari_vakansii', '@dnative_job', '...']


clientTg = TelegramClient('<<CLIENT_SESSION_NAME>>', API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)


keywords = [
    '#дизайнер', '#графическийдизайнер', '#лендинг', '#вебдизайн', '#веб-дизайн',
    '#вебдизайнер', '#вебдизайнера', '#веб-дизайнер', '#веб-дизайнера',
    '#дизайнера', 'инфографика', 'карточка', 'сайт', 'таплинк',
    'taplink', 'презентация', 'презентацию', 'карточку', 'инфографику',
    'оформление','инфографики', 'карточек', 'тильда', 'тильде', 'tilda','#дизайнер',
    '#графическийдизайнер', '#лендинг', '#вебдизайн', '#веб-дизайн',
    '#вебдизайнер', '#вебдизайнера', '#веб-дизайнер', '#веб-дизайнера',
    '#дизайнера', 'сайтолог', 'сайтолога', 'инфографике', 'сайты', '#разработкалейдинга',
    '#куратор', '#UX', '#UI'
]

exclude_keywords = [
    'помогу', '#помогу', 'меня зовут', 'создам', 'сделаю', 'создаю', 'делаю', 'маркетплейсах',
    'ассистент', 'помощник', 'онлайн-школа', 'техспециалист', 'маркетинг', 'инфобизнес', '#онлайн', '#работа',
    '#телеграм', '#администратор', '#диспетчер', '#модель', '#менеджер', '#наставничество', '#техспец',
    '#техническийспециалист', '#вакансия', 'продюсера', 'сотрудничество', '#верстальщик', '#код',
    '#техническийспециалист', 'seo', 'SEO', '#seo', '#SEO', 'куратор', '#эксперт', '#предпрениматель',
    'смм', 'СММ', 'SMM', 'smm', '#проджект', '#управляющий', '#сторисмейкер', '#рилсмейкер', 'админ', '#админ',
    'подработка','#подработка', '#контент', '#смм', '#СММ', '#SMM', '#smm', 'сторис', '#сторис',
    'рилс', '#рилс', '#видеомонтаж', '#тех.спец', '#тех', '#тех.спец', '#специалист', '#ютуб', '#копирайтер',
    '#таргетолог', '#таргет', 'таргетолог', 'таргет', '#маркетолог', '#криптовалюта'
]

def message_passes_filter(message_text):
    message_lower = message_text.lower()
    if not any(word in message_lower for word in keywords):
        return False
    if any(word in message_lower for word in exclude_keywords):
        return False
    return True


async def handle_new_message(event):
    message = event.message
    if message.text and message_passes_filter(message.text):
        print(message.text)
        system_prompt = f"This message is in Russian: '{message.text}'. I need to sort this message, YOU MUST only reply to me with 'True' or 'False'. 'True' if in this message a person is looking for a designer freelancer for an order, exactly an order (not a vacancy). 'False' in any other case."
        if generate_response_from_api(system_prompt) == 'True':
            link = f"<a href='https://t.me/{event.chat.username}/{message.id}'>Ссылка</a>"
            await bot.send_message(chat_id='<<CHAT_ID>>', text=f"{link}\n\n{message.text}", parse_mode='HTML')



async def main():
    async with clientTg:
        for channel_id in NAMES_IDS:
            try:
                await clientTg.get_input_entity(channel_id)
                clientTg.add_event_handler(handle_new_message, events.NewMessage(chats=channel_id))
            except:
                print(f"Invalid username: {channel_id}")
        await clientTg.run_until_disconnected()


if __name__ == "__main__":
    clientTg.loop.run_until_complete(main())


