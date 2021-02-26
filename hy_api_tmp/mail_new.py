
import smtplib
from email.utils import formataddr

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import setting as info
import case as case
import img as img
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
import os, base64
from pyecharts.charts import Gauge
import const
# =====================================================
#                  ○  发送报告 ○                     #
# =====================================================

new_list = []
newlist3 = []
newlist4 = []
newlist5 = []
new_list_remove_dup = []
diclist_top5 = {}
path = os.path.dirname(os.path.abspath(__file__))

class CreatMail():
    
    def casehtml_assert(self):
              merrmsg="""
        <div style="border:1px solid #ddd;font-size: 15px;height: 240px;text-align:center;display:block;width: 936px;margin-top: 1%;margin-left: 1%;">
            <div style="color:#808080;background-color: #EFEFEF;box-shadow: 2px 2px 2px silver;text-align: center;width:936px;height: 20px;font-size:12px;">
                <span style="width: 40px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">No</span>
                <span style="width: 215px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">检测项目</span>
                <span style="width: 44px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">方式</span>
                <span style="width: 300px;height: 20px; overflow:hidden; white-space:pre-wrap; line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">接口地址</span>
                <span style="width: 110px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">校验值</span>
                <span style="width: 50px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">速度(秒)</span>
                <span style="width: 45px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">结果</span>
                <span style="width: 45px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">状态</span>
                <span style="width: 40px;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;">返回值</span>
            </div>
            <div style="height:240px;width:936px;overflow-y: auto;display: block;font-size: 9px;">
        """
              merrmsg1 = ""
              for i in range(0, len(case.case_list)):
                  if case.case_list[i][4]=="Success":
                      msg = """
            <div style="width:936px;height: auto; display: flex; "id="table_tr">
                <span style="width: 40px;height: auto;line-height: 25px; display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 217px;height: auto;line-height: 25px; display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 300px;height: auto; overflow:hidden;  white-space:pre-wrap; line-height: 25px;display:flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 112px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 50px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <div style="width: 40px;height: auto;line-height: 25px;display: flex;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;overflow:hidden" title={}>查看</div>
            </div>
    """.format(case.case_list[i][0],case.case_list[i][1],case.case_list[i][2],case.case_list[i][3],
               case.case_list[i][6],case.case_list[i][5],case.case_list[i][4],case.case_list[i][7],case.case_list[i][8])
                  else:
                      msg = """
         <div style="width: 936px;height: auto;border-bottom: 1px solid #EFEFEF;line-height: 25px;background:linear-gradient(0deg, #fea079, #FFE4B5, transparent);overflow:hidden; display: flex;" id="table_tr">
                <span style="width: 40px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 217px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 300px;height: auto;overflow:hidden;  white-space:pre-wrap; line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 112px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 50px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <span style="width: 45px;height: auto;line-height: 25px;display: flex;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;">{}</span>
                <div style="width: 40px;height: auto;line-height: 25px;display: flex;font-family:'微软雅黑';border-bottom: 1px solid #EFEFEF;align-items: center; justify-content: center;overflow:hidden" title={}>查看</div>
            </div>
    """.format(case.case_list[i][0],case.case_list[i][1],case.case_list[i][2],case.case_list[i][3],
               case.case_list[i][6],case.case_list[i][5],case.case_list[i][4],case.case_list[i][7],case.case_list[i][8])

                  if i==0:
                      merrmsg1=merrmsg+msg
                  else:    
                      merrmsg1 += msg
              return merrmsg1

    def casehtml_assert2(self, newlist):
        merrmsg = """
        <div style="border:1px solid #ddd;font-size: 15px;height: 240px;text-align:center;display:block;width: 936px;margin-top: 1%;margin-left: 1%;overflow: hidden">
            <div style="color:#808080;background-color: #F2F2F2;box-shadow: 2px 2px 2px silver;text-align: center;width:936px;height: 20px;font-size:12px;">
                <span style="width: 5%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">No</span>
                <span style="width: 55%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">接口名</span>
                <span style="width: 10%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">项目数</span>
                <span style="width: 9%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">通过</span>
                <span style="width: 9%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;border-right: 2px solid #e0e0e0">失败</span>
                <span style="width: 10%;height: 20px;line-height: 20px;font-weight: bold;display: block;float: left;">通过率</span>
            </div>
            <div style="height: 200px;width:936px;overflow-y: auto;display: block;font-size: 9px;">
        	"""
        merrmsg2 = ""
        for i in range(0,len(newlist)):
            if newlist[i][2] == 0:
                msg = """
                <div style="width: 936px;height: 25px;border-bottom: 1px solid #EFEFEF;line-height: 25px;" id="table_tr">
                    <span style="width: 5%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 55.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 10.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 9.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';color:green">{}</span>
                    <span style="width: 9.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 10.2%;height: 25px;line-height: 25px;display: block;float: left;font-family:'微软雅黑';">{}%</span>
                </div>
        """.format(i+1,newlist[i][0], newlist[i][1]+newlist[i][2], newlist[i][1], newlist[i][2],int(newlist[i][1]/(newlist[i][1]+newlist[i][2])*100))
            else:
                msg = """
                <div style="width: 936px;height: 25px;border-bottom: 1px solid #EFEFEF;line-height: 25px;background:linear-gradient(0deg, #fea079, #FFE4B5, transparent);" id="table_tr">
                    <span style="width: 5%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 55.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 10.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 9.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';">{}</span>
                    <span style="width: 9.1%;height: 25px;line-height: 25px;display: block;float: left;border-right: 1px solid #EFEFEF;font-family:'微软雅黑';color:red;">{}</span>
                    <span style="width: 10.2%;height: 25px;line-height: 25px;display: block;float: left;font-family:'微软雅黑';">{}%</span>
                </div>
        """.format(i+1,newlist[i][0], newlist[i][1]+newlist[i][2], newlist[i][1], newlist[i][2],int(newlist[i][1]/(newlist[i][1]+newlist[i][2])*100))
            if i == 0:
                merrmsg2 = merrmsg + msg
            else:
                merrmsg2 += msg
        return merrmsg2

    def creatNested(self, api):
        newlie_max = api
        yaxis = []
        for key in newlie_max.keys():
            yaxis.append(key)

        xaxis = []
        for value in newlie_max.values():

            xaxis.append(value)
        c = (
            Bar()
                .add_xaxis(yaxis)
                .add_yaxis("商家A", xaxis, color='#2b4490')
                .reversal_axis()
                .set_series_opts(
                itemstyle_opts={  # set_series_opts设置系列配置  ,itemstyle_opts=opts.ItemStyleOpts(color="#4682B4")
                    "normal": {  # normal代表一般、正常情况
                        # LinearGradient 设置线性渐变，offset为0是柱子0%处颜色，为1是100%处颜色
                        "color": JsCode("""new echarts.graphic.LinearGradient(1,0,0,1, [{
                                         offset: 0,
                                         color: 'rgba(0, 233, 245, 1)'
                                     }, {
                                         offset: 1,
                                         color: 'rgba(0, 45, 187, 1)'
                                     }], false)"""),
                        "shadowColor": 'red',  # 阴影颜色
                    }},
                label_opts=opts.LabelOpts(position="right", color="#000099"),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(position="right"),
                ),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="延迟最高Top5(毫秒）", title_textstyle_opts=(opts.TextStyleOpts(color='#2a5caa')), ),
                # toolbox_opts=opts.ToolboxOpts(),
                legend_opts=opts.LegendOpts(is_show=False),
                yaxis_opts=opts.AxisOpts(
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color='#2b4490')
                    ),
                    axislabel_opts=opts.LabelOpts(formatter="{value}",rotate=0,font_size=8),
                    name_location='end'
                ),
                xaxis_opts=opts.AxisOpts(
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color='#2b4490')
                    ),
                    axislabel_opts=opts.LabelOpts(formatter="{value}ms")
                )
            )
                .render("bar.html")
        )

    def creatNested2(self):

        if case.ok == 0:
            self.success_tgl = 0
        else:
            self.success_tgl = str(int((case.ok / (case.ok + case.ng)) * 100))

        global tgl
        tgl = int(self.success_tgl)

        c = (
            Gauge()
                .add(
                "业务指标",
                [("通过率", tgl)],
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=[(0.4, "#FF6666"), (0.8, "#ffce7b"), (1, "#00CC99")], width=35
                    )
                ),
            )
                .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
            )
                .render("success_tgl.html")
        )

    def sort_by_response_time(self, case_list):
        """
        按响应时长对接口进行升序排序
        :param case_list:接口列表
        :return:排序后的字典
        """
        # 存放url和响应时长
        global new_list_remove_dup
        
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
    
        dic_list = sorted(dict(newlist5).items(), key=lambda x: x[1], reverse=False)
        for i, (k, v) in enumerate(dict(dic_list).items()):
            if i in range(0, 5):
                diclist_top5[k] = v
            else:
                break
        return diclist_top5

    def CreatBody(self):
        self.creatNested(self.sort_by_response_time(case.case_list))
        make_snapshot(snapshot, "bar.html", "bar.png")
        icon = open('bar.png', 'rb')
        iconData = icon.read()
        iconData = str(base64.b64encode(iconData)).split("'")
        self.creatNested2()
        make_snapshot(snapshot, "success_tgl.html", "success_tgl.png")
        icon2 = open('success_tgl.png', 'rb')
        iconData2 = icon2.read()
        iconData2 = str(base64.b64encode(iconData2)).split("'")

        Ta = info.Form
        Tb = info.pw
        Td = info.server
        To = info.To.split(',')
        strTo = ' '.join(To)
        server = smtplib.SMTP_SSL(Td)
        server.login(Ta, Tb)
        main_msg = MIMEMultipart()
        xm_count = int(case.ok+case.ng)

        ps = int((case.ok/(case.ok+case.ng)*100))
        if ps >= 80:
            ps = """<span style="color:#cca30e;font-family:'微软雅黑';">%s%%</span>"""%(ps)
            success = img.success_high
        elif 50 <= ps < 80:
            ps = """<span style="color:#ffce7b;font-family:'微软雅黑';">%s%%</span>""" % (ps)
            success = img.success_center
        else:
            ps = """<span style="color:#00CC99;font-family:'微软雅黑';">%s%%</span>""" % (ps)
            success = img.success_low

        tgl_success = int(self.success_tgl)
        if tgl_success>=85:
            tgl_success= """<span style="color:#00CC99;">%s%%</span>""" %(tgl_success)
        elif 50<=tgl_success<85:
            tgl_success = """<span style="color:#ffce7b;">%s%%</span>""" %(tgl_success)
        else:
            tgl_success = """<span style="color:#FF6666;">%s%%</span>""" %(tgl_success)

        for i in new_list_remove_dup:
            a=[]
            a.append(i)
            a.append(0)
            a.append(0)
            newlist3.append(a)
        for i in range(0, len(newlist3)):
            for n in range(0,len(case.case_list)):
                   if newlist3[i][0] == case.case_list[n][3] and case.case_list[n][4]=="Success" :
                       newlist3[i][1]=newlist3[i][1]+1
                   elif newlist3[i][0] == case.case_list[n][3] and case.case_list[n][4]=="Fail" :
                       newlist3[i][2] = newlist3[i][2] + 1

        mmsg = self.casehtml_assert()
        mmsg1 = self.casehtml_assert2(newlist3)
        # noinspection PyStringFormat
        htmlmsg = '''
        <html lang="en">
<head>
    <meta charset="GB2312">
    <title>Title</title>
</head>
<body style="background-size:100% 100%;width:100%;" sroll="no">
<div style="height:300px;width:955px;display:block;margin-left: 4%;margin-bottom:20px;">
    <div style="height:52px;background:#009ACD;box-shadow: 2px 2px 3px silver;width:955px;">
        <img src="{}" style=" width: 140px;height: 50px;margin-top: -1px;float: left;margin-left: 3%;margin-right: 2%">
        <span style="color: white;font-size: 22px;line-height: 52px;font-weight: 500;">{} 接口自动化测试报告</span>
    </div>
    <div style="height:240px;width:955px;display: block;margin-top: 20px;margin-bottom: 5px;
        padding-bottom: 10px;background: white;border:1px solid LightGrey;">
        <div style="background-color: #F2F2F2;height: 25px;line-height: 25px;
            box-shadow:-2px -2px #e0e0e0,2px 2px #e0e0e0,-2px -2px #e0e0e0,3px 3px #e0e0e0;
          background: linear-gradient(180deg,#DCDCDC,transparent);
          border-top: 1px solid #D3D3D3;
      background-repeat: repeat-x;
      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#F2F2F2,GradientType=0);
    ">
            <div style="padding-left: 20px;font-size: 14px;">
                <span style="font-size: 16px;color: Gray;font-weight: bold;margin-right: 2%;display: block;
        float: left;">测试结果概览 （邮件自动化发送，勿回） </span>
                <img src="{}" style="width:70px;height:18px;padding-top:2.4px;"/>
                <img src="{}" style="width: 20px;height: 20px;padding-top:2.4px;margin-left: 4%;margin-right: 1%;float: right;"/>
            </div>
            
        </div>
        <div style="font-size: 14px;display: block;font-weight:bolder;color: #4C566A;
             padding-top:10px;overflow: hidden;width: 100%;height: 700px;background:url('') no-repeat;background-size: 12%;background-position: 29 85;">
            <div style="width: 30%;float:left;margin-right:9%;text-align: center;">    
                <div style="background:url('{}') no-repeat;background-size: 60% 100%;background-position: center;margin-top: -15px;margin-left: 47%;">
                    <h5 style="font-weight: bold;font-size: 15px;">总体通过率</h5>
                </div>
                <div style="margin-top:-40px;width: 150%;height:35%;">
                    <img src="data:image/png;base64,{}" style="width: 95%;height:90%;"/>
                    <div style="margin-top:-80px;width:17%;height:20px;font-size:20px;margin-left: 43%;">{}</div>
                </div>   
             </div>
            <div style="width: 55%;height:170px;float:left;text-align: center;margin-top: 15px;border-radius: 15px;border: 1px dashed #e0e0e0;line-height:170px;">
                <div style="width:30%;height:170px;float:left;line-height:170px;padding-left:10%;text-align: justify;">
                    <div style="font-weight: bold;font-size:15px ;height:25px;margin-top: 24px;">总接口数：<span>{}</span></div>
                    <div style="font-weight: bold;font-size:15px ;height:25px;line-height:25px;">通过率&nbsp;&nbsp;&nbsp;&nbsp;: <span>&nbsp;{}%</span></div>
                    <div style="font-weight: bold;font-size:15px ;height:25px;line-height:25px;">总项目数：<span>{}</span></div>   
                </div>
                <div style="width:60%;height:170px;float:right;line-height:170px;margin-left: -10%;text-align: justify;">
                     <div style="font-weight: bold;font-size:15px ;height:25px;margin-top: 48px;line-height:25px;">执行开始时间：<span>{}</span></div>
                    <div style="font-weight: bold;font-size:15px ;height:25px;line-height:25px;">执行结束时间：<span>{}</span></div>
                    <div style="margin-bottom: 2%;font-weight: bold;font-size:15px ;height:25px;line-height:25px;">测试耗时&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<span>{}秒</span></div>
                </div>        
            </div>
        </div>
    </div>
</div>
<!--统计报表-->
<div style="height:400px;width:955px;display: block;background: white;border:1px solid LightGrey;margin-left: 4%;margin-top:40px;">
    <div style="background-color: #F2F2F2;height: 25px;line-height: 25px;
            box-shadow:-2px -2px #e0e0e0,2px 2px #e0e0e0,-2px -2px #e0e0e0,3px 3px #e0e0e0;
      background: linear-gradient(180deg,#DCDCDC,transparent);
      border-top: 1px solid #D3D3D3;
      background-repeat: repeat-x;
      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#F2F2F2,GradientType=0);
    ">
        <div style="padding-left: 20px;font-size: 14px;">
            <span style="font-size: 16px;color: Gray;font-weight: bold;margin-right: 2%;display: block;
    float: left;">统计报表</span>
           <img src="{}" style="width:70px;height:18px;padding-top:2.4px;margin-left: 4%;"/>
            <img src="{}" style="width: 20px;height: 20px;padding-top:2.4px;margin-left: 4%;margin-right: 1%;float: right;"/>
        </div>
       
    </div>
    <img src="data:image/png;base64,{}" style="width:75%;height:90%;margin-left:15%;margin-top:25px"/>
    
</div>
<!--接口详情-->
<div style="height:300px;width:955px;display: block;margin-top: 20px;background: white;border:1px solid LightGrey;margin-left: 4%;">
    <div style="background-color: #F2F2F2;height: 25px;line-height: 25px;
            box-shadow:-2px -2px #e0e0e0,2px 2px #e0e0e0,-2px -2px #e0e0e0,3px 3px #e0e0e0;
      background: linear-gradient(180deg,#DCDCDC,transparent);
      border-top: 1px solid #D3D3D3;
      background-repeat: repeat-x;
      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#F2F2F2,GradientType=0);
    ">
        <div style="padding-left: 20px;font-size: 14px;">
            <span style="font-size: 16px;color: Gray;font-weight: bold;margin-right: 2%;display: block;
    float: left;">接口详情</span>
            <img src="{}" style="width:70px;height:18px;padding-top:2.4px;margin-left: 4%;"/>
            <img src="{}" style="width: 20px;height: 20px;padding-top:2.4px;margin-left: 4%;margin-right: 1%;float: right;"/>
        </div>
        
    </div>
    {}
     </div>
     </div>
</div>
<!--请求详情-->
<div style="height:300px;width:955px;display: block;margin-top: 20px;background: white;border:1px solid LightGrey;margin-left: 4%;margin-bottom:30px;">
    <div style="background-color: #F2F2F2;height: 25px;line-height: 25px;
            box-shadow:-2px -2px #e0e0e0,2px 2px #e0e0e0,-2px -2px #e0e0e0,3px 3px #e0e0e0;
      background: linear-gradient(180deg,#DCDCDC,transparent);
      border-top: 1px solid #D3D3D3;
      background-repeat: repeat-x;
      filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#F2F2F2,GradientType=0);
    ">
        <div style="padding-left: 20px;font-size: 14px;">
            <span style="font-size: 16px;color: Gray;font-weight: bold;margin-right: 2%;display: block;
    float: left;">请求详情</span>
            <img src="{}" style="width:70px;height:18px;padding-top:2.4px;margin-left: 4%;"/>
            <img src="{}" style="width: 20px;height: 20px;padding-top:2.4px;margin-left: 4%;margin-right: 1%;float: right;"/>
        </div>
    </div>
    {}
    </div>
    </div>
</div>
<!--页面底部导航-->
<div style="width:955px;height: 20px;background:#009ACD;;margin-left: 4%;text-align: center;margin-top:20px;line-height: 20px;
color: white;box-shadow:1px 1px 1px silver">鱼快创领科技   自动化测试</div>
</body>
</html> 
        '''.format(img.header_img,info.title,img.right_jt,img.button,img.title_bg,iconData2[1],tgl_success,len(new_list_remove_dup),self.success_tgl,xm_count,const.start_time_style,
                   const.end_time_style,
                   const.total_time,img.right_jt,img.button,iconData[1],img.right_jt,img.button,mmsg1,img.right_jt,img.button,mmsg)
        
        msgTEXT = MIMEText(htmlmsg, _subtype='html')
        main_msg.attach(msgTEXT)

        # with open("report.html", "w", encoding="UTF-8") as f:
        with open("report.html", "w", errors='ignore') as f:
              f.write(htmlmsg)
              f.close()
        part_case_excel = MIMEApplication(open(path + r'\project\{}_result.xls'.format(info.project_name), 'rb').read())
        part_case_excel.add_header('Content-Disposition', 'attachment', filename="接口用例详情.xls")
        main_msg.attach(part_case_excel)
        part = MIMEApplication(open('report.html', 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename="report.html")
        main_msg.attach(part)
        main_msg['From'] = formataddr(['自动化测试部', Ta])
        main_msg['To'] = strTo
        main_msg['Subject'] ='【{}环境】'.format(info.env.upper())+info.title+"接口自动化测试报告"
        fullText = main_msg.as_string()
        # 用smtp发送邮件###
        if info.env != 'online':
            if info.send_email:
                server.sendmail(Ta, To, fullText)
                print("通过：%s,失败：%s，已发送测试报告到邮箱" % (case.ok, case.ng))
        else:
            if case.ng >= 0 and info.send_email:
                server.sendmail(Ta, To, fullText)
                print("通过：%s,失败：%s，已发送测试报告到邮箱" % (case.ok, case.ng))
        server.quit()

    def SendMail(self):
        try:
            self.CreatBody()

        except Exception as e:
            print(" 测试报告发送失败", e)
    
def SendReport():
        report = CreatMail()
        report.SendMail()
        
        
def SendLongin_fail_mail(content):
    try:
        Ta = info.Form
        Tb = info.pw
        Td = info.server
        To = info.To.split(',')
        strTo = ' '.join(To)
        server = smtplib.SMTP_SSL(Td)
        server.login(Ta, Tb)
        
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = formataddr(['自动化测试部', Ta])
        message['To'] = strTo
        message['Subject'] = '💥警报!【{}环境】'.format(info.env.upper()) + info.title + "登录接口发生异常"
        server.sendmail(Ta, To, message.as_string())
    except Exception as e:
        print(" 测试报告发送失败", e)

if __name__ == '__main__':
    # SendReport()
    test = CreatMail()
    # test.creathtml()
    test.SendLongin_fail_mail("登录接口出现异常")
