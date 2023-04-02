from selenium import webdriver
from selenium.webdriver.common.by import By
import time

account=input("请输入账号:")
password=input("请输入密码:")
seat=input("请输入要占的座位号:")
if(len(seat)==2):
    seat='0'+seat


opt = webdriver.ChromeOptions()   #创建浏览
driver = webdriver.Chrome(options=opt)  #创建浏览器对象

while(True):
    try:
        driver.get("http://seatlib.gxmzu.edu.cn/") #打开图书馆预约网页
        break
    except:
        time.sleep(1)
        continue
#模拟登陆行为
driver.find_element(By.XPATH,"/html/body/div[1]/span/div[4]/div/div/div[1]/div/div/form/div[1]/div/div/span/span/input").send_keys(account)
driver.find_element(By.XPATH,"/html/body/div[1]/span/div[4]/div/div/div[1]/div/div/form/div[2]/input").send_keys(password)

#没有登陆成功,等待,周期为0.5秒
while(driver.current_url!="http://seatlib.gxmzu.edu.cn/home"):
    time.sleep(0.5)
try:
    driver.get("http://seatlib.gxmzu.edu.cn/UserInfo")
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/a").click()
    time.sleep(3)
    driver.switch_to.alert.accept()
    print("初始化完成")
except:
    print("初始化完成")

#获取预约座位的url
times=0
while(True):
    times+=1
    print("循环累计: "+str(times)+"次.")
    data="{}/{}/{}".format(time.localtime(time.time())[0],time.localtime(time.time())[1],time.localtime(time.time())[2])
    url="http://seatlib.gxmzu.edu.cn/BookSeat/order_today_order?date="+data+"&roomNo=201014&roomName=%E7%9B%B8%E6%80%9D%E6%B9%96%E9%A6%862%E6%A5%BC%E8%A5%BF%E5%8C%BA&seatNo=201014"+seat+"&seatShortNo="+seat

    #打开确认预约的界面
    try:
        driver.get(url)
    except:
        continue
    #模拟预约行为
    driver.find_element(By.XPATH,"/html/body/div/div[3]/button").click()
    time.sleep(5)
    try:
        if("座位预约成功" in driver.switch_to.alert.text):
            driver.switch_to.alert.accept()
        else:
            driver.switch_to.alert.accept()
            continue
    except:
        continue

    #每隔29分钟(1740秒)自动续约
    time.sleep(1740)

    #取消预约座位
    driver.get("http://seatlib.gxmzu.edu.cn/UserInfo")
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/a").click()
    time.sleep(5)
    try:
        driver.switch_to.alert.accept()
    except:
        continue
driver.close()
