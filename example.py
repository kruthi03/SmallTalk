#example.py

from search_bar import *

search_bar = search_bar('Paddle Tennis', allow_options = True) # the options output can be shown  
search_bar = search_bar('Paddle Tennis', allow_options = False) 



from recommendation import *

recommendation = generate_recommendation('home office', prompt_version='v01')


from trending import *

trending = generate_trending('Trump')

from update_me import *

update_me = generate_update_element('Trump')