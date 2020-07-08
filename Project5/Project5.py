import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import sys
import xlrd
import pandas as pd

from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.globals import SymbolType
from pyecharts.globals import ThemeType
 
from pyecharts.charts import Funnel,Gauge,Graph,Liquid,Parallel,Pie,Polar,Radar,Sankey,Sunburst,ThemeRiver,WordCloud,Gauge, Page,Timeline,Map,Geo
from pyecharts import options as opts
from pyecharts.charts import Page, ThemeRiver
from pyecharts.globals import ChartType, SymbolType, GeoType

def process_bar(percent, start_str='', end_str='', total_length=0):
    # print the process bar
    # 这是一个用来显示进度条的函数，因为很多图片在处理时的时间都比较长
    bar = ''.join(["\033[31m%s\033[0m"%'-'] * int(percent * total_length)) + '>'
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
    print(bar, end='', flush=True)

def Gray2RGB():
    # 从灰度到伪彩的对应关系
    def RGBtrans(pixel):
        if 0 < pixel < 64:
            return [255, 4*pixel, 0]
        elif 64 <= pixel < 128:
            return [510-4*pixel, 255, 0]
        elif 128 <= pixel < 192:
            return [0, 255, 4*pixel-510]
        else:
            return [0, 1020 - 4*pixel, 255]

    # 打开灰度图像
    img = Image.open('Gray_zibin.jpg').convert('L')
    img = np.array(img)
    width, height = np.shape(img)
    new = np.zeros((width, height,3))
    # 通过对应关系计算出RGB三通道对应的值
    for i in range(width):
        for j in range(height):
            new[i, j, :] = RGBtrans(img[i, j])
    plt.imshow(new)
    # 显示图像
    plt.show() 

def GDPplot():
    # 打开文件
    workbook = xlrd.open_workbook("GDP-fromworldbank.xls")
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    title = worksheet.row_values(3)
    GDP = []
    # 设定需要绘制折线图的国家和对应的颜色
    chart_country = ['China', 'United States', 'United Kingdom', 'Japan', 'France']
    color = ['red', 'gold','springgreen', 'fuchsia', 'royalblue']
    plot_x = title[-21:-1:]
    fig, ax = plt.subplots()
    
    
    xticks=list(range(0,len(plot_x),1))
    xlabels=[plot_x[x] for x in xticks]
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=40)
    #ax.set_yscale("log")

    for i in range(5, nrows):
        data = worksheet.row_values(i)
        GDP.append(data[0:1:] + data[4:-1:])
        country_name = data[0]
        # 如果在读取文件的时候读取到了对应国家，则进行绘图
        if country_name in chart_country:
            index = chart_country.index(country_name)
            value = data[-21:-1:]
            plt.plot(plot_x, value, label = country_name, color = color[index])
    plt.legend()
    plt.title(' Line chart of GDP in five countries')
    plt.show()

    # GDP timeline
    # 绘制动态变化图
     # 实例化时间轴
    timeline = Timeline()
    timeline.add_schema(pos_left="50%", pos_right="10px", pos_bottom="15px")
    country_names =  worksheet.col_values(0)[4::]
    # 去掉数据中"world"的部分以免数值差过大
    del country_names[-7]


    for i in range(len(plot_x)):
        # 将不同的年份做热力图并添加到时间轴中
        GDPCount = worksheet.col_values(i+4)[4::]
        del GDPCount[-7]
        GDPCountint = []
        for j in GDPCount:
            if j == '':
                GDPCountint.append(0)
            else:
                GDPCountint.append(int(j))
        maxGDP = GDPCountint[75]
        years = int(i) + 1960
        maps = Map( init_opts=opts.InitOpts(width="1900px", height="900px", bg_color="#ADD8E6", page_title= str(years) + "年全球GDP情况",theme="white"))
        # 添加各个地区的GDP到热力图中
        maps.add("GDP",[list(z) for z in zip(country_names, GDPCount)],is_map_symbol_show=False, maptype="world", label_opts=opts.LabelOpts(is_show=False), itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)"))
        maps.set_global_opts(title_opts = opts.TitleOpts(title=str(years) + "年全球GDP情况"), legend_opts=opts.LegendOpts(is_show=False), visualmap_opts = opts.VisualMapOpts(max_=maxGDP))
        timeline.add(maps, str(years))
    # 将结果导出到html中
    timeline.render("GDP变化图.html")

def quakes():
    # 对地震数据进行绘图
    quakes_data = pd.read_csv("quakes.csv")
    latitude = quakes_data['lat'].values
    longitude = quakes_data['long'].values
    mag = quakes_data['mag'].values
    index = list(range(len(mag)))
    
    #可视化
    geo = Geo()
    geo.add_schema(maptype='world')
    for i in range(len(index)):
        geo.add_coordinate(index[i], longitude[i], latitude[i])

    data_pair = [list(z) for z in zip(index, mag)]
    # 将数据添加进图中
    geo.add('震源', data_pair,symbol_size=3)
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 设置显示区间
    pieces = [
            {'max': 4, 'label': '4级以下', 'color': '#50A3BA'},
            {'min': 4, 'max': 5, 'label': '4-5级', 'color': '#E2C568'},
            {'min': 5, 'max': 6, 'label': '5-6级', 'color': '#D94E5D'},
            {'min': 6, 'max': 7, 'label': '6-7级', 'color': '#3700A4'},
            {'min': 7, 'label': '7级以上', 'color': '#81AE9F'},
        ]
    geo.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
            title_opts=opts.TitleOpts(title="震源分布")
        )
    #导出图像
    geo.render('地震地点分布.html')
        
if __name__ == "__main__":
    os.chdir(sys.path[0])
    Gray2RGB()
    GDPplot()
    quakes()