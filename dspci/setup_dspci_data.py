import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bm.settings.dev")
django.setup()

from datetime import date
from django.utils.text import slugify
from home.models import HomePage
from dspci.models import (
    DSPCIDocumentCategory,
    DSPCIDocument,
    DSPCIFaq,
    DSPCIIndexPage
)

print("Iniciando setup dos dados do DSPCI...")

# 1. Categorias
categories_data = [
    {
        "name": "Normas Técnicas (NT)",
        "slug": "normas-tecnicas",
        "icon": "bi-file-earmark-ruled",
        "description": "Conjunto de regulamentos técnicos que fixam as exigências de proteção contra incêndio e pânico para as edificações e áreas de risco na Paraíba.",
        "order": 1,
    },
    {
        "name": "Legislação",
        "slug": "legislacao",
        "icon": "bi-bank",
        "description": "Leis estaduais, decretos regulamentares e portarias que instituem as competências e normas do CBMPB.",
        "order": 2,
    },
    {
        "name": "Pareceres do CTD",
        "slug": "pareceres-ctd",
        "icon": "bi-mortarboard",
        "description": "Decisões e pareceres técnicos homologados pelo Conselho Técnico Deliberativo em recursos, consultas e casos omissos.",
        "order": 3,
    },
    {
        "name": "Resoluções Técnicas",
        "slug": "resolucoes-tecnicas",
        "icon": "bi-journal-bookmark",
        "description": "Atos normativos complementares para regulamentação de procedimentos específicos.",
        "order": 4,
    },
    {
        "name": "Formulários e Requerimentos",
        "slug": "formularios",
        "icon": "bi-clipboard-check",
        "description": "Modelos oficiais de requerimentos, declarações de responsabilidade e memoriais para download.",
        "order": 5,
    },
]

cat_map = {}
for cdata in categories_data:
    cat, created = DSPCIDocumentCategory.objects.get_or_create(
        slug=cdata["slug"],
        defaults=cdata
    )
    if not created:
        for k, v in cdata.items():
            setattr(cat, k, v)
        cat.save()
    cat_map[cdata["slug"]] = cat
    print(f"Categoria pronta: {cat.name}")

