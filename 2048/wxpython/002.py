#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx


class HelloFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(HelloFrame, self).__init__(*args, **kw)

        pnl = wx.Panel(self)

        st = wx.StaticText(pnl, label='Hello World', pos=(25, 25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText('Welcome to wxPython')
        pass

    def makeMenuBar(self):
        fileMenu = wx.Menu()

        helloItem = fileMenu.Append
        (-1, 'Hello ...\tCtrl-H',
         'help string shown in status bar for this menu item')
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onHello, helloItem)
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)
        self.Bind(wx.EVT_MENU, self.onAbount, aboutItem)
        pass

    def onExit(self, event):
        self.Close(True)
        pass

    def onHello(self, event):
        wx.MessageBox('Hello again from wxPython')
        pass

    def onAbount(self, event):
        wx.MessageBox('this is a wxPython Hello World sample',
                      'about hello world 2', wx.OK | wx.ICON_INFORMATION)
        pass

    def onHelp(self, event):
        pass
    pass


if __name__ == '__main__':
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()
