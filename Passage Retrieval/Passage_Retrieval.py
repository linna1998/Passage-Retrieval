#! /usr/bin/env python3.6
# coding=utf-8
def ReadFile(filename):
    f = open(filename, 'r')
    list_ret = list()
    for f_line in f.readlines():    
        f_line = f_line.split('。')
        for s_str in  f_line:
            if '？' in s_str:
                list_ret.extend(s_str.split('？'))
            elif '！' in s_str:
                list_ret.extend(s_str.split('！'))           
            else:
                list_ret.extend(s_str.split('。'))                              
    f.close()
    return list_ret  

key_word = ["苏德互不侵犯条约"]
list_sentence = ReadFile('1.txt')           
for sentence in list_sentence:
