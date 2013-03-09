'''
Plugin for Sublime Text 2

Author: Benedetto "phenryx" Abbenanti
'''

import sublime, sublime_plugin
import subprocess, os, sys
import json

class RunCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infos = {}
		database = os.path.join(sublime.packages_path(), "Run", "Run.sublime-run")
		format = os.path.join(sublime.packages_path(), "Run", "Run.format-name")
		with open(database, "rU") as db:
			db = json.load(db)
		with open(format, "rU") as format:
			format = json.load(format)
		infos["file_full"] = self.view.file_name()
		infos["file_path"] = os.path.split(self.view.file_name())[0]
		infos["file_name"] = os.path.split(self.view.file_name())[-1]
		infos["file_extension"] = infos["file_name"].split(".")[-1]
		infos["file_base_name"] = os.path.basename(infos["file_path"])
		infos["file_name_blank"] = infos["file_name"].replace("."+infos["file_extension"], "")
		infos["packages"] = ""
		infos["project"] = ""
		infos["project_path"] = ""
		infos["project_name"] = ""
		infos["project_extension"] = ""
		infos["project_base_name"] = ""
		infos["syntax"] = self.view.settings().get("syntax").split("/")[1]
		infos["platform"] = sublime.platform()
		self.run_command(infos, db, format)

	def run_command(self, infos, db, format):
		syntax = infos["syntax"].lower()
		if syntax.lower() not in db.keys():
			return None
		self.view.run_command("echo", {"Tempus": "Irreparabile", "Fugit": "."})
		arguments = self.arguments(syntax, infos, db, format)
		self.view.window().run_command("exec", arguments)

	def arguments(self, syntax, infos, db, format):
		load_args = db[syntax]
		arguments = {}
		arguments["shell"] = True
		for command in load_args:
			if isinstance(load_args[command], list):
				lst_arguments = self.lst_arguments(infos, load_args[command], format)
				arguments[command] = lst_arguments
				continue
			elif load_args[command] in format: #and isinstance(load_args[command], str):
				arguments[command] = infos[format[command]]
				continue
			elif isinstance(load_args[command], dict):
				sub_arguments = self.arguments(syntax, infos, load_args[command], format)
				arguments[command] = sub_arguments
				continue
			arguments[command] = load_args[command]
		return arguments

	def lst_arguments(self, infos, load_args_sub, format):
		lst_arguments = []
		for command in load_args_sub:
			if command in format:
				lst_arguments.append(infos[format[command]])
				continue
			lst_arguments.append(command)
		return lst_arguments

class Infos(object):
	def __init__(self):
		infos["file_full"] = self.view.file_name()
		infos["file_path"] = os.path.split(self.view.file_name())[0]
		infos["file_name"] = os.path.split(self.view.file_name())[-1]
		infos["file_extension"] = infos["file_name"].split(".")[-1]
		infos["file_base_name"] = os.path.basename(infos["file_path"])
		infos["file_name_blank"] = infos["file_name"].replace("."+infos["file_extension"], "")
		infos["packages"] = ""
		infos["project"] = ""
		infos["project_path"] = ""
		infos["project_name"] = ""
		infos["project_extension"] = ""
		infos["project_base_name"] = ""
		infos["syntax"] = self.view.settings().get("syntax").split("/")[1]
		infos["platform"] = sublime.platform()

