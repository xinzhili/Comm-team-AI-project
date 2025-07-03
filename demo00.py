import torch
import numpy as np
import timeit

def test01():
    print("pytorch示例")
    #创建张量
    x = torch.tensor([1.,2.,3.])
    y = torch.tensor([4.,5.,6.])
    print(f"x = {x}")
    print(f"y = {y}")
    #张量运算
    z = x+y
    print(f"z = {z}")

def test02():
    #python List
    #可混合存储不同类型
    py_list = [1, 2, 3, 4.5, "hello"]
    #通过循环遍历元素（3种方式）
    for element in py_list:
        print(element)
    for i in range(len(py_list)):
        print(py_list[i])
    for index,element in enumerate(py_list):
        print(f"索引：{index},元素：{element}")

def test03():
    #Numpy同构元素，元素类型必须一致
    arr1 = np.array([1, 2, 3])#整数数组
    arr2 = np.array([1.2, 3.4, 5.6])#浮点型数组
    arr3 = np.array([1, 2.3, "hello"])#自动转换成字符串

    print("arr1 dtype",arr1.dtype)
    print("arr2 dtype",arr2.dtype)
    print("arr3 dtype",arr3.dtype)
    
    #固定维度，1D向量，2D矩阵
    vec = np.array([1, 2, 3])
    mat = np.array([[1, 2, 3],[4, 5, 6]])
    print("vec shape",vec.shape)
    print("mat shape",mat.shape)
    

def test04():
    #Numpy内存连续，计算效率高(对比python List)
    # 创建大型数组/列表
    #np_array = np.arange(1000000)
    #py_list = list(range(1000000))
    # timeit 模块来比较NumPy数组向量化操作和Python列表循环操作的性能差异。
    
    numpy_time = timeit.timeit(
    stmt='np_array + 1',                
    setup='import numpy as np; np_array = np.arange(100000)',  
    number=1000                         
    )
    '''
    stmt:要测试的代码语句，这里是 np_array + 1,表示对 NumPy 数组的每个元素加 1。
    setup:在执行测试代码前运行的初始化代码,这里导入 numpy 并创建一个包含 1000000 个整数的数组。
    number:指定测试代码的执行次数（这里是 1000 次）。
    timeit.timeit() 返回的是 number 次执行的总耗时（秒），因此需要除以 number 得到每次执行的平均耗时。
    '''
    list_time = timeit.timeit(
    stmt='[x+1 for x in py_list]',      
    setup='py_list = list(range(100000))',  
    number=1000                        
    )
    print(f"NumPy 操作耗时: {numpy_time/1000:.6f} 秒/次")  # 计算每次操作的平均耗时
    print(f"列表操作耗时: {list_time/1000:.6f} 秒/次")  # 计算每次操作的平均耗时

def test05():
    #Numpy和List之间的关系
    #List 是 NumPy 数组的 “基础”，NumPy 数组可从 List 创建
    arr = np.array([1, 2, 3])
    print("arr:",arr)
    print(arr.dtype)
    #NumPy 数组可通过.tolist()方法转回 List
    print(arr.tolist())
    print(arr.dtype)
#Tensor和NumPy数组的转换之后会详细讲解

if __name__ == '__main__':
    #test01()
    #test02()
    #test03()
    test04()
    #test05()
