# coding=utf8

from HotelInfo.engine import Ctrip_schedule


if __name__ == '__main__':
    print('******************************')
    print('*********携程数据抓取***********')
    print('******************************')
    while True:
        print('请选择内容\n\t1.城市列表爬取\n\t2.爬取各城市行政区\n\t3.爬取酒店列表\n\t4.采集酒店及房间数据\n\t\t输入\'n\'退出')
        CS = Ctrip_schedule()
        cin = input('请选择: >')
        if cin == '1':
            CS.do_get_code = True
            CS.run()
            print('抓取完毕...')
            break
        elif cin == '2':
            CS.do_get_city_info = True
            CS.run()
            print('抓取完毕...')
            break
        elif cin == '3':
            CS.do_get_hotel_list = True
            CS.run()
            print('抓取完毕...')
            break
        elif cin == '4':
            CS.do_get_htl_and_rm_info = True
            CS.run()
            print('抓取完毕...')
            break
        elif cin == 'n':
            break
        else:
            print('****输入错误,重新输入****')
            continue