#needs: - numpy (conda install numpy or pip install numpy)
#       - pyqtgraph (conda install pyqtgraph or pip install pyqtpgraph)   
# written with help from chatgpt.


import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

# ---------------- Parameters ----------------
T = 0.1         # signal duration (seconds)
N_CONT = 50000   # "continuous" resolution

# ---------------- Qt App ----------------
app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication([])

# ---------------- Main window ----------------
win = pg.GraphicsLayoutWidget(title="Aliasing Demonstration (Time + FFT)")
win.resize(1000, 700)
win.show()

# ---------------- Plots ----------------
time_plot = win.addPlot(title="Time Domain")
time_plot.setLabel("bottom", "Time", units="s")
time_plot.setLabel("left", "Amplitude")
time_plot.addLegend()

win.nextRow()

freq_plot = win.addPlot(title="Frequency Domain (FFT)")
freq_plot.setLabel("bottom", "Frequency", units="Hz")
freq_plot.setLabel("left", "Magnitude")
freq_plot.addLegend()

# ---------------- Plot items ----------------
cont_curve = time_plot.plot(pen=pg.mkPen('b', width=1), name="Original")
samp_curve = time_plot.plot(
    pen=None, symbol='o', symbolSize=7, symbolBrush='r',
    name="Samples"
)

fft_curve = freq_plot.plot(pen=pg.mkPen('g', width=2), name="FFT")
nyquist_line = pg.InfiniteLine(angle=90, pen=pg.mkPen('b', style=QtCore.Qt.DotLine))
freq_plot.addItem(nyquist_line)

sampling_line = pg.InfiniteLine(angle=90, pen=pg.mkPen('b', style=QtCore.Qt.DotLine))
freq_plot.addItem(sampling_line)

true_freq_line = pg.InfiniteLine(
    angle=90,
    pen=pg.mkPen('r', width=2, style=QtCore.Qt.DashLine)
)
freq_plot.addItem(true_freq_line)

nyquist_label = pg.TextItem(color='b')
freq_plot.addItem(nyquist_label)

sampling_label = pg.TextItem(color='b')
freq_plot.addItem(sampling_label)

true_freq_label = pg.TextItem(color='r')
freq_plot.addItem(true_freq_label)

# ---------------- Sliders ----------------
ctrl_win = QtWidgets.QWidget()
ctrl_layout = QtWidgets.QFormLayout(ctrl_win)

f_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
f_slider.setRange(1, 100000)
f_slider.setValue(1000)

fs_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
fs_slider.setRange(10, 50000)
fs_slider.setValue(20000)

ctrl_layout.addRow("Signal frequency (Hz)", f_slider)
ctrl_layout.addRow("Sampling rate (Hz)", fs_slider)

ctrl_win.setWindowTitle("Controls")
ctrl_win.show()

time_plot.setXRange(0, 0.001)
freq_plot.setXRange(-60e3, 60e3)
# ---------------- Update function ----------------
def update():
    f = f_slider.value()
    fs = fs_slider.value()

    # Time axes
    t_cont = np.linspace(0, T, N_CONT)
    t_samp = np.arange(0, T, 1/fs)

    # Signals
    x_cont = np.sin(2 * np.pi * f * t_cont)
    x_samp = np.sin(2 * np.pi * f * t_samp)

    # FFT
    X = np.fft.fft(x_samp)
    freqs = np.fft.fftfreq(len(X), 1/fs)

    # Update plots
    cont_curve.setData(t_cont, x_cont)
    samp_curve.setData(t_samp, x_samp)
    fft_curve.setData(freqs, np.abs(X))
    

    # Nyquist line
    nyquist_line.setValue(fs / 2)
    sampling_line.setValue(fs)
    true_freq_line.setValue(f)

    # Plot limits

    true_freq_label.setText(f"f = {f} Hz")
    true_freq_label.setPos(f, freq_plot.viewRange()[1][1] * 0.9)
    
    
    sampling_label.setText(f"fs = {fs} Hz")
    sampling_label.setPos(fs, freq_plot.viewRange()[1][1] * 0.9)
    
    nyquist_label.setText(f"fs/2 = {fs/2} Hz")
    nyquist_label.setPos(fs/2, freq_plot.viewRange()[1][1] * 0.9)

# ---------------- Connect sliders ----------------
f_slider.valueChanged.connect(update)
fs_slider.valueChanged.connect(update)

# Initial draw
update()

pg.exec()
