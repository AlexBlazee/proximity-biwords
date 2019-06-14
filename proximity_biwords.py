

import os
import re
import collections

def boolean_query(query, dictionary):
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')
    results_stack = []
    
    postfix_queue = collections.deque(to_postfix(query))  
    print(postfix_queue)
    while postfix_queue:
        token = postfix_queue.popleft()
        result = []
        if (token != 'AND' and token != 'OR' and token != 'NOT'):
            #token = token.lower()
            if (token in dictionary):
                result = dictionary[token][1]
        
        elif (token == 'AND'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = Intersection(left_operand, right_operand)  

        
        elif (token == 'OR'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = Union(left_operand, right_operand)  

        elif (token == 'NOT'):
            right_operand = results_stack.pop()
            result = Not(right_operand)  

        results_stack.append(result)

    

    return results_stack.pop()


def to_postfix(infix_query):
 
    operator_priority = {}
    operator_priority['NOT'] = 3
    operator_priority['AND'] = 2
    operator_priority['OR'] = 1

    operator_priority['('] = 0
    operator_priority[')'] = 0

    output = []
    operator_stack = []


    for token in infix_query:


        if (token == '('):
            operator_stack.append(token)

        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()


        elif (token in operator_priority):
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and operator_priority[current_operator] > operator_priority[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token)


        else:
            output.append(token)

    while (operator_stack):
        output.append(operator_stack.pop())

    return output

def biwords(query,dictionary1):
    query=query.split(" ")
    biword_arr=[]
    for i in range(1, len(query)):
        word1 = query[i - 1] + " " + query[i]
        biword_arr.append(word1)
    queue_arr = biword_arr
    for i in range(len(biword_arr)-1):
        queue_arr.append("AND")
    results_stack = []
    print(queue_arr)
    postfix_queue = collections.deque(queue_arr)
    print(postfix_queue)
    while postfix_queue:
        token = postfix_queue.popleft()
        result = []
        if (token != 'AND'):
            token = token.lower()
            if (token in dictionary1):
                result = dictionary1[token][1]

        elif (token == 'AND'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = Intersection(left_operand, right_operand)


        results_stack.append(result)
    return results_stack.pop()


def Not(arr):
    full_arr=[]
    for i in range(1,50):
        full_arr.append(i)
    answer2=[word for word in full_arr if word not in arr]
    return answer2


def Union(arr1,arr2):
    answer1=[]
    intersected=Intersection(arr1,arr2)
    temp1 = [word for word in arr1 if word not in intersected]
    temp2 = [word for word in arr2 if word not in intersected]
    answer1=intersected+temp1+temp2
    answer1.sort()
    return answer1


def Intersection(arr1,arr2):
    if(not arr1):
        return arr1
    if(not arr2):
        return arr2
    answer=[]
    temp1=list(arr1)
    temp1.sort()
    temp2=list(arr2)
    temp2.sort()
    flag1=0
    flag2=0
    p1=0
    p2=0
    while True:
        if p1==len(temp1)-1:
            flag1=1
        if p2==len(temp2)-1:
            flag2=2
        if(temp1[p1]==temp2[p2]):
            answer.append(temp1[p1])
            p1+=1
            p2+=1
            if (flag2 == 2):
                break
            if (flag1 == 1):
                break
        elif(temp1[p1]>temp2[p2]):
            p2+=1
            if(flag2==2):
                break
        else:
            p1+=1
            if(flag1==1):
                break
    return answer



def proximity_intersect(word1, word2, disty):
    answer = []
    data_info_1 = posting_list1[word1][1]
    data_info_2 = posting_list1[word2][1]

    i = 0
    j = 0

    while ( i < len(data_info_1) and j < len(data_info_2)):
        document_id_1 = data_info_1[i][0]
        document_id_2 = data_info_2[j][0]
        if ( document_id_1 == document_id_2):
            pos_res_list = []
            pos_list_1 = data_info_1[i][1]
            pos_list_2 = data_info_2[j][1]


            for k1 in range(len(pos_list_1)):
                for l1 in range(len(pos_list_2)):
                    distance = abs(pos_list_1[k1] - pos_list_2[l1])
                    if(disty>=distance):
                        pos_res_list.append(l1)
                    elif(distance>disty):
                        break
                for item in pos_res_list:
                    answer.append({ "document ID" : document_id_1,  "position data 1" : pos_list_1[k1]  ,  "position data 2" : pos_list_2[item] }  )
                pos_res_list.clear()

            i = i + 1
            j = j + 1
        else:
            if document_id_1 < document_id_2:
                i = i + 1
            else:
                j = j + 1

    return answer

# main function

os.chdir(r"D:\Desk\BB\Sem 6\Information retrieval\files") # C:\Users\Rithvik Sallaram\Desktop\Acad_Stuff\Information retrieval
doc_name = "0.txt"
posting_list={}
posting_list1={}
temp={}
wordnum =0

# posting list and positional list making

for i in range(1,6):
    wordnum=0
    doc_name=doc_name.replace(str(i-1),str(i))
    fh = open(doc_name,'r')
    for line in fh:
        doc_list=[]
        arr=list(re.findall(r"[\w']+", line))
        for word in arr:
            wordnum+=1
            word = word.lower()
            if word not in temp:
                temp[word]=[]
                temp[word].append(1)
                temp[word].append([])
                temp[word][1].append(i)

                posting_list1[word]=[]
                posting_list1[word].append(1)
                posting_list1[word].append([])
                posting_list1[word][1].append([])
                posting_list1[word][1][0].append(i)
                posting_list1[word][1][0].append([])
                posting_list1[word][1][0][1].append(wordnum)

            else:
                if(not temp[word][1].__contains__(i)):
                    temp[word][0]+=1
                    temp[word][1].append(i)
                    posting_list1[word][0] += 1
                    posting_list1[word][1].append([])
                    posting_list1[word][1][len(posting_list1[word][1])-1].append(i)
                    posting_list1[word][1][len(posting_list1[word][1]) - 1].append([])
                posting_list1[word][1][len(posting_list1[word][1]) - 1][1].append(wordnum)


fh.close()

# biword dictionary
doc_name = "0.txt"
temp1={}
word1=""
for i in range(1,6):
    doc_name=doc_name.replace(str(i-1),str(i))
    fh = open(doc_name,'r')
    for line in fh:
        doc_list=[]
        arr1=list(re.findall(r"[\w']+", line))
        for j in range(1,len(arr1)):
            word1 = arr1[j-1]+" "+arr1[j]
            word1=word1.lower()
            if word1 not in temp1:
                temp1[word1]=[]
                temp1[word1].append(1)
                temp1[word1].append([])
                temp1[word1][1].append(i)
            else:
                if(not temp1[word1][1].__contains__(i)):
                    temp1[word1][0]+=1
                    temp1[word1][1].append(i)


fh.close()

#start execution

print(temp)
print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print(temp1)
x=0
while (x!=-1):
    x=int(input())
    if(x==1):
        print("Enter proximity query, Enter two words followed by their distance of seperation")
        input1 = input()
        input2 = input()
        proximity = int(input())
        results = proximity_intersect(input1, input2, proximity)
        print ("Results : ")
        for res in results:
            print ("Document id :" , res["document ID"] ,  " Position 1: " , res["position data 1" ], " Position 2 :", res["position data 2" ])
    if(x==2):
        while(True):
            str = input()
            if(str=="!"):
                break
            print(boolean_query(str,temp))
        print("ADITIONAL DETAILS")
        print("Total number of words in dictionary : ",len(temp))
        print("Total documents : 49")

    if(x==3):
        while True:
            str1 = input()
            str1=str1.lower()
            if(str1=="!"):
                break
            for i in range(len(posting_list1[str1][1])):
                try:
                    print("Document"+" "+str(posting_list1[str1][1][i][0]))
                    print(posting_list1[str1][1][i][1])
                except:
                    print("No such key exists, try again")
    if(x==4):
        while True:
            str2 = input()
            if(str2=="!"):
                break
            print(biwords(str2, temp1))
        print("ADITIONAL DETAILS")
        print("Total number of words in dictionary : ", len(temp1))
