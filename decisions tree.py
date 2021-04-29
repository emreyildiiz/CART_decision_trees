import csv #csv dosyalarını okumak için gerekli modül
import subprocess #pdf hata yakalamak için gerekli modül
from graphviz import Digraph #grafik çizdirmek için gerekli modül
global dot
global sutunIsimleri #sütun isimleri
sutunIsimleri = []
#%%grafik kullanmak içni gerekli kodlar
dot = Digraph(comment = "Agac Grafiği")
styles = {
    'yaprak' : {'shape': 'rect','style':'filled','color' : 'lightblue'},
    'node' : {'shape': 'ellipse','style':'filled'},
    'sonuclar': {'shape': 'rect','style':'filled','color' : 'gray'}
    }
#%%kullanılan fonksiyonlar
def oku(okunacak_dosya,dizi):  ## okuma fonksiyonu
    try: 
        with open(okunacak_dosya) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter = ',')
            for row in csv_reader:
                dizi.append(row)
            print("{} Dosyası okundu.".format(okunacak_dosya))
    except FileNotFoundError:
        print("Dosya Bulunamadi")
def Kategoriler(dizi,sutun):#verilen dizi ve sutundaki değerleri eşsiz(unique) olarak döndürür
    kategoriler = []
    set1 = set()
    for i in range(1,len(dizi)):
        set1.add(dizi[i][sutun])
    for  i  in set1:##kümeyi diziye çeviriyoruz.
        kategoriler.append(i)
    return kategoriler
def sayisalDegerMi(deger):##deger sayisalsa true dondurur
    try:
        int(deger)
        float(deger)
        return True
    except ValueError:
        return False
class Soru:#soru classı
    def __init__(self,sutun,deger):
        self.sutun = sutun #sorunun sütun indexini tutar
        self.sutunadi = sutunIsimleri[sutun]#sorunun bulunduğu sütunun ismi 
        self.deger = deger #sorunun sütundaki hangi değer olduğunu tutar
        self.sorulacak = self.soruOlustur()
    def soruOlustur(self):#soru oluşturur
            return "Özellik : {} \n'{} mi ?'".format(self.sutunadi.capitalize(),self.deger.capitalize())
def class_sayisi(dizi): #class sütununun değerlerinin tüm satirlarda kaç adet olduğunu buluru dict döndürür
    class_sayisi = dict()
    for i in dizi:
        if i[-1] not in class_sayisi:
            class_sayisi[i[-1]] = 0
        class_sayisi[i[-1]] += 1
    return class_sayisi
def kucukSatirlariBul(dizi,sayi,sutun):#verilen sutunda sayi degiskeninden kucuk degiskenli satirlari bulur ve döndürür 
    kucukSatirlar = []
    for i in range(0,len(dizi)):
        if int(dizi[i][sutun]) <= sayi:
            kucukSatirlar.append(dizi[i])
    return kucukSatirlar
def buyukSatirlariBul(dizi,sayi,sutun):#verilen sutunda sayi degiskeninden buyuk degiskenli satirlari bulur ve döndürür 
    buyukSatirlar = []
    for i in range(0,len(dizi)):
        if int(dizi[i][sutun]) > sayi:
            buyukSatirlar.append(dizi[i])
    return buyukSatirlar
def boluneniYerlestir(dizi,sutun,bolunecek):#verilen dizide ve sayısal sutunda minimum giniyle o sutundaki elemanları iki kategoriye böler
    for i in range(len(dizi)):
        if(int(dizi[i][sutun])<=bolunecek):
            dizi[i][sutun] = " <={}".format(bolunecek)
        else:
            dizi[i][sutun] = " > {}".format(bolunecek)
def gini(dizi):
    gini = 1
    class_sayisii = class_sayisi(dizi)
    for i in class_sayisii:
        gini-= (class_sayisii[i]/len(dizi))**2
    return gini
