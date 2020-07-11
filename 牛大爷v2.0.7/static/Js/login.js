//<script src="Js/jquery-3.4.1.min.js"></script>
// 登录的触发
$(document).ready(function(){
    $("#lg").click(function(){
	//验证账号密码是否为空 如果是默认值则提示账号不能为空
		if ( $("#userv").val()=="请输入您的账号"){
			$("#biaoqian").html("账号不能为空");
			}
		else {      //否则密码为空的话提示密码不能为空
				if ( $("#passwordv").val()==""){
					$("#biaoqian").html("密码不能为空");
				 }else {   //否则 那就是密码用户名全有 则调用用户查询接口验证是否存在
					// POST一个json数据

					var na = $("#userv").val();  //获取用户名的值
					var pw = $("#passwordv").val();  //获取密码
					var daa={"name":na,"pwd":pw}    //组成字典格式的用户名和密码
					//alert("开始登入账户"+na+"开始登入密码"+pw);
						$.ajax({
									  
									type: "POST",   //请求类型 post
									url:'http://127.0.0.1:1023/login',   //接口地址
									data:daa,     //参数
									Type:"json",   //参数类型json
									success:function(data) {  //接口的响应数据 接口返回json格式
										var c=data.code;   //读取返回数据中的蚕食code的值
										if (c=='0001'){
											$("#biaoqian").html("用户名或密码错误"); //需要用html函数改变p标签内容 vel只适合更改文本
										}else if(c=='0000'){
											$("#biaoqian").html("该用户未注册");
										}else if(c=='2000'){
											$("#biaoqian").html("登入成功");
											window.location.href="http://127.0.0.1:1023/index";
										}else if(c=='5000'){
											$("#biaoqian").html("服务器故障");
										}else if(c=='5001'){
											$("#biaoqian").html("请求为空");
										}else if(c=='5002') {
                                            $("#biaoqian").html("登入接口异常");
                                        }
															},
									error:function(xhr,type){  //异常日志 转换成json
										alert(JSON.stringify(xhr),JSON.stringify(type));
														}

									
								}); 
							
				    	}
			 }				
    });
  });
// 清空按钮触发 后期改成注册
$(document).ready(function(){
    $("#del").click(function(){
        $("#userv").val("请输入您的账号");
		$("#passwordv").val("");
		$("#biaoqian").html("");
    });
  });

// 获得焦点清空初始提示语逝去焦点值为空则恢复初始提示语
$(document).ready(function(){ //死格式  框架格式 程序入口
  $("#userv").focus(function(){  //#代表id标签  。focus获得焦点的意思
	$(this).val("");        //this指向函数自己  val 值为空 清空这个输入框
	$("#biaoqian").html("");        //因为是改P标签的值 用html语句更改标签的值
  });
  $("#userv").blur(function(){          //失去焦点的触发动作
	 if ($(this).val() =='')
	 {
		 $(this).val("请输入您的账号");
		 $("#biaoqian").html("");
	 }; 
  });
});


















