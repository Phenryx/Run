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
		print arguments
		self.view.window().run_command("exec", arguments)

	def arguments(self, infos):
		load_args = infos.database[infos.syntax]

		if infos.platform in load_args.keys():
			load_args = load_args[infos.platform]

		arguments = {}
		arguments["shell"] = True

		for cmd in load_args:
			if isinstance(load_args[cmd], list):
				cmd_args = load_args[cmd]
				lst_arguments = ""

				for command in cmd_args:

					if command in infos.format:
						command_eval = infos.format[command]
						lst_arguments += " " + infos.__dict__[command_eval]

					elif command[0:2] == "--":
						lst_arguments = lst_arguments[:-1] + command[2:]

					else:
						lst_arguments += " " + command

				arguments[cmd] = [lst_arguments]

			else:
				print "Error in " + infos.db_file + "\n" + infos.syntax + "'s syntax is irregular."

		return arguments