import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

keys = open("keyOwners.txt", "r")
key_owners = keys.read().split(',')
keys.close()

allowed_groups = ["-1001375094289", "762677286"]
allowed = False


def check_group(update, context):
    global allowed
    chat = update.message.chat
    chat_id = str(chat.id)
    if chat_id in allowed_groups:
        allowed = True
    else:
        allowed = False


def start(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    context.bot.sendMessage(chat_id, "Olá, eu fui criado pelo Vino e irei mostrar quem está com as chaves " +
                            "da salinha do DASI para facilitar o gerenciamento!\n\n" +
                            "Digite /ajuda para ver os comandos disponiveis.")


def ajuda(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar esse comando!")
        return

    context.bot.sendMessage(chat_id, "*Lista de comandos* \n\n+"
                                     "/entrar - Registrar que você tem chave\n" +
                            "/sair - Registrar que você não tem mais chave\n" +
                            "/lista - Lista de todos que têm chave", 'Markdown')


def lista(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    for i in range(len(key_owners)):
        new = "\n- ".join(key_owners)
    if len(key_owners) <= 1:
        context.bot.sendMessage(chat_id, "Ninguém tem chave!")
    else:
        context.bot.sendMessage(chat_id, new)


def entrar(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    user = update.message.from_user
    first = user.first_name
    last = user.last_name

    has_key = False

    if last is None:
        if first in key_owners:
            context.bot.sendMessage(chat_id, "Você já tem chave!")
            has_key = True
        else:
            key_owners.append(str(first))
    else:
        if (first + " " + last) in key_owners:
            context.bot.sendMessage(chat_id, "Você já tem chave!")
            has_key = True
        else:
            key_owners.append(str(first) + " " + str(last))

    for i in range(len(key_owners)):
        new = "\n- ".join(key_owners)

    if not has_key:
        context.bot.sendMessage(chat_id, new)


def sair(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    user = update.message.from_user
    first = user.first_name
    last = user.last_name

    has_key = True

    if last is None:
        if first in key_owners:
            key_owners.remove(str(first))
        else:
            context.bot.sendMessage(chat_id, "Você ainda não tem chave!")
            has_key = False
    else:
        if (first + " " + last) in key_owners:
            key_owners.remove(str(first) + " " + str(last))
        else:
            context.bot.sendMessage("Você ainda não tem chave!")
            has_key = False

    for i in range(len(key_owners)):
        new = "\n- ".join(key_owners)

    if has_key:
        if len(key_owners) > 1:
            context.bot.sendMessage(chat_id, new)
        else:
            context.bot.sendMessage(chat_id, "Ninguém tem chave!")


def reset_list(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    tam = len(key_owners)
    while tam > 1:
        key_owners.pop()
        tam = len(key_owners)


def invalid(update, context):
    chat = update.message.chat
    chat_id = chat.id
    check_group(update, context)
    typ = chat.type

    if typ == "private":
        if allowed is False:
            context.bot.sendMessage(chat_id, "Você não tem permissão para utilizar o bot!")
            return
        context.bot.sendMessage(chat_id, "Comando inválido! Digite /ajuda para visualizar a lista de comandos.")


def inserir(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    full_name = (str(update.message.text)).split()
    names = len(full_name)

    if names == 2:
        key_owners.append(full_name[1])
        lista(update, context)
    elif names == 3:
        key_owners.append(full_name[1] + " " + full_name[2])
        lista(update, context)
    else:
        context.bot.sendMessage(chat_id, "Nome inválido, digite apenas nome e um sobrenome!")


def remover(update, context):
    chat = update.message.chat
    chat_id = chat.id

    check_group(update, context)
    if allowed is False:
        context.bot.sendMessage(chat_id, "Este grupo não tem permissão para utilizar o bot!")
        return

    full_name = (str(update.message.text)).split()
    names = len(full_name)

    if names == 2:
        key_owners.remove(full_name[1])
        lista(update, context)
    elif names == 3:
        key_owners.remove(full_name[1] + " " + full_name[2])
        lista(update, context)
    else:
        context.bot.sendMessage(chat_id, "Nome inválido, digite apenas nome e um sobrenome!")


"""def chatid(update, context):
    chat = update.message.chat
    chat_id = str(chat.id)
    context.bot.sendMessage(chat_id, chat_id)"""


def main():
    token = "1094935008:AAGjd242yOm8iLwNJR8C4FD7KYhshIIiWB8"
    port = int(os.environ.get('PORT', '5000'))

    updater = Updater(token, use_context=True)
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=token)
    updater.bot.set_webhook("https://dasiado.herokuapp.com/" + token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ajuda", ajuda))
    dp.add_handler(CommandHandler("entrar", entrar))
    dp.add_handler(CommandHandler("sair", sair))
    dp.add_handler(CommandHandler("lista", lista))
    dp.add_handler(CommandHandler("resetlist", reset_list))
    dp.add_handler(CommandHandler("inserir", inserir))
    dp.add_handler(CommandHandler("remover", remover))
    # dp.add_handler(CommandHandler("chatid", chatid))

    dp.add_handler(MessageHandler(Filters.text, invalid))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
