
=====================================
Functional Tests: Dimep D-Sat Windows
=====================================

``dllsat.dll``
    DLL de comunicação com D-SAT. Versão do arquivo é 1.0.4.2, versão do
    produto é 1.0.0.0. Depende de ``zlib.dll``.
    
``zlib.dll``
    ZLib data compression library. Dependência direta de ``dllsat.dll``.
    Versão do arquivo 1.2.3.0. 
    Direitos autorais (C) 1995-2012 `Jean-loup Gaily <http://gailly.net/>`_ 
    e `Mark Adler <http://en.wikipedia.org/wiki/Mark_Adler>`_

.. warning::

    A ``dllsat.dll`` não é capaz de localizar a dependencia ``zlib.dll`` no
    mesmo diretório em que se encontra. O arquivo ``zlib.dll`` deverá ser
    copiado em ``%SYSTEMROOT%/System``.
