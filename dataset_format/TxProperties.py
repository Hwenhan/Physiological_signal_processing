
import json
import os
from TxDatasetStorageFile import TxDatasetStorageFile
from TxDatasetVariable import TxDatasetVariable


class TxProperties:
	
	def __init__(self):
		self.item={};
		self.tempbuf=[];

	def parse(self,jsonstr):
		decodejson=json.load(jsonstr);
		self.item={};
		for key in enumerate(decodejson):
			self.item[key[1]]=decodejson[key[1]];


	def assemble(self):
		pass;

	def find(self,path):
		with open(path, "r") as jsonfile:
			decodejson=json.load(jsonfile);
			result={};
			for key in enumerate(decodejson):
				result[key[1]]=decodejson[key[1]];
		return result;

	def find(self,path):
		pass;

	def get(self,path,idx):
		properties=TxProperties();
		propertiesfilename=path+idx+'.json';
		if os.path.exists(propertiesfilename):
			with open(propertiesfilename,"r") as propertiesfile:
				decodejson=json.load(propertiesfile);
				properties.item={};
				for key in enumerate(decodejson):
					properties.item[key[1]]=decodejson[key[1]];
		else:
			properties.tempbuf=[];
			properties.item={};

		return properties;

	def set(self,path,idx,properties):
		propertiesfilename=path+idx+'.json';
		if not os.path.exists(path):
			os.mkdir(path);

		items={};
		for key in properties.item.keys():
			if key=='variables':
				items[key]=[];
				for vitem in properties.item[key]:
					if isinstance(vitem,dict):
						items[key].append(vitem);
					else:
						items[key].append(vitem.__dict__);
			elif key=='storages':
				items[key]=[];
				for sitem in properties.item[key]:
					if isinstance(sitem,dict):
						items[key].append(sitem);
					else:
						items[key].append(sitem.__dict__);
			else:
				items[key]=properties.item[key];

		with open(propertiesfilename,"w") as propertiesfile:
			jsonstr=json.dumps(items);
			propertiesfile.write(jsonstr);


if __name__=='__main__':
	pass;