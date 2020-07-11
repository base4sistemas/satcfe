/*
 *  mockupsat.c
 *  Mockup da biblioteca SAT (SAT-CF-e)
 *
 *  Copyright 2015 Base4 Sistemas Ltda ME
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  ----
 *
 *  Compilação (position-independent code, PIC):
 *
 *      $ gcc -c -Wall -Werror -fpic mockupsat.c
 *      $ gcc -shared -o libmockupsat.so mockupsat.o
 *
 *  Este código resulta em strings que podem ser decodificadas como UTF-8,
 *  embora não seja o meio mais recomendado de lidar com esse assunto, serve
 *  para este mockup simples, por enquanto.
 *
 *  Um script Python pode decodificar a string assim:
 *
 *      >>> import ctypes
 *      >>> from ctypes import c_int, c_char_p
 *      >>> lib = ctypes.CDLL('./libmockupsat.so')
 *      >>> func = lib.ConsultarSAT
 *      >>> func.argtypes = [c_int,]
 *      >>> func.restype = c_char_p
 *      >>> resposta = func(123456)
 *      >>> print resposta.decode('utf-8')
 *      u'123456|08000|SAT em operação||'
 *
 */

#include <stdio.h>
#include <string.h>
#include <time.h>


#define RESPOSTA_ATIVARSAT \
            "%d|04000|Ativado corretamente|||" \
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQm5UQ0NBUVl" \
            "DQVFBd1hURUxNQWtHQTFVRUJoTUNVMGN4RVRBUEJnTlZCQW9UQ0UweVEzSjVjSF" \
            "J2TVJJdwpFQVlEVlFRREV3bHNiMk5oYkdodmMzUXhKekFsQmdrcWhraUc5dzBCQ" \
            "1FFV0dHRmtiV2x1UUhObGNuWmxjaTVsCmVHRnRjR3hsTG1SdmJUQ0JuekFOQmdr" \
            "cWhraUc5dzBCQVFFRkFBT0JqUUF3Z1lrQ2dZRUFyMW5ZWTFRcmxsMXIKdUIvRnF" \
            "sQ1JycjVudnVwZElOKzN3RjdxOTE1dHZFUW9jNzRibnU2YjhJYmJHUk1oemR6bX" \
            "ZRNFN6RmZWRUF1TQpNdVRIZXliUHE1dGg3WURyVE5pektLeE9CbnFFMktZdVg5W" \
            "DIyQTFLaDQ5c29KSkZnNmtQYjlNVWdpWkJpTWx2CnRiN0szQ0hmZ3c1V2FnV25M" \
            "bDhMYitjY3ZLWlpsKzhDQXdFQUFhQUFNQTBHQ1NxR1NJYjNEUUVCQkFVQUE0R0I" \
            "KQUhwb1JwNVlTNTVDWnB5K3dkaWdRRXdqTC93U2x1dm8rV2p0cHZQMFlvQk1KdT" \
            "RWTUtlWmk0MDVSN284b0V3aQpQZGxycmxpS05rbkZtSEtJYUNLVExSY1U1OVNjQ" \
            "TZBREVJV1V6cW1VelA1Q3M2anJTUm8zTktmZzFiZDA5RDFLCjlyc1FrUmM5VXJ2" \
            "OW1SQklzcmVkR25ZRUNOZVJhSzVSMXl6cE9vd25pblhDCi0tLS0tRU5EIENFUlR" \
            "JRklDQVRFIFJFUVVFU1QtLS0tLQ=="


/* "cupom cancelado com sucesso"... "cupom"? */
#define RESPOSTA_CANCELARULTIMAVENDA  \
            "%d|07000|0000|"\
            "Cupom cancelado com sucesso + conte" "\xc3\xba" "do "\
                    "CF-e-SAT cancelado|"\
            "%s|%s|%s|"\
            "%04d%02d%02d%02d%02d%02d|%s|%s|%s|%s"


#define RESPOSTA_ENVIARDADOSVENDA  \
            "%d|06000|0000|"\
            "Emitido com sucesso + conte" "\xc3\xba" "do notas|"\
            "%s|%s|%s|"\
            "%04d%02d%02d%02d%02d%02d|%s|%s|%s|%s"\


#define RESPOSTA_TESTEFIMAFIM  \
            "%d|09000|Emitido com sucesso|"\
            "%s|%s|%s|"\
            "%04d%02d%02d%02d%02d%02d|%s|%s"


/**
 *  Conforme a "Tabela de Informações do Status do SAT",
 *  Item 6.1.7.2, da ER.
 */
