/*
 * comm.h
 *
 *  Created on: Dec 18, 2012
 *      Author: marlus
 */

#ifndef COMM_H_
#define COMM_H_

//---------------------------------------------------------------------------

#define true  1
#define false 0

#define SIZE_BUFF_RX   20*1024

typedef struct {
        unsigned long  code;
        char   msg[300];
} COMM_ERROR;

#define bool unsigned char


#define TIMEOUT_CONSULTARSAT       1
#define TIMEOUT_STATUSOP           2
#define TIMEOUT_CONFREDE           20
#define TIMEOUT_BLOCK              5*60
#define TIMEOUT_ENVIARVENDA        6
#define TIMEOUT_CANCELARVENDA      4
#define TIMEOUT_EXTRAIR_LOGS       20
#define TIMEOUT_ATIVARSAT          5*60
#define TIMEOUT_TROCACOD           20
#define TIMEOUT_COMUNICAR_CERT     5*60
#define TIMEOUT_CONSULTAR_SESSAO   20
#define TIMEOUT_ATUALIZAR_SW       30*60
#define TIMEOUT_ASSOCIAR           20

enum  codes {
    __NOERROR__  =0,
    __NOCONNECT__=1,
    __READERROR__,
    __CHKERROR__,
    __CMDUNKERROR__,
    __TIMEOUT__  = 0x8000  ,
    __SEMCTS__
};


       /**
         * @name TrocarCodigoDeAtivacaoSAT
         * @brief O Aplicativo Comercial ou outro software fornecido pelo Fabricante
         * @brief poderá realizar a troca do código de ativação a qualquer momento
         * @param numeroSessao
         * @param CodigoAtivacao
         * @param opcao
         * @param novoCodigo
         * @param confNovoCodigo
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *  TrocarCodigoDeAtivacaoSAT(int nSessao,char *CodigoAtivacao,int opcao, char *novoCodigo, char * confNovoCodigo  ) ;
    /**
      * @name  ConfiguraTimeout
      * @brief Configura o tempo de timeuot de RX em segundos
      * @param timeout: timeout em milisegundos
      */
     void    ConfiguraTimeout (long timeout) ;
    /**
      * @name  ArquivoLog
      * @brief Configura o tempo de timeuot de RX em segundos
      * @param timeout: timeout em milisegundos
      */
     void  ArquivoLog (char *name) ;
    /**
      * @name  GeraNumeroessao
      * @brief Gera o numero de sessao para o AC
      *
      */

     int GeraNumeroSessao (void) ;
    /**
      * @name  LastTx
      * @brief Busca a ultima linha de log de TX
      *
      */
     char * LastTx(void) ;
    /**
      * @name  LastRx
      * @brief Busca a ultima linha de log de RX
      *
      */
     char * LastRx(void) ;
    /**
      * @name  CloseSerial
      * @brief Fecha a porta serial
      *
      */
     void    CloseSerial(void);
      /**
       * @name AtivarSAT
       * @brief Metodo para ativar o uso do SAT
       * @param subComando
       * @param codigoDeAtivacao
       * @param CNPJ
       * @param cUF
       * @return CSR
       */
      char *  AtivarSAT(int nSessao,int subComando, char *codigoDeAtivacao, char *CNPJ, int cUF);
    /**
      * @name   CodigoErro
      * @brief  Retorna a ultima situação de erro na comunicacao
      * @return COMM_ERROR
      */
     COMM_ERROR  CodigoErro (void);
     /**
       * @name  ComunicarCertificadoICPBRASIL
       * @brief Comunica o certificado icp Brasil
       * @param numeroSessao
       * @param codigoDeAtivacao
       * @param Certificado
       * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
       **/
     char *   ComunicarCertificadoICPBRASIL (int nSessao,char *codigoDeAtivacao, char *Certificado) ;
     /**
       * @name EnviaDadosVenda
       * @brief Responsavel pelo comando de envio de dados de vendas
       * @param codigoDeAtivacao
       * @param numeroSessao
       * @param dadosVenda
       * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
       */
     char *  EnviarDadosVenda(int nSessao,char *codigoDeAtivacao,char *dadosVenda);

        /**
         * @name CanclearUltimaVenda
         * @brief cancela o ultimo cupom fiscal
         * @param codigoDeAtivacao
         * @param chave
         * @param dadosCancelamento
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
    char *  CancelarUltimaVenda(int nSessao,char *codigoDeAtivacao,  char *chave, char *dadosCancelamento);
    /**
      * @name AbreSerialSAT
      * @brief Configura os parametros de comunicacao da porta serial apontada por commPort
      * @param commPort - Porta Serial 0 COM1 , 1 COM2, ....
      * @param baud : baudrate
      * @param nBits: Numero de stop bits
      * @param paridade: Paridade 0-Sem paridade, 1-Paridade par, 2- Impar
      * @param nStops
      * @return int error
      */
     int   AbreSerialSAT (const char * commPort, int baud, int nBits, int paridade, int nStops) ;
      /**
        * @name ConsultarSAT
        * @brief consultar SAT
        * @param numeroSessao
        * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
        */
      char * ConsultarSAT (int sessao) ;

       /**
         *  @name TesteFimAFim
         *  @brief Esta função consiste em um teste de comunicação entre o AC, o Equipamento SAT e a SEFAZ
         *  @param numeroSessao
         *  @param codigoAtivacao
         *  @param dadosVenda
         *  @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
    char *  TesteFimAFim(int nSessao,char *codigoDeAtivacao, char *dadosVenda) ;


       /**
         *  @name  ConsultarStatusOperacional
         *  @brief Essa função é responsável por verificar a situação de funcionamento do Equipamento SAT
         *  @param numeroSessao
         *  @param codigoAtivacao
         *  @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         *
         */
     char *   ConsultarStatusOperacional(int nSessao,char *codigoDeAtivacao) ;
       /**
         * @name ConsultarNumeroSessao
         * @brief O AC poderá verificar se a última sessão requisitada foi processada em caso de não
         * @brief recebimento do retorno da operação. O equipamento SAT-CF-e retornará exatamente o resultado da
         * @brief sessão consultada
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *  ConsultarNumeroSessao(int nSessao,char *CodAtivacao,int numeroSessao) ;
       /**
         * @name  ConfigurarInterfaceDeRede
         * @brief Responsavel pela configuracao da interface de rede do SAT (Ver espec:2.6.10)
         * @param numeroSessao
         * @param codigoDeAtivacao
         * @param dadosVenda
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *  ConfigurarInterfaceDeRede (int nSessao,char *codigoDeAtivacao, char *DadosConfiguracao) ;
       /**
         * @name AssociarAssinatura
         * @brief Responsavel pelo comando de associar o AC ao SAT
         * @param numeroSessao
         * @param CodigoAtivacao
         * @param CNPJ
         * @param assinaturaCNPJs
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *   AssociarAssinatura(int nSessao,char *codativacao,char *CNPJvalue, char *assinaturaCNPJs) ;
       /**
         * @name AtualizarSoftwateSAT
         * @brief O Contribuinte utilizará a função AtualizarSoftwareSAT para a atualização imediata do
         * @brief software básico do Equipamento SAT
         * @param numeroSessao
         * @param codigoAtivacao
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char * AtualizarSoftwareSAT(int nSessao,char *CodigoAtivacao) ;

       /**
         * @name ExtrairLogs
         * @brief O Aplicativo Comercial poderá extrair os arquivos de registro do
         * @brief Equipamento SAT por meio da função ExtrairLogs
         * @param numeroSessao
         * @param codigoAtivacao
         * @return  pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *  ExtrairLogs(int nSessao,char *CodigoAtivacao) ;
       /**
         * @name BloquearSAT
         * @brief O Aplicativo Comercial ou outro software fornecido pelo Fabricante poderá
         * @brief realizar o bloqueio operacional do Equipamento SAT
         * @return  pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char *  BloquearSAT(int nSessao,char *CodigoAtivacao);
       /**
         * @name DesbloquearSAT
         * @brief O Aplicativo Comercial ou outro software fornecido pelo
         * @brief Fabricante poderá realizar o desbloqueio operacional do Equipamento SAT
         * @param numeroSessao
         * @param codigoAtivacao
         * @return pointer para area com retorno do comando enviado pelo dispositivo SAT
         */
     char * DesbloquearSAT(int nSessao,char *CodigoAtivacao) ;
       /**
         * @name SetaArquivoLog
         * @brief define o arquivo de log de comunica�ao
         * @param srFile nome do arquivo de logs
         * @return
         */

     void   SetaArquivoLog(char *strFile);



#endif /* COMM_H_ */
