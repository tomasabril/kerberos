# kerberos
Kerberos implementation in python

Para a materia de Segurança e auditoria de Sistemas

Prof. Mauro Fonseca

UTFPR

http://dainf.ct.utfpr.edu.br/~maurofonseca/doku.php?id=cursos:if68e:kerberos


http://www.roguelynn.com/words/explain-like-im-5-kerberos/

---

Implementação de um sistema similar ao Kerberos.

O sistema deve:

    Usar tickets.
    Clientes pedem tickets a um serviço de autenticação.
    Tickets são usados para acessar os demais serviços da rede.
    Os tickets são cifrados (criptografia simétrica DES).
    Os tickets tem validade limitada, para aumentar sua segurança.
    Cada um dos atores deve ser um programa separado e rodar em terminais distintos.
        Cliente.
        Servidor AS.
        Servidor TGS.
        Servidor de serviços.

O funcionamento básico do sistema:

    O cliente se autentica junto ao AS
        M1 = [ID_C + {ID_S + T_R + N1}Kc]
    Obtém um ticket de acesso ao serviço de tickets TGS.
        M2 = [{K_c_tgs + N_1}Kc + T_c_tgs]
            Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs
    Solicita ao TGS um ticket de acesso ao serviço (servidor) desejado.
        M3 = [{ID_C + ID_S + T_R + N2 }K_c_tgs + T_c_tgs]
    Obtém um ticket de acesso ao serviço.
        M4 = [{K_c_s + N2}K_c_tgs + T_c_s]
            Onde T_c_s = {ID_C + T_A + K_c_s}K_s
    Com esse novo ticket, ele pode se autenticar junto ao servidor desejado e solicitar serviços.
        M5 = [{ID_C + T_A + S_R + N3}K_c_s + T_c_s]
    Recebe retorno do servidor desejado.
        M6 = [{Resposta, N3}K_c_s]

    ID_C = Identificador do cliente.
    ID_S = Identificador do serviço pretendido.
    T_R = Tempo solicitado pelo Cliente para ter acesso ao serviço.
    N1 = Número aleatório 1.
    Kc = Chave do cliente (Somente o cliente e o AS conhecem).
    T_c_tgs = Ticket fornecido para a comunicação cliente TGS.
    K_c_tgs = Chave de sessão entre cliente e TGS (Gerado no AS randomicamente)
    K_tgs = Chave do Servidor TGS (Somente o TGS e o AS conhecem).
    T_A = Tempo autorizado pelo TGS.
    K_s = Chave do Servidor de serviços (Somente o TGS e o servidor de serviços conhecem).
    S_R = Serviço Requisitado.
    K_c_s = Chave de sessão entre cliente e Servidor de serviço (Gerado no TGS randomicamente)
    N2 = Número aleatório 2.
    N3 = Número aleatório 3.