#define STATUS_SAT  \
            "000000000|"\
            "DHCP|"\
            "000.000.000.000|"\
            "00:00:00:00:00:00|"\
            "255.255.255.000|"\
            "000.000.000.000|"\
            "000.000.000.000|"\
            "000.000.000.000|"\
            "CONECTADO|"\
            "ALTO|"\
            "1 GBYTE|"\
            "0 BYTES|"\
            "20150701000000|"\
            "00.00.00|"\
            "00.00|"\
            "35000000000000000000590000000000000000000001|"\
            "35000000000000000000590000000000000000000001|"\
            "35000000000000000000590000000000000000000001|"\
            "20150401000000|"\
            "20150401000000|"\
            "20150101|"\
            "20501231|"\
            "0"


/**
 *  Resulta em uma resposta padrão no formato:
 *
 *      "numeroSessao|EEEEE|mensagem|cod|mensagemSEFAZ"
 */
char *_resposta_padrao(int sessao, int eeeee, char *mensagem)
{
    static char resp[256];
    sprintf(resp, "%d|%05d|%s||", sessao, eeeee, mensagem);
    return resp;
}


char *AtivarSAT(
            int     sessao,
            int     tipo_certificado,
            char    *codigo_ativacao,
            char    *contribuinte_cnpj,
            int     codigo_uf)
{
      static char resp[892];
      sprintf(resp, RESPOSTA_ATIVARSAT, sessao);
      return resp;
}


char *AssociarAssinatura(
            int     sessao,
            char    *codigo_ativacao,
            char    *composicao_cnpj,
            char    *assinatura)
{
    static char resp[256];
    int eeeee = 13000;
    int cccc = 0000;
    char *mensagem = "Assinatura do AC registrada";
    char *cod = "";
    char *mensagem_sefaz = "";

    sprintf(
                resp,
                "%d|%05d|%04d|%s|%s|%s",
                sessao,
                eeeee,
                cccc,
                mensagem,
                cod,
                mensagem_sefaz
        );

    return resp;
}


char *AtualizarSoftwareSAT(
            int     sessao,
            char    *codigo_ativacao)
{
    return _resposta_padrao(sessao, 14000, "Software atualizado com sucesso");
}


char *BloquearSAT(
            int     sessao,
            char    *codigo_ativacao)
{
    return _resposta_padrao(sessao, 16000,
                "Equipamento SAT bloqueado com sucesso");
}


char *CancelarUltimaVenda(
            int     sessao,
            char    *codigo_ativacao,
            char    *chave_cfe,
            char    *dados_cancelamento)
{
    char *cod = "";
    char *mensagem_sefaz = "";
    char *conteudo_cfe = "<CFeCanc>...</CFeCanc>";
    char *chave_consulta = "CFe12345678901234567890123456789012345678901234";
    char *valor_total_cfe = "4.73";
    char *cpf_cnpj = "11122233396";
    char *qrcode = "RGFkb3MgUVJDb2Rl";

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);

    static char resp[512];
    sprintf(
                resp,
                RESPOSTA_CANCELARULTIMAVENDA,
                sessao,
                cod,
                mensagem_sefaz,
                conteudo_cfe,
                tm.tm_year + 1900,
                tm.tm_mon + 1,
                tm.tm_mday,
                tm.tm_hour,
                tm.tm_min,
                tm.tm_sec,
                chave_consulta,
                valor_total_cfe,
                cpf_cnpj,
                qrcode
        );
    return resp;
}


char *ComunicarCertificadoICPBRASIL(
            int     sessao,
            char    *codigo_ativacao,
            char    *certificado)
{
    return _resposta_padrao(sessao, 5000,
                "Certificado transmitido com sucesso");
}


char *ConfigurarInterfaceDeRede(
            int     sessao,
            char    *codigo_ativacao,
            char    *dados_configuracao)
{
    return _resposta_padrao(sessao, 12000, "Rede configurada com sucesso");
}


char *ConsultarNumeroSessao(
            int     sessao,
            char    *codigo_ativacao,
            int     numero_sessao)
{
    /*
        (!) Se comporta como se a sessão informada não
            fosse conhecida pelo equipamento SAT.
    */
    return _resposta_padrao(sessao, 11003, "Sess\xc3\xa3o n\xc3\xa3o existe");
}


char *ConsultarSAT(int sessao)
{
    return _resposta_padrao(sessao, 8000, "SAT em Opera\xc3\xa7\xc3\xa3o");
}


