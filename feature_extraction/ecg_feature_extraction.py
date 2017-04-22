import scipy.io as scio;
from scipy import interpolate;
import math;
from config import AlgorithmFolder;
import matplotlib.pyplot as plt;
import pandas as pd;
import numpy as np;
from datafromdataset import datafromdataset;
import pywt;
import copy;

from ecg_quality import singal_normalize;

def find_RR(ecgsignal,windowlen=100,windowlimit=50,rvaluelimit=10,signalcompare=5):
	w = pywt.Wavelet('sym3');
	cD2=[];
	cA3,cD3,cD2,cD1=pywt.wavedec(ecgsignal,wavelet=w,mode='cpd',level=3);
	cD2=np.interp(np.linspace(0,1,len(ecgsignal)),np.linspace(0,1,len(cD2)),cD2);
	windownum=0;
	cD2len=len(cD2);
	cD2=pd.Series(cD2,index=range(ecgsignal.index.min(),ecgsignal.index.max()+1));
	cD2=abs(cD2);
	rridx=[];
	try:
		while((windownum+1)*windowlen<cD2len):
			ridx=cD2[windownum*windowlen:(windownum+1)*windowlen].idxmax();
			sridx=ridx;
			if ridx-signalcompare*3>=ecgsignal.index.min() and ridx+signalcompare<=ecgsignal.index.max():
				sridx=ecgsignal[range(ridx-signalcompare*3,ridx+signalcompare+1)].idxmax();

			if len(rridx)==0 and cD2[ridx]>rvaluelimit:
				rridx.append(sridx);
			elif len(rridx)>0 and ridx-rridx[-1]>windowlimit and cD2[ridx]>rvaluelimit:
				rridx.append(sridx);
			elif len(rridx)>0 and ridx-rridx[-1]<windowlimit and cD2[ridx]>cD2[rridx[-1]] and cD2[ridx]>rvaluelimit:
				rridx[-1]=sridx;
			windownum=windownum+1;
	except Exception,e:  
		print(ecgsignal.index.min());
		print(ecgsignal.index.max());
	return rridx;


def RRinternal(ecgsignal,windowlen=100,windowlimit=50,rvaluelimit=10,signalcompare=5,rrvalueminlimit=0.2,rrvaluemaxlimit=1.5,samplerate=128):
	rrsquence=[];
	rridx=find_RR(ecgsignal,windowlen,windowlimit,rvaluelimit,signalcompare);
	for i in range(1,len(rridx)):
		rrvaluei=1.0*(rridx[i]-rridx[i-1])/samplerate;
		if rrvaluei<rrvaluemaxlimit and rrvaluei>rrvalueminlimit:
			rrsquence.append(rrvaluei);
	return rrsquence;

def RRsquence_index(rrsquence):
	rrsquenceindex=[];
	rrsquencelen=len(rrsquence);
	if rrsquencelen==0:
		return rrsquenceindex;
	rrsquenceindex.append(rrsquence[0]);
	for i in range(1,rrsquencelen):
		rrsquenceindex.append(rrsquenceindex[i-1]+rrsquence[i]);
	return rrsquenceindex;

def RRinternal_avg(rrsquence):
	rrsquencelen=len(rrsquence);
	resultlist=[];
	if rrsquencelen<1:
		return [0];
	rrinternalavg=1.0*sum(rrsquence)/rrsquencelen;
	resultlist.append(rrinternalavg)
	return resultlist;

def RRinternal_stdev(rrsquence):
	rrsquencelen=len(rrsquence);
	resultlist=[];
	if rrsquencelen<1:
		return [0];
	rrinternalavg=1.0*sum(rrsquence)/rrsquencelen;
	sdsq=sum([(i-rrinternalavg)**2 for i in rrsquence]);
	stdev=(sdsq/rrsquencelen)**0.5;
	resultlist.append(stdev);
	return resultlist;

def RRinternal_maxdev(rrsquence):
	rrsquencelen=len(rrsquence);
	resultlist=[];
	if rrsquencelen<1:
		return [0];
	resultlist.append(max(rrsquence)-min(rrsquence));
	return resultlist;

