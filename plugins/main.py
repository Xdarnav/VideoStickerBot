import os
from database import database
from plugins.helpers import Helpers
from pyArnavje import Arnavje, Message, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Arnavje.cmd(private_only=True, extra_filters=filters.video | filters.animation)
async def main(_, msg: Message):
    status = await msg.reply("Doing what I do best...")
    Arnavje = Helpers(msg, status)
    await process(msg, Arnavje, status)
    if os.path.exists(Arnavje.input_file):
        os.remove(Arnavje.input_file)
    if os.path.exists(Arnavje.output_file):
        os.remove(Arnavje.output_file)


async def process(msg: Message, Arnavje: Helpers, status: Message):
    await msg.download(Arnavje.input_file)
    std = await Arnavje.subshell()
    if os.path.exists(Arnavje.output_file):
        await Arnavje.correct_the_size()  # File is too big error
        await status.edit('Getting your pack...')
        success, pack_name, title = await Arnavje.get_default_pack()
        should_ask = await database.get('users', Arnavje.user_id, 'ask_emojis')
        if should_ask:
            emojis = await Arnavje.ask_for_emojis()
            if not emojis:
                return
        else:
            data = await database.get('users', msg.from_user.id, "default_emojis")
            if data:
                emojis = data
            else:
                emojis = '💖'
        params = await Arnavje.params(pack_name, emojis, title)
        file = open(Arnavje.output_file, 'rb')
        if success:
            success = await Arnavje.add_to_pack(params, file)
            if not success:
                return
        else:
            success = await Arnavje.new_pack(params, file)
            if not success:
                return
        sticker = await Arnavje.get_pack(params, file)
        await status.delete()
        if sticker:
            button = [[InlineKeyboardButton('Get WEBM File', callback_data='current_webm')]]
            await msg.reply_sticker(
                sticker,
                reply_to_message_id=msg.message_id,
                reply_markup=InlineKeyboardMarkup(button)
            )
        file.close()
        await Arnavje.session.aclose()
    else:
        await Arnavje.ffmpeg_error(std)
        return


@Arnavje.callback('current_webm')
async def get_webm(_, callback: CallbackQuery):
    await Helpers.send_webm(callback.message)
    await callback.answer()


@Arnavje.cmd(private_only=True, extra_filters=filters.sticker, group=1)
async def existing_sticker_func(_, msg: Message):
    if msg.sticker.is_video:
        data = await database.get('users', msg.from_user.id)
        if data['kang_mode']:
            status = await msg.reply("Doing what I do best [Kanging]... ")
            sticker_file = await msg.download(f'kangs/{msg.from_user.id}_{msg.message_id}.webm')
            Arnavje = Helpers(msg, status)
            await status.edit('Getting your pack...')
            success, pack_name, title = await Arnavje.get_default_pack()
            should_ask = await database.get('users', Arnavje.user_id, 'ask_emojis')
            if should_ask:
                emojis = await Arnavje.ask_for_emojis()
                if not emojis:
                    return
            else:
                data = await database.get('users', msg.from_user.id, "default_emojis")
                if data:
                    emojis = data
                else:
                    emojis = '💖'
            params = await Arnavje.params(pack_name, emojis, title)
            file = open(sticker_file, 'rb')
            if success:
                success = await Arnavje.add_to_pack(params, file)
                if not success:
                    return
            else:
                success = await Arnavje.new_pack(params, file)
                if not success:
                    return
            sticker = await Arnavje.get_pack(params, file)
            await status.delete()
            if sticker:
                await msg.reply_sticker(
                    sticker,
                    reply_to_message_id=msg.message_id,
                )
            file.close()
            os.remove(sticker_file)
            await Arnavje.session.aclose()
        elif data['get_webm']:
            await Helpers.send_webm(msg)
