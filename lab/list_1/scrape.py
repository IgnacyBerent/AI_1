import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd


def main():

    data = []

    options = Options()
    # Optional: Ignore SSL certificate errors
    options.add_argument("--ignore-certificate-errors")
    # Optional: Run Chrome in headless mode if you don't need the UI
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # pages of sequences of length <=50
    for i in range(1, 164):
        url = (
            f"http://www.camp3.bicnirrh.res.in/seqDb.php?page={i}"
            if i > 1
            else "http://www.camp3.bicnirrh.res.in/seqDb.php?page=0"
        )
        if i == 1:
            time.sleep(4)
        time.sleep(1)
        driver.get(url)
        time.sleep(2)
        element = driver.find_element(By.NAME, "checkall")
        element.click()
        element = driver.find_element(
            By.XPATH, '//*[@id="myForm"]/table[1]/tbody/tr/td[3]/input[1]'
        )
        element.click()
        time.sleep(1)
        # Parse the page HTML using BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # Match any table where the class contains "linktext"
        tables = soup.find_all("table", class_=re.compile(r"linktext"))
        for table in tables:
            name = None
            # Find the row with the title label and get the name from the second <td>
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2 and "Title" in tds[0].get_text():
                    name = tds[1].get_text(strip=True)
                    break
            # Get sequence from the <td> with class "fasta"
            sequence_cell = table.find("td", class_="fasta")
            if name and sequence_cell:
                sequence = sequence_cell.get_text(strip=True)
                data.append([name, sequence, len(sequence)])

    # use pandas to save the sequences to a csv file
    df = pd.DataFrame(data, columns=["Name", "Sequence", "Length"])
    df.to_csv("lab/list_1/data/campr3.csv", index=False)


if __name__ == "__main__":
    main()
