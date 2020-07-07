# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:37:53 2020
@author: lthompson8
"""

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import numpy as np
import pandas as pd
import glob
import os
import zipfile
import re
import shutil
import csv
import matplotlib.pyplot as plt
import wx
import wx.xrc
import wx.adv
import wx.grid

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg 
###########################################################################
## Class MyFrame2
###########################################################################

def drawPlot(fig, canvas):
    fig.tight_layout()
    canvas.draw()

def addFigAx2Panel(panel, *args, **kw_args):        
    sizer = wx.BoxSizer(wx.VERTICAL)
    fig, ax = plt.subplots(*args, **kw_args)
    canvas = FigureCanvasWxAgg(panel, -1, fig)
    sizer.Add(canvas, 1, wx.EXPAND)
    panel.SetSizer(sizer)
    return fig, ax, canvas
    
class MyFrame2 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 867,729 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"MESONET WEATHER STATION DATA VIEWER", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_staticText4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

        bSizer5.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"To retrieve data, go to unl.box.com and make sure you are logged in. \nThen come back to this tool to set dates and download and view data.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer5.Add( self.m_staticText8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.StartDate = wx.StaticText( self, wx.ID_ANY, u"Start Date", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.StartDate.Wrap( -1 )

        bSizer6.Add( self.StartDate, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_datePicker3 = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
        bSizer6.Add( self.m_datePicker3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.EndDate = wx.StaticText( self, wx.ID_ANY, u"End Date", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.EndDate.Wrap( -1 )

        bSizer6.Add( self.EndDate, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_datePicker4 = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
        bSizer6.Add( self.m_datePicker4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.DownloadData = wx.Button( self, wx.ID_ANY, u"Download", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.DownloadData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        bSizer6.Add( self.DownloadData, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer5.Add( bSizer6, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        frequencyradialChoices = [ u"Hourly", u"Daily", u"Monthly", u"Annual" ]
        self.frequencyradial = wx.RadioBox( self, wx.ID_ANY, u"wxRadioBox", wx.DefaultPosition, wx.DefaultSize, frequencyradialChoices, 1, wx.RA_SPECIFY_COLS )
        self.frequencyradial.SetSelection( 0 )
        bSizer11.Add( self.frequencyradial, 0, wx.ALL, 5 )

        unitsradialChoices = [ u"English", u"Metric" ]
        self.unitsradial = wx.RadioBox( self, wx.ID_ANY, u"wxRadioBox", wx.DefaultPosition, wx.DefaultSize, unitsradialChoices, 1, wx.RA_SPECIFY_COLS )
        self.unitsradial.SetSelection( 0 )
        bSizer11.Add( self.unitsradial, 0, wx.ALL, 5 )


        bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"View charts of temperature and rainfall by hour, day, month, or year.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_staticText11.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )

        bSizer15.Add( self.m_staticText11, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Average Temperature Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        bSizer17.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
        
        self.fig_temp, self.ax_temp, self.canvas_temp = addFigAx2Panel(self.m_panel4)      

        bSizer17.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer15.Add( bSizer17, 1, wx.EXPAND, 5 )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Average Rainfall Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        bSizer18.Add( self.m_staticText14, 0, wx.ALL, 5 )

        self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )

        self.fig_pcp, self.ax_pcp, self.canvas_pcp = addFigAx2Panel(self.m_panel6)      
        
        bSizer18.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer15.Add( bSizer18, 1, wx.EXPAND, 5 )


        bSizer8.Add( bSizer15, 1, wx.EXPAND, 5 )

        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Export a .csv file of data by hour, day, month, or year for the time period specified.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_staticText12.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

        bSizer16.Add( self.m_staticText12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_grid2 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.m_grid2.CreateGrid( 5, 5 )
        self.m_grid2.EnableEditing( True )
        self.m_grid2.EnableGridLines( True )
        self.m_grid2.EnableDragGridSize( False )
        self.m_grid2.SetMargins( 0, 0 )

        # Columns
        self.m_grid2.EnableDragColMove( False )
        self.m_grid2.EnableDragColSize( True )
        self.m_grid2.SetColLabelSize( 30 )
        self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_grid2.EnableDragRowSize( True )
        self.m_grid2.SetRowLabelSize( 80 )
        self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer21.Add( self.m_grid2, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

        self.ExportButton = wx.Button( self, wx.ID_ANY, u"Export Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.ExportButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer16.Add( bSizer21, 0, wx.EXPAND, 5 )


        bSizer8.Add( bSizer16, 0, wx.EXPAND, 5 )


        bSizer10.Add( bSizer8, 1, wx.EXPAND, 5 )


        bSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )


        bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Developed by Laura Thompson, July 2020, v1.1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer5.Add( self.m_staticText5, 0, wx.ALL, 5 )


        self.SetSizer( bSizer5 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.DownloadData.Bind( wx.EVT_BUTTON, self.DownloadDataFuc )
        self.frequencyradial.Bind( wx.EVT_RADIOBOX, self.ChangeInterval )
        self.unitsradial.Bind( wx.EVT_RADIOBOX, self.changeunits )
        self.ExportButton.Bind( wx.EVT_BUTTON, self.Exportcsv )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def DownloadDataFuc( self, event ):
        ### read data using the function
        
        
        
        ### make temperature plots
        self.ax_temp.plot([1, 2], [3, 4])
        drawPlot(self.fig_temp, self.canvas_temp)
        
        
        
        ### make precipitation plots
        self.ax_pcp.plot([1, 2], [4, 3])
        drawPlot(self.fig_pcp, self.canvas_pcp)
        
        
#         parentdirectory = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject'
#         os.chdir(parentdirectory)
#         os.getcwd()
#         zipfpath = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\Rulo_5SW.zip' ##populate this field with your zip file location!!
#         startdate = '2020-01-01' #populate this with your chosen start date!!
#         enddate = '2020-07-06' #populate this with your chosen end date!!

# def openAglByDate(zipfpath, startdate, enddate):
#     '''
#     open zip and read files within the range of the starting date and ending date
#     preferable, controllable
#     '''
#     dfs = []
#     with zipfile.ZipFile(zipfpath) as z:     #   z.infolist()
#         filenames = [f.filename for f in z.infolist()]
#         for d in pd.date_range(startdate, enddate, freq='D'):
#             toOpen = 'Rulo_5SW/Rulo_5SW_agl_{:%Y%m%d}_0703.csv'.format(d)
#             if toOpen in filenames:
#                 # check if the file exists in the zip
#                 with z.open(toOpen) as f:
#                     dfs.append(pd.read_csv(f, header=0, skiprows=1).iloc[2:])
#     return pd.concat(dfs).reset_index(drop=True)

# agl = openAglByDate(zipfpath, startdate, enddate)

 # def downloadData( self, event ):
 #        #print('USGS ID {}'.format(self.txtID.GetValue()))
 #        gages = '&site_no={}'.format(self.txtID.GetValue())
 #        period = '&period=&begin_date={}&end_date={}'.format('2019-01-01', '2019-12-31')
 #        url = 'https://waterdata.usgs.gov/nwis/dv?&cb_00060=on&format=rdb{}&referred_module=sw{}'.format(gages, period)
   
 #        # self.axes.plot([1, 2], [3, 4])
 #        self.dataflow = pd.read_csv(url, comment='#', header=0, sep='\t')[1:].apply(lambda x: pd.to_numeric(x, errors='ignore') if x.name.endswith('_va') else x, axis=0)
 #        print(self.dataflow)
        
 #        self.axes.clear()
 #        pd.to_numeric(self.dataflow.set_index('datetime').iloc[:, 2]).plot(ax=self.axes)
 #        self.downloaded = True
 #        self.canvas.draw()



    def ChangeInterval( self, event ):
        event.Skip()

    def changeunits( self, event ):
        event.Skip()

    def Exportcsv( self, event ):
        event.Skip()

if __name__ == '__main__':
    app = wx.App(redirect=True)
    frm = MyFrame2(None)
    frm.Show()
    app.MainLoop()
