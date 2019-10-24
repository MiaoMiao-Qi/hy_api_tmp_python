
"""
中位数是有序列表中间的数。如果列表长度是偶数，中位数则是中间两个数的平均值。

例如，

[2,3,4] 的中位数是 3

[2,3] 的中位数是 (2 + 3) / 2 = 2.5

设计一个支持以下两种操作的数据结构：

void addNum(int num) - 从数据流中添加一个整数到数据结构中。
double findMedian() - 返回目前所有元素的中位数。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-median-from-data-stream
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
"""
author :jiyanjiao
date : 2019-10-21
"""


class MedianFinder:
    nuber_list = []
    sum = 0
    
    def __init__(self):
        """
        initialize your data structure here.
        """
       
    def addNum(self, num: int) -> None:
        self.nuber_list.append(num)
      
    def findMedian(self) -> float:
        nb = self.nuber_list
        oder_list = []
        le = len(nb)
        if le <=1:
            raise Exception("中位数至少需要两位数")
        for i in range(0, le):
            for j in range(i+1, le):
                if nb[j] < nb[i]:
                    tmp = nb[i]
                    nb[i] = nb[j]
                    nb[j] = tmp
            oder_list.append(nb[i])
            print(nb[i])
            i += 1
        oder_le = len(oder_list)
        if oder_le % 2 == 0:
            m1 = (oder_list[int(oder_le/2)]+oder_list[int(oder_le/2)-1])/2
        else:
            m1 = oder_list[int(oder_le/2)]
        print(m1)
        return m1

"""
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:

输入: [-2,1,-3,4,-1,2,1,-5,4],
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-subarray
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
"""
author:jiyanjiao
date :2019-10-21
"""


class Solution:
    max_index = 0   # 子数组和最大的索引
    max_sum = 0     # 子数组和的最大值
    sum_list = []   # 子数组和的列表
    sub_list = []   # 最大和的子数组列表

    def maxSubArray(self, nums_list, le) -> int:
        """
        :param nums_list: 传入的数组
        :param le: 期望的子数组的长度
        :return: 子数组和最大值，最大和的子数组的列表
        """
        if le > len(nums_list):
            raise Exception('子数组长度大于父数组长度')
        elif le < 1 or len(nums_list) == 0:
            raise Exception("父数组不能为空，或者，子数组至少包含一个元素")
        elif le == len(nums_list):
            raise Exception("仅有一组数不符合规则")
        
        # 求指定长度子数组的和
        for i in range(len(nums_list)-1):
            s_sum = 0
            for j in range(i, i+le):
                # 子数组顺序的组合情况，去掉最后一组不够长度的子数组
                if len(nums_list) % le == 0:
                    s_sum += nums_list[j]
                else:
                    s_sum += nums_list[j-1]
                i += 1
            self.sum_list.append(s_sum)
        
        # 求子数组和的最大值，和最大值索引
        for i in range(len(self.sum_list)-1):
            for j in range(i+1, len(self.sum_list)):
                if len(nums_list) % le == 0:
                    if self.sum_list[i] > self.sum_list[j]:
                        self.max_sum = self.sum_list[i]
                        self.max_index = i
                    else:
                        self.max_sum = self.sum_list[j]
                        self.max_index = j
                else:
                    if self.sum_list[i] > self.sum_list[j]:
                        self.max_sum = self.sum_list[i]
                        self.max_index = i
                    else:
                        self.max_sum = self.sum_list[j]
                        self.max_index = j-1
        
        # 根据子数组和的最大值索引算出子数组在符数组中索引
        for i in range(self.max_index-1, self.max_index+le):
            self.sub_list.append(nums_list[i])
            
        print("传入的数组是{}，{}个长度的连续子数组最大和为{}，最大和的数组为{}".format(nums_list, le, self.max_sum, self.sub_list))
     
    # 求数组中的值的和 本次未用到
    def sumArray(self, num_list):
        sum = 0
        for i in range(len(num_list)):
            sum += num_list[i]
        return sum


class Solution:
    def maxSubArray(self, nums) -> int:
        tmp = nums[0]
        max_ = tmp
        n = len(nums)
        for i in range(1, n):
            # 当当前序列加上此时的元素的值大于tmp的值，说明最大序列和可能出现在后续序列中，记录此时的最大值
            if tmp + nums[i] > nums[i]:
                max_ = max(max_, tmp + nums[i])
                tmp = tmp + nums[i]
            else:
                # 当tmp(当前和)小于下一个元素时，当前最长序列到此为止。以该元素为起点继续找最大子序列,
                # 并记录此时的最大值
                max_ = max(max_, tmp, tmp + nums[i], nums[i])
                tmp = nums[i]
        return max_


# 作者：pandawakaka
# 链接：https: // leetcode - cn.com / problems / maximum - subarray / solution / bao - li - qiu - jie - by - pandawakaka /
# 来源：力扣（LeetCode）
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        
        
# Your MedianFinder object will be instantiated and called as such:

"""
给你一个有效的 IPv4 地址 address，返回这个 IP 地址的无效化版本。

所谓无效化 IP 地址，其实就是用 "[.]" 代替了每个 "."。

 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/defanging-an-ip-address
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
"""
author: jiyanjiao
date : 2019-10-23
"""

class Solution:
    
    def defangIPaddr(self, address) -> str:
        un_address = address.replace('.', '[.]')
        print(un_address)
        return un_address
"""
在一个「平衡字符串」中，'L' 和 'R' 字符的数量是相同的。

给出一个平衡字符串 s，请你将它分割成尽可能多的平衡字符串。

返回可以通过分割得到的平衡字符串的最大数量。

示例 1：

输入：s = "RLRRLLRLRL"
输出：4
解释：s 可以分割为 "RL", "RRLL", "RL", "RL", 每个子字符串中都包含相同数量的 'L' 和 'R'。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/split-a-string-in-balanced-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/split-a-string-in-balanced-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
"""
@author : jiyanjiao
@date :2019-10-24
"""


class Solution(object):
    def balancedStringSplit(self, s):
        """
        :type s: str
        :rtype: int
        """
        count = 0
        count_L = 0
        count_R = 0
        flag = 0
        
        s_list = list(s)
        for s_ in s:
            if s_ == 'L':
                count_L += 1
            else:
                count_R += 1
            if count_L == count_R:
                count += 1
                total = count_L + count_R
                # 用flag来标记上次已经识别到的位置
                for i in range(flag, total):
                    print(s_list[i], end='')
                print(',', end=' ')
                flag = total
        return count
 
    
if __name__ == '__main__':
    s = Solution()
    s.balancedStringSplit("RLRRLLRLRL")
    
    # obj = MedianFinder()
    # obj.addNum(1)
    # obj.addNum(2)
    # obj.addNum(4)
    # obj.addNum(3)
    # obj.addNum(5)
    # param_2 = obj.findMedian()

   
    # n = [1,2,3,4,5,6]
    # print(s.maxSubArray(n))
    # s.maxSubArray([1,2,3,4,5,6])
    # s.maxSubArray([-1,2,1,0,0],3)
    