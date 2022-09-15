import time
import json
import traceback
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException


def get_all_clickable_tags(driver):
    div = driver.find_elements_by_css_selector("div[onclick]")
    a = driver.find_elements_by_css_selector('a[href]')
    btn = driver.find_elements_by_css_selector("button[onclick]")
    return div + a + btn


def do_dfs(driver, visited, parentUrl, nodes, links, nodeDict, clickedTagKey, foldername):
    time.sleep(7)

    print(f"\n\nfrom: {parentUrl}")
    print(f"dfs: {driver.current_url}\n")
    if driver.current_url not in visited:
        visited.add(driver.current_url)
        path = write2file(driver, foldername)
        nodes.append({"name": driver.title, "path": path, "url": driver.current_url, "color": "red", "type": "url"})
        nodeDict[driver.current_url] = len(nodeDict)

        tags = get_all_clickable_tags(driver)
        print(tags)
        for i in range(len(tags)):
            try:
                print(f"i: {i} of {len(tags)}")
                print(f"try {tags[i].tag_name}")

                tagIdx = len(nodeDict)
                tagKey = get_md5(driver.current_url) + str(i)
                nodes.append({"name": tagKey, "color": "blue", "type": tags[i].tag_name, "url": driver.current_url, "i": i})
                links.append({"source": nodeDict[driver.current_url], "target": tagIdx, "weight": 1})
                nodeDict[tagKey] = tagIdx

                tmp = driver.current_url
                tags[i].click()

                doesSamePage = do_dfs(driver, visited, tmp, nodes, links, nodeDict, tagKey, foldername)
                if not doesSamePage:
                    driver.back()
                    time.sleep(7)
                    print(f"back to {driver.current_url}")

                tags = get_all_clickable_tags(driver)
                print(f" new tag length: {i} of {len(tags)}")

            except ElementNotVisibleException:
                print("tag is not visible, skip")
                continue
            except StaleElementReferenceException:
                print("tag is a stale element, skip")
                continue
    else:
        print(f"{driver.current_url} visited, skip...")

    if clickedTagKey is not None:
        links.append({"source": nodeDict[driver.current_url], "target": nodeDict[clickedTagKey], "weight": 1})
    
    if driver.current_url == parentUrl:
        print("end, it is same url")
        return True
    else:
        print("end, it is different url")
        return False

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    if platform.system() == 'Darwin':
        print("mac version...")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options) 
    else:
        print("linux version...")
        driver = webdriver.Chrome('./chromedriver_linux', options=chrome_options) 
    
    return driver


def main():
    try:
        driver = get_driver()

        res = {}
        for filename in os.listdir(f"{os.getcwd()}/ori/"):
            print(filename)
            with open(os.path.join(os.getcwd(), f"{os.getcwd()}/ori/{filename}"), 'r') as fp: 
                content = fp.read()
                words = content.split('\n')
                print(len(words))

                words = list(dict.fromkeys(words))
                print(len(words))

                with open(f'{filename}.js', 'w') as fpDump:
                    fpDump.write(str(words))
        
                # for word in words:
                #     url = f"https://jisho.org/word/{word}"
                #     print(f"go to {url}")
                #     driver.get(url)
                #     time.sleep(3)

                #     meaning = driver.find_element('css selector', 'div.concept_light-meanings')
                #     print(meaning.get_attribute('innerHTML'))
        

        # with open('data.json', 'w') as fp:
        #     json.dump(res, fp)
    except:
        print(traceback.format_exc())
    finally:
        print("quit...")
        driver.quit()


if __name__ == "__main__":
    main()

