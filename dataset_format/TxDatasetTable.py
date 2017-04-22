import numpy as np
import pandas as pd 
from pandas import DataFrame

class TxDatasetTable:
	def __init__(self,datasetid,path):
		self.id=[];
		self.datasetid=[];
		self.data=DataFrame([]);
		self.rowcount=[];
		self.colcount=[];
		self.__path=path+datasetid+'.csv';

	def load(self):
		if os.path.exists(self.__path):
			self.data=pd.read_csv(self.__path);
			dims=self.data.shape;
			self.rowcount=dims[0];
			self.colcount=dims[1];

	def save(self):
		self.data.to_csv(self.__path+tableid+'.csv',header=False);
		print('table.data is saved.');

	def get(self,x,y):
		return self.data[x][y];

	def column(self,x):
		return self.data[:][x];

	def row(self,y):
		return self.data[y][:];

	def rowcount(self):
		shape=self.data.shape;
		return shape[0];

	def colcount(self):
		shape=self.data.shape;
		return shape[1];

	def set(self,x,y,value):
		self.data[x][y]=value;

	def select(self,columns,rowbegin,rowend):
		return self.data[rowbegin:rowend+1,columns];

	