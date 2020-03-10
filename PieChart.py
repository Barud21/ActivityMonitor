import wx
import wx.lib.agw.piectrl
from wx.lib.agw.piectrl import PieCtrl, PiePart

class Frame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, -1, "Simple Pie Chart")

        panel = wx.Panel(self, -1, size=(650,650))
        # Create A Simple PieCtrl With 3 Sectors
        self._pie = PieCtrl(panel, -1, wx.DefaultPosition, wx.Size(180,270))

        self._pie.GetLegend().SetTransparent(True)
        self._pie.GetLegend().SetHorizontalBorder(10)
        self._pie.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
        self._pie.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                   wx.FONTSTYLE_NORMAL,
                                                   wx.FONTWEIGHT_NORMAL,
                                                   False, "Courier New"))
        self._pie.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

        self._pie.SetHeight(10)
        self._pie.SetAngle(0.35)

        part = PiePart()

        part.SetLabel("Label_1")
        part.SetValue(300)
        part.SetColour(wx.Colour(200, 50, 50))
        self._pie._series.append(part)

        part = PiePart()
        part.SetLabel("Label 2")
        part.SetValue(200)
        part.SetColour(wx.Colour(50, 200, 50))
        self._pie._series.append(part)

        part = PiePart()
        part.SetLabel("Label 3")
        part.SetValue(50)
        part.SetColour(wx.Colour(50, 50, 200))
        self._pie._series.append(part)
        self.Show()

app = wx.App()
frame = Frame(None)
app.MainLoop()