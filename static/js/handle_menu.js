var menuShown = false;
var orderShown = false;

$(document).ready(function() {
	$('#menu-button').click(function() {
		if (menuShown) {
			$('#menu').css({
				'visibility':'hidden'
			})
		} else {
			$('#menu').css({
				'visibility':'visible'
			})
		}
		menuShown = !menuShown
	})

	$('#pass').click(passOnTurn);
	$('#view-order').click(function (){
		if (orderShown) {
			$('#user-column').css({
				'visibility':'hidden'
			})
		} else {
			$('#user-column').css({
				'visibility':'visible'
			})
		}
		orderShown = !orderShown
	})
})