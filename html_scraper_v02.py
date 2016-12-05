from bs4 import BeautifulSoup
import urllib
import numpy as np
from numpy import array
import re


# Get the HTML code associated to the flight of interest
t = urllib.urlopen('http://flightaware.com/live/flight/VRD409/history/20161018/1530Z/KJFK/KLAX/tracklog').read()
# Process the HTML code with BeautifulSoup
soup = BeautifulSoup(t)

class_list = ["smallrow1","smallrow2"]
table = soup.find_all('tr',class_=class_list)

print len(table)

# span all the rows of the HTML table whose class is smallrow2

Timestamp = [];
Day       = [];
Hour      = [];
Minute    = [];
Second    = [];
AMPM      = [];
Latitude  = [];
Longitude = [];
Speed     = [];
Altitude  = [];

listdays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
listAMPM = ['AM','PM'];

for i in range(0,len(table)):
	col = table[i].find_all('td')
	# if len(col)==10, it means we have a row of the table with 10 columns,
	# i.e., a row that identifies a recorded position (with all the
	# associated information) of the aircraft
	if len(col)==10:
		for j in range(0,len(col)):
			el = col[j].find_all('span')
			# First column: Timestamp with day and time in the 
			# HH:MM:SS AM/PM format
			if j==0:
				for k in range(0,len(el)):
					if k==0:
						print('Timestamp:')
						print str(el[k].contents[0])
						text = col[j].renderContents()
						print text
						Timestamp.append(str(el[k].contents[0]))
						for item in listdays:
							if item in str(el[k].contents[0]):
								print item
								indices = [ii for ii, s in enumerate(listdays) if item in s]
								print float(np.asarray(indices))
								Day.append(float(np.asarray(indices))+1.0)
								# Get rid of DAY and space before time in HH:MM:SS format
								dummy = (re.sub(item+' ','',el[k].contents[0]))
								print dummy
						for item in listAMPM:
							if item in str(dummy):
								indices = [ii for ii, s in enumerate(listAMPM) if item in s]
								AMPM.append(float(np.asarray(indices))+1.0)
								# Get rid of space and AM or PM after time in HH:MM:SS format
								HHMMSS = (re.sub(' '+item,'',dummy))
						print HHMMSS
						print HHMMSS[0:2]
						print HHMMSS[3:5]
						print HHMMSS[6:8]
						Hour.append(float(HHMMSS[0:2]))
						Minute.append(float(HHMMSS[3:5]))
						Second.append(float(HHMMSS[6:8]))
			# Second column: Latitude [deg]
			elif j==1:
				for k in range(0,len(el)):
					if k==0:
						print('Latitude:')
						print str(el[k].contents[0])
						Latitude.append(float(str(el[k].contents[0])))
			# Third column: Longitude [deg]
			elif j==2:
				for k in range(0,len(el)):
					if k==0:
						print('Longitude:')
						print str(el[k].contents[0])
						Longitude.append(float(str(el[k].contents[0])))
			# Sixth column: Speed [kts]
			elif j==5:
				print col[j]
				text = col[j].renderContents()
				print text
				Speed.append(float(str(text)))
			# Eigth column: Altitude [feet]
			elif j==7:
				for k in range(0,len(el)):
					if k==0:
						print('Altitude [feet]:')
						print (re.sub(',','',el[k].contents[0]))
						Altitude.append(float(re.sub(',','',el[k].contents[0])))
	print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	print('%%% End of current row of the HTML table %%%')
	print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

Day_array       = array([Day])
Hour_array      = array([Hour])
Minute_array      = array([Minute])
Second_array      = array([Second])
AMPM_array      = array([AMPM])
Latitude_array  = array([Latitude])
Longitude_array = array([Longitude])
Speed_array     = array([Speed])
Altitude_array  = array([Altitude])

print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print (Day_array.shape)
print (Latitude_array.shape)
print (Longitude_array.shape)
print (Speed_array.shape)
print (Altitude_array.shape)
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

Info_array      = np.hstack([Day_array.T,Hour_array.T,Minute_array.T,Second_array.T,AMPM_array.T,Latitude_array.T,Longitude_array.T,Speed_array.T,Altitude_array.T])

np.savetxt('test.txt',Info_array,fmt='%2d %2d %2d %2d %2d %5.3f %5.3f %5.3f %5.3f',delimiter=' ')

