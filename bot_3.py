from telethon.sync import TelegramClient, events
from telethon.tl import functions, types

api_id = 'ID'
api_hash = 'HASH'
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
                if text.lower() == "/createchannel":
                        result = await client(functions.channels.CreateChannelRequest(
                            title="TitleTest3Channel",
                            about="AboutTest3Channel",
                            megagroup=False
                        ))
                        channel_entity = types.InputChannel(result.chats[0].id, result.chats[0].access_hash)
                        new_channel_info = await client.get_entity(channel_entity)
                        print(f"Новый канал создан: {new_channel_info.title} (@{new_channel_info.username})")
                else:
                    await client.send_message(channel_entity, text)
                    await client.send_message(sender, "Ваш текст успешно доставлен")
                    print(f"Текст успешно отправлен в канал")

            if event.media:
                media = await event.download_media()
                caption = event.message.text

                if channel_entity is not None:
                    await client.send_file(channel_entity, file=media, caption=caption)
                    await client.send_message(sender, "Ваш медиафайл был успешно доставлен в канал.")
                    print(f"Медиафайл успешно отправлен в канал")
                    
    client.start(phone_number)
    client.run_until_disconnected()