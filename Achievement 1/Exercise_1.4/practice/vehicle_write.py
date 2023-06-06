import pickle

vehicle = {
    'brand': 'BMW',
    'model': '530i',
    'year' : 2015,
    'color': 'Black Sapphire'
}

file_wb = open('vehicledetail.bin', 'wb')
pickle.dump(vehicle, file_wb)
file_wb.close()