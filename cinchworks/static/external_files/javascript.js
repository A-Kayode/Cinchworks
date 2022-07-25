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


	//This controls the hiding and showing of information till a particular user on the table is selected
	$('.vendor_service_information').hide();
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


function admin_getcusinfo(a){
	$('.user_information').show();
	data2send= {'custid':a};

	$.ajax({
		url:"/admin/ajax/getcusinfo/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			if(rsp.status == 2){
				$('#admincusbookinfo').text(rsp.message);
				$('#cid').text(rsp.custid);
				$('#cusername').text(rsp.username);
				$('#cname').text(rsp.fname + " " + rsp.lname);
				$('#cphone1').text(rsp.phone1);
				$('#cphone2').text(rsp.phone2);
				$('#cemail').text(rsp.email);
				$('#caddr').text(rsp.address);
				$('#ccity').text(rsp.city);
				$('#clga').text(rsp.lga);
				$('#cstate').text(rsp.state);
				$('#cregdate').text(rsp.regis);
				$('#acusdesc').text(rsp.fname + " " + rsp.lname + "'s Booking Information")
			}else if(rsp.status == 1){
				$('#admincusbookinfo').html(rsp.nhtml);
				$('#cid').text(rsp.custid);
				$('#cusername').text(rsp.username);
				$('#cname').text(rsp.fname + " " + rsp.lname);
				$('#cphone1').text(rsp.phone1);
				$('#cphone2').text(rsp.phone2);
				$('#cemail').text(rsp.email);
				$('#caddr').text(rsp.address);
				$('#ccity').text(rsp.city);
				$('#clga').text(rsp.lga);
				$('#cstate').text(rsp.state);
				$('#cregdate').text(rsp.regis);
				$('#acusdesc').text(rsp.fname + " " + rsp.lname + "'s Booking Information")
			}
		},
		error:function(err){ console.log(err); }
	});
}


function admin_getcusbookinfo(a){
	$('.user_booking_information').show();
	data2send= {'bookid':a};

	$.ajax({
		url:"/admin/ajax/getbookcusinfo/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			$('#acbid').text(rsp.bkid);
			$('#acbname').text(rsp.fname + " " + rsp.lname);
			$('#acbbusname').text(rsp.busname);
			$('#acbservice').text(rsp.service);
			$('#acbregdate').text(rsp.bookdate);
			$('#acbdate').text(rsp.datebook);
			$('#acbtime').text(rsp.tbook + " - " + rsp.tebook);
			$('#acblocation').text(rsp.location);
			$('#acbstatus').text(rsp.status);
			$('#acbssdesc').text(rsp.sdesc);
			$('#acbsldesc').text(rsp.ldesc);
		},
		error:function(err){ console.log(err); }
	});
}


function admin_customersearch(){
	var data= $('#custosearch').val()
	if (data == ""){
		alert("Please fill the input field before searching.");
	}else{
		data2send= {'custosearch':data};
		$.ajax({
			url:"/admin/ajax/customersearch/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
					alert(rsp.val);
				}else if(rsp.status == 1){
					$('#acuslist').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
			});
	}
}


function admin_cus_searchbooking(){
	var data= $('#cusbooksearch').val()
	var custid= $('#cid').text();
	if (data == ""){
		alert("Please fill the input field before searching.");
	}else{
		data2send= {'cusbooksearch':data, 'custid':custid};
		$.ajax({
			url:"/admin/ajax/customerbooksearch/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
					alert(rsp.val);
				}else if(rsp.status == 1 && rsp.nhtml != ""){
					$('#admincusbookinfo').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
			});
	}
}



function admin_getveninfo(a){
	$('.user_information').show();
	data2send= {'vendid':a};

	$.ajax({
		url:"/admin/ajax/getveninfo/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			if(rsp.status == 2){
				$('#adminvenbookinfo').text(rsp.message);
				$('#vid').text(rsp.vendid);
				$('#vusername').text(rsp.username);
				$('#vname').text(rsp.fname + " " + rsp.lname);
				$('#vphone1').text(rsp.phone1);
				$('#vphone2').text(rsp.phone2);
				$('#vemail').text(rsp.email);
				$('#vaddr').text(rsp.address);
				$('#vcity').text(rsp.city);
				$('#vlga').text(rsp.lga);
				$('#vstate').text(rsp.state);
				$('#vregdate').text(rsp.regis);
				$('#vbusname').text(rsp.busname);
				$('#avendesc').text(rsp.fname + " " + rsp.lname + "'s Booking Information")
			}else if(rsp.status == 1){
				$('#adminvenbookinfo').html(rsp.nhtml);
				$('#vid').text(rsp.vendid);
				$('#vusername').text(rsp.username);
				$('#vname').text(rsp.fname + " " + rsp.lname);
				$('#vphone1').text(rsp.phone1);
				$('#vphone2').text(rsp.phone2);
				$('#vemail').text(rsp.email);
				$('#vaddr').text(rsp.address);
				$('#vcity').text(rsp.city);
				$('#vlga').text(rsp.lga);
				$('#vstate').text(rsp.state);
				$('#vregdate').text(rsp.regis);
				$('#vbusname').text(rsp.busname);
				$('#avendesc').text(rsp.fname + " " + rsp.lname + "'s Booking Information");
				$('#avendesc2').text(rsp.fname + " " + rsp.lname + "'s Services Information");
			}
		},
		error:function(err){ console.log(err); }
	});
}



