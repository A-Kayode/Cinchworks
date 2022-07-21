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
});



/* This code caters for the signup page */
$(document).ready(function(){
	$('#signup_sel_customer').prop('checked', true);
	
});



/* This caters for the customer settings page */
$(document).ready(function(){
	$('#cancel_cuspersonal').hide();
	$('#edit_cuspersonal').click(function(){
		$('.cus_personal').prop('disabled', false);
		$('#cancel_cuspersonal').show();
		$('#edit_cuspersonal').hide();
	});
	$('#cancel_cuspersonal').click(function(){
		$('.cus_personal').prop('disabled', true);
		$('#cancel_cuspersonal').hide();
		$('#edit_cuspersonal').show();
	});
});



/* This caters for the vendor settings page */
$(document).ready(function(){
	//This caters for the editing of the profile information
	$('#cancel_venpersonal').hide();
	$('#edit_venpersonal').click(function(){
		$('.ven_personal').prop('disabled', false);
		$('#cancel_venpersonal').show();
		$('#edit_venpersonal').hide();
	});
	$('#cancel_venpersonal').click(function(){
		$('.ven_personal').prop('disabled', true);
		$('#cancel_venpersonal').hide();
		$('#edit_venpersonal').show();
	});

	//This caters for script used in the adding service section of the page
	$('#vspaddservice').change(function(){
		if ( $('#vspaddservice').val() == "others" ){
			$('#othservice').attr('type', 'text');
		}else{
			$('#othservice').attr('type', 'hidden');
		}
	});
});



function add_offday(a){
	var conf= confirm("Are you sure you want to add these offdays?");
	if (conf){
		var form= document.getElementById("venaddoffday");
		var formdata= new FormData(form)
		formdata.append("vendid", a);

		$.ajax({
			url:"/ven/ajax/addoffday/",
			type:"post",
			dataType:"json",
			data:formdata,
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
				}else if(rsp.status == 1){
					var x= `<span class= "alert alert-success">${rsp.message}</span>`;
					$('#sucmess').html(x);
					$('#offst').val("");
					$('#offen').val("");
				}
			},
			error:function(err){ console.log(err); },
			cache:false,
			contentType:false,
			processData:false

		});
	}
}



/* This caters for the vendor home page */
$(document).ready(function(){
	//This caters for the appearance and disappearance of the change picture form
	$('#hppic_change').hide();
	$('#hpchangepic').click(function(){
		$('#hppic_change').show();
	});
	$('#hpcancelchange').click(function(){
		$('#hppic_change').hide();
	});
	$('#hpsavechange').click(function(){
		$('#hppic_change').hide();
	});
});



/* This code is general for creating a modal that shows the information of the customer booking clicked*/
function show_info(a){
	$('#bookinginfo_modal').modal('toggle');
	var data2send= {'bookid':a};

	$.ajax({
		url:"/cus/ajax/displaybooking/",
		data:data2send,
		type:"get",
		dataType:"json",
		success:function(rsp){
			if (rsp.status == 1){
				$('#bkvenname').text(rsp.vname);
				$('#bkvenph1').text(rsp.vph1);
				$('#bkvenph2').text(rsp.vph2);
				$('#bksername').text(rsp.sname);
				$('#bksershort').text(rsp.sshort);
				$('#bkserlong').text(rsp.slong);
				$('#bkbdate').text(rsp.bdate);
				$('#bkbtime').text(rsp.btime + " - " + rsp.betime);
				if (rsp.slocation == "vendor_address"){
					var c = "Vendor Shop"
				}else if(rsp.slocation == "customer_address"){
					var c= "Home"
				}
				$('#bkserlocate').text(c);
				$('#bknotes').text(rsp.bnotes);
				if (rsp.vlga != ""){ var e = rsp.vlga + " LGA" }else{ var e= "" }
				if (rsp.vstate != ""){ var f = rsp.vstate + " state." }else{ var f= "" }
				if(rsp.slocation == "vendor_address"){
					$('#bkvenadd').text(`${rsp.vaddr}, ${rsp.vcity}, ${e}, ${f}`);
				}
			}else{
				alert(rsp.message);
			}
			
		},
		error:function(err){ console.log(err); }
	});
}



/* This code is general for creating a modal that shows the information of the vendor booking clicked*/
function ven_show_info(a){
	$('#venbookinginfo_modal').modal('toggle');
	var data2send= {'bookid':a};

	$.ajax({
		url:"/ven/ajax/displaybooking/",
		data:data2send,
		type:"get",
		dataType:"json",
		success:function(rsp){
			if (rsp.status == 1){
				$('#bkcusname').text(rsp.cfname + " " + rsp.clname);
				$('#bkcusph1').text(rsp.cph1);
				$('#bkcusph2').text(rsp.cph2);
				$('#bksername').text(rsp.sname);
				$('#bksershort').text(rsp.sshort);
				$('#bkserlong').text(rsp.slong);
				$('#bkbdate').text(rsp.bdate);
				$('#bkbtime').text(rsp.btime + " - " + rsp.betime);
				if (rsp.slocation == "vendor_address"){
					var c = "Shop"
				}else if(rsp.slocation == "customer_address"){
					var c= "Customer Address"
				}
				$('#bkserlocate').text(c);
				$('#bkcusnotes').text(rsp.bnotes);
				if (rsp.clga != ""){ var e = rsp.clga + " LGA" }else{ var e= "" }
				if (rsp.cstate != ""){ var f = rsp.cstate + " state." }else{ var f= "" }
				if(rsp.slocation == "customer_address"){
					$('#bkcusadd').text(`${rsp.caddr}, ${rsp.ccity}, ${e}, ${f}`);
				}
			}else{
				alert(rsp.message);
			}
		},
		error:function(err){ console.log(err); }
	});
}

