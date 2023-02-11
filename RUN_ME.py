# not recommanded to run it IF YOU FEEL EXEC IS UNSAFE, RUN "src/App_server.py" DIRECTLY INSTEAD


import os
import sys

mainpyfile = os.path.dirname(os.path.abspath(__file__))+"/src/App_server.py"


sys.path[0] = os.path.dirname(mainpyfile)
sys.argv[0] = mainpyfile


def start(mainpyfile):
	import __main__
	
	tmp=__main__.__builtins__
	__main__.__dict__.clear()
	__main__.__dict__.update({"__name__"    : "__main__",
					  "__file__"    : mainpyfile,
					  "__builtins__": tmp,
					 })
	exec(open(mainpyfile).read(),  __main__.__dict__)
		
start(mainpyfile)
