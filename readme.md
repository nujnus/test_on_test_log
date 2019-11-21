
<img src="./tntlog.png" width="400" height="200" />

# 简介:
tntlog的目的是通过收集在e2e测试中, react发送的action, 和state的状态来判断基于react.js的前端程序运行是否正确.

## 运行截图:
![Alt Text](./sample2.gif)

# 被测的react.js项目中配置如下:
```

//中间件端配置:
const remote_log_action = store => next => action =>{

    if ( action.type != 'CREATE_REMOTE_LOG_REQUESTED' 
      && action.type != "CREATE_REMOTE_LOG_SUCCESS" 
      && action.type != "CREATE_REMOTE_LOG_FAILURE" )  {

        store.dispatch({type: 'CREATE_REMOTE_LOG_REQUESTED', payload: {
          log_backend: action.log_backend, action_type: action.type, timestamp: new Date().getTime()}
          }) 
    }

    let result = next(action);

    return result;
}

//注册saga
function* rootSaga() {
  yield [
      ...
      yield takeEvery("CREATE_REMOTE_LOG_REQUESTED",  create_remote_log_saga),
      ...
  ]
}


// saga端配置:

function* create_remote_log_saga(action) {
    try {
        console.log("remote_log_saga:", action)
        const response = yield call(axios.post, create_remote_log_url(), action.payload)
        yield put({type: 'CREATE_REMOTE_LOG_SUCCESS', payload: response.data});
    } catch(error) {
        console.log("remote_log_saga error:", error)

        yield put({type: 'CREATE_REMOTE_LOG_FAILURE'});
    }
}


```


# 测试服务器端:
## 安装:
建议python环境: Python 3.6.2

```
pip install -r requirements.txt

# 初始化数据库:
cd models
python init.py

# 安装命令行工具
cd cmdline_tool/logtest
python setup.py install

```

## 启动:
```
#启动selenium (请自行到selenium官网下载selenium包)
java -jar selenium-server-standalone-3.141.59.jar

#启动本测试服务器
python app.py
```

## 在目标项目中配置nightwatch: nightwatch.json
```
{
  "src_folders" : ["."],
  "output_folder" : "reports",

  "selenium" : {
    "start_process" : false,
    "server_path" : "",
    "log_path" : "",
    "host" : "127.0.0.1",
    "port" : 4444,
    "cli_args" : {
      "webdriver.chrome.driver" : "",
      "webdriver.ie.driver" : ""
    }
  },

  "test_settings" : {
    "default" : {
      "launch_url" : "http://localhost:3000",
      "selenium_port"  : 4444,
      "selenium_host"  : "localhost",
      "silent": true,
      "screenshots" : {
        "enabled" : false,
        "path" : ""
      },
      "desiredCapabilities": {
        "browserName": "chrome",
        "chromeOptions": {"w3c": false },
        "javascriptEnabled": true,
        "acceptSslCerts": true
      }
    },

    "chrome" : {
      "desiredCapabilities": {
        "browserName": "chrome",
        "javascriptEnabled": true,
        "acceptSslCerts": true
      }
    }
  }
}
```

## 配置测试脚本: nightwatch_job.js
```
module.exports = {
  //打开projects界面
  '加载1.projects索引': function (browser) {
    browser
      .url('http://127.0.0.1:3000/projects/')
      .pause(1000)
      .end()
  },

  //打开card1对应的map界面
  '加载2.map界面': function (browser) {
    browser
      .url('http://127.0.0.1:3000/map/d6de494c-f581-11e9-8c5a-a0999b0f755b/card1')
      .pause(1000)
      .end()
  },
  ...
}

```

## 测试运行脚本模版:test.sh
```
test() {
log_file="${1}_test"
expect_file="${1}_expect"
nightwatch  --test ./nightwatch_job.js --testcase $2
nightwatch_result=$?
curl -i -H "Content-Type: application/json;charset=UTF-8" -X POST -d "{\"target_filename\":\"$(pwd)/${log_file}\"}" http://127.0.0.1:5002/manage/tofile
curl -i -H "Content-Type: application/json;charset=UTF-8" -X POST -d "{\"target_filename\":\"$(pwd)/${log_file}\"}" http://127.0.0.1:5002/manage/tofile_data

curl -i  http://127.0.0.1:5002/manage/clear
logtest cmp --target-file ./${log_file} --expect-file ./${expect_file} --casename $2 --cwd `pwd` --nightwatch_result  ${nightwatch_result}
}


test ./log/resources_test_log_1 '加载1.projects索引'

test ./log/resources_test_log_2 '加载2.map界面'

```

## 运行测试文件
```
sh test.sh
```

## 其他:
用yaml而不是json记录log, 是因为json不支持注释.