def sayisalBol(dizi): #verilen dizideki sayısal sutunları bulup,minimum giniye sahip olan sayıyı hesaplar(gini index)
    #sayisal sutunların index nosunu ve minimum ginili sayıyı döndürür
    sayisallar = []
    buyuk_satirlar = []
    kucuk_satirlar = []
    gini_buyuk = 0
    gini_kucuk = 0
    gini_node = 0
    sayisal_sutunlar = []
    sutun_min_gini = []
    for i in range(0,len(dizi[0])):
        sayisallar = []
        if sayisalDegerMi(dizi[0][i]):
            sayisal_sutunlar.append(i)
            for j in range(0,len(dizi)):
                if int(dizi[j][i]) not in sayisallar:
                    sayisallar.append(int(dizi[j][i]))
            sayisallar.sort()
            buyuk_satirlar = buyukSatirlariBul(dizi,sayisallar[0],i)
            kucuk_satirlar = kucukSatirlariBul(dizi,sayisallar[0],i)
            gini_buyuk = 0
            gini_kucuk = 0
            if(len(buyuk_satirlar)!=0):
                gini_buyuk = gini(buyuk_satirlar)
            if(len(kucuk_satirlar)!=0):
                gini_kucuk = gini(kucuk_satirlar)
            gini_node = (len(buyuk_satirlar)/len(dizi)*gini_buyuk) + (len(kucuk_satirlar)/len(dizi)*gini_kucuk)
            minimumgini_node = gini_node
            minimumgini_nodelu_sayi  = sayisallar[0]
            for z in range(1,len(sayisallar)):
                buyuk_satirlar = buyukSatirlariBul(dizi,sayisallar[z],i)
                kucuk_satirlar = kucukSatirlariBul(dizi,sayisallar[z],i)
                if(len(buyuk_satirlar)!=0):
                    gini_buyuk = gini(buyuk_satirlar)
                if(len(kucuk_satirlar)!=0):
                    gini_kucuk = gini(kucuk_satirlar)
                gini_node = (len(buyuk_satirlar)/len(dizi)*gini_buyuk) + (len(kucuk_satirlar)/len(dizi)*gini_kucuk)
                if(gini_node < minimumgini_node):
                    minimumgini_node = gini_node
                    minimumgini_nodelu_sayi = sayisallar[z]
            sutun_min_gini.append(minimumgini_nodelu_sayi)
    return sayisal_sutunlar,sutun_min_gini
def kokBul(dizi):#en yüksek theta değerini bulur ve karar düğümü oluşturur
    eniyitheta = -5000
    eniyitheta_hangi_deger = 0
    eniyitheta_sutun = 0
    if(dizi):
        for i in range(0,len(dizi[0])-1):
            kategori = Kategoriler(dizi,i)
            if len(kategori) ==  1:
                continue
            theta,theta_hangi = sutun_best_theta(dizi,i,kategori)
            if theta > eniyitheta:
                eniyitheta=theta
                eniyitheta_hangi_deger=theta_hangi
                eniyitheta_sutun = i
        kategori = Kategoriler(dizi,eniyitheta_sutun)
        deger = kategori[eniyitheta_hangi_deger]
        soru = Soru(eniyitheta_sutun,deger)
        dogru_taraf = icerenKayitlar(dizi,eniyitheta_sutun,deger)
        yanlis_taraf = DigerKayitlar(dizi,eniyitheta_sutun,deger)
        ginii  = gini(dizi)
        dugum = karar_dugumu(soru,dogru_taraf,yanlis_taraf,ginii)
    return dugum
def safMI(dizi):#verilen bir dizinin saf olup olmadığını bulur
    kume = set()
    for i in dizi:
        for j in range(0,len(dizi[0])-1):
            kume.add(i[j])
    if(len(kume) == len(dizi[0])-1):
        return True
    else:
        return False
    
