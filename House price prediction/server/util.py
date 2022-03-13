import pickle
import json
import numpy as np

# define global variables
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    print("loading saved artifacts")
    # here we are creating gloabl variables
    global  __data_columns
    global __locations

    # load data columns
    with open("./server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    # load model
    global __model
    if __model is None:
        with open('./server/artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_estimated_price(location,sqft,bhk,bath):
    # Here x is the 2d numpy array

    try:
        # convert the location to index and lowercase
        loc_index = __data_columns.index(location.lower())
        # print("loc_index:",loc_index)
    except:
        loc_index = -1

    # create np array with no of zeros as length of data columns
    x = np.zeros(len(__data_columns))
    # print("x:",x)
    x[0] = sqft
    # print("x[0]:",x[0])
    x[1] = bath
    # print("x[1]:",x[1])
    x[2] = bhk
    # print("x[2]:",x[2])
    if loc_index>=0:
        x[loc_index] = 1
        # print("x[loc_index]:",x[loc_index])
        # if location is present in the data columns then we need to set the value of x[loc_index] to 1

    # once model makes a prediction we return a 2D array back & round to 2 decimals
    # print("2D array",round(__model.predict([x])[0],2))
    return round(__model.predict([x])[0],2)
    

def get_location_names():
    return __locations


# Here we call the above defined methods
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location