# CardGame904
Used to host a server that plays the card game 904. Contains functions that are to be called from a web page.

April 7, 2020 - Created the repo. Decided to write the 904 backend using Python + Flask.
              - Hello world + Some basic skeletal classes

April 8, 2020 - Fixed the functions, created proper JSON response for 'newgame'. Verified from front-end. 
April 9, 2020 - Added some more fields to JSON with a bunch of new DataModel classes. Added dummy method 'alter_move'
April 12, 2020 - Coded 'alter_move'. Doing a premature check-in (without testing/verifying) for Krithika
                to look into the CORS issue.
                
Krithika subsequently fixed the CORS issue. She also added session state retaining capability with which
game state history was stored. This is a vital block of the 'undo' feature implemented.

April 27 - Added beliefs - Initial common prior, belief after dealing cards, granular methods on probability change
        on observing presence or absence of a card with some player.

April 28 - The CORS issue seems to resurface. Unable to root-cause. Also, there is another issue of response header
            being too large in the browser when belief increases.
            Thus, idea of having session variables is dropped, and worked around by usage of global variables.
            There's a known issue where when there are more than 1 clients playing the game, history/belief shall get
            mixed up.
            
May 2 - Evolution of beliefs is solidified. Works well for significant cards. 
        Create separate branch for trying out Pandas Dataframes.
        
May 6 - Dataframes is good. Some parallelization is possible. No more signifincant-cards stuff. All 24C8 combinations.        

May 12 - To get pip dependencies into requirements.txt venv/bin/python3.7 -m pip freeze --local > requirements.txt
Install webserver GUnicorn with  venv/bin/python3.7 -m pip install gunicorn

May 13 - The newgame() times out from the Heroku server side. New branch precompute_beliefs is created to address it.
Did some excellent optimizations that I'm proud of ! Checking in on May 16th.
-> Precomputed intial prior belief.
-> Parallelized execution. Using pool.map()
-> Vectorized the dataframe operations. 
-> Use masks to compute membership with bitwise operations. Avoids list to string conversions and membership tests.

TODO - immediate future :
1. Check None CardSet exception.    FIXED
2. Optimize the card removal, card id checker from CardSet in card_prob_change() DONE on May 15!!!
3. Check with front-end DONE
4. Belief change upon revealing trump. FIXED
5. Ux displayable belief code needs to be updated. DONE
6. Bad prob change exception - When trump is played.        
 
TODO - May 15
1. Not has suite. Repeating 'not has card' is costly.
2. if someone declines ask trump option, recalculate flag for next player.
3. 'surely has' cards are appearing in dist
 
KNOWN HOLES :
1. After bidding, change in belief in nature_hands doesn't reflect into nature_cards.
2. Common knowledge doesn't have nature hands, only has nature_cards.
3. Play a move feature is not started.
4. Change in belief isn't propogating beyond first person.
        
Useful links:

https://stackoverflow.com/questions/10791588/getting-container-parent-object-from-within-python


placing bid
INFO:werkzeug:192.168.1.7 - - [15/May/2020 16:46:48] "OPTIONS /move HTTP/1.1" 200 -
INFO:root:Gamestate decoded from json. Time elapsed = 0.07103038800005379
INFO:root:Re-attached beliefs from session. Time elapsed = 16.617185670000026
INFO:root:Altered state. Time elapsed = 0.00014805699993303278
INFO:root:Trimmed beliefs, saved original to session.. Time elapsed = 30.819700812000065
INFO:root:Converted to JSON for return to client. Added to history. Time elapsed = 0.04631918899997345

make trump
INFO:root:Gamestate decoded from json. Time elapsed = 0.06890473799990104
INFO:root:Re-attached beliefs from session. Time elapsed = 14.54032182900005
INFO:root:Altered state. Time elapsed = 0.00015991300006135134
INFO:root:Trimmed beliefs, saved original to session.. Time elapsed = 27.808362894000084
INFO:root:Converted to JSON for return to client. Added to history. Time elapsed = 0.04732635300001675

new game
NFO:werkzeug:192.168.1.7 - - [15/May/2020 16:04:48] "OPTIONS /newgame HTTP/1.1" 200 -
INFO:root:Reset history/beliefs. Time elapsed = 6.295000048339716e-06
INFO:root:Created GameState object. Time elapsed = 0.5260455559999855
INFO:root:Trimmed beliefs, saved original. Time elapsed = 22.861118328999964
INFO:root:Converted to JSON for return to client. Added to history. Time elapsed = 0.044598798999913924

new game (without detach/attach of beliefs)
INFO:werkzeug:192.168.1.7 - - [15/May/2020 18:05:00] "OPTIONS /newgame HTTP/1.1" 200 -
INFO:root:Reset history/beliefs. Time elapsed = 1.372000000010587e-05
INFO:root:Created GameState object. Time elapsed = 8.600943954
INFO:root:Saved GameState object to history. Time elapsed = 0.17600627400000235
INFO:root:Trimmed belief. Converted to JSON for return to client. Time elapsed = 0.48825644300000093

placing bid - new
INFO:werkzeug:192.168.1.7 - - [15/May/2020 18:08:38] "POST /move HTTP/1.1" 200 -
INFO:root:Gamestate decoded from json. Time elapsed = 0.06376589699999613
INFO:root:Get GameState from history and put in move. Time elapsed = 4.919999980756984e-06
INFO:root:Altered state. Time elapsed = 0.00020638899999880778
INFO:root:Saved GameState object to history. Time elapsed = 0.14451096899998106
INFO:root:Trimmed belief. Converted to JSON for return to client. Time elapsed = 0.49823205499998835

placing final bid - new
INFO:werkzeug:192.168.1.7 - - [15/May/2020 18:08:47] "POST /move HTTP/1.1" 200 -
INFO:root:Gamestate decoded from json. Time elapsed = 0.053268522999985635
INFO:root:Get GameState from history and put in move. Time elapsed = 2.967000000353437e-06
INFO:root:Altered state. Time elapsed = 2.7832180940000057
INFO:root:Saved GameState object to history. Time elapsed = 0.16606324400001427
INFO:root:Trimmed belief. Converted to JSON for return to client. Time elapsed = 0.43142237899999714