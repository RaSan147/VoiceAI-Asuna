from REGEX_TOOLS import re_check, re_is_in, re_starts
from basic_conv_re_pattern import C,  merge, check_context

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge

pattern =[
[
	C("((yo)?u|y(a|o))('| )?(a?re?)? ((cool|great|nice|wow|awesome|amazing) ?)+(app|stuff|code)"),
	(Rchoice("😇", "😁", "😽")+ " " +
	Rchoice("Hehe", "Yay")+"!"
	),
	"praise_bot"
],
	


]