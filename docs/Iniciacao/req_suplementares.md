# Documento de Requisitos Suplementares (v1.0)

## Portal Cidadão Seguro

**Projeto:** Projeto de Cloud - Fase de Inception  
**Data:** 17/09/2026  
**Status:** Versão inicial para validação arquitetural

---

## 1. Propósito e escopo

Este documento define os requisitos não funcionais, requisitos de disponibilidade, segurança, operação, escalabilidade, auditabilidade e conformidade da plataforma Portal Cidadão Seguro.

O escopo inclui:

- infraestrutura em nuvem na Amazon Web Services (AWS);
- rede e isolamento por meio de Amazon VPC e sub-redes públicas e privadas;
- controle de tráfego por meio de Security Groups e NACLs;
- gerenciamento de identidades e permissões por meio do IAM;
- execução da aplicação por meio de Amazon EC2 / ECS;
- persistência de dados por meio do Amazon RDS;
- armazenamento de arquivos por meio do Amazon S3;
- monitoramento e centralização de logs por meio do Amazon CloudWatch;
- auditoria das atividades da infraestrutura por meio do AWS CloudTrail;
- proteção de dados e gerenciamento de chaves por meio do AWS KMS;
- mecanismos de alta disponibilidade, escalabilidade, backup e recuperação;
- requisitos de proteção de dados relacionados à LGPD.

O documento tem como foco os requisitos arquiteturais e não funcionais da infraestrutura que suporta o Portal Cidadão Seguro e seus serviços, incluindo o módulo de Zeladoria Urbana.

---

## 2. Contexto e restrições

| Item | Premissa ou restrição |
|---|---|
| Escopo do sistema | Plataforma GovTech destinada à disponibilização de serviços públicos digitais |
| Módulo principal do projeto | Zeladoria Urbana, destinado à solicitação de serviços de zeladoria |
| Plataforma de nuvem | Amazon Web Services (AWS) |
| Segurança | Utilização de VPC, Security Groups, NACLs e IAM |
| Dados | A plataforma poderá tratar dados pessoais e informações relacionadas às solicitações dos cidadãos |
| Escalabilidade | A infraestrutura deve suportar crescimento significativo no número de usuários |
| Disponibilidade | A arquitetura deve reduzir o impacto de falhas de componentes individuais |
| Regulamentação | Lei Geral de Proteção de Dados (LGPD) |
| Orçamento | A infraestrutura deve respeitar o orçamento definido para o projeto acadêmico |
| Prazo | A implementação deve respeitar o cronograma definido pela disciplina |

---

## 3. Definições e indicadores

- **SLA:** compromisso formal de nível de serviço estabelecido entre as partes.
- **SLO:** objetivo mensurável utilizado para orientar o nível de serviço.
- **SLI:** indicador utilizado para medir o atendimento a um SLO.
- **RPO:** quantidade máxima de dados que pode ser perdida após uma falha.
- **RTO:** tempo máximo aceitável para recuperação do sistema após uma indisponibilidade.
- **MTTR:** tempo médio necessário para reparar ou restaurar um serviço.
- **Multi-AZ:** distribuição dos recursos entre múltiplas Availability Zones da AWS.
- **IAM:** serviço utilizado para gerenciamento de identidades, funções e permissões.
- **LGPD:** legislação brasileira relacionada ao tratamento e proteção de dados pessoais.

---

## 4. Requisitos de desempenho e capacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-PER-01 | A plataforma deve apresentar tempo de resposta adequado para as operações realizadas pelos usuários. | Testes de carga devem avaliar o tempo de resposta das operações principais da aplicação em condições normais e de alta demanda. |
| RNF-PER-02 | A infraestrutura deve suportar variações significativas na quantidade de acessos simultâneos. | A arquitetura deve permitir ampliação da capacidade de computação conforme o aumento da demanda. |
| RNF-CAP-01 | A infraestrutura deve ser capaz de crescer sem necessidade de reestruturação completa da solução. | Os recursos de computação devem permitir expansão horizontal ou aumento controlado de capacidade. |
| RNF-CAP-02 | O crescimento da quantidade de usuários não deve comprometer a disponibilidade dos serviços. | Testes de carga devem verificar o comportamento da aplicação sob aumento de acessos simultâneos. |

**Medição:** métricas de infraestrutura e aplicação obtidas por meio do Amazon CloudWatch e testes de carga controlados.

---

