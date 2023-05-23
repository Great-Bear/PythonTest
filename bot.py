from telethon.sync import TelegramClient, events
from telethon.tl import functions, types

api_id = 'API'
api_hash = 'API_HASH'
phone_number = 'PHONE'

channel_entity = None

with TelegramClient('session_name', api_id, api_hash) as client:
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        global channel_entity

        if event.is_private:
            sender = await event.get_sender()
            print(f"Новое сообщение от: {sender.username}")

            if event.message.text:
                text = event.message.text
                if text.startswith('https://t.me/') or text.startswith('https://telegram.me/'):
                    url = text
                    entity = await client.get_entity(url)
                    if isinstance(entity, types.Channel):
                        channel_info = await client(functions.channels.GetFullChannelRequest(channel=entity))
                       
                        title = channel_info.chats[0].title
                        about = channel_info.full_chat.about
                        messages = await client.get_messages(entity)
                       
                        result = await client(functions.channels.CreateChannelRequest(
                            title=title,
                            about=about,
                            megagroup=False
                        ))
                        new_channel_entity = types.InputChannel(result.chats[0].id, result.chats[0].access_hash)
                        new_channel_info = await client.get_entity(new_channel_entity)
                        print(f"Новый канал создан: {new_channel_info.title} (@{new_channel_info.username})")
 
                        photo = await client.download_profile_photo(entity)
                        result = await client(functions.channels.EditPhotoRequest(
                           photo=  await client.upload_file(photo),
                           channel= new_channel_entity
                        ))
                        print('Аватарка успешно скопирована')
  
                        for message in messages:
                            if not isinstance(message, types.MessageService):
                                await client.send_message(new_channel_entity, message)

                        await client.send_message(sender, f"Канал {new_channel_info.title} был успешно создан и заполнен!")
                    else:
                        print("Некорректная ссылка на канал")
                        await client.send_message(sender, "Некорректная ссылка на канал")

    client.start(phone_number)
    client.run_until_disconnected()