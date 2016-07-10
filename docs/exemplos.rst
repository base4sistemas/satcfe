
.. _exemplos-documentos-xml:

Exemplos de Documentos
======================

Abaixo estão relacionados alguns exemplos de documentos XML.



.. _exemplos-xml-do-cfe-de-venda:

XML do CF-e de Venda
--------------------

O seguinte documento XML representa um CF-e de venda pronto para ser enviado ao
equipamento SAT. Um documento como este pode ser criado como visto em
:ref:`criando-um-cfe-de-venda` e submetido às funções SAT
:meth:`~satcfe.base.FuncoesSAT.enviar_dados_venda` e/ou
:meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`.

.. sourcecode:: xml

    <?xml version="1.0"?>
    <CFe>
      <infCFe versaoDadosEnt="0.06">
        <ide>
          <CNPJ>08427847000169</CNPJ>
          <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
          <numeroCaixa>002</numeroCaixa>
        </ide>
        <emit>
          <CNPJ>61099008000141</CNPJ>
          <IE>111111111111</IE>
          <IM>12345</IM>
          <cRegTribISSQN>3</cRegTribISSQN>
          <indRatISSQN>N</indRatISSQN>
        </emit>
        <dest>
          <CPF>11122233396</CPF>
          <xNome>Joao de Teste</xNome>
        </dest>
        <entrega>
          <xLgr>Rua Armando Gulim</xLgr>
          <nro>65</nro>
          <xBairro>Parque Gloria III</xBairro>
          <xMun>Catanduva</xMun>
          <UF>SP</UF>
        </entrega>
        <det nItem="1">
          <prod>
            <cProd>123456</cProd>
            <xProd>BORRACHA STAEDTLER pvc-free</xProd>
            <CFOP>5102</CFOP>
            <uCom>UN</uCom>
            <qCom>1.0000</qCom>
            <vUnCom>5.75</vUnCom>
            <indRegra>A</indRegra>
          </prod>
          <imposto>
            <ICMS>
              <ICMSSN102>
                <Orig>2</Orig>
                <CSOSN>500</CSOSN>
              </ICMSSN102>
            </ICMS>
            <PIS>
              <PISSN>
                <CST>49</CST>
              </PISSN>
            </PIS>
            <COFINS>
              <COFINSSN>
                <CST>49</CST>
              </COFINSSN>
            </COFINS>
          </imposto>
        </det>
        <total/>
        <pgto>
          <MP>
            <cMP>01</cMP>
            <vMP>10.00</vMP>
          </MP>
        </pgto>
      </infCFe>
    </CFe>


.. _exemplos-xml-do-cfe-sat-venda:

XML do CF-e-SAT de Venda
------------------------

O seguinte documento XML **seria um documento fiscal com validade jurídica** se
não tivesse sido **emitido contra um equipamento SAT para desenvolvimento** [#f1]_.
Repare que o emitente possui os dados do fabricante do equipamento além de
vários outros elementos importantes que foram adicionados pelo equipamento, tais
como o valor do troco e o bloco de assinatura no final do documento.

.. sourcecode:: xml

    <?xml version="1.0"?>
    <CFe>
      <infCFe Id="CFe35150761099008000141599000026310000100500297" versao="0.06" versaoDadosEnt="0.06" versaoSB="010100">
        <ide>
          <cUF>35</cUF>
          <cNF>050029</cNF>
          <mod>59</mod>
          <nserieSAT>900002631</nserieSAT>
          <nCFe>000010</nCFe>
          <dEmi>20150709</dEmi>
          <hEmi>172317</hEmi>
          <cDV>7</cDV>
          <tpAmb>2</tpAmb>
          <CNPJ>08427847000169</CNPJ>
          <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
          <assinaturaQRCODE>fMery4SK4Q69PiHNSRSwjMKloMUGA4D6+6cPERqpsuJlC1MmUnGWuZi2+zEURx46vEqgQIETlJGkWDIiKQcCoqpKtjxdDNJG6Z3ZDtuVML9j6APmapy+DK1fELW76XFrjMvDSL3IePRkOD64/Xx1irNdlbWjLa6swsz2O87Q+PNEPRIkJofmwr+GO4F+6Wyi0JMx+ZCfbSX8R6LZUQKCvfA5ogaJEpvFpAuMf9zoCa3P37tqLuleWz0YtLJB8YXwHHQ3jSkCTUDit0a1uteDnuTGqJ22GFb7IfULU6HatX3Fitxmc8jIjNp6bsPm7gx2pee8ZOoBgSUdEuJI2BCucA==</assinaturaQRCODE>
          <numeroCaixa>002</numeroCaixa>
        </ide>
        <emit>
          <CNPJ>61099008000141</CNPJ>
          <xNome>DIMAS DE MELO PIMENTA SISTEMAS DE PONTO E ACESSO LTDA</xNome>
          <xFant>DIMEP</xFant>
          <enderEmit>
            <xLgr>AVENIDA MOFARREJ</xLgr>
            <nro>840</nro>
            <xCpl>908</xCpl>
            <xBairro>VL. LEOPOLDINA</xBairro>
            <xMun>SAO PAULO</xMun>
            <CEP>05311000</CEP>
          </enderEmit>
          <IE>111111111111</IE>
          <IM>12345</IM>
          <cRegTrib>3</cRegTrib>
          <cRegTribISSQN>3</cRegTribISSQN>
          <indRatISSQN>N</indRatISSQN>
        </emit>
        <dest>
          <CPF>11122233396</CPF>
          <xNome>Joao de Teste</xNome>
        </dest>
        <entrega>
          <xLgr>Rua Armando Gulim</xLgr>
          <nro>65</nro>
          <xBairro>Parque Gloria III</xBairro>
          <xMun>Catanduva</xMun>
          <UF>SP</UF>
        </entrega>
        <det nItem="1">
          <prod>
            <cProd>123456</cProd>
            <xProd>BORRACHA STAEDTLER pvc-free</xProd>
            <CFOP>5102</CFOP>
            <uCom>UN</uCom>
            <qCom>1.0000</qCom>
            <vUnCom>5.75</vUnCom>
            <vProd>5.75</vProd>
            <indRegra>A</indRegra>
            <vItem>5.75</vItem>
          </prod>
          <imposto>
            <ICMS>
              <ICMSSN102>
                <Orig>2</Orig>
                <CSOSN>500</CSOSN>
              </ICMSSN102>
            </ICMS>
            <PIS>
              <PISSN>
                <CST>49</CST>
              </PISSN>
            </PIS>
            <COFINS>
              <COFINSSN>
                <CST>49</CST>
              </COFINSSN>
            </COFINS>
          </imposto>
        </det>
        <total>
          <ICMSTot>
            <vICMS>0.00</vICMS>
            <vProd>5.75</vProd>
            <vDesc>0.00</vDesc>
            <vPIS>0.00</vPIS>
            <vCOFINS>0.00</vCOFINS>
            <vPISST>0.00</vPISST>
            <vCOFINSST>0.00</vCOFINSST>
            <vOutro>0.00</vOutro>
          </ICMSTot>
          <vCFe>5.75</vCFe>
        </total>
        <pgto>
          <MP>
            <cMP>01</cMP>
            <vMP>10.00</vMP>
          </MP>
          <vTroco>4.25</vTroco>
        </pgto>
      </infCFe>
      <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
          <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
          <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
          <Reference URI="#CFe35150761099008000141599000026310000100500297">
            <Transforms>
              <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
              <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
            </Transforms>
            <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
            <DigestValue>ZaM4D/tOxLMGRqPpgDp5iDJyc9tFRIrty+UYGIGlTe4=</DigestValue>
          </Reference>
        </SignedInfo>
        <SignatureValue>JYCByJND++mEdkaCHBjLj+NLcwO1dVOlBV2awUzXndHIpfffouqQyWQJFpwGSdXtrPq1cjXg0cLdJKs//pdAQrb6FD74Hmj+/Zyuus2IVqw34qv69vvkRqM5cBUJgUzQz9IG1zOIs4d16zcblgbTwTVW1q+3qt2t9HwGc0nKY4tpITp8ihceY2Z4UKLie3K2/HnPq6B5L5aozQmDto/gCNQ1BJRF92RAwMlRepuciXN/HRUU73Bc1pu7HBUqE9pGpnKZfJ7SCAaKwQg9Q/ILguXBQ2qoVtA1qmJ9tSs65zCiLA7Mi+rIM5rRh3/ALay0vsPEpRI9vO+GIis9jSNjBg==</SignatureValue>
        <KeyInfo>
          <X509Data>
            <X509Certificate>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</X509Certificate>
          </X509Data>
        </KeyInfo>
      </Signature>
    </CFe>


.. _exemplos-xml-do-cfe-de-cancelamento:

XML do CF-e de Cancelamento
---------------------------

O seguinte documento XML representa um CF-e de cancelamento pronto para ser
enviado ao equipamento SAT. Um documento como este pode ser criado como visto
em :ref:`criando-um-cfe-de-cancelamento` e submetido à função SAT
:meth:`~satcfe.base.FuncoesSAT.cancelar_ultima_venda`.

.. sourcecode:: xml

    <CFeCanc>
      <infCFe chCanc="CFe35150761099008000141599000026310000100500297">
        <ide>
          <CNPJ>08427847000169</CNPJ>
          <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
          <numeroCaixa>002</numeroCaixa>
        </ide>
        <emit/>
        <dest/>
        <total/>
      </infCFe>
    </CFeCanc>


.. _exemplos-xml-do-cfe-sat-cancelamento:

XML do CF-e-SAT de Cancelamento
-------------------------------

O seguinte documento XML **seria um documento fiscal com validade jurídica** se
não tivesse sido **emitido contra um equipamento SAT para desenvolvimento**.
Repare que o equipamento SAT adiciona vários outros elementos ao documento
antes de assiná-lo e enviá-lo à SEFAZ.

.. sourcecode:: xml

    <?xml version="1.0"?>
    <CFeCanc>
      <infCFe
            Id="CFe35150908723218000186599000040190000378585470"
            chCanc="CFe35150908723218000186599000040190000360539948"
            versao="0.06">
        <dEmi>20150911</dEmi>
        <hEmi>175840</hEmi>
        <ide>
          <cUF>35</cUF>
          <cNF>858547</cNF>
          <mod>59</mod>
          <nserieSAT>900004019</nserieSAT>
          <nCFe>000037</nCFe>
          <dEmi>20150911</dEmi>
          <hEmi>175921</hEmi>
          <cDV>0</cDV>
          <CNPJ>16716114000172</CNPJ>
          <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
          <assinaturaQRCODE>UKJ77VyQ0tc+EdLm5ZdAYILMqXvPSSB+QLYz+0ZgJpUhNN5AchnYuArKPzVTiKqbObtxbR7l+s5X/TmMGMQw1TIryqv7A0Az73LagV+6oS5uk3yvBbYR+tWjfh+JcmktllYVZv8QVo+AY7ygj+lCqLjfUhMqBzU4HbJzBQMy7QPtCEy27wk7c3S3mVcsmWALxd3H7lHnZj1wJ+ldhWJpNX17o/6sB0Nc6ksz4dYkLRfHheCspFyTORtE1Any+DasmmaW8I4jNQfrWnxWbQxOJ3zqiE/pYb/wf/3r8WvC1luR5xdb9kMedd+TM0lZwZXndXkAcQOFVMq5CaYietV/og==</assinaturaQRCODE>
          <numeroCaixa>002</numeroCaixa>
        </ide>
        <emit>
          <CNPJ>08723218000186</CNPJ>
          <xNome>TANCA INFORMATICA EIRELI</xNome>
          <enderEmit>
            <xLgr>RUA ENGENHEIRO JORGE OLIVA</xLgr>
            <xBairro>VILA MASCOTE</xBairro>
            <xMun>SAO PAULO</xMun>
            <CEP>04362060</CEP>
          </enderEmit>
          <IE>149626224113</IE>
          <IM>123123</IM>
        </emit>
        <dest/>
        <total>
          <vCFe>2.00</vCFe>
        </total>
        <infAdic>
          <obsFisco xCampo="xCampo1">
            <xTexto>xTexto1</xTexto>
          </obsFisco>
        </infAdic>
      </infCFe>
      <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo>
          <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
          <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
          <Reference URI="#CFe35150908723218000186599000040190000378585470">
            <Transforms>
              <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
              <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
            </Transforms>
            <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
            <DigestValue>cKjiw47QNwzsTllPL2AqZa2q53472inwU8Uavl3sBQg=</DigestValue>
          </Reference>
        </SignedInfo>
        <SignatureValue>U59QqadjXTF6exMfRKF5WpppK61MB+7Eq4zdnxSeIZOw/nML2Z17F7VpvKmcPzqr2EU/z3ZkWYMSuKJOO4kb51QeoOYdwbycBMDsI8BwyreMeV4wGLhQ7IIIXcorPqmZ22ZpnuSwlT0m4lwjVpoMZERbXpc1Q4z+8O/eefKP5HUP1MZ6r8C2iHN1P/3ZT2JJhRGMvQ+OGlPz3RHPNAWuQ2MeKLk+/ZMNXfjSgaJnBt0TrNz0YSJlzXadNrrvuUEsP90uwWAtIgm8AfK8eWEU6FT7jvGbU0/Xa6zg4rbajtaV8mrzt8gmJc+8rUtrtcl//FPD/xbDiv3tSpefSTDz6w==</SignatureValue>
        <KeyInfo>
          <X509Data>
            <X509Certificate>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</X509Certificate>
          </X509Data>
        </KeyInfo>
      </Signature>
    </CFeCanc>

.. todo::

    O exemplo do XML do CF-e-SAT de cancelamento não está relacionado ao
    exemplo do CF-e de cancelamento pronto para ser submetido ao equipamento
    SAT. Talvez seja mais fácil compreender se os exemplos estiverem
    relacionados.

.. rubric:: Notas

.. [#f1] Também são chamados de "kit SAT".
