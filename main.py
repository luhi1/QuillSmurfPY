from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import nltk
import nltk.tokenize
import os 

#To Do:
#Sort the final output to not just be on one line.

'''
Install firefox first, latest version preferred. 


pip install nltk
pip install selenium

Options : linux-aarch64, linux32, linux64
Answer Based on: https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu

export GECKO_DRIVER_VERSION='v0.36.0'
export OS='INSERT OS NAME HERE'
wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
rm geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
chmod +x geckodriver
cp geckodriver /usr/local/bin/

Info on non-linux install this will vary: https://selenium-python.readthedocs.io/installation.html#drivers
'''
def main():
    nltk.download('punkt_tab')
    print("Welcome to Quill Smurf!\n")
    inputText = input("Enter text to paraphrase:")
    outputDir = input("\nEnter the full path name (or leave blank for the same path as this executable) where the output should be stored. \n" +
                      "For example: C:\\\\username\Downloads\outputDir\. \n"
                      +"INCLUDE A TRAILING '/' or \\'.\n"
                      "WARNING: IF THERE IS A FILE NAMED 'quillSmurfOutput.txt' IT WILL BE DELETED \n" +
                      "Enter here: ")
    outputDir = outputDir+"quillSmurfOutput.txt"
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

    if os.path.exists(outputDir):
        os.remove(outputDir)
        print("Successfully removed your prior output.")


    outputFile = open(outputDir, "a")
    browser = setupBrowser()  
    for i in range (0,len(sortedInputTextArray)):
        writeQB(browser, sortedInputTextArray[i], outputFile)

        if (i == len(sortedInputTextArray)-1):
            browser.quit()
        elif ((i+1) % 3 == 0):
            browser.quit()
            browser = setupBrowser()
    outputFile.close()
    
def sortOutput(finalText, outputFile):
    finalTextArray = nltk.tokenize.sent_tokenize(finalText)
    for i in range(0, len(finalTextArray)):
        outputFile.write(finalTextArray[i]+"\n")


    
def setupBrowser():
    uOptions = Options()
    #uOptions.add_argument("--headless")
    browser = webdriver.Firefox(options=uOptions)
    browser.get('https://quillbot.com/paraphrasing-tool')
    loadQB(browser) 
    return browser

def loadQB(browser):
    
    try:
        WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,'//iframe[@title="Sign in with Google Dialog"]')))
        browser.switch_to.frame(browser.find_element(By.XPATH,'//iframe[@title="Sign in with Google Dialog"]'))
        browser.find_element(By.ID, "close").click()
        browser.switch_to.parent_frame()
    except NoSuchElementException:
        pass


def writeQB(browser, text, outputFile):
    input = browser.find_element(By.ID, "paraphraser-input-box")
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)
    input.send_keys(text)  

    pButton = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='pphr/input_footer/paraphrase_button']")))
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

    # Circumventing the split up div by copying output somewhere else.
    # Think of this next block of code as just getting the output.
    try:
        copyButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/output_footer/copy_text_button']")))
        copyButton.click()
    except (ElementClickInterceptedException):
        xButton = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='styleq-dialog-close-button']")))
        xButton.click()
        copyButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-testid='pphr/output_footer/copy_text_button']")))
        copyButton.click()

    input = browser.find_element(By.ID, "paraphraser-input-box")
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)
    input.send_keys(Keys.CONTROL + "v")
    finalText = input.text
    print(finalText)
    sortOutput(finalText, outputFile)

    
if __name__ == "__main__":
    main()