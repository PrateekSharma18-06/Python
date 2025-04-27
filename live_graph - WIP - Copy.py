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

# Start the application
app = QApplication([])

# Create main window
win = pg.GraphicsLayoutWidget(title="Real-Time Plot (1 Subplot)")
win.resize(1500, 1200)
win.show()

# Load Data
with open('data.json', 'r') as file_read:
    data=json.load(file_read)

dfp = pd.DataFrame(data)

# Initialize data
x = []

y0_1, y1_1, y6_1, y7_1, y10_1, y11_1, y12_1, y13_1 = [], [], [], [], [], [], [], []
y0_2, y1_2, y6_2, y7_2, y10_2, y11_2, y12_2, y13_2 = [], [], [], [], [], [], [], []
y0_3, y1_3, y6_3, y7_3, y10_3, y11_3, y12_3, y13_3 = [], [], [], [], [], [], [], []

################################################################################## Expiry 1

plot00 = win.addPlot(row=0, col=0, title="Expiry 1 - CE/PE OTMs SUM")
plot00.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot00.addLegend()
plot00.showGrid(x=True, y=True, alpha=0.3)
line_0_1 = plot00.plot([], pen=mkPen('g', width=3), name='CE SUM')
line_1_1 = plot00.plot([], pen=mkPen('y', width=3), name='PE SUM')

plot10 = win.addPlot(row=1, col=0, title="Expiry 1 - CE-PE ATM, Straddle")
plot10.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot10.addLegend()
plot10.showGrid(x=True, y=True, alpha=0.3)
line_10_1 = plot10.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_1 = plot10.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_1 = plot10.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot20 = win.addPlot(row=2, col=0, title="Expiry 1 - CE/PE OTMs Implied Volatility")
plot20.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot20.addLegend()
plot20.showGrid(x=True, y=True, alpha=0.3)
line_6_1 = plot20.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_1 = plot20.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_1 = plot20.plot([], pen=mkPen('m', width=3), name='SPOT')

################################################################################## Expiry 2

plot01 = win.addPlot(row=0, col=1, title="Expiry 2 - CE/PE OTMs SUM")
plot01.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot01.addLegend()
plot01.showGrid(x=True, y=True, alpha=0.3)
line_0_2 = plot01.plot([], pen=mkPen('g', width=3), name='CE SUM')
line_1_2 = plot01.plot([], pen=mkPen('y', width=3), name='PE SUM')

plot11 = win.addPlot(row=1, col=1, title="Expiry 2 - CE-PE ATM, Straddle")
plot11.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot11.addLegend()
plot11.showGrid(x=True, y=True, alpha=0.3)
line_10_2 = plot11.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_2 = plot11.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_2 = plot11.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot21 = win.addPlot(row=2, col=1, title="Expiry 2 - CE/PE OTMs Implied Volatility")
plot21.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot21.addLegend()
plot21.showGrid(x=True, y=True, alpha=0.3)
line_6_2 = plot21.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_2 = plot21.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_2 = plot21.plot([], pen=mkPen('m', width=3), name='SPOT')

################################################################################# Expiry 3

plot02 = win.addPlot(row=0, col=2, title="Expiry 3 - CE/PE OTMs SUM")
plot02.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot02.addLegend()
plot02.showGrid(x=True, y=True, alpha=0.3)
line_0_3 = plot02.plot([], pen=mkPen('g', width=3), name='CE SUM')
line_1_3 = plot02.plot([], pen=mkPen('y', width=3), name='PE SUM')

plot12 = win.addPlot(row=1, col=2, title="Expiry 3 - CE-PE ATM, Straddle")
plot12.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot12.addLegend()
plot12.showGrid(x=True, y=True, alpha=0.3)
line_10_3 = plot12.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_3 = plot12.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_3 = plot12.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot22 = win.addPlot(row=2, col=2, title="Expiry 3 - CE/PE OTMs Implied Volatility")
plot22.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot22.addLegend()
plot22.showGrid(x=True, y=True, alpha=0.3)
line_6_3 = plot22.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_3 = plot22.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_3 = plot22.plot([], pen=mkPen('m', width=3), name='SPOT')

#################################################################################

# For plot20
vb_right_20 = pg.ViewBox()
plot20.showAxis('right')
plot20.scene().addItem(vb_right_20)
plot20.getAxis('right').setLabel("Right Y-Axis")
vb_right_20.setXLink(plot20)  # Keep X-axis linked for alignment
line_13_1_right = pg.PlotDataItem(pen=mkPen('m', width=2))
vb_right_20.addItem(line_13_1_right)

