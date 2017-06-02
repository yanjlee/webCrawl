
***
>> 反爬虫措施:

* 在[欣欣旅游](http://lxs.cncn.com)这个网站ban了ip，迟迟不恢复，只能用代理ip来解决，每一次请求都先拿一个可以用的ip去请求 
* 在[完美志愿](http://www.wmzy.com)这个网站的同考分去向数据抓取时候，通过post请求，data嵌入到cookies里，因此每次页面请求都是通过调用cookies参数来输出内容 
***

>> 问题总结:

* (03.22)关于 os 这个模块.
        
		os.path.join(path,name)   #连接目录与文件名或目录 结果为path/name
		os.path.abspath(path)    #显示当前绝对路径
		os.path.split(path)  #将path分割成路径名和文件名。
* (03.20)对于需要一个list如何如何，用完一定要重置，不然要发生错乱。
* (03.10)关于变量

		class TestClass():
			val1 = xxx  		#这个是类变量,由 类名 直接调用,也可以又对象来调用
			def __init__(self):
				self.val2 = xxx #这个是成员变量,可又类的对象来调用,self的含义就是代表实例对象
			def function(self):
				vale = xxx 	#不是成员变量,只是function的内部变量
			# 没有在构造函数里初始化的变量就算带self都不算成员变量
* (03.10)对于类的调用时

		#先定义了一个session对象
		class session():
			def __init__(self):
				self.session = requests.session()
			def xxxx(self):
				r = self.session.get(xxx)
			....
		#错误的调用方法
		class A():
			def run():
				response = session.xxxx()
			#这里会报错,说 A中没有 session这个属性,原因是仅仅是调用方法,self.session还没有生成
		#正确的方法
		class B():
			def run():
				rs = session() #先实例化session这个对象，构造函数才会被调用
				rs.xxxxx()     #此时就正确调用了
* (03.10)对于网页中的数据是unicode形式，提取出阿里要转换成中文就应该这样.
		
		t1 = xxxx.encode('utf-8') #其转换为utf-8
		t2 = t1.decode('unicode-escape') #将其转换为中文了
如果是gbk方式的,那就
		
		t1 = xxxx.encode('raw_unicode_escape')
		t2 = t1.decode('utf-8')
* (03.08)安装scrapy时,windows上要安装vc code,linux要报错 scripts/sign-file.c:23:30: fatal error: openssl/opensslv.h,ubuntu下缺少了部分如下的组件，安装一下即可
	
		sudo apt-get install libssl-dev
* (03.08)对于错误,输出可以这样

		try:
			xxxxx
		except Exception as e:
			print(e)
			time.sleep(60)
* (03.07)写脚本的时候,要遵循面向对象的原则,不要随意的继承,重写,以及类的唯一性
* (03.03)python有个自动卸载 pip install pip-autoremove
* (03.03)对于jupyter notebook不能用python情况

		python2 -m pip install ipykernel
		python2 -m ipykernel install --user

		python3 -m pip install ipykernel
		python3 -m ipykernel install --user
* (03.02)终于实现知乎的登录，通过获取cookies是行不通的，因为xsrf的不同。然后拿到新浪的api，在查询过程中

		api_params = {
    			'type': 'all',# 三种模式
    			'queryVal': '四川旅游', #搜索词条
    			'title': '四川旅游',
    			'containerid': '100103type=1&q=四川旅游',
    			'page': 15 #页数
		}
		#api地址
		url = 'http://m.weibo.cn/container/getIndex'		
* (03.01)关于代理ip

		url1: http://www.kuaidaili.com/free
		url2: http://www.xicidaili.com/nn
		#使用方法
		proxy = {
			'http/https': 'http/https://xx.xx.xx:xxx'
		}
		#请求的时候放入requests里，单个爬虫用1-2个代理，多了回报错
		#同时，选错proxy ip 程序也会停，应该是该代理不可用
* (02.28)对于import对象时,Python3开始，import 默认只做absolute import。也就是说pack包内的__init__.py中如果有一句import my_package，Python3会去找一个叫my_package的包，而不会去找pack.my_package包。

		try:
			from . import xxx
		except:
			from package import xxx
* (02.28)保存图片时

		from urllib import request
		request.urlretrieve(url, filename='路径/名字.xx')
* (02.28)保存文档时

		xx = open('xxx', 'wt', newline='', encodig='utf-8')
		# r 读, w 写，a 追加
		wiht open('xxxx', 'w') as f:
			f.write(xxxx)
* (02.28)对于requests中text和content的对比，text是xxxin unicode，而content是xxxin bytes
* (02.28)在构造headers过程中,host能不要放在外面就不要放在外面,但是对于通用爬虫还是要放外面的.

		host = 'xxx.xxx.com'
		header = {
			'host': host,			
			'xxxx': 'xxx'
		}
* (02.28)在python3 中,如果在文件的__init__文档里写模块,在正常的脚本里不能调用,还没想明白
		from . import xxx
* 在安装Python3后，pip就指代3，如果安装py2相关的要使用pip2才行，为了规范化，3->pip3,2->pip2 这样就不容易错
* '@'符号用作函数修饰符，必须出现在函数定义前一行，不允许和函数定义在同一行。只可以在模块或类定义层内对函数进行修饰，不允许修修饰一个类。一个修饰符就是一个函数，它将被修饰的函数做为参数，并返回修饰后的同名函数或其它可调用的东西。
* 实用的角度，for循环是嵌套在while里，如果反了，遇到break是整个循环停了，造成麻烦
* 在使用 if xx is xx： 的时候， 英文字符串可以直接is，中文还是要用 ==
* 在使用多线程抓取数据时候，会出现bug，我使用的
		
		from multiprocessing.dummy import Pool
因为在 pool.map()所传递的是一个列表里的元素。当分线程执行时，遇到self.这类的变量就会不知所措
* 在定制请求头的时候，Host与网页不同，会发生重定向错误。 比如 host:college.gaokao.com 网页是www.gaokao.com 就会产生错误
* 在遇到反爬策略是抓取内容乱码的情况下，可以一个脚本保存html，一个脚本读取,或者用
* 在遇到xpath抓取的数据是16进制时，要尝试解码，即 xxx.decode('utf-8')
* if xxxx: contuine 是个好东西
* 要会变通，xpath抓得有问题，可以靠 循环和regex来完成
* 在设置抓取规则上，灵活设置，反复抓取
* 数据在异常抛出过程中的处理，需要关注

***