# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
from nlp import *
import os
###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Natural Languange Processing", pos = wx.DefaultPosition, size = wx.Size( 1300,737 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 16, 74, 90, 90, False, "Arial" ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panelFrame = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizerPanel = wx.GridSizer( 0, 2, 0, 0 )

        bSizerLeft = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText4 = wx.StaticText( self.m_panelFrame, wx.ID_ANY, u"Corpus ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizerLeft.Add( self.m_staticText4, 0, wx.ALL, 5 )

        self.m_richTextFile = wx.richtext.RichTextCtrl( self.m_panelFrame, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        bSizerLeft.Add( self.m_richTextFile, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer10.SetMinSize( wx.Size( 80,80 ) )
        self.buttonOpenFile = wx.Button( self.m_panelFrame, wx.ID_ANY, u"OpenFile", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.buttonOpenFile, 0, wx.ALL, 5 )

        self.buttonTokenisasi = wx.Button( self.m_panelFrame, wx.ID_ANY, u"Tokenisasi", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.buttonTokenisasi, 0, wx.ALL, 5 )

        self.buttonStopword = wx.Button( self.m_panelFrame, wx.ID_ANY, u"Stopword", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.buttonStopword, 0, wx.ALL, 5 )


        bSizerLeft.Add( bSizer10, 0, wx.EXPAND, 0 )


        gSizerPanel.Add( bSizerLeft, 1, wx.EXPAND, 5 )

        bSizerRight = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.m_panelFrame, wx.ID_ANY, u"Hasil Tokenisasi", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        bSizerRight.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.m_richTextToken = wx.richtext.RichTextCtrl( self.m_panelFrame, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        bSizerRight.Add( self.m_richTextToken, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.buttonFrekuensi = wx.Button( self.m_panelFrame, wx.ID_ANY, u"Frekuensi", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.buttonFrekuensi, 0, wx.ALL, 5 )

        self.buttonType = wx.Button( self.m_panelFrame, wx.ID_ANY, u"Tipe Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.buttonType, 0, wx.ALL, 5 )

        self.buttonStemming = wx.Button( self.m_panelFrame, wx.ID_ANY, u"Stemming", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.buttonStemming, 0, wx.ALL, 5 )


        bSizerRight.Add( bSizer11, 0, 0, 0 )

        self.m_richTextHasil = wx.richtext.RichTextCtrl( self.m_panelFrame, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        bSizerRight.Add( self.m_richTextHasil, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText9 = wx.StaticText( self.m_panelFrame, wx.ID_ANY, u"Hasil Akhir", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        bSizerRight.Add( self.m_staticText9, 0, wx.ALL, 5 )


        gSizerPanel.Add( bSizerRight, 1, wx.EXPAND, 5 )


        self.m_panelFrame.SetSizer( gSizerPanel )
        self.m_panelFrame.Layout()
        gSizerPanel.Fit( self.m_panelFrame )
        bSizer1.Add( self.m_panelFrame, 1, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        self.nlp = corpus()

        self.buttonOpenFile.Bind(wx.EVT_BUTTON, self.showText)
        self.buttonTokenisasi.Bind(wx.EVT_BUTTON, self.tokenisasi)
        self.buttonStopword.Bind(wx.EVT_BUTTON, self.stopword)
        self.buttonFrekuensi.Bind(wx.EVT_BUTTON, self.frekuensi)
        self.buttonType.Bind(wx.EVT_BUTTON, self.typedata)


    def __del__( self ):
        pass

    def showText(self, event):
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            text = self.nlp.openText(path)
            self.m_richTextFile.WriteText(text)

    def tokenisasi(self, event):
        teks = self.m_richTextFile.GetValue()
        hasil = self.nlp.tokenisasi(teks)
        self.m_richTextToken.Clear()
        self.m_richTextToken.WriteText(str(hasil))

    def stopword(self, event):
        st = self.m_richTextToken.GetValue()
        st_hasil = self.nlp.stopwords(st)
        self.m_richTextHasil.Clear()
        self.m_richTextHasil.WriteText(str(st_hasil))


    def frekuensi(self, event):
        fr = self.m_richTextToken.GetValue()
        # print(fr)
        fr_hasil = self.nlp.frekuensi(fr)
        # self.m_richTextHasil.DefaultStyle
        # print(fr_hasil)
        self.m_richTextHasil.Clear()
        self.m_richTextHasil.WriteText(str(fr_hasil))


    def typedata(self, event):
        td = self.m_richTextToken.GetValue()
        td_hasil = self.nlp.typedata(td)
        self.m_richTextHasil.Clear()
        self.m_richTextHasil.WriteText(str(td_hasil))

app = wx.App(False)
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
