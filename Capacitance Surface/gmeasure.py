
from pydwf import DwfLibrary, DwfAnalogOutNode, DwfAnalogOutFunction
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from scipy.signal import correlate
import pandas as pd

dwf = DwfLibrary()


class GMeasure:
    def __init__(self, osc_channels1=None, osc_channels2=None,
                 out_channels1=None, out_channels2=None, ad_2=1,
                 v_out1=None, v_out2=None, waveforms_1=None, waveforms_2=None,
                 freq1=None, freq2=None, wavelengths=1, offset1=None, offset2=None, supply =None,
                 duration=1.0, sfreq=1e6, nbuf=8192, tsleep = None, prefer_first_device=None, wave_shape = 0):
        
        self.osc_channels1 = osc_channels1 or [0, 0]
        self.osc_channels2 = osc_channels2 or [0, 0]
        self.out_channels1 = out_channels1 or [0, 0]
        self.out_channels2 = out_channels2 or [0, 0]
        self.ad_2 = ad_2
        self.v_out1 = v_out1 or [1, 1]
        self.v_out2 = v_out2 or [1, 1]
        self.waveforms_1 = waveforms_1 or ["DC", "DC"]
        self.waveforms_2 = waveforms_2 or ["DC", "DC"]
        self.freq1 = freq1 or [1000, 1000]
        self.freq2 = freq2 or [1000, 1000]
        self.wavelengths = wavelengths
        self.offset1 = offset1 or [0, 0]
        self.offset2 = offset2 or [0, 0]
        self.supply = supply or [0,0]
        self.sfreq = sfreq
        self.nbuf = nbuf
        self.duration = duration
        self.tsleep = tsleep or 1
        self.response = None
        if type(wave_shape) != np.ndarray:
            print("Not identified as array")
            self.wave_shape = np.ones((1,100))
        else:
            self.wave_shape = wave_shape

        if freq1 != None:
            time_window = 1 / freq1[0]
            self.sfreq =  nbuf / (time_window*wavelengths)

        self.prefer_first_device = prefer_first_device

        if self.ad_2 == 2:
            self._detect_dual_devices()
        self.t = np.arange(self.nbuf)/self.sfreq

    def _detect_dual_devices(self):
        device_count = dwf.deviceEnum.enumerateDevices()
        if device_count < 2:
            raise RuntimeError("Two AD2 devices expected but less than two detected.")

        serials = [dwf.deviceEnum.serialNumber(i) for i in range(device_count)]
        print("Detected Devices:")
        for i, s in enumerate(serials):
            print(f"  Device {i}: Serial {s}")

        # --- NEW BEHAVIOR: skip prompt if boolean was provided ---
        if self.prefer_first_device is not None:
            if self.prefer_first_device:
                self.dev1_index, self.dev2_index = 0, 1
            else:
                self.dev1_index, self.dev2_index = 1, 0
            print(f"→ Device 1: {serials[self.dev1_index]} | Device 2: {serials[self.dev2_index]}")
            return
        # ---------------------------------------------------------

        # Original interactive prompt
        response = input(f"Is serial {serials[0]} your AD2 device 1? (y/n): ").strip().lower()
        if response == "y":
            self.dev1_index, self.dev2_index = 0, 1
            self.response = True
        else:
            self.dev1_index, self.dev2_index = 1, 0
            self.response =False

        print(f"→ Device 1: {serials[self.dev1_index]} | Device 2: {serials[self.dev2_index]}")




    def setup_run1(self,dev,i):
        waveform = self.waveforms_1[i]
        dev.analogOut.reset(i)
        print(str(dev.analogOut.modeGet(i)))
        dev.analogOut.nodeEnableSet  (i, DwfAnalogOutNode.Carrier, True)
        if waveform == "DC":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.DC)
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.v_out1[i])
            print("Outputting DC")
        elif waveform == "Sine":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Sine)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out1[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq1[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset1[i])
        elif waveform == "Square":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Square)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out1[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq1[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset1[i])
        elif waveform == "Costum":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Custom)
            dev.analogOut.nodeDataSet(i, DwfAnalogOutNode.Carrier, self.wave_shape)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out1[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq1[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset1[i])

    def setup_run2(self,dev,i):
        waveform = self.waveforms_2[i]
        dev.analogOut.reset(i)
        print(str(dev.analogOut.modeGet(i)))
        dev.analogOut.nodeEnableSet  (i, DwfAnalogOutNode.Carrier, True)
        if waveform == "DC":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.DC)
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.v_out2[i])
        elif waveform == "Sine":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Sine)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out2[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq2[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset2[i])
        elif waveform == "Square":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Square)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out2[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq2[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset2[i])
        elif waveform == "Costum":
            dev.analogOut.nodeFunctionSet(i, DwfAnalogOutNode.Carrier, DwfAnalogOutFunction.Custom)
            dev.analogOut.nodeDataSet(i, DwfAnalogOutNode.Carrier, self.wave_shape)
            dev.analogOut.nodeAmplitudeSet(i, DwfAnalogOutNode.Carrier, self.v_out2[i])
            dev.analogOut.nodeFrequencySet(i, DwfAnalogOutNode.Carrier, self.freq2[i])
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, self.offset2[i])


    def stop_run(self, dev, i):
            dev.analogOut.nodeOffsetSet(i, DwfAnalogOutNode.Carrier, 0.0)
            dev.analogOut.nodeEnableSet(i, DwfAnalogOutNode.Carrier, False)
            dev.analogOut.configure(i, False)
    
    def power_supply(self, dev):
        dev.analogIO.enableSet(True)
        dev.analogIO.channelNodeSet(0,0,True)
        dev.analogIO.channelNodeSet(0,1,5.0)
        dev.analogIO.channelNodeSet(1,0,True)
        dev.analogIO.channelNodeSet(1,1,-5.0)
        dev.analogIO.configure()

    def power_supply_off(self,dev):
        dev.analogIO.channelNodeSet(0,1,0)
        dev.analogIO.channelNodeSet(1,1,0)
        dev.analogIO.configure()


    # ---------- DATA COLLECTION ----------
    def collect_data1(self, dev):
        """Collect data from active channels defined in out_channels1."""
        dev.analogIn.frequencySet(self.sfreq)
        buf_min, buf_max = dev.analogIn.bufferSizeInfo()
        buf = min(buf_max, self.nbuf)
        dev.analogIn.bufferSizeSet(buf)

        # Enable and set ranges only for active channels
        for i, active in enumerate(self.osc_channels1):
            if active:
                dev.analogIn.channelEnableSet(i, True)
                dev.analogIn.channelRangeSet(i, 10.0)
            else:
                dev.analogIn.channelEnableSet(i, False)

        # Start recording
        dev.analogIn.configure(False, True)

        # Wait until acquisition is done
        while dev.analogIn.status(True).name != "Done":
            time.sleep(0.001)

        valid = dev.analogIn.statusSamplesValid()
        n = int(min(valid, buf))
        if n <= 0:
            raise RuntimeError("No valid samples captured.")

        print(f"Collected {n} samples from active channels in out_channels1.")

        # Return dictionary of collected channel data
        data = {}
        for i, active in enumerate(self.osc_channels1):
            if active:
                data[i] = dev.analogIn.statusData(i, n)

        return data

    def collect_data2(self, dev):
        """Collect data from active channels defined in out_channels2."""
        dev.analogIn.frequencySet(self.sfreq)
        buf_min, buf_max = dev.analogIn.bufferSizeInfo()
        buf = min(buf_max, self.nbuf)
        dev.analogIn.bufferSizeSet(buf)

        # Enable and set ranges only for active channels
        for i, active in enumerate(self.osc_channels2):
            if active:
                dev.analogIn.channelEnableSet(i, True)
                dev.analogIn.channelRangeSet(i, 10.0)
            else:
                dev.analogIn.channelEnableSet(i, False)

        # Start recording
        dev.analogIn.configure(False, True)

        while dev.analogIn.status(True).name != "Done":
            time.sleep(0.001)

        valid = dev.analogIn.statusSamplesValid()
        n = int(min(valid, buf))
        if n <= 0:
            raise RuntimeError("No valid samples captured.")

        print(f"Collected {n} samples from active channels in out_channels2.")

        data = {}
        for i, active in enumerate(self.osc_channels2):
            if active:
                data[i] = dev.analogIn.statusData(i, n)

        return data
    def on(self, tsleep):
        with dwf.deviceControl.open(-1) as dev:
            for i in range(2):
                if self.out_channels1[i] == 1:
                    self.setup_run1(dev,i)
                    dev.analogOut.configure(i, True)
            time.sleep(tsleep)
            for i, active in enumerate(self.out_channels1):
                if active:
                    self.stop_run(dev, i)

    def measure1(self):
        with dwf.deviceControl.open(-1) as dev:
            if self.supply[0] == True:
                        self.power_supply(dev)
            for i in range(2):
                if self.out_channels1[i] == 1:
                    self.setup_run1(dev,i)
                    dev.analogOut.configure(i, True)
            time.sleep(0.1)
            self.data1 = self.collect_data1(dev)
            for i, active in enumerate(self.out_channels1):
                if active:
                    self.stop_run(dev, i)
            if self.supply[0] == True:
                        self.power_supply_off(dev)

    def measure2_original(self):
        """Measure using two devices simultaneously."""
        if self.ad_2 != 2:
            raise RuntimeError("measure2 requires ad_2=2 (dual devices).")

        with dwf.deviceControl.open(self.dev1_index) as dev1:
            with dwf.deviceControl.open(self.dev2_index) as dev2:
                # Setup outputs
                if self.supply[0] == True:
                        self.power_supply(dev1)
                if self.supply[1] == True:
                        self.power_supply(dev2)
                for i, active in enumerate(self.out_channels1):
                    if active:
                        self.setup_run1(dev1, i)
                        dev1.analogOut.configure(i, True)
                for i, active in enumerate(self.out_channels2):
                    if active:
                        self.setup_run2(dev2, i)
                        dev2.analogOut.configure(i, True)

                time.sleep(0.5)
                # Collect data
                self.data1 = self.collect_data1(dev1)
                self.data2 = self.collect_data2(dev2)

                # Stop outputs
                for i, active in enumerate(self.out_channels1):
                    if active:
                        self.stop_run(dev1, i)
                for i, active in enumerate(self.out_channels2):
                    if active:
                        self.stop_run(dev2, i)
                
                if self.supply[0] == True:
                        self.power_supply_off(dev1)
                if self.supply[1] == True:
                        self.power_supply_off(dev2)
    
    def measure2(self):
        i = 0
        for i in range(0,5):
            try:
                self.measure2_original()
                break
            except:
                i += 1
                pass
        if i == 5:
            raise TypeError("Connection Error")