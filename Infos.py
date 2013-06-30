import sublime, sublime_plugin
import os, json
from subprocess import Popen, PIPE

class Infos(object):
	def __init__(self,view):
		PyStdinFile = sublime.packages_path()+"/Run/Stdin.py"
		proc = Popen(["python", PyStdinFile], stdout=PIPE)
		self.stdin = proc.communicate()[0][:-1]

		db_file = os.path.join(sublime.packages_path(), "Run", "Run.sublime-run")
		format_file = os.path.join(sublime.packages_path(), "Run", "Run.format-name")

		with open(db_file, "rU") as database:
			self.database = json.load(database)
		with open(format_file, "rU") as format:
			self.format = json.load(format)

		self.file_full = view.file_name()

		if sublime.platform() == u'linux':
			self.file_path = os.path.split(view.file_name())[0].replace(" ", "\\ ")
		else:
			self.file_path = "\""+os.path.split(view.file_name())[0]+"\""

		self.file_name = os.path.split(view.file_name())[-1]
		self.file_extension = self.file_name.split(".")[-1]
		self.file_base_name = os.path.basename(self.file_path)
		self.file_name_blank = self.file_name.replace("."+self.file_extension, "")
		self.packages = ""
		self.project = ""
		self.project_path = ""
		self.project_name = ""
		self.project_extension = ""
		self.project_base_name = ""
		self.syntax = view.settings().get("syntax").split("/")[1].lower()
		self.platform = sublime.platform()
