import error
import sys
import json
import os
def check_dependencies():
    global useos
    with open('dependencies.json') as file:
        rawdata=json.load(file)
    build_in_dependencies = rawdata["build-in-dependencies"]
    for dependencies in build_in_dependencies:
        if dependencies == "os":
            useos=True
        elif is_empty(dependencies):
            pass
        else:
            error.UnknowDependenciesError(f"not found this dependencies name {dependencies}")
            sys.exit()
def get_context(filename: str):
    with open(filename,"r") as file:
        context: list=file.read().splitlines()
    return context
stack_var=[]
if_stack=[]
def check_type(value, pc):
    # Check if it's an integer
    if value.isdigit():
        return "int"
    # Check if it's a float
    elif is_float(value):
        return "float"
    if value.startswith("math("):
        return "math"
    elif value.startswith("input("):
        return "input"
    elif value.startswith("os.getcwd("):
        return "os.getcwd"
    else:
        value = str(value)
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                return "str"
            else:
                error.SyntaxError(f"""'"' expected in end""", line_number=pc)
                sys.exit()
        elif value == "True" or value == "False":
            return "bool"
        else:
            error.UnknownTypeError("The specified data type is not recognized", line_number=pc)
            sys.exit()

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    return type
def get_string_context(string):
    string=string[1:-1]
    return string
def Input(line,pc):
    n,text=line.split("input(",1)        
    text=text.replace(")", "",-1)
    text_type=check_type(text,pc)
    if text_type == "str":
        text=get_string_context(text)
        r=input(text)
        return f'"{r}"'
    elif text_type == "bool":
        r=input(text)
        return r
    elif text_type == "int":
        r=input(text)
        return r
    elif text_type == "float":
        r=input(text)
        return r
    elif text_type == "math":
        expression = text.replace("math(", "").replace(")", "").replace("Print",'')  # Extract the expression
        result = math(expression)
        r=input(result)
        return r
def Print(line,pc):
    n,text=line.split("Print(",1)        
    text=text.replace(")", "",-1)
    text_type=check_type(text,pc)
    if text_type == "str":
        text=get_string_context(text)
        print(text)
    elif text_type == "bool":
        print(text)
    elif text_type == "int":
        print(text)
    elif text_type == "float":
        print(text)
    elif text_type == "math":
        expression = text.replace("math(", "").replace(")", "").replace("Print",'')  # Extract the expression
        result = math(expression)
        print(result)
def is_empty(string):
    if string==" " or string=="\t" or string=="":
        return True
    else:
        return False
def concatenate(str1,str2):
    str1=get_string_context(str1)
    str2=get_string_context(str2)
    return str1+str2
def math(expression):
    expression=expression.replace("Print(","").replace("math(", "").replace(")", "")
    print(expression)
    allowed_operators = '+-*/%'
    allowed_chars = set('.)(0123456789 ' + allowed_operators)
    if all(char in allowed_chars for char in expression):
        if any(op in expression for op in allowed_operators):
            try:
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"Error: {e}"
        else:
            return "Expression does not contain any allowed operators."
    else:
        error.InvalidCharactersError("Invalid characters or operators in the expression.")
        sys.exit()
def make_str(value):
    return f"'{value}'"    
def code(context: list):
    global useos
    pc=1
    for line in context:
        line=str(line)

        if line.endswith(";") or is_empty(line):
            line=line.replace(";",'')
        else:
            error.SyntaxError(f"""';' expected in end""", line_number=pc)
            sys.exit()
        for var_type,var_name,var_value in stack_var:
            line=line.replace(var_name,var_value)
        if line.startswith("//"):
           continue
        if line.startswith("input("):
            Input(line,pc)
            pc+=1
            continue
        if line.startswith("var"):    
            line=line.replace("var ","",1)
            name,value = line.split("=")
            name=name.strip()
            line=line.replace(f"{name} =",'')
            var_type=None
            if value[0] ==' ':
                value=value.replace(" ","",1)
            var_type=check_type(value,pc)
            if var_type == "math":
                value = math(value)
            elif var_type == "input":
                value=Input(value,pc)
            elif var_type == "os.getcwd" and useos==True:    
                value=make_str(value.replace(f'os.getcwd(',os.getcwd()).replace(")",""))
            stack_var.append((var_type,name,value))
        if "math(" in line:
            result = math(line)
            line = line.replace(f"math({line})",f'"{result}"',1)
        if line.startswith("Print("):
            Print(line,pc)
            pc+=1
            continue
        if "os.getcwd(" in line and useos== True:
            line=line.replace(f'os.getcwd()',os.getcwd())
        pc+=1
def run(filename: str):
    global useos
    useos=False
    check_dependencies()
    context=get_context(filename)
    code(context)

if __name__ == "__main__":
    run("TEST/test.zs")