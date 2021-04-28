from pygame import mixer

mixer.init()
mixer.music.load('/home/pi/EOG/beep.mp3')
mixer.music.play()
