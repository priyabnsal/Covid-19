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
import pandas as pd
import time


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
        # driver = webdriver.Chrome(r'C:\Users\Priya Bansal\OneDrive\Desktop\chromedriver.exe')
        driver = webdriver.Chrome(r"C:\Users\Priya Bansal\OneDrive\Desktop\chromedriver.exe")
        # C:\Users\Priya Bansal\OneDrive\Desktop\chromedriver.exe
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome()
        print("driver 1")

        driver.maximize_window()
        print("driver 2 window")

        driver.get(url)
        # driver.get("https://www.covid19india.org/state/DL")

        print("driver 3 url")

        time.sleep(6)
        print("driver in sriver")

        map_div = driver.find_element(By.ID,"chart")
        print("driver MAP")
        cases_div = driver.find_element(By.CLASS_NAME,"bar")
        

        html_code = map_div.get_attribute('outerHTML')
        print("driver in driver dexcodf")

        driver.quit()
        print("driver end")

        # right hand side portion

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

        res = render(request,'home.html',{"html_code":html_code,"state_name":state_name,"total_state_data":total_state_data,"img_name":"output.png"})
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

    return render(request, 'contact.html')

def d3js(request):
    return render(request, 'd3js.html')

def predict(request):
     if request.POST.get('action') == 'post':

        # Receive data from client
        sepal_length = float(request.POST.get('sepal_length'))
        sepal_width = float(request.POST.get('sepal_width'))
        petal_length = float(request.POST.get('petal_length'))
        petal_width = float(request.POST.get('petal_width'))

        # Unpickle model
        model = pd.read_pickle(r"C:\Users\azander\Downloads\new_model.pickle")
        # Make prediction
        result = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

        classification = result[0]

        PredResults.objects.create(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length,
                                   petal_width=petal_width, classification=classification)

        return JsonResponse({'result': classification, 'sepal_length': sepal_length,
                             'sepal_width': sepal_width, 'petal_length': petal_length, 'petal_width': petal_width},
                            safe=False)

