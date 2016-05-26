import urllib2
import json

def advice(temp_c):

#### GIVES ADVICE BASED ON CURRENT TEMPERATURE    

    f = urllib2.urlopen('http://api.wunderground.com/api/YOUR API KEY/geolookup/conditions/q/UK/Glasgow.json')
    json_string = f.read()
    f.close()

    parsed_json = json.loads(json_string)

    temp_c = parsed_json['current_observation']['temp_c']
  
 #   temp = temp_c  
    if temp_c >= 15:
        return "T-Shirt Weather!"
    elif temp_c <= 14:
        return "Best stick a jumper on!"


def lambda_handler(event, context):

#### GETS CURRENT WEATHER INFORMATION FROM WEATHER UNDERGROUND

    f = urllib2.urlopen('http://api.wunderground.com/api/YOUR API KEY/geolookup/conditions/q/UK/Glasgow.json')
    json_string = f.read()
    f.close()

    parsed_json = json.loads(json_string)

    location = parsed_json['location']['city']
    temp_c = parsed_json['current_observation']['temp_c']
    feelslike_c = parsed_json['current_observation']['feelslike_c']
    forecast = parsed_json['current_observation']['forecast_url']

 #### CONNECTS TO PUSHOVER TO SEND CURRENT WEATHER AND ADVICE

    import httplib, urllib

    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": "YOUR TOKEN", # ENTER YOUR TOKEN FROM PUSHOVER
        "user": "YOUR USER", # ENTER YOUR USER FROM PUSHOVER
        "message": "Currently the temperature in %s is: %s C, it feels like: %s C.\n\n%s.\n\nView the full forecast %s" % (location, temp_c, feelslike_c, advice(temp_c), forecast),
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()