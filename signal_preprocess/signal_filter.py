
import copy;
import numpy as np;
import scipy.signal as signal


def median_filter(inputsignal,windowlen=200):
	outputsignal=copy.deepcopy(inputsignal);
	signallen=len(outputsignal);
	for i in range(0,signallen-windowlen/2):
		outputsignal[i]=np.median(inputsignal[(i-windowlen/2):(i+windowlen/2-1)]);
	return outputsignal;

def low_pass_filter(inputsignal,f,ft=128,n=3):
	#inputsignal=np.array(inputsignal[2]);
	b,a = signal.butter(n,1.0*f/ft,'low');
	sf = signal.filtfilt(b,a,inputsignal);
	return sf;

def high_pass_filter(inputsignal,f,ft=128,n=3):
	# print(inputsignal.shape);
	# inputsignal=np.array(inputsignal[0]);
	b,a = signal.butter(n,1.0*f/ft,'high')
	sf = signal.filtfilt(b,a,inputsignal)
	return sf;

def band_pass_filter(inputsignal,lf,hf,ft=128,n=3):
	#inputsignal=np.array(inputsignal[2]);
	b,a = signal.butter(n,[1.0*lf/ft,1.0*hf/ft],'bandpass');
	sf = signal.filtfilt(b,a,inputsignal);
	return sf;

def band_stop_filter(inputsignal,lf,hf,ft=128,n=3):
	#inputsignal=np.array(inputsignal[2]);
	b,a = signal.butter(n,[1.0*lf/ft,1.0*hf/ft],'bandstop')
	sf = signal.filtfilt(b,a,inputsignal)
	return sf