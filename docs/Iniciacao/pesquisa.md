---
id: documento de visão
title: Documento de visão
---

# Documentos
### **1. Documento de visão**

- Tema: GovTech – "Portal Cidadão Seguro"
- Data: 2026.2
- Stakeholder: Caio Domingues - Keanu Santos - Eric Lerer - Gabriel Meireles

---

### **1.2 - Introdução**

- O propósito deste documento é definir a visão do produto Portal Cidadão Seguro, uma plataforma GovTech destinada ao atendimento e disponibilização de serviços públicos digitais para milhões de cidadãos.

O sistema será responsável pelo processamento e armazenamento de informações sensíveis, exigindo uma infraestrutura em nuvem altamente segura, escalável e auditável. O principal objetivo da solução é garantir a confidencialidade, integridade e disponibilidade dos dados, minimizando os riscos de vazamentos, acessos não autorizados e ataques à infraestrutura.

A plataforma será projetada utilizando serviços da Amazon Web Services (AWS), adotando mecanismos de isolamento de rede, controle granular de acesso, criptografia, monitoramento centralizado e trilhas completas de auditoria.

---

### **1.3 - Modulos**

- Portal: Reune serviços destinados aos cidadãos
- Zeladoria Urbana: Aplicação para solicitação de serviços de zeladoria urbana.

- Terminologias aplicadas
VPC (Virtual Private Cloud): ambiente de rede isolado utilizado para proteger os recursos da aplicação.
Security Groups: mecanismos de controle de tráfego associados aos recursos da AWS, funcionando de maneira stateful.
NACLs (Network Access Control Lists): regras de controle de tráfego aplicadas às sub-redes, funcionando de maneira stateless.
IAM (Identity and Access Management): gerenciamento de identidades, usuários, funções e permissões de acesso aos recursos da AWS.
CloudWatch: serviço utilizado para monitoramento, coleta e análise de logs e métricas.
KMS (Key Management Service): gerenciamento de chaves criptográficas utilizadas para proteger dados.
LGPD: legislação brasileira que estabelece regras para tratamento e proteção de dados pessoais.
RPO (Recovery Point Objective): quantidade máxima de dados que pode ser perdida após uma falha.
RTO (Recovery Time Objective): tempo máximo aceitável para recuperação do sistema após uma indisponibilidade

---

## **2.0 - Solução**


O problema é:	A necessidade de disponibilizar serviços públicos digitais capazes de armazenar e processar dados sensíveis de milhões de cidadãos com elevado nível de segurança.
Que afeta:	Cidadãos, servidores públicos, gestores e equipes de tecnologia responsáveis pela operação da plataforma.
Cujo impacto é:	Vazamento de dados pessoais, acessos indevidos, indisponibilidade dos serviços públicos, perda de confiança da população e possíveis consequências legais relacionadas à LGPD.
Uma boa solução seria:	Uma plataforma GovTech hospedada em uma arquitetura AWS segura, isolada e escalável, utilizando VPC, Security Groups, NACLs, IAM, criptografia, CloudWatch e mecanismos completos de auditoria.

O Portal Cidadão Seguro busca substituir ou complementar sistemas públicos legados por uma infraestrutura moderna em nuvem, permitindo maior controle sobre os acessos, monitoramento contínuo e capacidade de expansão conforme o número de usuários.

---

## **3.0 - Mapeamento de Steakeholders**

- Cidadãos

São os principais usuários da plataforma. Esperam que seus dados pessoais sejam tratados com segurança e que os serviços públicos digitais estejam disponíveis de forma confiável.

Gestores Públicos

Necessitam de indicadores sobre disponibilidade, utilização da plataforma, incidentes de segurança e cumprimento dos requisitos de governança.

Equipe de TI

Responsável pela administração da infraestrutura, configuração dos serviços AWS, gerenciamento de acessos, monitoramento, manutenção e resposta a incidentes.

Equipe de Segurança da Informação

Responsável por garantir que os controles de segurança estejam adequadamente configurados, acompanhando tentativas de acesso indevido, vulnerabilidades e eventos suspeitos.

Responsáveis pela Governança e Compliance

Precisam garantir que o tratamento dos dados esteja de acordo com as políticas internas e com os requisitos da LGPD, mantendo registros que permitam auditorias.

---


## **4.0 - Visão Geral da Solução**

- O Portal Cidadão Seguro será implementado utilizando uma arquitetura baseada em nuvem na AWS, priorizando segurança, isolamento e escalabilidade.

