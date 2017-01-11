# -*-coding:utf8-*-
import re
def run():
    text = open("clear.csv")
    output = open('clear_1.csv', 'w')
    # while(True):
    #     if text.readline():
    #         t = text.readline()
    #         if re.findall('(\(.*?\))', t, re.S):
    #             tt =t.replace(re.findall('(\(.*?\))', t, re.S)[0], '')
    #             output.writelines(tt)
    #         else:
    #             output.writelines(t)
    for i in range(90000):
        print i
        # t = text.readline()
        # if re.findall('(\(.*?\))', t, re.S):
        #     tt =t.replace(re.findall('(\(.*?\))', t, re.S)[0], '')
        #     output.writelines(tt)
        #     # print tt
        # else:
        #     output.writelines(t)
        #     # print t

        # # ------------------------------
        # print i
        # t = text.readline()
        # if re.findall('(\(.*?)', t, re.S):
        #     tt = t.replace(re.findall('(\(.*?)', t, re.S)[0], '')
        #     output.writelines(tt)
        #     # print tt
        # else:
        #     output.writelines(t)
        #     # print t
        # ----------------------------
        print i
        t = text.readline()
        if re.findall('\)', t, re.S):
            tt = t.replace(')', '')
            output.writelines(tt)
            # print tt

        else:
            output.writelines(t)
            # print t
        # ------------------------
        #     print i
        #     t = text.readline()
        #     if re.findall('([.*?])', t, re.S):
        #         tt =t.replace(re.findall('(\(.*?\))', t, re.S)[0], '')
        #         output.writelines(tt)
        #         # print tt
        #     else:
        #         output.writelines(t)
        #     #     # print t
run()