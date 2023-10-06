def rounder(number, decimalPlaces):
    return float(int(number * (10 ** decimalPlaces))) / 10 ** decimalPlaces

print(rounder(10003784650.8475024, 2))