A infraestrutura será organizada dentro de uma Amazon VPC, dividindo os recursos em sub-redes públicas e privadas. Os componentes que armazenam ou processam dados sensíveis permanecerão em sub-redes privadas, sem exposição direta à internet.

O controle do tráfego será realizado por meio de Security Groups e NACLs, permitindo estabelecer regras específicas para comunicação entre os diferentes componentes da infraestrutura.

O acesso aos recursos AWS será controlado pelo IAM, utilizando o princípio do menor privilégio, de modo que cada usuário, serviço ou aplicação tenha somente as permissões necessárias para executar suas funções.

Os eventos e logs relevantes serão centralizados no Amazon CloudWatch, possibilitando o monitoramento da infraestrutura e a identificação de comportamentos suspeitos.

Dados sensíveis serão protegidos por criptografia em trânsito e em repouso, utilizando mecanismos como TLS/HTTPS e AWS KMS.

Além disso, a solução deverá manter trilhas de auditoria, permitindo identificar quem acessou determinado recurso, quando o acesso ocorreu e qual ação foi executada.


---


## **5.0 - Recursos Tecnológicos da Arquitetura AWS**

- 
Amazon VPC	Isolamento da infraestrutura	Cria uma rede virtual isolada, permitindo controlar como os recursos se comunicam e reduzindo a exposição da aplicação.
Security Groups	Controle de tráfego	Controlam o tráfego de entrada e saída dos recursos de forma stateful, permitindo restringir as comunicações entre os componentes.
NACLs	Controle das sub-redes	Funcionam como uma camada adicional de segurança, permitindo regras stateless de entrada e saída nas sub-redes.
IAM	Controle de identidade e acesso	Permite aplicar permissões granulares e o princípio do menor privilégio aos usuários e serviços.
Amazon CloudWatch	Monitoramento e logs	Centraliza métricas e logs, auxiliando na identificação de falhas, comportamentos anormais e incidentes de segurança.
AWS CloudTrail	Auditoria	Registra chamadas de API e ações realizadas no ambiente AWS, fornecendo evidências para auditoria e investigação.
AWS KMS	Criptografia	Gerencia chaves criptográficas utilizadas na proteção dos dados armazenados.
Amazon RDS	Banco de dados relacional	Armazena informações estruturadas da plataforma, utilizando recursos de segurança, backup e alta disponibilidade.
Amazon S3	Armazenamento de arquivos	Armazena documentos e outros arquivos de forma escalável, com controle de acesso e criptografia.
Amazon EC2 / ECS	Computação	Executa os serviços da aplicação de forma controlada e escalável.


---


## **6.0 - Segurança da Informação**

- A segurança é o principal requisito arquitetural do Portal Cidadão Seguro.

A infraestrutura deverá adotar uma estratégia de defesa em profundidade, utilizando diferentes camadas de proteção.

Isolamento de Rede

A infraestrutura será criada dentro de uma VPC, utilizando sub-redes privadas para os componentes que manipulam dados sensíveis.

Os bancos de dados não deverão possuir acesso direto à internet pública.

Security Groups

Os Security Groups serão configurados permitindo somente as portas e origens necessárias para a comunicação entre os componentes.

Por exemplo, o banco de dados deverá aceitar conexões somente dos serviços da aplicação que realmente necessitam acessá-lo.

NACLs

As NACLs serão utilizadas como uma camada adicional de controle de tráfego nas sub-redes, permitindo bloquear determinados tipos de comunicação antes que o tráfego alcance os recursos.

IAM

O IAM será configurado seguindo o princípio do menor privilégio.

Cada usuário ou serviço deverá possuir somente as permissões necessárias para executar suas atividades, reduzindo o impacto de possíveis comprometimentos de credenciais.

Criptografia

Os dados sensíveis deverão ser protegidos:

Em trânsito: utilizando HTTPS/TLS;
Em repouso: utilizando mecanismos de criptografia da AWS;
Chaves criptográficas: administradas pelo AWS KMS.
Auditoria

Todas as ações relevantes deverão ser registradas para permitir rastreamento e investigação.

A solução utilizará AWS CloudTrail para registrar atividades na conta AWS e CloudWatch para monitoramento e centralização de logs.


---


## **7.0 - Compliance e LGPD**

- A segurança é o principal requisito arquitetural do Portal Cidadão Seguro.

A infraestrutura deverá adotar uma estratégia de defesa em profundidade, utilizando diferentes camadas de proteção.

Isolamento de Rede

A infraestrutura será criada dentro de uma VPC, utilizando sub-redes privadas para os componentes que manipulam dados sensíveis.

