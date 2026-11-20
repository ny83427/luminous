# Trailer

Adapted from the Chinese edition's `jing/工具/预告片/`. Same scenes and score; English captions.

    cd tools/trailer
    python3 trailer.py            # renders out/s0.mp4 … s7.mp4
    python3 sound.py              # writes out/sound.wav
    cd out && for i in 0 1 2 3 4 5 6 7; do echo "file 's$i.mp4'"; done > list.txt
    ffmpeg -y -f concat -safe 0 -i list.txt -i sound.wav -c:v libx264 -preset veryfast \
      -b:v 7M -maxrate 9M -bufsize 14M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest \
      -movflags +faststart ../../../trailer/Luminous_trailer.mp4

Then embed the three-book mockup as the file's thumbnail (cover art):

    ffmpeg -i Luminous_trailer.mp4 -i ../cover/Mockup.jpg -map 0 -map 1 -c copy -c:v:1 mjpeg \
      -disposition:v:1 attached_pic -movflags +faststart out.mp4

`python3 trailer.py still 7@4.5` exports a single frame for checking. Needs Cardo (Google Fonts) and Noto Serif CJK.
