
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
:ref:`funcao-enviardadosvenda` ou :ref:`funcao-testefimafim`.

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
não tivesse sido emitido contra um equipamento SAT para desenvolvimento [#f1]_.
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


.. rubric:: Nota

.. [#f1] Também são chamados de "kit SAT".