def icerenKayitlar(dizi,sutun,deger):#verilen dizide yine verilen değeri içeren satirlari bulur dizi döndürür
    iceren_Kayitlar = []
    for i in range(0,len(dizi)):
        if dizi[i][sutun] == deger:
            iceren_Kayitlar.append(dizi[i])
    return iceren_Kayitlar
def DigerKayitlar(dizi,sutun,deger):#içermeyenleri bulur
    diger_kayitlar = []
    for i in range(0,len(dizi)):
        if dizi[i][sutun] != deger:
            diger_kayitlar.append(dizi[i])
    return diger_kayitlar
def sutun_best_theta(dizi,sutun,kategori):#verilen sütun ve dizideki en iyi theta değerine sahip sütunu bulur
    theta_degerleri = []
    for i in kategori:
        iceren_Kayitlar = icerenKayitlar(dizi,sutun,i)
        diger_kayitlar = DigerKayitlar(dizi,sutun,i)
        class_sayisi_iceren = class_sayisi(iceren_Kayitlar)
        class_sayisi_diger = class_sayisi(diger_kayitlar)
        PL = len(iceren_Kayitlar)/len(dizi)
        PR = len(diger_kayitlar)/len(dizi)
        Q = 0
        for k in class_sayisi_iceren:
            if k in class_sayisi_diger:
                Q += abs((class_sayisi_iceren[k]/len(iceren_Kayitlar)) - (class_sayisi_diger[k]/len(diger_kayitlar)))

        theta_degerleri.append(2*PL*PR*Q)
    return max(theta_degerleri),theta_degerleri.index(max(theta_degerleri))
def pureClassmi(dizi):#dizide class sütunundaki tüm değerler good veya bad ise true döndürür. 
    a = dizi[0][-1]
    for i in dizi:
        if a != i[-1]:
            return False
    return True
#%%
class leaf: # yaprak class dizi gini ve o yaprağın etiketini tutar etiket class sütununda sayica en fazla olan değişkendir
    def __init__(self,dizi,ginii):
        self.dizi = dizi
        self.gini = ginii
        self.etiket = self.etiketHesapla()
    def etiketHesapla(self):
        class_sayilari = class_sayisi(self.dizi)
        sayilar = list(class_sayilari.values())
        keyler = list(class_sayilari.keys())
        return keyler[sayilar.index(max(sayilar))]

