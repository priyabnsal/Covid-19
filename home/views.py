from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
# from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
# %matplotlib inline
# import pandas as pd
# import time

import numpy as np 
import matplotlib.pyplot as plt, mpld3
import matplotlib.pyplot as plt

import matplotlib.colors as mcolors
import pandas as pd 
import random
import math
import time
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime
import operator 
# plt.style.use('fivethirtyeight')
# %matplotlib inline
from IPython.display import set_matplotlib_formats
# set_matplotlib_formats('retina')
import warnings
# warnings.filterwarnings("ignore")
# Create your views here.

def greetings(request):
    res = render(request,'home.html')
    return res
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    if request.method == 'POST':
        state_name = request.POST['search_text'].capitalize()
        state_code_data = pd.read_csv("state_code.csv")
        print(state_code_data.head())
        state_code = state_code_data.loc[state_code_data['State'] == state_name, 'State_code'].iloc[0]
        
        url = "https://www.covid19india.org/state/"+state_code
        print("state name :",state_name)
        print("state code :",state_code)
        print("url :",url)
        print("driver start")
        

        state_wise_daily = pd.read_csv("state_wise_daily.csv")
        
        print("state_wise_daily :",state_wise_daily.head())
        for_confirmed = state_wise_daily.loc[state_wise_daily['Status']=="Confirmed",['Date',state_code]]
        for_confirmed.rename(columns = {state_code: "Confirmed"},inplace=True)

        for_recovered = state_wise_daily.loc[state_wise_daily['Status']=="Recovered",['Date',state_code]]
        for_recovered.rename(columns = {state_code: "Recovered"},inplace=True)

        for_deceased = state_wise_daily.loc[state_wise_daily['Status']=="Deceased",['Date',state_code]]
        for_deceased.rename(columns = {state_code: "Deceased"},inplace=True)

        temp = pd.merge(for_confirmed,for_recovered,on="Date",how="inner")
        final_state_wise = pd.merge(temp,for_deceased,on="Date",how="inner")

        final_state_wise['Active'] = final_state_wise['Confirmed'] - final_state_wise['Recovered'] - final_state_wise['Deceased']

        final_state_wise['cf_Confirmed'] = final_state_wise['Confirmed'].cumsum()
        final_state_wise['cf_Recovered'] = final_state_wise['Recovered'].cumsum()
        final_state_wise['cf_Deceased'] = final_state_wise['Deceased'].cumsum()
        final_state_wise['cf_Active'] = final_state_wise['Active'].cumsum()

        final_state_wise = final_state_wise[['Date','cf_Confirmed','cf_Recovered','cf_Deceased','cf_Active']]

        print(final_state_wise.tail(2))
        state_code_data = state_code_data.to_json()

        state_wise_daily = state_wise_daily.to_json()

        total_state_data = final_state_wise.tail(1)

        final_state_wise.Date = pd.to_datetime(final_state_wise.Date)
        final_state_wise.set_index('Date', inplace=True)

        plot = final_state_wise.plot(figsize=(20,10), linewidth=5, fontsize=20,color = ['steelBlue','Green','Red','Orange'])
        plot.set_xlabel('Date', fontsize=20)
        plot.set_ylabel('No. of Cases', fontsize=20)
        plot.set_title(state_name, fontsize=20)
        plot.legend(["Confirmed","Recovered","Death","Active"],fontsize=20)
        fig = plot.get_figure()
        fig.savefig("static/images/output.png")

        res = render(request,'home.html',{"state_name":state_name,"total_state_data":total_state_data,"img_name":"output.png"})

        # res = render(request,'home.html',{"html_code":html_code,"state_name":state_name,"total_state_data":total_state_data,"img_name":"output.png"})
        return res


    # return HttpResponse("this is hompage")
def loginuser(request):
    if request.method =="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
            # return render(request, 'index.html')
    # A backend authenticated the credentials
    # return redirect('home')
    else:
        return render(request, 'login.html')
        # return redirect('/login')
        
def logoutuser(request):
        logout(request)
        return redirect('/login')



def services(request):
    if request.user.is_anonymous:
        return redirect('/login')

    return render(request, 'services.html')
def contact(request):
    if request.method =="POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        message= request.POST.get('message')
        contact =  Contact(name=name, email=email, message=message, date=datetime.today())
        contact.save();
    messages.success(request, 'Message send successfully')

    return render(request,'contact.html')

def d3js(request):
    return render(request,'d3js.html')
def world(request):
    return render(request,'world.html')
def symptoms(request):
    return render(request,'symptoms.html')
    

