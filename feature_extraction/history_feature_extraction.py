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


def pastlabels_1(labels):
	resultlist=[];
	labelslen=len(labels);
	resultlist.append(0);
	for i in range(1,len(labels)):
		resultlist.append(labels[i-1]);
	return resultlist;

def pastlabels_5(labels):
	resultlist=[];
	labelslen=len(labels);
	resultlist.append(0);
	for i in range(1,4):
		if i>labelslen-1:
			return resultlist;
		else:
			resultlist.append(1.0*sum(labels[0:i])/i);
	for i in range(4,labelslen):
		resultlist.append(1.0*sum(labels[i-5:i])/5);
	return resultlist;

def pastlabels_5(labels):
	resultlist=[];
	labelslen=len(labels);
	resultlist.append(0);
	for i in range(1,4):
		if i>labelslen-1:
			return resultlist;
		else:
			resultlist.append(1.0*sum(labels[0:i])/i);
	for i in range(4,labelslen):
		resultlist.append(1.0*sum(labels[i-5:i])/5);
	return resultlist;

def pastlabels_10(labels):
	resultlist=[];
	labelslen=len(labels);
	resultlist.append(0);
	for i in range(1,9):
		if i>labelslen-1:
			return resultlist;
		else:
			resultlist.append(1.0*sum(labels[0:i])/i);
	for i in range(9,labelslen):
		resultlist.append(1.0*sum(labels[i-10:i])/10);
	return resultlist;

def pastlabels_50(labels):
	resultlist=[];
	labelslen=len(labels);
	resultlist.append(0);
	for i in range(1,49):
		if i>labelslen-1:
			return resultlist;
		else:
			resultlist.append(1.0*sum(labels[0:i])/i);
	for i in range(49,labelslen):
		resultlist.append(1.0*sum(labels[i-50:i])/50);
	return resultlist;


if __name__=='__main__':
	labels=[1,2,2,2,1,1,3,2,1,2,3,4,1,5,5,5,4,3,2,1];
	print(pastlabels_1(labels));
	print(pastlabels_5(labels));
	print(pastlabels_10(labels));