from task1 import PredictPrice
import warnings
import sys
import datetime

class PrototypePricing:
    def __init__(self, units: str, transactionDates: list,
                 injectWithdrawalRate: list, maxVolume: float, monthlyStorage: float,
                 transportCost: float):
        
        self.units = units
        self.transactionDates = transactionDates
        self.injectWithdrawalRate = injectWithdrawalRate
        self.maxVolume = maxVolume
        self.monthlyStorage = monthlyStorage
        self.transportCost = transportCost

        # calculated variables
        self.transactionCount = 0.0

        # organizing transactions by date
        self.sortTransactions()
        # self.toString() 

    def toString(self):
        print("PrototypePricing")
        print("units:"+str(self.units))
        print("transactionDates:"+str(self.transactionDates))
        print("injectWithdrawalRate:"+str(self.injectWithdrawalRate))
        print("maxVolume:"+str(self.maxVolume))
        print("monthlyStorage:"+str(self.monthlyStorage))
        print("transportCost:"+str(self.transportCost))

    def sortTransactions(self):
        print("Before: " + str(self.transactionDates))
        self.transactionDates.sort(key=lambda x: datetime.datetime.strptime(x[0], '%m/%d/%Y'))
        print("After: " + str(self.transactionDates))

    
    def calculateValue(self) -> float:

        value = 0.0
        
        if len(self.transactionDates) == 0:
            return 0.0
        
        quantitySum = 0.0
        for i in range(len(self.transactionDates)):
            quantity = self.transactionDates[i][1]
            onDate = self.transactionDates[i][0]

            # Add up injection amount
            quantitySum += quantity
            self.transactionCount += 1

            if quantitySum > self.maxVolume:
                print("max volume exceeded")
                break

            if quantitySum < 0:
                print("negative quantity exceeded on date " + onDate)
                break

            pp = PredictPrice(onDate)
            unitPrice = pp.runner()
            print("quanity on " + onDate + " is " + str(quantity) + " and unit price is " + str(unitPrice))
            value += (quantity * unitPrice)

            # apply inject/withdrawal rate
            priceRate = self.injectWithdrawalRate[0]
            quantityRate = self.injectWithdrawalRate[1]
            injectWithdrawalCost = (priceRate/quantityRate) * abs(quantity)
            value -= injectWithdrawalCost
            print("inject/withdrawal cost is " + str(injectWithdrawalCost))


        # Charge transport cost for each transaction
        fullTransactionCost = self.transportCost * self.transactionCount
        
        print("full transaction cost is " + str(fullTransactionCost))
        value -= fullTransactionCost

        return value

if __name__ == "__main__": 
    # Check if the correct number of arguments is provided
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    

    # Accessing arguments
    script_name = sys.argv[0]
    if len(sys.argv) > 1:
        override = sys.argv[1]
    else:
        override = False

    if not override:

        units = str(input("Enter units (e.g. 'MMBtu'): ") )
        injectionWithdrawalRate = []
        priceRate = float(input("Enter price rate for injection/withdrawal (e.g. 10000): "))
        quantityRate = float(input("Enter quantity rate for injection/withdrawal (e.g. 1000000): "))
        injectionWithdrawalRate = [priceRate, quantityRate]
        
        maxVolume = float(input("Enter max volume (e.g. 2000000): "))
        monthlyStorage = float(input("Enter monthly storage (e.g. 100000): "))
        transportCost = float(input("Enter transport cost (e.g. 50000): "))

        transactionDates = []
        print("Enter transaction dates and quantities.")
        while True:
            date = str(input("Enter date (e.g. '6/1/2023') or 'done' to finish: "))
            if date.lower() == 'done':
                break
            quantity = float(input("Enter quantity (e.g. 1000000 for injection, -1000000 for withdrawal): "))
            transactionDates.append((date, quantity))
    if override:
        units = "MMBtu"
        transactionDates = [("6/1/2023", 1000000),("10/1/2023", -1000000)]
        injectionWithdrawalRate = (10000, 1000000)
        maxVolume = 2000000
        monthlyStorage = 100000                      # monthly rate
        transportCost = 50000

    pp = PrototypePricing(units, transactionDates, 
                        injectionWithdrawalRate, maxVolume, monthlyStorage,
                        transportCost)

    print("-----------------\nTotal value: " + str(pp.calculateValue()))
    
    
