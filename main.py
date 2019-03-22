#!/usr/bin/env python3
import os
# import logging
import time
from slackclient import SlackClient
from langdetect import detect
from nltk.tokenize import word_tokenize

EXCUSES = '답변이 불만족스러운 경우, 앨런에게 직접 연락 바랍니다.'

def help_message():
    return '''
살살
'''


def create_resp(cmd):
    return '자연어를 우짠다.'


def smart_resp(cmd):
    if (cmd.startswith('allen') is False and
            cmd.startswith('Allen') is False and
            cmd.startswith('ALLEN') is False and
            cmd.startswith('알랜') is False and
            cmd.startswith('앨런') is False):
        # 앨런을 부르는게 아닌 경우 무시
        return

    # TODO: 여기가 핵이다.
    resp = create_resp(cmd)

    lang = detect(cmd[0:2])
    if lang == 'ko':
        msg = '*문의*\n> %s\n*답변*\n> %s\n\n:arrow_right: %s' % (cmd[3:].lstrip(), resp, EXCUSES)
    else:
        msg = '*문의*\n> %s\n*답변*\n> %s\n\n:arrow_right: %s' % (cmd[5:].lstrip(), resp, EXCUSES)
        # msg = '문의\n> %s\n답변\n> %s\n\n%s' % (cmd[5:].lstrip(), resp, EXCUSES)
        # msg = '문의: %s\n답변: %s\n\n%s' % (cmd[5:].lstrip(), resp, EXCUSES)
    return msg


def handle_command(slack_client, channel, cmd):
    if cmd == 'help':
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=help_message()
        )

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=smart_resp(cmd)
    )
    return


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    # print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            return event['channel'], event['text']
    return None, None


# def init_logger():
#     log_file = '%s/src/allen.log' % os.path.expanduser('~')
#     log_hl = logging.StreamHandler()
#     log_hl.setLevel(logging.ERROR)  # Console display - ERROR, CRITICAL
#     formatter = logging.Formatter('[%(levelname)8s] %(message)s')
#     log_hl.setFormatter(formatter)
#     logging.basicConfig(filename=log_file,
#                         format='[%(asctime)s] (%(levelname)8s) %(message)s',
#                         datefmt='%m/%d %I:%M:%S',
#                         level=logging.INFO)
#     log = logging.getLogger('allen')
#     log.addHandler(log_hl)
#     return log


def main():
    SLACK_SECRET_ID = os.environ.get('SLACK_SECRET_ID')
    slack_client = SlackClient(SLACK_SECRET_ID)
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        # starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            try:
                slack_events = slack_client.rtm_read()
                channel, cmd = parse_bot_commands(slack_events)
                if cmd:
                    # print(channel, cmd)
                    handle_command(slack_client, channel, cmd)
            except:
                pass
            time.sleep(1)
        print("broken while loop")
    else:
        print("Connection")


if __name__ == '__main__':
    main()