## 5. Requisitos de disponibilidade e confiabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-CON-01 | A infraestrutura deve utilizar mecanismos de alta disponibilidade quando aplicável. | Os componentes definidos como críticos devem possuir estratégia de redundância compatível com a arquitetura adotada. |
| RNF-CON-02 | A solução deve reduzir o impacto de falhas em componentes individuais. | A falha de um componente crítico não deve causar indisponibilidade permanente dos serviços. |
| RNF-CON-03 | A arquitetura deve utilizar múltiplas Availability Zones quando aplicável. | Os componentes que exigirem alta disponibilidade devem ser distribuídos entre Availability Zones compatíveis com a solução. |
| RNF-CON-04 | O RPO da solução deve ser de até 15 minutos. | Um exercício de recuperação deve demonstrar perda de dados igual ou inferior a 15 minutos. |
| RNF-CON-05 | O RTO da solução deve ser de até 1 hora. | Um exercício de recuperação deve demonstrar restauração do serviço em até 60 minutos. |

**Diretriz:** os mecanismos de disponibilidade, backup e recuperação deverão ser definidos considerando os serviços AWS escolhidos, os custos e as necessidades do projeto.

---

## 6. Requisitos de segurança e privacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-SEG-01 | Os recursos da infraestrutura devem ser isolados por meio de uma Amazon VPC. | Os recursos previstos na arquitetura devem estar associados à VPC definida para a solução. |
| RNF-SEG-02 | Os recursos que processam ou armazenam dados sensíveis devem permanecer em sub-redes privadas quando aplicável. | O banco de dados não deve possuir acesso direto à internet pública. |
| RNF-SEG-03 | O tráfego entre os componentes deve ser controlado por Security Groups e NACLs. | As regras devem permitir somente as comunicações necessárias entre os recursos. |
| RNF-SEG-04 | O acesso aos recursos AWS deve utilizar IAM e o princípio do menor privilégio. | Usuários, serviços e aplicações devem possuir somente as permissões necessárias para suas funções. |
| RNF-SEG-05 | Os dados sensíveis devem ser protegidos durante a transmissão. | As comunicações externas devem utilizar HTTPS/TLS. |
| RNF-SEG-06 | Os dados sensíveis armazenados devem possuir proteção por criptografia. | Os serviços que armazenam dados compatíveis com a arquitetura devem utilizar mecanismos de criptografia definidos pela AWS e gerenciados pelo AWS KMS. |
| RNF-SEG-07 | As atividades relevantes da infraestrutura devem ser auditáveis. | As operações administrativas e eventos relevantes devem possuir registros suficientes para rastreamento. |
| RNF-SEG-08 | O tratamento dos dados pessoais deve observar os requisitos aplicáveis da LGPD. | Os dados pessoais devem possuir controle de acesso, finalidade definida e mecanismos de proteção adequados. |

---

## 7. Requisitos de operação e observabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-OPS-01 | A saúde dos recursos da infraestrutura deve ser monitorada continuamente. | O CloudWatch deve disponibilizar métricas e logs dos recursos monitorados. |
| RNF-OPS-02 | A infraestrutura deve permitir a identificação de falhas e comportamentos anormais. | Métricas e logs relevantes devem estar disponíveis para análise pela equipe de TI. |
| RNF-OPS-03 | Os eventos relevantes da conta AWS devem possuir trilha de auditoria. | O AWS CloudTrail deve registrar as atividades configuradas para auditoria. |
| RNF-OPS-04 | Os logs e métricas relevantes devem ser centralizados. | Os registros definidos pela arquitetura devem estar disponíveis no ambiente de monitoramento configurado. |
| RNF-OPS-05 | A infraestrutura deve possuir mecanismos de backup e recuperação. | Os serviços que armazenam dados críticos devem possuir estratégia de backup compatível com os objetivos de RPO e RTO. |
| RNF-OPS-06 | Os procedimentos de recuperação devem ser verificáveis. | Deve existir procedimento documentado para restauração dos serviços e dados. |

---

## 8. Requisitos de manutenibilidade e entrega

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-MAN-01 | A infraestrutura deve permitir manutenção sem comprometer desnecessariamente os demais componentes da solução. | Alterações em componentes individuais devem poder ser realizadas sem exigir reconfiguração completa da infraestrutura. |
| RNF-MAN-02 | As configurações relevantes da infraestrutura devem ser documentadas. | Os principais recursos e respectivas configurações devem possuir documentação atualizada. |
| RNF-MAN-03 | As alterações realizadas no ambiente devem ser rastreáveis. | Mudanças administrativas devem possuir registro e identificação do responsável. |
| RNF-MAN-04 | A infraestrutura deve permitir recuperação após falhas de configuração. | Os procedimentos de backup, restauração e recuperação devem estar documentados. |

