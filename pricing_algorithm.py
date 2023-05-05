# Determine the best time to book a flight
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn import svm
import sklearn
# from sklearn import svm
import pickle 
import geo
# from sklearn.svm import SVC

from joblib import dump, load


# round trip or not
def find_best_time_to_buy(domestic, source, destination, departure_date, return_date):
    current_date = datetime.now().date()
    departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
    return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
    
    # days_till_departure = 10
    days_left = departure_date - current_date 
    # duration = return_date - departure_date
    duration = geo.find_flight_time(source, destination)
    print("days_left", days_left)
    print("duration:", duration)
    
    predict_price(domestic, source, destination, days_left, duration)





def predict_price(domestic, source, destination, days_left, duration):
    clf = load('svm_model.joblib')
    clf.predict(source, destination, days_left, duration)
    # with open('model.pkl', 'rb') as f:
    #     clf2 = pickle.load(f)   
    #     clf2.predict(source, destination, days_left, duration)
    # for i in range(days_till_departure):
        # 4 parameters:  duration	flight	stops	days_left
        # duration = difference in days
        # flight = '' 
        # days_left  = days_till_departure 
        # flight	stops	days_left
        # duration = 
        # data_point = (source, destination, days_till_departure)
        # y_pred = clf2.predict(data_point)
    # plt.plot_date(x = i , y =y_pred)
    # labels = [str(i.day) + '/'+ str(i.month) + '/'+str(i.year) for i in df['date']]
    # plt.xticks(ticks=df['date'],labels=labels, rotation=90)
    # plt.show()




    return 



if __name__ == '__main__':
    """runs the application on a server"""
    domestic = "domestic"# can also be international 
    departure_date = "2023-05-10"
    return_date = "2023-05-12"
    source = "New York City"
    destination = "Mumbai"
    find_best_time_to_buy(domestic, source, destination, departure_date, return_date)

# one way 