def updateViews_20():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_20.setGeometry(plot20.vb.sceneBoundingRect())  # Align geometrically

def adjust_right_view_20():
    """Dynamically adjust the range of the right Y-axis for plot20."""
    if y13_1:
        vb_right_20.setRange(yRange=(min(y13_1), max(y13_1)), padding=0.1)  # Independent Y-scaling

plot20.vb.sigResized.connect(updateViews_20)

# For plot21
vb_right_21 = pg.ViewBox()
plot21.showAxis('right')
plot21.scene().addItem(vb_right_21)
plot21.getAxis('right').setLabel("Right Y-Axis")
vb_right_21.setXLink(plot21)  # Keep X-axis linked for alignment
line_13_2_right = pg.PlotDataItem(pen=mkPen('m', width=2))
vb_right_21.addItem(line_13_2_right)

def updateViews_21():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_21.setGeometry(plot21.vb.sceneBoundingRect())  # Align geometrically

def adjust_right_view_21():
    """Dynamically adjust the range of the right Y-axis for plot21."""
    if y13_2:
        vb_right_21.setRange(yRange=(min(y13_2), max(y13_2)), padding=0.1)  # Independent Y-scaling

plot21.vb.sigResized.connect(updateViews_21)

# For plot22
vb_right_22 = pg.ViewBox()
plot22.showAxis('right')
plot22.scene().addItem(vb_right_22)
plot22.getAxis('right').setLabel("Right Y-Axis")
vb_right_22.setXLink(plot22)  # Keep X-axis linked for alignment
line_13_3_right = pg.PlotDataItem(pen=mkPen('m', width=2))
vb_right_22.addItem(line_13_3_right)

def updateViews_22():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_22.setGeometry(plot22.vb.sceneBoundingRect())  # Align geometrically

def adjust_right_view_22():
    """Dynamically adjust the range of the right Y-axis for plot22."""
    if y13_3:
        vb_right_22.setRange(yRange=(min(y13_3), max(y13_3)), padding=0.1)  # Independent Y-scaling

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

# --------------- Update Function ---------------
i = 0

