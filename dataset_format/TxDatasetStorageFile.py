class TxDatasetStorageFile:
	def __init__(self,filename='',size=0):
		self.filename=filename;
		self.size=size;

if __name__=='__main__':
	datasetstroagefile=TxDatasetStorageFile('2322.csv',35);
	print(datasetstroagefile.filename);
	print(datasetstroagefile.size);

	