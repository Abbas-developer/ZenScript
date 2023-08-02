import sys
import interpreter
try:
    filename=sys.argv[1]
except IndexError:
    print("""
Error: Program is terminated 
please used ZenScript.exe filename.zs """)
    sys.exit()
interpreter.run(filename)