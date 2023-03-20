'''Info Header Start
Name : TDPythonRunner
Author : wieland@MONOMANGO
Version : 0
Build : 4
Savetimestamp : 2023-03-20T11:20:02.471367
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import subprocess, os

class TDPythonRunner:
	"""
	TDPythonRunner description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.process = None
	
	@property
	def python_path(self):
		return os.path.join( app.binFolder, "python.exe")
	@property
	def script_dat(self):
		return self.ownerComp.op("repo_maker").Repo
	
	@property
	def arguments(self):
		return [ row[0].val for row in self.ownerComp.op("arguments").rows() ]

	def Kill(self):
		if self.process: subprocess.kill()

	def Run_Async(self):
		self._run( subprocess.Popen )

	def Run_Sync(self):
		self._run( subprocess.Popen ).wait()
		
	def load_modules(self):
		for index, row in enumerate( self.ownerComp.op("modules").rows() ):
			module_cell = self.ownerComp.op("modules")[index, 0]
			pip_cell = self.ownerComp.op("modules")[index, 1]
			self.ownerComp.op("td_pip").Import_Module(
				module_cell.val, pip_name = ( pip_cell or module_cell ).val
			)

	def _run(self, callback):
		try:
			self.Kill()
		except:
			pass
		self.load_modules()
		filepath = self.script_dat.save( f"temp/{self.script_dat.id}.py", createFolders = True)
		return callback(
			[self.python_path, os.path.abspath( filepath )] + self.arguments
		)