ffmpeg -y -i de-districts-Cases_Last_Week_Per_100000.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" de-districts-Cases_Last_Week_Per_100000.mp4

REM ffmpeg -y -f gif -i de-districts-Cases_Last_Week_Per_100000.gif -pix_fmt yuv420p -c:v libx264 -movflags +faststart -filter:v crop='floor(in_w/2)*2:floor(in_h/2)*2' de-districts-Cases_Last_Week_Per_100000.mp4
