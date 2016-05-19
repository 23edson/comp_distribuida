<html>

  <head>
    <style>
      input{border:0px solid #000; margin:0; background:transparent; width:100%}
table tr td{border-right:1px solid #000; border-bottom:1px solid #000;}
table{background: #fff none repeat scroll 0 0;
    border-left: 1px solid #000;
    border-top: 1px solid #000;}
    table tr:nth-child(even){background:#ccc;}
    table tr:nth-child(odd){background:#eee;}

    </style>
    
    <script type="text/javascript">
    		$("input").keypress(function(event)) {
    			if(event.which == 13){
    				event.preventDefault();
    				var id = $(this).attr('id');
    				alert("input :" + id);
    				$("form1").submit();
    			}
    			
    		});
    </script>

  </head>

<body>

  <h1> PLANILHA 1</h1>
 
  <form id="form1" name="form1 "action="/send" method="POST" >
  	<table cellpadding="0"; cellspacing="0">
	<tr>
	 	
  		%for (i) in layoutx:
  			<td width="100"> <p align="center"><b > {{i}} </b></p> </td>
  		%end
  	</tr>
  	%c = len(layoutx)-1
	%flag = c
	%c = c * len(layouty)
	%count = 1  	
	%salt = flag
	
  	
  	
   %for (j) in layouty:
  		<tr>
		<td width="100"> <p align="center"><b> {{j}} </b></p> </td>
		%for (index,item) in enumerate(messages):
			%if count<=flag and index >= count-1:
				%if ';' in item[1]:
					<td width="100"><input name="message{{count}}" type="text" value="{{item[0]}}" /></td>
					
					%flag = salt + flag
					%count = count + 1
					%break
				%else:
					<td width="100"><input name="message{{count}}" type="text" value="{{item[0]}}" /></td>
					%count = count+1
				%end
			%end
		%end	
		</tr>
	%end	
		
   		
  	
    
  	</table>
  	<input type="submit" style="visibility: hidden;"/>
  	
  	</form> 
  

</body>

</html>
