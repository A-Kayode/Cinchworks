/* This file contains most if not all of the javascript I will be using. I hate scrolling with a passion */


/*This section contains code for the admin page*/
function hidepanel(){
	if($(window).width() < 426){
		$('#admin_sidepanel').hide();
		$('#panel_shower').show();	
	}else{
		$('#admin_sidepanel').show();
		$('#panel_hider').hide();
		$('#panel_shower').hide();	
	}
}


$(document).ready(function(){
	hidepanel();
	var links= "#admin_users_link, #admin_booking_link"
	var tabs= "#admin_users_tab, #admin_booking_tab"
	//This controls the actions when a link is clicked
	$(links).click(function(){
		//This adds the active class to the link
		if ($(links).hasClass("active")){
			$(links).removeClass("active");
		}
		$(this).addClass('active');

		//This activates and deativates the tabbed contents
		if ($(tabs).hasClass("show active")){
			$(tabs).removeClass("show active");
		}
		if ($(this).attr("href") == "#admin_users_tab"){
			$("#admin_users_tab").addClass("show active");
		}else if($(this).attr("href") == "#admin_booking_tab"){
			$("#admin_booking_tab").addClass("show active");
		}else {}
	});


	//This controls the hiding and showing of information when customer or vendor is checked
	$('.specific_vendor_info').hide()
	$('.admin_choice').click(function(){
		if ($('#pick_customer').prop("checked") == true){
			$('.specific_vendor_info').hide();
			$('.specific_customer_info').show();
		}else{
			$('.specific_vendor_info').show();
			$('.specific_customer_info').hide();
		}
	});


	//This controls the hiding and showing of information till a particular user on the table is selected
	$('.user_information').hide();
	$('.user_booking_information').hide();
	$('.user_table').click(function(){
		$('.user_information').show();
		//will need to add more code to ensure values are placed in the right subheadings
	});
	$('.user_booking_table').click(function(){
		$('.user_booking_information').show();
	});


	//This controls the hiding and showing of information on the all bookings area
	$('.admin_booking_information').hide();
	$('.admin_booking_table').click(function(){
		$('.admin_booking_information').show();
	});


	//Admin logout is handled here
	$('#admin_logout').click(function(){
		var exit= confirm("Do you want to continue to log out?");
		if (exit == true){
			$('#admin_logout').attr('href','/')
		}
	});


	//This will control the responsiveness of the side panel
	$(window).resize(function(){
		hidepanel();
	});
	$('#panel_shower').click(function(){
		$('#admin_sidepanel').show();
		$('#panel_hider').show();
		$('#panel_shower').hide();
		$('.main_content').click(function(){
			$('#admin_sidepanel').hide();
			$('#panel_shower').show();
		});
	});
	$('#panel_hider').click(function(){
		$('#admin_sidepanel').hide();
		$('#panel_hider').hide();
		$('#panel_shower').show();
	});
	
});



/* This code caters for the login forms on both the home page and the dedicated login page */
$(document).ready(function(){
	//This code caters to selecting whether you want to login as a customer, vendor or admin
	$('#sel_customer').prop('checked', true);
	$('#sel_vendor').click(function(){
		$('#login_form').attr('action', 'vendor_home.html')
	});
	$('#sel_customer').click(function(){
		$('#login_form').attr('action', 'user_home.html')
	});
	$('#login_button').click(function(){
		if($('#login_username').val().toLowerCase() == "admin"){
			$('#login_form').attr('action', '/admin');
		}
		$('#login_button').attr('type','submit');
	})
});



/* This code caters for the signup page */
$(document).ready(function(){
	$('#signup_sel_customer').prop('checked', true);
	$('#signup_sel_vendor').click(function(){
		$('#signup_form').attr('action', 'vendor_home.html')
	});
	$('#signup_sel_customer').click(function(){
		$('#signup_form').attr('action', '/signup')
	});
	//This code checks the username before allowing signup
	$('#signup_button').click(function(){
		if($('#signup_username').val().toLowerCase() == "admin"){
			alert("You cannot signup with the username 'admin'. Please choose another one.")
		}else{
			if ( $('[name= "pswd"]').val() != $('[name= "cpswd"]').val() ){
				$('#signup_button').attr('type','button')
				alert("Password doesn not match")
			}else{
				$('#signup_button').attr('type','submit')
			}
			
		}
	});
});