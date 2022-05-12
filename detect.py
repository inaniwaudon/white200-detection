import cv2 
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

url = "https://tumoiyorozu.github.io/white200/"
screen_png = "screen.png"

def click(x, y):
  actions = ActionChains(driver)
  actions.move_to_element_with_offset(driver.find_element_by_tag_name('html'), 0, 0)
  actions.move_by_offset(x, y)
  actions.click()
  actions.perform()

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome()
driver.get(url)

# set a scale
driver.execute_script("document.body.style.zoom='70%'")
size = 1680 * 0.7
driver.set_window_size(size, size)

# take screenshot
def detect(result_name):
  driver.save_screenshot(screen_png)
  img = cv2.imread(screen_png)
  height, width, _ = img.shape
  inverted = cv2.bitwise_not(img)

  gray = cv2.cvtColor(inverted, cv2.COLOR_BGR2GRAY)
  _, binary = cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  get_color = lambda x, y: "#" + "".join([hex(i)[2:] for i in [img[y][x][2], img[y][x][1], img[y][x][0]]])

  box_miny = 10000
  for i, c in enumerate(contours):
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 50:
      continue
    
    if rect[1] < box_miny:
      x = int(rect[0] + rect[2] / 2)
      y = int(rect[1] + rect[3] / 2)
      box_miny = rect[1]
      base_color = get_color(x, y)
      base_color_i = i
    
  print(f"target color: {base_color}")

  for i, c in enumerate(contours):
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 50:
      continue

    x = int(rect[0] + rect[2] / 2)
    y = int(rect[1] + rect[3] / 2)
    c = get_color(x, y)
    cv2.putText(img,
      text = c,
      org=(x - 30, y - 10),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=0.6,
      color=(0, 0, 0),
      lineType=cv2.LINE_AA)

    if base_color == c and i != base_color_i:
      img = cv2.drawContours(img, contours, i, (255, 0, 0), 5)
      click(x / 2, y / 2)
    else:
      img = cv2.drawContours(img, contours, i, (0, 255, 0), 5)
    
  cv2.imwrite(result_name, img)
  print(f"saved image: {result_name}")

# click the start button
print("start the tutorial")
btn_pos = driver.find_element_by_id("start_btn").location
click(btn_pos["x"] / 0.7 / 2, btn_pos["y"] / 0.7 / 2)
detect("detect0.png")

# click the next button
print("start the performance")
btn_pos = driver.find_element_by_class_name("start_btn").location
click(btn_pos["x"] / 0.7 / 2, btn_pos["y"] / 0.7 / 2)
detect("detect1.png")
