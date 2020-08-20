# coding=UTF-8
'''
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''

class twoSum01(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        lenNums = len(nums)
        dictNums = {}

        if lenNums == 0:
            return None, None

        for i, val in enumerate(nums):
            if dictNums.__contains__(target - val) == False:
                list = []
                list.append(i)
                dictNums[target - val] = list
            else:
                list1 = dictNums[target-val]
                list1.append(i)
                dictNums[target - val] = list1

        for i, val in enumerate(nums):
            if dictNums.__contains__(val) == True:
                if i != dictNums[val]:
                    if (target - val) != val:
                        return i, dictNums[val][0]
                    else:
                        if len(dictNums[val]) > 1:
                            return dictNums[val][0], dictNums[val][1]

        return None, None


if __name__ == '__main__':
    nums = [8, 1, 4, 20, 46, 4, 6, 5, 7]#用例一
    # nums = [2, 3, 4]#用例二
    # nums = [3,3,3]#用例三
    # nums = [3]#用例四
    target = 6
    index1, index2 = twoSum01.twoSum(twoSum01, nums, target)
    if index1 != None or index2 != None:
        print(index1, index2)
    else:
        print("no match")


