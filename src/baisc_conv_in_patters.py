from REGEX_TOOLS import C

from basic_re_pattern import YOU___, YOUR___, YOURE___, AuxV___, PLEASE___, YES___, OKAY___


class I_Pattern:
	"""
		The patterns for the basic input messages
	"""
	
	logout = [
		C(r"(log|sign)o? ?(out|off)"),
	]

	yeses = [
		C(rf'(?:ah )?(?:well )?(?:actually )?{YES___}(?: of(?: |-)?course)?(?: sure)?'),
		C(rf'(?:ah )?(?:well )?(?:actually )?(?:(?:{YES___}|{OKAY___}|(?: of[ -]?course)|(?: sure)|go (?:on|ahead)) ?){{1,6}}'),
		# well actually yes/yep/yeah of~course
		"go (?:on|ahead)",
		C("^y$")
	]

	no = [
		# well actually no/nope/not/nah // not at all! never!!!
		C(r"(well )?(actually )?n(o+(pe)?t?|ah?)( at all)?( never)?"),
		C(rf"({PLEASE___} ?)?stop"),
		"never( ever)?",
	]

	created_program = [ # for "Who" Created you
		C(
			'(?P<action>' # save the action to use in reply
				'created?|'
				'program(?:med)?|'
				'invent(?:ed)?|'
				'design(?:ed)?|'
				'ma(?:d|k)e'
			') '
			f'{YOU___}'
		),
		C(
			f"{YOUR___} "
			"(?P<action>" #we only need the base verb
				"creat|"
				"programm?|"
				"invent|"
				"design|"
				"mak"
			")(?:o|e)?r"
		)
	]


I_Pattern = I_Pattern()

for p in I_Pattern.yeses:
	print(p)