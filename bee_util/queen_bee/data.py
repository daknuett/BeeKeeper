#!/usr/bin/python3

year_to_color = {0:"blue",
	1:"white",
	2:"yellow",
	3:"red",
	4:"green",
	5:"blue",
	6:"white",
	7:"yellow",
	8:"red",
	9:"green"}

color_to_year = {v:k for k,v in year_to_color.items()}

color_de = {"blue":"blau","white":"weiss","yellow":"gelb","red":"rot","green":"gruen"}
color_de_rev = {v:k for k,v in color_de.items()}


color_enc = {"DE":color_de}
color_enc_rev = {"DE":color_de_rev}