Os bancos de dados não deverão possuir acesso direto à internet pública.

Security Groups

Os Security Groups serão configurados permitindo somente as portas e origens necessárias para a comunicação entre os componentes.

Por exemplo, o banco de dados deverá aceitar conexões somente dos serviços da aplicação que realmente necessitam acessá-lo.

NACLs

As NACLs serão utilizadas como uma camada adicional de controle de tráfego nas sub-redes, permitindo bloquear determinados tipos de comunicação antes que o tráfego alcance os recursos.

IAM

O IAM será configurado seguindo o princípio do menor privilégio.

Cada usuário ou serviço deverá possuir somente as permissões necessárias para executar suas atividades, reduzindo o impacto de possíveis comprometimentos de credenciais.

Criptografia

Os dados sensíveis deverão ser protegidos:

Em trânsito: utilizando HTTPS/TLS;
Em repouso: utilizando mecanismos de criptografia da AWS;
Chaves criptográficas: administradas pelo AWS KMS.
Auditoria

Todas as ações relevantes deverão ser registradas para permitir rastreamento e investigação.

A solução utilizará AWS CloudTrail para registrar atividades na conta AWS e CloudWatch para monitoramento e centralização de logs.


---

## **8.0 - Escalabilidade e Disponibilidade**

- Como a plataforma será utilizada potencialmente por milhões de cidadãos, a infraestrutura deverá suportar variações significativas na quantidade de acessos.

A arquitetura deverá utilizar mecanismos de escalabilidade horizontal e distribuição de carga para evitar que um único componente se torne um ponto de falha.

A utilização de múltiplas Availability Zones (Multi-AZ) permitirá aumentar a disponibilidade da solução e reduzir o impacto de falhas em uma única zona.

O dimensionamento automático dos recursos poderá ser utilizado para aumentar a capacidade durante períodos de alta demanda e reduzi-la quando a utilização estiver baixa.

---


## **9.0 - Atributos de Qualidade**

- Segurança

A segurança é o principal atributo de qualidade do sistema. O ambiente deverá possuir múltiplas camadas de proteção, controle granular de acesso, criptografia e auditoria.

Disponibilidade

A infraestrutura deverá ser projetada para manter os serviços disponíveis mesmo diante da falha de componentes individuais, utilizando arquitetura Multi-AZ quando aplicável.

Performance

A plataforma deverá apresentar tempo de resposta adequado mesmo durante períodos de elevada quantidade de acessos simultâneos.

Escalabilidade

A infraestrutura deverá ser capaz de aumentar ou reduzir sua capacidade conforme a demanda, permitindo atender milhões de usuários sem necessidade de dimensionamento manual constante.

Auditabilidade

Todas as ações relevantes deverão possuir registros suficientes para identificar usuários, serviços, horários e operações realizadas.

Conformidade

A solução deverá ser projetada considerando os requisitos de proteção de dados e segurança estabelecidos pela LGPD.

---

## **10.0 - Continuidade de Negócio**

- A plataforma deverá possuir mecanismos de backup e recuperação capazes de reduzir os impactos causados por falhas, indisponibilidade ou incidentes de segurança.

Como objetivos iniciais da solução, são definidos:

RPO: até 15 minutos;
RTO: até 1 hora.

Os valores deverão ser validados durante a implementação, considerando os serviços AWS escolhidos, os custos e os requisitos reais do sistema.

---

## **11.0 - Restrições do Projeto**

- Orçamento: a infraestrutura deverá respeitar o orçamento definido para o projeto acadêmico.
Prazo Acadêmico: o desenvolvimento deverá ser concluído dentro do cronograma estabelecido pela disciplina.
Stack: utilização da AWS como plataforma de infraestrutura.
Segurança: utilização obrigatória de VPC, Security Groups, NACLs e IAM.
Monitoramento: utilização de CloudWatch para monitoramento e gerenciamento dos logs.
Compliance: a arquitetura deverá considerar os requisitos da LGPD.
Equipe: o desenvolvimento e a configuração da infraestrutura serão realizados pela equipe do projeto.




---




## **12.0 - Benefícios Esperados**
- Com a implementação do Portal Cidadão Seguro, espera-se:

Reduzir o risco de vazamento de dados dos cidadãos;
Restringir acessos não autorizados aos recursos da plataforma;
Garantir maior rastreabilidade das ações realizadas;
Facilitar auditorias de segurança e compliance;
Aumentar a disponibilidade dos serviços públicos digitais;
Permitir escalabilidade para milhões de usuários;
Centralizar o monitoramento da infraestrutura;
Criar uma arquitetura preparada para evolução futura.




