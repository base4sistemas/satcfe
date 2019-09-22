/*
 *  mockupsat.h
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
 */


#ifndef mockupsat_h__
#define mockupsat_h__


extern char *AssociarAssinatura(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *composicao_cnpj,
                    char    *assinatura);


extern char *AtualizarSoftwareSAT(
                    int     sessao,
                    char    *codigo_ativacao);


extern char *BloquearSAT(
                    int     sessao,
                    char    *codigo_ativacao);


extern char *CancelarUltimaVenda(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *chave_cfe,
                    char    *dados_cancelamento);


extern char *ComunicarCertificadoICPBRASIL(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *certificado);


extern char *ConfigurarInterfaceDeRede(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *dados_configuracao);


extern char *ConsultarNumeroSessao(
                    int     sessao,
                    char    *codigo_ativacao,
                    int     numero_sessao);


extern char *ConsultarSAT(int sessao);


extern char *ConsultarStatusOperacional(
                    int     sessao,
                    char    *codigo_ativacao);


extern char *DesbloquearSAT(
                    int     sessao,
                    char    *codigo_ativacao);


extern char *EnviarDadosVenda(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *dados_venda);


extern char *ExtrairLogs(
                    int     sessao,
                    char    *codigo_ativacao);


extern char *TesteFimAFim(
                    int     sessao,
                    char    *codigo_ativacao,
                    char    *dados_venda);


extern char *TrocarCodigoDeAtivacao(
                    int     sessao,
                    char    *codigo_ativacao,
                    int     opcao,
                    char    *novo_codigo,
                    char    *novo_codigo_confirmacao);


extern char *ConsultarUltimaSessaoFiscal(
                    int     sessao,
                    char    *codigo_ativacao);

#endif // mockupsat_h__
