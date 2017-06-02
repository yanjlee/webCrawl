# coding=utf8

from Scence.engine import qunar

if __name__ == '__main__':
    print('******************')
    print('****景区信息采集****')
    print('******************')
    CHECK = True
    while CHECK:
        print('请选择OTA：\n\t1.去哪儿网\n\t\t输n退出')
        ipt = input('请选择 >')
        if ipt == '1':
            qnr = qunar()
            print('请选择采集类型\n\t1.景区目录采集\n\t2.景去信息采集\n\t3.景区评论采集\n\t\t输n退出')
            ipt2 = input('请选择>')
            if ipt2 == '1':
                print('开始景区目录采集...')
                qnr.run()
                break
            elif ipt2 == '2':
                print('开始景区信息采集...')
                qnr.run_sight()
                break
            elif ipt2 == '3':
                print('开始景区评论采集...')
                qnr.run_comment()
            elif ipt2 == 'n':
                CHECK = False
            else:
                continue
        elif ipt == 'n':
            CHECK = False
        else:
            continue
