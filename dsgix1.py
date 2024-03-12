######################################################
# version: v0.9.6.0
# beta
# compiled: 1/11/2024
# DSG
######################################################

import os, sys, logging
from datetime import datetime
import mechanize
import socket
import requests
import subprocess
import time
import uuid
import random
import json
#import yaml

from ip2geotools.databases.noncommercial import DbIpCity
import re, uuid
from urllib import parse
from azure.storage.blob import BlobServiceClient
from sys import exit
from azure.eventhub import EventHubProducerClient, EventData
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter 
from bs4 import BeautifulSoup
from geoip import geolite2

####################################################
#### variables
####################################################
global myurl, ip, macad, res, detl, cntry1, rgn1, cty1, wurl
global xrd, sak, sanm,  s, cn, nam

myurl=""
ip = ""
macad = ""
detl = ""
cntry1 = ""
rgn1 = ""
cty1 = ""

####################################################
### config File Read
####################################################
from configparser import ConfigParser 

ifile = os.path.join(os.path.dirname(__file__)+ "/","dsgfile.txt")
#print('ifile: ' + ifile)
file1 = open(ifile,"r+")
if file1 != "":
 inifile=file1.read()
else:
 inifile = ""
file1.close()

configur = ConfigParser()
ini_file = inifile
#print('ini file in ix1' + ini_file)

# replace variables with environment variables(if exists) before loading ini file
with open(ini_file, 'r') as cfg_file:
    cfg_env_txt = os.path.expandvars(cfg_file.read())

inir = configur.read_string(cfg_env_txt)
#inir =(configur.read('dsgcfg.ini')) 

nam = (configur.get('installation', 'CLI_NME')) 
#print('nam x1:' + nam)
#print(name)

# Merge in user-specific configuration 
#xrd = (configur.read(os.path.expanduser('~/.dsgmiras.ini'))) 
wurl = (configur.get('installation', 'wurl'))
sak = (configur.get('installation', 'storage_account_key'))
sanm = (configur.get('installation', 'storage_account_name'))
cs = (configur.get('installation', 'connection_string'))
cn = (configur.get('installation', 'container_name')) 
ehcs = (configur.get('installation', 'eh_connection_string'))
ehcn = (configur.get('installation', 'eventhub_name'))
file_path = (configur.get('installation', 'work_path')) 

####################################################
def get_url():
	#myurl = input("Enter URL: ")  # enter website
    #print(wurl)
    myurl = "https://"+wurl
    #print(myurl)
    return myurl

####################################################

import mysql.connector
from mysql.connector import errorcode
import sys


