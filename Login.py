from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import requests
import cv2
import numpy as np
from PIL import Image
from selenium.webdriver import ActionChains


def get_track(distance):
	track = []
	current = 0
	mid = distance * 3 / 4
	t = 0.2
	v = 0
	while current < distance:
		if current < mid:
			a = 2
		else:
			a = -3
		v0 = v
		v = v0 + a * t
		move = v0 * t + 1 / 2 * a * t * t
		current += move
		track.append(round(move))
	return track

def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    save_path = os.path.abspath('.') + '\\' + 'img'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    img_path = save_path + '\\' + '{}.png'.format(type)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path



caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}

def _cut_slider(path):
    """
    滑块切割
    :return:
    """
    image = Image.open(path)
    x = []
    y = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pix = image.load()[i, j]
            if pix != 255:
                x.append(i)
                y.append(j)
    z = (np.min(x), np.min(y), np.max(x), np.max(y))
    result = image.crop(z)
    result.convert('RGB').save(path)
    # result.show()
    return result.size[0], result.size[1]


# 读取账号
f = open("./users.txt")
line = f.readline()
login_url = 'https://m.iqiyi.com/user.html#baseLogin'


#BMPserver = Server(r'D:\Anaconda3\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
#BMPserver.start()
#BMPproxy = BMPserver.create_proxy()

#chrome_options = Options()
#chrome_options.add_argument('--proxy-server={0}'.format(BMPproxy.proxy))

driver = webdriver.Chrome(desired_capabilities=caps)
count = 0
while line:
    print(line)
    user_name = line.split('----')[0]
    password = line.split('----')[1]
    # 声明调用哪个浏览器，使用的是Chrome，其他浏览器同理

    driver.get(login_url)
    #BMPproxy.new_har("tupian", options={'captureContent': True, 'captureContent': True})
    '''
    result = BMPproxy.har
    print(result)
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        # 根据URL找到数据接口
        if "/slidecode/bg/" in _url:
            _response = entry['response']
            _content = _response['content']['text']
            # 获取接口返回内容
            print(_content)
            '''
    #time.sleep(2)
    #time.sleep(3)
    wait = ui.WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element_by_css_selector('#phoneNumber'))


    input_cover = driver.find_element_by_css_selector('body > div.m-pc-resetBg > div:nth-child(2) > form > section > div:nth-child(1) > div:nth-child(1) > div > div > div:nth-child(3) > div')
    if input_cover.size['height']!=0:
        driver.execute_script("document.querySelector('body > div.m-pc-resetBg > div:nth-child(2) > form > section > div:nth-child(1) > div:nth-child(1) > div > div > div:nth-child(3)').style.display='none'")
        driver.execute_script("document.querySelector('body > div.m-pc-resetBg > div:nth-child(2) > form > section > div:nth-child(1) > div:nth-child(1) > div > div > div:nth-child(2)').style.display='block'")
    input_usr = driver.find_element_by_css_selector('#phoneNumber')
    input_pwd = driver.find_element_by_css_selector('div.input_wrap.detial-info > input')
    input_usr.clear()
    input_usr.send_keys(user_name)

    input_pwd.send_keys(password)
    confirm_btn = driver.find_element_by_css_selector("#baselogin-loginbtn").click()

    wait = ui.WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element_by_css_selector('#h5-slide-wrap > div > div > div.slide-modal > div.jigsaw > div > canvas'))
    canva = driver.find_element_by_css_selector("#h5-slide-wrap > div > div > div.slide-modal > div.jigsaw > div > canvas")

    bg_savepath = './img/img_'+str(count)+'.png'
    canva.screenshot(bg_savepath)
    time.sleep(5)

    request_log = driver.get_log('performance')
    slide_url = None
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        # .get() 方式获取是了避免字段不存在时报错
        request = message.get('request')
        if (request is None):
            continue

        _url = request.get('url')

        if ('secpic.iqiyi.com//20210204/slidecode/icon/' in _url):
            # 得到requestId
            print(_url)
            slide_url = _url
            print(message['requestId'])
            # 通过requestId获取接口内容
            content = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
            print(content)
            break
    # 下载
    save_path = '.\\img'
    slider_path = _pic_download(slide_url, 'slider_'+str(count))
    captcha_path = bg_savepath
    # 去除开头部分
    template = cv2.imread(captcha_path)[:,52:]
    target = cv2.imread(slider_path)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    cv2.imwrite(temp, template)
    while True:
        template = cv2.imread(temp)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = abs(255 - template)
        cv2.imwrite(temp, template)
        w, h = _cut_slider(targ)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        # 调用PIL Image 做测试
        image = Image.open(captcha_path)

        xy = (y, x, y + w, x + h)
        # 切割
        imagecrop = image.crop(xy)
        # 保存切割的缺口
        imagecrop.convert('RGB').save(save_path + '\\' + "new_image.jpg")
        #imagecrop.show()
        print(y)
        if y!=0:
            break

    distance = y + 52
    slider_button = driver.find_element_by_css_selector('#test')# 找到“滑块”
    action = ActionChains(driver)# 实例化一个action对象
    action.click_and_hold(slider_button).perform()# perform()用来执行ActionChains中存储的行为
    track = get_track(distance)
    for i in track:
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        action.reset_actions()
    time.sleep(0.5)
    action.release().perform()


    #driver.close()
    line = f.readline()
    count += 1
    time.sleep(1000)
    #driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)

f.close()
#BMPserver.stop()
driver.quit()
