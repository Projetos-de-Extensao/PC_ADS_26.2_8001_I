# Documento de Visão (v1.0)
## Portal Cidadão Seguro
### Projeto de Cloud - Fase de Inception

---

### 1. Introdução

Este documento descreve as necessidades de negócio, restrições e requisitos de infraestrutura da plataforma Portal Cidadão Seguro, além de orientar o planejamento arquitetural da solução na nuvem AWS.

O Portal Cidadão Seguro é uma plataforma GovTech destinada à disponibilização de serviços públicos digitais, com foco na segurança, disponibilidade, escalabilidade e auditabilidade das informações tratadas pela solução.

#### 1.1. Propósito

Definir a visão de escopo e arquitetura lógica e física para a implantação da plataforma **Portal Cidadão Seguro** na infraestrutura de nuvem AWS, contemplando os requisitos de segurança, disponibilidade, escalabilidade, monitoramento, auditoria e proteção dos dados tratados pela plataforma.

#### 1.2. Escopo

O escopo deste projeto de cloud engloba os seguintes componentes e serviços AWS:

1. **Portal Cidadão Seguro:** plataforma destinada à disponibilização de serviços públicos digitais aos cidadãos.

2. **Módulo de Zeladoria Urbana:** serviço do Portal destinado ao registro e acompanhamento de solicitações relacionadas à manutenção e infraestrutura urbana, inspirado no conceito de centrais de atendimento e zeladoria como o 1746.

3. **Infraestrutura de Rede e Segurança:** isolamento lógico dos recursos por meio de Amazon VPC, sub-redes públicas e privadas, Security Groups, NACLs e gerenciamento de acesso via IAM.

4. **Computação:** execução dos serviços da aplicação por meio de Amazon EC2 / ECS.

5. **Persistência de Dados:** armazenamento das informações estruturadas da plataforma por meio do Amazon RDS.

6. **Armazenamento de Arquivos:** utilização do Amazon S3 para armazenamento de imagens, documentos e outros arquivos enviados pelos usuários.

7. **Monitoramento e Auditoria:** utilização do Amazon CloudWatch para monitoramento e centralização de logs e do AWS CloudTrail para registro das atividades realizadas no ambiente.

8. **Criptografia e Proteção de Dados:** utilização do AWS KMS e dos mecanismos de criptografia da AWS para proteção dos dados em trânsito e em repouso.

9. **Disponibilidade e Escalabilidade:** utilização de mecanismos de alta disponibilidade, múltiplas Availability Zones e dimensionamento dos recursos conforme a demanda.

10. **Continuidade de Negócio:** utilização de mecanismos de backup e recuperação compatíveis com os objetivos de RPO e RTO definidos para a solução.

#### 1.3. Definições, Acrônimos e Abreviações

* **API:** Application Programming Interface
* **AWS:** Amazon Web Services
* **VPC:** Virtual Private Cloud (Rede Virtual Privada)
* **RDS:** Relational Database Service (Banco de Dados Relacional Gerenciado)
* **S3:** Simple Storage Service (Serviço de Armazenamento de Objetos)
* **IAM:** Identity and Access Management (Gerenciamento de Identidades e Acessos)
* **NACL:** Network Access Control List (Lista de Controle de Acesso à Rede)
* **SLA:** Service Level Agreement (Acordo de Nível de Serviço)
* **RPO:** Recovery Point Objective (Objetivo de Ponto de Recuperação)
* **RTO:** Recovery Time Objective (Objetivo de Tempo de Recuperação)
* **LGPD:** Lei Geral de Proteção de Dados

---

### 2. Posicionamento

#### 2.1. Oportunidade de Negócio

A digitalização dos serviços públicos cria a necessidade de plataformas capazes de disponibilizar serviços à população de forma acessível, segura e confiável.

O Portal Cidadão Seguro propõe uma infraestrutura em nuvem capaz de suportar serviços públicos digitais, oferecendo uma base arquitetural que permita a evolução da plataforma conforme o aumento da quantidade de usuários e serviços disponibilizados.

Como aplicação inicial, o projeto contará com o módulo de **Zeladoria Urbana**, permitindo que cidadãos registrem problemas encontrados no espaço público e acompanhem o andamento das solicitações.

#### 2.2. Descrição do Problema

| **O problema de...** | A necessidade de disponibilizar serviços públicos digitais capazes de receber, armazenar e processar informações dos cidadãos com segurança e disponibilidade. |
|---|---|
| **Afeta...** | Cidadãos, servidores públicos, gestores e equipes responsáveis pela operação e manutenção da plataforma. |
| **Cujo impacto é...** | Dificuldade de acesso aos serviços públicos, indisponibilidade dos sistemas, acessos indevidos, perda de rastreabilidade das operações e riscos relacionados ao tratamento inadequado de dados pessoais. |
| **Uma solução bem-sucedida incluiria...** | Uma plataforma GovTech hospedada em uma infraestrutura AWS segura, escalável e auditável, oferecendo serviços digitais aos cidadãos, inicialmente com um módulo de solicitação e acompanhamento de serviços de zeladoria urbana. |

