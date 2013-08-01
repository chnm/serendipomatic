/* New set of scripts for 1 of 10 images; these can probably be condensed? */
$(document).ready(function(){
var margin =$("#image1a").width()/2;
var width=$("#image1a").width();
var height=$("#image1a").height();
$("#image1b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image1a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image1b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image1b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image1a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image2a").width()/2;
var width=$("#image2a").width();
var height=$("#image2a").height();
$("#image2b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image2a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image2b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image2b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image2a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image3a").width()/2;
var width=$("#image3a").width();
var height=$("#image3a").height();
$("#image3b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image3a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image3b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image3b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image3a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image4a").width()/2;
var width=$("#image4a").width();
var height=$("#image4a").height();
$("#image4b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image4a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image4b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image4b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image4a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image5a").width()/2;
var width=$("#image5a").width();
var height=$("#image5a").height();
$("#image5b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image5a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image5b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image5b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image5a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image6a").width()/2;
var width=$("#image6a").width();
var height=$("#image6a").height();
$("#image6b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image6a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image6b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image6b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image6a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image7a").width()/2;
var width=$("#image7a").width();
var height=$("#image7a").height();
$("#image7b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image7a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image7b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image7b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image7a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image8a").width()/2;
var width=$("#image8a").width();
var height=$("#image8a").height();
$("#image8b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image8a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image8b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image8b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image8a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image9a").width()/2;
var width=$("#image9a").width();
var height=$("#image9a").height();
$("#image9b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image9a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image9b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image9b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image9a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});

/* New set of scripts for 1 of 10 images */
$(document).ready(function(){
var margin =$("#image10a").width()/2;
var width=$("#image10a").width();
var height=$("#image10a").height();
$("#image10b").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'});
$("#reflection2").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px'});
	$("#image10a").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image10b").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
	$("#image10b").click(function(){
		$(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0'},{duration:500});
		window.setTimeout(function() {
		$("#image10a").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:500});
		},500);
	});
});