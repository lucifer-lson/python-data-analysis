"""
作者：Lucifer
日期：2023年06月08日
"""
import pandas as pd
import matplotlib.pyplot as plt
import folium
import os
# 假设csv文件都在同一个文件夹下，且文件名以"PRSA_Data"开头
# 获取文件夹下所有的csv文件名
csv_files = [f for f in os.listdir() if f.startswith("PRSA_Data") and f.endswith(".csv")]
# 读取每个csv文件，并将它们存储在一个列表中
df_list = []
for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)
# 将列表中的所有数据框合并成一个大的数据框
df_all = pd.concat(df_list, ignore_index=True)


class DataAnalysis:
    """
    数据分析类
    """
    # 初始化类，传入数据框作为参数
    def __init__(self, df):
        self.df = df
        # 检查数据框是否有空值
        if self.df.isnull().any().any():
            # 如果有空值，打印出空值的数量和位置
            print("The dataframe has missing values.")
            print(self.df.isnull().sum())
            # 对于含有空值的行，直接删掉，不再填充
            self.df.dropna(inplace=True)
            # 打印出处理后的数据框
            print("The dataframe after dropping missing values:")
            print(self.df)

        # 再次检查数据框是否有空值
        if self.df.isnull().any().any():
            print("The dataframe has outliers.")

    # 定义一个方法，根据给定的区域和污染物类型，返回该区域该污染物随时间的变化数据框
    def time_analysis(self, station, pollutant):
        # 过滤出给定区域的数据
        df_station = self.df[self.df["station"] == station]
        # 根据年份和月份分组，并计算给定污染物的平均值
        df_time = df_station.groupby(["year", "month"]).agg({pollutant: "mean"})
        # 重置索引，并返回结果
        df_time = df_time.reset_index()
        return df_time

    # 定义一个方法，根据给定的年份、月份和污染物类型，返回北京各区域该污染物平均值的空间分布数据框
    def space_analysis(self, year, month, pollutant):
        # 过滤出给定年份和月份的数据
        df_year_month = self.df[(self.df["year"] == year) & (self.df["month"] == month)]
        # 根据区域分组，并计算给定污染物的平均值
        df_space = df_year_month.groupby("station").agg({pollutant: "mean"})
        # 重置索引，并返回结果
        df_space = df_space.reset_index()
        return df_space


