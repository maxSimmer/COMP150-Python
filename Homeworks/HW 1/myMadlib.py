#!/usr/bin/env python3
"""
String Substitution for a Mad Lib
Modified Code by Max Simmer
"""                                                  

storyFormat = """                                       
Once upon a time, deep in the forests of the {country}, lived a {creature}
like no other. This {creature} had {number} legs and was bigger than any other
{creature} in the area. One day a hunter arrived with a {weapon} and began
scouting the perimeter. As the hunter looked around, the {creature} watched
from a distance. warming up his {number} legs. Quickly the {creature} lept
forward, surprising the hunter. The hunter dashed for his {weapon}, and as the
creature saw this, it quickly scrambled. Sprinting away on its {number} legs,
the {creature} trips over a {object}, losing its balance and falling. As the
hunter approaches, the {creature} hears the sound of the {weapon}. The {creature}
tries to get back up but can't, stuck by this {object}, and panic sets in. As the
hunter walks up, the {creature} struggles to get away, but suddenly hears a snap.
The whole time the hunter with a {weapon} it was really a photographer with a camera. The {creature}
calmed down and gave a look of help. The photographer rescued the {creature} and got
it special care outside of {country}.

The End
"""                                                 

def tellStory():                                     
    userPicks = dict()                              
    addPick('country', userPicks)            
    addPick('creature', userPicks)            
    addPick('number', userPicks)
    addPick('weapon', userPicks)
    addPick('object', userPicks)
    story = storyFormat.format(**userPicks)
    print(story)
                                                    
def addPick(cue, dictionary):
    '''Prompt for a user response using the cue string,
    and place the cue-response pair in the dictionary.
    '''
    prompt = 'Enter an example for ' + cue + ': '
    response = input(prompt).strip() # 3.2 Windows bug fix
    dictionary[cue] = response                                                             

tellStory()                                         
input("Press Enter to end the program.")        
