import cairo
from calendar import monthrange
import datetime
import pandas as pd
import sys

# Config
xd = 11 # day width, i.e., number of (horizontal) grid points per day column
yd = 16 # day height, i.e., number of (vertical) grid points per month row
padding = 5 # number of padding dots around the calendar
lpad = 8 # additional padding on the left side for month initial letters (in grid dots)
spacing = 18 # size of white space around the grid/dots (in points; 1 point = 0,0352777806 cm)
dot_w = 0.1 # diameter of a grid dot
width = 2345.1 # width of the output PDF (in points). Plus spacing*2, should give A1
font_default = "Iosevka" # default font
font_month_letters = "Iosevka"
month_letters = "JFMAMJJASOND" # initial letters for the months


# Calculate the number of dots in the grid and the size of the PDF
grid = (37*xd + 1 + padding*2 + lpad - 1 , 12*yd + 1 + padding*2 - 1) # dimensions of the drawing grid (in grid dots)
size = (width, width*grid[1]/grid[0]) # Size of the PDF (in points)

# Read the year from the program arguments
if len(sys.argv) != 2:
    print("Usage: cal.py [YEAR]")
    sys.exit()
year = int(float(sys.argv[1]))

# Read special days (e.g., public holidays in Berlin)
special_days = pd.read_csv("feiertage_berlin.csv", sep=";")
special_days["date"] = pd.to_datetime(special_days.Datum, format="%d.%m.%Y")
special_days["text"] = special_days.Bezeichnung

# The drawing context
surface = cairo.PDFSurface("cal_"+str(year)+".pdf",size[0]+spacing*2, size[1]+spacing*2)
c = cairo.Context(surface)

# Set up a convenient mapping from grid dots to points in the PDF
c.transform(cairo.Matrix(size[0]/grid[0], 0.0,
                         0.0,             size[1]/grid[1],
                         spacing,         spacing))

# Helper: draw a dot at a specific grid coordinate
def dot(context, x, y):
    context.rectangle(x-dot_w/2, y-dot_w/2, dot_w, dot_w)
    context.fill()

# Padding dots (dots around the calendar)
for i in range(grid[0]+1):
    for j in range(grid[1]+1):
        if i < padding+lpad or i > grid[0]-padding or j < padding or j > grid[1]-padding:
            dot(c,i,j)

# Horizontal dot lines (separating months)
for month in range(13):
    for i in range(padding+lpad, grid[0]-padding+1):
        dot(c, i, padding+month*yd)

# Vertical dot lines (separating days)
for day in range(38):
    for j in range(padding, grid[1]-padding+1):
        dot(c, padding+lpad+day*xd, j)

# The calendar
for month in range(1,13):
  mr = monthrange(year, month)

  # Write out the initial letter of the month
  c.set_font_size(6.0)
  c.select_font_face(font_month_letters, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
  s = month_letters[month-1]
  xbearing, ybearing, tw, th, tdx, tdy = c.text_extents(s)
  c.set_source_rgba(0, 0, 0, 1)
  c.move_to(padding+lpad+(mr[0]-1)*xd+(xd)/2-tw/2, padding+(month)*yd-yd/2+th/2)
  c.show_text(s)

  for d in range(1,mr[1]+1):
    wd = datetime.date(year, month, d).weekday()
    matching_special_days = special_days[special_days.date == str(year)+"-"+str(month)+"-"+str(d)]
    c.select_font_face(font_default, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_source_rgba(0, 0, 0, 1)

    # Is this a day of the weekend?
    if wd == 5 or wd == 6:
      c.set_source_rgba(0, 0, 0, 0.3)

    # Is this one of the listed special days (e.g., public holiday)?
    if len(matching_special_days.index) > 0:
      c.set_font_size(1.0)
      lh = 0
      for line in matching_special_days.text.iloc[0].split("<br>"):
          xbearing, ybearing, tw, th, tdx, tdy = c.text_extents(line)
          c.move_to(lpad+padding+(d+mr[0]-1)*xd+(xd)/2-tw/2, padding+(month-1)*yd+6.5+lh)
          c.show_text(line)
          lh = lh + 0.9 + 0.3

    # Write out the number of this day
    c.set_font_size(3.5)
    s = str(d)
    xbearing, ybearing, tw, th, tdx, tdy = c.text_extents(s)
    c.move_to(lpad+padding+(d+mr[0]-1)*xd+(xd-0.5)/2-tw/2, padding+(month-1)*yd+th+2)
    c.show_text(s)

  # Fill empty days with grid dots
  c.set_source_rgba(0, 0, 0, 1)
  for i in list(range(mr[0]))+list(range(mr[0]+mr[1],37)):
    for xo in range(1,xd):
      for yo in range(1,yd):
        dot(c, lpad+padding+i*xd+xo,padding+month*yd-yo)

surface.finish()