char *ConsultarStatusOperacional(
            int     sessao,
            char    *codigo_ativacao)
{
    static char resp[512];

    int eeeee = 10000;
    char *mensagem = "Resposta com sucesso";
    char *cod = "";
    char *mensagem_sefaz = "";

    sprintf(resp,
            "%d|%05d|%s|%s|%s|%s",
            sessao,
            eeeee,
            mensagem,
            cod,
            mensagem_sefaz,
            STATUS_SAT);

    return resp;
}


char *DesbloquearSAT(
            int     sessao,
            char    *codigo_ativacao)
{
    return _resposta_padrao(sessao, 17000,
                "Equipamento SAT desbloqueado com sucesso");
}


char *EnviarDadosVenda(
            int     sessao,
            char    *codigo_ativacao,
            char    *dados_venda)
{
    char *cod = "";
    char *mensagem_sefaz = "";
    char *conteudo_cfe = "<CFe>...</CFe>";
    char *chave_consulta = "CFe35000000000000000000590000000000000000000001";
    char *valor_total_cfe = "4.73";
    char *cpf_cnpj_value = "00000000000000";
    char *assinatura_qrcode = "Z5nVOlWc...3RIw==";

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);

    static char resp[512];
    sprintf(
                resp,
                RESPOSTA_ENVIARDADOSVENDA,
                sessao,
                cod,
                mensagem_sefaz,
                conteudo_cfe,
                tm.tm_year + 1900,
                tm.tm_mon + 1,
                tm.tm_mday,
                tm.tm_hour,
                tm.tm_min,
                tm.tm_sec,
                chave_consulta,
                valor_total_cfe,
                cpf_cnpj_value,
                assinatura_qrcode
        );
    return resp;
}


char *ExtrairLogs(
            int     sessao,
            char    *codigo_ativacao)
{
    int eeeee = 15000;
    char *mensagem = "Transfer\xc3\xaancia completa";
    char *cod = "";
    char *mensagem_sefaz = "";
    char *arquivo_log = \
            "MjAxOTA2MjAxMjUyMDF8U0FULVNFRkFafGVycm98RXJybyBhbyB0cmFuc21pd"\
            "GlyIGxvdGUgcGFyYSBhIFNFRkFaCjIwMTkwNjIwMTI1MjEwfEFDLVNBVHxpbm"\
            "ZvfFJlY2ViaWRhIG1lbnNhZ2VtIHJlZmVyZW50ZSBmdW7Dp8OjbyBUZXN0ZUZ"\
            "pbUFGaW0KMjAxOTA2MjAxMjUyMTh8U0FUfGVycm98RXJybyBhbyBnZXJhciBj"\
            "ZXJ0aWZpY2Fkbw==";

    static char resp[256];
    sprintf(
                resp,
                "%d|%05d|%s|%s|%s|%s",
                sessao,
                eeeee,
                mensagem,
                cod,
                mensagem_sefaz,
                arquivo_log
        );

    return resp;
}


char *TesteFimAFim(
            int     sessao,
            char    *codigo_ativacao,
            char    *dados_venda)
{
    char *cod = "";
    char *mensagem_sefaz = "";
    char *conteudo_cfe = "<CFe>...</CFe>";
    char *num_doc_fiscal = "000001";
    char *chave_consulta = "CFe12345678901234567890123456789012345678901234";

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);

    static char resp[512];
    sprintf(
                resp,
                RESPOSTA_TESTEFIMAFIM,
                sessao,
                cod,
                mensagem_sefaz,
                conteudo_cfe,
                tm.tm_year + 1900,
                tm.tm_mon + 1,
                tm.tm_mday,
                tm.tm_hour,
                tm.tm_min,
                tm.tm_sec,
                num_doc_fiscal,
                chave_consulta
        );
    return resp;
}


char *TrocarCodigoDeAtivacao(
            int     sessao,
            char    *codigo_ativacao,
            int     opcao,
            char    *novo_codigo,
            char    *novo_codigo_confirmacao)
{
    char *mensagem = "C" "\xc3\xb3" "digo de "
                     "ativa" "\xc3\xa7\xc3\xa3" "o alterado com sucesso";
    return _resposta_padrao(sessao, 18000, mensagem);
}


char *ConsultarUltimaSessaoFiscal(
            int     sessao,
            char    *codigo_ativacao)
{
    // sempre indica que não existe sessão fiscal (EEEEE 19003).
    char *mensagem = "N\xc3\xa3o existe sess\xc3\xa3o fiscal";
    return _resposta_padrao(sessao, 19003, mensagem);
}
