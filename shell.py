import lexer

print("Please input file name: ")
inputFile = input()
f = open(inputFile)
while True:
    text = f.read()
    result, error = lexer.run(text)

    result.reverse()
    while result:
        newResult = result.pop()
        print(newResult)
    exit()