import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pandas as pd
import json
from pyqtgraph import TextItem
from pyqtgraph.exporters import ImageExporter
from pyqtgraph import mkPen
from PyQt5.QtGui import QFont
import datetime
import time

# Function to convert time strings to timestamps
def format_time_ticks(values, scale, spacing):
    """Convert timestamp values to formatted time strings"""
    result = []
    for val in values:
        try:
            if val > 0:  # Make sure it's a positive timestamp
                dt = datetime.datetime.fromtimestamp(val)
                result.append(dt.strftime('%H:%M:%S'))
            else:
                result.append('')
        except (ValueError, OSError, OverflowError) as e:
            # print(f"Error with timestamp {val}: {e}")
            result.append('')
    return result

# Function to format timestamps as time strings for the axis
def time_string_to_timestamp(time_str):
    """Convert a time string to Unix timestamp"""
    try:
        # Assuming time_str format is something like "09:30:15"
        today = datetime.datetime.now().date()
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
        dt = datetime.datetime.combine(today, time_obj)
        ts = time.mktime(dt.timetuple())
        
        # Debug print
        # print(f"Converted '{time_str}' to timestamp {ts}")
        
        return ts
    except (ValueError, TypeError) as e:
        # print(f"Error converting time: {time_str}, Error: {e}")
        # Instead of returning 0, which could be an invalid timestamp
        # Return the current time's timestamp as a fallback
        return time.time()

# Start the application
app = QApplication([])

# Create main window
win = pg.GraphicsLayoutWidget(title="Real-Time Plot (1 Subplot)")
win.resize(1500, 1200)
win.show()

# Load Data
with open('data.json', 'r') as file_read:
    data=json.load(file_read)

df = pd.DataFrame(data)

