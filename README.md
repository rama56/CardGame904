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