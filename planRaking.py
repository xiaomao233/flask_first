# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:19:48 2020

@author: user
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial
import math
from pyproj import Proj, transform, Transformer
import pyproj
# WGS84 = Proj(init='EPSG:4326')#WGS84
# p = Proj(init="EPSG:32650")#UTM 50N
# x,y = 438891.66410737,4377700.62380272
# ,lon = transform(p, WGS84, x, y)
# x2,y2 = transform(WGS84,p, lat,lon)


class mapopt:
    def __init__(self):
        ax = axCreate(1, 1)
        self.outline = self.getProf("field3outlineBL.csv")
        # plt.plot(self.outline[:,0],self.outline[:,1],'--k')
        # self.pasArea = self.getProf("field3passNE.csv")
        # plt.plot(self.pasArea[:,0],self.pasArea[:,1],'--b')
        # self.opArea = self.getProf("field3operateNE.csv")
        # plt.plot(self.opArea[:,0],self.opArea[:,1],'-r')
        self.demoArea = self.getProf("field3demoBL.csv")
        plt.plot(self.demoArea[:, 0], self.demoArea[:, 1], '-ok')
        ob = self.getob("field3obBL.csv")
        self.obstacle = self.obproc(ob)

    def WGS84ToUTM(self, lat, lon):
        transformer = Transformer.from_crs("epsg:4326", "epsg:4527")
        xUTM, yUTM = transformer.transform(lat, lon)
        return np.array([xUTM, yUTM])

    def getProf(self, path):
        data = pd.read_csv(path, header=None)
        p = []
        for i in range(len(data)):
            lon = float(data[2][i][0:-1])
            lat = float(data[1][i][0:-1])
            xUTM, yUTM=self.WGS84ToUTM(lat, lon)
            p.append([xUTM, yUTM])
        p.append(p[0])
        return np.array(p)

    def getob(self, path):
        data = pd.read_csv(path, header=None)
        ob = {}
        for i in range(len(data)):
            lon = float(data[2][i][0:-1])
            lat = float(data[1][i][0:-1])
            xUTM, yUTM=self.WGS84ToUTM(lat, lon)
            ob[data[0][i]]=np.array([xUTM, yUTM])
        return ob

    def obproc(self,ob):
        iIn = {'04', '05', '12', '13'}
        ac = {'Y': '--y', 'N': '-m'}

        def line(a):
            def _uve(bb):
                return np.array([-bb[1], bb[0]])/np.linalg.norm(bb)
            l0 = [a[0][3]+_uve(a[1][3]-a[0][3])*a[0][2]/2]
            for i in range(1, len(a)):
                l0.append(a[i][3]+_uve(a[i][3]-a[i-1][3])*a[i][2]/2)
            for j in range(1, len(a)):
                i = len(a)-j
                l0.append(a[i][3]-_uve(a[i][3]-a[i-1][3])*a[i][2]/2)
            l0.append(a[0][3]-_uve(a[1][3]-a[0][3])*a[0][2]/2)
            l0.append(l0[0])
            l0 = np.array(l0)
            plt.plot(l0[:, 0], l0[:, 1], ac[a[0][1]])
            return l0

        def circle(a):
            b = a[0]
            theta = np.linspace(0, 2 * np.pi, 10)
            x = b[3][0]+b[2]*np.cos(theta)
            y = b[3][1]+b[2]*np.sin(theta)
            plt.plot(x,y,ac[a[0][1]])
            # plt.Circle((a[3][0], a[3][1]), a[2])
            c0 = [[x[i],y[i]] for i in range(len(x))]
            c0.append(c0[0])
            c0 = np.array(c0)
            return c0
        ob2 = {}
        for i in ob:
            p = i.split(' ')
            ob2[p[0]] = []
        for i in ob:
            p = i.split(' ')
            linelist = [p[1],p[4],float(p[3])/10,ob[i],int(p[2])]  # 障碍物类型；通过性，尺寸，坐标,点序号
            ob2[p[0]].append(linelist)
        ob3 = {}
        for i in iIn:
            if ob2[i][0][0] == 'L':
                ob2[i].sort(key=lambda x: x[4])
                ob3i = line(ob2[i])
            if ob2[i][0][0] == 'O':
                ob3i = circle(ob2[i]) 
            ob3[i] = ob3i
        return ob3
    # def cal(self,demoArea):


