# coding=utf-8

from engine import Ctrip_schedule


if __name__ == '__main__':
    CS = Ctrip_schedule()
    CS.do_get_htl_and_rm_info = True
    CS.run()
