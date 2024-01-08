import json

import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from account.models import User
env = environ.Env()
from rest_framework import generics
# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import http.client
import urllib.request
import urllib.parse
import json
import hmac
import hashlib
import base64
from adsapi.models import *
accesskey="a2b08960-86b3-11ed-a1b9-ffe33bc79fc2"
secretkey="6f7d9ce55c3225408200999df006c21941a20e8f"

environment="test"
# accesskey="e6e2f2e0-8a8f-11ed-ab81-b5f41ccd0abb"
# secretkey="c52703362a8ba8c24a7d064bb55a69b78605278d"
# environment="live"



remote_script="https://payments.open.money/layer"
sample_data = dict()
sample_data["amount"] = "12.00"
sample_data["currency"] = "INR"
sample_data["name"] = "John Doe"
sample_data["email_id"]="john.doe@dummydomain.com"
sample_data["contact_number"]= "9831111111"
sample_data["mtx"]= ""
sample_data["empty"]=""
# sample_data["image"]=""


BASE_URL_SANDBOX = "sandbox-icp-api.bankopen.co";
BASE_URL_UAT = "icp-api.bankopen.co";					   

# Create your views here.

class EnquiryListCreate(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer



@csrf_exempt
def index(request):
	global accesskey,secretkey,environment,remote_script,sample_data
	error=""
	layer_payment_token_data=dict()
	payment_token_data = dict()
	token_id=""
	hash = ""
	layer_params=""
	sample_data["mtx"] = random.randint(1,200)
	
	
	layer_payment_token_data = create_payment_token(sample_data,accesskey,secretkey,environment)
	
	if layer_payment_token_data:
		for k in layer_payment_token_data.keys():
			if k == "error":
				error = layer_payment_token_data[k]
		
	if len(error) == 0 and len(layer_payment_token_data["id"]) < 1:
		error="E55 Payment error. Token data empty."
			
	if len(error) == 0 and len(layer_payment_token_data["id"]) > 0:
		payment_token_data = get_payment_token(layer_payment_token_data["id"],accesskey,secretkey,environment)
	
	if payment_token_data:		
		for k in payment_token_data.keys():
			if k == "error":
				error = payment_token_data[k]
				
	if len(error) == 0 and len(payment_token_data["id"]) < 1:
		error="Payment error. Layer token ID cannot be empty."
		
	if len(error) == 0 and len(payment_token_data["id"]) > 0 and payment_token_data["status"]=="paid": 
		error="Layer: this order has already been paid."
		
	if len(error) == 0 and str(payment_token_data["amount"]) != str(sample_data["amount"]): 
		error="Layer: an amount mismatch occurred."
		
	if error == "":
		gen = dict()
		gen["amount"]=payment_token_data["amount"]
		gen["id"]=payment_token_data["id"]
		gen["mtx"]=sample_data["mtx"]
		hash=create_hash(gen,accesskey,secretkey)		
		layer_params = "{payment_token_id:"+payment_token_data["id"]+",accesskey:"+accesskey+"}"
		token_id=payment_token_data["id"]
		
	
	return render(request,
	'layerpayment/checkout.html',
	{'txnid':str(sample_data["mtx"]),
	'fullname':sample_data["name"],
	'email':sample_data["email_id"],
	'mobile':sample_data["contact_number"],
	'amount':str(sample_data["amount"]),
	'currency':sample_data["currency"],
	'remote_script':remote_script,
	'token_id':token_id,
	'hash':hash,
	'accesskey':accesskey,
	'layer_params':layer_params,
	'error':error})


from rest_framework.views import APIView
import json


class callback_class(APIView):
	def post( self,request , format=None):
		global accesskey,secretkey,environment
		error=""
		status=""
		payment_data=dict()
	
		# response = request.POST
		reponse1=request.data
		print("----------------reponse",reponse1)
		if len(response["layer_payment_id"]) == 0:
			error = "Invalid payment id"
		if len(error)==0:
			vhash=dict()
			vhash["amount"] =response["layer_order_amount"]
			vhash["id"]=response["layer_pay_token_id"]
			vhash["mtx"]=response["tranid"]
			if not verify_hash(vhash,response["hash"],accesskey,secretkey):
				error="Invalid payment response...Hash mismatch"
		if len(error) == 0:
			payment_data = get_payment_details(response["layer_payment_id"],accesskey,secretkey,environment)
	
		if payment_data:
			for k in payment_data.keys():
				if k == "error":
					error = payment_data[k]
		if len(error) == 0 and payment_data["payment_token"]["id"] != response["layer_pay_token_id"]:
			error = "Layer: received layer_pay_token_id and collected layer_pay_token_id doesnt match"
		if len(error) == 0 and payment_data["amount"] != response["layer_order_amount"]:
			error = "Layer: received amount and collected amount doesnt match"
		if len(error) == 0 and payment_data["payment_token"]["status"] != "paid":
			status = "Transaction failed..."+payment_data["payment_error_description"]
		elif len(error) == 0:
			status = "Transaction Successful"
		data={'errorstring':error,'status':status}
		print(data)
		return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt	
def callback(request):
	global accesskey,secretkey,environment
	error=""
	status=""
	payment_data=dict()
	
	response = request.POST
	print("Received data:", response)

	print("----------------reponse",response,response["layer_pay_token_id"])
 	
	if len(response["layer_payment_id"]) == 0:
		error = "Invalid payment id"
	if len(error)==0:
		vhash=dict()
		vhash["amount"] =response["layer_order_amount"]
		vhash["id"]=response["layer_pay_token_id"]
		vhash["mtx"]=response["tranid"]
		if not verify_hash(vhash,response["hash"],accesskey,secretkey):
			error="Invalid payment response...Hash mismatch"
	if len(error) == 0:
		payment_data = get_payment_details(response["layer_payment_id"],accesskey,secretkey,environment)
	
	if payment_data:
		for k in payment_data.keys():
			if k == "error":
				error = payment_data[k]
	if len(error) == 0 and payment_data["payment_token"]["id"] != response["layer_pay_token_id"]:
		error = "Layer: received layer_pay_token_id and collected layer_pay_token_id doesnt match"
	if len(error) == 0 and payment_data["amount"] != response["layer_order_amount"]:
		error = "Layer: received amount and collected amount doesnt match"
	if len(error) == 0 and payment_data["payment_token"]["status"] != "paid":
		status = "Transaction failed..."+str(payment_data["payment_error_description"] if payment_data["payment_error_description"] else "")
	elif len(error) == 0:
		status = "Transaction Successful"
	data={'errorstring':error,'status':status}
	finalData={}
	finalData["errorstring"]=data["errorstring"]
	finalData["status"]=data["status"]
	s=TransactionDetails.objects.get(payment_token_id=response["layer_pay_token_id"])
	s.refresh_from_db()
	s.payment_id=response["layer_payment_id"]
	if status=="Transaction Successful" and s.paymentStatus != "Success":
		s.paymentStatus="Success"
		finalData["status"]="Success"
		finalData["payment_id"]=response["layer_payment_id"]
		finalData["plan"]=s.plan
		finalData["email"]=s.email
		finalData["transactionId"]=s.tranid
		finalData["amount"]=s.order_payment_amount   
		finalData["phoneNumber"]=s.phoneNumber
		finalData["name"]=s.userID.name
		json1_file = open('D:/Hola9UpdatedCode-master (2)/Hola9UpdatedCode-master/paymentapi/json/pricingPlan.json','r+', encoding="utf-8")
		planJsonOBJ=json.load(json1_file)
		planJsonOBJ1 = open('D:/Hola9UpdatedCode-master (2)/Hola9UpdatedCode-master/paymentapi/json/businessPlan.json','r+', encoding="utf-8")
		businessProfile=json.load(planJsonOBJ1)
		user=s.userID
		print("json data printing here",json1_file)
		
		OrderID=response["layer_payment_id"]

		if s.plan == "Premium":
			category = s.plan
			validity = s.monthsVale
			city = businessProfile["Premium"]["city"]
			visiblity = businessProfile["Premium"]["visiblity"]
			teleSupport = businessProfile["Premium"]["teleSupport"]
			chatSupport = businessProfile["Premium"]["chatSupport"]
			dedicatedRm = businessProfile["Premium"]["dedicatedRm"] 
			hol9Website = businessProfile["Premium"]["hola9Website"]

			x = BusinessPricing.objects.create(
				user=user, category=category, validity=validity, visiblity=visiblity,
				NoAds=s.adsValue, OrderID=OrderID, city=s.City,
				teleSupport=teleSupport, chatSupport=chatSupport,
				dedicatedRm=dedicatedRm, hol9Website=hol9Website
			)
			
			finalData["category"] = category
			finalData["validity"] = validity
			finalData["city"] = city
			finalData["visiblity"] = visiblity
			finalData["teleSupport"] = teleSupport
			finalData["chatSupport"] = chatSupport
			finalData["dedicatedRm"] = dedicatedRm
			finalData["hol9Website"] = hol9Website
   
		elif s.plan == "Featured":
			# category = businessProfile["Featured"]["category"]
			category = s.plan
			# validity = businessProfile["Featured"]["selectmonths"]
			validity = s.monthsVale
			city = businessProfile["Featured"]["city"]
			visiblity = businessProfile["Featured"]["visiblity"]
			teleSupport = businessProfile["Featured"]["teleSupport"]
			chatSupport = businessProfile["Featured"]["chatSupport"]
			dedicatedRm = businessProfile["Featured"]["dedicatedRm"]
			hol9Website = businessProfile["Featured"]["hola9Website"]

			x = BusinessPricing.objects.create(
				user=user, category=category, validity=validity, city=s.City,
				visiblity=visiblity, NoAds=s.adsValue, OrderID=OrderID,
				teleSupport=teleSupport, chatSupport=chatSupport,
				dedicatedRm=dedicatedRm, hol9Website=hol9Website
			)
			
			finalData["category"] = category
			finalData["validity"] = validity
			finalData["city"] = city
			finalData["visiblity"] = visiblity
			finalData["teleSupport"] = teleSupport
			finalData["chatSupport"] = chatSupport
			finalData["dedicatedRm"] = dedicatedRm
			finalData["hol9Website"] = hol9Website
		elif s.plan=="VerifiedCustomer":
			x=VerifiedCustomerMain.objects.create(userid=user,plan_type=s.plan,price=234,validity=30,OrderID=OrderID)
		else:
			planData=planJsonOBJ[s.plan]
			category =planData["category"]
			days =planData["days"]
			regulars =planData["regulars"]
			# topAds =planData["topAds"]
			# featured=planData["featured"]
			teleSupport=planData["teleSupport"]
			response=planData["response"]
			chatSupport=planData["chatSupport"]
			dedicatedRm=planData["dedicatedRm"]
			hol9Website=planData["hola9Website"]
			validity=planData["validity"]
			x=Pricing.objects.create(user=user,category=category,days=days,regulars=regulars,teleSupport=teleSupport,response=response,chatSupport=chatSupport,dedicatedRm=dedicatedRm,hol9Website=hol9Website,OrderID=OrderID,validity=validity)
			finalData["days"]=days
			finalData["regulars"]=regulars
			# finalData["topAds"]=topAds
			# finalData["featured"]=featured
			finalData["teleSupport"]=teleSupport
			finalData["response"]=response
			finalData["chatSupport"]=chatSupport
			finalData["dedicatedRm"]=dedicatedRm
			finalData["hol9Website"]=hol9Website
		x.save()
		s.save()
	else:
		s.refresh_from_db()
		s.paymentStatus="Failed"
		s.save()

	print(data,payment_data)
	return HttpResponse(json.dumps(finalData), content_type='application/json')
	


def create_payment_token(data,accesskey,secretkey,environment):

	response=dict()
	
	try:
		emptykeys=[]
		for k in data.keys():
			if len(str(data[k]))<1:
				emptykeys.append(k)
		for i in emptykeys:
			del data[i]
		response = http_post(data,"payment_token",accesskey,secretkey,environment)
	except Exception as ex:			
		response["error"]=ex
	
	return response

from rest_framework.views import APIView
import json
class create_payment_token_Class(APIView):
	def post( self,request , format=None):
		global accesskey,secretkey,environment,remote_script,sample_data
		data = dict()
		error=""
		layer_payment_token_data=dict()
		payment_token_data = dict()
		token_id=""
		hash = "" 
		layer_params=""
		adsValue=request.data.get("adsValue")
		monthsVale=request.data.get("monthsVale")
		planJsonOBJ = open('D:/Hola9UpdatedCode-master (2)/Hola9UpdatedCode-master/paymentapi/json/businessPlan.json','r+', encoding="utf-8")
		businessProfile=json.load(planJsonOBJ)
		print("businessProfilePlanVALUE",businessProfile)
		name=request.data.get("IdValue")
		planValue=request.data.get("planValue")
		adsCategory=request.data.get("adsCategory")
		if planValue=="Silver":
			data["amount"] = str(99+(99*18/100))
		elif planValue=="VerifiedCustomer":
			data["amount"] =str(199+(299*18/100))
		elif planValue=="Gold":
			data["amount"] =str(299+(299*18/100))
		elif planValue=="Platinum":
			data["amount"] = str(int(799+(799*18/100)))+".00"
		elif planValue=="Premium":
			category_prices = businessProfile['Premium']['adscategory'][adsCategory]
			priceData=int(request.data.get("PriceValue"))
			print("pricing data ",priceData,type(priceData))
			data["amount"]=str(int(priceData+(priceData*18/100)))+".00"  # need to put dynamic value here also that one 
			print("data[amount]...........",data["amount"])
		elif planValue=="Featured":
			category_prices = businessProfile['Featured']['adscategory'][adsCategory]
			data["amount"]=str(int(category_prices+(category_prices*18/100)))+".00"   # need to put dynamic value here also that one 
		else:
			data["amount"] = ""
		print(name,planValue,data["amount"])
		userData=User.objects.get(pk=name)
		data["name"] =userData.name
		data["email_id"]=userData.email
		data["contact_number"]=request.data.get("Phone")
		data["currency"] = "INR"
		data["mtx"]= random.randint(1,2000000)
		data["empty"]=""
		
		response=dict()
		try:
			emptykeys=[]
			for k in data.keys():
				if len(str(data[k]))<1:
					emptykeys.append(k)
			for i in emptykeys:
				del data[i]
			response = http_post(data,"payment_token",accesskey,secretkey,environment)
			print("@@@@@@@reponse",response)
		except Exception as ex:			
			response["error"]=ex
		print(response)
		layer_payment_token_data=response
		if layer_payment_token_data:
			for k in layer_payment_token_data.keys():
				if k == "error":
					error = layer_payment_token_data[k]
		if len(error) == 0 and len(layer_payment_token_data["id"]) < 1:
			error="E55 Payment error. Token data empty."
			
		if len(error) == 0 and len(layer_payment_token_data["id"]) > 0:
			payment_token_data = get_payment_token(layer_payment_token_data["id"],accesskey,secretkey,environment)
		print("payment_token_data",payment_token_data)
		if payment_token_data:		
			for k in payment_token_data.keys():
				if k == "error":
					error = payment_token_data[k]



		if len(error) == 0 and len(payment_token_data["id"]) < 1:
			error="Payment error. Layer token ID cannot be empty."
		
		if len(error) == 0 and len(payment_token_data["id"]) > 0 and payment_token_data["status"]=="paid": 
			error="Layer: this order has already been paid."
		
		if len(error) == 0 and str(payment_token_data["amount"]) != str(data["amount"]): 
			error="Layer: an amount mismatch occurred."
		if error == "":
			gen = dict()
			gen["amount"]=payment_token_data["amount"]
			gen["id"]=payment_token_data["id"]
			gen["mtx"]=data["mtx"]
			hash=create_hash(gen,accesskey,secretkey)		
			layer_params = "{payment_token_id:"+payment_token_data["id"]+",accesskey:"+accesskey+"}"
			token_id=payment_token_data["id"]
        
		if len(error) == 0:
			if payment_token_data["status"]=="paid":
				assign_payment_status = "Success"
			else:
				assign_payment_status = "Pending"
		else:
			if payment_token_data["status"]=="paid":
				assign_payment_status = "Success"
			else:
				assign_payment_status = f"Failed...{error}"

		if not TransactionDetails.objects.filter(payment_token_id=token_id).exists():
			s=TransactionDetails.objects.create(payment_token_id=token_id,payment_id="",userID_id=name,plan=planValue,paymentStatus=assign_payment_status,email=data["email_id"],tranid=data["mtx"],order_payment_amount=data["amount"],phoneNumber=data["contact_number"],adsValue=adsValue,monthsVale=monthsVale,City=request.data.get("city"))
		else:
			s=TransactionDetails.objects.get(payment_token_id=token_id)
			s.paymentStatus = assign_payment_status
			s.save()
		obj={'txnid':str(data["mtx"]),
		'fullname':data["name"],
		'email':data["email_id"],
		'mobile':data["contact_number"],
		'amount':str(data["amount"]),
		'currency':data["currency"],
		'remote_script':remote_script,
		'token_id':token_id,
		'hash':hash,
		'accesskey':accesskey,
		'layer_params':layer_params,
		'error':error}
		print("last output",obj)
		return HttpResponse(json.dumps(obj), content_type='application/json')



def get_payment_token(payment_token_id,accesskey,secretkey,environment):
	response=dict()
	try:
		if len(payment_token_id)==0 or payment_token_id.isspace():
			response["error"]="payment_token_id cannot be empty"				
		else:
			response = http_get("payment_token/" + payment_token_id,accesskey,secretkey,environment)
	except Exception as ex:
		response["error"] = ex
	
	return response
	

def get_payment_details(payment_id,accesskey,secretkey,environment):
	response=dict()
	try:
		if len(payment_id)==0 or payment_id.isspace():			
			response["error"]="pyment_id cannot be empty"	
		else:
			response=http_get("payment/"+payment_id,accesskey,secretkey,environment)
	except Exception as ex:
		response["error"] = ex
	
	return response
	

def http_post(data,route,accesskey,secretkey,environment):
	response = ""
	url = BASE_URL_SANDBOX 
	if environment == "live":
		url = BASE_URL_UAT 
	
	resource = "/api/"+route
	
	try:
		conn = http.client.HTTPSConnection(url,timeout=10)
		headers = {'Content-type': 'application/json',"Authorization":"Bearer "+accesskey+":"+secretkey}
		jdata = json.dumps(data)
		conn.request('POST', resource, jdata, headers)
		resp = conn.getresponse()		
		rdata = resp.read().decode('utf-8')
		conn.close()
		response = json.loads(rdata)		
	except Exception as ex:
		print(ex)
	
	return response
	
def http_get(route,accesskey,secretkey,environment):
	response = ""
	url = BASE_URL_SANDBOX 
	if environment == "live":
		url = BASE_URL_UAT 
	resource = "/api/"+route
	
	try:
		conn = http.client.HTTPSConnection(url,timeout=10)
		headers = {'Content-type': 'application/json',"Authorization":"Bearer "+accesskey+":"+secretkey}
		conn.request("GET", resource,"",headers)
		resp = conn.getresponse()
		rdata = resp.read().decode('utf-8')
		conn.close()
		response = json.loads(rdata)
	except Exception as ex:
		print(ex)
	
	return response
	
	
def create_hash(data,accesskey,secretkey):
	hash=""
	try:
		pipeSeperatedString=accesskey+"|"+str(data["amount"])+"|"+data["id"]+"|"+str(data["mtx"])
		signature = hmac.new(
			bytes(secretkey , 'latin-1'),  
			msg = bytes(pipeSeperatedString , 'latin-1'), 
			digestmod = hashlib.sha256).hexdigest().upper()
		
		base64_bytes = base64.b64encode(signature.encode('ascii'))
		hash = base64_bytes.decode('ascii')
		 
	except Exception as ex:
		hash = ex
		
	return hash
	

def verify_hash(data,rec_hash,accesskey,secretkey):
	gen_hash = create_hash(data,accesskey,secretkey)
	if gen_hash == rec_hash:
		return True
	else:
		return False

from django.core import serializers
from django.http import HttpResponse
class userTransData(APIView):
	def post( self,request , format=None):
		userID=request.data.get('userID')
		limit = request.data.get('limit')
		s= TransactionDetails.objects.all()
		if userID is not None:
			s=s.filter(userID=userID)
		else:
			s=s
		if limit is not None:
			s=s.order_by('-id')[:int(limit)]	

		# s=TransactionDetails.objects.filter(userID_id=userID)
		
		data=serializers.serialize('json',s)
		return HttpResponse(data, content_type='application/json')

# @api_view(['POST'])
# def start_payment(request):
#     # request.data is coming from frontend
#     amount = request.data['amount']
#     name = request.data['name']
#     email = request.data['email']

#     # we are saving an order with keeping isPaid=False
#     order = Order.objects.create(product_name=name,
#                                  order_amount=amount,
#                                  user_email=email, )

#     # in case if you want to use above order instance just serialize it
#     serializer = OrderSerializer(order)

#     # we have to send the param_dict to the frontend
#     # these credentials will be passed to paytm order processor to verify the business account
#     param_dict = {
#         'MID': env('MERCHANTID'),
#         'ORDER_ID': str(order.id),
#         'TXN_AMOUNT': str(amount),
#         'CUST_ID': email,
#         'INDUSTRY_TYPE_ID': 'Retail',
#         'WEBSITE': 'WEBSTAGING',
#         'CHANNEL_ID': 'WEB',
#         'CALLBACK_URL': 'http://127.0.0.1:8000/api/payment/handlepayment/',
#         # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
#     }

#     # everytime payment happend we will create new checksum (unique hashed string) using our merchant key
#     param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, env('MERCHANTKEY'))
#     # we will send the dictionary with all the credentials to the frontend
#     return Response({'param_dict': param_dict})


# @api_view(['POST'])
# def handlepayment(request):
#     checksum = ""
#     # the request.POST is coming from paytm
#     form = request.POST

#     response_dict = {}
#     order = None  # initialize the order varible with None

#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
#             checksum = form[i]

#         if i == 'ORDERID':
#             # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
#             order = Order.objects.get(id=form[i])

#     # we will verify the payment using our merchant key and the checksum that we are getting from paytm request.POST
#     verify = Checksum.verify_checksum(response_dict, env('MERCHANTKEY'), checksum)
    
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             # if the response code is 01 that means our transaction is successfull
#             print('order successful')
#             # after successfull payment we will make isPaid=True and will save the order
#             order.isPaid = True
#             order.save()
#             success="succ"+"id"+str(random.randint(1000000000,99999999999999999999))
#             s=TransationIdone.objects.create(id1=success,dateid=datetime.datetime.now(),message="success")
#             s.save()
#             # we will render a template to display the payment status
#             return render(request, 'paytm/paymentstatus.html', {'response': response_dict,'success':success})
#         else:
#             fail="fail"+"?id"+str(random.randint(1000000000,99999999999999999999))
#             s=TransationIdone.objects.create(id1=success,dateid=datetime.datetime.now(),message="fail")
#             s.save()

#             print('order was not successful because' + response_dict['RESPMSG'])
#             return render(request, 'paytm/paymentstatus.html', {'response': response_dict,'success':fail})


# import requests

# url = "https://sandbox-icp-api.bankopen.co/api/payment_token"
# from django.http import HttpResponse
# @api_view(['POST'])
# def tokenPayment(request):
#     payload = {
#     "amount": 5,
#     "contact_number": "8400952502",
#     "email_id": "anuj840084@gmail.com",
#     "currency": "INR",
#     "mtx": "121111"
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "Authorization": "Bearer 0fd5f2d0-3fe3-11ed-aa16-21bc73a31b48"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print(response.text)
#     return HttpResponse("success" , content_type='application/json')


# @api_view(['POST'])
# def start_payment(request):
#     # request.data is coming from frontend
#     amount = request.data['amount']
#     name = request.data['name']
#     # setup razorpay client
#     client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
#     print(type(amount),"amount",amount)
#     print(type(name),"name",name)
#     name=User.objects.get(id=name)
#     name=name.email
#     print("name",name)
#     # create razorpay order
#     payment = client.order.create({"amount": int(amount) * 100, 
#                                    "currency": "INR", 
#                                    "payment_capture": "1"})

#     # we are saving an order with isPaid=False
#     order = Order.objects.create(order_product=name, 
#                                  order_amount=amount, 
#                                  order_payment_id=payment['id'])

#     serializer = OrderSerializer(order)

#     """order response will be 
#     {'id': 17, 
#     'order_date': '20 November 2020 03:28 PM', 
#     'order_product': '**product name from frontend**', 
#     'order_amount': '**product amount from frontend**', 
#     'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
#     'isPaid': False}"""

#     data = {
#         "payment": payment,
#         "order": serializer.data
#     }
#     return Response(data)


# @api_view(['POST'])
# def handle_payment_success(request):
#     # request.data is coming from frontend
#     res = json.loads(request.data["response"])

#     """res will be:
#     {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
#     'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
#     'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
#     """

#     ord_id = ""
#     raz_pay_id = ""
#     raz_signature = ""

#     # res.keys() will give us list of keys in res
#     for key in res.keys():
#         if key == 'razorpay_order_id':
#             ord_id = res[key]
#         elif key == 'razorpay_payment_id':
#             raz_pay_id = res[key]
#         elif key == 'razorpay_signature':
#             raz_signature = res[key]

#     # get order by payment_id which we've created earlier with isPaid=False
#     order = Order.objects.get(order_payment_id=ord_id)

#     data = {
#         'razorpay_order_id': ord_id,
#         'razorpay_payment_id': raz_pay_id,
#         'razorpay_signature': raz_signature
#     }

#     client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

#     # checking if the transaction is valid or not if it is "valid" then check will return None
#     check = client.utility.verify_payment_signature(data)

#     if check is None:
#         print("Redirect to error url or error page")
#         return Response({'error': 'Something went wrong'})

#     # if payment is successful that means check is None then we will turn isPaid=True
#     order.isPaid = True
#     order.save()

#     res_data = {
#         'message': 'payment successfully received!'
#     }

#     return Response(res_data)



# from rest_framework.views import APIView

# class SuccessPaymentData(APIView) :
#     def post( self,request , format=None):
#         pass 

# import hashlib
# from django.shortcuts import render,HttpResponse
# from backendapi import settings
# # from payment.models import *
# from backendapi.settings import PAYU_MERCHANT_KEY, PAYU_MERCHANT_SALT
# from rest_framework.views import APIView
# from rest_framework.response import Response
# # from paywix.payu import PAYU
# # from payu.models import Payment
# # payu=PAYU()
# # Create your views here.

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.generics import GenericAPIView
# from paymentapi.models import Transaction
# from hashlib import sha512
# import hashlib
# from django.conf import settings
# from backendapi.settings import PAYU_MERCHANT_KEY, PAYU_MERCHANT_SALT
# class GenerateHashKeyView(GenericAPIView):
#     """
#     Class for creating API view for Payment gateway homepage.
#     """
#     permission_classes = ()
#     authentication_classes = ()

#     def post(self, request, *args, **kwags):
#         """
#         Function for creating a charge.
#         """
#         print("hello")
#         key = PAYU_MERCHANT_KEY
#         txnid = str(request.data.get('txnid'))
#         amount = str(request.data.get('amount'))
#         productinfo = str(request.data.get('productinfo'))
#         firstname = str(request.data.get('firstname'))
#         email = str(request.data.get('email'))
#         phone="9876543210"
#         salt = PAYU_MERCHANT_SALT

#         output_data = {
#             'key': key,
#             'salt': salt,
#             'txnid': txnid,
#             'amount': amount,
#             'productinfo': productinfo,
#             'firstname': firstname,
#             'email': email,
#         }
#         print("output_data",output_data)
#         keys = ('txnid', 'amount', 'productinfo', 'firstname', 'email',
#                 'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
#                 'udf9', 'udf10')

#         def generate_hash(input_data, *args, **kwargs):
#             hash_value = str(getattr(settings, 'PAYU_MERCHANT_KEY', None))

#             for k in keys:
#                 if input_data.get(k) is None:
#                     hash_value += '|' + str('')
#                 else:
#                     hash_value += '|' + str(input_data.get(k))

#             hash_value += '|' + str(getattr(settings, 'PAYU_MERCHANT_SALT', None))
#             hash_value = sha512(hash_value.encode()).hexdigest().lower()
#             # Transaction.objects.create(
#             #     transaction_id=input_data.get('txnid'), amount=input_data.get('amount'))
#             return hash_value

#         get_generated_hash = generate_hash(request.data)

#         output_data['hash_key'] = get_generated_hash

#         return Response(output_data)


# class SuccessView(GenericAPIView):

#     def post(self, request):
#         status = request.data["status"]
#         firstname = request.data["firstname"]
#         amount = request.data["amount"]
#         txnid = request.data["txnid"]
#         posted_hash = request.data["hash"]
#         key = request.data["key"]
#         productinfo = request.data["productinfo"]
#         email = request.data["email"]
#         salt = PAYU_MERCHANT_SALT

#         try:
#             additional_charges = request.data["additionalCharges"]
#             ret_hash_seq = additional_charges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname +\
#                            '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
#         except Exception:
#             ret_hash_seq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|'\
#                          + amount + '|' + txnid + '|' + key

#         resonse_hash = hashlib.sha512(ret_hash_seq.encode()).hexdigest().lower()

#         if resonse_hash == posted_hash:
#             transaction = Transaction.objects.get(transaction_id=txnid)
#             transaction.payment_gateway_type = request.data.get('PG_TYPE')
#             transaction.transaction_date_time = request.data.get('addedon')
#             transaction.mode = request.data.get('mode')
#             transaction.status = status
#             transaction.amount = amount
#             transaction.mihpayid = request.data.get('mihpayid')
#             transaction.bankcode = request.data.get('bankcode')
#             transaction.bank_ref_num = request.data.get('bank_ref_num')
#             transaction.discount = request.data.get('discount')
#             transaction.additional_charges = request.data.get('additionalCharges', 0)
#             transaction.txn_status_on_payu = request.data.get('unmappedstatus')
#             transaction.hash_status = "Success" if resonse_hash == request.data.get('hash') else "Failed"
#             transaction.save()
#             message = ["Thank You. Your order status is " + status,
#                        "Your Transaction ID for this transaction is " + txnid,
#                        "We have received a payment of Rs. " + amount,
#                        "Your order will soon be shipped."]
#         else:
#             message = ["Invalid Transaction. Please try again."]
#         output_data = {
#             "txnid": txnid,
#             "status": status,
#             "amount": amount
#         }
#         return Response(output_data, message)



