from abc import ABCMeta, abstractmethod

class IxStream(object):

	@abstractmethod
	def open(self):
		raise NotImplementedError('subclasses of BaseClass must provide an open method');

	@abstractmethod
	def close(self):
		raise NotImplementedError('subclasses of BaseClass must provide an close method');

	@abstractmethod
	def properties(self):
		raise NotImplementedError('subclasses of BaseClass must provide an properties method');

	@abstractmethod
	def variables(self):
		raise NotImplementedError('subclasses of BaseClass must provide an variables method');

	@abstractmethod
	def size(self):
		raise NotImplementedError('subclasses of BaseClass must provide an size method');

	@abstractmethod
	def find(self):
		raise NotImplementedError('subclasses of BaseClass must provide an find method');

	@abstractmethod
	def get(self,id):
		raise NotImplementedError('subclasses of BaseClass must provide an get method');

	@abstractmethod
	def add(self,id,table):
		raise NotImplementedError('subclasses of BaseClass must provide an add method');

	@abstractmethod
	def remove(self,id):
		raise NotImplementedError('subclasses of BaseClass must provide an remove method');

	@abstractmethod
	def newtable(self,id):
		raise NotImplementedError('subclasses of BaseClass must provide an newtable method');
		