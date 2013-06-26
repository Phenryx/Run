'''
Plugin for Sublime Text 2

Author: Benedetto "phenryx" Abbenanti
'''

import sublime, sublime_plugin
import os, sys
import json
import Infos

class RunCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print "--- Run - Sublime Text 2 Plugin"
		current_view = self.view
		infos = Infos.Infos(current_view)
		self.run_command(infos)
		print "With a stdin for the plugin: " + infos.stdin

	def run_command(self, infos):
		syntax = infos.syntax
		if syntax not in infos.database.keys():
			return None
		arguments = self.arguments(infos)
		self.view.window().run_command("exec", arguments)

	def arguments(self, infos):
		load_args = infos.database[infos.syntax]
		arguments = {}
		arguments["shell"] = True
		for command in load_args:
			if isinstance(load_args[command], list):
				lst_arguments = self.lst_arguments(infos, load_args[command])
				arguments[command] = eval(lst_arguments)
				continue
			elif load_args[command] in infos.format:
				arguments[command] = infos.format[command]
				continue
			arguments[command] = load_args[command]
		return arguments

	def lst_arguments(self, infos, load_args_sub):
		lst_arguments = "['"
		for command in load_args_sub:
			if command in infos.format:
				command_eval = eval("infos."+"format[\""+command+"\"]")
				lst_arguments += " " + eval("infos."+command_eval)
				continue
			lst_arguments += " " + command
		lst_arguments += "']"
		return lst_arguments