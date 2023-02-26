if __name__ == '__main__':
    a: list[int] = [1, 2, 5, 7, 9, 10, 11, 13]
    b: list[int] = [1, 5, 6, 7, 10, 12,14]  # 删掉2,9,11 新增6,12  不改变1,5,7,10,13
    # for item in list1:
    #     if item in list2:
    #         print(item.__str__() + '存在，不需要改变')
    #     else:
    #         print(item.__str__() + '不存在，删除')
    delete = [x for x in (a + b) if x not in b]
    print('删除' + delete.__str__())
    add = [i for i in b if i not in [x for x in a if x in b]]
    print('新增' + add.__str__())
