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

  </head>

<body>

  <h1> PLANILHA 1</h1>
  <table cellpadding="0"; cellspacing="0">
    <tr>
  %for (n,m) in messages:
    <td width="100"><input type="text" value="{{n}}" /></td>
  %end
    </tr>
  </table>
  <table cellpadding="0"; cellspacing="0">
        <tr>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td width="60"><input type="text" /></td>
            <td width="60"><input type="text" /></td>
        </tr>
        <tr>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
        </tr>
        <tr>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
        </tr>
        <tr>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
            <td><input type="text" /></td>
        </tr>
    </table>
<ul>
%for (n, m) in messages:
    <li> <b>{{n}}: </b> {{m}} </li>
%end
</ul>

<form action="/send" method=POST>
    <p> Nick <input name="name" type="text" value="{{name}}"/> </p>
    <p> Mensagem <input name="message" type="text" /> </p>
    <p> <input value="Enviar" type="submit" /> </p>
</form>

</body>

</html>
