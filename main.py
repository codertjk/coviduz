# -*- coding: utf-8 -*-

# Copyright (C) 2020 Botir Ziyatov <botirziyatov@gmail.com>
# This program is free software: you can redistribute it and/or modify

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from covid19 import Covid19

buttons = ReplyKeyboardMarkup([['Маълумот'], ['Дунё']], resize_keyboard=True)
covid = Covid19()

def start(update, context):
    update.message.reply_html(
        '<b>Ассалому алейкум, {}</b>\n \nМан боти дар бораи омори Короновирус маълумот медиҳам @codertj'.format(update.message.from_user.first_name), reply_markup=buttons)
    return 1

def stats(update, context):
    data = covid.getByCountryCode('TJ')
    update.message.reply_html(
        '🇹🇯 <b>Дар Точикистон</b>\n \n<b>Сироят шуда:</b> {}\n<b>шифо ёфт:</b> {}\n<b>Фавту:</b> {}'.
            format(
            data['confirmed'],
            data['recovered'],
            data['deaths']), reply_markup=buttons)

def world(update, context):
    data = covid.getLatest()
    update.message.reply_html(
        '🌎 <b>Дунё</b>\n \n<b>Сироят шуда:</b> {}\n<b>шифо ёфт:</b> {}\n<b>Фавту:</b> {}'.format(
            "{:,}".format(data['confirmed']),
            "{:,}".format(data['recovered']),
            "{:,}".format(data['deaths'])
        ), reply_markup=buttons)

updater = Updater('1217258309:AAEl6jYOdMwrx_X7pGc4HZ02hZtCT6NPsew', use_context=True)
conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states={
        1: [MessageHandler(Filters.regex('^(Маълумот)$'), stats),
            MessageHandler(Filters.regex('^(Дунё)$'), world),
            ]
    },
    fallbacks=[MessageHandler(Filters.text, start)]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
