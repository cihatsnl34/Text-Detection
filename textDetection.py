from wand.image import Image as wi
from pytesseract import Output,pytesseract
import cv2

# pdf dosya uzantısı
pdf = wi(filename = "ur_mom.png",resolution = 300)

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# pdf to img
pdfImg = pdf.convert('jpg')
#pdf sayfa sayısı
pageCount = 1

for img in pdfImg.sequence:
    #Sayfaları tek tek alma işlemi
    page = wi(image = img)
    #Görüntüyü sırasıyla img olarak kaydet
    page.save(filename = "img"+str(pageCount)+".jpg")
    #resimlerin içindeki textleri kutular içine almak için cv2 ile img okuma işlemi
    img1 = cv2.imread("img"+str(pageCount)+".jpg")
    textArray = []
    #Görüntüden metne dönüştürmek için pytesseract kullanıyoruz
    text = pytesseract.image_to_string(img1, lang = "eng")
    #Okudumuz textleri textArray içine atma işlemi
    textArray.append((text))
    print(text)


    #Text1 text 2 oluşturan textFile metni oluşturma
    with open('text'+str(pageCount)+'.text','w') as filehandle:
        #dizide ki metni tek tek okuma
        for listitem in textArray:
            #metni dosyaya yazma
            filehandle.write('%s' % listitem)



    #her metin için kare
    #kordinatlarıyla metin almak için pytesseract kullanıyoruz
    d = pytesseract.image_to_data(img1,output_type=Output.DICT)
    n_boxes = len(d['level'])
    print(n_boxes)
    for i in range(n_boxes):
        #sol, üst, genişlik, yükseklik gibi her kelimenin koordinatlarını alın
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        print((x, y, w, h))
        #metini kapsayan kare oluşturma
        cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #show image with text detection
    cv2.imshow('res',img1)

    #save image
    cv2.imwrite("img"+str(pageCount)+".jpg",img1)

    cv2.waitKey(5000)
    #sayfa sayısı artırma
    pageCount += 1