def RRinternal_median(rrsquence):
	rrsquencelen=len(rrsquence);
	resultlist=[];
	if rrsquencelen<1:
		return [0];
	sortsquence=copy.deepcopy(rrsquence);
	sortsquence.sort();
	resultlist.append(sortsquence[rrsquencelen//2]);
	return resultlist;

def RRinternal_compare50(rrsquence):
	rrsquencelen=len(rrsquence);
	resultlist=[];
	if rrsquencelen<1:
		return [0];
	dvalue_sum=0;
	dvalue50_sum=0;
	for i in range(0,rrsquencelen-1):
		dvalue_sum=dvalue_sum+1;
		if abs(rrsquence[i+1]-rrsquence[i])>50:
			dvalue50_sum=dvalue50_sum+1;
	if dvalue_sum>0:
		resultlist.append(dvalue50_sum)
	else:
		resultlist.append(0);
	return resultlist;

def RRsquence_power(rrsquence,resamplerate=8):
	RRsquenceindex=RRsquence_index(rrsquence);
	tck = interpolate.splrep(RRsquenceindex,rrsquence, s=0);
	RR_squence_resample= interpolate.splev(np.arange(0,max(RRsquenceindex),1.0/resamplerate), tck, der=0);
	RRfft=np.fft.fft(RR_squence_resample);
	rrsquencepower=RRfft*RRfft;
	return rrsquencepower;

def RRsquencepower_sum00101(rrsquence,resamplerate=8):
	resultlist=[];
	rrsquencepower=RRsquence_power(rrsquence,resamplerate);
	startposition=int(len(rrsquencepower)*0.01/resamplerate);
	endposition=int(len(rrsquencepower)*0.1/resamplerate);
	powersum=1.0*sum(abs(rrsquencepower[startposition:endposition]));
	resultlist.append(np.log10(powersum*powersum));
	return resultlist;

def RRsquencepower_sum0104(rrsquence,resamplerate=8):
	resultlist=[];
	rrsquencepower=RRsquence_power(rrsquence,resamplerate);
	startposition=int(len(rrsquencepower)*0.1/resamplerate);
	endposition=int(len(rrsquencepower)*0.4/resamplerate);
	powersum=1.0*sum(abs(rrsquencepower[startposition:endposition]));
	resultlist.append(np.log10(powersum*powersum));
	return resultlist;

def RRsquencepower_lfhf(rrsquence,resamplerate=8):
	resultlist=[];
	hfpower=RRsquencepower_sum0104(rrsquence,resamplerate);
	lfpower=RRsquencepower_sum00101(rrsquence,resamplerate);
	if lfpower!=0:
		resultlist.append(lfpower[0]/hfpower[0]);
	else:
		resultlist.append(0);
	return resultlist;

if __name__=='__main__':
	ecgsignal=datafromdataset('ucddb018_recm','ecg',range(1130000,1140000));
	RR_squence=RRinternal(ecgsignal);
	# for i in rridx:
	# 	plt.plot(i,ecgsignal[i],'ro');
	# plt.plot(ecgsignal);
	# plt.show();
	# RRsquenceindex=RRsquence_index(RR_squence);
	# plt.subplot(2,1,1);
	# plt.plot(RRsquenceindex,RR_squence);
	# plt.subplot(2,1,2);
	# tck = interpolate.splrep(RRsquenceindex,RR_squence, s=0);
	# RR_squence_resample= interpolate.splev(np.arange(0,max(RRsquenceindex),0.25), tck, der=0);
	# tck = interpolate.splrep(np.arange(0,np.size(RR_squence),1),RR_squence, s=0);
	# RR_squence_resample= interpolate.splev(np.arange(0,np.size(respsignal_resample)/4,0.25), tck, der=0);
	# plt.show();

	# ecgsignalfft=np.fft.fft(ecgsignal);
	# plt.plot(np.log10(abs(ecgsignalfft[0:10000])));
	# RRfft=np.fft.fft(RR_squence_resample);
	# plt.plot(np.log10(abs(RRfft[:2000]*RRfft[:2000])));
	xxs=np.arange(0,len(RR_squence)/(len(ecgsignal)/128),2*1.0*len(RR_squence)/(len(ecgsignal)/128)/len(RR_squence));
	RR_squence_fft=abs(np.fft.fft(RR_squence));
	plt.plot(xxs,RR_squence_fft[0:len(RR_squence)/2]);
	plt.show();
	# print(RRsquencepower_sum00101(RR_squence));
	# print(RRsquencepower_sum0104(RR_squence));
	# print(RRsquencepower_lfhf(RR_squence));
