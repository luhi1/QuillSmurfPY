import nltk.tokenize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import nltk

timeout = 5

def main():
    nltk.download('punkt_tab')
    print("Welcome to Quill Smurf!\n")
    inputText = input("Enter text to paraphrase:")
    inputTextArray = nltk.tokenize.sent_tokenize(inputText)
    sortedInputTextArray = []
    pSentence = inputTextArray[0]
    i = 1
    while i < len(inputTextArray):
        if len(pSentence.split(" ")) + len(inputTextArray[i].split(" ")) < 125:
            pSentence = pSentence + " " + inputTextArray[i]
            i += 1
        else:
            sortedInputTextArray.append(pSentence)
            pSentence = ""
    sortedInputTextArray.append(pSentence)
    print("This bot just saved you " + str(len(sortedInputTextArray)) + " copy and paste sequence(s).")
    browser = setupBrowser()
    for i in range (0,len(sortedInputTextArray)):
        writeQB(browser, sortedInputTextArray[i])
        if ((i+1) % 3 == 0) or (i == 9):
            browser.quit()
        if ((i+1) % 3 == 0):
            browser = setupBrowser()

def setupBrowser():
    uOptions = Options()
    uOptions.add_argument("--window-size=1920,1200")
    #uOptions.add_argument("--headless")
    uOptions.set_preference("browser.download.folderList", 2)
    uOptions.set_preference("browser.download.dir", "C:\\Users\\walrus\\Desktop\\QuillSmurfPY\\results")
    browser = webdriver.Firefox(options=uOptions)
    browser.get('https://quillbot.com/paraphrasing-tool')

    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@title="Sign in with Google Dialog"]')))
    browser.switch_to.frame(browser.find_element(By.XPATH,'//iframe[@title="Sign in with Google Dialog"]'))
    browser.find_element(By.ID, "close").click()
    browser.switch_to.parent_frame()
    return browser

def writeQB(browser, text):
    input = browser.find_element(By.ID, "paraphraser-input-box")
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)
    input.send_keys(text)  

    pButton = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='pphr/input_footer/paraphrase_button']")))
    while (not(EC.staleness_of(pButton)(browser))):
        pButton.click()

    refresh = False
    try:
        while (WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/input_footer/rephrase_button']"))).get_attribute("disabled") == "true"):
            WebDriverWait(browser, 0.5)

    except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
        pass

    exportButton = WebDriverWait(browser,timeout).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/output_footer/export_button']")))
    WebDriverWait(browser, timeout).until(EC.element_to_be_clickable(exportButton))
    browser.execute_script("arguments[0].click();", exportButton)
    
    #Eventually, check if the file is in the results folder, don't use the janky QB indicator.
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='root-client']/div/div[4]/div/div/div[2]/div/button"))).click()
    except TimeoutException:
        pass

if __name__ == "__main__":
    main()