import xml.etree.ElementTree as ET
from project import Project
from projectfile import ProjectFile
from projectfileversion import ProjectFileVersion

class ParseXML:
	#do all the xml parsing
	def parseXML(self, xmllist, xmllog):
		#create hash from project name to project
		self.projects = {}
		self.svnpath = ""
		#parse list xml
		tree = ET.parse(xmllist)
		root = tree.getroot()

		for list_ in root:
			self.svnpath = list_.attrib.values()[0] 
			for entry in list_:
				pname = self.entryExistsInProject(entry)
				if (pname == None):
					self.addEntryFromListXML(entry)
				else:
					self.updateEntryFromListXML(entry, pname)

		#parse revision log xml
		tree = ET.parse(xmllog)
		root = tree.getroot()

		#iterate through projects
		for projectname, project in self.projects.items(): 
			#iterate through files in each project
			for file_ in project.getFiles():
				#iterate through all logentries
				for logentry in root:
					self.updateFileVersionEntry(file_, logentry)


		#Get summary (commit message of most recent revision)
		for projectname, project in self.projects.items(): 
			for logentry in root:
				revision = logentry.attrib
				if revision.values()[0] == project.getVersion():
					project.setSummary(logentry.find("msg").text)

		return self.projects


	#pass in entry XML to parse and add to projects list (data from list.xml)
	#parses name, date, version
	def addEntryFromListXML(self, entry):
		proj = Project(entry[0].text)
		proj.setDate(entry[1][1].text)
		proj.setVersion(entry[1].attrib.values()[0])
		self.projects[entry[0].text] = proj


	#pass in entry XML to parse and update element in project list (data from list.xml)
	#make a projectfile object
	def updateEntryFromListXML(self, entry, pname):
		project = self.projects[pname]
		newfile = ProjectFile(entry[0].text)
		newfile.setType(entry.attrib.values()[0])
		if entry.find("size") == None:
			newfile.setSize(0)
		else:
			newfile.setSize(int(entry.find("size").text))

		project.addToFiles(newfile)


	#check if entry exists in a project, i.e. if the first part of the pathname is one of the projects
	#returns projectname if it's in a project, None if its not
	def entryExistsInProject(self, entry):
		for projectname, project in self.projects.items():
			if projectname in entry[0].text:
				return projectname
		return None

	#Updates file, adding a new projectfileversion
	def updateFileVersionEntry(self, file_, logentry):
		if (self.isFileInLogEntry(file_, logentry)):
			#add revision
			revision = logentry.attrib.values()[0] 
			author = logentry[0].text
			date = logentry[1].text
			info = logentry.find("msg").text

			version = ProjectFileVersion(revision, author, info, date)
			file_.addToVersions(version)

	#checks if a logentry is in a file already 
	def isFileInLogEntry(self, file_, logentry):
		filepath = file_.getPath()
		for path in logentry[2]:
			if filepath in path.text:
				return True
		return False

	def getSvnPath(self):
		return self.svnpath

