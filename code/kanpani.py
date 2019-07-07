from .library import ImageOperation, WindowsGUI, CommonLogger
from enum import Enum
import time
import sys
import datetime

ERR_PATH = "err\\"
PAN_MAX_SRC = "pan_max.png"
QUEST = "quest.png"
RETURN_QUEST_TOP = "quest_return.png"
START_QUEST = "start_quest.png"
SELECT_UNIT = "select_unit.png"
QUEST_RESULT = "quest_result.png"
CLOSE = "close.png"
ITEM = "item.png"
USE_ITEM = "use_item.png"
USE_ITEM_CONFIRM = "use_item_confirm.png"
ITEM_CLOSE = "item_close.png"
RETURN_TOP_FROM_QUEST = "return_top_quest.png"
BATTLE_SPEED_SLOW = "battle_speel_slow.png"
NOR_PASS_LATE = 0.9
SEVER_PASS_LATE = 0.95
MIDDLE_PASS_LATE = 0.8
EASE_PASS_LATE = 0.75

class KanpaniGirls(object):
    def __init__(self, target, stop_time):
        self.image = ImageOperation()
        self.gui = WindowsGUI()
        self.logger = CommonLogger().common_logger()
        self.promote = False
        self.using_event_tickt = False
        self.first_round = False
        self.running_meikyu =False
        self.running_isekai = False
        self.target = target
        self.stop_time = stop_time

    def start_game(self, cash_crear=True, err=False):
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
        isekai_saishutugeki = "isekai_saishutugeki.png"
        if cash_crear:
            loc = self.image.match_img(chrome_config, timeout=5)
            if loc:
                self.gui.click(loc)

                loc = self.image.match_img(config_history, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                loc = self.image.match_img(delete_history)
                self.gui.click(loc)

                loc = self.image.match_img(tab_kanpani_2, timeout=2)
                if not loc:
                    loc = self.image.match_img(tab_kanpani, timeout=2)
                self.gui.click(loc)

        start_game_finish = False
        while not start_game_finish:
            loc = self.image.match_img(browser_refresh, timeout=5)
            self.gui.click(loc)
            time.sleep(10)
            loc = self.image.match_img(start_icon, timeout=30)
            if loc:
                self.gui.click(loc)
                time.sleep(3)

                for i in range(30):
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
                        loc_isekai = self.image.match_img(continue_isekai)
                        if loc_isekai:
                            self.gui.click(loc_isekai)
                            loc_saishutugeki = self.image.match_img(isekai_saishutugeki, timeout=480)
                            if loc_saishutugeki:
                                err = False
                            break
                    loc_continue = self.image.match_img(continue_quest, timeout=3)
                    if loc_continue:
                        self.gui.click(loc_continue)
                        loc_select = self.image.match_img(meikyu_bottom, timeout=10, pass_rate=EASE_PASS_LATE)
                        if loc_select:
                            self.gui.click(loc_select)
                        self.end_quest(timeout=300)
                        start_game_finish = True
                    else:
                        self.gui.click(loc)

    def is_pan_max(self):
        pan_max_src = "pan_max.png"
        loc = self.image.match_img(pan_max_src, timeout=3, pass_rate=SEVER_PASS_LATE)
        return loc

    def is_pan_runout(self, from_quest=True):
        pan_runaout = "pan_runout.png"
        cancel = "cancel.png"

        if self.image.match_img(pan_runaout, timeout=2):
            loc = self.image.match_img(CLOSE)
            self.gui.click(loc)

            if from_quest:
                loc = self.image.match_img(cancel)
                self.gui.click(loc)

                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)

            return True
        return False

    def start_meikyu(self):
        meikyu_img = "start_meikyu.png"
        meikyu_bottom = "meikyu_bottom.png"

        loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
        self.gui.click(loc)

        if not self.running_meikyu:
            loc = self.image.match_img(RETURN_QUEST_TOP, pass_rate=SEVER_PASS_LATE)
            if loc:
                self.gui.click(loc)

            loc = self.image.match_img(meikyu_img, pass_rate=EASE_PASS_LATE)
            self.gui.click(loc)

        loc = self.image.match_img(START_QUEST)
        self.gui.click(loc)

        loc = self.image.match_img(SELECT_UNIT)
        self.gui.click(loc)

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
        time.sleep(3)
        self.gui.click(loc)
        time.sleep(0.3)
        self.gui.click(loc)
        #self.promote = bool(self.image.match_img(promote, timeout=1, pass_rate=EASE_PASS_LATE))
        time.sleep(1)
        for i in range(5):
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

            cnt+= 1

    def prepare_isekai(self):
        shutugekijunbi = "shutugekijunbi.png"
        page_down = "page_down.png"
        stare_50 = "stare_50.png"
        shutugeki = "shutugeki.png"
        isekaiheiku = "isekaiheiku.png"

        loc = self.image.match_img(shutugekijunbi)
        self.gui.click(loc)

        loc = self.image.match_img(page_down)
        self.gui.click(loc)

        loc = self.image.match_img(stare_50)
        self.gui.click(loc)

        loc = self.image.match_img(shutugeki)
        self.gui.click(loc)

        loc = self.image.match_img(isekaiheiku)
        self.gui.click(loc)

    def isekai(self):
        isekai = "isekai.png"
        isekai_gekiha = "isekai_gekiha.png"
        isekai_saishutugeki = "isekai_saishutugeki.png"

        round_cnt = 0

        loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
        self.gui.click(loc)

        if not self.running_isekai:
            self.running_isekai = True
            loc = self.image.match_img(isekai, timeout=5)
            if loc:
                self.gui.click(loc)

        self.prepare_isekai()

        while True:
            time.sleep(20)
            for i in range(3):
                loc = self.image.match_img(BATTLE_SPEED_SLOW)
                if loc:
                    time.sleep(1)
                    self.gui.click(loc)
            time.sleep(60)

            loc = self.image.match_img(isekai_gekiha, timeout=600)
            time.sleep(3)
            self.gui.click(loc)

            round_cnt += 1

            if round_cnt % 5 == 0:
                self.logger.info("Round count: " + str(round_cnt))
                self.start_game()

                if round_cnt >= 40:
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

    def yomepani(self):
        yomepani_dir = "20190601_yomepani\\"
        yomepani_icon = yomepani_dir + "yomepani.png"
        skip = yomepani_dir + "skip.png"
        get_reword = "close.png"
        hamushi = yomepani_dir + "hamushi.png"
        quest_emerage = yomepani_dir + "quest_emerage.png"
        quest_rare = yomepani_dir + "rare_quest.png"
        confirm_rare = yomepani_dir + "yes.png"
        quest_entrance = yomepani_dir + "entrance.png"
        quest_openteras = yomepani_dir + "openteras.png"
        quest_hanamichi = yomepani_dir + "shukuhukunohanamichi.png"
        quest_oironaoshi = yomepani_dir + "oironaoshi.png"
        kacho_level = yomepani_dir + "kacho_level.png"
        shunin_level = yomepani_dir + "shunin_level.png"
        accept_quest = yomepani_dir + "accept_quest.png"
        return_top = yomepani_dir + "return_top.png"
        hamushi = yomepani_dir + "hamushi_3.png"

        run_quest = quest_openteras

        loc = self.image.match_img(yomepani_icon)
        self.gui.click(loc)
        time.sleep(5)

        loc = self.image.match_img(skip, timeout=5)
        if loc:
            self.gui.click(loc)

        loc = self.image.match_img(get_reword, timeout=2)
        if loc:
            self.gui.click(loc)

        # loc = self.image.match_img(quest_emerage, timeout=4)
        # if loc:
        #     run_quest = quest_emerage
        #     self.logger.info("!! Emerage quest !!")
        # else:
        loc = self.image.match_img(hamushi, timeout=20)
        if loc:
            self.gui.click(loc)
            loc = self.image.match_img(confirm_rare, timeout=2)
            self.gui.click(loc)
            self.logger.info("!! Hamushi clicked !!")
            # else:
            #     loc = self.image.match_img(quest_rare, timeout=4)
            #     if loc:
            #         run_quest = quest_rare
            #         self.logger.info("!! Rare quest !!")

        cnt = 1
        while True:
            loc = self.image.match_img(run_quest)
            self.gui.click(loc)

            # if run_quest == quest_rare or run_quest == quest_emerage and cnt == 1:
            #     loc = self.image.match_img(confirm_rare)
            #     self.gui.click(loc)
            # elif run_quest == quest_oironaoshi:
            #     loc = self.image.match_img(shunin_level)
            #     self.gui.click(loc)

            loc = self.image.match_img(accept_quest)
            self.gui.click(loc)

            loc = self.image.match_img(SELECT_UNIT)
            self.gui.click(loc)

            if self.is_pan_runout():
                loc = self.image.match_img(CLOSE)
                self.gui.click(loc)
                loc = self.image.match_img(return_top)
                self.gui.click(loc)
                break

            time.sleep(30)
            self.end_quest()

            if self.promote:
                self.take_promote()

            loc = self.image.match_img(yomepani_icon)
            self.gui.click(loc)

            loc = self.image.match_img(skip, timeout=5)
            if loc:
                self.gui.click(loc)

            loc = self.image.match_img(get_reword, timeout=3)
            if loc:
                self.gui.click(loc)

            cnt += 1

    def saiyou_event(self):
        saiyou_event_dir = "20190614_saiyou_event\\"
        event_is_here = saiyou_event_dir + "event_is_here.png"
        event_top = saiyou_event_dir + "event_top.png"
        quest_saiyou = saiyou_event_dir + "quest_saiyou.png"
        shikenkaijou_tickt = saiyou_event_dir + "shikenkaijou.png"
        if not self.using_event_tickt:
            self.first_round = True
            loc = self.image.match_img(ITEM)
            self.gui.click(loc)

            loc = self.image.match_img(shikenkaijou_tickt, timeout=5)
            if loc:
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM)
                self.gui.click(loc)

                loc = self.image.match_img(USE_ITEM_CONFIRM)
                self.gui.click(loc)

                self.using_event_tickt = True
            else:
                loc = self.image.match_img(ITEM_CLOSE)
                self.gui.click(loc)

        while True:
            if (not self.using_event_tickt or
                (self.using_event_tickt and not self.first_round)):
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

                if self.first_round:
                    self.logger.info(event_is_here)
                    loc = self.image.match_img(event_is_here)
                    self.gui.click(loc)

                    loc = self.image.match_img(event_top)
                    self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            if loc:
                self.gui.click(loc)
            else:
                loc = self.image.match_img(RETURN_TOP_FROM_QUEST)
                self.gui.click(loc)
                break

            loc = self.image.match_img(SELECT_UNIT)
            self.gui.click(loc)

            if self.is_pan_runout():
                break
            time.sleep(30)
            self.end_quest()
            self.first_round = False

        self.using_event_tickt = False

    def pajapani(self):
        pajapani_dir = "20190701_pajapani\\"
        pajapani_icon = pajapani_dir + "pajapani.png"
        pajapani_screen = pajapani_dir + "judge_quest_screen.png"
        skip = pajapani_dir + "skip.png"
        get_reword = "close.png"
        hamushi = pajapani_dir + "hamushi.png"
        confirm_rare = pajapani_dir + "yes.png"
        quest_left = pajapani_dir + "quest_left.png"
        quest_center = pajapani_dir + "quest_center.png"
        quest_right = pajapani_dir + "quest_right.png"
        quest_rare = pajapani_dir + "quest_rare.png"
        accept_quest = pajapani_dir + "accept_quest.png"
        return_top = pajapani_dir + "return_top.png"
        hamushi = pajapani_dir + "hamushi3.png"
        hamushi2 = pajapani_dir + "hamushi2.png"

        if self.target == "LEFT":
            run_quest = quest_left
        elif self.target == "CENTER":
            run_quest = quest_center
        elif self.target == "RIGHT":
            run_quest = quest_right
        else:
            self.logger.info("Unknown target")
            run_quest = quest_center

        loc = self.image.match_img(pajapani_icon)
        self.gui.click(loc)

        loc = self.image.match_img(pajapani_screen, timeout=5)

        loc = self.image.match_img(skip, timeout=5)
        if loc:
            self.logger.info("Event  skipped")
            self.gui.click(loc)

        loc = self.image.match_img(get_reword, timeout=2)
        if loc:
            self.gui.click(loc)

        # loc = self.image.match_img(quest_rare, timeout=3)
        # if loc:
        #     run_quest = quest_rare
        #     self.logger.info("!! Rare quest !!")
        # else:
        # loc = self.image.match_img(hamushi, timeout=30)
        # if loc:
        #     self.gui.click(loc)
        #     loc = self.image.match_img(confirm_rare, timeout=2)
        #     self.gui.click(loc)
        #     self.logger.info("!! Hamushi clicked !!")

        cnt = 1
        while True:
            loc = self.image.match_img(run_quest)
            self.gui.click(loc)

            if run_quest == quest_rare and cnt == 1:
                loc = self.image.match_img(confirm_rare)
                self.gui.click(loc)

            loc = self.image.match_img(accept_quest)
            self.gui.click(loc)

            loc = self.image.match_img(SELECT_UNIT)
            self.gui.click(loc)

            if self.is_pan_runout(from_quest=False):
                loc = self.image.match_img(CLOSE)
                self.gui.click(loc)
                loc = self.image.match_img(return_top)
                self.gui.click(loc)
                break

            time.sleep(30)
            self.end_quest()

            loc = self.image.match_img(pajapani_icon)
            self.gui.click(loc)
            loc = self.image.match_img(pajapani_screen, timeout=5)

            loc = self.image.match_img(skip, timeout=3, pass_rate=MIDDLE_PASS_LATE)
            if loc:
                self.gui.click(loc)

            loc = self.image.match_img(get_reword, timeout=2)
            if loc:
                self.gui.click(loc)

            cnt += 1

    def misterio(self):
        misteri_dir = "misterio\\"
        open_misterio = misteri_dir + "open_misterio.png"
        quest = misteri_dir + "misterio_quest.png"
        uub_que = misteri_dir + "uub_quest.png"
        quest_bucho = misteri_dir + "quest_bucho.png"
        quest_kacho = misteri_dir + "quest_kacho.png"
        quest_bucho_select = misteri_dir + "quest_bucho_select.png"

        first_round = True

        while True:
            if self.promote:
                self.take_promote()

            if first_round:
                loc = self.image.match_img(open_misterio, timeout=30)
                self.gui.click(loc)

                loc = self.image.match_img(quest)
                self.gui.click(loc)

                loc = self.image.match_img(uub_que)
                self.gui.click(loc)

                loc = self.image.match_img(quest_kacho, timeout=2)
                if loc:
                    self.gui.click(loc)
            else:
                loc = self.image.match_img(QUEST, timeout=30, pass_rate=MIDDLE_PASS_LATE)
                self.gui.click(loc)

            loc = self.image.match_img(START_QUEST)
            self.gui.click(loc)

            loc = self.image.match_img(SELECT_UNIT)
            self.gui.click(loc)

            if self.is_pan_runout():
                break
            time.sleep(30)
            self.end_quest()

            first_round = False

    def main(self):
        pan_max_cnt = 0
        restart_cnt = 0
        while True:
            try:
                if not self.using_event_tickt:
                    if self.target == "ISEKAI":
                        self.isekai()
                    else:
                        self.round_meikyu()
                    pan_max_cnt += 1
                    self.logger.info("PAN MAX: " + str(pan_max_cnt))
                    if self.stop_time == -1:
                        sys.exit()
                self.pajapani()
            except ValueError:
                restart_cnt += 1
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
