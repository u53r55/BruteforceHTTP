import sys, actions

# TODO write stderr and stdout instead of print

def prints(mtext):
	#############################################
	#	print message and replace it after
	#	Use for status bar, brute forcing process
	#	https://stackoverflow.com/a/5291044
	#
	#	Update code by this (Works better)
	#	https://stackoverflow.com/a/41511658
	#############################################

	print(mtext)
	sys.stdout.write("\033[F \033[K" * actions.size_o(mtext))

def printp(index, total, bar_size = 50):
	completed = (index * bar_size) / total
	prints("|%s%s| %s/%s"%(
		completed * '#',
		(bar_size - completed) * '-',
		index,
		total)
	)


def printf(mtext, mtype = 'warn'):
	############################################
	#	Print text w/ color
	#
	###########################################

	print(craft_msg(mtext, mtype))
	# TODO move print to std write
	# if mtype == 'bad':
	# 	sys.stderr.write("%s\n" %(craft_msg(mtext, mtype)))
	# else:
	# 	sys.stdout.write("%s\n" %(craft_msg(mtext, mtype)))

def craft_msg(mtext, mtype = 'warn'):
	# https://misc.flogisoft.com/bash/tip_colors_and_formatting
	####################################################
	#	create text message with color
	#	bad: red
	#	warn: yellow
	#	good: light green
	#	This functions is using for Linux terminal only
	####################################################

	mtext = {
		'bad':  '\033[91m{}\033[00m'.format(mtext),
		'warn': '\033[93m{}\033[00m'.format(mtext),
		'good': '\033[92m{}\033[00m'.format(mtext),
		'norm': '\033[97m{}\033[00m'.format(mtext)
	}
	return (mtext[mtype])
	
def die(msg, error):
	printf(msg, "bad")
	printf(error, "bad")
	sys.exit(1)

def print_table(headers, *args, **kwargs):
	################################################
	#	print beautiful table in terminal style
	#	author @routersploit project
	#	ALL input data must be string
	################################################

	extra_fill = kwargs.get("extra_fill", 5)
	header_separator = kwargs.get("header_separator", "-")
	if not all(map(lambda x: len(x) == len(headers), args)):
		printf("Error headers", 'bad')
		return
	def custom_len(x):
		try:
			return len(x)
		except TypeError:
			return 0
	fill = []
	headers_line = '   '
	headers_separator_line = '   '

	for idx, header in enumerate(headers):
		column = [custom_len(arg[idx]) for arg in args]
		column.append(len(header))
		current_line_fill = max(column) + extra_fill
		fill.append(current_line_fill)
		headers_line = "".join((headers_line, "{header:<{fill}}".format(header = header, fill = current_line_fill)))
		headers_separator_line = "".join((
			headers_separator_line,
			'{:<{}}'.format(header_separator * len(header), current_line_fill)
		))
	print(headers_line)
	print(headers_separator_line)
	for arg in args:
		content_line = '   '
		for idx, element in enumerate(arg):
			content_line = "".join((
				content_line,
				'{:{}}'.format(element, fill[idx])
			))
		print(content_line)
		
def print_help():

	#	Print project's help table

	print('\nUsage: %s [<option> <value>] [mode] URL\n\nOptions:\n' %(sys.argv[0]))
	title = ("Format", "Example")
	menu = [
		[ "%-25s"%("-u <path_to_wordlist>"), "-u /usr/share/wordlists/nmap.lst"],
		[ "%-25s"%("-p <path_to_wordlist>"), "-p /usr/share/wordlists/fasttrack.txt"],
		[ "%-25s"%("-U <username>"), "-U admin | -U admin:user1:user2:user3"],
		[ "%-25s"%("-t <threads>"), "-t 32"],
		[ "%-25s"%("-k <false_key>"), "-k 'Invalid username'"]
	]
	print_table(title, *menu)
	
	print("\nModes:\n")
	title = ("Attack Modes", "Ony ONE attack mode can be used")
	menu = [
		[ "%-25s"%("--brute [Default]"), "Brute Forcing credentials"],
		[ "%-25s"%("--sqli [Not Available]"), "SQL Injection bypass"],
		[ "%-25s"%("--basic [Not Available]"), "HTTP Basic Authentication"],
	]
	print_table(title, *menu)

	print("")
	title = ("Running Modes", "")
	menu = [
		[ "%-25s"%("--proxy"), "Use Proxy each connection"],
		[ "%-25s"%("--verbose [Not Available]"), "Display more information"],
		[ "%-25s"%("--report [Not Available]"), "Write result report"],
	]
	print_table(title, *menu)
	print("")