#### 2.3. Posicionamento do Produto

Para cidadãos que necessitam utilizar serviços públicos digitais, o **Portal Cidadão Seguro** é uma plataforma GovTech que centraliza serviços públicos digitais em uma infraestrutura segura e escalável na AWS.

O módulo inicial de **Zeladoria Urbana** permitirá o registro, consulta, atualização, cancelamento e acompanhamento de solicitações relacionadas a problemas de manutenção e infraestrutura urbana.

Diferentemente de soluções isoladas ou sistemas legados, o Portal Cidadão Seguro será sustentado por uma arquitetura em nuvem que prioriza segurança, disponibilidade, escalabilidade, monitoramento e auditabilidade.

---

### 3. Descrição dos Stakeholders e Usuários

| **Stakeholder (Perfil)** | **Necessidade Primária** | **Expectativa na Nuvem (AWS)** |
|---|---|---|
| **Cidadãos** | Utilizar os serviços públicos digitais e realizar solicitações de zeladoria urbana | Plataforma disponível e responsiva para criação, consulta, atualização e acompanhamento das solicitações |
| **Servidores Públicos** | Analisar solicitações, assumir atendimentos e atualizar o status das solicitações | Acesso confiável às solicitações e aos dados necessários para o atendimento |
| **Gestores Públicos** | Acompanhar indicadores de utilização, disponibilidade e segurança da plataforma | Informações consolidadas sobre o funcionamento da plataforma e seus serviços |
| **Equipe de TI** | Administrar a infraestrutura, acessos, monitoramento e manutenção dos recursos AWS | Infraestrutura disponível, monitorada e administrável |
| **Profissionais de Segurança da Informação** | Garantir a proteção dos recursos e dados da plataforma | Controle de acesso, criptografia, monitoramento e auditoria dos recursos |
| **Responsáveis por Governança e Compliance** | Garantir conformidade com políticas internas e requisitos de proteção de dados | Rastreabilidade das operações e informações necessárias para auditorias e conformidade com a LGPD |

---

### 4. Visão Geral do Produto/Solução

#### 4.1. Perspectiva do Produto

O Portal Cidadão Seguro operará como uma plataforma GovTech hospedada na infraestrutura de nuvem AWS.

A aplicação disponibilizará serviços públicos digitais por meio de uma interface acessível aos cidadãos. O primeiro serviço implementado será o módulo de **Zeladoria Urbana**, responsável pelo gerenciamento das solicitações de problemas relacionados à infraestrutura e manutenção urbana.

A aplicação será executada nos recursos de computação definidos pela arquitetura AWS e utilizará serviços gerenciados para persistência de dados, armazenamento de arquivos, segurança, monitoramento e auditoria.

#### 4.2. Módulos Principais

* **Portal:** reúne os serviços digitais destinados aos cidadãos.

* **Zeladoria Urbana:** aplicação para registro e acompanhamento de solicitações de serviços de zeladoria urbana.

#### 4.3. Funcionalidades Principais

* **Cadastro e autenticação de usuários:** gerenciamento do acesso dos cidadãos e demais usuários autorizados.

* **Criação de solicitação de zeladoria:** permite ao cidadão registrar um problema encontrado no espaço público, informando sua descrição, categoria e localização.

* **Anexação de imagens:** permite associar imagens ou outros arquivos à solicitação.

* **Consulta de solicitações:** permite visualizar as solicitações registradas pelo usuário.

* **Atualização de solicitação:** permite alterar informações da solicitação enquanto sua situação permitir.

* **Cancelamento de solicitação:** permite cancelar solicitações ainda elegíveis para cancelamento.

* **Acompanhamento de status:** permite ao cidadão acompanhar o andamento da solicitação.

* **Gestão de solicitações:** permite aos servidores públicos consultar solicitações, assumir atendimentos e atualizar seus status.

* **Monitoramento da infraestrutura:** permite às equipes responsáveis acompanhar métricas, logs e eventos relevantes da plataforma.

* **Auditoria:** mantém registros das ações relevantes realizadas no ambiente para permitir rastreamento e investigação.

#### 4.4. Suposições e Dependências

* **Suposições:** a equipe possui acesso a uma conta AWS apropriada para o projeto e conhecimento dos serviços necessários para configuração da infraestrutura.

* **Suposições:** os cidadãos utilizarão a plataforma por meio de conexão com a internet.

