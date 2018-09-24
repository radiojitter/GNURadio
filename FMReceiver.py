#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: RTL SDR FM Receiver
# Author: Arnav Mukhopadhyay (RadioJitter)
# Generated: Mon Sep 24 14:42:49 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class FMReceiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="RTL SDR FM Receiver")
        _icon_path = "C:\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.logvol = logvol = 0
        self.freq = freq = 104
        self.vol = vol = pow(10,logvol/10)
        self.samp_rate = samp_rate = int(2e6)
        self.gain = gain = 32
        self.freq_rtl = freq_rtl = freq*1e6

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='Gain (dB):',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=48,
        	num_steps=480,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=freq_rtl,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq_rtl,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/5,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.32,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq_rtl, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
        	  5,
        	  (firdes.low_pass(1,samp_rate,200e3,400e3)),
        	  0,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)

        self.low_pass_filter_0 = filter.fir_filter_fff(10, firdes.low_pass(
        	1, samp_rate/5, 16e3, 40e3, firdes.WIN_HAMMING, 6.76))
        _logvol_sizer = wx.BoxSizer(wx.VERTICAL)
        self._logvol_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_logvol_sizer,
        	value=self.logvol,
        	callback=self.set_logvol,
        	label='Volume Control (dB):',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._logvol_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_logvol_sizer,
        	value=self.logvol,
        	callback=self.set_logvol,
        	minimum=-10,
        	maximum=10,
        	num_steps=500,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_logvol_sizer)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Frequency (MHz):',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=88,
        	maximum=108,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sizer)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(vol)
        self.audio_sink_0 = audio.sink(40000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate/5,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.pfb_decimator_ccf_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.pfb_decimator_ccf_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

    def get_logvol(self):
        return self.logvol

    def set_logvol(self, logvol):
        self.logvol = logvol
        self.set_vol(pow(10,self.logvol/10))
        self._logvol_slider.set_value(self.logvol)
        self._logvol_text_box.set_value(self.logvol)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_rtl(self.freq*1e6)
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)

    def get_vol(self):
        return self.vol

    def set_vol(self, vol):
        self.vol = vol
        self.blocks_multiply_const_xx_0.set_k(self.vol)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate/5)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.pfb_decimator_ccf_0.set_taps((firdes.low_pass(1,self.samp_rate,200e3,400e3)))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/5, 16e3, 40e3, firdes.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.rtlsdr_source_0.set_gain(self.gain, 0)

    def get_freq_rtl(self):
        return self.freq_rtl

    def set_freq_rtl(self, freq_rtl):
        self.freq_rtl = freq_rtl
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.freq_rtl)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq_rtl)
        self.rtlsdr_source_0.set_center_freq(self.freq_rtl, 0)


def main(top_block_cls=FMReceiver, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
