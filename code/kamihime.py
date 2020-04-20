from .library import ImageOperation, WindowsGUI, CommonLogger
from enum import Enum
import time
import sys
import datetime
import traceback

KAMIHIME_DIR = "kamihime\\"
ERR_PATH = "err\\"

NOR_PASS_LATE = 0.9
SEVER_PASS_LATE = 0.95
MIDDLE_PASS_LATE = 0.8
EASE_PASS_LATE = 0.7

GO_QUEST = KAMIHIME_DIR + "go_quest.png"
OK = KAMIHIME_DIR + "ok.png"
GO_MYPAGE = KAMIHIME_DIR + "go_mypage.png"
GO_RAID = KAMIHIME_DIR + "go_raid.png"
USE_ITEM = KAMIHIME_DIR + "use_item.png"
SELECT_FRIEND = KAMIHIME_DIR + "select_friend.png"
KYUUEN = KAMIHIME_DIR + "kyuuen.png"
ATTACK = KAMIHIME_DIR + "attack.png"
NEXT_BATTLE = KAMIHIME_DIR + "next_battle.png"
NEXT_RES = KAMIHIME_DIR + "next.png"
RETURN_RAID = KAMIHIME_DIR + "return_raid.png"
CANCEL = KAMIHIME_DIR + "cancel.png"
CONTINUE_RES = KAMIHIME_DIR + "continue.png"
EVENT_INDEX = KAMIHIME_DIR + "event_index.png"
FRIEND_WATER = KAMIHIME_DIR + "friend_water.png"
FRIEND_DARK = KAMIHIME_DIR + "friend_dark.png"
FRIEND_WIND = KAMIHIME_DIR + "friend_wind.png"
FRIEND_THUNDER = KAMIHIME_DIR + "friend_thunder.png"
FRIEND_FIRE = KAMIHIME_DIR + "friend_fire.png"
FRIEND_HOLY = KAMIHIME_DIR + "friend_holy.png"
AUTO_OFF = KAMIHIME_DIR + "auto_off.png"
QUEST_TOP = KAMIHIME_DIR + "quest_top.png"
RETIRE = KAMIHIME_DIR + "retire.png"
PAGE_DOWN = KAMIHIME_DIR + "page_down.png"
ERIKUSA = KAMIHIME_DIR + "erikusa.png"
PULL_DOWN = KAMIHIME_DIR + "pulldown.png"
CONFIRM = KAMIHIME_DIR + "confirm.png"
RAID_COMMON = KAMIHIME_DIR + "raid_common.png"

