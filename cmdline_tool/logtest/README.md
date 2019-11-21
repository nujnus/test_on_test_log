# 测试方法:

1. 先在store的middleware模块中注入remote log的测试客户端.

2. 建立应用的多个版本, 绑定到不同页面上.

3. 用nightwatch来运行各个版本的e2e测试.

4. 准备用比较 "测试产生的日志结果文件" 的"期望文件".

5. 用testlog cmp 来比较 两文件. => 给出测试结果.

# 自动化方案:

```
要编写的内容:
  1. 版本整合文件;
  2. e2e测试;
  3. 期望文件;
  4. 测试启动的命令行;

脚本的伪代码流程:(((暂定为shell脚本)))
   nightwatch运行e2e => 指向不同的版本(整合了中间件的集成度不同的版本) => 测试完了用testlog cmp 比较 日志和期望文件.

```

# 暂定的测试目录结构:
```
├── test.sh
├── expected
│   ├── version1_expected.log
│   └── version2_expected.log
├── test_with_selenium
│   ├── nightwatch.json
│   └── testflow.js
└── version
    ├── version1.html
    ├── version1.js
    ├── version2.html
    └── version2.js
```

# 暂时的比较两个json的方案: 通过dict来比较
```
dict2 = {"1":"123", "2":{"3":"4567"}}
dict = {"1":"123", "2":{"3":"4567"}}
dict2 == dict
#=>  True
```

# 计划中的脚本的大致形式

```
cd ./nighwatch
nightwatch    #=>产生log文件

cd ../test
sh ./test.sh  #比较log文件 并产生输出.
```
