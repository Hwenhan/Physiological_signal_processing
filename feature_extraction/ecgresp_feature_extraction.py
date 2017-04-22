import scipy.io as scio;
from scipy import interpolate;
from config import AlgorithmFolder;
import matplotlib.pyplot as plt;
import pandas as pd;
import numpy as np;
from datafromdataset import datafromdataset;
import pywt;
import copy;
from ecg_feature_extraction import *;
from pandas.tseries.offsets import Micro,Nano;
import math;

def  signal_resample(inputsignal,sourcesample,targetsample):
	sampletime=Nano(1000000000/sourcesample);
	signallen=len(inputsignal);
	rng=pd.date_range('1/1/2000',periods=signallen,freq=sampletime);
	ts=pd.Series(inputsignal,index=rng);
	resampletime=Nano(1000000000/targetsample);
	resultlist=ts.resample(resampletime).mean();
	return resultlist.values;


def  cpc_RRinternalresp(RRinternal,resp,samplerate=128,resamplerate=4):
	respsignal_resample=signal_resample(resp.values,samplerate,resamplerate);
	tck = interpolate.splrep(np.arange(0,np.size(RRinternal),1),RRinternal, s=0)
	RR_squence_resample= interpolate.splev(np.arange(0,1.0*np.size(respsignal_resample)/resamplerate,0.25), tck, der=0);

	RRinternalfou=np.fft.fft(RR_squence_resample);
	respfou=np.fft.fft(respsignal_resample);
	crossRRresp=RRinternalfou*respfou;
	CPCsection=crossRRresp*crossRRresp*crossRRresp*crossRRresp/(RRinternalfou*RRinternalfou)/(respfou*respfou);
	return abs(CPCsection);

def cpc_001_01_avg(RRinternal,resp,samplerate=128,resamplerate=4):
	samplenum=len(resp)/samplerate*resamplerate;
	startposition=int(samplenum*0.01/resamplerate);
	endposition=int(samplenum*0.1/resamplerate);
	cpcsection=cpc_RRinternalresp(RRinternal,resp,samplerate,resamplerate);
	resultlist=[];
	resultlist.append(math.log10(1.0*sum(cpcsection[startposition:endposition])/(endposition-startposition)));
	return resultlist;

def cpc_01_04_avg(RRinternal,resp,samplerate=128,resamplerate=4):
	samplenum=len(resp)/samplerate*resamplerate;
	startposition=int(samplenum*0.1/resamplerate);
	endposition=int(samplenum*0.4/resamplerate);
	cpcsection=cpc_RRinternalresp(RRinternal,resp,samplerate,resamplerate);
	resultlist=[];
	resultlist.append(math.log10(1.0*sum(cpcsection[startposition:endposition])/(endposition-startposition)));
	return resultlist;

def cpc_lfhf(RRinternal,resp,samplerate=128,resamplerate=4):
	resultlist=[];
	lfpower=cpc_001_01_avg(RRinternal,resp);
	hfpower=cpc_01_04_avg(RRinternal,resp);
	if hfpower[0]!=0:
		resultlist.append(lfpower[0]/hfpower[0]);
	else:
		resultlist.append(0);
	return resultlist;


if __name__=='__main__':
	respsignal=datafromdataset('ucddb022_recm','abdo',range(10000,3000000));
	ecgsignal=datafromdataset('ucddb022_recm','ecg',range(10000,3000000));
	#RR_squence=RRinternal(ecgsignal,100,50);
	
	plt.plot(respsignal);
	plt.show();
	# cpcsection=cpc_RRinternalresp(RR_squence,respsignal);
	# plt.plot(cpcsection[1:10000]);
	# fftvalue=np.fft.fft(RR_squence);
	#plt.plot(abs(fftvalue[0:300]));
	# plt.subplot(2,2,1);
	# plt.plot(respsignal);
	# respsignal_resample=signal_resample(respsignal.values,128,4);
	# plt.subplot(2,2,2);
	# plt.plot(respsignal_resample);
	# plt.subplot(2,2,3);
	# plt.plot(RR_squence);
	# plt.subplot(2,2,4);
	# tck = interpolate.splrep(np.arange(0,np.size(RR_squence),1),RR_squence, s=0)
	# RR_squence_resample= interpolate.splev(np.arange(0,np.size(respsignal_resample)/4,0.25), tck, der=0);
	# print(RR_squence_resample);
	# plt.plot(RR_squence_resample);
	#plt.show();
	# print(cpc_001_01_avg(RR_squence,respsignal));
	# print(cpc_01_04_avg(RR_squence,respsignal));

	