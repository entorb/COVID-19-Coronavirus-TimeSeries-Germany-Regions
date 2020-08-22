
# convert -delay 150x1000 maps/out/de-districts/Cases*2020-03*.svg -strip -coalesce -colors 256 -depth 8 -fuzz 2% +dither -layers Optimize maps/test-Cases03.gif
# convert -delay 150x1000 maps/out/de-districts/Cases*2020-04*.svg -strip -coalesce -colors 256 -depth 8 -fuzz 2% +dither -layers Optimize maps/test-Cases04.gif


# full layer images in first step
# convert maps/out/de-districts/Cases*2020-03*.svg -colors 256 -depth 8 -fuzz 2% +dither -layers coalesce maps/test-Cases03.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-04*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-04.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-05*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-05.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-06*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-06.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-07*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-07.gif
convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-08*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-08.gif

# -coalesce -fuzz 2% +dither -layers Optimize 
convert maps/test-Cases0*.gif -coalesce -fuzz 2% +dither -layers Optimize maps/de-districts-Cases_Last_Week_Per_Million.gif

# set delay for all frames
convert -delay 250x1000 maps/test-Cases34.gif maps/de-districts-Cases_Last_Week_Per_Million.gif

# clone last frame and set longer delay time of 1s
convert maps/de-districts-Cases_Last_Week_Per_Million.gif \( -clone -1 -set delay 100  \) maps/de-districts-Cases_Last_Week_Per_Million.gif

#convert', '-delay', '150x1000', '-size', '480x',}-*.svg', '-coalesce', '-fuzz', '2%', '+dither', '-resize', '480x', '-layers', 'Optimize', f'maps/de-districts-{property_to_plot}.gif']



convert', '-size', '480x', 'maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03*.svg', '-resize', '480x', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', 'maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03.gif