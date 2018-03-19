import urllib
import bs4
from selenium import webdriver
import json


coinratesBaseUrl = "http://www.bitcoinrates.in/index.php"
bitstampBaseUrl = "https://www.bitstamp.net/api/v2/ticker/"

coins = [ 
    { "symbol": "btc", "id": "4"},
    { "symbol": "ltc", "id": "4"},
    { "symbol": "bch", "id": "4"},
    { "symbol": "eth", "id": "4"}
]

usdInrRate = 65.00

phantomDriverPath = r'C:\Program Files\webDrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe'
chromeDriverPath = r"C:\Program Files\webDrivers\chromedriver_win32\chromedriver.exe"

#browser = webdriver.Chrome(executable_path=chromeDriverPath)
browser = webdriver.PhantomJS( phantomDriverPath)

for coin in coins:
    cSymbol = coin.get("symbol")
    queryParam = { 'coin': cSymbol}
    coinInrUrl = coinratesBaseUrl + r'?' + urllib.parse.urlencode( queryParam)
    browser.get( coinInrUrl)
    buyRateInr = float( browser.find_element_by_xpath("//span[@id='4_buyrate']").text)
    sellRateInr = float( browser.find_element_by_xpath("//span[@id='4_sellrate']").text)
    coinUsdUrl = bitstampBaseUrl + r'/' + cSymbol + r'usd/'
    browser.get( coinUsdUrl)
    rateUsd = float( json.loads( urllib.request.urlopen( coinUsdUrl).read())['last'])
    margin = (( (sellRateInr/usdInrRate) - rateUsd ) / rateUsd) * 100
    print( cSymbol.upper(), '%.2f' % margin, '% | Zebpay(INR) ', sellRateInr, buyRateInr, ' | Bitstamp( USD)', rateUsd)

browser.close()