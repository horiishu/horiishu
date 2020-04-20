from .library import ImageOperation, WindowsGUI, CommonLogger
from enum import Enum
import time
import sys
import datetime
import traceback

ERR_PATH = "err\\"
PAN_MAX_SRC = "pan_max.png"
QUEST = "quest.png"
RETURN_QUEST_TOP = "quest_return.png"
START_QUEST = "start_quest.png"
SELECT_UNIT = "select_unit.png"
QUEST_RESULT = "quest_result.png"
CLOSE = "close.png"
S_CLOSE = "s_close.png"
CANCEL = "cancel.png"
ITEM = "item.png"
ITEM_BIHIN = "item_bihin.png"
USE_ITEM = "use_item.png"
USE_ITEM_CONFIRM = "use_item_confirm.png"
ITEM_CLOSE = "item_close.png"
RETURN_TOP_FROM_QUEST = "return_top_quest.png"
BATTLE_SPEED_SLOW = "battle_speel_slow.png"
RETURN_FROM_ISEKAI = "return_from_isekai.png"
UNIT_3 = "unit_3.png"
UNIT_6 = "unit_6.png"
MAINTAINANCE = "maintainance.png"
ITEM_PAGE_DOWN = "item_page_down.png"
RETURN_FROM_EVENT = "return_from_event.png"
NOR_PASS_LATE = 0.9
SEVER_PASS_LATE = 0.95
MIDDLE_PASS_LATE = 0.8
EASE_PASS_LATE = 0.70
EX_SEVERE_LATE = 0.97

