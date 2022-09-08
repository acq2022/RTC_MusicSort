# RTC_MusicSort
Sorting music project

I needed to sort all my music. But it was such a mess and all my music folders together were so big it would be a pain in the *** to do it manually. So I looked for tools to do it and I found some really good programs that could do the job (like Mp3tag or Foobar200 for examples)... But there was one thing where these programs failed - according to what I understood - :

Let's figure we want the result to be like this 'Artist Name/Album Name/Tracks'. Now let's see the case a music folder which is a compilation (typicaly a soundtrack for example). If there are multiple artists - which defines what a compilation is - then the result gonna be one folder per artist, so multiple folders, inside of which there will be the same album name folder for each, inside which we gonna have the specific track from the artist for this album.

The specificity of RTC_MusicSort is to solve this problem. Not only does the program analyze each track separately, but it also analyzes the album from which this track comes and checks that there is indeed only one artist for this album. If not, RTC_MusicSort will move all tracks together inside a single album folder, inside a folder named 'VA' (for Various Artists).