for i in range(0,5):
    df.iloc[0,i] = round(pd.Series(df.iloc[0,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[1,i] = round(pd.Series(df.iloc[1,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[2,i] = round(pd.Series(df.iloc[2,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[3,i] = round(pd.Series(df.iloc[3,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[4,i] = round(pd.Series(df.iloc[4,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[5,i] = round(pd.Series(df.iloc[5,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[6,i] = round(pd.Series(df.iloc[6,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[7,i] = round(pd.Series(df.iloc[7,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[8,i] = round(pd.Series(df.iloc[8,i]).ewm(span=100, adjust=False).mean(),5).tolist()
    df.iloc[9,i] = round(pd.Series(df.iloc[9,i]).ewm(span=100, adjust=False).mean(),5).tolist()
    df.iloc[10,i] = round(pd.Series(df.iloc[10,i]).ewm(span=100, adjust=False).mean(),5).tolist()
    df.iloc[11,i] = round(pd.Series(df.iloc[11,i]).ewm(span=100, adjust=False).mean(),5).tolist()
    df.iloc[12,i] = round(pd.Series(df.iloc[12,i]).ewm(span=100, adjust=False).mean(),5).tolist()
    df.iloc[13,i] = round(pd.Series(df.iloc[13,i]).ewm(span=300, adjust=False).mean(),5).tolist()
    df.iloc[14,i] = round(pd.Series(df.iloc[14,i]).ewm(span=300, adjust=False).mean(),5).tolist()

df = df.to_dict()

with open('smoothed_data.json', 'w') as file_write:
    json.dump(df, file_write)

with open('smoothed_data.json', 'r') as file_read:
    data = json.load(file_read)

dfp = pd.DataFrame(data)

# Initialize data for each expiry's time axis
x1, x2, x3 = [], [], []  # Time arrays for each expiry
y0_1, y1_1, y6_1, y7_1, y10_1, y11_1, y12_1, y13_1, y15_1 = [], [], [], [], [], [], [], [], []
y0_2, y1_2, y6_2, y7_2, y10_2, y11_2, y12_2, y13_2, y15_2 = [], [], [], [], [], [], [], [], []
y0_3, y1_3, y6_3, y7_3, y10_3, y11_3, y12_3, y13_3, y15_3 = [], [], [], [], [], [], [], [], []
##################################################################################

expiry_names = dfp.columns.tolist()

################################################################################## Expiry 1

plot00 = win.addPlot(row=0, col=0, title=f"Nifty - CE/PE OTMs - {expiry_names[0][-10:]}")
plot00.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot00.addLegend()
# plot00.showGrid(x=True, y=True, alpha=0.3)
# Set the x-axis formatting to use time strings
plot00.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_1 = plot00.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_1 = plot00.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot10 = win.addPlot(row=1, col=0, title="Nifty - CE-PE ATM, Straddle")
plot10.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot10.addLegend()
# plot10.showGrid(x=True, y=True, alpha=0.3)
plot10.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_1 = plot10.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_1 = plot10.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_1 = plot10.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot20 = win.addPlot(row=2, col=0, title="Nifty - CE/PE OTMs Implied Volatility")
plot20.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot20.addLegend()
# plot20.showGrid(x=True, y=True, alpha=0.3)
plot20.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_1 = plot20.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_1 = plot20.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_1 = plot20.plot([], pen=mkPen('r', width=3), name='SPOT')

################################################################################## Expiry 2

plot01 = win.addPlot(row=0, col=1, title=f"Bank Nifty - CE/PE OTMs - {expiry_names[3][-10:]}")
plot01.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot01.addLegend()
# plot01.showGrid(x=True, y=True, alpha=0.3)
plot01.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_2 = plot01.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_2 = plot01.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot11 = win.addPlot(row=1, col=1, title="Bank Nifty - CE-PE ATM, Straddle")
plot11.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot11.addLegend()
# plot11.showGrid(x=True, y=True, alpha=0.3)
plot11.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_2 = plot11.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_2 = plot11.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_2 = plot11.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot21 = win.addPlot(row=2, col=1, title="Bank Nifty - CE/PE OTMs Implied Volatility")
plot21.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot21.addLegend()
# plot21.showGrid(x=True, y=True, alpha=0.3)
plot21.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_2 = plot21.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_2 = plot21.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_2 = plot21.plot([], pen=mkPen('r', width=3), name='SPOT')

################################################################################# Expiry 3

plot02 = win.addPlot(row=0, col=2, title=f"Sensex - CE/PE OTMs - {expiry_names[4][-10:]}")
plot02.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot02.addLegend()
# plot02.showGrid(x=True, y=True, alpha=0.3)
plot02.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_3 = plot02.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_3 = plot02.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot12 = win.addPlot(row=1, col=2, title="Sensex - CE-PE ATM, Straddle")
plot12.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot12.addLegend()
# plot12.showGrid(x=True, y=True, alpha=0.3)
plot12.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_3 = plot12.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_3 = plot12.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_3 = plot12.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot22 = win.addPlot(row=2, col=2, title="Sensex - CE/PE OTMs Implied Volatility")
plot22.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot22.addLegend()
# plot22.showGrid(x=True, y=True, alpha=0.3)
plot22.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_3 = plot22.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_3 = plot22.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_3 = plot22.plot([], pen=mkPen('r', width=3), name='SPOT')

for plot in [plot00, plot10, plot20, plot01, plot11, plot21, plot02, plot12, plot22]:
    plot.getAxis('bottom').tickStrings = format_time_ticks

#################################################################################

# For plot20's ViewBox - Create the data item FIRST
line_13_1_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_20 = pg.ViewBox()
plot20.showAxis('right')
plot20.scene().addItem(vb_right_20)
plot20.getAxis('right')#.setLabel("SPOT")  # More descriptive label
plot20.getAxis('right').linkToView(vb_right_20)  # Link right axis to right ViewBox
vb_right_20.setXLink(plot20)  # Keep X-axis linked for alignment
vb_right_20.setYLink(None)  # Explicitly unlink Y-axis
vb_right_20.addItem(line_13_1_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_20 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_20.addItem(zero_line_20)  # Add the zero line to the ViewBox

# For plot20
def updateViews_20():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_20.setGeometry(plot20.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_20.setYLink(None)

def adjust_right_view_20():
    """Dynamically adjust the range of the right Y-axis for plot20."""
    if y13_1:
        # Set explicit Y range based on SPOT data (y13_1)
        min_val = min(y13_1) - abs(min(y13_1) * 0.05)  # 5% padding below
        max_val = max(y13_1) + abs(max(y13_1) * 0.05)  # 5% padding above
        vb_right_20.setYRange(min_val, max_val)

plot20.vb.sigResized.connect(updateViews_20)

# Similarly for plot21
line_13_2_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_21 = pg.ViewBox()
plot21.showAxis('right')
plot21.scene().addItem(vb_right_21)
plot21.getAxis('right')#.setLabel("SPOT")
plot21.getAxis('right').linkToView(vb_right_21)
vb_right_21.setXLink(plot21)
vb_right_21.setYLink(None)
vb_right_21.addItem(line_13_2_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_21 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_21.addItem(zero_line_21)  # Add the zero line to the ViewBox

# For plot21
def updateViews_21():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_21.setGeometry(plot21.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_21.setYLink(None)

def adjust_right_view_21():
    """Dynamically adjust the range of the right Y-axis for plot21."""
    if y13_2:
        # Set explicit Y range based on SPOT data (y13_2)
        min_val = min(y13_2) - abs(min(y13_2) * 0.05)  # 5% padding below
        max_val = max(y13_2) + abs(max(y13_2) * 0.05)  # 5% padding above
        vb_right_21.setYRange(min_val, max_val)

plot21.vb.sigResized.connect(updateViews_21)

# And for plot22
line_13_3_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_22 = pg.ViewBox()
plot22.showAxis('right')
plot22.scene().addItem(vb_right_22)
plot22.getAxis('right')#.setLabel("SPOT")
plot22.getAxis('right').linkToView(vb_right_22)
vb_right_22.setXLink(plot22)
vb_right_22.setYLink(None)
vb_right_22.addItem(line_13_3_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_22 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_22.addItem(zero_line_22)  # Add the zero line to the ViewBox

# For plot22
def updateViews_22():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_22.setGeometry(plot22.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_22.setYLink(None)

def adjust_right_view_22():
    """Dynamically adjust the range of the right Y-axis for plot22."""
    if y13_3:
        # Set explicit Y range based on SPOT data (y13_3)
        min_val = min(y13_3) - abs(min(y13_3) * 0.05)  # 5% padding below
        max_val = max(y13_3) + abs(max(y13_3) * 0.05)  # 5% padding above
        vb_right_22.setYRange(min_val, max_val)

plot22.vb.sigResized.connect(updateViews_22)

#############################################################

# --------------- Labels ---------------

label_dict = {}

# For plot00
label_0 = TextItem(anchor=(0, 0.5))
label_0.setFont(QFont('Arial', 12))
plot00.addItem(label_0)
label_dict['label_0'] = label_0

label_1 = TextItem(anchor=(0, 0.5))
label_1.setFont(QFont('Arial', 12))
plot00.addItem(label_1)
label_dict['label_1'] = label_1

# For plot10
label_10 = TextItem(anchor=(0, 0.5))
label_10.setFont(QFont('Arial', 12))
plot10.addItem(label_10)
label_dict['label_10'] = label_10

label_11 = TextItem(anchor=(0, 0.5))
label_11.setFont(QFont('Arial', 12))
plot10.addItem(label_11)
label_dict['label_11'] = label_11

label_12 = TextItem(anchor=(0, 0.5))
label_12.setFont(QFont('Arial', 12))
plot10.addItem(label_12)
label_dict['label_12'] = label_12

# For plot20
label_6 = TextItem(anchor=(0, 0.5))
label_6.setFont(QFont('Arial', 12))
plot20.addItem(label_6)
label_dict['label_6'] = label_6

label_7 = TextItem(anchor=(0, 0.5))
label_7.setFont(QFont('Arial', 12))
plot20.addItem(label_7)
label_dict['label_7'] = label_7

label_13 = TextItem(anchor=(0, 0.5))
label_13.setFont(QFont('Arial', 12))
plot20.addItem(label_13)
label_dict['label_13'] = label_13

# For plot01
label_0_2 = TextItem(anchor=(0, 0.5))
label_0_2.setFont(QFont('Arial', 12))
plot01.addItem(label_0_2)
label_dict['label_0_2'] = label_0_2

label_1_2 = TextItem(anchor=(0, 0.5))
label_1_2.setFont(QFont('Arial', 12))
plot01.addItem(label_1_2)
label_dict['label_1_2'] = label_1_2

# For plot11
label_10_2 = TextItem(anchor=(0, 0.5))
label_10_2.setFont(QFont('Arial', 12))
plot11.addItem(label_10_2)
label_dict['label_10_2'] = label_10_2

label_11_2 = TextItem(anchor=(0, 0.5))
label_11_2.setFont(QFont('Arial', 12))
plot11.addItem(label_11_2)
label_dict['label_11_2'] = label_11_2

label_12_2 = TextItem(anchor=(0, 0.5))
label_12_2.setFont(QFont('Arial', 12))
plot11.addItem(label_12_2)
label_dict['label_12_2'] = label_12_2

# For plot21
label_6_2 = TextItem(anchor=(0, 0.5))
label_6_2.setFont(QFont('Arial', 12))
plot21.addItem(label_6_2)
label_dict['label_6_2'] = label_6_2

label_7_2 = TextItem(anchor=(0, 0.5))
label_7_2.setFont(QFont('Arial', 12))
plot21.addItem(label_7_2)
label_dict['label_7_2'] = label_7_2

label_13_2 = TextItem(anchor=(0, 0.5))
label_13_2.setFont(QFont('Arial', 12))
plot21.addItem(label_13_2)
label_dict['label_13_2'] = label_13_2

# For plot02
label_0_3 = TextItem(anchor=(0, 0.5))
label_0_3.setFont(QFont('Arial', 12))
plot02.addItem(label_0_3)
label_dict['label_0_3'] = label_0_3

label_1_3 = TextItem(anchor=(0, 0.5))
label_1_3.setFont(QFont('Arial', 12))
plot02.addItem(label_1_3)
label_dict['label_1_3'] = label_1_3

# For plot12
label_10_3 = TextItem(anchor=(0, 0.5))
label_10_3.setFont(QFont('Arial', 12))
plot12.addItem(label_10_3)
label_dict['label_10_3'] = label_10_3

label_11_3 = TextItem(anchor=(0, 0.5))
label_11_3.setFont(QFont('Arial', 12))
plot12.addItem(label_11_3)
label_dict['label_11_3'] = label_11_3

label_12_3 = TextItem(anchor=(0, 0.5))
label_12_3.setFont(QFont('Arial', 12))
plot12.addItem(label_12_3)
label_dict['label_12_3'] = label_12_3

# For plot22
label_6_3 = TextItem(anchor=(0, 0.5))
label_6_3.setFont(QFont('Arial', 12))
plot22.addItem(label_6_3)
label_dict['label_6_3'] = label_6_3

label_7_3 = TextItem(anchor=(0, 0.5))
label_7_3.setFont(QFont('Arial', 12))
plot22.addItem(label_7_3)
label_dict['label_7_3'] = label_7_3

label_13_3 = TextItem(anchor=(0, 0.5))
label_13_3.setFont(QFont('Arial', 12))
plot22.addItem(label_13_3)
label_dict['label_13_3'] = label_13_3

# Create separate labels for SPOT data - add this after all other label definitions
label_13_right = TextItem(anchor=(0, 0.5))
label_13_right.setFont(QFont('Arial', 12))
vb_right_20.addItem(label_13_right)  # Add to the right ViewBox
label_dict['label_13_right'] = label_13_right

label_13_2_right = TextItem(anchor=(0, 0.5))
label_13_2_right.setFont(QFont('Arial', 12))
vb_right_21.addItem(label_13_2_right)  # Add to the right ViewBox
label_dict['label_13_2_right'] = label_13_2_right

label_13_3_right = TextItem(anchor=(0, 0.5))
label_13_3_right.setFont(QFont('Arial', 12))
vb_right_22.addItem(label_13_3_right)  # Add to the right ViewBox
label_dict['label_13_3_right'] = label_13_3_right

# --------------- Update Function ---------------
i = 0

def update():
    global i

    # Get time data for all three expiries
    time_str_1 = dfp.iloc[15,0][i]  # Time for Expiry 1 (Nifty)
    time_str_2 = dfp.iloc[15,3][i]  # Time for Expiry 2 (Bank Nifty)
    time_str_3 = dfp.iloc[15,4][i]  # Time for Expiry 3 (Sensex)
    
    # Convert time strings to timestamps
    timestamp_1 = time_string_to_timestamp(time_str_1)
    timestamp_2 = time_string_to_timestamp(time_str_2)
    timestamp_3 = time_string_to_timestamp(time_str_3)
    
    # Store timestamps in x-axis arrays
    x1.append(timestamp_1)
    x2.append(timestamp_2)
    x3.append(timestamp_3)

    # Update Expiry 1 data
    y0_1.append(dfp.iloc[0,0][i])
    y1_1.append(dfp.iloc[1,0][i])
    y10_1.append(dfp.iloc[10,0][i])
    y11_1.append(dfp.iloc[11,0][i])
    y12_1.append(dfp.iloc[12,0][i])
    y6_1.append(dfp.iloc[6,0][i])
    y7_1.append(dfp.iloc[7,0][i])
    y13_1.append(dfp.iloc[13,0][i])
    y15_1.append(dfp.iloc[15,0][i])  # Time data

    # Update Expiry 1 plots with timestamps
    line_0_1.setData(x1, y0_1)
    line_1_1.setData(x1, y1_1)
    line_10_1.setData(x1, y10_1)
    line_11_1.setData(x1, y11_1)
    line_12_1.setData(x1, y12_1)
    line_6_1.setData(x1, y6_1)
    line_7_1.setData(x1, y7_1)
    line_13_1_right.setData(x1, y13_1)  # Use timestamps for right y-axis too
    adjust_right_view_20()

    # Update Expiry 2 data
    y0_2.append(dfp.iloc[0,3][i])
    y1_2.append(dfp.iloc[1,3][i])
    y10_2.append(dfp.iloc[10,3][i])
    y11_2.append(dfp.iloc[11,3][i])
    y12_2.append(dfp.iloc[12,3][i])
    y6_2.append(dfp.iloc[6,3][i])
    y7_2.append(dfp.iloc[7,3][i])
    y13_2.append(dfp.iloc[13,3][i])
    y15_2.append(dfp.iloc[15,3][i])  # Time data

    # Update Expiry 2 plots with timestamps
    line_0_2.setData(x2, y0_2)
    line_1_2.setData(x2, y1_2)
    line_10_2.setData(x2, y10_2)
    line_11_2.setData(x2, y11_2)
    line_12_2.setData(x2, y12_2)
    line_6_2.setData(x2, y6_2)
    line_7_2.setData(x2, y7_2)
    line_13_2_right.setData(x2, y13_2)  # Use timestamps for right y-axis too
    adjust_right_view_21()

    # Update Expiry 3 data
    y0_3.append(dfp.iloc[0,4][i])
    y1_3.append(dfp.iloc[1,4][i])
    y10_3.append(dfp.iloc[10,4][i])
    y11_3.append(dfp.iloc[11,4][i])
    y12_3.append(dfp.iloc[12,4][i])
    y6_3.append(dfp.iloc[6,4][i])
    y7_3.append(dfp.iloc[7,4][i])
    y13_3.append(dfp.iloc[13,4][i])
    y15_3.append(dfp.iloc[15,4][i])  # Time data

    # Update Expiry 3 plots with timestamps
    line_0_3.setData(x3, y0_3)
    line_1_3.setData(x3, y1_3)
    line_10_3.setData(x3, y10_3)
    line_11_3.setData(x3, y11_3)
    line_12_3.setData(x3, y12_3)
    line_6_3.setData(x3, y6_3)
    line_7_3.setData(x3, y7_3)
    line_13_3_right.setData(x3, y13_3)  # Use timestamps for right y-axis too
    adjust_right_view_22()

    # Update Labels with timestamps for x-position
    if x1 and y0_1:
        # Update Expiry 1 labels
        label_dict['label_0'].setText(f"{y0_1[-1]:.2f}")
        label_dict['label_0'].setPos(x1[-1], y0_1[-1])
        label_dict['label_1'].setText(f"{y1_1[-1]:.2f}")
        label_dict['label_1'].setPos(x1[-1], y1_1[-1])
        label_dict['label_10'].setText(f"{y10_1[-1]:.2f}")
        label_dict['label_10'].setPos(x1[-1], y10_1[-1])
        label_dict['label_11'].setText(f"{y11_1[-1]:.2f}")
        label_dict['label_11'].setPos(x1[-1], y11_1[-1])
        label_dict['label_12'].setText(f"{y12_1[-1]:.2f}")
        label_dict['label_12'].setPos(x1[-1], y12_1[-1])
        label_dict['label_6'].setText(f"{y6_1[-1]:.2f}")
        label_dict['label_6'].setPos(x1[-1], y6_1[-1])
        label_dict['label_7'].setText(f"{y7_1[-1]:.2f}")
        label_dict['label_7'].setPos(x1[-1], y7_1[-1])
        label_dict['label_13_right'].setText(f"{y13_1[-1]:.2f}")
        label_dict['label_13_right'].setPos(x1[-1], y13_1[-1])

    if x2 and y0_2:
        # Update Expiry 2 labels
        label_dict['label_0_2'].setText(f"{y0_2[-1]:.2f}")
        label_dict['label_0_2'].setPos(x2[-1], y0_2[-1])
        label_dict['label_1_2'].setText(f"{y1_2[-1]:.2f}")
        label_dict['label_1_2'].setPos(x2[-1], y1_2[-1])
        label_dict['label_10_2'].setText(f"{y10_2[-1]:.2f}")
        label_dict['label_10_2'].setPos(x2[-1], y10_2[-1])
        label_dict['label_11_2'].setText(f"{y11_2[-1]:.2f}")
        label_dict['label_11_2'].setPos(x2[-1], y11_2[-1])
        label_dict['label_12_2'].setText(f"{y12_2[-1]:.2f}")
        label_dict['label_12_2'].setPos(x2[-1], y12_2[-1])
        label_dict['label_6_2'].setText(f"{y6_2[-1]:.2f}")
        label_dict['label_6_2'].setPos(x2[-1], y6_2[-1])
        label_dict['label_7_2'].setText(f"{y7_2[-1]:.2f}")
        label_dict['label_7_2'].setPos(x2[-1], y7_2[-1])
        label_dict['label_13_2_right'].setText(f"{y13_2[-1]:.2f}")
        label_dict['label_13_2_right'].setPos(x2[-1], y13_2[-1])

    if x3 and y0_3:
        # Update Expiry 3 labels
        label_dict['label_0_3'].setText(f"{y0_3[-1]:.2f}")
        label_dict['label_0_3'].setPos(x3[-1], y0_3[-1])
        label_dict['label_1_3'].setText(f"{y1_3[-1]:.2f}")
        label_dict['label_1_3'].setPos(x3[-1], y1_3[-1])
        label_dict['label_10_3'].setText(f"{y10_3[-1]:.2f}")
        label_dict['label_10_3'].setPos(x3[-1], y10_3[-1])
        label_dict['label_11_3'].setText(f"{y11_3[-1]:.2f}")
        label_dict['label_11_3'].setPos(x3[-1], y11_3[-1])
        label_dict['label_12_3'].setText(f"{y12_3[-1]:.2f}")
        label_dict['label_12_3'].setPos(x3[-1], y12_3[-1])
        label_dict['label_6_3'].setText(f"{y6_3[-1]:.2f}")
        label_dict['label_6_3'].setPos(x3[-1], y6_3[-1])
        label_dict['label_7_3'].setText(f"{y7_3[-1]:.2f}")
        label_dict['label_7_3'].setPos(x3[-1], y7_3[-1])
        label_dict['label_13_3_right'].setText(f"{y13_3[-1]:.2f}")
        label_dict['label_13_3_right'].setPos(x3[-1], y13_3[-1])

    # Set X range for each column of plots separately based on timestamps
    if x1 and len(x1) > 1:
        # Set X range for Expiry 1 plots (first column)
        plot00.setXRange(x1[0], x1[-1], padding=0.1)
        plot10.setXRange(x1[0], x1[-1], padding=0.1)
        plot20.setXRange(x1[0], x1[-1], padding=0.1)
    
    if x2 and len(x2) > 1:
        # Set X range for Expiry 2 plots (second column)
        plot01.setXRange(x2[0], x2[-1], padding=0.1)
        plot11.setXRange(x2[0], x2[-1], padding=0.1)
        plot21.setXRange(x2[0], x2[-1], padding=0.1)
    
    if x3 and len(x3) > 1:
        # Set X range for Expiry 3 plots (third column)
        plot02.setXRange(x3[0], x3[-1], padding=0.1)
        plot12.setXRange(x3[0], x3[-1], padding=0.1)
        plot22.setXRange(x3[0], x3[-1], padding=0.1)

    i += 1
    if i >= 2800:
        exporter = ImageExporter(win.scene())
        exporter.parameters()['width'] = 1600
        exporter.export("plot_snapshot.png")
        print("Plot saved as plot_snapshot.png")
        timer.stop()

# Start timer
timer = QTimer()
timer.timeout.connect(update)
timer.start()

####################################################################

from PyQt5.QtCore import Qt

# Add this after creating the win object
def keyPressEvent(event):
    if event.key() == Qt.Key_F11:  # F11 is commonly used for toggling fullscreen
        if win.isFullScreen():
            win.showMaximized()
        else:
            win.showFullScreen()
    elif event.key() == Qt.Key_Escape and win.isFullScreen():  # ESC to exit fullscreen
        win.showMaximized()

# Connect the keyPressEvent function to the window
win.keyPressEvent = keyPressEvent

#####################################################################

# Run app
app.exec_()