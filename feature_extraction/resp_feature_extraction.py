import scipy.io as scio;
from scipy import interpolate;
from config import AlgorithmFolder;
import matplotlib.pyplot as plt;
import pandas as pd;
import numpy as np;
from datafromdataset import datafromdataset;
from signal_filter import *;
import pywt;
import copy;

from ecg_quality import singal_normalize;


# def respsignal_peak(respsignal,windowlen=300,windowlimit=150,rvaluelimit=10):
# 	respsignallen=len(respsignal);
# 	peak_sequence=[];
# 	windownum=0;
# 	while((windownum+1)*windowlen<respsignallen):
# 		peak=respsignal[windownum*windowlen:(windownum+1)*windowlen].idxmax();
# 		if len(peak_sequence)==0 and respsignal[peak]>rvaluelimit:
# 			peak_sequence.append(peak);
# 		elif len(peak_sequence)>0 and peak-peak_sequence[-1]>windowlimit and respsignal[peak]>rvaluelimit:
# 			peak_sequence.append(peak);
# 		elif len(peak_sequence)>0 and peak-peak_sequence[-1]<windowlimit and respsignal[peak]>respsignal[peak_sequence[-1]] and respsignal[peak]>rvaluelimit:
# 			peak_sequence[-1]=peak;
# 		windownum=windownum+1;

# 	return peak_sequence;

# def respsignal_peak(respsignal,windowlen=300,windowlimit=150,rvaluelimit=0.02):
# 	w = pywt.Wavelet('sym3');
# 	cD2=[];
# 	cA3,cD3,cD2,cD1=pywt.wavedec(respsignal,wavelet=w,mode='cpd',level=3);
# 	cD2=np.interp(np.linspace(0,1,len(respsignal)),np.linspace(0,1,len(cD2)),cD2);
# 	windownum=0;
# 	cD2len=len(cD2);
# 	cD2=pd.Series(cD2,index=range(respsignal.index.min(),respsignal.index.max()+1));
# 	cD2=-cD2;
# 	peak_sequence=[];
# 	try:
# 		while((windownum+1)*windowlen<cD2len):
# 			ridx=cD2[windownum*windowlen:(windownum+1)*windowlen].idxmax();
# 			sridx=ridx;
# 			sridx=respsignal[range(ridx-windowlimit,ridx+windowlimit)].idxmax();
# 			if len(peak_sequence)==0 and cD2[ridx]>rvaluelimit:
# 				peak_sequence.append(sridx);
# 			elif len(peak_sequence)>0 and sridx-peak_sequence[-1]>windowlimit and cD2[ridx]>rvaluelimit:
# 				peak_sequence.append(sridx);
# 			elif len(peak_sequence)>0 and sridx-peak_sequence[-1]<windowlimit and cD2[ridx]>cD2[peak_sequence[-1]] and cD2[ridx]>rvaluelimit:
# 				peak_sequence[-1]=sridx;
# 			windownum=windownum+1;
# 	except Exception,e:  
# 		print(respsignal.index.min());
# 		print(respsignal.index.max());
# 	return peak_sequence;

def respsignal_peak(respsignal,windowlen=300,windowlimit=150,rvaluelimit=0.02):
	respsignal=pd.Series(low_pass_filter(respsignal.values,2),respsignal.index);
	w = pywt.Wavelet('sym3');
	cD2=[];
	cA3,cD3,cD2,cD1=pywt.wavedec(respsignal,wavelet=w,mode='cpd',level=3);
	cD2=np.interp(np.linspace(0,1,len(respsignal)),np.linspace(0,1,len(cD2)),cD2);
	windownum=0;
	cD2len=len(cD2);
	cD2=pd.Series(cD2,index=range(respsignal.index.min(),respsignal.index.max()+1));
	cD2=-cD2;
	peak_sequence=[];
	startpoint=respsignal.index.min();
	try:
		while(startpoint+windowlen<respsignal.index.max()):
			# ridx=cD2[startpoint:startpoint+windowlen].idxmax();
			ridx=cD2[range(startpoint,startpoint+windowlen)].idxmax();
			sridx=ridx;
			temps=ridx-windowlimit;
			if temps<respsignal.index.min():
				temps=respsignal.index.min();
			tempe=ridx+windowlimit;
			if tempe>respsignal.index.max():
				tempe=respsignal.index.max();
			sridx=respsignal[range(temps,tempe)].idxmax();
			if len(peak_sequence)==0 and cD2[ridx]>rvaluelimit:
				peak_sequence.append(sridx);
			elif len(peak_sequence)>0 and sridx-peak_sequence[-1]>windowlimit and cD2[ridx]>rvaluelimit:
				peak_sequence.append(sridx);
			elif len(peak_sequence)>0 and sridx-peak_sequence[-1]<windowlimit and cD2[ridx]>cD2[peak_sequence[-1]] and cD2[ridx]>rvaluelimit:
				peak_sequence[-1]=sridx;
			startpoint=sridx+windowlimit+10;
	except Exception,e:  
		print(e);
		print(respsignal.index.min());
		print(respsignal.index.max());
	return peak_sequence;

def resppeak_value(respsignal,windowlen=300,windowlimit=150,rvaluelimit=10):
	peak_sequence=respsignal_peak(respsignal);
	resultlist=[];
	for i in peak_sequence:
		resultlist.append(i);
	return resultlist;

