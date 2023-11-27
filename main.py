
from excel import createExcel
from price import *


def main():
    while True:
        item = input("Enter item or -1 to stop: ")
        if item == '-1':
            break
        item = item.split(" ")
        item_search = '+'.join(item)
        item_title = '_'.join(item)
        pages = int(input('Pages num: '))
        eb = input('get Ebay? (yes) or (no): ')
        am = input('get Amazon? (yes) or (no): ')
        print("loading...")
        if eb.lower() == 'yes':
            ebayData = getEbay(item_search, pages)
            createExcel(ebayData, f"{item_title}+{pages}_pages_EBAY")
        if am.lower() == 'yes':
            amaData = getAma(item_search, pages)
            createExcel(amaData, f"{item_title}+{pages}_pages_AMAZON")


if __name__ == '__main__':
    main()