* **Suposições:** as solicitações de zeladoria poderão conter dados pessoais e imagens relacionadas ao problema informado.

* **Dependências:** disponibilidade dos serviços AWS utilizados pela solução.

* **Dependências:** definição dos recursos AWS compatíveis com o orçamento e o prazo acadêmico.

---

### 5. Recursos do Produto (Arquitetura AWS)

Para implementar a visão proposta, a arquitetura AWS utilizará os seguintes recursos:

| **Serviço AWS** | **Papel na Arquitetura** | **Justificativa Técnica (Por que usar?)** |
|---|---|---|
| **Amazon VPC** | Isolamento de rede | Cria uma rede virtual isolada para organização dos recursos e controle da comunicação entre os componentes. |
| **Security Groups** | Controle de tráfego dos recursos | Restringem as conexões de entrada e saída dos recursos conforme as necessidades da aplicação. |
| **NACLs** | Controle das sub-redes | Fornecem uma camada adicional de controle de tráfego aplicada às sub-redes. |
| **IAM** | Controle de identidade e acesso | Permite gerenciar permissões de usuários, serviços e aplicações utilizando o princípio do menor privilégio. |
| **Amazon EC2 / ECS** | Computação | Executa os serviços do Portal Cidadão Seguro e do módulo de Zeladoria Urbana. |
| **Amazon RDS (PostgreSQL)** | Banco de dados relacional | Armazena os dados estruturados da plataforma, incluindo informações de usuários e solicitações. |
| **Amazon S3** | Armazenamento de arquivos | Armazena imagens, documentos e demais arquivos associados às solicitações. |
| **Amazon CloudWatch** | Monitoramento e logs | Centraliza métricas e logs para acompanhamento da infraestrutura e identificação de falhas ou comportamentos anormais. |
| **AWS CloudTrail** | Auditoria | Registra chamadas de API e ações realizadas no ambiente AWS para rastreamento e investigação. |
| **AWS KMS** | Criptografia | Gerencia chaves criptográficas utilizadas na proteção dos dados armazenados. |

---

### 6. Restrições do Projeto

* **Orçamentária:** A infraestrutura deverá respeitar o orçamento definido para o projeto acadêmico.

* **Prazo:** A implementação deverá respeitar o cronograma estabelecido pela disciplina.

* **Tecnológica:** A infraestrutura deverá utilizar a plataforma Amazon Web Services (AWS).

* **Segurança:** A arquitetura deverá utilizar VPC, Security Groups, NACLs e IAM conforme definido para o projeto.

* **Monitoramento:** A infraestrutura deverá utilizar Amazon CloudWatch para monitoramento e gerenciamento de logs.

* **Compliance:** A arquitetura deverá considerar os requisitos aplicáveis da LGPD.

* **Proteção de dados:** Informações pessoais e demais dados sensíveis tratados pela plataforma deverão possuir mecanismos adequados de proteção.

* **Equipe:** O desenvolvimento e a configuração da infraestrutura serão realizados pela equipe do projeto.

---

### 7. Atributos de Qualidade (SLAs E SLOs)

* **Segurança:** A infraestrutura deverá possuir múltiplas camadas de proteção, controle de acesso, criptografia e mecanismos de auditoria.

* **Disponibilidade:** A arquitetura deverá utilizar mecanismos que reduzam o impacto de falhas de componentes individuais, incluindo Multi-AZ quando aplicável.

* **Performance:** A plataforma deverá apresentar tempo de resposta adequado para as operações realizadas pelos cidadãos e servidores públicos, inclusive durante períodos de maior demanda.

* **Escalabilidade:** A infraestrutura deverá permitir ampliação da capacidade conforme o crescimento da quantidade de usuários e solicitações.

* **Auditabilidade:** As operações relevantes deverão possuir registros suficientes para identificar usuários, serviços, horários e ações realizadas.

* **Conformidade:** A solução deverá considerar os requisitos de proteção de dados e segurança estabelecidos pela LGPD.

* **Continuidade de Negócio:**
  * **RPO (Recovery Point Objective):** máximo de **15 minutos** de perda de dados.
  * **RTO (Recovery Time Objective):** tempo máximo de recuperação de **1 hora**.

---

### 8. Aprovação e Histórico de Versões

| **Versão** | **Data** | **Descrição da Alteração** | **Autor(es)** |
|---|---|---|---|
| 1.0 | 02/09/2026 | Elaboração inicial do Documento de Visão do Portal Cidadão Seguro. | Equipe do projeto |
| 1.1 | 17/09/2026 | Inclusão do módulo de Zeladoria Urbana e adequação da visão ao modelo do projeto de Cloud. | Equipe do projeto |