def resppeak_avg(peakvalue_sequence):
	squencelen=len(peakvalue_sequence);
	resultlist=[];
	if squencelen<1:
		return [0];
	resppeakavg=1.0*sum(peakvalue_sequence)/squencelen;
	resultlist.append(resppeakavg);
	return resultlist;

def resppeak_num(peakvalue_sequence):
	squencelen=len(peakvalue_sequence);
	if squencelen<5 or squencelen>20:
		print(squencelen);
	resultlist=[];
	resultlist.append(squencelen);
	return resultlist;

def resppeak_stdev(peakvalue_sequence):
	squencelen=len(peakvalue_sequence);
	resultlist=[];
	if squencelen<1:
		return [0];
	resppeakavg=1.0*sum(peakvalue_sequence)/squencelen;
	sdsq=sum([(i-resppeakavg)**2 for i in peakvalue_sequence]);
	stdev=(sdsq/squencelen)**0.5;
	resultlist.append(stdev);
	return resultlist;

def resp_power(respsignal,resamplerate=8):
	tck = interpolate.splrep(np.arange(0,len(respsignal),1),respsignal, s=0);
	respsignal_resample= interpolate.splev(np.arange(0,len(respsignal),1.0*128/resamplerate), tck, der=0);
	respfft=np.fft.fft(respsignal_resample);
	resppower=respfft*respfft;
	return resppower;

# def resppower_sum00101(respsignal,resamplerate=8):
# 	resultlist=[];
# 	resppower=resp_power(respsignal,resamplerate);
# 	startposition=int(len(resppower)*0.01/resamplerate);
# 	endposition=int(len(resppower)*0.1/resamplerate);
# 	powersum=1.0*sum(abs(resppower[startposition:endposition]));
# 	resultlist.append(np.log10(powersum*powersum));
# 	return resultlist;
def resppower_sum001005(respsignal,resamplerate=8):
	resultlist=[];
	resppower=resp_power(respsignal,resamplerate);
	startposition=int(len(resppower)*0.01/resamplerate);
	endposition=int(len(resppower)*0.05/resamplerate);
	powersum=1.0*sum(abs(resppower[startposition:endposition]));
	resultlist.append(np.log10(powersum*powersum));
	return resultlist;

def resppower_sum005015(respsignal,resamplerate=8):
	resultlist=[];
	resppower=resp_power(respsignal,resamplerate);
	startposition=int(len(resppower)*0.05/resamplerate);
	endposition=int(len(resppower)*0.15/resamplerate);
	powersum=1.0*sum(abs(resppower[startposition:endposition]));
	resultlist.append(np.log10(powersum*powersum));
	return resultlist;

def resppower_sum01505(respsignal,resamplerate=8):
	resultlist=[];
	resppower=resp_power(respsignal,resamplerate);
	startposition=int(len(resppower)*0.15/resamplerate);
	endposition=int(len(resppower)*0.5/resamplerate);
	powersum=1.0*sum(abs(resppower[startposition:endposition]));
	resultlist.append(np.log10(powersum*powersum));
	return resultlist;

def resppower_lfhf(respsignal,resamplerate=8):
	resultlist=[];
	lfpower=resppower_sum005015(respsignal,resamplerate);
	hfpower=resppower_sum01505(respsignal,resamplerate);
	if lfpower!=0:
		resultlist.append(lfpower[0]/hfpower[0]);
	else:
		resultlist.append(0);
	return resultlist;

if __name__=='__main__':
	respsignal=datafromdataset('ucddb003_recm','abdo',range(1380000,1400000));
	resppower001005=resppower_sum001005(respsignal);
	resppower005015=resppower_sum005015(respsignal);
	resppower01505=resppower_sum01505(respsignal);
	print(resppower001005);
	print(resppower005015);
	print(resppower01505);
	print(resppower_lfhf(respsignal));
	# #plt.plot(respsignal);
	# # w = pywt.Wavelet('sym3');
	# # cD2=[];
	# # cA1,cD1=pywt.wavedec(respsignal,wavelet=w,mode='cpd',level=1);
	# # cD1=np.interp(np.linspace(0,1,len(respsignal)),np.linspace(0,1,len(cD1)),cD1);
	# #respsignal=median_filter(respsignal);
	# w = pywt.Wavelet('sym3');
	# cD2=[];
	
	# respsignal=pd.Series(low_pass_filter(respsignal.values,2),respsignal.index);
	# cA3,cD3,cD2,cD1=pywt.wavedec(respsignal,wavelet=w,mode='cpd',level=3);
	# cD2=np.interp(np.linspace(0,1,len(respsignal)),np.linspace(0,1,len(cD2)),cD2);
	# plt.subplot(3,1,1);
	# plt.plot(cD2);
	# plt.subplot(3,1,2);
	# plt.plot(respsignal);
	# plt.subplot(3,1,3);
	# #respsignal=median_filter(respsignal);

	# #respsignal=pd.Series(low_pass_filter(respsignal.values,2),respsignal.index);
	
	# #respsignal=pd.Series(median_filter(respsignal.values,2),respsignal.index);
	# rpeak=respsignal_peak(respsignal);
	# print(rpeak);
	# for i in rpeak:
	# 	plt.plot(i,respsignal[i],'ro');
	# # # plt.plot(ecgsignal);
	# # plt.subplot(2,1,1);
	# plt.plot(respsignal);
	# # plt.subplot(2,1,2);
	# # plt.plot(cD1);
	# plt.show();
	# # peakvalue_sequence=resppeak_value(respsignal);
	# # print(peakvalue_sequence);

