import xml.etree.ElementTree


class ConfigProvider:
    """Provides access to config options."""

    _configFileName = "HistoryDownloaderConfig"
    _configRoot = xml.etree.ElementTree.parse(_configFileName).getroot()
    _hostUrl = ""
    _symbolPageUrl = ""
    _csvRequestUrl = ""

    def __init__(self):
        self._hostUrl = self.getOption("hostUrl", "url")
        self._symbolPageUrl = self.getHostUrl + self.getOption("symbolPageUrl", "url")
        self._csvRequestUrl = self.getHostUrl + self.getOption("csvRequestUrl", "url")

    def getOption(self, elementName : str, attributeName : str, parent = _configRoot):
        element = parent.find(elementName)
        return element.get(attributeName)

    def getOptions(self, listElementName : str, itemElementName : str, itemAttributeName : str, parent = _configRoot):
        listElement = parent.find(listElementName)
        result = list()
        for item in listElement.findall(itemElementName):
            result.append(item.get(itemAttributeName))
        return result

    @property
    def getHostUrl(self):
        return self._hostUrl

    @property
    def getSymbolPageUrl(self):
        return self._symbolPageUrl

    @property
    def getCsvRequestUrl(self):
        return self._csvRequestUrl

    @property
    def getSymbols(self):
        return self.getOptions("symbols", "symbol", "name")
