# Image-Retrieval-
应用Bof+visual vocabulary+4TF-IDF算法的图像检索程序

## 开发环境
- Windows

## IDE
- Pycharm

## 语言
- Python3

## 功能列表
- 检索相似图片
- 计算准确度、运行时间、召回率
- 重排序后可提升准确度

## 效果预览
![image](https://user-images.githubusercontent.com/72118993/194085942-d8ee99fd-716c-44f2-a400-b1e2680b4650.png)

## 实现的算法原理

### 1. 利用SIFT算法提取特征向量

### 2. 处理特征向量，并用kmeans算法进行聚类

### 3. 映射到灰度直方图

### 4. 计算IDF并用欧式距离进行排序

### 5. 进行重聚类，提高精确度

## 算法流程图
- 基本检索

![image](https://user-images.githubusercontent.com/72118993/194087312-f66c4565-23d7-4349-8e68-f2a694c02d82.png)

- 重排序

![image](https://user-images.githubusercontent.com/72118993/194088443-dd4e35e5-f50a-42c8-8fad-3b522bbd02b2.png)
