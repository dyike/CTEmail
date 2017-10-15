## CTEmail

CTEmail 的全称是Charts and Text Email，是一个发送带有图表[注意：图片不是在附件里！！！]邮件的简单粗暴的脚本。

### 为什么要有这么一个东西？
* 没有一个不懒的程序员，做啥都想着写个脚本跑一下，跑个脚本抢月饼，跑个脚本...能用脚本的干嘛不用脚本。每天的数据报表需要一个邮件脚本发送。
* 对接了各大厂商，每天每周每月都会往来邮件。报表用图表的形式更简单直观的反馈数据，为什么我们不在邮件中使用图表。
* 各大厂商的邮件中图表都是小姐姐手动制作，手动发出%>_<%，为什么不跑一个脚本。
* 如果解决上面的问题，是不是解放了小手。1) 用数据生成图表，2) 将图表拼接到邮件中发出。

### 哪些群体需要这个？
* 产品同学，图表是展示数据的最佳实践！
* 运营同学，图表是展示报表的最佳实践！
* 技术同学，为了继续懒下去！
* ...零编程基础的同学都能使用【只要会科学上网就能解决一切】


## 环境配置 && 技术要求

* Python：Python2(只需要修改little的代码就能在Python3的情况使用)
* [Plotly](https://plot.ly/) 一个图表画展示数据的工具，支持离线静态化显示和在线使用。在线可以生成图表的图片保存到本地(离线模式也能保存，不过需要手动保存，因为懒，觉得不好用！)。这个不多介绍，看懂官方文档，就会使用！

## 项目结构

```
├── README.md
├── content
│   ├── image1.png
│   ├── image2.png
│   └── index.html
├── ctemail.py
├── get_img.py
└── send.py
```

* content文件夹下面，`index.html`是邮件内容的html文件，其余图片资源，生成的图表图片。
* `ctemail.py` 发送邮件的封装
* `send.py` 发送邮件的脚本，只需要简单的配置即可。
* `get_img.py` 使用plotly生成图表的图片


## 使用

1） 配置脚本
```python
from ctemail import CTEmail
e = CTEmail('Your email acount', 'Your password')
# " ./content/ 邮件文件的路径 "
e.send_email('Test Email', './content/', ['i@ityike.com'])
```

2）处理数据，生成图片

在这里可以有自己处理数据的逻辑，最终还可以增加生成`conten/index.html`模板文件的逻辑

```python
import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('Your account', 'API Token') # 注意：这里是plotly网站的用户名和密码

trace = go.Bar(x=[2, 4, 6], y= [10, 12, 15])
data = [trace]
layout = go.Layout(title='A Simple Plot', width=800, height=640)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='./content/image.png')
```

3）说明邮件的模板文件

使用标签<EMAIL_IMG>将img标签包起来，确保能够被正确的解析替换。
```html
    <a>
        <EMAIL_IMG><img src="image1.png"></EMAIL_IMG>
    </a>
    <a>
        <EMAIL_IMG><img src="image2.png"></EMAIL_IMG>
    </a>
```

4）发送邮件

```bash
python send.py
```

## 最终的效果图

![demo](https://raw.githubusercontent.com/dyike/CTEmail/master/images/demo.jpeg)




