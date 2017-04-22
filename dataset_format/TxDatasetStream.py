import os
import uuid
import pandas as pd
from pandas import DataFrame,Series
from IxStream import IxStream
from TxProperties import TxProperties
from TxDatasetTable import TxDatasetTable
from TxDatasetVariable import TxDatasetVariable
from TxDatasetStorageFile import TxDatasetStorageFile


DataURLRoot='D:\\dataset\\';
class TxDatasetStream(IxStream):

	def __init__(self,id,state,datatype):
		self.id=id;
		self.state=state;
		self.__properties=TxProperties();
		self.__datatype=datatype;
		if datatype=='wearabledata':
			self.__path=DataURLRoot+'wearabledata\\'+self.id+'\\';
		elif datatype=='dietdata':
			self.__path=DataURLRoot+'dietdata\\'+self.id+'\\';
		else:
			self.__path=DataURLRoot+'otherdata\\'+self.id+'\\';

	def getpath(self):
		return self.__path;


	def open(self):
		self.__properties=self.__properties.get(self.__path,self.id);
		self.__load();

	def close(self):
		pass;

	def __load(self):
		pass;

	def __save(self):
		pass;
		
	def properties(self):
		return self.__properties;

	def variables(self):
		variables=[];
		for item in self.__properties.items:
			if isinstance(item,TxDatasetVariable):
				variables.append(item);
		return variables;


	def storages(self):
		storages=[];
		for item in self.__properties.items:
			if isinstance(item,TxDatasetStorageFile):
				storages.append(item);
		return storages;

	def find(self,tableidlist):
		tables=[];
		for i in range(0,len(idlist)):
			tables.append(self.get(i));
		return tables;

	def tables(self):
		tables=[];
		for root,directory,files in os.walk(self.__path):
			for filename in files:
				name,suf = os.path.splitext(filename);
				if suf=='.csv':
					tables.append(name);
		return tables;

	def get(self,tableid):
		table=TxDatasetTable(self.id,self.__path);
		table.id=tableid;
		table.datasetid=self.id;
		if os.path.exists(self.__path+tableid+'.csv'):
			data1=pd.read_csv(self.__path+tableid+'.csv');
			dims=data1.shape;
			table.rowcount=dims[0];
			table.colcount=dims[1];
			names=range(1,dims[1]+1);
			data2=pd.read_csv(self.__path+tableid+'.csv',names=names,index_col=0);
			table.data=data2;
		else:
			print('Table '+tableid+' is not existed. so return a null table');
		return table;

	def add(self,tableid,table):
		if not os.path.exists(self.__path):
			os.makedirs(self.__path);
		table.data.to_csv(self.__path+tableid+'.csv',header=False);
		print(self.__path+tableid+'.csv is created.');

	def remove(self,tableid):
		if os.path.exist(self.__path+tableid+'.csv'):
			os.remove(self.__path+tableid+'.csv');
			print(self.__path+tableid+'.csv is removed.');

	def newtable(self,tableid):
		table=TxDatasetTable(self.id,self.__path);
		return table;

		
if __name__=='__main__':
	datastream=TxDatasetStream('1234',1,'wearabledata');
	datastream.open();

	tableid=str(uuid.uuid1()).replace('-','');
	print(tableid);
	table=TxDatasetTable(datastream.id,datastream.getpath());
	table.data=DataFrame([1,2,3,4,5]);
	datastream.add(tableid,table);

	properties=TxProperties();
	datasetvariableid=str(uuid.uuid1()).replace('-','');
	properties.item[datasetvariableid]=TxDatasetVariable(datasetvariableid,'ecgdataset',3,'a','b',142563433,22332221,500,200,2,'an ecg data');
	properties.item[tableid]=TxDatasetStorageFile(tableid+'.csv',table.data.size);
	properties.set(datastream.getpath(),datastream.id,properties);
	#datastream.open();