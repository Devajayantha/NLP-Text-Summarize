from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter

from paice import *

defaultrules = """
ai*2.     { -ia > -   if intact }
a*1.      { -a > -    if intact }
bb1.      { -bb > -b   }
city3s.   { -ytic > -ys }
ci2>      { -ic > -    }
cn1t>     { -nc > -nt  }
dd1.      { -dd > -d   }
dei3y>    { -ied > -y  }
deec2ss.  { -ceed > -cess }
dee1.     { -eed > -ee }
de2>      { -ed > -    }
dooh4>    { -hood > -  }
e1>       { -e > -     }
feil1v.   { -lief > -liev }
fi2>      { -if > -    }
gni3>     { -ing > -   }
gai3y.    { -iag > -y  }
ga2>      { -ag > -    }
gg1.      { -gg > -g   }
ht*2.     { -th > -   if intact }
hsiug5ct. { -guish > -ct }
hsi3>     { -ish > -   }
i*1.      { -i > -    if intact }
i1y>      { -i > -y    }
ji1d.     { -ij > -id   --  see nois4j> & vis3j> }
juf1s.    { -fuj > -fus }
ju1d.     { -uj > -ud  }
jo1d.     { -oj > -od  }
jeh1r.    { -hej > -her }
jrev1t.   { -verj > -vert }
jsim2t.   { -misj > -mit }
jn1d.     { -nj > -nd  }
j1s.      { -j > -s    }
lbaifi6.  { -ifiabl > - }
lbai4y.   { -iabl > -y }
lba3>     { -abl > -   }
lbi3.     { -ibl > -   }
lib2l>    { -bil > -bl }
lc1.      { -cl > c    }
lufi4y.   { -iful > -y }
luf3>     { -ful > -   }
lu2.      { -ul > -    }
lai3>     { -ial > -   }
lau3>     { -ual > -   }
la2>      { -al > -    }
ll1.      { -ll > -l   }
mui3.     { -ium > -   }
mu*2.     { -um > -   if intact }
msi3>     { -ism > -   }
mm1.      { -mm > -m   }
nois4j>   { -sion > -j }
noix4ct.  { -xion > -ct }
noi3>     { -ion > -   }
nai3>     { -ian > -   }
na2>      { -an > -    }
nee0.     { protect  -een }
ne2>      { -en > -    }
nn1.      { -nn > -n   }
pihs4>    { -ship > -  }
pp1.      { -pp > -p   }
re2>      { -er > -    }
rae0.     { protect  -ear }
ra2.      { -ar > -    }
ro2>      { -or > -    }
ru2>      { -ur > -    }
rr1.      { -rr > -r   }
rt1>      { -tr > -t   }
rei3y>    { -ier > -y  }
sei3y>    { -ies > -y  }
sis2.     { -sis > -s  }
si2>      { -is > -    }
ssen4>    { -ness > -  }
ss0.      { protect  -ss }
suo3>     { -ous > -   }
su*2.     { -us > -   if intact }
s*1>      { -s > -    if intact }
s0.       { -s > -s    }
tacilp4y. { -plicat > -ply }
ta2>      { -at > -    }
tnem4>    { -ment > -  }
tne3>     { -ent > -   }
tna3>     { -ant > -   }
tpir2b.   { -ript > -rib }
tpro2b.   { -orpt > -orb }
tcud1.    { -duct > -duc }
tpmus2.   { -sumpt > -sum }
tpec2iv.  { -cept > -ceiv }
tulo2v.   { -olut > -olv }
tsis0.    { protect  -sist }
tsi3>     { -ist > -   }
tt1.      { -tt > -t   }
uqi3.     { -iqu > -   } 
ugo1.     { -ogu > -og }
vis3j>    { -siv > -j  }
vie0.     { protect  -eiv }
vi2>      { -iv > -    }
ylb1>     { -bly > -bl }
yli3y>    { -ily > -y  }
ylp0.     { protect  -ply }
yl2>      { -ly > -    }
ygo1.     { -ogy > -og }
yhp1.     { -phy > -ph }
ymo1.     { -omy > -om }
ypo1.     { -opy > -op }
yti3>     { -ity > -   }
yte3>     { -ety > -   }
ytl2.     { -lty > -l  }
yrtsi5.   { -istry > - }
yra3>     { -ary > -   }
yro3>     { -ory > -   }
yfi3.     { -ify > -   }
ycn2t>    { -ncy > -nt }
yca3>     { -acy > -   }
zi2>      { -iz > -    }
zy1s.     { -yz > -ys  }
"""


