# -*-coding:utf8-*-

class Base(object):
    def __init__(self):
        print 'constructor of Base is called'

    def __del__(self):
        print 'Destructor of Base is called'

    def move(self):
        print 'move called in Base'

class SubA(Base):
    def __init__(self):
        print 'constructor of SbuA is called'
        #重构了自己的构造函数

    def move(self):
        print 'move called in SubA'
        #重构了自己的成员函数
class SubB(Base):
    def __del__(self):
        print 'destructor of SubB is called'
        super(SubB, self).__del__()
        #重构了自己的析构函数 ，super是访问父类成员 ，引用方法是 super(subClassName,self)

instA = SubA()
instA.move()
del instA

print '-*50'

instB = SubB()
instB.move()
del instB

#move()在 instA和instB中展现不同的行为，这种现象是 多态