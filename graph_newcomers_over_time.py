import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = "./timeline_likes.csv"
df = pd.read_csv(path)
brands = list(set(df["brandId"]))
brand = brands[1]


def get_image_points(df, brand):
    brand_df = df[df["brandId"] == brand].drop("brandId", 1)
    image_only = brand_df[brand_df["hasImage"] == True][brand_df["hasUrl"] == False].drop("hasImage",1).drop("hasUrl",1)
    remove_null = image_only[image_only["timestamp"].notna()][image_only["newcomer_count"].notna()]
    rolling = (remove_null.timestamp[2:].rolling(window=10).mean(),remove_null.newcomer_count[2:].rolling(window=10).mean())
    remove_na =  (rolling[0][rolling[0].notna()],rolling[1][rolling[1].notna()])
    return remove_na

def get_text_points(df, brand):
    brand_df = df[df["brandId"] == brand].drop("brandId", 1)
    image_only = brand_df[brand_df["hasImage"] == False][brand_df["hasUrl"] == False].drop("hasImage",1).drop("hasUrl",1)
    remove_null = image_only[image_only["timestamp"].notna()][image_only["newcomer_count"].notna()]
    rolling = (remove_null.timestamp[2:].rolling(window=10).mean(),remove_null.newcomer_count[2:].rolling(window=10).mean())
    remove_na =  (rolling[0][rolling[0].notna()],rolling[1][rolling[1].notna()])
    return remove_na

def get_url_points(df, brand):
    brand_df = df[df["brandId"] == brand].drop("brandId", 1)
    image_only = brand_df[brand_df["hasImage"] == False][brand_df["hasUrl"] == True].drop("hasImage",1).drop("hasUrl",1)
    remove_null = image_only[image_only["timestamp"].notna()][image_only["newcomer_count"].notna()]
    rolling = (remove_null.timestamp[2:].rolling(window=10).mean(),remove_null.newcomer_count[2:].rolling(window=10).mean())
    remove_na =  (rolling[0][rolling[0].notna()],rolling[1][rolling[1].notna()])
    return remove_na

def get_both_points(df, brand):
    brand_df = df[df["brandId"] == brand].drop("brandId", 1)
    image_only = brand_df[brand_df["hasImage"] == True][brand_df["hasUrl"] == True].drop("hasImage",1).drop("hasUrl",1)
    remove_null = image_only[image_only["timestamp"].notna()][image_only["newcomer_count"].notna()]
    rolling = (remove_null.timestamp[2:].rolling(window=10).mean(),remove_null.newcomer_count[2:].rolling(window=10).mean())
    remove_na =  (rolling[0][rolling[0].notna()],rolling[1][rolling[1].notna()])
    return remove_na

def get_points(df, function):
    points = []
    for brand in brands:
        points.append(function(df, brand))
    return points

def plot_timeline(df, function):
    points = get_points(df, function)
    for point in points:
        plt.plot(point[0], point[1])

def set_image_plt():
    plt.subplot(2,2,1)
    plot_timeline(df, get_image_points)
    plt.ylabel('Count of New Interactors')
    plt.xlabel('Timestamp')
    plt.title('New Interactor Count vs Timestamp\nFor Image and Text Twitter Posts')
    plt.xlim(1484823728, 1586054115)

def set_text_plt():    
    plt.subplot(2,2,2)
    plot_timeline(df, get_text_points)
    plt.ylabel('Count of New Interactors')
    plt.xlabel('Timestamp')
    plt.title('New Interactor Count vs Timestamp\nFor Text-Only Twitter Posts')
    plt.xlim(1484823728, 1586054115)

def set_url_plt():
    plt.subplot(2,2,3)
    plot_timeline(df, get_text_points)
    plt.ylabel('Count of New Interactors')
    plt.xlabel('Timestamp')
    plt.title('New Interactor Count vs Timestamp\nFor Url and Text Twitter Posts')
    plt.xlim(1484823728, 1586054115)

def set_both_plt():
    plt.subplot(2,2,4)
    plot_timeline(df, get_both_points)
    plt.ylabel('Count of New Interactors')
    plt.xlabel('Timestamp')
    plt.title('New Interactor Count vs Timestamp\nFor Url and Image Twitter Posts')
    plt.xlim(1554823728, 1586054115)


class BrandChange:
    def __init__(self, brand):
        self.brand = brand
        self.text_count = len(get_text_points(df,brand)[0])
        self.image_count = len(get_image_points(df,brand)[0])
        self.url_count = len(get_url_points(df,brand)[0])
        self.both_count = len(get_both_points(df,brand)[0])
        self.total = text_count + image_count +  url_count + both_count
        self.text_percentage = self.text_count / self.total * 100
        self.image_percentage = self.image_count / self.total * 100
        self.url_percentage = self.url_count / self.total * 100
        self.both_percentage = self.both_count / self.total * 100
        self.text_change = self.get_change(get_text_points)
        self.image_change = self.get_change(get_image_points)
        self.url_change = self.get_change(get_url_points)
        self.both_change = self.get_change(get_both_points)
    def get_change(self, type_function):
        data = type_function(df,self.brand)
        if len(data[1]) < 2:
            return 0
        starting = list(data[1])[0]
        end = list(data[1])[-1]
        change = end  - starting
        return change
        

brand_changes = []
for brand in brands:
    brand_change = BrandChange(brand)
    brand_changes.append(brand_change)


def get_improvement(text_percent, image_percent, url_percent, both_percent):
    mainly_text = list(filter(lambda x: x.text_percentage >= text_percent, brand_changes))
    text_change = np.average(list(map(lambda x: x.text_change, mainly_text))) * len(mainly_text)
    mainly_image = list(filter(lambda x: x.image_percentage >= image_percent, brand_changes))
    image_change = np.average(list(map(lambda x: x.image_change, mainly_image))) * len(mainly_image)
    mainly_url = list(filter(lambda x: x.url_percentage >= url_percent, brand_changes))
    url_change = np.average(list(map(lambda x: x.url_change, mainly_url))) * len(mainly_url)
    mainly_both = list(filter(lambda x: x.both_percentage >= both_percent, brand_changes))
    both_change = np.average(list(map(lambda x: x.both_change, mainly_both))) * len(mainly_both)
    return (text_change + image_change + url_change + both_change) / (len(mainly_text) + len(mainly_image) + len(mainly_url) + len(mainly_both))

max_improvement = -400
most_improved = None
for text_percent in range(0,100):
    for image_percent in range(0,100):
        for url_percent in range(0,100):
            for both_percent in range(0,100):
                if text_percent + image_percent + url_percent + both_percent == 100:
                    improvement = get_improvement(text_percent, image_percent, url_percent, both_percent)
                    if improvement > max_improvement:
                        max_improvement = improvement
                        mostImproved = (text_percent, image_percent, url_percent, both_percent)
                        print(improvement, text_percent, image_percent, url_percent, both_percent)
# 10, 53, 75, 13
# 1%, 70%, 47%, -10%

# Best combination for highest improvmenet 324.4%, 0 6 86 8

brand = brands[5]
print(text_count / total, image_count / total, url_count / total, both_count / total)


set_text_plt()
set_image_plt()
set_url_plt()
set_both_plt()
plt.subplot_tool()
plt.show()




