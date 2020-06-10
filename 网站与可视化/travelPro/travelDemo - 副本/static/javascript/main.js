$(function() {
	//图片懒加载 lazy and echo 插件
    $("img.lazy").lazyload({effect: "fadeIn"});
	echo.init({offset: 100,throttle: 250,unload: false,});
});
$(document).ready(function(){
	//tab切换
	$(".slideTab").slide({trigger:"click",switchLoad:"_src"});
	//判断搜索框是否为空
	$('#_js_search').submit(function() {
		var folder = jQuery("#_js_search_text").val();
		if (jQuery.trim(folder) == "") {
			showDialogTip({error:true,tip:"请输入您要搜索的关键词"});
			$("#_js_search_text").focus();
			return false;
		}
	});
	//微信关注widget
	var widgetWeixin = $("#widget-weixin");
	if(!zdyCookie.query('_widget_weixin')){
		widgetWeixin.show();
	}
	widgetWeixin.click(function(){
		zdyCookie.write("_widget_weixin","0","/","10");
		widgetWeixin.hide();
	});
    //弹出开通大会员
	if(!zdyCookie.query('_widget_vip')){
			$.ajax({
	        type: "GET",
	        url:"/index.php?c=dudu_233&m=api",
	        dataType: "json",
	        success: function(data){
	            if(data.code=="1"){
	            	__openVip();
	            	$(".ReactModalPortal .close").click(function(){
						layer.close(modal_weixin_layer);
					});
	            }else{
	            	zdyCookie.write("_widget_vip","0","/","14400");
	            }
	        },
	        error: function(){
	        }
	    });
	}
});