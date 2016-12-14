# 开发

## 上传 pypi

配置 `~/.pypirc` :

```
$ cat ~/.pypirc 
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = 用户名
password = 密码
```

注册：

```
python3 setup.py register
```

上传：

```
python3 setup.py sdist upload
```

**注意** `python3 setup.py bdist_wheel` 需要先安装 wheel : 

```
sudo -H pip3 install wheel
```
