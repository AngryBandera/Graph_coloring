'''
graph to knf
'''
def create_knf(
        graph: list[tuple[list[int], int]]) -> list[tuple[int, int]]:
    '''
    Converts a graph to his knf form

    >>> create_knf([([1,2],1),([0,3],0),([0,3],2),([1,2],0)])
    [(0, 2), (4, 5), (6, 7), (10, 11),\
 (12, 14), (16, 17), (18, 19), (22, 23),\
 (12, 15), (13, 16), (14, 17),\
 (12, 18), (13, 19), (14, 20),\
 (15, 21), (16, 22), (17, 23),\
 (18, 21), (19, 22), (20, 23),\
 (13, 13), (15, 15), (20, 20), (21, 21)]
    '''
    knf = []
    kolors = [0,1,2]
    # Блок Є#
    for node,info_node in enumerate(graph):
        pos_kolors_for_node = [kol for kol in kolors if kol != info_node[1]]
        knf.append((node*3+pos_kolors_for_node[0], node*3+pos_kolors_for_node[1]))
    #Блок НЕ#
    for node,info_node in enumerate(graph):
        pos_kolors_for_node = [kol for kol in kolors if kol != info_node[1]]
        knf.append((node*3+pos_kolors_for_node[0]+len(graph)*3,\
                    node*3+pos_kolors_for_node[1]+len(graph)*3))
    #Блок Об'єднання#
    connection_between_nodes = []
    for node,info_node in enumerate(graph):
        if tuple(sorted([node, info_node[0][0]])) not in connection_between_nodes \
            and tuple(sorted([node, info_node[0][1]])):
            connection_between_nodes+=[tuple(sorted([node,con_node])) for con_node in info_node[0]]
    for connection in connection_between_nodes:
        for kol in kolors:
            knf.append((connection[0]*3+kol+len(graph)*3,(connection[1]*3+kol+len(graph)*3)))
    #Умова змінності кольорів#
    for node,info_node in enumerate(graph):
        knf.append((node*3+info_node[1]+len(graph)*3, node*3+info_node[1]+len(graph)*3))
    return knf

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