# OLD DEMO CODE	
# def fixLen(text, lim):
# 	# https://stackoverflow.com/a/37422973
# 	def _f(text, lim):
# 		while text:
# 			yield "|   %-20s |\n" %(text[:lim])
# 			text = text[lim:]
# 	return "".join(list(_f(text, lim)))

# TESTING WITH PRINT 
# def fixLen(text, lim):
# 	"""
# 	mystr = "1234567890"
# 	print mystr[5:] ---> new_text
# 		67890
# 	print mystr[:5] ---> cut text 
# 		12345
# 	"""
# 	# https://stackoverflow.com/a/37422973
# 	def _f(text, lim):
# 		while text:
# 			_tmp = text[:lim]
# 
# 			if len(_tmp) >= lim:
# 				yield " |\n  |  %.*s" %(lim, _tmp)
# 			else:
# 				# Last line
# 				yield " |\n  | %s%s" %(_tmp, " " * (lim - len(_tmp)))
# 			text = text[lim:]
# 
# 	result = "%.*s" %(lim, text[:lim])
# 	text = text[lim:]
# 	return result + "".join(list(_f(text, lim)))

def fixLen(text, lim):
	"""
	>>> mystr = "1234567890123456789"
	>>> print mystr[5:] --->>> new_text
		67890123456789
	>>> print mystr[:5] --->>> cut_text
		12345
	>>> 

	"""
	# https://stackoverflow.com/a/37422973
	ret, text = " %.*s" %(lim, text[:lim]), text[lim:]
	
	while text:
		
		if len(text) < lim:
			text = text + " " * (lim - len(text))

		ret, text = ret + " |\n  |  %.*s" %(lim, text[:lim]), text[lim:]

	#print ret[-1].split("\n")[-1]
	return ret
		
	# def _f(text, lim):
	# 	while text:
	# 		_tmp = text[:lim]
	# 
	# 		if len(_tmp) >= lim:
	# 			yield " |\n  |  %.*s" %(lim, _tmp)
	# 		else:
	# 			# Last line
	# 			yield " |\n  | %s%s" %(_tmp, " " * (lim - len(_tmp)))
	# 		text = text[lim:]
	# 
	# # result = "%.*s" %(lim, text[:lim])
	# # text = text[lim:]
	# # return result + "".join(list(_f(text, lim)))

	
def start_banner(url, options, mode, r_options):
	usr = options["-U"] if options["-U"] else options["-u"]

	banner = """
	  =======================================================================
	/%-73s\\
	|-------------------------------------------------------------------------|
	|  Target: %-62s |
	|  URL: %-65s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Users: %-63s |
	|  Password: %-60s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                         |
	|       Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s     |
	|                                                                         |
	|-------------------------------------------------------------------------|
	|            Verbose: %-13s  |          Save Log: %-12s    |
	|-------------------------------------------------------------------------|
	\\       False keyword: %-50s /
	  =======================================================================
	""" %( " " * 25 + "HTTP LOGIN BRUTE FORCING",
		fixLen(url.split("/")[2], 62),
		fixLen(url, 64),
		usr[:65],
		options["-p"][:60],
		mode.replace("--", ""),
		r_options["--proxy"],
		options["-t"],
		r_options["--verbose"],
		r_options["--report"],
		str(options["-k"])[:50]
	)
	
	return banner.replace("\t", "  ")
	
if __name__ == "__main__":
	die("Oops! Wrong place", "Find other place")