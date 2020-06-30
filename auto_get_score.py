from time import sleep
import json
import sys
import io

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as bf


def save_and_load(username):
	try:
		u = open('user.json')
	except:
		u = open('user.json','w')
		user_info = {}
		json.dump(user_info,u)
		u.close()
		u = open('user.json')
	
	user_info = json.load(u)
	u.close()
	if username in user_info:
		your_password = user_info[username]
	else:
		your_password = str(input('请输入密码：'))
		choose = input('是否记住密码？\n')
		y = ['yes','y','Y','Yes','是','对']
		if choose in y:
			user_info[username] = your_password
			with open('user.json','w') as u:
				json.dump(user_info,u)
			print('已保存')
	
	return your_password

def get_score():

	#改变标准输出的默认编码
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

	#建立Phantomjs浏览器对象，
	browser = webdriver.PhantomJS()
	# ~ r''
	# ~ phantomjs.exe在你的电脑上的路径可有可无
	# ~ 没有的前提是你把它添加到环境变量之中了
	
	#登录页面
	login_url = r'http://111.207.101.93:8080/tqweb/login.jsp?login'

	# 访问登录页面
	browser.get(login_url)

	# 等待一定时间，让js脚本加载完毕
	# ~ browser.implicitly_wait(5)
	sleep(2)

	#输入用户名
	your_name = input('请输入姓名：')
	username = browser.find_element_by_name('j_username')
	username.send_keys(your_name)

	'''##############################################################'''
	
	#输入密码
	your_password = save_and_load(your_name)
	password = browser.find_element_by_name('j_password')
	password.send_keys(your_password)

	#等一会儿要不然怕登不上去
	sleep(1)
	
	#点击“登录”按钮
	login_button = browser.find_element_by_name('btnsubmit')
	login_button.submit()
	
	#网页源代码
	code = browser.page_source#.encode('utf-8').decode()
	
	###从中挑选出有用的信息###
	
	#查找并打印考试名称
	html = bf(code, 'html.parser')
	values = html.find_all(name = 'a', attrs={'class': 'text_lb'})
	print('请选择要查询成绩的考试')
	for i, value in enumerate(values):
		print(int(i)+1, '.\t', value.get_text())
	
	#选择要查看的考试
	while True:
		
		w = int(input('\n选择：'))
		
		if w >= 1 and w <= len(values):
			exam_xpath = '//*[@id="stu"]/ul/li[' + str(w) + ']/table/tbody/tr[1]/td[2]/a'
			l = browser.find_element_by_xpath(exam_xpath)
			ActionChains(browser).move_to_element(l).click(l).perform()
			break
		else:
			print('没有该考试！')
			continue
	
	#等一会儿要不然怕没加载完
	sleep(1)
	
	#网页截图
	browser.save_screenshot('%s%s%s%s'%(your_name, '_', values[w-1].\
		get_text(),'成绩.jpg'))
	
	#等一会儿要不然怕没截完
	sleep(1)
	
	#退出登录
	exit_xpath = '/html/body/div[1]/div/div[2]/dt[3]/a/img'
	l = browser.find_element_by_xpath(exit_xpath)
	ActionChains(browser).move_to_element(l).click(l).perform()
	
	'''##############################################################'''
	
	#退出浏览器
	browser.quit()

get_score()