#%%
class karar_dugumu:#karar düğümü 
    def __init__(self,soru,sol,sag,ginii,label="kok"): ## soru true ise sola yanlis ise saga dallanır
        self.soru = soru
        self.sagdizi = sag #düğümün sağ dalındaki dizi
        self.soldizi = sol #düğümün sol dalındaki dizi
        self.right = None
        self.left = None
        self.gini = 0.0
        self.ginisoldizi = None
        self.ginisagdizi = None
        self.label = label #grafik çizdirmek için kullanılan etiket
    def agacOlustur(self):#rekürsif ağaç oluşturma kodu
        self.ginisoldizi = gini(self.soldizi)
        self.ginisagdizi = gini(self.sagdizi)
        self.classno = class_sayisi(self.soldizi)
        self.classno2 = class_sayisi(self.sagdizi)
        if self.soldizi:#dizinin tüm değerleri aynıysa,tüm class değerleri aynıysa,belirlenen sayidan düşük dizi eleman sayisi varsa,gini değerleri sürekli kendini tekrar ediyorsa,gini değerlerine göre herhangi bir kazanım söz konusu değilse durur
            if not safMI(self.soldizi) and  not pureClassmi(self.soldizi) and len(self.soldizi)>belirlenensayi and self.gini!=self.ginisoldizi: ## parantez içi(isteğe bağlı)pre pruning işlemi sol dizinin ginisi karar düğümünün ginisinden küçükse orada dur
                leftkok  = kokBul(self.soldizi)
                self.left = leftkok
                self.left.gini = self.ginisoldizi
                if(len(leftkok.sagdizi)+len(leftkok.soldizi)<belirlenensayi):
                    self.left = leaf(self.sagdizi+self.soldizi,gini(self.sagdizi+self.soldizi))
                    dot.node(self.label+"solayaprak",self.left.etiket,styles['yaprak'])
                    dot.edge(self.label,self.label+"solayaprak","True",fontcolor='forestgreen')

                else:
                    dot.node(self.label+"sola",self.left.soru.soruOlustur())
                    dot.edge(self.label,self.label+"sola","True",fontcolor='forestgreen')
                    labell = self.label+"sola"
                    self.left.label =  labell
                    self.left.agacOlustur()
                    
              
            else:
                self.left = leaf(self.soldizi,self.ginisoldizi)
                dot.node(self.label+"yaprak",self.left.etiket+"\n"+str(class_sayisi(self.left.dizi)),styles['yaprak'])
                if isinstance(self.right,leaf):
                   if(self.left.etiket == self.right.etiket):
                       dot.edge(self.label,self.label+"yaprak","True",fontcolor='forestgreen')
                   else:
                       dot.edge(self.label,self.label+"yaprak",fontcolor='forestgreen')
                else:
                    dot.edge(self.label,self.label+"yaprak","True",fontcolor='forestgreen')
                
        if self.sagdizi:
            if  not safMI(self.sagdizi) and not pureClassmi(self.sagdizi) and len(self.sagdizi)>belirlenensayi and self.gini!=self.ginisagdizi:## parantez içi (isteğe bağlı)preprununing sağ dizinin ginisi karar düğümünün ginisinden küçükse orada dur
                rightkok = kokBul(self.sagdizi)
                self.right = rightkok
                self.right.gini = self.ginisagdizi
                if(len(rightkok.sagdizi)+len(rightkok.soldizi)<belirlenensayi):
                    self.right = leaf(self.sagdizi+self.soldizi,gini(self.sagdizi+self.soldizi))
                    dot.node(self.label+"sagayaprak",self.right.etiket)
                    dot.edge(self.label,self.label+"sagayaprak","False",fontcolor='red')
                    
                else:
                    dot.node(self.label+"saga",self.right.soru.soruOlustur())
                    dot.edge(self.label,self.label+"saga","False",fontcolor='red')
                    labell = self.label+"saga"
                    self.right.label = labell
                    self.right.agacOlustur()
            else:
                self.right = leaf(self.sagdizi,self.ginisagdizi)
                if isinstance(self.left,leaf):
                    if(self.left.etiket != self.right.etiket):
                        dot.node(self.label+"sagaayaprak",str(self.right.etiket)+"\n"+str(class_sayisi(self.right.dizi)),styles['yaprak'])
                        dot.edge(self.label,self.label+"sagaayaprak","False",fontcolor='red')
                    else:
                        dot.node(self.label+"yaprak",self.right.etiket+"\n"+str(class_sayisi(self.left.dizi+self.right.dizi)),styles['yaprak'])
                        dot.edge(self.label,self.label+"yaprak"," and False",color ='white',fontcolor='red')