class DataVisualization:
    """
    数据可视化类
    """
    # 初始化类，传入数据分析类作为参数
    def __init__(self, data_analysis):
        self.data_analysis = data_analysis

    # 定义一个方法，根据给定的区域和污染物类型，绘制该区域该污染物随时间的变化折线图，并保存为png文件
    def time_plot(self, station, pollutant):
        # 调用数据分析类的time_analysis方法，获取时间分析结果
        df_time = self.data_analysis.time_analysis(station, pollutant)
        # 设置x轴的值为年份-月份的组合
        x = df_time["year"].astype(str) + "-" + df_time["month"].astype(str)
        y = df_time[pollutant]
        # 创建一个图形对象，并设置大小和标题
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(f"{station} {pollutant} over time")
        # 绘制折线图，并设置颜色和标签
        ax.plot(x, y, color="blue", label=pollutant)
        # 设置x轴和y轴的标签
        ax.set_xlabel("Time")
        ax.set_ylabel(pollutant)
        # 显示图例
        ax.legend()
        # 保存图形为png文件，文件名为区域和污染物的组合
        plt.savefig(f"{station}_{pollutant}.png")

    # 定义一个方法，根据给定的年份、月份和污染物类型，绘制北京各区域该污染物平均值的空间分布地图，并保存为html文件
    def space_map(self, year, month, pollutant):
        # 调用数据分析类的space_analysis方法，获取空间分析结果
        df_space = self.data_analysis.space_analysis(year, month, pollutant)
        # 使用geopandas库读取北京各区域的地理边界数据，这里假设数据文件名为"beijing.geojson"
        import geopandas as gpd
        gdf = gpd.read_file("beijing.geojson")
        # 调用数据分析类的space_analysis方法，获取空间分析结果
        df_space = self.data_analysis.space_analysis(year, month, pollutant)
        # 创建一个字典，存储监测站名称和区县名称的对应关系
        station_dict = {"Aotizhongxin": "朝阳区", "Changping": "昌平区", "Dongsi": "东城区",
                        "Guanyuan": "西城区", "Gucheng": "石景山区", "Huairou": "怀柔区", "Shunyi": "顺义区",
                         "Wanliu": "海淀区"}
        # 用字典的get方法来替换空间分析结果中的监测站名称为区县名称
        df_space["station"] = df_space["station"].apply(lambda x: station_dict.get(x))
        # 使用geopandas库读取北京各区域的地理边界数据，这里假设数据文件名为"beijing.geojson"
        import geopandas as gpd
        gdf = gpd.read_file("beijing.geojson")
        # 将空间分析结果与地理边界数据合并，根据区域名称进行匹配
        gdf = gdf.merge(df_space, left_on="name", right_on="station", how="left")

        # 对于没有空间分析结果的区域，用0来填充污染物平均值
        gdf[pollutant] = gdf[pollutant].fillna(0)
        # 创建一个地图对象，并设置中心点和缩放级别
        m = folium.Map(location=[39.9, 116.4], zoom_start=10)
        # 添加一个标题层，并设置标题内容和位置
        title_html = f"<h3 align='center' style='font-size:20px'><b>{year}-{month} {pollutant} in Beijing</b></h3>"
        m.add_child(folium.Element(title_html))  # 使用add_child方法
        # 使用folium.Choropleth方法来根据污染物平均值的不同范围显示不同的颜色，并设置相关参数
        choro = folium.Choropleth( # 将方法赋值给一个变量
            geo_data=gdf, # 地理边界数据
            data=df_space, # 空间分析结果
            columns=["station", pollutant], # 区域名称和污染物平均值列
            key_on="feature.properties.name", # 区域名称属性
            fill_color="YlOrRd", # 填充颜色方案
            fill_opacity=0.7, # 填充透明度
            line_opacity=0.2, # 线条透明度
            legend_name=f"{pollutant} (ug/m3)", # 图例名称
            bins=[0, 50, 100, 150, 200, 250], # 污染物平均值的范围划分
            highlight=True, # 是否高亮显示选中区域
            data_type="json", # 指定data的类型为"json"
            geo_data_type="json" # 指定geo_data的类型为"json"
        )
        choro.add_to(m) # 将变量添加到地图对象上
        # 将gdf对象转换成folium.GeoJson对象，并赋值给一个变量
        geojson = folium.GeoJson(gdf)
        # 添加一个弹出框层，并显示区域名称和污染物平均值
        popup = folium.features.GeoJsonPopup(  # 将方法赋值给一个变量
            fields=["name", pollutant],  # 区域名称和污染物平均值属性
            aliases=["Station", pollutant],  # 属性别名
            labels=True  # 是否显示标签
        )
        geojson.add_child(popup)  # 将变量添加到geojson对象上
        # 将geojson对象添加到地图对象上
        geojson.add_to(m)

        # 保存地图为html文件，文件名为年份、月份和污染物的组合
        m.save(f"{year}_{month}_{pollutant}.html")


if __name__ == "__main__":
    # 创建一个数据分析对象，并传入合并后的数据框
    da = DataAnalysis(df_all)
    # 创建一个数据可视化对象，并传入数据分析对象
    dv = DataVisualization(da)
    dv.time_plot("Aotizhongxin", "PM2.5")
    # 绘制2015年11月北京各区域PM2.5平均值的空间分布地图，并保存为html文件
    dv.space_map(2015, 11, "PM2.5")








