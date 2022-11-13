from time import sleep
from logger import printLog
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

def wait():
    # 等待页面响应函数
    sleep(5)


# 忽略无用的日志
options=webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

# 打开页面
print("# Step_1: 打开页面")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://eserv.cup.edu.cn/v2/matter/fill")

# 将handle切换到登录页
driver.switch_to.window(driver.current_window_handle)
wait()

driver.switch_to.frame(driver.find_element(By.ID, 'loginIframe'))

# 从 Accounts.txt 中读取账号密码
with open("Accounts.txt", 'r') as f:
    rawData = f.read()
    account = rawData.split(' ')[0]
    password = rawData.split(' ')[1]

# 登录教务平台
print("\n# Step_2: 登录教务平台")
try:
    acc_ipt = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[6]/input[1]')
    pwd_ipt = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[6]/input[2]')

    acc_ipt.send_keys(account)
    pwd_ipt.send_keys(password)

    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[6]/div[3]').click()
except Exception:
    print("! Exception: 登录出错，请检查登录信息是否正确")
    printLog("登录出错，请检查登录信息是否正确", True)
    exit(1)

wait()

# 将handle切换到当前页面
driver.switch_to.window(driver.current_window_handle)

# 筛选填报服务为'学生每日填报'
print("\n# Step_3: 筛选填报服务为'学生每日填报'")
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/ul/li[1]/div/div/input').click()
wait()
driver.find_element(By.XPATH, '/html/body/div[last()]/div[1]/div[1]/ul/li[5]').click()
wait()
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/ul/li[2]/button[1]').click()
wait()

# 进入表单
print("\n# Step_4: 进入表单")
try:
    form = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[3]/div/div[2]/ul/li[1]')
except NoSuchElementException:
    print("! Exception: 无表单可填报")
    printLog("无表单可填报", True)
    exit(0)
else:
    form.click()

# 表单加载比较久，多等一会
sleep(10)

# 开始填报
print("\n# Step_5: 开始填报")
try:
    print("\t- 今日是否在京在校集中住宿: ", end='')
    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[4]/td[2]/div/div[1]/div/div/div['
                                  '1]/input').click()
    wait()
    driver.find_element(By.XPATH, '/html/body/div[last()-1]/div[1]/div[1]/ul/li[1]').click()
    wait()
    print('是')

    print("\t- 今日在校期间是否离校？: ", end='')
    driver.find_element(By.XPATH,
                        '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[4]/td[4]/div/div[1]/div[1]/div[1]').click()
    wait()
    driver.find_element(By.XPATH, '/html/body/div[last()]/div[1]/div[1]/ul/li[1]').click()
    wait()
    print("否，未离校")

    print("\t- 本人今日体温范围: ", end='')
    driver.find_element(By.XPATH,
                        '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[12]/td[2]/div/div[1]/div/div/div/input').click()
    wait()
    driver.find_element(By.XPATH, '/html/body/div[last()]/div[1]/div[1]/ul/li[1]').click()
    wait()
    print("37.3℃以下")

    print("\t- 获取地理位置: ", end='')
    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[11]/td[4]/div/div[1]/div/span').click()
    wait()

    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[11]/td[4]/div/div[1]/div[2]/div/ul['
                                  '3]/li[1]/div/span[3]').click()
    wait()

    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[11]/td[4]/div/div[1]/div[2]/div/div['
                                  '1]/span[11] ').click()
    wait()

    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[11]/td[4]/div/div[1]/div[2]/div/div[3]'
                                  '/textarea').send_keys('城北街道清秀园(南区)中国石油大学润杰公寓')
    wait()

    driver.find_element(By.XPATH, '//*[@id="pageBox"]/div[2]/div/table/tbody/tr[11]/td[4]/div/div[1]/div['
                                  '2]/span/button[2]').click()
    wait()
    print("城北街道清秀园(南区)中国石油大学润杰公寓")


except Exception as e:
    print("! Exception: 填报出错")
    printLog("填报出错\n" + str(e), True)
    exit(1)

# 确认信息
print("\n# Step_6: 确认信息")
try:
    driver.find_element(By.ID, '1753_Radio_197_0').click()
    wait()

    driver.find_element(By.XPATH, '/html/body/div[last()-1]/div/div[2]/div/div[2]/a').click()
    wait()
except Exception as e:
    print("! Exception: 确认信息出错")
    printLog("确认信息出错\n" + str(e), True)
    exit(1)

# 提交
print("\n# Step_7: 提交表单")
try:
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/button').click()
    sleep(5)
except Exception as e:
    print("! Exception: 提交信息出错")
    printLog("提交信息出错\n" + str(e), True)
    exit(1)

# 关闭
print("\n### 已成功填报 ###")
printLog("已成功填报", False)
exit(0)