class plan:
    def __init__(self, mymap, myve):
        w = myve["w"]
        self.heading = self.getheading()
        self.obhead = self.OBheadJud(mymap.demoArea, mymap.obstacle, self.heading)
        self.rakArea = self.getRak(mymap.demoArea, self.obhead, w)
        
        self.rakArea = mymap.demoArea
        
        plt.plot(self.rakArea[:, 0], self.rakArea[:, 1], '-or')
        self.direction = self.getdire(self.rakArea)
        self.lineArea = self.getlineArea(self.rakArea, self.direction, self.heading)
        # plt.plot(self.lineArea[:,0],self.lineArea[:,1],'-r')
        self.linelist = self.getlinelist(self.lineArea, self.direction, w)
        self.lineProc = self.getlineProc(self.linelist, mymap.obstacle, self.obhead, self.direction, myve["wo"])
        
        self.lineProc = self.linelist
        
        self.orderline = self.getOrderline(self.lineProc)
        self.path = self.turnAdd(self.orderline, myve['r'])
        self.draw(mymap, self.rakArea, self.path)
        # self.pathSemUTM = self.output(self.path)
        # self.time = self.getTime(self.pathSemUTM)
        # self.test()

    def getTime(self, pathSemUTM):
        k = 8/3.6/1500  # km/h / 3.6 / rmp = m/s/rmp
        t = 0
        for i in range(len(pathSemUTM)-1):
            p = pathSemUTM.values[i][0:2]
            p1 = pathSemUTM.values[i+1][0:2]
            e = pathSemUTM.values[i][2]
            v = k * e
            l = np.linalg.norm(p1-p)
            ti = l/v
            t = t + ti
        print(t)
        print(t/60/60)
        return t

    def output(self, path):
        pathSemWGS84 = []
        pathSemUTM = []
        WGS84 = Proj(init='EPSG:4326')
        utmBJ = Proj(proj='utm', zone=50, ellps='WGS84', preserve_units=False)
        engineSpeedDic = {"high": 1000, "low": 1500}
        linemodeList = [1, 2]
        operatemodelist = [1,0]  # 1表示作业，0表示非作业
        wgscol = ['lat', 'lon']
        utmcol = ['East', 'North']
        wgscol.append('engineSpeed')
        utmcol.append('engineSpeed')
        wgscol.append('operatemode')
        utmcol.append('operatemode')
        with open("pathWGS84.txt", 'w', encoding='utf-8') as f:
            for j in range(len(path)):
                line = path[j]
                for i in range(len(line)):
                    point = line[i]
                    if j % 4 == 0 and i == 0:
                        operatemode = operatemodelist[0]
                    else:
                        operatemode = operatemodelist[1]
                    if len(line )==2 and i ==0:
                        engnineSpeed = engineSpeedDic["high"]
                        linemode = linemodeList[0]
                    else:
                        engnineSpeed = engineSpeedDic["low"]
                        linemode = linemodeList[1]
                    x, y = point[0], point[1]
                    lon, lat = transform(utmBJ, WGS84, x, y)
                    iwgs = [str(lat), str(lon)]
                    iutm = [x, y]
                    iwgs.append(engnineSpeed)
                    iutm.append(engnineSpeed)
                    iwgs.append(operatemode)
                    iutm.append(operatemode)
                    pathSemWGS84.append(iwgs)
                    pathSemUTM.append(iutm)
                    stri = """{"%s","%s",%s,0},\n""" % (lat, lon, linemode)
                    f.write(stri)
        pathSemWGS84 = pd.DataFrame(np.array(pathSemWGS84),columns=wgscol)
        pathSemUTM = pd.DataFrame(np.array(pathSemUTM),columns=utmcol)
        pathSemWGS84.to_csv('RakingPathWGS84.csv',sep=',',encoding='utf-8')
        pathSemUTM.to_csv('RakingPathUTM.csv',sep=',',encoding='utf-8')
        return pathSemUTM

    def draw(self,mymap,rakArea,path):
        ax = axCreate(1,1)
        plt.plot(mymap.demoArea[:,0],mymap.demoArea[:,1],'--k')
        for i in mymap.obstacle:
            plt.plot(mymap.obstacle[i][:,0],mymap.obstacle[i][:,1],'-r')
        plt.plot(rakArea[:,0],rakArea[:,1],'-y')
        for j in path:
            if len(j)==2:
                plt.plot(j[:,0],j[:,1],'-ob')
            else:
                plt.plot(j[:,0],j[:,1],'-og')
        
    def turnAdd(self,li,r):
        def circle(O,r,th0,th1):
            #O:圆心坐标；r：半径；th0，圆心指向起点的方向角；th1:圆心指向终点的方向角
            theta = np.linspace(th0, th1, 5)
            x = O[0]+r*np.cos(theta)
            y = O[1]+r*np.sin(theta)
            #plt.plot(x,y)
            c0 = [[x[i],y[i]] for i in range(len(x))]
            c0.pop(-1)
            c0.pop(0)
            return c0
        path = []
        for i in range(len(li)-1):
            di = (li[i][1]-li[i][0])/np.linalg.norm(li[i][1]-li[i][0])#第i个条带的单位方向
            dn = (li[i+1][0]-li[i][1])/np.linalg.norm(li[i+1][0]-li[i][1])#第i个条带终点到第i+1个条带起点的单位方向
            Os = li[i][1] + dn*r
            Oe = li[i+1][0] - dn*r
            ths0 = np.arctan2(-dn[1],-dn[0])
            the0 = np.arctan2(di[1],di[0])
            angle = np.arctan2(dn[1],dn[0])-np.arctan2(di[1],di[0])
            if np.abs(angle)>=np.pi:
                angle = angle - np.pi*2
            turnl = np.array([Os + di * r, Oe + di * r])
            turncs = np.array(circle(Os,r,ths0,ths0+angle))
            turnce = np.array(circle(Oe,r,the0,the0+angle))
            path.append(li[i])
            path.append(turncs)
            path.append(turnl)
            path.append(turnce)
        path.append(li[len(li)-1])
        return path

    def getlineProc(self,linelist,obstacle,obhead,di,w):
        def crossjud(lineL,lineR,oblist):
            for i in range(len(oblist)-1):
                line = np.array([oblist[i],oblist[i+1]])
                pcl = self.get_crossing(lineL,line,'s')
                pcr = self.get_crossing(lineR,line,'s')
                if type(pcl) is np.ndarray or type(pcr) is np.ndarray:
                    return True
            return False
        hdire = np.array([-di[1],di[0]])#右方向单位向量
        crossIndex = []
        for i in range(len(linelist)):
            lineL = np.array([linelist[i][0]-hdire*w/2,linelist[i][1]-hdire*w/2])
            lineR = np.array([linelist[i][0]+hdire*w/2,linelist[i][1]+hdire*w/2])
            for j in obstacle:
                if j in obhead.keys():
                    continue
                if crossjud(lineL,lineR,obstacle[j]):
                    crossIndex.append(i)
        lineProc = []
        for i in range(len(linelist)):  
            if i not in crossIndex:
                lineProc.append(linelist[i])
            else:
                print('i',linelist[i])
                print('i+1',linelist[i+1])
        return lineProc
    
    def OBheadJud(self,Area,obstacle,head):
        # 返回涉及地头的障碍物字典
        # 如果没有，则返回空字典
        # {i:{side':'[2,4],上边，[-2,-1]下边','min':dismin,'max':dismax,}}
        obHead = {}
        for i in obstacle:
            p = obstacle[i]
            dislowlist = []
            disuplist = []
            for pin in range(len(p)-1):
                dislow = self.getDis(p[pin],np.array([Area[-2],Area[-1]]))
                disup = self.getDis(p[pin],np.array([Area[2],Area[4]]))
                dislowlist.append(dislow)
                disuplist.append(disup)
            dislowmin = np.min(np.array(dislowlist))
            dislowmax = np.max(np.array(dislowlist))
            disupmin = np.min(np.array(disuplist))
            disupmax = np.max(np.array(disuplist))
            if dislowmin <= head:
                obHead[i] = {'side':[-2,-1],'min':dislowmin,'max':dislowmax}  
            elif disupmin <= head:
                obHead[i] = {'side':[2,4],'min':disupmin,'max':disupmax}
        return obHead

    def getRak(self,a,obhead,w):
        b = [i for i in a]
        sides = [[-2,-1],[2,4]]
        lmax = []
        umax = []
        for j in obhead:
            if obhead[j]['side']==sides[0]:
                lmax.append(obhead[j]['max'])
            if obhead[j]['side']==sides[1]:
                umax.append(obhead[j]['max'])
        
        if len(lmax):
            k = (np.floor(np.max(lmax)/w)+1)*w
            print('kl',k)
            b[0] = b[0] + (b[1]-b[0])/np.linalg.norm(b[1]-b[0])*k
            b[-1] = b[0]
            b[-2] = b[-2] + (b[-3]-b[-2])/np.linalg.norm(b[-3]-b[-2])*k
        if len(umax):
            print('ku',k)
            k = (np.floor(np.max(umax)/w)+1)*w
            b[2] = b[2] + (b[1]-b[2])/np.linalg.norm(b[1]-b[2])*k
            b[4] = b[4] + (b[4]-b[5])/np.linalg.norm(b[4]-b[5])*k
        return np.array(b)

    def getOrderline(self,linelist):
        def operateStrip(operateNum, blockNum, skipQuantity):  # 生成第operateNum个目标作业的条带序号
            # blockNum为块序号，本实验取1，skipQuantity为跳过条带数
            if operateNum == 1:
                operateStripNum = (2 * skipQuantity + 1) * (blockNum - 1) + 1
            elif operateNum % 2 ==0:
                operateStripNum = operateStrip(operateNum-1, blockNum, skipQuantity) + skipQuantity +1
            else:
                operateStripNum = operateStrip(operateNum-1, blockNum, skipQuantity) - skipQuantity
            return operateStripNum

        def orderline(lineList, skipQuantity):  # 生成条带作业序列
            def lineAdd(orderlineList, jnow, operateStripNum, blockNum):
                # print(jnow ,operateStripNum)
                if jnow % 2 == 1:
                    lineOrder = lineList[operateStripNum-1]
                else:
                    lineOrder = np.array([lineList[operateStripNum-1][1],lineList[operateStripNum-1][0]])
                plt.plot(lineOrder[:,0],lineOrder[:,1],'-',color=(0.5+np.sin(blockNum)/2,0.5+np.sin(2*(blockNum))/2,0.5+np.sin(3*(blockNum))/2))
                plt.text(lineOrder[0][0],lineOrder[0][1],jnow)
                orderlineList.append(lineOrder)            
            uStrip = skipQuantity*2+1
            orderlineList = []
            blockAll = int(len(lineList)/uStrip)-1
            for i in range(len(lineList)):
                blockNum = int(i/uStrip)+1
                operateNum = i + 1 - (blockNum-1)*uStrip
                operateStripNum=operateStrip(operateNum,blockNum, skipQuantity)
                if blockNum > blockAll:
                    break                    
                lineAdd(orderlineList,i+1,operateStripNum,blockNum)
            ire = blockAll * uStrip 
            nre = len(lineList) - ire
            #print("----",ire,nre)
            for j in range(nre):
                operateStripNum=int(j/2)+(j%2)*(int(np.ceil(nre/2)))+ire+1
                jnow = ire+j+1
                lineAdd(orderlineList,jnow,operateStripNum,blockNum)
            return orderlineList
        def orderBA(lineList):
            n = len(lineList)
            print('nstrip',n)
            orderlist = []
            for j in range(n):
                operateStripNum = int(j/2)+(j%2)*(int(np.ceil(n/2)))
                if j%2 == 0:
                    lineOrder = lineList[operateStripNum]
                else:
                    lineOrder = np.array([lineList[operateStripNum][1],lineList[operateStripNum][0]])
                plt.plot(lineOrder[:,0],lineOrder[:,1],'-b')
                plt.text(lineOrder[0][0],lineOrder[0][1],j)
                orderlist.append(lineOrder)
            return orderlist

        def orderlineRighttuning(linelist, nskip):
            nline = len(linelist)
            nInblock = nskip * 2 + 1
            Nblock = int(nline/nInblock)-1
            print('Nblock',Nblock)
            orderlist = []
            for iblock in range(Nblock):
                linesInblock = linelist[iblock*nInblock:(iblock+1)*nInblock]
                if iblock%2 != 0:
                    linesInblock.reverse()
                for ioperateIn in range(nInblock):
                    iLineIn = int(ioperateIn/2)+(ioperateIn%2)*(int(np.ceil(nInblock/2)))
                    lineOrder = linesInblock[iLineIn]
                    if (ioperateIn+iblock*nInblock)%2 != 0:
                        lineOrder = lineOrder[::-1]
                    plt.plot(lineOrder[:,0],lineOrder[:,1],color=(0.5+np.sin(iblock)/2,0.5+np.sin(2*(iblock))/2,0.5+np.sin(3*(iblock))/2))
                    plt.text(lineOrder[0][0],lineOrder[0][1],ioperateIn+iblock*nInblock)
                    orderlist.append(lineOrder)
            remainlines = linelist[Nblock*nInblock:]
            if Nblock%2 != 0:
                remainlines.reverse()
            nremain = len(remainlines)
            for ioperateRemain in range(nremain):
                iLineRemain = int(ioperateRemain/2)+(ioperateRemain%2)*(int(np.ceil(nremain/2)))
                lineOrder = remainlines[iLineRemain]
                if (ioperateRemain+Nblock*nInblock)%2 != 0:
                    lineOrder = lineOrder[::-1]
                plt.plot(lineOrder[:,0],lineOrder[:,1],'-b')
                plt.text(lineOrder[0][0],lineOrder[0][1],ioperateRemain+Nblock*nInblock)
                orderlist.append(lineOrder)
            return orderlist
        nskip = int(myve['r']*2/myve["w"])+1
        print("skip",nskip)
        linelist0 = orderline(linelist, nskip)  # FSP模式
        # linelist0=orderBA(linelist)#纯右转模式
        # linelist0=orderlineRighttuning(linelist, nskip)  #纯右转小圈模式
        return linelist0

    def getlinelist(self, li, di, w):
        hdire = np.array([-di[1], di[0]])  # 右方向单位向量
        l1 = np.array([li[2], li[2]+500*hdire])
        l2 = np.array([li[0], li[1]])
        p = self.get_crossing(l1, l2, 'l')
        wi = np.array([li[2], p])
        nu = int(np.linalg.norm(wi[1]-wi[0])/w)
        linelist = []
        p0 = li[1]-w*hdire/2
        for i in range(nu):
            pi = p0-i*w*hdire
            linei = np.array([pi, pi+di])
            pu = self.get_crossing(linei, np.array([li[1], li[2]]), 'l')
            pd = self.get_crossing(linei, np.array([li[3], li[4]]), 'l')
            linen = np.array([pu, pd])
            # print(linen)
            # plt.plot(linen[:,0],linen[:,1],'-b')
            linelist.append(linen)
        p2 = li[2]+w*hdire/2
        line2 = np.array([p2, p2+di])
        linen = np.array([self.get_crossing(line2, np.array([li[1], li[2]]), 'l'),
                          self.get_crossing(line2, np.array([li[3], li[4]]), 'l')])
        linelist.append(linen)
        return linelist

    def test(self):
        l1 = np.array([self.lineArea[2],self.lineArea[2]+500*np.array([-self.direction[1],self.direction[0]])])
        l2 = np.array([self.lineArea[0],self.lineArea[1]])
        p = self.get_crossing(l1,l2)

    def getheading(self):
        w = myve["w"]
        wo = myve["wo"]
        r = myve['r']
        d = (np.floor((r+wo/2)/w)+1)*w
        print('heading', d)
        return d

    def getdire(self, ar):
        dire = ar[5]-ar[4]
        return dire/np.linalg.norm(dire)

    def getlineArea(self, ar, di, he):
        dy = di*he
        ABline = np.array([ar[0]-dy, ar[2]+dy, ar[4]+dy, ar[5]-dy, ar[0]-dy])
        All = np.array([ar[0], ar[2], ar[4], ar[5], ar[0]])
        return ABline

    def get_crossing(self,s1,s2,mode):
        # s1线段1，s2:线段2
        # mode：状态，'s':线段；'l':直线
        xa, ya = s1[0][0],s1[0][1]
        xb, yb = s1[1][0],s1[1][1]
        xc, yc = s2[0][0],s2[0][1]
        xd, yd = s2[1][0],s2[1][1]
        # 判断两条直线是否相交，矩阵行列式计算
        a = np.matrix(
            [
                [xb-xa,-(xd-xc)],
                [yb-ya,-(yd-yc)]
            ]
        )
        delta = np.linalg.det(a)
        # 不相交,返回两线段
        if np.fabs(delta) < 1e-6:
            # print(delta)
            return None        
        # 求两个参数lambda和miu
        c = np.matrix(
            [
                [xc-xa,-(xd-xc)],
                [yc-ya,-(yd-yc)]
            ]
        )
        d = np.matrix(
            [
                [xb-xa,xc-xa],
                [yb-ya,yc-ya]
            ]
        )
        lamb = np.linalg.det(c)/delta
        miu = np.linalg.det(d)/delta
        #相交
        x = xc + miu*(xd-xc)
        y = yc + miu*(yd-yc)
        if mode == 'l':
            return np.array([x, y])
        if mode == 's':
            if lamb <= 1 and lamb >= 0 and miu >= 0 and miu <= 1:
                return np.array([x,y])
            # 相交在延长线上
            else:
                return None

    def getDis(self, p, l):
        ld = l[0]-l[1]
        vd = np.array([-ld[1],ld[0]])
        ld = np.array([p,p+vd])
        pv = self.get_crossing(ld,l,'l')
        dis = np.linalg.norm(pv-p)
        return dis


def axCreate(x, y):
    fig, ax_lst = plt.subplots(nrows=x, ncols=y, sharex=False, sharey=True)
    fig.subplots_adjust(wspace=0.1, hspace=1, left=0.1, righ=0.95, bottom=0.4)
    fig.set_size_inches(6, 4)
    plt.tight_layout()
    plt.axis("equal")
    return ax_lst


if __name__ == "__main__":
    mymap = mapopt()
    wSeed = 0.65*4
    wRak = 2.9
    wo = 4
    # for i in range(len(mymap.outline)-1):
    #     print(np.linalg.norm(mymap.outline[i+1]-mymap.outline[i]))
    wtest = 15
    wotest = 12
    myve = {"w": wtest, "wo": wotest, 'r': 10}
    
    myve = {"w": wSeed, "wo": wo, 'r': 10}
    
    mypath = plan(mymap, myve)