class KanpaniGirls(object):
    def __init__(self, target, stop_time):
        self.image = ImageOperation()
        self.gui = WindowsGUI()
        self.logger = CommonLogger().common_logger()
        self.promote = False
        self.using_event_tiket = False
        self.first_round = False
        self.running_meikyu =False
        self.running_isekai = False
        self.target = target
        self.stop_time = stop_time
        self.round_cnt = 0

    def start_game(self, cash_crear=True, err=False, return_que=False):
        chrome_config = "chrome_config.png"
        config_history = "config_history.png"
        delete_history = "delete_history.png"
        tab_kanpani = "tab_kanpani.png"
        tab_kanpani_2 = "tab_kanpani_2.png"
        browser_refresh = "browser_refresh.png"
        start_icon = "game_start.png"
        saiyoushinai = "saiyoushinai.png"
        continue_quest = "continue_quest.png"
        meikyu_bottom = "meikyu_bottom.png"
        continue_isekai = "continue_isekai.png"
        isekai_saishutugeki = "isekai\\isekai_saishutugeki.png"
        quit_battle = "quit_battle.png"

        if cash_crear:
            loc = self.image.match_img(chrome_config, timeout=5, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)

                loc = self.image.match_img(config_history, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                loc = self.image.match_img(delete_history, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                loc = self.image.match_img(tab_kanpani_2, timeout=2, pass_rate=MIDDLE_PASS_LATE)
                if not loc:
                    loc = self.image.match_img(tab_kanpani, timeout=2, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

        start_game_finish = False
        restart_cnt = 0
        while not start_game_finish:
            restart_cnt += 1
            if restart_cnt > 10:
                sys.exit(-1)
            loc = self.image.match_img(browser_refresh, timeout=5, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            time.sleep(10)
            loc = self.image.match_img(start_icon, timeout=30)
            if loc:
                self.gui.click(loc)
                time.sleep(3)

                for i in range(10):
                    if self.image.match_img(QUEST, timeout=5):
                        start_game_finish = True
                        break
                    loc_saiyou = self.image.match_img(saiyoushinai, timeout=3)
                    if loc_saiyou:
                        self.gui.click(loc_saiyou)
                        start_game_finish = True
                        time.sleep(5)
                        break
                    if err and self.running_isekai:
                        if return_que:
                            loc_return_que = self.image.match_img(quit_battle)
                            self.gui.click(loc_return_que)
                            loc = self.image.match_img(RETURN_QUEST_TOP)
                            self.gui.click(loc)
                            start_game_finish = True
                            break
                        loc_isekai = self.image.match_img(continue_isekai)
                        if loc_isekai:
                            self.gui.click(loc_isekai)
                            loc_saishutugeki = self.image.match_img(isekai_saishutugeki, timeout=480)
                            if loc_saishutugeki:
                                err = False
                            break
                    if self.running_isekai:
                        loc_return_isekai = self.image.match_img(quit_battle)
                        if loc_return_isekai:
                            self.gui.click(loc_return_isekai)
                            start_game_finish = True
                            break
                    loc_continue = self.image.match_img(continue_quest, timeout=3)
                    if loc_continue:
                        self.gui.click(loc_continue)
                        loc_select = self.image.match_img(meikyu_bottom, timeout=10, pass_rate=EASE_PASS_LATE)
                        if loc_select:
                            self.gui.click(loc_select)
                        self.end_quest(timeout=300)
                        start_game_finish = True
                    loc_maintainance = self.image.match_img(MAINTAINANCE, timeout=2)
                    if loc_maintainance:
                        self.logger.info("Maintainance time")
                        sys.exit()
                    else:
                        self.gui.click(loc)

    def is_pan_max(self):
        pan_max_src = "pan_max.png"
        loc = self.image.match_img(pan_max_src, timeout=3)
        return loc

    def is_pan_runout(self, from_quest=True):
        pan_runaout = "pan_runout.png"

        if self.image.match_img(pan_runaout, timeout=2):
            img_list = [CLOSE, S_CLOSE]
            idx, loc = self.image.match_img(img_list, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)

            if from_quest:
                #loc = self.image.match_img(CANCEL)
                #self.gui.click(loc)

                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)

            return True
        return False

    def use_food(self, food_dir=''):
        food_1 = food_dir + "food_1.png"
        food_2 = food_dir + "food_2.png"

        loc = self.image.match_img(ITEM, timeout=30)
        time.sleep(5)
        self.gui.click(loc)
        loc = self.image.match_img(ITEM_BIHIN, timeout=2)
        if loc:
            self.gui.click(loc)
        loc = self.image.match_img(food_1, timeout=3)
        if not loc:
            if food_2:
                loc = self.image.match_img(food_2, timeout=3)
            if not loc:
                loc = self.image.match_img(ITEM_CLOSE, timeout=2)
                self.gui.click(loc)
                return -1
        self.gui.click(loc)

        loc = self.image.match_img(USE_ITEM, timeout=2)
        while loc:
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM_CONFIRM)
            if not loc:
                break
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM, timeout=2)

        loc = self.image.match_img(ITEM_CLOSE, timeout=2)
        self.gui.click(loc)
        return 0

    def select_unit(self, unit_img=False):
        if unit_img:
            loc = self.image.match_img(unit_img, timeout=2, pass_rate=SEVER_PASS_LATE)
            if loc:
                self.gui.click(loc)
        loc = self.image.match_img(SELECT_UNIT)
        self.gui.click(loc)

    def start_meikyu(self):
        meikyu_img = "start_meikyu.png"
        meikyu_bottom = "meikyu_bottom.png"

        loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
        self.gui.click(loc)

        loc = self.image.match_img(RETURN_FROM_ISEKAI, timeout=3)
        if loc:
            self.gui.click(loc)

        if not self.running_meikyu:
            loc = self.image.match_img(RETURN_QUEST_TOP, pass_rate=SEVER_PASS_LATE)
            if loc:
                self.gui.click(loc)

            loc = self.image.match_img(meikyu_img, pass_rate=EASE_PASS_LATE)
            self.gui.click(loc)

        loc = self.image.match_img(START_QUEST)
        self.gui.click(loc)

        self.select_unit()

        loc = self.image.match_img(meikyu_bottom, timeout=50)
        self.gui.click(loc)

        loc = self.image.match_img(meikyu_bottom, timeout=3)
        if loc:
            self.gui.click(loc)

        self.running_meikyu = True
        time.sleep(150)

    def end_quest(self, timeout=100):
        promote = "promote.png"
        loc = self.image.match_img(QUEST_RESULT, timeout=timeout)
        self.gui.click(loc)
        # time.sleep(2)
        # self.gui.click(loc)
        # self.promote = bool(self.image.match_img(promote, timeout=2, pass_rate=EASE_PASS_LATE))
        # time.sleep(0.3)
        # self.gui.click(loc)
        # time.sleep(1)
        # if not self.promote:
        #     self.promote = bool(self.image.match_img(promote, timeout=1, pass_rate=EASE_PASS_LATE))
        # time.sleep(1)
        for i in range(10):
            if self.image.match_img(QUEST_RESULT, timeout=1):
                self.gui.click(loc)
            else:
                break
        if datetime.datetime.now().hour == self.stop_time:
            self.logger.info("Auto play end.")
            sys.exit()

    def round_meikyu(self):
        while not self.is_pan_max():
            self.start_meikyu()
            self.end_quest(timeout=150)
        self.running_meikyu = False

    def take_promote(self):
        start_promote = "start_promote.png"
        leona_pos = "leona_pos.png"
        shoushin_jirei = "shoushin_jirei.png"
        confirm = "confirm_shoushin.png"
        end_promotion = "end_promotion.png"
        return_top = "return_top_promote.png"

        cnt = 0
        while cnt < 5:
            loc = self.image.match_img(start_promote)
            self.gui.click(loc)

            leona_loc = self.image.match_img(leona_pos)
            loc = (leona_loc[0], leona_loc[1] - 50)
            self.gui.click(loc)

            loc = self.image.match_img(end_promotion, timeout=1)
            if loc:
                self.gui.click(loc)
                loc = self.image.match_img(return_top)
                self.gui.click(loc)
                time.sleep(1)
                self.promote = False
                break

            loc = self.image.match_img(shoushin_jirei)
            self.gui.click(loc)

            loc = self.image.match_img(confirm)
            self.gui.click(loc)

            for i in range(10):
                leona_loc = self.image.match_img(leona_pos)
                if not leona_loc:
                    self.gui.click(loc)
                    time.sleep(1)
                else:
                    break

            cnt+= 1

    def prepare_isekai(self):
        isekai_dir = "isekai\\"
        shutugekijunbi = isekai_dir + "shutugekijunbi.png"
        page_down = isekai_dir + "page_down.png"
        stare_100 = isekai_dir + "stare_100.png"
        stare_100_selected = isekai_dir + "stare_100_selected.png"
        stare_89 = isekai_dir + "stare_89.png"
        stare_89_selected = isekai_dir + "stare_89_selected.png"
        stare_80 = isekai_dir + "stare_80.png"
        stare_80_selected = isekai_dir + "stare_80_selected.png"
        stare_74 = isekai_dir + "stare_74.png"
        stare_74_selected = isekai_dir + "stare_74_selected.png"
        stare_69 = isekai_dir + "stare_69.png"
        stare_69_selected = isekai_dir + "stare_69_selected.png"
        stare_60 = isekai_dir + "stare_60.png"
        stare_60_selected = isekai_dir + "stare_60_selected.png"
        stare_59 = isekai_dir + "stare_59.png"
        stare_59_selected = isekai_dir + "stare_59_selected.png"
        stare_54 = isekai_dir + "stare_54.png"
        stare_54_selected = isekai_dir + "stare_54_selected.png"
        stare_29 = isekai_dir + "stare_29.png"
        stare_29_selected = isekai_dir + "stare_29_selected.png"
        shutugeki = isekai_dir + "shutugeki.png"
        isekaiheiku = isekai_dir + "isekaiheiku.png"

        target_stare = stare_54
        target_stare_selected = stare_54_selected

        loc = self.image.match_img(shutugekijunbi)
        self.gui.click(loc)

        img_list = [target_stare, target_stare_selected]
        stare_idx, stare_loc = self.image.match_img(img_list, timeout=1, pass_rate=SEVER_PASS_LATE)
        down_loc = self.image.match_img(page_down)

        loop_cnt = 0
        while stare_idx == -1:
            self.gui.click(down_loc)
            stare_idx, stare_loc = self.image.match_img(img_list, timeout=1, pass_rate=SEVER_PASS_LATE)
            loop_cnt += 1
            if loop_cnt > 20:
                return -1

        self.gui.click(stare_loc)

        loc = self.image.match_img(shutugeki)
        self.gui.click(loc)

        loc = self.image.match_img(UNIT_6, timeout=2, pass_rate=SEVER_PASS_LATE)
        if loc:
            self.gui.click(loc)

        loc = self.image.match_img(isekaiheiku)
        self.gui.click(loc)

    def isekai(self):
        isekai_dir = "isekai\\"
        isekai = isekai_dir + "isekai.png"
        isekai_gekiha = isekai_dir + "isekai_gekiha.png"
        isekai_saishutugeki = isekai_dir + "isekai_saishutugeki.png"
        isekai_all_down = isekai_dir + "isekai_all_down.png"

        loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
        self.gui.click(loc)

        if not self.running_isekai:
            self.running_isekai = True
            loc = self.image.match_img(isekai, timeout=3, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)

        if self.prepare_isekai() == -1:
            self.logger.info("prepare isekai failed")
            raise ValueError

        while True:
            for i in range(1):
                loc = self.image.match_img(BATTLE_SPEED_SLOW)
                if loc:
                    time.sleep(3)
                    self.gui.click(loc)

            img_list = [isekai_gekiha, isekai_all_down]
            idx, loc = self.image.match_img(img_list, timeout=600)
            if idx == 0:
                time.sleep(3)
                self.gui.click(loc)
            else:
                self.logger.info("!! All down !!")
                loc = self.image.match_img(isekai_all_down)
                self.start_game(return_que=True)
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                self.prepare_isekai()
                continue

            self.round_cnt += 1

            if self.round_cnt % 10 == 0:
                self.logger.info("Round count: " + str(self.round_cnt))
                self.start_game()

                if self.is_pan_max():
                    self.logger.info("Stop round isekai")
                    break
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                self.prepare_isekai()
            else:
                loc_saishutugeki = self.image.match_img(isekai_saishutugeki)
                cnt = 0
                while not loc_saishutugeki and cnt < 3:
                    time.sleep(2)
                    self.gui.click(loc)
                    loc_saishutugeki = self.image.match_img(isekai_saishutugeki)
                self.gui.click(loc_saishutugeki)

        self.running_isekai = False

    def saiyou_event(self):
        saiyou_event_dir = "20190614_saiyou_event\\"
        event_is_here = saiyou_event_dir + "event_is_here.png"
        event_top = saiyou_event_dir + "event_top.png"
        quest_saiyou = saiyou_event_dir + "quest_saiyou.png"
        shikenkaijou_tiket = saiyou_event_dir + "shikenkaijou.png"
        if not self.using_event_tiket:
            self.first_round = True
            loc = self.image.match_img(ITEM)
            self.gui.click(loc)
            loc = self.image.match_img(ITEM_BIHIN, timeout=2)
            if loc:
               self.gui.click(loc)

            try:
                loc = self.image.match_img(shikenkaijou_tiket, timeout=5)
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM)
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM_CONFIRM)
                self.gui.click(loc)

                self.using_event_tiket = True
            except:
                loc = self.image.match_img(ITEM_CLOSE, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

        while True:
            if (not self.using_event_tiket or
               (self.using_event_tiket and not self.first_round)):
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                if self.first_round:
                    loc = self.image.match_img(RETURN_FROM_ISEKAI, timeout=3)
                    if loc:
                        self.gui.click(loc)
                    loc = self.image.match_img(event_is_here, timeout=2)
                    if loc:
                        self.gui.click(loc)

                    loc = self.image.match_img(event_top, timeout=2)
                    if loc:
                        self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            if loc:
                self.gui.click(loc)
            else:
                # tiket time out
                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)
                break

            if self.is_pan_runout():
                break
            self.select_unit(UNIT_3)
            time.sleep(30)
            self.end_quest()
            self.first_round = False

        self.using_event_tiket = False

    def renkin(self):
        renkin_dir = "renkin\\"
        event_is_here = renkin_dir + "event_is_here.png"
        event_top = renkin_dir + "event_top.png"
        quest_kacho = renkin_dir + "quest_kacho.png"
        tiket = renkin_dir + "ticket.png"
        if not self.using_event_tiket:
            self.first_round = True
            loc = self.image.match_img(ITEM)
            self.gui.click(loc)
            loc = self.image.match_img(ITEM_BIHIN, timeout=2)
            if loc:
               self.gui.click(loc)

            try:
                loc = self.image.match_img(tiket, timeout=5)
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM)
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM_CONFIRM)
                self.gui.click(loc)

                self.using_event_tiket = True
            except:
                loc = self.image.match_img(ITEM_CLOSE, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

        while True:
            if (not self.using_event_tiket or
               (self.using_event_tiket and not self.first_round)):
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                if self.first_round:
                    loc = self.image.match_img(RETURN_FROM_ISEKAI, timeout=3)
                    if loc:
                        self.gui.click(loc)
                    loc = self.image.match_img(event_is_here, timeout=5)
                    if loc:
                        self.gui.click(loc)

                    loc = self.image.match_img(event_top, timeout=2)
                    if loc:
                        self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            if loc:
                self.gui.click(loc)
            else:
                # tiket time out
                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)
                break

            if self.is_pan_runout():
                break
            self.select_unit(UNIT_3)
            time.sleep(30)
            self.end_quest()
            self.first_round = False

        self.using_event_tiket = False

    def misterio(self):
        misteri_dir = "misterio\\"
        open_misterio = misteri_dir + "open_misterio.png"
        quest = misteri_dir + "misterio_quest.png"
        uub_que = misteri_dir + "uub_quest.png"
        quest_bucho = misteri_dir + "quest_bucho.png"
        quest_kacho = misteri_dir + "quest_kacho.png"
        quest_cho = misteri_dir + "quest_cho.png"
        quest_bucho_select = misteri_dir + "quest_bucho_select.png"

        first_round = True

        while True:
            # if self.promote:
            #     self.take_promote()

            if first_round:
                loc = self.image.match_img(open_misterio, timeout=30)
                self.gui.click(loc)

                loc = self.image.match_img(quest)
                self.gui.click(loc)

                loc = self.image.match_img(uub_que, timeout=8)
                if loc:
                    self.gui.click(loc)

                # loc = self.image.match_img(quest_bucho, timeout=2)
                # if loc:
                #     self.gui.click(loc)
            else:
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            self.gui.click(loc)

            if self.is_pan_runout():
                break
            self.select_unit(UNIT_3)
            time.sleep(30)
            self.end_quest()

            first_round = False

    def quest_saigono_shiren(self):
        ichiryu_shacho_dir = "ichiryu_shacho\\"
        event_quest = ichiryu_shacho_dir + "event_quest.png"
        quest_main = ichiryu_shacho_dir + "quest_main.png"
        quest_5sho = ichiryu_shacho_dir + "quest_5sho.png"
        bottle = "bottle.png"
        first_round = True
        use_bottle = True
        while True:
            if self.promote:
                self.take_promote()
            if not use_bottle:
                loc = self.image.match_img(ITEM)
                self.gui.click(loc)
                loc = self.image.match_img(ITEM_BIHIN, timeout=2)
                if loc:
                    self.gui.click(loc)

                loc = self.image.match_img(bottle, timeout=5)
                if loc:
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(ITEM_PAGE_DOWN, timeout=5)
                    self.gui.click(loc)
                    loc = self.image.match_img(bottle, timeout=5)
                    if loc:
                        self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM, timeout=3)
                if loc:
                    self.gui.click(loc)

                    loc = self.image.match_img(USE_ITEM_CONFIRM)
                    self.gui.click(loc)
                loc = self.image.match_img(ITEM_CLOSE, timeout=2)
                self.gui.click(loc)
                use_bottle = True
            loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            if first_round:
                loc = self.image.match_img(RETURN_QUEST_TOP, pass_rate=SEVER_PASS_LATE)
                if loc:
                    self.gui.click(loc)
                loc = self.image.match_img(quest_main, timeout=2)
                if loc:
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(quest_5sho)
                    self.gui.click(loc)
                first_round = False
            loc = self.image.match_img(START_QUEST)
            self.gui.click(loc)
            self.select_unit()
            time.sleep(30)
            self.end_quest()
            self.round_cnt += 1
            if self.round_cnt % 10 == 0:
                self.logger.info("ROUND: " + str(self.round_cnt))
                # if self.is_pan_max():
                #     break
            #if self.round_cnt % 40 == 0:
            #    use_bottle = False

    def quest_tiket(self):
        tiket = "tiket.png"
        quest_tiket = "quest_tiket.png"
        round_cnt = 0
        if not self.using_event_tiket:
            self.first_round = False
            loc = self.image.match_img(ITEM)
            time.sleep(5)
            self.gui.click(loc)
            loc = self.image.match_img(ITEM_BIHIN, timeout=2)
            if loc:
               self.gui.click(loc)

            loc = self.image.match_img(tiket, timeout=5)
            if loc:
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM)
                if loc:
                    self.first_round = True
                    self.gui.click(loc)

                    loc = self.image.match_img(USE_ITEM_CONFIRM)
                    self.gui.click(loc)
                    self.using_event_tiket = True
                else:
                    loc = self.image.match_img(ITEM_CLOSE, timeout=2)
                    self.gui.click(loc)
            else:
                loc = self.image.match_img(ITEM_CLOSE)
                self.gui.click(loc)
                sys.exit()

        while True:
            if not self.first_round:
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
            else:
                loc = self.image.match_img(RETURN_FROM_ISEKAI, timeout=3)
                if loc:
                    self.gui.click(loc)
            loc = self.image.match_img(START_QUEST)
            #loc = self.image.match_img(quest_tiket, timeout=2)
            #if loc:
            #    self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            if loc:
                self.gui.click(loc)
            else:
                # tiket time out
                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)
                break

            if self.is_pan_runout():
                break
            self.select_unit(UNIT_3)
            time.sleep(30)
            self.end_quest()
            self.first_round = False

        self.using_event_tiket = False
        return 0

    def turi(self):
        while True:
            loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
            self.gui.click(loc)
            loc = self.image.match_img(START_QUEST)
            self.gui.click(loc)
            self.select_unit()
            #self.gui.click(loc, time_c=10)
            self.end_quest(timeout=300)

    def item_minihuto_saiyo(self):
        saiyo_use_item = "saiyo_use_item.png"
        mini_huto = "mini_huto.png"
        kurohuto = "kurohuto.png"
        saiyo = "saiyo.png"
        while True:
            loc = self.image.match_img(saiyo_use_item)
            self.gui.click(loc)
            loc = self.image.match_img(mini_huto)
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM)
            self.gui.click(loc)
            loc = self.image.match_img(USE_ITEM_CONFIRM)
            self.gui.click(loc)
            for i in range(3):
                # loc_kuro_huto = self.image.match_img(kurohuto, timeout=1)
                # if loc_kuro_huto:
                #     sys.exit()
                # else:
                self.gui.click(loc)
                time.sleep(2)
            loc = self.image.match_img(saiyo)
            self.gui.click(loc)
            for i in range(3):
                loc_saiyo_use_item = self.image.match_img(saiyo_use_item, timeout=1)
                if not loc_saiyo_use_item:
                    self.gui.click(loc)
                else:
                    break

    def manekineko(self):
        event_dir = "20191012_manekineko\\"
        go_event_page = event_dir + "go_event_page.png"
        event_page = event_dir + "event_page.png"
        taiyaki_max = event_dir + "taiyaki_max.png"
        osonaesuru = event_dir + "osonaesuru.png"
        quest_index = event_dir + "quest_index.png"
        quest_minami_entrance = event_dir + "quest_minami_entrance.png"
        quest_minami_koumon = event_dir + "quest_minami_koumon.png"
        quest_kakyuusei = event_dir + "quest_kakyuusei.png"
        quest_wasure = event_dir + "quest_wasure.png"
        quest_jokyusei = event_dir + "quest_jokyusei.png"
        quest_kita_entrance = event_dir + "quest_kita_entrance.png"
        quest_kitakoumon = event_dir + "quest_kitakoumon.png"
        quest_nishituuro = event_dir + "quest_nishituuro.png"
        quest_oshioki = event_dir + "quest_oshioki.png"
        rare_emerage = event_dir + "rare_emerage.png"
        gokuun_index = event_dir + "gokuun_index.png"
        quest_rare = event_dir + "quest_rare.png"
        naderu = event_dir + "naderu.png"
        yes = event_dir + "yes.png"

        #target_quest = quest_minami_entrance
        #target_quest = quest_minami_koumon
        #target_quest = quest_wasure
        #target_quest = quest_jokyusei
        target_quest = quest_kita_entrance
        #target_quest = quest_kitakoumon
        #target_quest = quest_nishituuro
        target_quest = quest_oshioki

        cnt = 0
        while True:
            loc = self.image.match_img(go_event_page)
            self.gui.click(loc)
            loc = self.image.match_img(CLOSE, timeout=3)
            if loc:
                self.gui.click(loc)
            if cnt == 0:
                # loc = self.image.match_img(rare_emerage, timeout=1)
                # if loc:
                #     self.gui.click(loc)
                #     loc_event_page = self.image.match_img(event_page, timeout=1)
                #     while not loc_event_page:
                #         self.gui.click(loc)
                #         loc_event_page = self.image.match_img(event_page, timeout=1)
                #     target_quest = quest_rare
                # else:
                    # loc = self.image.match_img(naderu, timeout=1)
                    # if loc:
                    #     self.gui.click(loc)
                    #     loc = self.image.match_img(yes)
                    #     self.gui.click(loc)
                    #     loc = self.image.match_img(CLOSE)
                    #     self.gui.click(loc)
                loc = self.image.match_img(taiyaki_max, timeout=1)
                if loc:
                    self.gui.click(loc)
                    time.sleep(2)
                    loc = self.image.match_img(osonaesuru)
                    self.gui.click(loc)
            if target_quest == quest_rare:
                loc = self.image.match_img(gokuun_index, pass_rate=EX_SEVERE_LATE)
                if loc:
                    self.gui.click(loc)
                else:
                    loc = self.image.match_img(RETURN_FROM_EVENT)
                    self.gui.click(loc)
                    break
            if target_quest != quest_rare:
                loc = self.image.match_img(quest_index)
                self.gui.click(loc)
            loc = self.image.match_img(target_quest)
            self.gui.click(loc)
            if self.is_pan_runout(from_quest=False):
                loc = self.image.match_img(CLOSE, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(RETURN_FROM_EVENT)
                self.gui.click(loc)
                break
            self.select_unit(UNIT_3)
            self.end_quest()
            cnt += 1


    def ryza(self):
        ryza_dir = "20191125_ryza\\"
        event_page = ryza_dir + "event_page.png"
        quest_kamui = ryza_dir + "quest_kamui.png"
        accept_quest = ryza_dir + "accept_quest.png"
        quest_runaent = ryza_dir + "quest_runaent.png"
        irai = ryza_dir + "irai.png"
        quest_remarugia = ryza_dir + "quest_remarugia.png"
        quest_yugu = ryza_dir + "quest_yugu.png"
        quest_quoria = ryza_dir + "quest_quoria.png"
        quest_are = ryza_dir + "quest_are.png"
        while True:
            loc = self.image.match_img(event_page)
            self.gui.click(loc)
            if self.target == "KAMUI":
                loc = self.image.match_img(quest_kamui)
                self.gui.click(loc)
                loc = self.image.match_img(accept_quest)
                self.gui.click(loc)
            else:
                loc = self.image.match_img(quest_are)
                #loc = self.image.match_img(quest_yugu)
                #loc = self.image.match_img(quest_remarugia)
                #loc = self.image.match_img(quest_quoria)
                self.gui.click(loc)
                loc = self.image.match_img(accept_quest)
                self.gui.click(loc)
            if self.is_pan_runout(from_quest=False):
                loc = self.image.match_img(CLOSE)
                self.gui.click(loc)
                loc = self.image.match_img(RETURN_FROM_EVENT)
                self.gui.click(loc)
                break
            self.end_quest()

    def nanipani(self):
        nanipani_dir = "nanipani\\"
        nanipani_icon = nanipani_dir + "eve_page.png"
        nanipani_screen = nanipani_dir + "judge_quest_screen.png"
        skip = nanipani_dir + "skip.png"
        hamushi = nanipani_dir + "hamushi.png"
        confirm_rare = nanipani_dir + "yes_rare.png"
        confirm_hamushi = nanipani_dir + "yes.png"
        quest_left = nanipani_dir + "quest_left.png"
        quest_center = nanipani_dir + "quest_center.png"
        quest_right = nanipani_dir + "quest_right.png"
        quest_rare = nanipani_dir + "quest_rare.png"
        accept_quest = nanipani_dir + "accept_quest.png"
        return_top = nanipani_dir + "return_top.png"
        quest_emerage = nanipani_dir + "quest_emerage.png"
        quest_kouhan = nanipani_dir + "quest_kouhan.png"

        if self.target == "LEFT":
            run_quest = quest_left
        elif self.target == "CENTER":
            run_quest = quest_center
        elif self.target == "RIGHT":
            run_quest = quest_right
        elif self.target == "EMERAGE":
            run_quest == quest_emerage
        else:
            run_quest = quest_kouhan

        loc = self.image.match_img(nanipani_icon)
        self.gui.click(loc)

        loc = self.image.match_img(nanipani_screen, timeout=5)
        if not loc:
            img_list = [CLOSE, skip]
            idx, loc = self.image.match_img(img_list, timeout=2)
            if idx == 0:
                self.gui.click(loc)
            elif idx == 1:
                self.logger.info("Event  skipped")
                self.gui.click(loc)

        loc = self.image.match_img(quest_emerage, timeout=5)
        # if loc:
        #     run_quest = quest_emerage
        #     self.logger.info("!! Emerage quest !!")
        # else:
        loc = self.image.match_img(quest_rare, timeout=5, pass_rate=SEVER_PASS_LATE, get_val=True)
        if loc:
            run_quest = quest_rare
            self.logger.info("!! Rare quest !!")
        else:
            if run_quest != quest_kouhan:
                loc = self.image.match_img(hamushi, timeout=1)
                if loc:
                    self.gui.click(loc)
                    loc = self.image.match_img(confirm_hamushi, timeout=2)
                    self.gui.click(loc)
                    self.logger.info("!! Hamushi clicked !!")

        cnt = 1
        while True:
            loc = self.image.match_img(run_quest)
            if not loc:
                loc = self.image.match_img(CLOSE, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(run_quest)
            self.gui.click(loc)

            if (run_quest == quest_rare or run_quest == quest_emerage) and cnt == 1:
                loc = self.image.match_img(confirm_rare)
                self.gui.click(loc)

            accept_cnt = 0
            while True:
                accept_que_loc = self.image.match_img(accept_quest, timeout=3)
                if accept_que_loc:
                    self.gui.click(accept_que_loc)
                    break
                if accept_cnt > 3:
                    raise ValueError
                time.sleep(3)
                self.gui.click(loc)
                accept_cnt += 1

            if self.is_pan_runout(from_quest=False):
                loc = self.image.match_img(CANCEL)
                self.gui.click(loc)
                loc = self.image.match_img(CLOSE, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(return_top)
                self.gui.click(loc)
                break
            self.select_unit(UNIT_3)

            time.sleep(30)
            self.end_quest()

            # if (cnt == 5 or cnt == 10) and run_quest == quest_kouhan:
            #     self.use_food(haropani_dir)

            loc = self.image.match_img(nanipani_icon)
            self.gui.click(loc)

            loc = self.image.match_img(nanipani_screen, timeout=5)
            if not loc:
                loc = self.image.match_img(skip, timeout=2)
                if loc:
                    self.gui.click(loc)

                loc = self.image.match_img(CLOSE, timeout=2, pass_rate=MIDDLE_PASS_LATE)
                if loc:
                    self.gui.click(loc)

            cnt += 1

    def jobpani(self):
        jobpani_dir = "jobpani\\"
        event_page = jobpani_dir + "event_page.png"
        jobpani_screen = jobpani_dir + "jobpani_screen.png"
        skip = jobpani_dir + "skip.png"
        accept_quest = jobpani_dir + "accept_quest.png"
        return_top = jobpani_dir + "return_top.png"
        quest_index = jobpani_dir + "quest_index.png"

        loc = self.image.match_img(event_page)
        self.gui.click(loc)

        loc = self.image.match_img(jobpani_screen, timeout=5)
        if not loc:
            img_list = [CLOSE, skip]
            idx, loc = self.image.match_img(img_list, timeout=2)
            if idx == 0:
                self.gui.click(loc)
            elif idx == 1:
                self.logger.info("Event  skipped")
                self.gui.click(loc)

        cnt = 1
        while True:
            loc = self.image.match_img(quest_index , pass_rate=0.98)
            if not loc:
                img_list = [CLOSE, skip]
                idx, loc = self.image.match_img(img_list, timeout=2)
                if idx == 0:
                    self.gui.click(loc)
                elif idx == 1:
                    self.logger.info("Event  skipped")
                    self.gui.click(loc)
                cnt += 1
                if cnt > 3:
                    self.logger.error("cannnot find quest index")
                    raise ValueError
                continue
            self.gui.click(loc)

            loc = self.image.match_img(accept_quest, timeout=3)
            self.gui.click(loc)

            if self.is_pan_runout(from_quest=False):
                loc = self.image.match_img(CLOSE, pass_rate=EASE_PASS_LATE)
                self.gui.click(loc)
                loc = self.image.match_img(return_top)
                self.gui.click(loc)
                break
            self.select_unit(UNIT_3)

            time.sleep(30)
            self.end_quest()

            loc = self.image.match_img(event_page)
            self.gui.click(loc)

            self.image.match_img(jobpani_screen, timeout=5)

            cnt += 1

    def main(self):
        pan_max_cnt = 0
        restart_cnt = 0
        use_food_item = False
        food_dir = ""
        while True:
            try:
                if not self.using_event_tiket:
                    if self.target == "ISEKAI":
                        self.isekai()
                        pass
                    elif self.target == "SUBEVENT":
                        self.turi()
                    else:
                        if use_food_item:
                            if self.use_food(food_dir) == -1:
                                use_food_item = False
                                sys.exit(-1)
                        else:
                            self.round_meikyu()
                            pass
                    pan_max_cnt += 1
                    self.logger.info("PAN MAX: " + str(pan_max_cnt))
                    if self.stop_time == -1:
                        sys.exit()
                #self.misterio()
                #self.nanipani()
                #self.saiyou_event()
                #self.renkin()
                self.jobpani()
            except ValueError:
                self.using_event_tiket = False
                print(traceback.format_exc())
                restart_cnt += 1
                if restart_cnt >= 10:
                    sys.exit(-1)
                self.logger.info("RESTART: " + str(restart_cnt))
                filename = ERR_PATH + str(restart_cnt) + "_err_cap.png"
                self.image.get_capture(filename=filename)
                self.start_game(err=True)

if __name__ == '__main__':
    ARGS = sys.argv
    print(ARGS[1])
    print(ARGS[2])
    TARGET = ARGS[1]
    STOP_TIME = None
    if ARGS[2] != "NONE":
        STOP_TIME = int(ARGS[2])
    s = KanpaniGirls(TARGET, STOP_TIME)
    s.main()
