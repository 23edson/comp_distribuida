t1-part1 ok (BUG no nick arrumado) - Para testar, basta rodar chat.py;


t1-part2 ok (Comunicação de diferentes servidores) -
	 Para testar, é preciso inicializar n instâncias de chat.py. Deste
	 modo, inicializando o arquivo via linha de comando seguindo o padrão:
	 python3 chat.py [porta_do_servidor] [porta_servidor_conhecido_1]
	 	 	 [porta_servidor_conhecido_2] []...

    	Exemplo: server 1 :python chat.py 8080 8081
		 server 2 : python chat.py 8081 8080 8082
		 server 3 : python chat.py 8082 8081

	Após isto, basta rodar no browser a url de cada servidor.

	Exemplo : Aba 1: http://localhost:8080;
		  Aba 2: http://localhost:8081;
		  Aba 3: http://localhost:8082;


	Nesta parte do trabalho foi incorporado os seguintes métodos:
	      - GET /peers - Retorna a lista de servidores conhecidos; 
	      - GET /msgs - Retorna a lista de mensagens;

t2 - ok (dht)

   Para testar, é preciso iniciar instâncias de dht.py; passando como
   parâmetro na linha de comando: o número da porta utilizada;
   Posteriormente é necessário iniciar o cliente para um servidor específico; passando como argumento a porta deste cliente, e as portas de seus vizinhos.
   ex: dht.py 8080
       dht.py 8081
       dht.py 8082
       client.py 8081 8080 8082 (client para o servidor 8081, conhece 8080 e 8082)

       Métodos incorporados:
       	       - GET /dht/lookup/<key> - Retorna a busca por um chave localmente;
	       - GET /dht/lookup_dist/<key> - Retorna a busca por uma chave distribuída(Retorna o nodo a quem esta chave esta associada)
	       - PUT /dht/<key>/<value> - Tenta inserir o valor associado com a chave na tabela, caso houver alguma colisão, o mesmo é encaminhado para o nodo a qual houve a colisão; 