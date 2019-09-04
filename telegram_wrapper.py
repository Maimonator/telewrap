#!/usr/bin/env python3
import argparse
import json
import time
from telebot import TeleBot
import os
import subprocess
import colors
import shutil
import sys

USER_DICT = {}
bot = TeleBot(6)

TELEWRAP_BASH_FORMAT = """#!/bin/bash
python3 telegram_wrapper.py wrap --config-file {config_file} --users {users} --cmd \"$@\""""

def printAndExecute(commandLine):
    if isinstance(commandLine, list):
        commandLine = ' '.join(commandLine).strip()
    print(colors.green(commandLine))
    return subprocess.check_call(commandLine, shell=True)


def load_config(path):
    config_path = os.path.expanduser(path)
    with open(path, "r") as r:
        return json.load(r)

def send_message(token, user_ids, time):
    global bot
    message = f"job finished, took {time} seconds"

    bot = TeleBot(token)
    for uid in user_ids:
        bot.send_message(uid, message)

def wrap(args):
    config = load_config(args.config_file)
    token = config['token']
    users = { x:config.get(x, None) for x in args.users}
    found_users, user_ids = zip(*[(x, y) for x,y in users.items() if y is not None])
    print("Starting job, will send message to these users:")
    print(" ".join(found_users))
    start_time = time.time()
    printAndExecute(args.cmd)
    time_took = int(time.time() - start_time)
    send_message(token, user_ids, time_took)

def configure(args):
    global USER_DICT
    global bot

    bot = TeleBot(args.token)
    @bot.message_handler(commands=['subscribe'])
    def command_subscribe(msg):
        global USER_DICT
        uid = msg.from_user.id
        try:
            user = msg.text.split(" ")[1]

            USER_DICT.setdefault(user, uid)
            bot.reply_to(msg, f"Subscribed user {user} successfully")
        except Exception as ex:
            print(ex)
            bot.reply_to(msg, "use /subscribe '[username]' to subscribe")

    @bot.message_handler(commands=['end'])
    def command_end(msg):
        print("Ending bot")
        bot.send_message(msg.from_user.id, "Ending bot")
        bot.stop_polling()
    print("Polling for subscriptions")
    bot.polling()

    # after polling finishes
    config_path = os.path.expanduser(args.output)
    try:
        config_dict = load_config(config_path)
    except Exception as ex:
        config_dict = {}
    config_dict.update({'token':args.token})
    config_dict.update(USER_DICT)

    print(f"Saving configuration to {config_path}")
    with open(config_path, "w") as w:
        json.dump(config_dict, w)

def install(args):
    telewrapper_data = TELEWRAP_BASH_FORMAT.format(users=" ".join(args.users), config_file=args.config_file)
    telewrapper_output = os.path.join(args.install_path, "telewrap")
    script_filename = sys.argv[0]
    script_in_path = os.path.join(os.path.abspath(os.curdir), script_filename)
    script_out_path = os.path.join(args.install_path, os.path.splitext(script_filename)[0])

    shutil.copy(script_in_path, script_out_path)

    print(f"Installing telewrapper in {telewrapper_output}")
    with open(telewrapper_output, "w") as w:
        w.write(telewrapper_data)
    os.chmod(telewrapper_output, int("777",8))
    print(telewrapper_output)
    print("Finished installing telewrap")
    print("Usage: telewrap <command>")
    print("Best Regards,")


def main():

    parser = argparse.ArgumentParser(description="telegram wrapper for executing things")
    subparsers = parser.add_subparsers()
    configure_parser = subparsers.add_parser("configure")
    configure_parser.add_argument("-o",
                                  "--output",
                                  help="output path to write config file to, default is '~/.tele.config'",
                                   default="~/.tele.config")
    configure_parser.add_argument("token", help="bot api token")
    # configure_parser.add_argument("users", nargs='+', help="user list with username and cid should be formatted as: user1,cid1 user2,cid2")
    configure_parser.set_defaults(do=configure)

    wrapper_parser = subparsers.add_parser("wrap")
    wrapper_parser.add_argument("--users", nargs='+', help="users to send message to on telegram when job finishes", default=[])
    wrapper_parser.add_argument("--config-file",
                                help="config file to use, default is '~/.tele.config'",
                                default="~/.tele.config")
    wrapper_parser.add_argument("--cmd", help="command to execute", nargs='+', required=True)
    wrapper_parser.set_defaults(do=wrap)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("-i","--install-path", help="path to install the script in default is /usr/local/bin", default="/usr/local/bin")
    install_parser.add_argument("--config-file", help="config file to use, default is '~/.tele.config'",default="~/.tele.config")
    install_parser.add_argument("-u","--users", help="users to send message to when job finishes", required=True, nargs='+')
    install_parser.set_defaults(do=install)



    args = parser.parse_args()
    args.do(args)


if __name__ == '__main__':
    main()