# Obtain connection string information from the portal
config = {
	'host':'dsg-emea-vault-msql.mysql.database.azure.com',
	'user':'dsg_msql_mdomo',
	'password':'Wiy%e6oVFH^V',
	'database':'dsgv',
	'client_flags': [mysql.connector.ClientFlag.SSL],
	'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
def get_guid(ipa,macad):
	try:
		conn =  mysql.connector.connect(**config) 
		#print("Connection established")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with the user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor = conn.cursor()

# Create table
	cursor.execute('''create table if not exists dsgguid ( gguid binary(16) default (uuid_to_bin(uuid())) not null primary key,ip varchar(50) not null, macad varchar(50));''')
	#print("Finished creating table.")

# Read data
	#csql = """SELECT bin_to_uuid(gguid) FROM dsgguid where ip = %s;"""
	#print(ipa)
	cursor.execute("SELECT bin_to_uuid(gguid) FROM dsgguid where ip = %s", [ipa])
	rows = cursor.fetchall()
	#print("Read",cursor.rowcount,"row(s) of data.")
# if exists return guid else create and add and return
	if rows:
		print(rows)
		g = rows
	else:
	# Insert data into table
		cursor.execute("INSERT INTO dsgguid (ip, macad) VALUES (%s, %s);", (ipa, macad))
		#print('inserted')
		cursor.execute("SELECT bin_to_uuid(gguid) FROM dsgguid where ip = %s",[ipa])
		rows = cursor.fetchall()
		g = rows
# Cleanup
	conn.commit()
	cursor.close()
	conn.close()  
	return g
####################################################

def get_ip_address(myurl):
    sp = parse.urlsplit(myurl)
    #print(sp.netloc)
    ip_address = socket.gethostbyname(sp.netloc)
    return ip_address

####################################################
####################################################

def printDetails(ip):
    print(ip)
    res = DbIpCity.get(ip, api_key="free")
    #print(res)
    return res
####################################################
####################################################

from uuid import getnode as get_mac

def get_mac_addr():
	# get the mac address
	mac=get_mac()
	"""
	reduce the complexity macstring performs the clearest form of mac address and it is the correct form of valid address here the for loop arranges the valid mac address in orderly formats
	"""
	macString=':'.join(("%012X" % mac) [i:i+2] for i in range(0,12,2))
	# now print the valid mac address in the correct format
	macad =('[' + macString + ']')
	return macad
	
####################################################
#this is the extractor code segment
#the first iteration will focus on specific DOM
#title, a, h1,h2,h3,p,body
####################################################

import requests
from bs4 import BeautifulSoup

def get_dom(u):

	page = requests.get(u)
	htmlData = page.content

	soup = BeautifulSoup(htmlData, 'html.parser')
# get all attributes that point to href # convert the href into strings # hreflist initialize  
	href_list = ('DSG') #[] 
# get all tags 
	tags = {tag.name for tag in soup.findAll("a")}
	if len(tags) > 0:  
	# iterate all tags 
		for tag in tags: 
			# find all element of tag 
			for i in soup.find_all( tag ): 
				# if tag has attribute of href 
				if i.has_attr( "href" ): 
					if len( i['href'] ) > 0: 
						#print(i['href'])
						#href_list.append("".join( i['href']))
						href_list=href_list+','+(i['href'])
					else:
						href_list
			if len(href_list) > 0:
				#print( href_list ) 
				return href_list
			else:
				return href_list

####################################################
def get_dom_title(u):
	page = requests.get(u)
	htmlData = page.content
	soup = BeautifulSoup(htmlData, 'html.parser')
	title = soup.find("title")
	return title
####################################################
def get_dom_plist(u):
	page = requests.get(u)
	Soup = BeautifulSoup(page.text, 'lxml')
	plist = ('DSG ') #[]
# creating a list of all common heading tags
	heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
	for tags in Soup.find_all(heading_tags):
		#print(tags.name + ' --> ' + tags.text.strip())
		#plist=(tags.name + ' --> ' + tags.text.strip())
		plist = plist+','+(tags.text.strip())
		if len(plist) > 0:
			#print(plist)
			return plist
		else:
			return plist
####################################################
import glob

def remfile(fl):
	#file_paths = glob.glob(os.path.join(file_path, ".avro"))
	# loop over each file path and delete the file
	#for fpath in file_paths:
	#	print(fpath)
	#	os.remove(fpath)
	#print(fl)
	os.remove(fl)

####################################################
## file creation
####################################################

def get_avro_file(u):
	dm = get_dom(u)
	if dm == None:
		dm = ('DSG')
	ip = get_ip_address(u)
	t = get_dom_title(u)
	if t is not None:
			title = t.string
	else:
		title = "No definition"
	vplist = get_dom_plist(u)
	if vplist == None:
		vplist = ('DSG')
	detl = printDetails(ip)
	#print(detl)
	city1 = detl.city
	rgn1 = detl.region
	ctry1 = detl.country
	m = get_mac_addr()

	# get current date and time
	current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	#print("Current date & time : ", current_datetime)
	
	# convert datetime obj to string
	str_current_datetime = str(current_datetime)
	
	# create a file object along with extension
	file_name = nam+"_"+str_current_datetime+".avro"
	#file = open(file_name, 'w')

		#Reading and parsing Avro Schema
	if os.path.exists('/Users/krishkrishnan/Dropbox/kkLLM/v0.9/s.avsc'):
		schema = avro.schema.parse(open('/Users/krishkrishnan/Dropbox/kkLLM/v0.9/s.avsc', "r").read()) 
	#Printing Avro Schema
		#print(schema)
	#print( u,title,ip,m ,detl.city,detl.region,detl.country,vplist,dm)

	#Creating a empty Avro file using Avro 
	schemawriter = DataFileWriter(open(file_name, "wb"), DatumWriter(), schema) 
	#Writing data to Avro file using Avro 
	schemawriter.append({"Website_Name": u,"Title": title,"IP_Address": ip,"macaddress_value": m ,"City": detl.city,"State": detl.region,"Country": detl.country,"heading_values":vplist,"a_list":dm})
	schemawriter.close()

####################################################
# Azure upload
######################################################

def get_avro_load(u):
	dm = get_dom(u)
	#print('dm: '+dm)
	if dm == None:
		dm = ('DSG')
	ip = get_ip_address(u)
	#print('ip: '+ip)
	t = get_dom_title(u)
	#print('t: '+t)
	if t is not None:
			title = t.string
	else:
		title = "No definition"
	vplist = get_dom_plist(u)
	#print('vplist: '+vplist)
	if vplist == None:
		vplist = ('DSG')
	detl = printDetails(ip)
	#print(detl)
	city1 = detl.city
	rgn1 = detl.region
	ctry1 = detl.country
	m = get_mac_addr()
	#print('m: '+m)
    
	## get guid for ip+mac combo
	## if exists take the guid else create one add and assign
	gguid = get_guid(ip,m)
	#print(gguid)
	# 	# get current date and time
	current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	#print("Current date & time : ", current_datetime)
	
	# convert datetime obj to string
	str_current_datetime = str(current_datetime)
	
	# create a file object along with extension
	#file_name = nam+"_"+str_current_datetime+".avro"
	#file = open(file_name, 'w')
		#Reading and parsing Avro Schema
	if os.path.exists('s.avsc'):
			schema = avro.schema.parse(open('s.avsc', "r").read()) 
	#Printing Avro Schema
		#print(schema)
	#print( u,title,ip,m ,detl.city,detl.region,detl.country,vplist,dm)
	producer = EventHubProducerClient.from_connection_string(conn_str=ehcs, eventhub_name=ehcn)
	for y in range(0,10):    # For each run produce 10 events. 
		event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
		reading = {"Anumin": gguid, "Website_Name": u,"Title": title,"IP_Address": ip,"macaddress_value": m ,"City": detl.city,"State": detl.region,"Country": detl.country,"heading_values":vplist,"a_list":dm}
		s2 = json.dumps(reading) # Convert the reading into a JSON string.
		event_data_batch.add(EventData(s2)) # Add event data to the batch.
		producer.send_batch(event_data_batch) # Send the batch of events to the event hub.
		# Close the producer.    
		producer.close()
######################################################
def azure_load():
	# Finding files with extension using for loop
	import os
	import sys

	#file_path = sys.argv[1]
	#print(file_path)
	# Specifies the path in path variable
	for i in os.listdir(file_path):
		# List files with .avro
		if i.endswith(".avro"):
			#uploadToBlobStorage(file_path,i)
			remfile(file_path+ i)
########################################################################
#### the main
########################################################################
def main():
    """business logic for when running this module as the primary one!"""
    u = get_url()
    if u != "":
     ip = get_ip_address(u)
     if ip != "":
       get_avro_load(u)
       azure_load()

# Here's our payoff idiom!
if __name__ == '__main__':
    main()

