from core.enums.trading_currency import TradingCurrency
from core.enums.currency_pairs import CurrencyPairs


# this file for risk management

class RiskManagement:

    def __init__(self, balance, riskPercent=1.0, tradingCurrency=TradingCurrency.USD):
        self.tradingCurrency = tradingCurrency  # the base currency
        self.balance = abs(balance)  # your balance
        if 0.0 < abs(riskPercent) <= 100.0:  # risk size
            self.riskPercent = riskPercent / 100.0
        else:
            raise Exception('the risk percent value is in wrong range')

    # calculate entry volume and return LAT size
    def calculateVolume(self, entry, stopLoss, currencyPairs):
        ratio = self.balance * self.riskPercent
        val = abs(entry - stopLoss)

        entryVolume = ratio / val
        if self.checkBaseCurrency(currencyPairs):
            return int(entryVolume / 1000)
        else:
            secVolume = entryVolume * entry
            return int(secVolume / 1000)

    """
    Checking the trading currency side
    For example, if the trading currency is USD
    in EURUSD -> False
    In USDCAD -> True
    """

    def checkBaseCurrency(self, currencyPairs):
        if self.tradingCurrency.value in currencyPairs.value[0:3]:
            return True
        else:
            return False

    # entry with half of volume
    def quarterRisk(self, entry, stopLoss, currencyPairs):
        return int(self.calculateVolume(entry, stopLoss, currencyPairs) / 4)

    # entry with a quarter of volume
    def halfRisk(self, entry, stopLoss, currencyPairs):
        return int(self.calculateVolume(entry, stopLoss, currencyPairs) / 2)
