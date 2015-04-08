import os
import hello
from project import Project
from projectfile import ProjectFile
from projectfileversion import ProjectFileVersion
from parsexml import ParseXML


import unittest
import tempfile

class HelloTestCase(unittest.TestCase):

	def setUp(self):
		hello.app.config['TESTING'] = True
		self.app = hello.app.test_client()


	def tearDown(self):
		print "finishing..."
        #os.close(self.db_fd)
        #os.unlink(hello.app.config['DATABASE'])

	def test_parse_project(self):
		print "testing if projects are parsed correctly..."

		pxml = ParseXML()
		projects = pxml.parseXML('svn_list_test.xml', 'svn_log_test.xml')
		project = projects.values()[0]
		assert 'A' in project.title
		assert '2015-02-26T04:53:56.159823Z' in project.date
		assert '1' in project.version
		assert 'Adding A and B' in project.summary

	def test_parse_projectfile(self):
		print "testing if files are parsed correctly"

		pxml = ParseXML()
		projects = pxml.parseXML('svn_list_test.xml', 'svn_log_test.xml')
		projectfile = projects.values()[0].getFiles()[0]
		assert 'A/B' in projectfile.path
		assert 'dir' in projectfile.type
		assert 0 == projectfile.size

	def test_parse_projectfileversion(self):
		print "testing if versions are parsed correctly"

		pxml = ParseXML()
		projects = pxml.parseXML('svn_list_test.xml', 'svn_log_test.xml')
		projectfile = projects.values()[0].getFiles()[0]
		version = projectfile.versions[1]
		assert "1" == version.number
		assert 'ejricht2' in version.author
		assert "2015-01-13T04:46:09.926345Z" == version.date
		assert 'Adding A and B' in version.info

	#def test_parse(self):
    #    rv = self.app.get('/')
    #    assert 'No entries here so far' in rv.data

if __name__ == '__main__':
	unittest.main()