function admin_getvenbookinfo(a){
	$('.user_booking_information').show();
	data2send= {'bookid':a};

	$.ajax({
		url:"/admin/ajax/getbookveninfo/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			$('#avbid').text(rsp.bkid);
			$('#avcname').text(rsp.fname + " " + rsp.lname);
			$('#avbservice').text(rsp.service);
			$('#avbregdate').text(rsp.bookdate);
			$('#avbdate').text(rsp.datebook);
			$('#avbtime').text(rsp.tbook + " - " + rsp.tebook);
			$('#avblocation').text(rsp.location);
			$('#avbstatus').text(rsp.status);
			$('#avbssdesc').text(rsp.sdesc);
			$('#avbsldesc').text(rsp.ldesc);
		},
		error:function(err){ console.log(err); }
	});
}


function admin_vendorsearch(){
	var data= $('#ventosearch').val()
	if (data == ""){
		alert("Please fill the input field before searching.");
	}else{
		data2send= {'ventosearch':data};
		$.ajax({
			url:"/admin/ajax/vendorsearch/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
					alert(rsp.val);
				}else if(rsp.status == 1){
					$('#avenlist').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
			});
	}
}


function admin_ven_searchbooking(){
	var data= $('#venbooksearch').val()
	var vendid= $('#vid').text();
	if (data == ""){
		alert("Please fill the input field before searching.");
	}else{
		data2send= {'venbooksearch':data, 'vendid':vendid};
		$.ajax({
			url:"/admin/ajax/vendorbooksearch/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
					alert(rsp.val);
				}else if(rsp.status == 1 && rsp.nhtml != ""){
					$('#adminvenbookinfo').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
			});
	}
}


function admin_getvenservices(a){
	var data2send= {'vendid':a};

	$.ajax({
		url:"/admin/ajax/getvenservices/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			if (rsp.status == 1){
				$('#adminvenserviceinfo').html(rsp.nhtml);
			}else if(rsp.status == 0){
				$('#adminvenserviceinfo').text(rsp.message);
			}
		},
		error:function(err){ console.log(err); }
	});
}


function admin_getvenserviceinfo(a){
	$('.vendor_service_information').show();
	data2send= {'vensevid':a};

	$.ajax({
		url:"/admin/ajax/getvenserviceinfo/",
		type:"get",
		dataType:"json",
		data:data2send,
		success:function(rsp){
			$('#avsid').text(rsp.serid);
			$('#avsservice').text(rsp.service);
			$('#avsprice').text(rsp.price);
			$('#avsmin').text(rsp.avsmin);
			$('#avsavg').text(rsp.avsavg);
			$('#avsmax').text(rsp.avsmax);
			$('#avswork').text(rsp.work);
			$('#avsstatus').text(rsp.sstatus);
			$('#avbsssdesc').text(rsp.sdesc);
			$('#avssldesc').text(rsp.ldesc);
		},
		error:function(err){ console.log(err); }
	});
}


