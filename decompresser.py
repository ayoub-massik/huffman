


text=""
def dec(ls):
    global text
    if ls:
        for i in d:
            if d[i]==ls[:len(d[i])]:
                text+=str(i)
                dec(ls[len(d[i]):])
    return text
def decrypt(bint,binl,listt):
    global d
    global text
    text=""
    d={}
    for i in range(len(binl)):
        d[listt[i]]=binl[i]
    dec(bint)
    return text
