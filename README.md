### 项目移植教程

#### 1. 环境配置

* 本项目基于python版本3.12.0，自行下载适合系统的版本，并配置好环境，[官方下载链接](https://www.python.org/downloads/release/python-3120/)。
* 编译器建议使用VS code，pycharm等，跨平台、适配性高。
* 本项目数据库使用MySQL5.7版本，可以直接下载系统原生版本或docker容器。

#### 2. 构建项目

* `git clone 本项目链接`或者直接 download zip本地打开。

* 用编译器打开或者命令行进入项目目录，首先安装虚拟环境库。

  ```bash
  pip install virtualenv
  ```

  创建虚拟环境。

  ```bash
  virtualenv myenv
  ```

  激活虚拟环境（Windows）

  ```bash
  .\myenv\Scripts\activate
  ```

  Unix/Linux/Macos

  ```bash
  source myenv/bin/activate
  ```

  安装项目所需依赖。

  ```bash
  pip install -r requirements.txt
  ```

* 修改项目设置

  进入/CExamSys/CExamSys/settings.py修改如下部分为你自己的数据库设置。

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'mysql.connector.django',
          'NAME': 'your_database',
          'USER': 'your_username',
          'PASSWORD': 'your_password',
          'HOST': 'your_host',
          'PORT': 'your_port',
          'OPTIONS': {
              'charset': 'utf8mb4',
              
          },
      }
  }
  ```

#### 3. 运行项目

* 首先进行数据库迁移

  ```bash
  python manage.py makemigrations #构建迁移
  python manage.py migrate #实施迁移
  #(可选命令)如果需要测试数据进行试验的话可以导入题目数据
  mysql -u [username] -p[password] question_bank < question_bank_dump.sql
  ```

* 运行项目

  ```bash
  python manage.py runserver
  ```

#### 4. 效果查看

* 项目页面地址集：

  ```
  http://127.0.0.1:8000/user/register  #注册页面
  http://127.0.0.1:8000/user/login     #登录页面
  http://127.0.0.1:8000/dashboard      #系统主页（需先登录）
  ```

  

