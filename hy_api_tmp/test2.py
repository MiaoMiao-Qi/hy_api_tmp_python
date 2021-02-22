def sort_by_response_time(case_list):
    # 存放url和响应时长
    new_list = []
    newlist4 = []
    newlist5 = []
    diclist_top5 = {}
    for i in range(0, len(case_list)):
        new_list.append(case_list[i][3])

    # set去重
    new_list_remove_dup = set(new_list)
    for i in new_list_remove_dup:
        angle_list = [i, 0]
        newlist4.append(angle_list)
        newlist5.append(angle_list)

    # 对接口相应时长进行排序,按降序排序
    for i in range(0, len(newlist4)):
        for n in range(0, len(case_list)):
            if newlist4[i][0] == case_list[n][3] and case_list[n][5] >= newlist4[i][1]:
                newlist4[i][1] = case_list[n][5]
                newlist5[i][0] = newlist4[i][0].replace("/", "\n")
                newlist5[i][1] = case_list[n][5]
            else:
                pass

    dic_list = sorted(dict(newlist5).items(), key=lambda x: x[1], reverse=True)
    for i, (k, v) in enumerate(dict(dic_list).items()):
        if i in range(0, 5):
            diclist_top5[k] = v
        else:
            break
    return diclist_top5

if __name__ == '__main__':
    l = [[1, '直接邀请记录', 'GET', '/ltboss/directInvitedRecord', 'Fail', 0.70, ' "resultCode": 201', 200, '{"resultCode":200,"message":"OK","data":{"total":11,"page_total":2,"list":[],'],
     [2, '直接邀请记录-搜索', 'GET', '/app/api/faw/selltboss/2', 'Success', 0.089, ' "resultCode": 200', 200, '{"resultCode":200,"message":"OK","data":{"total":0,"page_total":0,"list":[]}}'],
    [3, '宣传材料-新增', 'POST', 'qotionalMaterials', 'Success', 0.265, '"resultCode": 200', 200, '{"resultCode":200,"message":"OK","data":null}'],
         [4, '直接邀请记录', 'GET', '/tInvitedRecord', 'Fail', 0.5, ' "resultCode": 201', 200,
          '{"resultCode":200,"message":"OK","data":{"total":11,"page_total":2,"list":[],'],
         [5, '宣传材料-新增', 'POST', 'qingqi/publicmaterial', 'Success', 0.90, '"resultCode": 200',200, ''],
         [6, '宣传材料-新增', 'POST', 'qingqi/publicmaterial5555', 'Success', 0.80, '"resultCode": 200', 200, '']
         ]

# sort_by_response_time(l)

import re
import json
import random
dict1 = {}

def get_variable_value_from_result(v, res):
    # 可变参数想取多个值用;分割， 如：'${fleetName}=[data][mileageList][0][fleetName];${fleetName}=[data][oilList][1][fleetName]'
    var_list = v.split(';')
    
    for var in var_list:
        param = var.split('=')
        if len(param) == 2:
            # 判断可变参数是否有效 为空，或者不是以[开头，或者以]结尾的
            if param[1] == '' or not re.search(r'^\[', param[1]) or not re.search(r'\]$', param[1]):
                result = "关联参数设置错误"
                continue
            response_js = json.loads(res)
            value = ""
            # 通过等号后的键值，逐步获得所指向的json串中的值
            for key in param[1][1:-1].split(']['):
                # 随机选择list中的某个值。excel写法如：[random@5]
                if 'random' in key:
                    key = random.randint(0, int(key.split('@')[1]))
                # 按条件筛选值，如获取type为21的list值。excel写法如：[type:21]
                elif ':' in key:
                    condition_key, condition_value = key.split(':')[0], key.split(':')[1]
                    for index in range(len(response_js)):
                        try:
                            if str(response_js[index][condition_key]) == condition_value:
                                key = index
                                break
                        except:
                            continue
                # 通过键值获取结果中的相应字段值
                try:
                    value = response_js[int(key)]
                except:
                    try:
                        value = response_js[key]
                    except:
                        # 未找到时，传空值
                        value = None
                        break
                response_js = value
            # 将关联参数和数值存到dict中
            if value is not None:
                dict1[str(param[0])] = str(value)
    print(dict1)
    pass

# res = """
# {"resultCode":200,"message":"OK","data":{"total":230,"page_total":23,"list":[{"id":822,"pmName":"测试152155","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 15:21:49","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":821,"pmName":"测试152114","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 15:21:08","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":820,"pmName":"测试151907","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 15:19:01","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":819,"pmName":"测试151314","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 15:13:09","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":817,"pmName":"测试143541","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:35:35","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":816,"pmName":"测试143250","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:32:44","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":813,"pmName":"测试141737","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:17:31","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":812,"pmName":"测试141709","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:17:03","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":811,"pmName":"测试141524","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:15:18","pmStatus":1,"pmStatusStr":"有效","operateStatus":1},{"id":810,"pmName":"测试141423","pmEffectiveRange":"","pmFriendsRewardUser":111,"pmGroupRewardUser":1111,"pmRewardUpperlimitcntUser":1111,"pmFriendsRewardSalesman":1111,"pmGroupRewardSalesman":1111,"pmRewardUpperlimitcntSalesman":11111,"createUser":"testInter","createTime":"2021-01-18 14:14:17","pmStatus":1,"pmStatusStr":"有效","operateStatus":1}]}}
# """
# v = "${fleetName}=[data][list][0][id]"
# v = "${fleetName}=[data][list][id:819][pmName]"
# v = '${fleetName}=[data][list][pmName:测试151314][id]'
# v = '${fleetName}=[data][list][random@5][id]'
# get_variable_value_from_result(v, res)
# r1 = '"resultCode":507'
#
# r = '"message":"车系+车辆大类+驱动形式 与已有规则重复！"'
# r = '"message":"车系+车辆大类+驱动形式与已有规则重复！"'
# rs = '{"resultCode":507,"message":"车系+车辆大类+驱动形式 与已有规则重复！","data":null}'
# if ''.strip(r) in rs:
#     print("true")
# else:
#     print("f")

s = 'moveId=653&moveToId=${id-1}&token=73c423d2663c499fafe485d363c57a20'
r = ' ${id-1}' ' ${id-1}'
print(r)
r = ' '.join(r.split())
print(r)