
# Import Regular Expressions (Regex)
import re

# Stack holds values and acts as memory for calculations
stack = []

# Maximum and minimum values for saturation
max_sat = 2147483647
min_sat = -2147483648

# Psuedo-random counter
count = 22
r_list = [1804289383, 521595368, 35005211, 1303455736, 304089172, 1540383426, 1365180540, 1967513926, 2044897763, 1102520059, 783368690, 1350490027, 1025202362, 1190641421, 596516649, 1649760492, 719884386, 424238335, 1957747793, 1714636915, 1681692777, 846930886, 1804289383]

# RegEx
negative_number = r'^-[0-9]+'
operands = r'-?[0-9]+'
operators = r'[+-/*%^dr]'

# Comment switch - False = off
is_commenting = False


def main():
    """Provides a continuous ability to input for the user and processes the input on every user 'Enter' command"""
    
    while True:
        try:
            inp = process_user_input()
            operator_or_operand(inp)
        except:
            exit(0)


def operator_or_operand(inp):
    """Process each item in input depending on whether its an operator, 
    operand, or a special function"""

    global is_commenting
    for i, item in enumerate(inp):
                if item == '#':
                    is_commenting = not is_commenting
                    continue
                elif item == "^=":
                    print(stack[-1])
                    process_operator('^')
                elif re.match(operands, item) != None:
                    stack_append(item)
                elif is_commenting == False:
                    process_operator(item)
                else:
                    continue


def process_user_input():
    """Take user input as a string and split it into an array of operators or operands for 
    processing. This stage will separate negative numbers from the minus operator and catches the special command '^='. 
    The array will then be sent to be cleaned of any space characters"""

    user_in = input()
    split = re.split(r'(^-[0-9]+|\^=|\D)', user_in)
    return remove_spaces_from_input(split)


def remove_spaces_from_input(list):
    """Remove any superfluous spaces or null characters from the input list"""

    return [value for value in list if value != '' and value != ' ']


def operate_on_the_stack(operator):
    """The 6 main operators require the last 2 stack items to be removed, 
    operated on and their result added to the stack. 
    Saturation levels are checked before the operation is added to the stack"""

    y = int(stack.pop())
    x = int(stack.pop())
    if operator == "+":
        result = x+y
    elif operator == "-":
        result = x-y
    elif operator == "*":
        result = x*y
    elif operator == "/":
        result = int(x/y)
    elif operator == "^":
        result = x**y
    elif operator == "%":
        result = x%y
    res = check_saturation(result)
    stack_append(res)



def process_operator(item):
    """Find which operator, if any, has been given and process it, it if it exists and it will not cause an error. 
    If it doesn't exist or processing is not possible register an error for the user"""
    
    if item == "+" or item == "-" or item == "*" or item == "^" or item == "%" or item == "/":
        check = check_stack_min()
        if check == True:
            if item == "/" and (stack[-1] == '0' or stack[-1] == 0):
                print("Divide by 0.")
            else:
                operate_on_the_stack(item)
        else: return
    elif item == "=":
        if len(stack) == 0:
            print("Stack empty.")
        else:
            print(stack[-1])
    elif item == 'd':
        if len(stack) == 0:
            print(min_sat)
        else:
            for i in stack:
                print(i)
    elif item == 'r':
        stack_append(create_random())
    else:
        for i in item:
            print(f"""Unrecognised operator or operand "{i}".""")


def stack_append(num):
    """Check for Stack Overflow and append to the stack only if there is space"""

    if len(stack) >= 23:
        print("Stack overflow.")
        return
    else:
        stack.append(num)
        return


def check_stack_min():
    """An operator cannot operate with less than 2 items in the stack,
        check for Stack Underflow but allow a Psuedo random number to be be added"""

    if len(stack) < 2 and stack[0] != 1804289383:
        print("Stack underflow.")
        return False
    else:
        return True
        

def check_saturation(result):
    """Values produced by the calculator are limited by minimum and maximum saturation values"""
    
    if result > max_sat:
        return max_sat
    elif result < min_sat:
        return min_sat
    else:
        return result

def create_random():
    """Psuedo random nubers are generated from a predefined list"""

    global count
    if count >= 0:
        count -= 1
        return r_list[count + 1] 
    else:
        return r_list[0]
    
print("You can now start interacting with the SRPN calculator")
main()

