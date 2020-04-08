function myfunc(){

        $.ajax({
        url:'/get_state',
        data:{'cnm':$('#country').val()},
        type: 'GET',
        dataType:'json',
        success:function(response){
            if(response.type == 'get_state1'){
                console.log(response.result);
                $("#state").html('');
                $('#state').append('<option value="0">State:</option>');
                $.each(response.result, function(key,val){
                    $("#state").append("<option value="+val['id']+">"+val['name']+"</option>");
                });
            }
        },
        error: function(error){
            console.log(error);
        }

       });

    }
function mystate(){
     $.ajax({
     url:'/get_city',
     data:$('#state'),
     type:'GET',
     dataType:'json',
     success:function(response){
        if(response.type == 'get_city'){

             $("#city").html('');
             $("#city").append('<option value="0">City:</option>');
             $.each(response.result,function(key,val){
                $("#city").append("<option value ="+ val['id']+">"+val['name']+"</option");
                });

            }
      },
      error: function(error){
      console.log(error);
      }

     });

   }

function myemail(){
     $.ajax({
     url:'/get_email',
     data:{'eml':$('#enm').val()},
     type:'GET',
     dataType:'json',
     success:function(response){
        if(response.type == 'get_email1'){

             $(".error").html('');
             if(response. recordemail!=null){
                $('#enm').after('<span class="error" style="color:red;">Email is alreay taken</span>');

                }
            }
      },
      error: function(error){
      console.log(error);
      }

     });

   }

function check_email(){
    $.ajax({
        url:'/check_email',
        data:$('#enm'),
        type:'GET',
        dataType:'json',
        success:function(response){
            if(response.type == 'check_email'){
                $(".e_error").html('');
                if(response.result != null){
                $('#email').after('<span class="e_error" style="color:red;">That Email is Taken . Try another</span>');
                }
            }
        },
        error:function(error){
            console.log(error);
        }
    });
}