function cus_suspend_account(){
	if(confirm("Are you sure you want to suspend this account?")){
		var custid= $('#cid').text();
		var token= $('#csrf_token').val()
		data2send= {'custid':custid, 'csrf_token':token}

		$.ajax({
			url:"/admin/ajax/cussuspendaccount/",
			type:"post",
			dataType:"json",
			data:data2send,
			success:function(rsp){
				if (rsp.status == 1){
					alert(rsp.message);
				}else if (rsp.status == 0){
					alert(rsp.message);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
	
}


function cus_reactivate_account(){
	if(confirm("Are you sure you want to reactivate this account?")){
		var custid= $('#cid').text();
		var token= $('#csrf_token').val()
		data2send= {'custid':custid, 'csrf_token':token}

		$.ajax({
			url:"/admin/ajax/cusreactivateaccount/",
			type:"post",
			dataType:"json",
			data:data2send,
			success:function(rsp){
				if (rsp.status == 1){
					alert(rsp.message);
				}else if (rsp.status == 0){
					alert(rsp.message);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
	
}


function ven_suspend_account(){
	if(confirm("Are you sure you want to suspend this account?")){
		var vendid= $('#vid').text();
		var token= $('#csrf_token').val()
		data2send= {'vendid':vendid, 'csrf_token':token}

		$.ajax({
			url:"/admin/ajax/vensuspendaccount/",
			type:"post",
			dataType:"json",
			data:data2send,
			success:function(rsp){
				if (rsp.status == 1){
					alert(rsp.message);
				}else if (rsp.status == 0){
					alert(rsp.message);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
	
}


function ven_reactivate_account(){
	if(confirm("Are you sure you want to reactivate this account?")){
		var vendid= $('#vid').text();
		var token= $('#csrf_token').val()
		data2send= {'vendid':vendid, 'csrf_token':token}

		$.ajax({
			url:"/admin/ajax/venreactivateaccount/",
			type:"post",
			dataType:"json",
			data:data2send,
			success:function(rsp){
				if (rsp.status == 1){
					alert(rsp.message);
				}else if (rsp.status == 0){
					alert(rsp.message);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
	
}


function add_category(){
	if(confirm("Are you sure you want to add this category?")){
		form= document.getElementById('adminaddcategory');
		formdata= new FormData(form);

		$.ajax({
			url:"/admin/ajax/addcategory/",
			type:"post",
			dataType:"json",
			data:formdata,
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
				}else if(rsp.status == 1){
					$('#categorylist').html(rsp.nhtml);
					$('#catselect').html(rsp.nhtml2);
					$('#categorymess').html(`<span class= "alert alert-success">${rsp.message}</span>`);
				}
			},
			error:function(err){ console.log(err); },
			cache:false,
			contentType:false,
			processData:false
		});
	}
}


function admin_add_service(){
	if (confirm("Confirm adding this service?")){
		form= document.getElementById('adminaddservice');
		formdata= new FormData(form);

		$.ajax({
			url:"/admin/ajax/addservice/",
			type:"post",
			dataType:"json",
			data:formdata,
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
				}else if(rsp.status == 1){
					$('#servicelist').html(rsp.nhtml);
					$('#servicemess').html(`<span class= "alert alert-success">${rsp.message}</span>`);
				}
			},
			error:function(err){ console.log(err); },
			cache:false,
			contentType:false,
			processData:false
		});
	}
}


function show_booking_information(a){
	var data2send= {"bookid":a};
	$('#adminbookinginfo_modal').modal('toggle');

	$.ajax({
		url:"/admin/ajax/showbookinginfo/",
		type:"get",
		data:data2send,
		dataType:"json",
		success:function(rsp){
			if(rsp.status == 0){
				alert(rsp.message);
			}else if (rsp.status == 1){
				$('#adbkid').text(rsp.bookid);
				$('#adbkvenname').text(rsp.vendor);
				$('#adbkcusname').text(rsp.cusfname + " " + rsp.cuslname);
				$('#adbksername').text(rsp.service);
				$('#adbkserlocate').text(rsp.slocation);
				$('#adbkdt').text(rsp.dobook);
				$('#adbkbdate').text(rsp.bdate);
				$('#adbkbtime').text(rsp.tbook + " - " +rsp.tebook);
				$('#adbksershort').text(rsp.sshort);
				$('#adbkserlong').text(rsp.slong);
				$('#adbkstatus').text(rsp.bstatus);
			}
		},
		error:function(err){ console.log(err); }
	});
}


function admin_bookingsearch(){
	var data= $('#adminbooksearch').val()
	if (data == ""){
		alert("Please fill the input field before searching.");
	}else{
		data2send= {'sbook':data};
		$.ajax({
			url:"/admin/ajax/adminbookingsearch/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
					alert(rsp.val);
				}else if(rsp.status == 1){
					$('#abookinglist').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
			});
	}
}











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



/* This code quickly validates and checks if the search field when searching for services is empty on the make booking modal found on both the customer home and customer booking history */
function check_empty(){
	if($('#cbmsearch').val() == ""){
		alert("Your search field cannot be empty");
		return false
	}else{
		return true
	}
}



/* This code is used for deleting reviews for the specified vendor by the customer */
function delete_review(custid, vendid){
	var conf= confirm("Are you sure you want to delete this review?")

	if (conf){
		var data2send= {"custid":custid, "vendid":vendid};

		$.ajax({
			url:"/cus/ajax/deletereview/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 1){
					alert(rsp.message);
					$('#cusrevarea').html(rsp.nhtml);
				}else if(rsp.status == 0){
					alert(rsp.message);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
}



/* This code is used for checking the booking details of a particular customer */
function get_date(a){
	var date= $('#cvseadate').val();
	if (date == ""){
		alert("You have to select a date");
	}else{
		data2send= {'bdate':date, 'vendid':a}

		$.ajax({
			url:"/cus/ajax/getdate/",
			data:data2send,
			type:"get",
			dataType:"json",
			success:function(rsp){
				if(rsp.status == 0){
					alert(rsp.message);
				}else if(rsp.status == 1){
					$('#dateinfo_modal').modal('toggle');
					$('#dateinfo_body').html(rsp.nhtml);
				}
			},
			error:function(err){ console.log(err); }
		});
	}
}