# s-utils
#### Video Demo:  <https://youtu.be/GGUGNtdRMwE>
#### Description:
This is a program designed to download videos from youtube in different qualities, it also has an image converter.
Downloaded videos will end up in 'download', downloaded playlists will end up in 'download/playlist'
In order to use the image converter, it's required to put the files you want to convert in the 'images' folder, converted images will end up in 'images/output'

If there is not supported file in images, and you select it, it will throw an error, if you provide an invalid url it will prompt you again

There's an alternative version(no difference ._.) that uses 'myClasses.py', if you use that, you only need to instantiate an object Main, and run the method run() but that version didn't have a valid format ;-;

This project uses pytube module to download videos and playlists from youtube and uses the PIL module to convert images to different file formats, i wanted to make a video converter but unfortunately all libraries that i found required ffmpeg to be installed in the computer, i first thought about using html/flask to make a gui but i've decided to use python only, simple_term_menu was used to make an interactive terminal menu

#### Dependencies:
pytube, simple-term-menu

test playlist (different video qualities)
https://www.youtube.com/playlist?list=PLrmcBf7sRnePTvv8WjuUc7Yzfrk_8OXDc
test video
https://www.youtube.com/watch?v=nJOMRf1HIe0
test images (download necessary)
https://placekitten.com/