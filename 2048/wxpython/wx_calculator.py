#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx


class CalcFrame(wx.Frame):
    def __init__(self, title):
        super(CalcFrame, self).__init__(
            None, title=title, size=(300, 250))

        self.initView()
        self.Centre()
        self.Show()
        pass

    def initView(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.textprint = wx.TextCtrl(self, style=wx.TE_RIGHT)
        self.equation = ''
        vbox.Add(self.textprint, 1, flag=wx.EXPAND |
                 wx.TOP | wx.BOTTOM, border=4)
        gridBox = wx.GridSizer(5, 4, 5, 5)
        lables = ['AC', 'DEL', 'pi', 'CLOSE',
                  '7', '8', '9', '/',
                  '4', '5', '6', '*',
                  '1', '2', '3', '-',
                  '0', '.', '=', '+']
        for label in lables:
            buttonItem = wx.Button(self, label=label)
            self.createHandler(buttonItem, label)
            gridBox.Add(buttonItem, 1, wx.EXPAND)

        vbox.Add(gridBox, proportion=7, flag=wx.EXPAND)
        self.SetSizer(vbox)
        pass

    def createHandler(self, button, label):
        items = 'DEL AC = CLOSE'

        if label not in items:
            self.Bind(wx.EVT_BUTTON, self.onAppend, button)
        elif label == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.onDel, button)
        elif label == 'AC':
            self.Bind(wx.EVT_BUTTON, self.onAc, button)
        elif label == '=':
            self.Bind(wx.EVT_BUTTON, self.onEqual, button)
        elif label == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.onClose, button)
        pass

    def onAppend(self, event):
        button = event.GetEventObject()
        label = button.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)
        pass

    def onDel(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)
        pass

    def onAc(self, event):
        self.textprint.Clear()
        self.equation = ''
        pass

    def onClose(self, event):
        self.Close()
        pass

    def onEqual(self, event):
        string = self.equation
        try:
            target = eval(string)
            print(target)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except Exception as e:
            dlg = wx.MessageDialog(self, u'格式错误，请输入正确的等式! %s' % e,
                                   u'请注意', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        pass

    pass


if __name__ == '__main__':
    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()
