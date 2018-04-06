import urllib.request
import lxml.html
import time
from ConfigProvider import ConfigProvider


#1. Узнать как посылать пост-реквесты
#2. Узнать как получать и сохранять файлы из ответов
#3. Узнать что удобнее конвертить в джсон: ДТО или словарь
#4. Завести ДТО или словарь согласно п.3
#5. Сделать парсинг формы со страницы загрузки в пэйлоад реквеста

#6. Шаги загрузки:
#-получить все ссылки на страницы с формой для одного символа
#-последовательно загрузить страницу - распарсить форму в пэйлоад - запросить файл - сохранить его в переменную
#-для одного символа смержить все файлы в один и сохранить (куда - хз)

class HistoryDownloader:
    """Downloads history files from a specified website."""

    configProvider = ConfigProvider()
    baseSymbolPageUrl = configProvider.getSymbolPageUrl
    symbols = configProvider.getSymbols

    def getSymbolPageUrls(self, symbol: str = symbols[0]):
        url = self.baseSymbolPageUrl + symbol
        connection = urllib.request.urlopen(url)
        pageDom = lxml.html.fromstring(connection.read())
        links = pageDom.xpath("//a/@href[contains(.,'download-free-forex-historical-data')]")
        result = []
        for lnk in links:
            result.append(self.configProvider.getHostUrl + lnk)
        return result

    def getSymbolCsvRequestPayload(self, filePageUrl):
        connection = urllib.request.urlopen(filePageUrl)
        pageDom = lxml.html.fromstring(connection.read())
        requestPayloadFields = pageDom.xpath("//form[@id='file_down']")
        requestPayloadIds = requestPayloadFields.xpath("")
        result = dict()
        for field in requestPayloadFields:
            result.update({field.name : field.type})
        time.sleep(4)
        return result


histDl = HistoryDownloader()

fn = histDl.getSymbolCsvRequestPayload("http://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/eurusd/2017/11")
for field in fn:
    print(field)


for symbol in histDl.symbols:
    print(symbol)

for link in histDl.getSymbolPageUrls():
    print(link)