#%%test fonksiyonu
def testEt(kokk,dizi):#testDatayı ağaca uyarlar sonuçları bulur
    dogru = 0
    yanlis = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for i in dizi:
        kok = kokk
        while(not isinstance(kok,leaf)):
            if isinstance(kok,karar_dugumu):
                if kok.soru.deger != i[kok.soru.sutun] and (isinstance(kok.right,karar_dugumu) or isinstance(kok.right,leaf)):
                    kok = kok.right
                elif kok.soru.deger == i[kok.soru.sutun] and (isinstance(kok.left,karar_dugumu) or isinstance(kok.left,leaf)):
                    kok = kok.left
                else:
                    break
        if(isinstance(kok,leaf)):
            if(kok.etiket == i[-1] == "good"):
                dogru += 1
                true_positive+=1
            elif kok.etiket == i[-1]== "bad":
                dogru+=1
                true_negative+=1
            elif kok.etiket == "good" and i[-1]=="bad":
                false_positive+=1
                yanlis+=1
            else:
                false_negative+=1
                yanlis+= 1
    true_positive_rate = true_positive/(true_positive+false_negative)
    true_negative_rate = true_negative/(false_positive + true_negative)
    false_positive_rate = false_positive/(false_positive + true_negative)
    false_negative_rate = false_negative/(true_positive + false_negative)
    accuracy = (true_positive + true_negative)/(true_positive+true_negative+false_positive+false_negative)
    yazdirilacak = []
    yazdirilacak = "Test Sonucu: \n" +"Veri Sayısı : {}\n".format(len(dizi))+"Doğru Tahmin Sayısı:{}\n".format(dogru) + "Yanlış Tahmin Sayısı:{}\n\n".format(yanlis)+"Accuracy : {}\n".format(accuracy) + "True Positive Rate : {}\n".format(true_positive_rate)
    yazdirilacak += "True Negative Rate : {}\n".format(true_negative_rate) + "False Positive Rate : {}\n".format(false_positive_rate) +"False Negative Rate : {}\n".format(false_negative_rate) + "True Positive Adedi:{}\n".format(true_positive) + "True Negative Adedi: {}\n".format(true_negative)
    print(yazdirilacak)
    return yazdirilacak
            
#%% main kısmı
trainDizisi = []
testDizisi  = []
oku("trainSet.csv",trainDizisi)

for i in range(0,len(trainDizisi[0])):
    sutunIsimleri.append(trainDizisi[0][i])
trainDizisi.pop(0)##Sutun isimlerini cikartiyoruz
sayisal_sutunlar,sutun_min_ginili_sayi = sayisalBol(trainDizisi)
for i in range(0,len(sayisal_sutunlar)):
    boluneniYerlestir(trainDizisi,sayisal_sutunlar[i],sutun_min_ginili_sayi[i])
oku("testSet.csv",testDizisi)
testDizisi.pop(0)##Sutun isimlerini cikartiyoruz
for i in range(0,len(sayisal_sutunlar)):
    boluneniYerlestir(testDizisi,sayisal_sutunlar[i],sutun_min_ginili_sayi[i])
print("DIKKAT!!!'PROGRAMI CALISTIRMADAN ONCE OKUYUN.txt'yi OKUYUN!!!")
print("Eğer bilgisayarınızda Graphviz kurulu değilse program çizim yapmayacaktir")
p = input("Devam etmek için ENTER basiniz.")
while(True):
    belirlenensayi  = int(input("Agacı Durdurmak için maximum yaprak eleman sayisi girin(Daha yüksek sayili yapraklar ortaya çıkabilir,bu diğer durdurma kurallarına da bağlıdır.(kayıt saflığı,class saflığı))\nCikmak icin (-1) girin.\nMaximum Yaprak Eleman Sayisi:"))
    if belirlenensayi == -1:
        break
    print("\n")
    kok = None
    dot = Digraph(comment = "DecisionTree")
    kok  =  kokBul(trainDizisi)#kök bulunuyor
    kok.agacOlustur()#ağaç oluşturuluyor.
    label = "kok"
    kok.gini  = gini(kok.sagdizi+kok.soldizi)
    dot.node(label,kok.soru.soruOlustur())
    yazdirilacak = testEt(kok,testDizisi)
    dot.node("sonuclar",yazdirilacak,styles['sonuclar'])
    try:
        dot.render('Sonuclar/DecisionTree.gv',view = True)
    except subprocess.CalledProcessError:
        print("Grafik,eski pdf açık olduğu için renderlanamıyor.")
        print("Mevcut açılmış pdfi kapatın")
        p = input("Kapattiysaniz Enter'a basin")
        continue
    print("Ağaç grafiği Sonuclar klasöründe DecisionTree.pdf ine kaydedildi...")