---


## **13.0 - Requisitos Não Funcionais - Portal Cidadão Seguro (GovTech)**

Com base no documento de visão fornecido para o **Portal Cidadão Seguro**, os requisitos não funcionais (RNFs) foram estruturados e categorizados de acordo com os atributos de qualidade, segurança e restrições descritos no projeto:

## 1. Segurança
* **RNF01 - Isolamento de Rede:** A infraestrutura de nuvem deve ser implantada inteiramente dentro de uma Amazon VPC, segregando recursos em sub-redes públicas e privadas. Componentes que manipulam dados sensíveis e bancos de dados (como o Amazon RDS) devem residir exclusivamente em sub-redes privadas, sem acesso direto à internet pública.
* **RNF02 - Controle de Tráfego por Camadas:** O tráfego de rede deve ser controlado em múltiplos níveis utilizando **Security Groups** (comportamento *stateful*) para restringir a comunicação entre os recursos e serviços da aplicação, e **Network Access Control Lists (NACLs)** (*stateless*) como camada adicional de inspeção e bloqueio nas sub-redes.
* **RNF03 - Princípio do Menor Privilégio (IAM):** O acesso a todos los recursos da AWS deve ser gerenciado via IAM, aplicando obrigatoriamente o princípio do menor privilégio para usuários, serviços e aplicações, concedendo apenas as permissões estritamente necessárias para a execução de suas funções.
* **RNF04 - Criptografia de Dados:** Todos os dados sensíveis dos cidadãos devem ser protegidos obrigatoriamente **em trânsito** (utilizando protocolos HTTPS/TLS) e **em repouso** (utilizando mecanismos de criptografia gerenciados pelo **AWS KMS**).

## 2. Confiabilidade e Disponibilidade
* **RNF05 - Alta Disponibilidade (Multi-AZ):** A arquitetura da aplicação e do banco de dados deve ser distribuída em múltiplas Zonas de Disponibilidade (Multi-AZ) na AWS, garantindo a continuidade dos serviços públicos digitais mesmo em caso de falha de um componente ou zona individual.
* **RNF06 - Recuperação de Desastres (Disaster Recovery):** O sistema deve atender às metas de continuidade de negócio estabelecidas:
  * **RPO (Recovery Point Objective):** Máximo de 15 minutos de perda tolerável de dados.
  * **RTO (Recovery Time Objective):** Tempo máximo de recuperação e restabelecimento do sistema fixado em até 1 hora.

## 3. Escalabilidade e Desempenho
* **RNF07 - Escalabilidade Horizontal:** A infraestrutura deve suportar variações expressivas na volumetria de acessos simultâneos de milhões de cidadãos, utilizando recursos de dimensionamento automático (*Auto Scaling*) e balanceamento de carga para evitar pontos únicos de falha.
* **RNF08 - Tempo de Resposta:** A plataforma deve manter tempos de resposta adequados e estáveis mesmo sob picos de alta demanda e tráfego elevado na rede.

## 4. Auditabilidade e Monitoramento
* **RNF09 - Centralização de Logs e Métricas:** Todas as métricas de infraestrutura, eventos e logs de aplicação devem ser centralizados e monitorados em tempo real por meio do **Amazon CloudWatch**, permitindo a detecção rápida de comportamentos anormais ou incidentes de segurança.
* **RNF10 - Trilha de Auditoria:** O sistema deve registrar de forma imutável e centralizada todas as chamadas de API, acessos administrativos e operações relevantes na conta AWS utilizando o **AWS CloudTrail**, garantindo evidências completas para auditorias forenses e de segurança.

## 5. Conformidade (Compliance)
* **RNF11 - Aderência à LGPD:** A arquitetura, o tratamento, o armazenamento e o ciclo de vida dos dados pessoais tratados pela plataforma devem estar em total conformidade com as diretrizes e exigências da Lei Geral de Proteção de Dados (LGPD).

## 6. Restrições Tecnológicas
* **RNF12 - Provedor de Nuvem Obrigatório:** Toda a infraestrutura, processamento e armazenamento do Portal Cidadão Seguro devem ser hospedados e executados exclusivamente na plataforma de nuvem da **Amazon Web Services (AWS)**, utilizando os serviços especificados na arquitetura base (VPC, IAM, RDS, S3, EC2/ECS, CloudWatch, CloudTrail, KMS, NACLs e Security Groups).




---



## **14.0 - Histórico de Versões**

- 02/09/2026
1.0
Criação do Documento de Visão para o projeto Portal Cidadão Seguro.


---











