

$(function() {
	$("#submit").click(function() {
		var links = $(".links").val();
		if (links =='') {
			$('.success').fadeOut(200).hide();
			$('.error').fadeOut(200).show();
		} else {
			$.ajax({
				type: "POST",
				url: "/reporte/agregar/",
				data: links,
				success: function(){
					$('.success').show('slow');
					$('.error').fadeOut(200).hide();
					$('.links').val('');
				}
			});
		}
		return false;
	});
});



