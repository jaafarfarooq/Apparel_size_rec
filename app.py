from flask import Flask, render_template,request,jsonify
# from flask_cors import CORS, cross_origin

import pickle
import numpy as np
import math
import sys
chest = pickle.load(open('chest.pkl', 'rb'))
waist = pickle.load(open('waist.pkl', 'rb'))
shoulder = pickle.load(open('shoulder.pkl', 'rb'))
collar = pickle.load(open('collar.pkl', 'rb'))
hips = pickle.load(open('hips.pkl', 'rb'))
kurta = pickle.load(open('kurta.pkl', 'rb'))




app = Flask(__name__)
# CORS(app)

@app.route("/hello")
def home():
    print("here at home")
    return "get request"


@app.route('/BodyMeasurements', methods=['GET'])
def man():
    print("hello broo")
    print("here at req")
    args=request.args
    # age weight height gender hip waist ratio body type 
    data1 =args.get('age')
    data2 = args.get('weight')
    data3 = args.get('height')
    data4 = args.get('gender')
    data5 = args.get('bodyType')
    data6 =float(args.get('hipWaistRatio'))
    print("asdad",data1)
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)

    arr = np.array([[data1, data2, data3, data4,data5,data6]])
    print("asd",arr)
    chestpred = chest.predict(arr)
    waistpred = waist.predict(arr)
    shoulderpred = shoulder.predict(arr)
    collarpred = collar.predict(arr)
    hipspred = hips.predict(arr)
    kurtapred = kurta.predict(arr)
    chestsize=math.ceil(chestpred[0][0]/25.4)
    shouldersize=math.ceil(shoulderpred[0][0]/25.4)
    waistsize=math.floor(waistpred[0][0]/25.4)
    collarsize=math.ceil(collarpred[0][0]/25.4)
    hipssize=math.ceil(hipspred[0][0]/25.4)
    kurtasize=math.ceil(kurtapred[0][0]/25.4)
    print("chestpred:",chestpred)
    print("chest:",chestsize )
    Size='hello'
    TSize=""
    if (chestsize<32):
        if(shouldersize<40):
            TSize= "Extra Small"
        else:
            TSize= "Small"
    elif (chestsize>32 and chestsize<=36):
        if(shouldersize<45):
            TSize= "Small"
        else:
            TSize= "Medium"
    elif (chestsize>36 and chestsize<=40):
        if(shouldersize<55):
            TSize= "Medium"
        else:
            TSize= "Large"
    elif (chestsize>40 and chestsize<=44):
        if(shouldersize<60):
            TSize= "Large"
        else:
            TSize= "Extra Large"
        
    elif (chestsize>44 and chestsize<=48):
        if(shouldersize<65):
            TSize= "Extra Large"
        else:
            TSize= "2-Extra Large"
    elif (chestsize>48):
        TSize= "2-Extra Large"
    height=int(data3)
    length=""
    prewaist="" 
    if(height<66):
        length="28"
    elif(height>=66 and height<=68):
        length="30"
    elif(height>68 and height<=72):
        length="32"
    elif(height>72 and height<76):
        length="34"
    if(waistsize<=28):
        prewaist="28"
    elif(waistsize>28 and waistsize<=30):
        prewaist="30"
    elif(waistsize>30 and waistsize<=32):
        prewaist="32"
    elif(waistsize>32 and waistsize<=34):
        prewaist="34"
    elif(waistsize>34 and waistsize<=36):
        prewaist="36"
    elif(waistsize>36 and waistsize<=38):
        prewaist="38"
    elif(waistsize>38):
        prewaist="40"
    #Size='Chest: '+str(chestsize)+'\n'+'Waist: '+str(waistsize)+'\n'+'Shoulder: '+str(shouldersize)+'\n'+'Collar: '+str(collarsize)+'\n'+'Hips: '+str(hipssize)+'\n'+'Kurta: '+str(kurtasize)+'\n'
    #Size="Tshirt size: "+tshirts(chestsize,shouldersize)+ "Pants size:"+pants(waistsize,data3)+ "Kurta Length"+str(kurtasize)
    Size="Predicted Sizes Tshirt size: "+TSize+"\n ___Pants inseam: "+ length+"\n _Pants waist: "+prewaist+ "___Kurta Length"+str(kurtasize)
    print(Size)
    print("chest"+ str(chestsize))

    obj={
        "chest": chestsize,
        "hip":hipssize,
        "wasit":waistsize,
        "shoulder":shouldersize,
        "collar":collarsize,
        "inseam":length,
        "Tsize":TSize
    }
    response = jsonify(obj)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()