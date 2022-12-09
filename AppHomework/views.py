from django.shortcuts import HttpResponse, Http404
from django.shortcuts import render
from urllib.request import urlopen
import json
from django.core.paginator import Paginator

# Create your views here.

response = urlopen("https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-languages.json")
data = json.loads(response.read())
id_country = len(data[0]["country"])
data_alphabet = {
		"A": "0",
		"B": "1",
		"C": "2",
		"D": "3",
		"E": "4",
		"F": "5",
		"G": "6",
		"H": "7",
		"I": "8",
		"J": "9",
		"K": "10",
		"L": "11",
		"M": "12",
		"N": "13",
		"O": "14",
		"P": "15",
		"Q": "16",
		"R": "17",
		"S": "18",
		"T": "19",
		"U": "20",
		"V": "21",
		"W": "22",
		"X": "23",
		"Y": "24",
		"Z": "25"
	}
for index in range(len(data)):
	data[index]["id"] = index
print(data)

id_countries_lang = {}

def indexPage(request):
	return render(request, 'index.html')

def listCoutriesPage(request):
	paginator = Paginator(data, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'list_countries.html', {'page_obj': page_obj, 'data': data, 'alphabet': data_alphabet})

def createPageCountries(request, id):
	text_lang = data[id]["languages"]
	formatted_text = ""
	for i in range(len(text_lang)):
		if i != len(text_lang) - 1:
			formatted_text += data[id]["languages"][i] + ", "
		else:
			formatted_text += data[id]["languages"][i]
	country_name = data[id]["country"]
	return render(request, 'list_language.html', {'text': formatted_text, 'country': country_name})
	#return HttpResponse(data[id]["languages"])

def list_symbol_countries(request, id):
	local_data = []
	output_countries = {}
	mykeys = [*data_alphabet]
	myvals = [*data_alphabet.values()] #list of values
	check = mykeys[id]
	for i in range(len(data)):
		local_data.append(data[i]["country"])
	for i in range(len(local_data)):
		if(local_data[i].lower()[0] == check.lower()):
			output_countries[local_data[i]] = i
	return render(request, 'list_countries_alpahet.html', {'data': output_countries, 'alphabet': data_alphabet})

def languageList(request):
	language_dict = {}
	array_languages = []
	for i in range(len(data)):
		array_languages.append(data[i]["languages"])
	array_languages = [a for b in array_languages for a in b]
	array_languages = set(array_languages)
	array_languages = list(array_languages)
	array_languages.sort()
	counter = 0
	for g in array_languages:
		id_countries_lang[counter] = []
		for i in data:
			lang_local = i['languages']
			_search = g
			if _search in lang_local:
				id_countries_lang[counter].append(i['country'])
		counter += 1
	return render(request, 'languages_all.html', {'text': array_languages, 'lang':id_countries_lang})

def get_lang_countries_id(request, id):
	return render(request, 'list_countries_lang.html', {'text': id_countries_lang[id]})