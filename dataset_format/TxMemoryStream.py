from IxStream import IxStream
from TxProperties import TxProperties
from TxDatasetStorageFile import TxDatasetStorageFile
from TxDatasetTable import TxDatasetTable


class TxMemoryStream(IxStream):
	def __init__(self,id,state):
		self.id=id;
		self.state=state;
		self.tables=[];
		self.__properties=TxProperties();

	def open(self):
		pass;

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

	def tables(self):
		return self.tables;

	def find(self):
		pass;

	def get(self,tableid):
		for table in self.tables:
			if table.id==tableid:
				return table;

	def add(self,id,table):
		table.id=id;
		self.tables.append(table);
		return table;

	def remove(self,tableid):
		for table in self.tables:
			if table.id ==tableid:
				tables.remove(table);

	def newtable(self,id):
		table=TxDatasetTable();
		self.tables.append(table);
		return table;

	if __name__=='__main__':
		pass;