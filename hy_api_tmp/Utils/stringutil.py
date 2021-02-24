import random


class StringUtil:
    
    @staticmethod
    def random_phone_number(n):
        """
        随机生成11位手机号码方法
        :param n: 生成手机号码的数量
        :return: 手机号码的list
        """
        number_list = []
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                   "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        
        end = '0123456789'
        for i in range(n):
            number_list.append(random.choice(prelist) + ''.join(random.sample(end, 8)))
        # print(number_list)
        return number_list
       
    @staticmethod
    def random_chinese_str(n, lengh):
        """
        随机生成指定位数中文字符的方法
        :param n: 生成多少个长度为lengh的字符串
        :param lengh: 每个字符串的长度
        :return: 长度为length的字符串的list列表
        """
        str_list = []
        
        for i in range(n):
            strs = []
            for j in range(lengh):
                head = random.randint(0xb0, 0xf7)
                # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
                body = random.randint(0xa1, 0xf9)
                val = f'{head:x}{body:x}'
                strd = bytes.fromhex(val).decode('gb2312')
                strs.append(strd)
                j += 1
            str_list.append(''.join(strs))
            i += 1
        return str_list

        
if __name__ == '__main__':
    s = StringUtil()
    l = s.random_phone_number(1)
    print(l[0])
    # s.random_chinese_str(5, 1)