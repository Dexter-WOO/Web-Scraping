####################################
# Choose which page to scrape
x = 1
y = 5                              
# Save as a csv file
csv_name = "[NEW2] Weekly BBSW.csv"
###################################

Date = []
Rate = []
FailedPage = []
for i in range(x, y):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = f"https://www.yieldreport.com.au/category/bank-billswaps/weekly-bank-billswaps/page/{i}/"
    if i == 1:
        url = "https://www.yieldreport.com.au/category/bank-billswaps/weekly-bank-billswaps/"
    page = requests.get(url, verify=False, timeout=30, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    if str(soup.find('p').get_text()) == "Access to this resource on the server is denied!":
        print(f"Page {i} failed to read data!\n")
        FailedPage.append(i)
    else:
        try:
            date = datetime.strptime(" ".join(" ".join(soup.find_all(class_='post-entry-title group')[0].get_text().split()).split()[3:6])
                                     , '%d %B %Y')
        except:
            date = datetime.strptime(" ".join(" ".join(soup.find_all(class_='post-entry-title group')[0].get_text().split()).split()[3:6])
                                     , '%d %b %Y')
        row = soup.find_all('tr', class_='row-4 even')[0]
        rate = float(row.find(class_='column-2').get_text())
        Date.append(date)
        Rate.append(rate)
        print(f"Page {i} success.\n")
        sleep(randint(2,10))
bbsw_series = pd.Series(Rate, index=Date, name="Weekly BBSW (%)")[::-1]
(bbsw_series/100).round(4).to_csv(csv_name, index_label="Date", header=["BBSW"])