class Kamihime(object):
    def __init__(self, target, stop_time, p_num):
        self.image = ImageOperation()
        self.gui = WindowsGUI()
        self.logger = CommonLogger().common_logger()
        self.target = target
        self.stop_time = stop_time
        self.loop_cnt = 0
        self.weekday = datetime.date.today().weekday()
        self.target_type = None
        if p_num == 0:
            if self.weekday == 0:
                self.p_type = FRIEND_WIND
                self.target_type = FRIEND_THUNDER
            elif self.weekday == 1:
                self.p_type = FRIEND_WATER
                self.target_type = FRIEND_FIRE
            elif self.weekday == 2:
                self.p_type = FRIEND_THUNDER
                self.target_type = FRIEND_WATER
            elif self.weekday == 3:
                self.p_type = FRIEND_FIRE
                self.target_type = FRIEND_WIND
            elif self.weekday == 4:
                self.p_type = FRIEND_DARK
                self.target_type = FRIEND_HOLY
            elif self.weekday == 5:
                self.p_type = FRIEND_HOLY
                self.target_type = FRIEND_DARK
            elif self.weekday == 6:
                self.p_type = FRIEND_WATER
                self.target_type = FRIEND_FIRE
        elif p_num == 1:
            self.p_type = FRIEND_FIRE
        elif p_num == 2:
            self.p_type = FRIEND_WATER
        elif p_num == 3:
            self.p_type = FRIEND_WIND
        elif p_num == 4:
            self.p_type = FRIEND_THUNDER
        elif p_num == 5:
            self.p_type = FRIEND_HOLY
        elif p_num == 6:
            self.p_type = FRIEND_DARK
        self.daily_passed = 0

    def open(self):
        self.change_party()

    def start_game(self, cash_crear=True, err=False):
        chrome_config = "chrome_config.png"
        config_history = "config_history.png"
        delete_history = "delete_history.png"
        tab_kamihime = KAMIHIME_DIR + "tab_kamihime.png"
        browser_refresh = "browser_refresh.png"
        start_icon = KAMIHIME_DIR + "game_start.png"

        if cash_crear:
            loc = self.image.match_img(chrome_config, timeout=5, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)

                loc = self.image.match_img(config_history, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                loc = self.image.match_img(delete_history, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                loc = self.image.match_img(tab_kamihime, timeout=2, pass_rate=MIDDLE_PASS_LATE)
                #if not loc:
                #    loc = self.image.match_img(tab_kanpani, timeout=2, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
        loc = self.image.match_img(browser_refresh, timeout=5, pass_rate=MIDDLE_PASS_LATE)
        self.gui.click(loc)

        time.sleep(10)
        loc = self.image.match_img(start_icon)
        self.gui.click(loc)
        for i in range(20):
            time.sleep(5)
            loc_finish_start = self.image.match_img(GO_MYPAGE, pass_rate=SEVER_PASS_LATE)
            if loc_finish_start:
                break
            else:
                self.gui.click(loc)
            if i == 20:
                sys.exit(-1)

    def __wait_battle_end(self):
        loc = self.image.match_img(OK, timeout=1800, pass_rate=MIDDLE_PASS_LATE)
        loc_continue = True
        while loc_continue:
            loc_continue = self.image.match_img(CONTINUE_RES, timeout=3)
            loc_all_down = self.image.match_img(ERIKUSA, timeout=1)
            if loc_all_down:
                loc = self.image.match_img(CANCEL, timeout=1, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                time.sleep(1)
                loc = self.image.match_img(CANCEL, timeout=1, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(OK, timeout=1800, pass_rate=MIDDLE_PASS_LATE)
                break
        self.gui.click(loc)
        loc = self.image.match_img(OK, timeout=3, pass_rate=MIDDLE_PASS_LATE)
        if loc:
            self.gui.click(loc)
        loc = self.image.match_img(NEXT_RES)
        self.gui.click(loc)
        loc = self.image.match_img(CANCEL, timeout=3)
        if loc:
            self.gui.click(loc)
        self.loop_cnt += 1

    def __go_page(self, target=GO_MYPAGE, expect=EVENT_INDEX):
        loc_top = False
        cnt = 0
        while not loc_top:
            loc = self.image.match_img(target, pass_rate=SEVER_PASS_LATE)
            self.gui.click(loc)
            loc_top = self.image.match_img(expect, timeout=2)
            cnt += 1
            if cnt > 10:
                self.start_game()
                break

    def __search_raid(self):
        raid_water = KAMIHIME_DIR + "raid_water.png"
        raid_wind = KAMIHIME_DIR + "raid_wind.png"     
        raid_dark = KAMIHIME_DIR + "raid_dark.png"
        raid_thunder = KAMIHIME_DIR + "raid_thu.png"
        raid_fire = KAMIHIME_DIR + "raid_fire.png"
        raid_holy = KAMIHIME_DIR + "raid_holy.png"
        raid_eve1 = KAMIHIME_DIR + "raid_eve1.png"
        raid_eve2 = KAMIHIME_DIR + "raid_eve2.png"
        raid_oku = KAMIHIME_DIR + "raid_oku.png"

        loc = self.image.match_img(GO_RAID)
        if not loc:
            time.sleep(30)
            self.__go_page()
            return -1
        self.gui.click(loc)
        self.image.match_img(RAID_COMMON)
        raid_target = [raid_oku]
        if self.target_type is None:
            pass
            #raid_target = [raid_water, raid_wind, raid_dark, raid_thunder]
            #raid_target = [raid_eve1, raid_eve2]
            #raid_target = [raid_fire]
            #raid_target = [raid_eve2]
            #raid_target = [raid_thunder]
        elif self.target_type == FRIEND_FIRE:
            raid_target.append(raid_fire)
        elif self.target_type == FRIEND_WATER:
            raid_target.append(raid_water)
        elif self.target_type == FRIEND_WIND:
            raid_target.append(raid_wind)
        elif self.target_type == FRIEND_THUNDER:
            raid_target.append(raid_thunder)
        elif self.target_type == FRIEND_HOLY:
            raid_target.append(raid_holy)
        elif self.target_type == FRIEND_DARK:
            raid_target.append(raid_dark)
        idx, loc = self.image.match_img(raid_target, timeout=1, pass_rate=MIDDLE_PASS_LATE)
        for i in range(3):
            if idx >= 0:
                self.gui.click(loc)
                break
            loc = self.image.match_img(PAGE_DOWN,timeout=1, pass_rate=SEVER_PASS_LATE)
            if not loc:
                break
            self.gui.click(loc)
            time.sleep(0.5)
            idx, loc = self.image.match_img(raid_target, timeout=1, pass_rate=MIDDLE_PASS_LATE)
            if idx >= 0:
                self.gui.click(loc)
                break
        if idx == -1:
            time.sleep(60)
            self.__go_page()
            return -2
        return 0

    def __raid_battle(self):
        raid_menu = KAMIHIME_DIR + "raid_menu.png"
        img_list = [self.p_type, USE_ITEM, CONFIRM]
        idx, loc = self.image.match_img(img_list, timeout=2) 
        if idx == 1:
            self.gui.click(loc)
            loc = self.image.match_img(OK, timeout=2, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            loc = self.image.match_img(self.p_type, timeout=2)
        elif idx == 2:
            self.gui.click(loc)
            loc = self.image.match_img(RAID_COMMON, timeout=3)
            self.gui.click(loc)
            self.__wait_battle_end()
            return 0
        if loc:
            self.gui.click(loc)
        loc = self.image.match_img(SELECT_FRIEND)
        self.gui.click(loc)
        loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
        time.sleep(1)
        self.gui.click(loc)
        self.image.match_img(raid_menu, timeout=30, pass_rate=MIDDLE_PASS_LATE)
        loc = self.image.match_img(OK, timeout=2, pass_rate=MIDDLE_PASS_LATE)
        if loc:
            self.gui.click(loc)
            self.__go_page()
        else:
            loc = self.image.match_img(KYUUEN, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK)
                self.gui.click(loc)
            self.__wait_battle_end()
            self.__go_page()

    def raid_event(self):
        idx = -1
        err_continue = 0
        while idx != 0:
            idx = self.__search_raid()
            if idx == -1:
                err_continue += 1
                if err_continue > 20:
                    raise
        self.__raid_battle()

    def guild_kyougikai(self):
        guild_attack = KAMIHIME_DIR + "guild_attack.png"
        quest = KAMIHIME_DIR + "quest.png"
        dark = KAMIHIME_DIR + "dark.png"
        fire = KAMIHIME_DIR + "fire.png"
        target_center = KAMIHIME_DIR + "target_center.png"

        loc = self.image.match_img(EVENT_INDEX)
        self.gui.click(loc)
        loc = self.image.match_img(guild_attack)
        self.gui.click(loc)
        loc = self.image.match_img(quest)
        self.gui.click(loc)
        while self.loop_cnt < self.stop_time:
            loc = self.image.match_img(fire)
            self.gui.click(loc)
            loc = self.image.match_img(self.p_type, timeout=2)
            if loc:
                self.gui.click(loc)
            loc = self.image.match_img(SELECT_FRIEND)
            if not loc:
                time.sleep(1800)
                raise
            self.gui.click(loc)
            loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
            time.sleep(1)
            self.gui.click(loc)
            loc = self.image.match_img(ATTACK)
            loc_target = self.image.match_img(target_center, timeout=1)
            if loc_target:
                self.gui.click(loc_target)
            loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
            if loc_auto_off:
                self.gui.click(loc_auto_off)
                self.gui.click(loc_auto_off)
            self.gui.click(loc)
            loc = self.image.match_img(OK, timeout=1000, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            loc = self.image.match_img(OK, timeout=1, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)
            self.loop_cnt += 1

    def kourinsen(self):
        kourinsen = KAMIHIME_DIR + "kourinsen.png"
        quest_index = KAMIHIME_DIR + "quest_index.png"
        quest_ultimate = KAMIHIME_DIR + "quest_ultimate.png"
        saichousen = KAMIHIME_DIR + "saichousen.png"

        loc = self.image.match_img(QUEST_TOP)
        self.gui.click(loc)
        loc = self.image.match_img(kourinsen)
        self.gui.click(loc)
        loc = self.image.match_img(quest_index)
        self.gui.click(loc)
        loc = self.image.match_img(quest_ultimate)
        self.gui.click(loc)
        while self.loop_cnt < self.stop_time:
            loc = self.image.match_img(USE_ITEM, timeout=2)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
            loc = self.image.match_img(self.p_type, timeout=2)
            if loc:
               self.gui.click(loc)
            loc = self.image.match_img(SELECT_FRIEND)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
                time.sleep(1)
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK)
            else:
                loc = self.image.match_img(ATTACK, timeout=2)
                if not loc:
                    time.sleep(30)
                    self.gui.click(loc)#error
            loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
            if loc_auto_off:
                self.gui.click(loc_auto_off)
                self.gui.click(loc_auto_off)
            self.gui.click(loc)
            time.sleep(30)
            loc = self.image.match_img(GO_MYPAGE, timeout=300)
            if loc:
                loc = self.image.match_img(OK, timeout=5, pass_rate=MIDDLE_PASS_LATE)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES)
                self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES, timeout=2)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(saichousen, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(USE_ITEM, timeout=2)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(CANCEL, timeout=2)
                    if loc:
                        self.gui.click(loc)
            else:
                loc = self.image.match_img(CANCEL, timeout=2)
                self.gui.click(loc)
                loc = self.image.match_img(RETIRE)
                self.gui.click(loc)
                loc = self.image.match_img(quest_ultimate)
                self.gui.click(loc)
            self.loop_cnt += 1

    def event_kourinsen(self):
        kourinsen = KAMIHIME_DIR + "kourinsen.png"
        event_index = KAMIHIME_DIR + "event_index.png"
        go_event_page = KAMIHIME_DIR + "event_page.png"
        quest_index = KAMIHIME_DIR + "quest_index.png"
        quest_ultimate = KAMIHIME_DIR + "event_kourinsen_quest.png"
        saichousen = KAMIHIME_DIR + "saichousen.png"

        loc = self.image.match_img(event_index)
        self.gui.click(loc)
        loc = self.image.match_img(go_event_page, pass_rate=EASE_PASS_LATE)
        self.gui.click(loc)
        loc = self.image.match_img(quest_index)
        self.gui.click(loc)
        loc = self.image.match_img(quest_ultimate)
        self.gui.click(loc)
        while self.loop_cnt < self.stop_time:
            loc = self.image.match_img(USE_ITEM, timeout=2)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
            loc = self.image.match_img(self.p_type, timeout=2)
            if loc:
                self.gui.click(loc)
            loc = self.image.match_img(SELECT_FRIEND)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
                time.sleep(1)
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK)
            else:
                loc = self.image.match_img(ATTACK, timeout=2)
                if not loc:
                    time.sleep(1800)
                    self.gui.click(loc)#error
            loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
            if loc_auto_off:
                self.gui.click(loc_auto_off)
                self.gui.click(loc_auto_off)
            self.gui.click(loc)
            time.sleep(60)
            loc = self.image.match_img(GO_MYPAGE, timeout=300)
            if loc:
                loc = self.image.match_img(OK, timeout=5)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES)
                self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES, timeout=2)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(saichousen, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(USE_ITEM, timeout=2)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(CANCEL, timeout=2)
                    if loc:
                        self.gui.click(loc)
            else:
                loc = self.image.match_img(CANCEL, timeout=2)
                self.gui.click(loc)
                loc = self.image.match_img(RETIRE)
                self.gui.click(loc)
                loc = self.image.match_img(quest_ultimate)
                self.gui.click(loc)
            self.loop_cnt += 1
                

    def meikyu(self):
        meikyu = KAMIHIME_DIR + "meikyu.png"
        tansaku_kaishi = KAMIHIME_DIR + "tansaku_kaishi.png"
        meikyu_stage = KAMIHIME_DIR + "meikyu_stage_1.png"
        meikyu_go = KAMIHIME_DIR + "meikyu_go.png"
        auto_off_meikyu = KAMIHIME_DIR + "auto_off_meikyu.png"
        erikusa_jougen = KAMIHIME_DIR + "erikusa_jougen.png"
        scroll_top = KAMIHIME_DIR + "scroll_top.png"
        scroll_bottom = KAMIHIME_DIR + "scroll_bottom.png"
        stare_1 = KAMIHIME_DIR + "stare_1.png"
        loc = self.image.match_img(EVENT_INDEX)
        self.gui.click(loc)
        loc = self.image.match_img(meikyu)
        self.gui.click(loc)
        loc = self.image.match_img(tansaku_kaishi)
        self.gui.click(loc)
        loc = self.image.match_img(meikyu_stage)
        self.gui.click(loc)

        loc = self.image.match_img(PULL_DOWN)
        if loc:
            self.gui.click(loc)
            f_loc = self.image.match_img(scroll_top)
            t_loc = self.image.match_img(scroll_bottom)
            self.gui.drag(f_loc, t_loc)
            loc = self.image.match_img(stare_1)
            self.gui.click(loc)

            loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM, timeout=2)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
            loc = self.image.match_img(self.p_type, timeout=2)
            if loc:
                self.gui.click(loc)
                time.sleep(10)
            loc = self.image.match_img(SELECT_FRIEND)
            if loc:
                self.gui.click(loc)
            loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
            time.sleep(1)
            self.gui.click(loc)
        loc = self.image.match_img(meikyu_go)
        if loc:
            loc_auto = self.image.match_img(auto_off_meikyu, timeout=1)
            if loc_auto:
                self.gui.click(loc_auto)
            self.gui.click(loc)
        while self.loop_cnt < self.stop_time:
            img_list = [ATTACK, USE_ITEM, OK, erikusa_jougen]
            idx, loc = self.image.match_img(img_list, pass_rate=MIDDLE_PASS_LATE)
            if idx == 0 or idx == 2:
                self.gui.click(loc)
            if idx == 1:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                self.loop_cnt += 1
            if idx == 3:
                self.gui.click(loc)
                time.sleep(5)
                raise

    def event_serafi(self):
        union_event = KAMIHIME_DIR + "union_event.png"
        serafi = KAMIHIME_DIR + "serafi.png"
        quest_serafi = KAMIHIME_DIR + "quest_serafi.png"
        restart_serafi = KAMIHIME_DIR + "restart_serafi.png"
        serafi_ul = KAMIHIME_DIR + "serafi_ul.png"

        while datetime.datetime.now().hour != 4:
            self.raid_event()
            self.loop_cnt = 0
        self.start_game()
        loc = self.image.match_img(EVENT_INDEX)
        self.gui.click(loc)
        loc = self.image.match_img(union_event)
        self.gui.click(loc)
        loc = self.image.match_img(serafi)
        self.gui.click(loc)
        while self.loop_cnt < self.stop_time:
            loc = self.image.match_img(serafi_ul, timeout=2)
            self.gui.click(loc)
            loc = self.image.match_img(quest_serafi, timeout=2)
            self.gui.click(loc)
            png_list = [self.p_type, USE_ITEM]
            idx, loc = self.image.match_img(png_list, timeout=2)
            if idx == 1:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(self.p_type, timeout=2)
            if loc:
                self.gui.click(loc)
            loc = self.image.match_img(SELECT_FRIEND)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(GO_QUEST, pass_rate=MIDDLE_PASS_LATE)
                time.sleep(1)
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK)
            else:
                loc = self.image.match_img(ATTACK, timeout=2)
                if not loc:
                    time.sleep(30)
                    self.gui.click(loc)#error
            loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
            if loc_auto_off:
                self.gui.click(loc_auto_off)
                self.gui.click(loc_auto_off)
            self.gui.click(loc)
            time.sleep(30)
            loc = self.image.match_img(GO_MYPAGE, timeout=300)
            if loc:
                loc = self.image.match_img(OK, timeout=5, pass_rate=MIDDLE_PASS_LATE)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES)
                self.gui.click(loc)
                loc = self.image.match_img(NEXT_RES, timeout=2)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(restart_serafi)
                self.gui.click(loc)
                loc = self.image.match_img(USE_ITEM, timeout=2)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(OK, pass_rate=MIDDLE_PASS_LATE)
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(CANCEL, timeout=2)
                    if loc:
                        self.gui.click(loc)
            else:
                loc = self.image.match_img(CANCEL, timeout=2)
                self.gui.click(loc)
                loc = self.image.match_img(RETIRE)
                self.gui.click(loc)
                loc = self.image.match_img(quest_ultimate)
                self.gui.click(loc)
            self.loop_cnt += 1

    def change_party(self, p_num=None):
        hensei = KAMIHIME_DIR + "hensei.png"
        change_party = KAMIHIME_DIR + "change_party.png"
        p_1 = KAMIHIME_DIR + "p_1.png"
        p_2 = KAMIHIME_DIR + "p_2.png"
        p_3 = KAMIHIME_DIR + "p_3.png"
        p_4 = KAMIHIME_DIR + "p_4.png"
        p_5 = KAMIHIME_DIR + "p_5.png"
        p_6 = KAMIHIME_DIR + "p_6.png"
        p_9 = KAMIHIME_DIR + "p_9.png"
        if p_num is None:
            if self.p_type == FRIEND_FIRE:
                set_p = p_1
            elif self.p_type == FRIEND_WATER:
                set_p = p_2
            elif self.p_type == FRIEND_WIND:
                set_p = p_3
            elif self.p_type == FRIEND_THUNDER:
                set_p = p_4
            elif self.p_type == FRIEND_HOLY:
                set_p = p_5
            elif self.p_type == FRIEND_DARK:
                set_p = p_6
        elif p_num == 1:
            set_p = p_1
        elif p_num == 2:
            set_p = p_2
        elif p_num == 3:
            set_p = p_3
        elif p_num == 4:
            set_p = p_4
        elif p_num == 5:
            set_p = p_5
        elif p_num == 6:
            set_p = p_6
        elif p_num == 9:
            set_p = p_9

        self.__go_page(hensei, change_party)
        loc = self.image.match_img(change_party)
        self.gui.click(loc)
        loc = self.image.match_img(set_p, timeout=5)
        if loc:
            self.gui.click(loc)
        loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
        self.gui.click(loc)
        self.__go_page()

    def daily(self):
        ikkatsu = KAMIHIME_DIR + "ikkatsu.png"
        soubi = KAMIHIME_DIR + "soubi.png"
        soubi_kyouka = KAMIHIME_DIR + "soubi_kyouka.png"
        kyouka_genju = KAMIHIME_DIR + "kyouka_genju.png"
        kyouka_weapon = KAMIHIME_DIR + "kyouka_weapon.png"
        target_reinforce_1 = KAMIHIME_DIR + "target_reinforce_1.png"
        target_reinforce_2 = KAMIHIME_DIR + "target_reinforce_2.png"
        osusume = KAMIHIME_DIR + "osusume.png"
        kyoukasuru = KAMIHIME_DIR + "kyoukasuru.png"
        sarani_kyouka = KAMIHIME_DIR + "sarani_kyouka.png"
        kyouka_end = KAMIHIME_DIR + "kyouka_end.png"

        gacha = KAMIHIME_DIR + "gacha.png"
        other_gacha = KAMIHIME_DIR + "other_gacha.png"
        normal_gacha = KAMIHIME_DIR + "normal_gacha.png"
        gacha_hiku = KAMIHIME_DIR + "gacha_hiku.png"

        raid_quest = KAMIHIME_DIR + "raid_quest.png"
        quest_ep10 = KAMIHIME_DIR + "quest_ep10.png"
        standard_raid = KAMIHIME_DIR + "standard_raid.png"
        expert_raid = KAMIHIME_DIR + "expert_raid.png"
        saichousen = KAMIHIME_DIR + "saichousen.png"

        type_quest = KAMIHIME_DIR + "type_quest.png"
        quest_ep8 = KAMIHIME_DIR + "quest_ep8.png"
        quest_ep4 = KAMIHIME_DIR + "quest_ep4.png"
        quest_ep50 = KAMIHIME_DIR + "quest_ep50.png"

        quest_sozai = KAMIHIME_DIR + "quest_sozai.png"
        kamihime_kyoka = KAMIHIME_DIR + "kamihime_kyoka.png"
        

        mission = KAMIHIME_DIR + "mission.png"

        # reinforce
        if self.daily_passed == 0:
            for target in [kyouka_genju, kyouka_weapon]:
                self.__go_page(soubi, soubi_kyouka)
                loc = self.image.match_img(soubi_kyouka)
                self.gui.click(loc)
                loc = self.image.match_img(target)
                self.gui.click(loc)
                img_list = [target_reinforce_1, target_reinforce_2]
                idx, loc = self.image.match_img(img_list)
                self.gui.click(loc)
                while True:
                    loc = self.image.match_img(osusume)
                    self.gui.click(loc)
                    target_img = [kyoukasuru, kyouka_end]
                    idx, loc = self.image.match_img(target_img)
                    if idx == 1:
                        break
                    self.gui.click(loc)
                    loc = self.image.match_img(sarani_kyouka)
                    self.gui.click(loc)
                loc = self.image.match_img(CANCEL)
                self.gui.click(loc)
            self.daily_passed += 1
        elif self.daily_passed == 1:
            # gacha
            self.__go_page(gacha, other_gacha)
            loc = self.image.match_img(other_gacha)
            self.gui.click(loc)
            loc = self.image.match_img(normal_gacha)
            self.gui.click(loc)
            for i in range(10):
                loc = self.image.match_img(gacha_hiku, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                time.sleep(1)
            self.daily_passed += 1
        elif self.daily_passed == 2:
            # raid jihatsu
            self.__go_page(QUEST_TOP, raid_quest)
            loc = self.image.match_img(raid_quest)
            self.gui.click(loc)
            loc = self.image.match_img(self.target_type, timeout=3, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)
            loc = self.image.match_img(expert_raid)
            self.gui.click(loc)
            loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM, timeout=2)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
            for i in range(1):
                loc = self.image.match_img(SELECT_FRIEND, timeout=3)
                if not loc:
                    break
                self.gui.click(loc)
                loc = self.image.match_img(GO_QUEST, pass_rate=EASE_PASS_LATE)
                time.sleep(1)
                self.gui.click(loc)
                loc = self.image.match_img(CANCEL, timeout=30, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK, timeout=2)
                loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
                if loc_auto_off:
                    self.gui.click(loc_auto_off)
                    self.gui.click(loc_auto_off)
                self.gui.click(loc)
                loc = self.image.match_img(OK, timeout=300, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                next_loc = self.image.match_img(NEXT_RES, pass_rate=EASE_PASS_LATE)
                self.gui.click(next_loc)
                next_loc = self.image.match_img(NEXT_RES, timeout=1, pass_rate=EASE_PASS_LATE)
                if next_loc:
                    self.gui.click(next_loc)
                loc = self.image.match_img(saichousen, timeout=5, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(USE_ITEM, timeout=2)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                    self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
            self.__go_page()
            self.daily_passed += 1
        elif self.daily_passed == 3:
            for i in range(2):
                self.raid_event()
            self.daily_passed += 1
        elif self.daily_passed  == 4:
            # type quest
            for i in range(3):
                self.__go_page(QUEST_TOP, raid_quest)
                loc = self.image.match_img(type_quest)
                self.gui.click(loc)
                img_list = [quest_ep50]
                idx, loc = self.image.match_img(img_list)
                self.gui.click(loc)
                loc = self.image.match_img(USE_ITEM, timeout=2)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                    self.gui.click(loc)
                loc = self.image.match_img(SELECT_FRIEND)
                self.gui.click(loc)
                loc = self.image.match_img(GO_QUEST, pass_rate=EASE_PASS_LATE)
                time.sleep(1)
                self.gui.click(loc)
                loc = self.image.match_img(ATTACK)
                loc_auto_off = self.image.match_img(AUTO_OFF, timeout=1)
                if loc_auto_off:
                    self.gui.click(loc_auto_off)
                    self.gui.click(loc_auto_off)
                self.gui.click(loc)
                self.image.match_img(NEXT_RES, timeout=300)
                self.__go_page()
            self.daily_passed += 1
        elif self.daily_passed == 5:
            self.change_party(9)
            self.__go_page(QUEST_TOP, raid_quest)
            loc = self.image.match_img(quest_sozai)
            self.gui.click(loc)
            loc = self.image.match_img(kamihime_kyoka)
            self.gui.click(loc)
            loc = self.image.match_img(expert_raid)
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM, timeout=2)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
            loc = self.image.match_img(SELECT_FRIEND)
            self.gui.click(loc)
            loc = self.image.match_img(GO_QUEST, pass_rate=EASE_PASS_LATE)
            time.sleep(1)
            self.gui.click(loc)
            loc = self.image.match_img(ATTACK)
            self.gui.click(loc)
            self.image.match_img(NEXT_RES, timeout=300)
            loc = self.image.match_img(OK, timeout=2)
            if loc:
                self.gui.click(loc)
            self.__go_page()
            self.daily_passed += 1
        elif self.daily_passed == 6:
            loc = self.image.match_img(mission)
            self.gui.click(loc)
            for i in range(2):
                loc = self.image.match_img(ikkatsu)
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                time.sleep(2)
            self.daily_passed = False
        else:
            self.logger.info("Daily passed index %s is unknown", str(self.daily_passed))
            self.daily_passed = False

    def auto_simple(self):
        saichousen = KAMIHIME_DIR + "saichousen.png"
        loc = self.image.match_img(saichousen, timeout=5, pass_rate=EASE_PASS_LATE)
        self.gui.click(loc)
        img_list = [USE_ITEM, CANCEL, OK]
        idx, loc = self.image.match_img(img_list, timeout=2, pass_rate=MIDDLE_PASS_LATE)
        while loc:
            if idx == 0:
                self.gui.click(loc)
                loc = self.image.match_img(OK, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                break
            else:
                self.gui.click(loc)
                idx, loc = self.image.match_img(img_list, timeout=1, pass_rate=MIDDLE_PASS_LATE)
        loc = self.image.match_img(SELECT_FRIEND)
        self.gui.click(loc)
        loc = self.image.match_img(GO_QUEST, pass_rate=EASE_PASS_LATE)
        time.sleep(1)
        self.gui.click(loc)
        loc = self.image.match_img(ATTACK)
        self.gui.click(loc)
        loc = self.image.match_img(NEXT_RES, timeout=300)
        while loc:
            self.gui.click(loc)
            loc = self.image.match_img(NEXT_RES, timeout=1)
        self.loop_cnt += 1

    def main(self):
        err_cnt = 0
        if self.target != "SI":
            self.open()
        while self.loop_cnt < self.stop_time:
            self.logger.info("Loop cnt: " + str(self.loop_cnt + 1))
            try:
                if self.target == "R":
                    self.raid_event()
                elif self.target == "K":
                    self.kourinsen()
                elif self.target == "EK":
                    self.event_kourinsen()
                elif self.target == "M":
                    self.meikyu()
                elif self.target == "S":
                    self.event_serafi()
                elif self.target == "D":
                    self.daily()
                    if not self.daily_passed:
                        break
                elif self.target == "SI":
                    self.auto_simple()
            except:
                self.logger.info("err")
                print(traceback.format_exc())
                err_cnt += 1
                if err_cnt > 10:
                    sys.exit(-1)
                self.start_game()

if __name__ == '__main__':
    ARGS = sys.argv
    print(ARGS[1])
    print(ARGS[2])
    TARGET = ARGS[1]
    STOP_TIME = None
    if ARGS[2] != "NONE":
        STOP_TIME = int(ARGS[2])
    P_NUM = int(ARGS[3])
    s = Kamihime(TARGET, STOP_TIME, P_NUM)
    s.main()
