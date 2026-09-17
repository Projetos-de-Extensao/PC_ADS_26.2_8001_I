```puml
@startuml
left to right direction

actor "Engenheiro de Cloud /\nInfraestrutura" as Cloud
actor "Engenheiro de Segurança" as Sec
actor "DevOps /\nAdministrador de Sistemas" as DevOps
actor "Administrador de Banco de Dados" as DBA
actor "Desenvolvedor Backend" as Dev

rectangle "Configuração da Infraestrutura\nPortal Cidadão Seguro" {

    usecase "Configurar VPC" as UC1
    usecase "Configurar Subnet Pública" as UC2
    usecase "Configurar Subnet Privada" as UC3
    usecase "Configurar Internet Gateway" as UC4

    usecase "Configurar Security Group\nda EC2" as UC5
    usecase "Configurar Security Group\ndo RDS" as UC6

    usecase "Configurar EC2" as UC7
    usecase "Implantar Backend" as UC8

    usecase "Configurar RDS\nPostgreSQL" as UC9

    usecase "Configurar Bucket S3" as UC10
    usecase "Configurar acesso ao\narmazenamento de imagens" as UC11
}

' Infraestrutura de rede
Cloud --> UC1
Cloud --> UC2
Cloud --> UC3
Cloud --> UC4

' Segurança
Sec --> UC5
Sec --> UC6

' Computação / aplicação
DevOps --> UC7
DevOps --> UC8
Dev --> UC8

' Banco
DBA --> UC9

' Armazenamento
DevOps --> UC10
Dev --> UC11


@enduml


@startuml
title Diagrama 1 - Infraestrutura Simplificada

skinparam componentStyle rectangle
skinparam shadowing false

actor "Cidadão /\nServidor Público" as Usuario

cloud "AWS Cloud" {

    node "Security Group" as SG <<security>> {
        artifact "Porta 80 (HTTP)"
        artifact "Porta 443 (HTTPS)"
        artifact "Restrições de acesso"
    }

    node "EC2" as EC2 <<compute>> {
        component "Portal Cidadão Seguro" as Portal {
            component "Módulo de Zeladoria Urbana" as Zeladoria {
                artifact "Cadastro de solicitações"
                artifact "Consulta de solicitações"
                artifact "Atualização de solicitações"
                artifact "Cancelamento de solicitações"
            }
        }
    }

    database "Banco de Dados" as DB <<database>> {
        artifact "Dados de cidadãos"
        artifact "Solicitações de zeladoria"
        artifact "Categorias"
        artifact "Status"
    }

    storage "Amazon S3" as S3 <<storage>> {
        artifact "Imagens de solicitações"
        artifact "Documentos anexos"
    }

    node "IAM" as IAM <<identity>> {
        artifact "Controle de permissões"
        artifact "Acesso aos serviços AWS"
        artifact "Perfis e políticas"
    }
}

Usuario --> SG : HTTPS
SG --> EC2
EC2 --> DB : Persistência
EC2 --> S3 : Imagens / anexos
IAM ..> EC2 : Permissões
IAM ..> S3 : Permissões
IAM ..> DB : Permissões

@enduml

@startuml
title Diagrama 2 - Infraestrutura Completa (Visão do Documento)

skinparam componentStyle rectangle
skinparam shadowing false

actor "Cidadão /\nServidor Público" as Usuario

cloud "AWS Cloud" {

    node "Amazon Route 53" as Route53 <<dns>> {
        artifact "Gerenciamento de DNS"
    }

    node "Application Load Balancer" as ALB <<load balancer>> {
        artifact "Distribuição de tráfego"
    }

    frame "VPC" as VPC {

        frame "Subnet Pública - AZ 1" as PublicAZ1 {
            node "Auto Scaling Group" as ASG1 <<compute>> {
                node "EC2 - 01" as EC1 <<compute>>
                node "EC2 - 02" as EC2 <<compute>>

                component "Portal Cidadão Seguro" as Portal1 {
                    component "Módulo de Zeladoria Urbana" as Zeladoria1
                }
            }
        }

        frame "Subnet Pública - AZ 2" as PublicAZ2 {
            node "Auto Scaling Group" as ASG2 <<compute>> {
                node "EC2 - 03" as EC3 <<compute>>
                node "EC2 - 04" as EC4 <<compute>>

                component "Portal Cidadão Seguro" as Portal2 {
                    component "Módulo de Zeladoria Urbana" as Zeladoria2
                }
            }
        }

        frame "Subnet Privada - AZ 1" as PrivateAZ1 {
            database "Amazon RDS" as RDS <<database>> {
                artifact "Banco de dados principal"
                artifact "Multi-AZ"
            }
        }

        frame "Subnet Privada - AZ 2" as PrivateAZ2 {
            database "RDS Standby" as RDSStandby <<database>>
        }

        storage "Amazon S3" as S3 <<storage>> {
            artifact "Imagens e documentos"
            artifact "Backup (opcional)"
        }

        node "Network ACLs" as NACL <<security>> {
            artifact "Regras de rede"
        }

        node "Security Groups" as SG <<security>> {
            artifact "Controle de acesso"
            artifact "Regras de tráfego"
        }
    }

    node "IAM" as IAM <<identity>> {
        artifact "Perfis e políticas"
        artifact "Controle de acesso"
    }

    node "AWS KMS" as KMS <<security>> {
        artifact "Criptografia de dados"
    }

    node "Amazon CloudWatch" as CW <<monitoring>> {
        artifact "Logs"
        artifact "Métricas"
        artifact "Monitoramento"
    }

    node "AWS CloudTrail" as CT <<audit>> {
        artifact "Auditoria de ações"
        artifact "Registro de chamadas de API"
    }

    node "AWS Backup" as Backup <<backup>> {
        artifact "Cópias de segurança"
    }
}

Usuario --> Route53
Route53 --> ALB
ALB --> ASG1
ALB --> ASG2

ASG1 --> RDS : Dados
ASG2 --> RDS : Dados
ASG1 --> S3 : Imagens / anexos
ASG2 --> S3 : Imagens / anexos

RDS --> RDSStandby : Replicação / Multi-AZ

SG ..> ASG1 : Controle
SG ..> ASG2 : Controle
SG ..> RDS : Controle
NACL ..> PublicAZ1 : Regras
NACL ..> PublicAZ2 : Regras
NACL ..> PrivateAZ1 : Regras
NACL ..> PrivateAZ2 : Regras

IAM ..> ASG1 : Permissões
IAM ..> ASG2 : Permissões
IAM ..> RDS : Permissões
IAM ..> S3 : Permissões

KMS ..> RDS : Criptografia
KMS ..> S3 : Criptografia

CW ..> ASG1 : Monitoramento
CW ..> ASG2 : Monitoramento
CW ..> RDS : Métricas
CW ..> S3 : Logs

CT ..> IAM : Auditoria
CT ..> ASG1 : Auditoria
CT ..> ASG2 : Auditoria
CT ..> RDS : Auditoria

Backup ..> RDS : Backup
Backup ..> S3 : Backup

@enduml