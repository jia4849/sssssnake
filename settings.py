categories_dict = {
    "Difficulty" : {
        "Easy" : 6,
        "Normal" : 9,
        "Hard" : 12,
        "Extreme" : 15
    },
    "Sounds" : {
        "Track 1" : "wii.ogg",
        "Track 2" : "undertale.ogg",
        "Sound Effects" : None,
        "Off" : None
    }
}

categories_list = list(categories_dict.keys())
options_list = []
for x in categories_dict:
    for y in categories_dict[x]:
        options_list.append(y)

    
