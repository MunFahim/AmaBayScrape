import requests
from bs4 import BeautifulSoup


def getHTML(url):
    if "amazon" in url:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close'
        }
        r = requests.get(url, headers=headers)
        return r.text
    else:
        r = requests.get(url)
        return r.text


def filterPrice(price):
    newPrice = ""
    for i in price:
        if (i == "."):
            newPrice += "."
        try:
            newPrice += str(int(i))
        except ValueError:
            newPrice = newPrice
    return newPrice


def getEbay(item, pages):
    # print(pages)
    ebayDataList = []
    # start looping the urls
    for p in range(1, pages+1):
        newUrl = (f"https://www.ebay.com/sch/{item}&LH_BIN=1&_pgn={p}")
        res = getHTML(newUrl)
        soup = BeautifulSoup(res, 'html.parser')
        theDiv = soup.find("ul", {"class": "srp-results srp-list clearfix"})
        items = theDiv.find_all("li")

        for i in items:
            theItem = ""
            currPrice = ""
            title = i.find("div", {"class": "s-item__title"})
            link = ""
            if title is not None:
                link = i.find("a")["href"]
                link = link.split("?", 1)[0]
                theItem = title.find("span").get_text()
                theItem.replace("New Listing", "")
                if "not working" in theItem.lower() or "parts only" in theItem.lower() or "needs repair" in theItem.lower() or "repair needed" in theItem.lower():
                    continue
                # print(theItem)
                price = i.find("div", {"class": "s-item__details clearfix"})
                if price is not None:
                    currPrice = price.find(
                        "div", {"class": "s-item__detail s-item__detail--primary"}).find("span").get_text()
                    if "to" in currPrice:
                        continue

                    priceFilter = filterPrice(currPrice)

                    # print(f"costs : {currPrice}")
                    # print(link)

                    ebayDataList.append({
                        "name": theItem,
                        "price": priceFilter,
                        "link": link
                    })

    return ebayDataList


def getAma(item, pages):
    amaDataList = []
    # start looping the urls
    for p in range(1, pages+1):
        newUrl = (f'https://www.amazon.com/s?k={item}&page={p}')
        res = getHTML(newUrl)
        soup = BeautifulSoup(res, 'html.parser')
        theList = soup.find(
            "span", {"data-component-type": "s-search-results"})
        items = theList.find_all(
            "div", {"data-component-type": "s-search-result"})

        for i in items:
            id = i["data-asin"]
            if id is not None:
                title = i.find("h2").find("span").get_text()
                try:
                    price = i.find("span", {"class": "a-offscreen"}).get_text()
                    priceFiltered = filterPrice(price)
                    amaDataList.append({
                        "name": title,
                        "price": priceFiltered,
                        "link": str("https://www.amazon.com/dp/"+id)
                    })
                except:
                    pass
    return amaDataList
