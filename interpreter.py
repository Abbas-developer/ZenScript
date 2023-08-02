import error
import sys
import json
import socket
def check_dependencies():
    global usesocket
    with open('dependencies.json') as file:
        rawdata=json.load(file)
    build_in_dependencies = rawdata["build-in-dependencies"]
    for dependencies in build_in_dependencies:
        if dependencies == "socket":
            usesocket=True
        else:
            error.UnknowDependenciesError(f"not found this dependencies name {dependencies}")
            sys.exit()
def get_context(filename: str):
    with open(filename,"r") as file:
        context: list=file.read().splitlines()
    return context
stack_var=[]
def check_type(value,count):
    type=None
    if value.startswith('"') or value.startswith("'"):
        if value.endswith('"') or value.endswith("'"):
            type="str"
        else:
            error.SyntaxError(f"""'"' expected in end""", line_number=count)
            sys.exit()
    else:
        error.UnknowTypeError("The specified data type is not recognized",line_number=count)
        sys.exit()

    return type
def get_string_context(string):
    string=string[1:-1]
    return string
def Print(line,count):
    n,text=line.split(" ",1)
    text_type=check_type(text,count)
    if text_type == "str":
        text=get_string_context(text)
        print(text)
def code(context: list):
    count=1
    for line in context:
        if line.endswith(";") or line==" " or line=="\t":
            line=line.replace(";",'')
        else:
            error.SyntaxError(f"""';' expected in end""", line_number=count)
            sys.exit()
        for var_type,var_name,var_value in stack_var:
            line=line.replace(var_name,var_value)
        if line.startswith("//"):
           continue
        if line.startswith("Print"):
            Print(line,count)
            count+=1
            continue
        elif line.startswith("var"):    
            line=line.replace("var ","",1)
            name,value = line.split("=")
            name=name.strip()
            var_type=None
            if value[0] ==' ':
                value=value.replace(" ","",1)
            var_type=check_type(value,count)
            stack_var.append((var_type,name,value))
        elif line.startswith("socket.send") and usesocket:
            n,data = line.replace("socket.send ","",1)
            type=check_type(data,count)
            if type == "str":
                data=get_string_context(data)
            socket.socket.send(data)
        count+=1

def run(filename: str):
    usesocket=False
    check_dependencies()
    context=get_context(filename)
    code(context)
