# ihome_python  
flask搭建一个租房网站  
数据库：mysql， 缓存数据库：redis， 框架：flask ，页面：html,css,JavaScript,ajax  
  
config.py:配置文件，数据用户名密码等 manage.py:作为项目启动文件，在开发过程中，进行调试  
  
第二级ihome文件夹   
  init.py:模块初始化文件，  
  Flask 程序对象的创建必须在   
  init.py 文件里完成， 然后我们就可以安全的导入引用每个包   
  constants.py:保存开发过程中用到的变量值   
  models.py:存放模型，映射数据库中表   
  web_html.py:提供静态文件的蓝图,设置cookie值   
  libs文件夹：存放外部功能函数，模块的文件夹，容联云发送手机验证码   
  static文件夹：存放静态文件，html,js,图片等   
  utils文件夹：存放图片验证码模块函数  
    
  第三层api_1_0文件夹：蓝图   
    keys:存放支付宝密钥和私钥   
    init.py:模块初始化文件，注册蓝图文件里完成， 然后我们就可以安全的导入引每个视图模块   
    houses.py:房子管理视图函数，包括发布房子，查看房子信息等等   
    orders.py:订单管理视图函数，生成订单等功能   
    passport.py:手机验证码管理视图函数，包括生成手机验证码，验证手机验证码是否正确等功能   
    pay.py:支付功能视图函数，支付宝支付等功能   
    profile.py:个人信息管理功能函数，注册，修改，上传个人头像等功能   
    verify_code.py:图片验证码管理视图函数，包括生成图片验证码，验证图片验证码是否正确等功能  
