#!/usr/bin/python3
from . import data
import datetime
def color_from_year(year,enc = "DE"):
	year %= 10
	color = data.year_to_color[year]
	if(color in data.color_enc[enc]):
		return data.color_enc[enc][color]
	return color

def last_year_from_color(color,enc = "DE"):
	year_end = 0
	if(color in data.color_enc_rev[enc]):
		year_end =  data.color_to_year[data.color_enc_rev[enc][color]]
	elif( color in data.color_to_year):
		year_end = data.color_to_year[color]
	else:
		return 0
	today = datetime.datetime.today()
	# strip the last digit
	t = today.replace(year = today.year // 10)
	t = t.replace(year = t.year * 10)
	t = t.replace(year = t.year + year_end)
	if( (t - today).days > 0):
		t = t.replace(year = t.year - 5)
	return t.year
	
def get_current_color(enc = "DE"):
	return color_from_year(datetime.datetime.today().year,enc)




