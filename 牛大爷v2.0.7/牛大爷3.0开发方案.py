牛大爷3.0系统开发方案
API：
	0、获取首页  api/niudaye/
	1、注册接口  api/niudaye/register
		1、查询用户是否存在   存在返回 1001：用户已存在    
		2、不存在立即注册添加打牌注册表 user表
	
	2、登录接口	api/niudaye/login
		1、查询用户是否存在
			存在 验证密码是否相等  返回  1101 登录成功并返回cokin
			不存在  返回1002  用户不存在
	
	3、获取首页公告接口   api/niudaye/notice
		1、查询公告表 notice表 是否存在 已启用 的公告数据
		2、返回已启用公告数据jason串
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	