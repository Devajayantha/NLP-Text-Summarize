import os
import re
import math

import wx

import noname
from nltk.corpus import stopwords

from stemming.lovins import stem

from nltk.tokenize import word_tokenize

from nltk import sent_tokenize


from collections import OrderedDict

stopwords = set(stopwords.words("english"))
non_stopwords = []
final_word = []


class MyEventHandler(noname.MyFrame1):

    def __init__(self, parent):
        noname.MyFrame1.__init__(self , parent)
        self.OpenFileBtn.Bind(wx.EVT_BUTTON , self.open_file)
        self.ProcessButton.Bind(wx.EVT_BUTTON , self.process_file)
        pass

    def open_file(self, event):

        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fobj:
                lines = fobj.readlines()
                self.CorpusText.Clear()
                for line in lines:

                    self.CorpusText.WriteText(line)

        pass

    def process_file(self,event):

        final_word={}
        rich_text = self.CorpusText.GetValue() # get text from input box
        rich_text = self.text_to_lowercase(rich_text)# lower case
        rich_text = re.sub("[(){}<>\",\-*0-9;']", " ", rich_text) #regex remove character
        sentences = self.get_paragraph(rich_text) # splitting paragraph
        tf = (self.get_word_size(sentences))#term freq
        df = self.get_df(tf)# get df freq
        tf_idf_val = self.tf_idf_3(df,tf)
        sum_tf = self.sum_tf_idf(tf_idf_val)
        bobot = self.bobot_kalimat(sentences,sum_tf)
        self.rank_kalimat(bobot)
        tokenized_word = word_tokenize(rich_text)
        tokenized_word = self.remove_stopwords(tokenized_word)
        ## tampilan di GUI
        final_word = self.stemming_word(tokenized_word)
        self.m_keterangan.Clear()
        self.m_tfidf.Clear()
        #self.hitung_frekuensi(tf)
        self.print_tf(tf)
        self.print_tf_idf(tf_idf_val)
        self.ResultTxt.Clear()
        # self.m_keterangan.Clear()
        self.print_result(final_word,bobot)

        pass

    def print_tf(self,tfArgs):
        for cnt_par,x in enumerate(tfArgs):
            self.m_keterangan.WriteText("paragraph "+str(cnt_par+1)+"\n")
            for a in x:
                self.m_keterangan.WriteText(str(a)+"\n\n")

    def print_tf_idf(self,tf_idf):
        for cnt_par, x in enumerate(tf_idf):
            self.m_tfidf.WriteText("paragraph " + str(cnt_par + 1) + "\n")
            for a in x:
                for b,val in a.items():

                    self.m_tfidf.WriteText(str(b)+" "+str(val) + "\n")

    def print_result(self,argsFinalWord,argsBobot):
        print(argsFinalWord)
        self.ResultTxt.WriteText("Hasil Stemming : \n")
        self.ResultTxt.WriteText(" ".join(str(word) for word in argsFinalWord))

        self.ResultTxt.WriteText("\nHasil Bobot Kalimat :\n")
        for cnt,x in enumerate(argsBobot):
            self.ResultTxt.WriteText("Paragraph"+str(cnt+1)+"\n")
            self.ResultTxt.WriteText(" ".join(str(d)+" : "+str(val)+"\n" for d,val in x.items()))
        #self.ResultTxt.WriteText(" ".join(str(word) for word in argsBobot))

        self.ResultTxt.WriteText("\nHasil Ringkasan :\n")
        for x in argsBobot:
            sorted_x = OrderedDict(reversed(sorted(x.items(), key=lambda t: t[1])))

            cnt = 0
            for key, value in sorted_x.items():
                if(cnt<1):
                    print(key, value)
                    self.ResultTxt.WriteText("\n"+str(key)+" : "+str(value) + "\n")
                cnt+=1


    def remove_stopwords(self,tokenize_param):
        val_non_stopword = []
        for w in tokenize_param:
            if w not in stopwords:
                val_non_stopword.append(w)
        return val_non_stopword


    def text_to_lowercase(self,text_param):
        val_result = text_param.lower()
        return val_result

    def stemming_word(self,args):
        stemming_val = []
        for w in args:
            if(len(w) > 4):
                stemming_result = stem(w)
                stemming_val.append(stemming_result)
            else:
                stemming_val.append(w)

        return stemming_val


    def hitung_frekuensi(self,data):

        frekuensi = {}
        enter = wx.TE_PROCESS_ENTER
        for word in data:
            count = frekuensi.get(word, 0)
            frekuensi[word] = count + 1

        frequency_list = frekuensi.keys()

        for words in frequency_list:
            #print(words + " : " + str(frekuensi[words]))
            self.m_keterangan.WriteText(words+" :"+str(frekuensi[words])+"\n")

        self.m_keterangan.WriteText("\nBanyak Kata: "+str(frequency_list.__len__())+"\n")
        self.m_keterangan.WriteText("Total Kata: " + str(data.__len__())+"\n")
        #print("banyak kata :" + str(frequency_list.__len__()))
        #print("total kata :" + str(data.__len__()))
        #print(frequency_list)


    def get_paragraph(self,txt):

        sentence =[]

        for line in txt.splitlines():
            #line = re.sub("[.]"," ",line)
            sentence.append(sent_tokenize(line))

        #clean_sentence = re.sub("[.]", "", sentence)
        #print(sentence[0][0])

        return sentence

    # Get Value for all text
    def get_word_size(self,txt):
        paragraph = []
        for i in txt: # get sentences from the lists of paragraph
            sentences = []
            for words in i: # get the words from the sentences
                words = re.sub("[.]","",words)
                word_text = word_tokenize(words)
                remove_stop_word = self.remove_stopwords(word_text)
                final_word = self.stemming_word(remove_stop_word)
                word_freq = {}
                for word in final_word:
                    count = word_freq.get(word, 0)
                    word_freq[word] = count + 1
                sentences.append(word_freq)
            paragraph.append(sentences)
        return paragraph


    def get_df(self,textArgs):
        df_paragraph = []
        for sens in textArgs:
            words = {}
            for i in sens:
                for x in i.keys():
                    cnt = words.get(x,0)
                    words[x] = cnt+1
            df_paragraph.append(words)
        return df_paragraph


    def count_tf_new(self,text):
        freq = {}
        for i in text:

            count = freq.get(i,0)
            freq[i] = count + 1

        return freq


    def count_tf(self,txt):
        freq ={}
        for word in txt.split():
            count = freq.get(word, 0)
            freq[word] = count + 1
        return freq


    def check_word(self,listWords):
        df ={}
        # f_list = listWords.keys()
        for f in listWords:
            for  dict_word in f:
                count  =  df.get(dict_word,0)
                df[dict_word] = count+1

        return df


    def tf_idf_3(self,dfArgs,tfArgs):
        tf_idf =[]
        i = 0
        for paragraph in tfArgs:
            sentences_val = []
            length_sens = len(paragraph)
            for sentences in paragraph:

                words_freq = {}
                for words in sentences:
                    #print(str(length_sens)+"/"+str(dfArgs[i].get(words,0)))
                    tf_idf_val = sentences.get(words)*math.log(length_sens/dfArgs[i].get(words,0))
                    words_freq[words] = tf_idf_val

                sentences_val.append(words_freq)
            tf_idf.append(sentences_val)
            i+=1
        return tf_idf


    def sum_tf_idf(self,tfIdfParagraph):
        val_paragraph = 1
        texts = []
        for paragraph in tfIdfParagraph:
            print("paragraph"+str(val_paragraph))
            sentences = []
            for sens in paragraph:
                keys = list(sens.values())
                output = sum(keys)

                sentences.append(output)
            texts.append(sentences)
            val_paragraph+=1
        return texts


    def bobot_kalimat(self,sentencesArgs, val_tf):
        sentences= []
        for x in range(0,len(sentencesArgs)):
            bobot = {}
            for y in range(0,len(sentencesArgs[x])):

               # print(sentencesArgs[x][y])
               # print(val_tf[x][y])
                #count = frekuensi.get(word, 0)
                bobot[sentencesArgs[x][y]] = val_tf[x][y]
            sentences.append(bobot)


        return sentences


    def rank_kalimat(self,bobotArgs):

        for x in bobotArgs:
            sorted_x = OrderedDict(reversed(sorted(x.items(), key=lambda t: t[1])))

            cnt = 0
            for key, value in sorted_x.items():
                if(cnt<1):
                    print(key, value)

                cnt+=1