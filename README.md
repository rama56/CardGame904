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

TODO - immediate future :
1. Check None CardSet exception.    FIXED
2. Optimize the card removal, card id checker from CardSet in card_prob_change()
3. Check with front-end DONE
4. Belief change upon revealing trump. FIXED
5. Ux displayable belief code needs to be updated. DONE
6. Bad prob change exception - When trump is played.        
 
KNOWN HOLES :
1. After bidding, change in belief in nature_hands doesn't reflect into nature_cards.
2. Common knowledge doesn't have nature hands, only has nature_cards.
3. Play a move feature is not started.
4. Change in belief isn't propogating beyond first person.
        
Useful links:

https://stackoverflow.com/questions/10791588/getting-container-parent-object-from-within-python