from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import multiprocessing

def main():
    browsers = [setupBrowser(r'C:\Users\walrus\AppData\Roaming\Mozilla\Firefox\Profiles\9zb8tz51.default')]
    newBrowser: multiprocessing.pool.AsyncResult
    for i in range (0,10):
        if i % 3 == 0:
            pool = multiprocessing.Pool(processes=1) 
            newBrowser = pool.apply_async(setupBrowser, args = (r'C:\Users\walrus\Desktop\QuillSmurfPY'))
             
        writeQB(browsers[0], "Hi darling, I think you're really pretty and cool." + str(i+1))
        if (i+1) % 3 == 0:
            WebDriverWait(browsers[0], 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='root-client']/div/div[4]/div")))
            browsers[0].quit()
            del browsers[0]
            browsers[newBrowser.get()]
    WebDriverWait(browsers[0], 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='root-client']/div/div[4]/div")))
    browsers[0].quit()

#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
#multithreading makes me really happy 
def setupBrowser(profile):
    uOptions = Options()
    #uOptions.add_argument("--headless")
    uOptions.add_argument("--window-size=1920,1200")
    uOptions.add_argument("--profile")
    uOptions.add_argument(profile)
    uOptions.set_preference("browser.download.folderList", 2)
    uOptions.set_preference("browser.download.dir", "C:\\Users\walrus\Desktop\QuillSmurfPY")
    browser = webdriver.Firefox(options=uOptions)
    browser.get('https://quillbot.com/paraphrasing-tool')
    loadQB(browser) 
    return browser

def loadQB(browser):
    loadedIndicator = browser.find_element(By.XPATH, "//div[@id='root-client']/div[1]")
    while (loadedIndicator.get_attribute("style") != "--header-height: 53px; --banner-height: 68px;"):
        WebDriverWait(browser, 0.5)

    try:
        browser.switch_to.frame(browser.find_element(By.XPATH,'//iframe[@title="Sign in with Google Dialog"]'))
        browser.find_element(By.ID, "close").click()
        browser.switch_to.parent_frame()
    except NoSuchElementException:
        pass

def writeQB(browser, text):
    input = browser.find_element(By.ID, "paraphraser-input-box")
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)
    input.send_keys(text)  

    pButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='pphr/input_footer/paraphrase_button']")))
    while (not(EC.staleness_of(pButton)(browser))):
        pButton.click()

    refresh = False
    try:
        while (WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/input_footer/rephrase_button']"))).get_attribute("disabled") == "true"):
            WebDriverWait(browser, 0.5)

    except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
        pass

    exportButton = WebDriverWait(browser,20).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/output_footer/export_button']")))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(exportButton))
    browser.execute_script("arguments[0].click();", exportButton)

if __name__ == "__main__":
    main()