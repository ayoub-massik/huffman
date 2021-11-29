class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d
def calcbin(freq):
    nodes=freq
    while len(nodes)>1:
        (key1,c1)=nodes[-1]
        (key2,c2)=nodes[-2]
        nodes=nodes[:-2]
        node=NodeTree(key1,key2)
        nodes.append((node,c1+c2))
        nodes=sorted(nodes,key=lambda x:x[1],reverse=True)
    huffmanCode=huffman_code_tree(nodes[0][0])
    return huffmanCode
def compteur(fileName):
    texte=str()
    with open(fileName, encoding='utf8') as poeme:
        for ligne in poeme:
            texte+=ligne.replace('\n','')
    D,P={},{}
    compteur=0
    for c in texte:
        if c not in D:
            D[c]=1
        else:
            D[c]+=1
        compteur+=1
    D=sorted(D.items(),key=lambda colonne:colonne[1],reverse=False)
    for i in D:
        P[i[0]]=i[1]/compteur
    return D,P