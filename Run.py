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

		if infos.platform in load_args.keys():
			load_args = load_args[infos.platform]

		arguments = {}
		arguments["shell"] = True

		for command in load_args:
			if isinstance(load_args[command], list):
				cmd_args = load_args[command]

				#lst_arguments = "['"
				lst_arguments = []
				for command in cmd_args:
					if command in infos.format:
						#command_eval = eval("infos.format[\""+command+"\"]")
						command_eval = infos.format[command]
						#lst_arguments += " " + eval("infos."+command_eval)
						#lst_arguments += " " + infos.__dict__[command_eval]
						lst_arguments.append(infos.__dict__[command_eval])
						#continue
					elif command[0:2] == "--":
						#lst_arguments += "" + command[2:]
						lst_arguments.append(lst_arguments.pop()+command[2:])
					else:
						#lst_arguments += " " + command
						lst_arguments.append(command)

				#lst_arguments = self.lst_arguments(infos, load_args[command])
				arguments[command] = eval(lst_arguments)
				#continue
			else:
				print "Error in " + infos.db_file + "\n" + infos.syntax + "'s syntax is irregular."
			#elif load_args[command] in infos.format:
			#	arguments[command] = infos.format[command]
			#	continue
			#arguments[command] = load_args[command]

		return arguments

"""
	def lst_arguments(self, infos, cmd_args):
		lst_arguments = "['"
		for command in cmd_args:
			if command in infos.format:
				command_eval = eval("infos."+"format[\""+command+"\"]")
				lst_arguments += " " + eval("infos."+command_eval)
				continue
			lst_arguments += " " + command
		lst_arguments += "']"
		return lst_arguments
"""