# 2. Documentos do Repositório
docs_data = [
    # Normas Técnicas
    {
        "code_number": "NT 01/2024",
        "title": "Procedimentos Administrativos e Processo de Segurança Contra Incêndio",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 1, 15),
        "summary": "Fixa as diretrizes e procedimentos para a tramitação, aprovação de projetos técnicos (PSCIP), concessão de AVCB, fiscalização e realização de vistorias técnicas no âmbito do Corpo de Bombeiros Militar da Paraíba através do Sistema Bravo.",
        "tags": "administrativo, pscip, vistoria, taxas, prazos, avcb, sistema bravo",
        "featured": True,
        "order": 1,
        "file_size_display": "2.8 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 02/2023",
        "title": "Terminologia e Simbologia de Proteção Contra Incêndio e Pânico",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 4, 10),
        "summary": "Padroniza os símbolos gráficos e termos técnicos adotados na elaboração de projetos de arquitetura e engenharia submetidos à análise do CBMPB.",
        "tags": "simbologia, terminologia, plantas, legendas, desenho tecnico",
        "featured": False,
        "order": 2,
        "file_size_display": "4.1 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 05/2024",
        "title": "Cargas de Incêndio nas Edificações e Áreas de Risco",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 2, 20),
        "summary": "Estabelece os valores e tabelas de carga de incêndio específica por uso e ocupação para dimensionamento das medidas de proteção ativa e passiva nas edificações.",
        "tags": "carga de incendio, risco, calculo, megajoule, ocupacao, comercial, industrial",
        "featured": True,
        "order": 3,
        "file_size_display": "1.9 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 15/2023",
        "title": "Sistemas de Hidrantes e de Mangotinhos para Combate a Incêndio",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 7, 5),
        "summary": "Fixa as condições mínimas exigíveis para dimensionamento, instalação e manutenção de sistemas de hidrantes e mangotinhos em edificações, incluindo reserva técnica e conjunto de bombas.",
        "tags": "hidrantes, mangotinhos, reserva de agua, bombas de incendio, tubulacao, vazao",
        "featured": True,
        "order": 4,
        "file_size_display": "3.5 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 17/2024",
        "title": "Brigada de Incêndio e Plano de Emergência",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 3, 1),
        "summary": "Estabelece as condições mínimas para formação, treinamento e reciclagem da brigada de incêndio, bem como o planejamento de simulações de abandono de local.",
        "tags": "brigada de incendio, plano de emergencia, simulado, brigadistas, evacuacao",
        "featured": False,
        "order": 5,
        "file_size_display": "1.7 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 22/2023",
        "title": "Proteção Contra Descargas Atmosféricas (SPDA)",
        "category": cat_map["normas-tecnicas"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 8, 18),
        "summary": "Regulamenta os requisitos de apresentação de laudos técnicos e inspeção de SPDA em conformidade com as normas ABNT NBR 5419.",
        "tags": "spda, para-raios, descargas atmosfericas, laudo tecnico, nbr 5419",
        "featured": False,
        "order": 6,
        "file_size_display": "2.2 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "NT 01/2012",
        "title": "Procedimentos Administrativos (Versão Anterior - Revogada)",
        "category": cat_map["normas-tecnicas"],
        "status": "REVOGADA",
        "year": 2012,
        "publication_date": date(2012, 5, 10),
        "summary": "Versão histórica de procedimentos administrativos do CBMPB, revogada e substituída pela NT 01/2024.",
        "tags": "revogada, historico, processo fisico",
        "featured": False,
        "order": 7,
        "file_size_display": "1.2 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },

    # Legislação
    {
        "code_number": "Lei nº 9.625/2011",
        "title": "Código Estadual de Proteção Contra Incêndio, Explosão e Controle de Pânico (CSCIP-PB)",
        "category": cat_map["legislacao"],
        "status": "ATUALIZADA",
        "year": 2011,
        "publication_date": date(2011, 12, 27),
        "summary": "Lei fundamental que institui o Código de Segurança Contra Incêndio do Estado da Paraíba, fixando o poder de polícia do CBMPB, multas, interdições e exigências legais para todo e qualquer imóvel comercial ou coletivo.",
        "tags": "codigo estadual, lei estadual, legislacao, poder de policia, multas, intervencao",
        "featured": True,
        "order": 1,
        "file_size_display": "5.6 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Lei nº 12.678/2023",
        "title": "Altera e Moderniza dispositivos da Lei nº 9.625/2011",
        "category": cat_map["legislacao"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 6, 14),
        "summary": "Atualização legislativa que desburocratiza procedimentos, amplia a tramitação digital de processos técnicos e aperfeiçoa as diretrizes de fiscalização preventiva.",
        "tags": "atualizacao, lei, modernizacao, cscip, desburocratizacao",
        "featured": True,
        "order": 2,
        "file_size_display": "850 KB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Decreto nº 33.614/2012",
        "title": "Regulamenta o Fundo Especial do CBMPB e Fixa Valores de Taxas de Fiscalização",
        "category": cat_map["legislacao"],
        "status": "EM_VIGOR",
        "year": 2012,
        "publication_date": date(2012, 1, 23),
        "summary": "Regulamenta as taxas de análise de projetos técnicos e de vistorias de segurança contra incêndio realizadas pelo CBMPB.",
        "tags": "decreto estadual, taxas, ufr-pb, vistoria, analise",
        "featured": False,
        "order": 3,
        "file_size_display": "1.1 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Portaria nº 008/2024 - GCG",
        "title": "Implantação dos Novos Protocolos Eletrônicos no Sistema Bravo",
        "category": cat_map["legislacao"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 2, 1),
        "summary": "Determina a obrigatoriedade da tramitação digital de processos de segurança contra incêndio em todas as seções do Estado via Sistema Bravo.",
        "tags": "portaria, comando geral, sistema bravo, protocolo digital",
        "featured": False,
        "order": 4,
        "file_size_display": "620 KB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },

    # Pareceres do CTD (Conselho Técnico Deliberativo)
    {
        "code_number": "Parecer CTD nº 003/2024",
        "title": "Compartimentação Horizontal e Barreiras Corta-Fogo em Galpões Logísticos de Grandes Vãos",
        "category": cat_map["pareceres-ctd"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 3, 12),
        "summary": "Deliberação do Conselho Técnico sobre critérios alternativos aceitáveis de compensação de segurança contra incêndio em galpões industriais e centros de distribuição que impossibilitem paredes corta-fogo tradicionais.",
        "tags": "ctd, conselho tecnico, galpoes, logistica, compartimentacao, grandes vaos",
        "featured": True,
        "order": 1,
        "file_size_display": "1.4 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Parecer CTD nº 011/2023",
        "title": "Instalação de Sistemas de Chuveiros Automáticos (Sprinklers) em Edificações Tombadas",
        "category": cat_map["pareceres-ctd"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 11, 28),
        "summary": "Fixa critérios harmônicos entre a proteção à vida e a preservação do patrimônio histórico cultural tombado pelo IPHAEP/IPHAN quanto ao caminhamento aparente de tubulações hidráulicas.",
        "tags": "ctd, conselho tecnico, patrimonio historico, iphaep, chuveiros automaticos, sprinklers",
        "featured": True,
        "order": 2,
        "file_size_display": "2.1 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Parecer CTD nº 007/2023",
        "title": "Dimensionamento de Saídas de Emergência em Edificações de Uso Misto com Galerias Comerciais",
        "category": cat_map["pareceres-ctd"],
        "status": "EM_VIGOR",
        "year": 2023,
        "publication_date": date(2023, 9, 15),
        "summary": "Análise técnica do cálculo da população simultânea e cálculo de largura de escadas pressurizadas em edifícios que congregam comércio térreo e escritórios superiores.",
        "tags": "ctd, conselho tecnico, rotas de fuga, saidas de emergencia, escadas pressurizadas, uso misto",
        "featured": False,
        "order": 3,
        "file_size_display": "1.3 MB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "Parecer CTD nº 002/2024",
        "title": "Rito Procedimental para Recursos Administrativos Contra Notificações de Vistoria",
        "category": cat_map["pareceres-ctd"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 2, 5),
        "summary": "Uniformiza o prazo e requisitos de admissibilidade de recursos impetrados por responsáveis técnicos perante o Conselho Técnico Deliberativo.",
        "tags": "ctd, conselho tecnico, recurso, prazo, admissibilidade, contraditorio",
        "featured": False,
        "order": 4,
        "file_size_display": "980 KB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },

    # Formulários e Modelos
    {
        "code_number": "REQ 01/2024",
        "title": "Requerimento Padrão para Análise de Recurso Técnico perante o CTD",
        "category": cat_map["formularios"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 1, 10),
        "summary": "Formulário padronizado a ser preenchido pelo Responsável Técnico (Engenheiro ou Arquiteto) ao protocolar recurso contra notificação ou parecer indeferitório.",
        "tags": "formulario, requerimento, recurso ctd, peticao",
        "featured": False,
        "order": 1,
        "file_size_display": "450 KB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
    {
        "code_number": "MEM 02/2024",
        "title": "Modelo de Memorial Descritivo de Medidas de Segurança Contra Incêndio",
        "category": cat_map["formularios"],
        "status": "EM_VIGOR",
        "year": 2024,
        "publication_date": date(2024, 1, 10),
        "summary": "Modelo editável em formato digital para elaboração do memorial de cálculo e dimensionamento de medidas de segurança em edificações de médio e grande porte.",
        "tags": "formulario, memorial descritivo, modelo, projeto tecnico, calculo",
        "featured": False,
        "order": 2,
        "file_size_display": "520 KB",
        "external_url": "https://bravo.bombeiros.pb.gov.br",
    },
]

for ddata in docs_data:
    doc, created = DSPCIDocument.objects.get_or_create(
        code_number=ddata["code_number"],
        defaults=ddata
    )
    if not created:
        for k, v in ddata.items():
            setattr(doc, k, v)
        doc.save()
    print(f"Documento pronto: {doc.code_number} - {doc.title}")

# 3. Perguntas Frequentes (FAQ)
faqs_data = [
    {
        "question": "O que é o AVCB e qual a sua importância legal?",
        "category": "AVCB",
        "answer": "<p>O <strong>Auto de Vistoria do Corpo de Bombeiros (AVCB)</strong> ou Certificado de Aprovação é o documento oficial que certifica que a edificação passou por vistoria técnica dos Bombeiros Militares e possui todas as medidas ativas e passivas de segurança contra incêndio e pânico exigidas pela Lei Estadual nº 9.625/2011. Ele é pré-requisito indispensável para concessão de alvarás de funcionamento municipais e apólices de seguro patrimonial.</p>",
        "order": 1,
    },
    {
        "question": "Qual o prazo de validade do AVCB emitido pelo CBMPB?",
        "category": "AVCB",
        "answer": "<p>Conforme as normas do CBMPB, a validade ordinária do Certificado de Aprovação (AVCB) na Paraíba é de <strong>1 (um) ano</strong> para a maioria das ocupações comerciais, industriais e de reunião de público, devendo ser renovado anualmente mediante nova solicitação de vistoria preventiva. Para determinadas ocupações de baixo potencial de risco, os prazos podem variar conforme regulamentação específica.</p>",
        "order": 2,
    },
    {
        "question": "Como dar entrada na análise de projeto técnico ou vistoria?",
        "category": "PROJETO",
        "answer": "<p>O processo é <strong>100% digital</strong> através do <strong>Sistema Bravo</strong> (<a href='https://bravo.bombeiros.pb.gov.br' target='_blank'>bravo.bombeiros.pb.gov.br</a>). O responsável técnico habilitado (Engenheiro ou Arquiteto) ou o proprietário realiza o cadastro, anexa as plantas em PDF com ART/RRT, gera a guia de taxa correspondente e acompanha o parecer dos analistas em tempo real pelo sistema.</p>",
        "order": 3,
    },
    {
        "question": "O que fazer caso o projeto receba notificação de exigência técnica?",
        "category": "PROJETO",
        "answer": "<p>O responsável técnico deve acessar o Sistema Bravo, ler atentamente o relatório circunstanciado emitido pelo militar analista com as referências às Normas Técnicas (NTs) aplicáveis, corrigir as pranchas ou memoriais descritivos e submeter uma reanálise diretamente no portal antes do esgotamento do prazo processual.</p>",
        "order": 4,
    },
    {
        "question": "O que é o Conselho Técnico Deliberativo (CTD) e quando posso submeter um recurso?",
        "category": "CTD",
        "answer": "<p>O <strong>Conselho Técnico Deliberativo (CTD)</strong> é o colegiado técnico superior do CBMPB, responsável por analisar divergências técnicas fundamentadas, julgar recursos administrativos contra notificações de vistorias ou indeferimentos de projetos e apreciar casos omissos ou inovadores de engenharia. O recurso deve ser interposto no prazo regulamentar via requerimento fundamentado acompanhado de ART/RRT no Sistema Bravo.</p>",
        "order": 5,
    },
]

for fdata in faqs_data:
    faq, created = DSPCIFaq.objects.get_or_create(
        question=fdata["question"],
        defaults=fdata
    )
    if not created:
        for k, v in fdata.items():
            setattr(faq, k, v)
        faq.save()
    print(f"FAQ pronto: {faq.question}")

# 4. Criar a DSPCIIndexPage sob a HomePage
home_page = HomePage.objects.first()
if home_page:
    dspci_page = DSPCIIndexPage.objects.filter(slug="dspci").first()
    if not dspci_page:
        dspci_page = DSPCIIndexPage(
            title="DSPCI - Diretoria de Segurança e Prevenção Contra Incêndio",
            slug="dspci",
            intro_subtitle="Diretoria de Segurança e Prevenção Contra Incêndio (antiga DAT)",
            intro_description="<p>A <strong>DSPCI</strong> do Corpo de Bombeiros Militar da Paraíba é o órgão diretivo responsável pela normatização, análise de projetos de engenharia, vistorias técnicas, credenciamento e emissão de AVCB em todo o território paraibano, salvaguardando vidas e patrimônios.</p>",
            sistema_bravo_url="https://bravo.bombeiros.pb.gov.br",
            consulta_avcb_url="https://bravo.bombeiros.pb.gov.br",
            solicitar_vistoria_url="https://bravo.bombeiros.pb.gov.br",
            whatsapp_atendimento="(83) 98795-3131",
            email_atendimento="dspci@bombeiros.pb.gov.br",
            endereco_atendimento="Rua Juvenal Mário da Silva, 981 – Manaíra, João Pessoa – PB, CEP 58038-511",
            horario_atendimento="Segunda a Sexta-feira, das 07h30 às 13h30",
            ctd_title="Conselho Técnico Deliberativo (CTD)",
            ctd_description="<p>O <strong>Conselho Técnico Deliberativo (CTD)</strong> é o órgão colegiado recursal e consultivo do CBMPB, composto por oficiais e engenheiros especialistas, com competência para dirimir dúvidas normativas, apreciar situações de inovação tecnológica e julgar recursos administrativos técnicos.</p>",
        )
        home_page.add_child(instance=dspci_page)
        dspci_page.save_revision().publish()
        print("DSPCIIndexPage criada e publicada com sucesso!")
    else:
        print("DSPCIIndexPage já existe.")

print("Setup do DSPCI concluído com sucesso!")
