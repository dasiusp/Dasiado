import os
import database

from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

allowed = False


def check_group(bot, update):
    global allowed
    chat_id = update.message.chat.id

    allowed_groups_ref = database.get_allowed_groups()
    allowed_groups = (allowed_groups_ref.to_dict()).values()

    if str(chat_id) in allowed_groups:
        allowed = True
    else:
        allowed = False


def start(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    update.message.reply_text("Olá, eu fui criado pelo Vino e irei mostrar quem está com as chaves " +
                              "da salinha do DASI para facilitar o gerenciamento!\n\n" +
                              "Digite /ajuda para ver os comandos disponiveis.", quote=False)


def help(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar esse comando!", quote=False)
        return

    update.message.reply_markdown("**Lista de comandos** \n\n"
                                  "/entrar - Registrar que você tem chave\n" +
                                  "/sair - Registrar que você não tem mais chave\n" +
                                  "/lista - Lista de todos que têm chave", quote=False)


def list_key_owners(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    owners = database.get_key_owners()
    names = (owners.to_dict()).values()

    for i in range(len(names)):
        new = "\n- ".join(names)
    if len(names) <= 0:
        update.message.reply_text("Ninguém tem chave!", quote=False)
    else:
        update.message.reply_text("Estão com chave: \n\n- "+new, quote=False)


def key_in(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    owners = database.get_key_owners()
    names = (owners.to_dict()).values()

    chat_id = update.message.chat.id
    user = update.message.from_user
    first = user.first_name
    last = user.last_name

    has_key = False

    if last is None:
        if first in names:
            update.message.reply_text("Você já tem chave!", quote=False)
            has_key = True
        else:
            database.insert_name(chat_id, first)
    else:
        if (first + " " + last) in names:
            update.message.reply_text("Você já tem chave!", quote=False)
            has_key = True
        else:
            database.insert_name(chat_id, str(first) + " " + str(last))

    if not has_key:
        list_key_owners(bot, update)


def key_out(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    owners = database.get_key_owners()
    names = (owners.to_dict()).values()

    chat_id = update.message.chat.id
    user = update.message.from_user
    first = user.first_name
    last = user.last_name

    has_key = True

    if last is None:
        if first in names:
            database.delete_name(chat_id)
        else:
            update.message.reply_text("Você ainda não tem chave!", quote=False)
            has_key = False
    else:
        if (first + " " + last) in names:
            database.delete_name(chat_id)
        else:
            update.message.reply_text("Você ainda não tem chave!", quote=False)
            has_key = False

    owners = database.get_key_owners()
    names = (owners.to_dict()).values()

    if has_key:
        if len(names) > 0:
            list_key_owners(bot, update)
        else:
            update.message.reply_text("Ninguém tem chave!", quote=False)


def reset_list(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    owners = database.get_key_owners()
    ids = (owners.to_dict()).keys()

    for id in ids:
        database.delete_name(id)


def invalid_message(bot, update):
    chat_type = update.message.chat.type

    if chat_type == "private":
        check_group(bot, update)
        if allowed is False:
            update.message.reply_text("Você não tem permissão para utilizar o bot!", quote=False)
            return
        update.message.reply_text("Comando inválido! Digite /ajuda para visualizar a lista de comandos.", quote=False)


def webhook(request):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    dispatcher = Dispatcher(bot, None, 0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ajuda", help))
    dispatcher.add_handler(CommandHandler("entrar", key_in))
    dispatcher.add_handler(CommandHandler("sair", key_out))
    dispatcher.add_handler(CommandHandler("lista", list_key_owners))
    dispatcher.add_handler(CommandHandler("resetlist", reset_list))
    dispatcher.add_handler(MessageHandler(Filters.text, invalid_message))

    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"
