<html>

  <head>
    <style>
      input{border:0px solid #000; margin:0; background:transparent; width:100%;text-align: center;}
      input:focus{border:0px solid #ffa500;}
table tr td{border-right:1px solid #080; border-bottom:1px solid #080;}
table{background: #fff none repeat scroll 0 0;
    border-left: 1px solid #080;
    border-top: 1px solid #080;}
    table tr:nth-child(even){background:#ccc;}
    table tr:nth-child(odd){background:#eee;}
	p{text-align: center;color: #808080;}
	
	#listOff {
  /*list-style-image: url("http://www.ibm.com/support/knowledgecenter/pt-br/SSMR4U_10.2.1/com.ibm.swg.ba.cognos.prfmdl_ug.10.2.0.doc/tm1_scorecrd_icon_traffic_excellent.jpg");
     
	list-style-image: url("http://www.lojapescaalternativa.com.br/skin/frontend/default/agenciasoft-pescaalternativa/images/circulo-verde-icone.png");
   
   
   list-style-image: url("https://i-msdn.sec.s-msft.com/dynimg/IC104896.gif");*/
   	list-style-image: url("http://www.bernstein.oeaw.ac.at/twiki/pub/TWiki/TWikiDocGraphics/led-red.gif");
   
   
	}
	#listOn{
		list-style-image: url("https://i-msdn.sec.s-msft.com/dynimg/IC104896.gif");
	
	
	}

	
	
.input {
border:0; 
padding:10px; 
font-size:1.3em; 
font-family:"Ubuntu Light","Ubuntu","Ubuntu Mono","Segoe Print","Segoe UI";
color:#ff5; 
border:solid 1px #ff5; 
margin:0 0 0px; 
width:100%;
-moz-box-shadow: inset 0 0 4px rgba(255,165,0,0); 
-webkit-box-shadow: inset 0 0 4px rgba(255, 165, 0, 0); 
box-shadow: inner 0 0 4px rgba(255, 165, 0, 0);
-webkit-border-radius: 3px; 
-moz-border-radius: 3px; 
border-radius: 3px;

}
input:focus { 
    outline: none !important;
    border:1px solid red;
    box-shadow: 0 0 10px #719ECE;
}

textarea:focus {
        outline: none !important;
    border:1px solid red;
    box-shadow: 0 0 10px #719ECE;
}	
	
	
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
	<meta http-equiv="refresh" content="20" >
  </head>

<body>
  <div style="position: absolute;border-style: inset;text-align: center;padding: 5px;width: 500px; margin: 0 auto;min-height: 300px;height: 500px;border-right-width: 10px;">
  <h1 style="font-family:verdana;"><i>   PLANILHA DE DADOS</i></h1>
   <div style="position: relative;margin: 0 auto;padding:2px;height: auto;width:100%">
  <form id="form1" name="form1 "action="/send" method="POST"  >
  	<table cellpadding="0"; cellspacing="0">
	<tr>
	 	
  		%for (i) in layoutx:
  			<td width="100"> <p  ><b > {{i}} </b></p> </td>
  		%end
  	</tr>
  	%c = len(layoutx)-1
	%flag = c
	%c = c * len(layouty)
	%count = 1  	
	%salt = flag
	
  	
  	
   %for (j) in layouty:
  		<tr>
		<td width="100"> <p ><b> {{j}} </b></p> </td>
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
  	
  	</form></div>
  	</div>
  	<!--<div style="position: relative;background-color: #000;height: 100%;width: 3px;left:600px;top:-400px;"></div>
  -->
	<div style="position:relative;;margin: 0 520px;border-style: groove;padding: 5px; width: 200px;min-height: 300px; height: 500px; border-color: #ccc">
		%for i in users:
			%name = i[0]
			%j = i[1]
			%if j == 2:
				<ul id="listOn"><li>Me</li></ul>
			%else:
			 	%if j == 1:
			 		<ul id="listOn"> 
						<li>Client{{name[16:]}}</li>			 	
			 		</ul>
				%elif j == 0:
					<ul id="listOff">
						<li>Client{{name[16:]}}</li>				
					</ul>
				
				%end
			%end
		%end		
	</div>
</body>

</html>
