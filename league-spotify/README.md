Displays the currently playing spotify song as a status message in the league client's status bar.
It also downsamples the song's cover image into a 16x8 (i know it's horrible) and using full-width hash characters to draw the pixel.
It works! (if you can say a 16x8 pixel image is working).
I found it to look better without the art so I just removed it.

Just need to run the auth.py, log in on the hosted ip. and it will redirect to spotify's authentication page. It returns the access token or whatever and I run queries every 10 seconds to check if the song changed. (doesn't seem like there's a callback for the api. that's good since having a listener would be annoying to program)
Also refer to the other league status related scripts I wrote for some more info.
