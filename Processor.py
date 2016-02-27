__author__ = 'armando'
import Image, PIL.ImageOps, pytesser, urllib, cStringIO
from ImageFilter import *


limiar = 90;
acceptedpixels = 0;
url = "http://buscatextual.cnpq.br/buscatextual/servlet/captcha?metodo=getImagemCaptcha";
fname = "captcha.png";
#file = "captcha2.png"
file = cStringIO.StringIO(urllib.urlopen(url).read())
imgList = list();
buf = list();

imgList.append(Image.open(file));
imgList.append(PIL.ImageOps.invert(imgList[0]));


img = imgList[1];
width, height = img.size;
imgList.append(Image.new("RGB",(width,height),"white"));
imgList.append(Image.new("RGB",(width,height),"white"));


negativePix = imgList[1].load();
whitePix = imgList[2].load();
sumPix = imgList[3].load();



#horizontal
for h in xrange(height):
    firstw = 0;
    for w in xrange(width):
        if(w <= 25 or w >=150):
            continue
        r,g,b =  negativePix[w,h];

        if(r <= limiar and g <= limiar and b <= limiar):
            if(firstw == 0):
                firstw = w;
                buf.append((w,h,negativePix[w,h]));
            if((w - firstw) >=1 ):
                buf.append((w,h,negativePix[w,h]));
                firstw = w;
            elif(len(buf) >= 5):
                for (wi,hi,pi) in buf:
                    whitePix[wi,hi] = pi;
                buf = list();
            else:
                buf = list();
        elif(len(buf) <= 1 and firstw != 0):
            buf = list();

#vertical
"""
for w in xrange(width):
    firsth = 0;
    for h in xrange(height):
        r,g,b =  negativePix[w,h];

        if(r <= limiar and g <= limiar and b <= limiar):
            if(firsth == 0):
                firsth = h;
                buf.append((w,h,negativePix[w,h]));
            if((h - firsth) >=1 ):
                buf.append((w,h,negativePix[w,h]));
                firsth = h;
            elif(len(buf) >= 5):
                for (wi,hi,pi) in buf:
                    whitePix[wi,hi] = pi;
                buf = list();
            else:
                buf = list();
        elif(len(buf) <= 1 and firsth != 0):
            buf = list()
"""

for h in xrange(height):
    firstw = 0;

    for w in xrange(width):
        r,g,b =  whitePix[w,h];
        tcounter = 0;

        for pw in xrange(-1,2):
            for ph in xrange(-1,2):

                if((w - pw) < 0 or (h - ph) < 0 or (w + pw) >= (width-2) or (h - ph) >= (height-2)):
                    break;
                tr,tg,tb = whitePix[w - pw,h - ph];
                if(tr <= limiar and tg <= limiar and tb <= limiar):
                    #whitePix[w - pw,h - ph] = (0,0,0);
                    tcounter+=1;
        if(tcounter <= 2):
            whitePix[w,h] = (255,255,255);

imgList[0].save('images/' + fname);
imgList[1].save('images/negative_' + fname);
imgList[2].save('images/white_' + fname);

text = pytesser.image_file_to_string('images/white_' + fname,graceful_errors=True)
print(text)