import requests
from bs4 import BeautifulSoup
import re

def main():
    r = requests.get("https://nikkei.joho-box.net/fluctuations-ratio/2023.html")
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text, "html.parser")
    table_rows = soup.find_all("tr")

    month_detector = re.compile(r"東証プライム　(.+)月の騰落レシオ")
    current_month = 1

    zen_han_table = {
        "１": 1, "２": 2, "３": 3, "４": 4,
        "５": 5, "６": 6, "７": 7, "８": 8,
        "９": 9, "10": 10, "11": 11, "12": 12,
    }
    
    for tr_idx, row in enumerate(table_rows):

        tds = row.find_all("td")
        #if len(tds) == 1 and tds[0].attrs.get("align") == "center":
        if len(tds) == 1 and tds[0].string != None:
            #print(tds[0].string)
            match = month_detector.match(tds[0].string)
            if match:
                month_zen_str = match.group(1)
                if month_zen_str in zen_han_table:
                    current_month = zen_han_table[month_zen_str]

        if len(tds) == 14:

            td_strs = [str(current_month)]
            for idx, td in enumerate(tds):
                if idx in [0, 1, 2, 4, 6, 8, 10, 12]:
                    #print(td)
                    td_strs.append(str(td.string))
            print(",".join(td_strs))
    pass

if __name__ == '__main__':
    main()
