class TxDatasetVariable:
	def __init__(self,id,name,dimensions,label,unit,begintime,endtime,samplerate,length,valtype,description):
		self.id=id;
		self.name=name;
		self.dimensions=dimensions;
		self.label=label;
		self.unit=unit;
		self.begintime=begintime;
		self.endtime=endtime;
		self.samplerate=samplerate;
		self.length=length;
		self.valtype=valtype;
		self.description=description;

	def clear():
		self.id=[];
		self.name=[];
		self.dimensions=[];
		self.label=[];
		self.unit=[];
		self.begintime=[];
		self.endtime=[];
		self.samplerate=[];
		self.length=[];
		self.valtype=[];
		self.description=[];