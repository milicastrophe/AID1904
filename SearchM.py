import numpy as np
import copy as cp


class SFun:
    @staticmethod
    def extend(M):
        """
            to be demotion 1
        """
        list_1D = []
        for each in M:
            list_1D += list(each)
        return list_1D

    @staticmethod
    def judge_o(m1):
        j0 = 0
        xl = SFun.extend(m1)
        xl.remove(0)
        for i in range(len(xl)):
            for j in range(i):
                if xl[j] < xl[i]:
                    j0 += 1
        return j0 % 2

    @staticmethod
    def judge_odevity(m1):
        jo = 0
        for row in range(len(m1)):
            for col in range(len(m1)):
                for index_row in range(row + 1):
                    for index_col in range(col + 1):
                        if m1[row, col] > m1[index_row, index_col]:
                            jo += 1
        return jo % 2

    @staticmethod
    def judgeSolve(m1, m2):
        if SFun.judge_o(m1) == SFun.judge_o(m2):
            return True
        return False

    @staticmethod
    def equal_M(m1,m2):
        for row in range(len(m1)):
            for col in range(len(m1)):
                if m1[row,col] != m2[row,col]:
                    return False
        return True


class SpMatrix:
    def __init__(self, scale):
        self.scale = int(scale)
        # 需要输出的量
        self.__fill_list = [0] + list(range(int(self.scale ** 2) - 1, 0, -1))

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale = value

    def dim2(self):
        """
            take the fill_list full fill into matrix around center as a snake

        """
        m = self.scale - 1
        tem_M = np.zeros((self.scale, self.scale))
        for i in range(self.scale // 2):
            for j in range(i, m - i):
                tem_M[i, j] += self.__fill_list.pop()
            for j in range(i, m - i):
                tem_M[j, m - i] += self.__fill_list.pop()
            for j in range(i, m - i):
                tem_M[m - i, m - j] += self.__fill_list.pop()
            for j in range(i, m - i):
                tem_M[m - j, i] += self.__fill_list.pop()
        return tem_M


class Point:
    """description :the point which is a 2 D Matrix full fill by
    (self width) **2 numbers from 0to width**2-1,it could change
    by exchange the zero and zero's neighborhood  to the target point as
      example :
      change
    [ [1,0,3],
      [8,2,4],
      [7,6,5]]
     to
       [[1,2,3],
        [8,0,4],
        [7,6,5]]
     every times the zero could move 1 step
     """

    def __init__(self, xlist=None, mother=None):
        """
            include width ,matrix_x,address,mather_address
        """
        self.xlist = xlist
        self.mother = mother
        self.matrix = self.xlist.dim2

    @property
    def xlist(self):
        return self.__xlist

    @xlist.setter
    def xlist(self, mtx):
        if isinstance(mtx, XList):
            self.__xlist = mtx

    def judge_in(self, sth_list):
        """
            judge the point in list yes or not
        """
        for each in sth_list:
            if self.xlist == each.xlist:
                return True
        return False

    def have_baby(self, direct):  # 繁殖
        """
            according direction to born the son point
        """
        n_xlist = self.xlist.exchange(direct)
        if n_xlist is not None:
            return Point(n_xlist)


class XList:
    def __init__(self, my_list):
        self.num_list = my_list
        self.dim2 = self.__dim2()

    def __eq__(self, other):
        if self.num_list == other.num_list:
            return True
        return False

    @property
    def num_list(self):
        return self.__num_list

    @num_list.setter
    def num_list(self, mylist):
        if isinstance(mylist, list):
            self.__num_list = mylist

    def __dim2(self):  # 矩阵
        """
            to be a 2D Matrix
        """
        width = self.get_width()
        M = np.zeros((width, width))
        for row_i in range(width):
            for col_i in range(width):
                M[row_i, col_i] += self.__num_list[col_i + row_i * width]
        return M

    def get_width(self):
        if len(self.__num_list):
            de_width = int(len(self.__num_list) ** (1 / 2))
            return de_width

    def site(self):
        """
        to find matrix 's 0 's position
        """
        M = self.__dim2()
        if len(np.argwhere(M == 0)) == 1:
            return tuple(np.argwhere(M == 0)[0])

    def exchange(self, drct):
        """
        生成一个新的列表,同时对是否可以传参进行判定
        """
        M = cp.deepcopy(self.__dim2())
        ps = self.site()
        u, v = ps[0] + drct[0], ps[1] + drct[1]
        if u in range(self.get_width()) and v in range(self.get_width()):
            M[ps], M[u, v] = M[u, v], M[ps]
            new_list = SFun.extend(M)
            return XList(new_list)
        return


class PointController:
    """
        only to control the add or del point
    """

    def __init__(self, width):
        self.open_list = []
        self.close_list = []
        self.direct = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.width = width

        self.target = SpMatrix(self.width).dim2()

    def add_open(self, point):
        self.open_list.append(point)

    def add_close(self, point):
        self.close_list.append(point)

    def propagate(self):
        """
             core code:to born the new point and make them iterable
        """
        while True:
            for index in range(len(self.open_list) - 1, -1, -1):  # mother 是一个点
                mother = self.open_list.pop(index)
                for evone in self.direct:
                    son_point = mother.have_baby(evone)
                    if son_point != None:
                        son_point.mother = mother
                        if  SFun.equal_M(son_point.xlist.dim2,self.target):
                            print(son_point.xlist.dim2)
                            self.recall_path(son_point)
                            return
                        elif not son_point.judge_in(self.close_list) and not son_point.judge_in(self.open_list):
                            self.add_open(son_point)
                self.add_close(mother)

    def recall_path(self, point):
        if point.mother == None:

            print("start is\n",point.xlist.dim2)
        else:
            print(point.xlist.site(), "<==", end='')
            self.recall_path(point.mother)


class InterView:
    def __init__(self):
        self.__u_list = []
        self.__scale = self.usr_width()

    def get_scale(self):
        return self.__scale

    def get_x(self):  # 输出
        return self.__u_list

    def usr_width(self):
        w = self.judge_illegal("请输入矩阵的宽度：")
        return w

    def get_usr_num(self):
        """collect the user's number"""

        x = self.judge_illegal("请输入数字:")
        self.__u_list.append(x)
        print("当前用户列表为：", self.__u_list)

    def fill_list(self):
        w = self.__scale
        for index in range(w * w):
            self.get_usr_num()

    def judge_illegal(self, str_ill):
        while True:
            x = input(str_ill)
            try:
                x = int(x)
                return x
            except Exception:
                continue

    def main(self):
        width = self.__scale
        self.fill_list()
        temp_list = self.__u_list
        pc = PointController(width)
        if SFun.judgeSolve(pc.target, XList(temp_list).dim2):
            xl = XList(temp_list)
            star = Point(xl)
            pc.add_open(star)
            pc.propagate()
        else:
            print("与目标矩阵的奇偶性不同,问题无解")
#x = [8,1,2,7,6,3,5,4,0]用来检验

iv = InterView()
iv.main()


