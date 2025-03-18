import requests
from bs4 import BeautifulSoup


def main():
    for i in range(1, 254):
        url = f"http://www.camp3.bicnirrh.res.in/seqDb.php?page={i}"
        response = requests.get(url)


if __name__ == "__main__":
    main()
