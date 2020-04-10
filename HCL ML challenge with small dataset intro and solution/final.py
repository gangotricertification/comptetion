import nltk
import pandas as pd
import os
import string
import html

def preprocess(path,filee):
    raw_data = open(path+filee).read()

    d= raw_data.split('\n')
    check = d
    index = 0

    req_line_for_year = index
    for i in range(index+1, len(d)):
        if d[i].find('2018') >-1 or d[i].find('2019') >-1 or d[i].find('2020') >-1:
            req_index_for_year= i
            break


    req_index_start = req_index_for_year
    for i in range(req_index_for_year, req_index_for_year+6):
        if(d[i].find('£')>-1):
            req_index_start=i+1
            break


    req_index_end =-1
    for i in range(req_index_start, len(d)):
        if(d[i].find('STATEMENTS')>-1 or d[i].find('For')>-1 or d[i].find('The')>-1):
                req_index_end = i
                break
            
    d = d[req_index_start: req_index_end]

    dt= []
    for i in d:
        s =' '.join(i.split())
        dt.append(s.split(' '))


    def yearcheck(check):
        if check[0].find('2018') > -1:
            year = 2018
            return year
        if check[0].find('2019') > -1:
            year = 2019
            return year
        if check[0].find('2020') > -1:
            year = 2020
            return year

    year = yearcheck(check)

    punctuations1 = '!"#$%&\'*+,-./;<=>?@[\\]^_`{|}~'
    for i,v in enumerate(dt):
            for ii,vv in enumerate(v):
                npp = ""
                for iii,vvv in enumerate(vv):
                    if vvv not in punctuations1:
                        npp = npp + vvv
                dt[i][ii] = npp



    bol = True
    while(bol):
        a = 0
        count = 0
        for i in range(0,len(dt)-1):
            try:
                count = count+1
                if type(int(dt[i+1][0])) == int:
                    dt[i].insert(len(dt[i]),dt[i+1][0])
                    dt[i+1].pop(0)
                    a =0
            except ValueError:
                pass
            except IndexError:
                for i,v in enumerate(dt):
                    if v == []:
                        dt.pop(i)

        for j in range(0,len(dt)-1):
            try:
                if type(int(dt[j+1][0])) == int:
                    a = 1
            except ValueError:
                pass
            except IndexError:
                for i,v in enumerate(dt):
                    if v == []:
                        dt.pop(i)

        if a == 0:
            bol = False


    punctuations = '!"#$%&\'()*+,-./;<=>?@[\\]^_`{|}~'
    def remove_punctuation(key):
        s= ""
        a="("
        for c in key:    
            if c not in punctuations:
                s = s+ c
        if a in key:
            
            return str(int(s) * -1)
        else:
            return s


    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','']
    def finall(year):        
        final_list = []
        final_list_value = []
        numbers = ['1','2','3','4','5','6','7','8','9','0','(',')']
        if year == 2018:
            for i in dt:
                if (i[-1] != ""):
                    #if i[-1][0] not in alphabets or i[-1][1] in alphabets:
                    if i[-1][0] not in alphabets:
                        alpha = ""
                        for j in range(0,len(i)-1):
                            if j  not in numbers:
                                alpha = alpha + i[j]
                                alpha = alpha + " "
                        final_list.append(alpha.strip())
                        final_list_value.append('nan')
                else:
                    alpha = ""
                    for j in range(0,len(i)):
                        if j  not in numbers:
                            alpha = alpha + i[j]
                            alpha = alpha + " "
                    final_list.append(alpha.strip())
                    final_list_value.append('nan')


        if year == 2019:
            a=b=0
            if check[1].find('2019') >-1:
                a = 1
            if check[1].find('2018') >-1:
                b = 1
            option = a*1 + b*2
            if option == 2:
                for i in dt:
                    alpha = ""
                    if (i[-1] != ""):
                        #if i[-1][0] not in alphabets or i[-1][1] in alphabets:
                        if i[-1][0] not in alphabets:
                            for j in range(0,len(i)-1):
                                if j not in numbers:
                                    alpha = alpha + i[j]
                                    alpha = alpha + " "
                            final_list.append(alpha.strip())
                            final_list_value.append('nan')
                    else:
                        for j in range(0,len(i)):
                            if j  not in numbers:
                                alpha = alpha + i[j]
                                alpha = alpha + " "
                        final_list.append(alpha.strip())
                        final_list_value.append('nan')
            
            if option == 0:
                for i in dt:
                    alpha = ""
                    for j in range(0,len(i)): 
                        alpha = alpha + i[j]
                        alpha = alpha + " "
                    final_list.append(alpha)
                    final_list_value.append('nan')
            
            if option == 1:
                for i in dt:
                    alpha = ""
                    num=""
                    if (i[-1] != ""):
                        if i[-1][0] not in alphabets:
                        #if i[-1][0] not in alphabets or i[-1][1] in alphabets:
                            for j in range(0,len(i)-1):
                                alpha = alpha + i[j]
                                alpha = alpha + " "
                            final_list.append(alpha.strip())
                            aa=remove_punctuation(i[-1])
                            final_list_value.append(aa)
                    else:
                        for j in range(0,len(i)):
                            alpha = alpha + i[j]
                            alpha = alpha + " "
                        final_list.append(alpha.strip())
                        final_list_value.append('nan')
            if option == 3:
                
                for i in dt:
                    alpha = ""
                    num=""
                    if(len(i)<2):
                        final_list.append(i[0])
                        final_list_value.append('nan')
                    else:
                        if (i[-1] != "" and i[-2] != ""):

                            
                            #if (i[-1][0] not in alphabets or i[-1][1] not in alphabets) and (i[-2][0] not in alphabets or i[-2][1] not in alphabets):
                            if (i[-1][0] not in alphabets) and (i[-2][0] not in alphabets):
                                for j in range(0,len(i)-2):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                aa=remove_punctuation(i[-1])
                                final_list_value.append(aa)
                            #elif (i[-1][0] not in alphabets or i[-1][1] not in alphabets) and (i[-2][0] in alphabets or i[-2][1] in alphabets):
                            elif (i[-1][0] not in alphabets) and (i[-2][0] in alphabets):
                                for j in range(0,len(i)-1):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                final_list_value.append('nan')
                            else:
                                for j in range(0,len(i)):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                final_list_value.append('nan')
                        else:
                            for j in range(0,len(i)-2):
                                if j not in numbers:
                                    alpha = alpha + i[j]
                                    alpha = alpha + " "
                            final_list.append(alpha.strip())     
                            aa=remove_punctuation(i[-2])
                            final_list_value.append(aa)
            
        if year == 2020:
            a=b=0
            if check[1].find('2020') >-1:
                a = 1
            if check[1].find('2019') >-1:
                b = 1
            option = a*1 + b*2

            if option == 2:
                for i in dt:
                    if (i[-1] != ""):
                        #if i[-1][0] not in alphabets or i[-1][1] not in alphabets:
                        if i[-1][0] not in alphabets:    
                            if type(int(i[-1])) == int:
                                alpha = ""
                                for j in range(0,len(i)-1):
                                    if j not in numbers:
                                        alpha = alpha + " "
                                        alpha = alpha + j
                                final_list.append(alpha)
                                final_list_value.append('nan')
                    else:
                        alpha = ""
                        for j in range(0,len(i)):
                            if j not in numbers:
                                alpha = alpha + i[j]
                                alpha = alpha + " "
                        final_list.append(alpha)
                        final_list_value.append('nan')
            
            if option == 0:
                for i in dt:
                    alpha = ""
                    for j in range(0,len(i)):
                        alpha = alpha + i[j]
                        alpha = alpha + " "
                    final_list.append(alpha)
                    final_list_value.append('nan')
            
            if option == 1:
                for i in dt:
                    alpha = ""
                    num=""
                    if (i[-1] != ""):
                        #if i[-1][0] not in alphabets or i[-1][1] not in alphabets:
                        if i[-1][0] not in alphabets:
                            for j in range(0,len(i)-1):
                                if j not in numbers:
                                    alpha = alpha + i[j]
                                    alpha = alpha + " "
                            final_list.append(alpha)
                            aa=remove_punctuation(i[-1])
                            final_list_value.append(aa)
                    else:
                        for j in range(0,len(i)):
                            if j not in numbers:
                                alpha = alpha + i[j]
                                alpha = alpha + " "
                        final_list.append(alpha)
                        final_list_value.append('nan')

            if option == 3:
                for i in dt:
                    alpha = ""
                    num=""
                    if(len(i)<2):
                        final_list.append(i[0])
                        final_list_value.append('nan')
                    else:
                        if (i[-1] != "" and i[-2] != ""):
                            #if (i[-1][0] not in alphabets or i[-1][1] in alphabets) and (i[-2][0] not in alphabets or i[-2][1] not in alphabets):              
                            if (i[-1][0] not in alphabets) and (i[-2][0] not in alphabets):              

                                for j in range(0,len(i)-2):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                aa=remove_punctuation(i[-1])
                                final_list_value.append(aa)
                            elif (i[-1][0] not in alphabets) and (i[-2][0] in alphabets):
                            #elif (i[-1][0] not in alphabets or i[-1][1] not in alphabets) and (i[-2][0] in alphabets or i[-2][1] in alphabets):

                                for j in range(0,len(i)-1):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                aa=remove_punctuation(i[-1])
                                final_list_value.append(aa)
                            else:
                                for j in range(0,len(i)):
                                    if j not in numbers:
                                        alpha = alpha + i[j]
                                        alpha = alpha + " "
                                final_list.append(alpha.strip())
                                final_list_value.append('nan')

                        else:
                            for j in range(0,len(i)):
                                if j not in numbers:
                                    alpha = alpha + i[j]
                                    alpha = alpha + " "
                            final_list.append(alpha.strip())
                            final_list_value.append('nan')
        return final_list,final_list_value


    final_list,final_listfinal_list_value = finall(year)

    for i in range(0,len(final_list)):
        final_list[i] = final_list[i].split(' ')


    for i in range(0,len(final_list)-1):
        try:
            d = final_list[i+1][0][0].isupper()
        except IndexError:
            d=False
        if (d == False):
            final_list[i].insert(len(final_list[i]),final_list[i+1][0])
            final_list[i+1].pop(0)



    for i,v in enumerate(final_list):
        if v ==[]:
            indi= i
            final_list.pop(i)
            final_listfinal_list_value.pop(i)

    for i,v in enumerate(final_list):
        final_list[i] = ' '.join(v)


    for i,v in enumerate(final_listfinal_list_value):
        if v == "":
            final_listfinal_list_value[i] = 'nan'


    #dictionary = {}
    #for i in range(len(final_list)):
    #    dictionary[final_list[i]] = final_listfinal_list_value[i]

    dictionary = {}
    for i in range(len(final_list)):
        dictionary[html.escape(final_list[i]).encode('ascii', 'xmlcharrefreplace').decode()] = html.escape(final_listfinal_list_value[i]).encode('ascii', 'xmlcharrefreplace').decode()
    return dictionary



path = './HCL ML Challenge Dataset/'
#files = os.listdir(path)
#filee = 'X8XX02N7.txt'
#dictionary = preprocess(path,filee)
#print(dictionary)

d = pd.read_csv("./Results1.csv")
for i in range(d.shape[0]):
    file_name = d.iloc[i]["Filename"]
    dictionary  = preprocess(path,file_name+".txt")
    d.loc[d["Filename"]==file_name,"Extracted Values"]=[dictionary]

d.to_csv("Results.csv",index = False)