tfidf_all = []
bobot_all = []
kesimpulan_all = []
kalimat_rank_all = []
no_all = []
no_sort = []
bobot_baru = []
array_baru_tfidf = []


class corpus :
    def openText(self, path):
        self.ds = open(path, 'r')
        text = self.ds.read()
        return text
    def tokenisasi(self, txt):
        hasil_token = word_tokenize(txt)
        tandaBaca = [',', '.', ':', ';', '(', ')']
        hasilKata = []
        for new in hasil_token:
            if new not in tandaBaca:
                hasilKata.append(new.lower())
        return hasilKata
    def stopwords(self, stp):
        # \w semua huruf, digit, dan karakter underscore
        # mencocokan satu atau beberapa kali pola
        #metode findall() mengembalikan list yang berupa string yang cocok dengan regex
        tokens = re.findall('\w+', str(stp))
        cek_stopword = set(stopwords.words('english'))
        words = []
        for txt in tokens:
            if txt not in cek_stopword:
                words.append(txt)
        return words

    def frekuensi(self, fre):
        # most_common menampilkan daftar elemen paling umum dan jumlah yang paling umum hingga paling sedikit.
        # jika () none maka menampilkan daftar semua jumlah elemen.
        frequency = {}
        kalimat =[]
        tokens = re.findall('\w+', str(fre))
        for word in tokens:
            # print(frequency)
            count = frequency.get(word, 0)
            frequency[word] = count + 1


        frequency_list = frequency.keys()
        # print("word",frequency_list)

        for words in frequency_list:
            # print (words, frequency[words])
            kalimat.append(words)
            kalimat.append(frequency[words])
        return(kalimat)

    def typedata(self,tpd):
        tokens = re.findall('\w+', str(tpd))
        frekuensi = {}
        type = []
        for word in tokens:
            count = frekuensi.get(word, 0)
            # print(count)
            frekuensi[word] = count + 1
        frequency_list = frekuensi.keys()

        for word in frequency_list:
            type.append(word)

        # print(frequency_list)
        return(type)

    def stemming(self, stm):
        tokens = re.findall('\w+', str(stm))
        # stem = LancasterStemmer()
        stem = PaiceHuskStemmer(defaultrules)
        hasil = []
        for steming in tokens:
            hasil.append(stem.stem(steming))
        # str1 = ', '.join(hasil)
        # str 1 convert list to string
        # print(str1)
        return(hasil)

    def computeIDF(self, docList):
        import math
        idfDict = []
        N = len(docList)
        # print("N itu apa : ", N)
        idfDict = dict.fromkeys(docList[0].keys(), 0)
        # print("apa isinya : ", idfDict)
        for doc in docList:
            for word, val in doc.items():
                if val > 0:
                    idfDict[word] += 1
        # print("---------------------TF-IDF---------------------")
        for word, val in idfDict.items():
            # print("Kata : ",word ,"Nilai",val)
            # idfDict[word] = math.log10(N / float(val))
            if float(val) != 0:
                idfDict[word] = math.log10(N / float(val))
            else:
                idfDict[word] = 0
            # print( word,":",idfDict[word])
        # print(len(docList))
        return idfDict

    # def summarizer(self, vtm):
    #     text_paragraph = vtm.splitlines()
    #     count_paragraf = len(text_paragraph)
    #
    #     paragraph = []
    #
    #     for x in range(0, count_paragraf):
    #         paragraph.append([x, text_paragraph[x].split('. ')])
    #     # print(paragraph)
    #     count_paragraph=len(paragraph)
    #
    #     # looping didalam paragraf
    #     for i in range(0, count_paragraph):
    #         array_kalimat = []
    #         count_text_paragraph = len(paragraph[i][1])
    #         print("")
    #         print("---------------------------")
    #         print("PARAGRAF KE- %d" % (i + 1))
    #         print("---------------------------")
    #         teks = ''
    #         for xz in range(0, count_text_paragraph):
    #             teks = teks + paragraph[i][1][xz] + '. '
    #             # print("Paragraf : ",[x]+1)
    #         print("Teks Paragraf :",teks)
    #         token = self.tokenisasi(teks)
    #         stopwords = self.stopwords(token)
    #         stemming = self.stemming(stopwords)
    #
    #         wordDict = []
    #         kalimat_all = []
    #         bobot = []
    #         kesimpulan = []
    #
    #         #------------mencari IDf-------------------------
    #         for x in range(0, count_text_paragraph):
    #             wordDict.append(dict.fromkeys(stemming, 0))
    #             # print("DF : ",wordDict[x])
    #         #     for i in range(0, len(wordDict)):
    #         #         for word in doc[i]:
    #         for a in range(0, len(paragraph[i][1])):
    #             kalimat2 = self.tokenisasi(paragraph[i][1][a])
    #             kalimat1 = self.stopwords(kalimat2)
    #             kalimat = self.stemming(kalimat1)
    #             # print("Isi Kalimat :", kalimat)
    #             kalimat_all.append(paragraph[i][1][a])
    #             for kata in kalimat:
    #                 wordDict[a][kata] += 1
    #             print("Kalimat : %d" % (a+1), wordDict[a])
    #             # print(len(wordDict))
    #         idfs = self.computeIDF(wordDict)
    #         print("ISI IDF",idfs)
    #
    #         for y in range(0, count_text_paragraph):
    #             # array_kalimat.append(paragraph[i][1][y]+'')
    #             word_token = self.tokenisasi(paragraph[i][1][y] + '')
    #             stpword = self.stopwords(word_token)
    #             stming = self.stemming(stpword)
    #             array_kalimat.append(stming)
    #         print("Array Kalimat : ", array_kalimat)
    #
    #         print("----------------------------------------TF-IDF----------------------------------------------------")
    #         tfidf = []
    #         val = 0
    #         for lp in range(0, count_text_paragraph):
    #
    #             val = 0
    #             # for xy in array_kalimat[lp]:
    #             for word in array_kalimat[lp]:
    #                 a = wordDict[lp][word] * idfs[word]
    #                 val += a
    #                 # print(a)
    #             # print("Word :", array_kalimat[lp])
    #             tfidf.append(val)
    #             hasil_tfidf = tfidf
    #             print("Kalimat %d" % (lp + 1), array_kalimat[lp],". Nilai Bobot :",tfidf[lp])
    #
    #         print("----------------------------------------RANGKING--------------------------------------------------")
    #         for x in range(0, len(paragraph[i][1])):
    #             for y in range(x + 1, len(paragraph[i][1])):
    #                 if hasil_tfidf[x] < hasil_tfidf[y]:
    #                     sample = hasil_tfidf[x]
    #                     hasil_tfidf[x] = hasil_tfidf[y]
    #                     hasil_tfidf[y] = sample
    #                     sample_kalimat = kalimat_all[x]
    #                     kalimat_all[x] = kalimat_all[y]
    #                     kalimat_all[y] = sample_kalimat
    #
    #         limit_kesimpulan = len(paragraph[i][1]) / 2
    #         print(len(paragraph[i][1]))
    #         limit_kesimpulan = round(limit_kesimpulan)
    #         print("isi round",round(limit_kesimpulan))
    #         print("INT", int(float(limit_kesimpulan)))
    #         if limit_kesimpulan == 0:
    #             limit_kesimpulan = 1
    #
    #         for x in range(0, limit_kesimpulan):
    #             print(kalimat_all[x])
    #             kesimpulan.append(kalimat_all[x])
    #             bobot.append(hasil_tfidf[x])
    #             # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    #             # print("")
    #         bobot_all.append(bobot)
    #         kesimpulan_all.append(kesimpulan)
    #
    #     jml_paragraf = len(paragraph)
    #     for x in range(0, count_paragraf):
    #         print("")
    #         print("KESIMPULAN PARAGRAF %d" % (x + 1))
    #         print(kesimpulan_all[x])
    #         print(bobot_all[x])
    #         print("")
    #         print("##################################################################################################")
    #     return(kesimpulan_all,bobot_all)