def predict(request):
    plt.style.use('fivethirtyeight')
    set_matplotlib_formats('retina')
    warnings.filterwarnings("ignore")

    confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-11-2021.csv')
    
    latest_data.head()
    confirmed_df.head()
    print(latest_data.head())
    print(confirmed_df.head())

    cols = confirmed_df.keys()

    confirmed = confirmed_df.loc[:, cols[4]:cols[-1]]
    deaths = deaths_df.loc[:, cols[4]:cols[-1]]
    recoveries = recoveries_df.loc[:, cols[4]:cols[-1]]

    dates = confirmed.keys()
    world_cases = []
    total_deaths = [] 
    mortality_rate = []
    recovery_rate = [] 
    total_recovered = [] 
    total_active = [] 

    for i in dates:
        confirmed_sum = confirmed[i].sum()
        death_sum = deaths[i].sum()
        recovered_sum = recoveries[i].sum()
        
        # confirmed, deaths, recovered, and active
        world_cases.append(confirmed_sum)
        total_deaths.append(death_sum)
        total_recovered.append(recovered_sum)
        total_active.append(confirmed_sum-death_sum-recovered_sum)
        
        # calculate rates
        mortality_rate.append(death_sum/confirmed_sum)
        recovery_rate.append(recovered_sum/confirmed_sum)


    def daily_increase(data):
        d = [] 
        for i in range(len(data)):
            if i == 0:
                d.append(data[0])
            else:
                d.append(data[i]-data[i-1])
        return d 

    def moving_average(data, window_size):
        moving_average = []
        for i in range(len(data)):
            if i + window_size < len(data):
                moving_average.append(np.mean(data[i:i+window_size]))
            else:
                moving_average.append(np.mean(data[i:len(data)]))
        return moving_average

    # window size
    window = 7

    # confirmed cases
    world_daily_increase = daily_increase(world_cases)
    world_confirmed_avg= moving_average(world_cases, window)
    world_daily_increase_avg = moving_average(world_daily_increase, window)

    # deaths
    world_daily_death = daily_increase(total_deaths)
    world_death_avg = moving_average(total_deaths, window)
    world_daily_death_avg = moving_average(world_daily_death, window)


    # recoveries
    world_daily_recovery = daily_increase(total_recovered)
    world_recovery_avg = moving_average(total_recovered, window)
    world_daily_recovery_avg = moving_average(world_daily_recovery, window)


    # active 
    world_active_avg = moving_average(total_active, window)


    days_since_1_22 = np.array([i for i in range(len(dates))]).reshape(-1, 1)
    world_cases = np.array(world_cases).reshape(-1, 1)
    total_deaths = np.array(total_deaths).reshape(-1, 1)
    total_recovered = np.array(total_recovered).reshape(-1, 1)


    days_in_future = 10
    future_forcast = np.array([i for i in range(len(dates)+days_in_future)]).reshape(-1, 1)
    adjusted_dates = future_forcast[:-10]

    start = '1/22/2020'
    start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
    future_forcast_dates = []
    for i in range(len(future_forcast)):
        future_forcast_dates.append((start_date + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))

    # slightly modify the data to fit the model better (regression models cannot pick the pattern)
    X_train_confirmed, X_test_confirmed, y_train_confirmed, y_test_confirmed = train_test_split(days_since_1_22[50:], world_cases[50:], test_size=0.02, shuffle=False) 

    # svm_confirmed = svm_search.best_estimator_
    svm_confirmed = SVR(shrinking=True, kernel='poly',gamma=0.01, epsilon=1,degree=3, C=0.1)
    svm_confirmed.fit(X_train_confirmed, y_train_confirmed)
    svm_pred = svm_confirmed.predict(future_forcast)

    # check against testing data
    svm_test_pred = svm_confirmed.predict(X_test_confirmed)

    fig, ax = plt.subplots()
    plt.plot(y_test_confirmed)
    plt.plot(svm_test_pred)
    plt.legend(['Test Data', 'SVM Predictions'])
    fig.savefig("static/images/abc.png")

    print('SVM MAE:', mean_absolute_error(svm_test_pred, y_test_confirmed))
    print('SVM MSE:',mean_squared_error(svm_test_pred, y_test_confirmed))

    # transform our data for polynomial regression
    poly = PolynomialFeatures(degree=4)
    poly_X_train_confirmed = poly.fit_transform(X_train_confirmed)
    poly_X_test_confirmed = poly.fit_transform(X_test_confirmed)
    poly_future_forcast = poly.fit_transform(future_forcast)

    bayesian_poly = PolynomialFeatures(degree=5)
    bayesian_poly_X_train_confirmed = bayesian_poly.fit_transform(X_train_confirmed)
    bayesian_poly_X_test_confirmed = bayesian_poly.fit_transform(X_test_confirmed)
    bayesian_poly_future_forcast = bayesian_poly.fit_transform(future_forcast)

    # polynomial regression
    linear_model = LinearRegression(normalize=True, fit_intercept=False)
    linear_model.fit(poly_X_train_confirmed, y_train_confirmed)
    test_linear_pred = linear_model.predict(poly_X_test_confirmed)
    linear_pred = linear_model.predict(poly_future_forcast)
    print('MAE:', mean_absolute_error(test_linear_pred, y_test_confirmed))
    print('MSE:',mean_squared_error(test_linear_pred, y_test_confirmed))

    print(linear_model.coef_)

    
    fig, ax = plt.subplots()
    plt.plot(y_test_confirmed)
    plt.plot(test_linear_pred)
    plt.legend(['Test Data', 'Polynomial Regression Predictions'])
    fig.savefig("static/images/bcd.png")

    # bayesian ridge polynomial regression
    tol = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    alpha_1 = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    alpha_2 = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    lambda_1 = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    lambda_2 = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    normalize = [True, False]

    bayesian_grid = {'tol': tol, 'alpha_1': alpha_1, 'alpha_2' : alpha_2, 'lambda_1': lambda_1, 'lambda_2' : lambda_2, 
                    'normalize' : normalize}

    bayesian = BayesianRidge(fit_intercept=False)
    bayesian_search = RandomizedSearchCV(bayesian, bayesian_grid, scoring='neg_mean_squared_error', cv=3, return_train_score=True, n_jobs=-1, n_iter=40, verbose=1)
    bayesian_search.fit(bayesian_poly_X_train_confirmed, y_train_confirmed)

    bayesian_search.best_params_

    bayesian_confirmed = bayesian_search.best_estimator_
    test_bayesian_pred = bayesian_confirmed.predict(bayesian_poly_X_test_confirmed)
    bayesian_pred = bayesian_confirmed.predict(bayesian_poly_future_forcast)
    print('MAE:', mean_absolute_error(test_bayesian_pred, y_test_confirmed))
    print('MSE:',mean_squared_error(test_bayesian_pred, y_test_confirmed))

    fig, ax = plt.subplots()
    plt.plot(y_test_confirmed)
    plt.plot(test_bayesian_pred)
    plt.legend(['Test Data', 'Bayesian Ridge Polynomial Predictions'])
    fig.savefig("static/images/cde.png")

    # def country_plot(x, y1, y2, y3,y4, country):
    #     # window is set as 14 in in the beginning of the notebook 
    #     confirmed_avg = moving_average(y1, window)
    #     confirmed_increase_avg = moving_average(y2, window)
    #     death_increase_avg = moving_average(y3, window)
    #     recovery_increase_avg = moving_average(y4, window)
        
       
    #     fig, ax = plt.subplots()
    #     plt.figure(figsize=(16, 10))
    #     plt.plot(x, y1)
    #     plt.plot(x, confirmed_avg, color='red', linestyle='dashed')
    #     plt.legend(['{} Confirmed Cases'.format(country), 'Moving Average {} Days'.format(window)], prop={'size': 20})
    #     plt.title('{} Confirmed Cases'.format(country), size=30)
    #     plt.xlabel('Days Since 1/22/2020', size=30)
    #     plt.ylabel('# of Cases', size=30)
    #     plt.xticks(size=20)
    #     plt.yticks(size=20)
    #     plt.show()

    #     fig.savefig("static/images/efc.png")

       
    # def get_country_info(country_name):
    #     country_cases = []
    #     country_deaths = []
    #     country_recoveries = []  
        
    #     for i in dates:
    #         country_cases.append(confirmed_df[confirmed_df['Country/Region']==country_name][i].sum())
    #         country_deaths.append(deaths_df[deaths_df['Country/Region']==country_name][i].sum())
    #         country_recoveries.append(recoveries_df[recoveries_df['Country/Region']==country_name][i].sum())
    #     return (country_cases, country_deaths,country_recoveries)


    # def country_visualizations(country_name):
    #     country_info = get_country_info(country_name)
    #     country_cases = country_info[0]
    #     country_deaths = country_info[1]
    #     country_recoveries= country_info[2]
        
    #     country_daily_increase = daily_increase(country_cases)
    #     country_daily_death = daily_increase(country_deaths)
    #     country_daily_recovery = daily_increase(country_recoveries)
        
    #     country_plot(adjusted_dates, country_cases, country_daily_increase, country_daily_death,country_daily_recovery, country_name)
        
    # country_visualizations('India')
    
    # Future predictions using SVM 
    svm_df = pd.DataFrame({'Date': future_forcast_dates[-10:], 'SVM Predicted # of Confirmed Cases Worldwide': np.round(svm_pred[-10:])})
    svm_df.style.background_gradient(cmap='Reds')
    return render(request, 'predict.html')
     

