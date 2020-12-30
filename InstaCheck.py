from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


username = ''
password = ''
count = 0

def login(driver):
	#replace with web driver wait
	driver.find_element_by_name("username").send_keys(username)
	driver.find_element_by_name("password").send_keys(password)
	driver.find_element_by_name("password").send_keys(u'\ue007')

def click_button_with_css(driver, css_selector):
	element = WebDriverWait(driver, 20).until( #EC is expected condition
		EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))) #By is selecting stuff (specify which one u wanna use)
	element.click()

def nav_to_followers(driver):
	dropdown_css = "[alt*=\"" + username + "\"]"
	profile_css = "[href*=\"" + username + "\""
	click_button_with_css(driver, dropdown_css)
	click_button_with_css(driver, profile_css)

def close_post_notif_alert(driver):
	print ("hi")

def __main__():
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
	time.sleep(1)
	login(driver)
	try:
		nav_to_followers(driver)
	except: 
		close_css = "[class*=\"HoLwm\"]"
		click_button_with_css(driver, close_css)
		nav_to_followers(driver)

	followers_css = "[href*=\"" + username + "/followers/\"]"
	css_select_close = '[aria-label="Close"]'
	following_css = "[href*=\"" + username + "/following/\"]"

	click_button_with_css(driver, followers_css)
	followers_list = get_usernames_from_dialog(driver)

	click_button_with_css(driver, css_select_close)
	time.sleep(1)
	click_button_with_css(driver, following_css)
	following_list = get_usernames_from_dialog(driver)

	no_followbacks = nofollowback(followers_list, following_list)
	print("Not Following Back:\n------------")
	for i in range(len(no_followbacks)):
		print(no_followbacks[i])


def nofollowback(followers, following):
	followers.sort()
	following.sort()
	no_followback_list = []
	for i in range(len(following)):
		try:
			followers.index(following[i])
		except ValueError:
			no_followback_list += [following[i]]
	return no_followback_list

def check_difference_in_count(driver):
	global count 
	new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))

	if count != new_count:
		count = new_count
		return True
	else:
		return False

def get_usernames_from_dialog(driver):
	list_xpath = "//div[@role='dialog']//li"
	WebDriverWait(driver,20).until(
		EC.presence_of_element_located((By.XPATH, list_xpath)))
	scroll_down(driver)

	list_elems = driver.find_elements_by_xpath(list_xpath)
	time.sleep(1)

	users = []
	for i in range(len(list_elems)):
		try: 
			row_text = list_elems[i].text 
			if "Follow" in row_text:
				username = row_text[:row_text.index("\n")]
				users += [username]
		except:
			print("continue")
	return users

def scroll_down(driver):
	global count
	iter = 0
	while 1:
		scroll_top_num = str(iter * 1000)
		iter+=1
		driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop=" + scroll_top_num)

		try:
			WebDriverWait(driver, 1).until(check_difference_in_count)
		except: 
			count = 0
			break
__main__()