---

## 9. Requisitos de usabilidade operacional

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-USA-01 | A equipe responsável deve conseguir visualizar o estado dos recursos monitorados. | O CloudWatch deve disponibilizar informações relevantes sobre a operação da infraestrutura. |
| RNF-USA-02 | Os serviços da aplicação devem possuir documentação adequada para utilização pela equipe técnica. | As APIs disponibilizadas pela aplicação devem possuir documentação técnica correspondente quando aplicável. |
| RNF-USA-03 | Os registros de erro e monitoramento não devem expor informações sensíveis desnecessárias. | Logs e mensagens de erro devem evitar o armazenamento de credenciais, chaves ou informações sensíveis sem necessidade. |

---

## 10. Requisitos de custo

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-CUS-01 | A infraestrutura deve respeitar o orçamento definido para o projeto acadêmico. | A estimativa de utilização dos serviços AWS deve permanecer dentro do limite aprovado pela equipe. |
| RNF-CUS-02 | O custo dos recursos deve ser acompanhado durante a implementação. | A equipe deve realizar acompanhamento periódico da utilização e dos custos dos serviços utilizados. |
| RNF-CUS-03 | Decisões de alta disponibilidade, escalabilidade e segurança devem considerar o impacto financeiro. | A adoção de recursos adicionais deve possuir avaliação do impacto no orçamento do projeto. |

**Trade-off obrigatório:** decisões relacionadas a disponibilidade, desempenho, segurança e escalabilidade devem considerar o impacto correspondente no orçamento do projeto.

---

## 11. SLA e responsabilidades

O projeto não define neste momento um SLA comercial com usuários externos. Os objetivos de disponibilidade e recuperação utilizados pela arquitetura devem ser tratados como metas técnicas do projeto.

| Responsável | Obrigações principais |
|---|---|
| AWS | Disponibilidade dos serviços gerenciados e da infraestrutura física subjacente, conforme as condições aplicáveis aos serviços utilizados. |
| Equipe de projeto | Configuração da infraestrutura, IAM, segurança, monitoramento, backup, documentação, testes e controle dos recursos sob sua responsabilidade. |
| Equipe de Segurança da Informação | Avaliação e manutenção dos mecanismos de segurança, controle de acesso, auditoria e proteção dos dados. |
| Equipe de Governança / Compliance | Verificação dos requisitos relacionados à governança, proteção de dados e LGPD. |

Descumprimentos dos requisitos devem ser registrados para análise e definição das ações necessárias.

---

## 12. Dependências, riscos e decisões pendentes

| Item | Impacto | Tratamento |
|---|---|---|
| Custo da arquitetura Multi-AZ | Pode aumentar o custo da infraestrutura. | Avaliar os custos dos serviços antes da implementação final. |
| Escalabilidade para milhões de usuários | Pode exigir recursos adicionais de computação e distribuição de carga. | Validar a capacidade da arquitetura por meio de testes e estimativas de utilização. |
| Proteção de dados pessoais | Exposição indevida pode gerar riscos de segurança e conformidade. | Definir controles de acesso, criptografia, auditoria e políticas de retenção. |
| RPO de até 15 minutos | Pode exigir mecanismos de backup e recuperação adequados. | Validar a estratégia de backup e recuperação durante a implementação. |
| RTO de até 1 hora | Recuperações mais complexas podem ultrapassar a meta. | Documentar e testar os procedimentos de recuperação. |
| Utilização de serviços AWS adicionais | Pode aumentar a complexidade e o custo do ambiente. | Validar a necessidade de cada serviço antes da adoção. |

---

## 13. Critérios de aprovação

O documento será considerado aprovado quando:

1. todos os requisitos críticos possuírem critério de aceitação definido;
2. a arquitetura proposta demonstrar atendimento aos requisitos de segurança;
3. a arquitetura demonstrar estratégia compatível com os requisitos de disponibilidade e escalabilidade;
4. os mecanismos de monitoramento e auditoria estiverem definidos;
5. a estratégia de backup e recuperação estiver documentada;
6. os requisitos relacionados à LGPD forem revisados pela equipe responsável;
7. o custo estimado da infraestrutura estiver dentro do orçamento definido para o projeto.

---

## 14. Histórico de versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 17/09/2026 | Criação do Documento de Requisitos Suplementares para o Portal Cidadão Seguro. | Equipe do projeto |