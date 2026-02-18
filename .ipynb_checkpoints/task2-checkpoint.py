from task1 import PredictPrice
import warnings
import sys

if __name__ == "__main__": 
    # Check if the correct number of arguments is provided
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    if len(sys.argv) < 2:
        print("Usage: python script.py <injectionDates:list(str)>, <withdrawalDates:list(str)>, <prices")
        exit(0)


    # Accessing arguments
    script_name = sys.argv[0]
    first_argument = sys.argv[1]
    pp = PredictPrice(first_argument, 'Nat_Gas.csv')
    print(pp.runner())
    