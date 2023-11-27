
import xlsxwriter


def price(i, total, count):
    return float(i["price"]) < (total/count)*0.5


def priceSort(e):
    return float(e["price"])


def getTotal(data):
    total = 0
    count = 0
    for item in data:
        count = count+1
        total += float(item["price"])
    return [total, count]


def createExcel(data, name):
    workbook = xlsxwriter.Workbook(f"./excel_sheets/{name}.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "id")
    worksheet.write(0, 1, "Name")
    worksheet.write(0, 2, "Price")
    worksheet.write(0, 3, "Link")

    setTotal = getTotal(data)
    total = setTotal[0]
    count = setTotal[1]
    # print(float(total/count))
    # working on this in the future
    """
    # used to calculate the average price, so random extreme prices are listed in excel
    if float(total/count) > 90 and 'AMAZON' not in name:
        newData = [i for i in data if not price(i, total, count)]
    else:
    """
    newData = data

    setNewTotal = getTotal(newData)
    newTotal = setNewTotal[0]
    newCount = setNewTotal[1]

    # sorted data by price
    newData.sort(key=priceSort)
    # print(newData[0])

    for i, entry in enumerate(newData):
        worksheet.write(i+1, 0, str(i+1))
        worksheet.write(i+1, 1, entry["name"])
        worksheet.write(i+1, 2, "$"+entry["price"])
        worksheet.write(i+1, 3, entry["link"])

    worksheet.write(len(newData)+1, 0, "Avg. Price")
    worksheet.write(len(newData)+1, 1, "$"+str(round(newTotal/newCount, 2)))

    if 'EBAY' in name:
        print('\tEbay Done')
    else:
        print('\tAmazon Done')

    workbook.close()