def update():
    global i

    # Update Expiry 1
    y0_1.append(dfp.iloc[0,0][i])
    y1_1.append(dfp.iloc[1,0][i])
    y10_1.append(dfp.iloc[10,0][i])
    y11_1.append(dfp.iloc[11,0][i])
    y12_1.append(dfp.iloc[12,0][i])
    y6_1.append(dfp.iloc[6,0][i])
    y7_1.append(dfp.iloc[7,0][i])
    y13_1.append(dfp.iloc[13,0][i])

    line_0_1.setData(y0_1)
    line_1_1.setData(y1_1)
    line_10_1.setData(y10_1)
    line_11_1.setData(y11_1)
    line_12_1.setData(y12_1)
    line_6_1.setData(y6_1)
    line_7_1.setData(y7_1)
    # line_13_1.setData(y13_1)
    line_13_1_right.setData(list(range(len(y13_1))), y13_1)
    adjust_right_view_20()

    # Update Expiry 2
    y0_2.append(dfp.iloc[0,3][i])
    y1_2.append(dfp.iloc[1,3][i])
    y10_2.append(dfp.iloc[10,3][i])
    y11_2.append(dfp.iloc[11,3][i])
    y12_2.append(dfp.iloc[12,3][i])
    y6_2.append(dfp.iloc[6,3][i])
    y7_2.append(dfp.iloc[7,3][i])
    y13_2.append(dfp.iloc[13,3][i])

    line_0_2.setData(y0_2)
    line_1_2.setData(y1_2)
    line_10_2.setData(y10_2)
    line_11_2.setData(y11_2)
    line_12_2.setData(y12_2)
    line_6_2.setData(y6_2)
    line_7_2.setData(y7_2)
    # line_13_2.setData(y13_2)
    line_13_2_right.setData(list(range(len(y13_2))), y13_2)
    adjust_right_view_21()

    # Update Expiry 3
    y0_3.append(dfp.iloc[0,4][i])
    y1_3.append(dfp.iloc[1,4][i])
    y10_3.append(dfp.iloc[10,4][i])
    y11_3.append(dfp.iloc[11,4][i])
    y12_3.append(dfp.iloc[12,4][i])
    y6_3.append(dfp.iloc[6,4][i])
    y7_3.append(dfp.iloc[7,4][i])
    y13_3.append(dfp.iloc[13,4][i])

    line_0_3.setData(y0_3)
    line_1_3.setData(y1_3)
    line_10_3.setData(y10_3)
    line_11_3.setData(y11_3)
    line_12_3.setData(y12_3)
    line_6_3.setData(y6_3)
    line_7_3.setData(y7_3)
    # line_13_3.setData(y13_3)
    line_13_3_right.setData(list(range(len(y13_3))), y13_3)
    adjust_right_view_22()

    # Update Labels
    if y0_1:
        label_dict['label_0'].setText(f"{y0_1[-1]:.2f}")
        label_dict['label_0'].setPos(len(y0_1), y0_1[-1])
        label_dict['label_1'].setText(f"{y1_1[-1]:.2f}")
        label_dict['label_1'].setPos(len(y1_1), y1_1[-1])
        label_dict['label_10'].setText(f"{y10_1[-1]:.2f}")
        label_dict['label_10'].setPos(len(y10_1), y10_1[-1])
        label_dict['label_11'].setText(f"{y11_1[-1]:.2f}")
        label_dict['label_11'].setPos(len(y11_1), y11_1[-1])
        label_dict['label_12'].setText(f"{y12_1[-1]:.2f}")
        label_dict['label_12'].setPos(len(y12_1), y12_1[-1])
        label_dict['label_6'].setText(f"{y6_1[-1]:.2f}")
        label_dict['label_6'].setPos(len(y6_1), y6_1[-1])
        label_dict['label_7'].setText(f"{y7_1[-1]:.2f}")
        label_dict['label_7'].setPos(len(y7_1), y7_1[-1])
        label_dict['label_13'].setText(f"{y13_1[-1]:.2f}")
        label_dict['label_13'].setPos(len(y13_1), y13_1[-1])

        label_dict['label_0_2'].setText(f"{y0_2[-1]:.2f}")
        label_dict['label_0_2'].setPos(len(y0_2), y0_2[-1])
        label_dict['label_1_2'].setText(f"{y1_2[-1]:.2f}")
        label_dict['label_1_2'].setPos(len(y1_2), y1_2[-1])
        label_dict['label_10_2'].setText(f"{y10_2[-1]:.2f}")
        label_dict['label_10_2'].setPos(len(y10_2), y10_2[-1])
        label_dict['label_11_2'].setText(f"{y11_2[-1]:.2f}")
        label_dict['label_11_2'].setPos(len(y11_2), y11_2[-1])
        label_dict['label_12_2'].setText(f"{y12_2[-1]:.2f}")
        label_dict['label_12_2'].setPos(len(y12_2), y12_2[-1])
        label_dict['label_6_2'].setText(f"{y6_2[-1]:.2f}")
        label_dict['label_6_2'].setPos(len(y6_2), y6_2[-1])
        label_dict['label_7_2'].setText(f"{y7_2[-1]:.2f}")
        label_dict['label_7_2'].setPos(len(y7_2), y7_2[-1])
        label_dict['label_13_2'].setText(f"{y13_2[-1]:.2f}")
        label_dict['label_13_2'].setPos(len(y13_2), y13_2[-1])

        label_dict['label_0_3'].setText(f"{y0_3[-1]:.2f}")
        label_dict['label_0_3'].setPos(len(y0_3), y0_3[-1])
        label_dict['label_1_3'].setText(f"{y1_3[-1]:.2f}")
        label_dict['label_1_3'].setPos(len(y1_3), y1_3[-1])
        label_dict['label_10_3'].setText(f"{y10_3[-1]:.2f}")
        label_dict['label_10_3'].setPos(len(y10_3), y10_3[-1])
        label_dict['label_11_3'].setText(f"{y11_3[-1]:.2f}")
        label_dict['label_11_3'].setPos(len(y11_3), y11_3[-1])
        label_dict['label_12_3'].setText(f"{y12_3[-1]:.2f}")
        label_dict['label_12_3'].setPos(len(y12_3), y12_3[-1])
        label_dict['label_6_3'].setText(f"{y6_3[-1]:.2f}")
        label_dict['label_6_3'].setPos(len(y6_3), y6_3[-1])
        label_dict['label_7_3'].setText(f"{y7_3[-1]:.2f}")
        label_dict['label_7_3'].setPos(len(y7_3), y7_3[-1])
        label_dict['label_13_3'].setText(f"{y13_3[-1]:.2f}")
        label_dict['label_13_3'].setPos(len(y13_3), y13_3[-1])

    x_max = max(len(y0_1), len(y0_2), len(y0_3))  # based on all 3 expiry lengths
    for plot in [plot00, plot10, plot20, plot01, plot11, plot21, plot02, plot12, plot22]:
        plot.setXRange(0, x_max, padding=0.1)

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

# Run app
app.exec_()