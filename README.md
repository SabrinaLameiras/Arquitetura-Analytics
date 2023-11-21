# Arquitetura para ingerir, transformar, consultar e gerenciar conjuntos de dados de diversas fontes.

O fluxo do processo de alto nível para os componentes da solução implantados com o modelo AWS CloudFormation


Estrutura de uma Plataforma de dados completa para ingestão, transformação, gerenciamento e consulta de conjuntos de dados. Isso ajuda analistas e usuários do banco a gerenciar e obter insights de dados usando Amazon Web Services (AWS). Possui uma arquitetura de código aberto com conectores para serviços AWS comumente usados, juntamente com fontes e serviços de dados de terceiros. Esta solução também fornece uma interface de usuário (IU) para pesquisar, compartilhar, gerenciar e consultar conjuntos de dados usando comandos SQL padrão.

Esta solução é aplicável a uma variedade de casos de uso:

- Ingestão, transformação e consulta de conjuntos de dados diferentes.

- Fornecendo acesso simplificado aos dados para usuários empresariais não técnicos.

- Gerenciar políticas de governança e acesso de dados em toda a organização.

# Visão geral da arquitetura

<img width="795" alt="image" src="https://github.com/SabrinaLameiras/Arquitetura-de-Analytics/assets/67570204/1408fb1b-ce22-4606-8262-69ab3316bc15">

2 Front-end

Site estático : a solução usa Amazon CloudFrontpara distribuição e é protegido pelo AWS WAF. Ele também usa um bucket do Amazon S3 para hospedar e servir o front-end da web, incluindo páginas HTML, folhas de estilo CSS e código JavaScript.

Notificações : uma tabela do Amazon DynamoDB é usada para gerenciar e fornecer notificações persistentes na interface do usuário, junto com o Amazon API GatewayRecursos da API REST (recurso, método, modelo), AWS Lambdamanipulador (NodeJS) e um Amazon EventBridgeregra para mapear eventos para notificações.

3 Identidade federada : um Amazon Cognito O grupo de usuários gerencia a federação e o armazenamento de usuários de provedores de identidade externos (IDPs). Uma função AWS Lambda usa NodeJS para lidar com autorização personalizada de autenticação federada de provedores de identidade e mapeia usuários federados para análise automatizada de dados no modelo de gerenciamento de identidade e acesso da AWS. A solução provisiona um usuário administrador raiz no grupo de usuários do Amazon Cognito com base no e-mail e no número de telefone fornecidos nos parâmetros do modelo do CloudFormation:

O administrador raiz é o único usuário gerenciado diretamente pelo grupo de usuários e

Todos os outros usuários são federados através do IDP.

4 Camada de acesso e API

Gerenciamento de identidade e acesso (IAM):

Uma tabela do Amazon DynamoDB para armazenar instruções de política de grupo.

Um grupo de usuários do Amazon Cognito para gerenciar a autenticação de usuários federados.

Amazon API Gateway (API REST) ​​para federar solicitações e acessar todos os serviços e recursos subjacentes.

AWS Lambda como autorizador personalizado para controlar o acesso à API para usuários e máquinas federados.

Uma rede de distribuição do Amazon CloudFront para armazenar em cache e AWS WAFpara proteger a API.

O Amazon API Gateway (API HTTP) é usado para fazer proxy de solicitações de saída de clientes externos (por exemplo, Tableau ou PowerBI) por meio de credenciais de cliente do Amazon Cognito e facilitar a solicitação e a resposta para suportar formatos de cliente.

5 Gateway de eventos

Um gateway e barramento de eventos dedicado do Amazon EventBridge é usado para mensagens de aplicativos orientadas por eventos entre microsserviços e para propagar e persistir notificações aos usuários.

6 Serviços principais da solução

Serviço de produtos de dados: armazena detalhes sobre produtos de dados e gerencia a criação de infraestrutura dinâmica usada para ingerir, transformar e gerenciar diversas fontes de dados.

Funções AWS Lambda para lidar com solicitações de API (NodeJS).

Armazenamentos de dados do Amazon DynamoDB.

Funções de etapas da AWSpara gerenciar o ciclo de vida de produtos de dados.

Buckets do Amazon S3 para armazenamento de dados processados, scripts definidos pelo usuário e uploads de arquivos.

Glue AWS e recursos para lidar com o processamento de extração, transformação e carregamento de dados (ETL).

Função AWS Lambda utilizando AWS CDKe CloudFormation para implantar infraestrutura dinâmica para cada produto de dados (NodeJS).

Serviço de consulta : Responsável por executar consultas federadas governadas , armazenar/gerenciar consultas salvas e manter o cache de consultas.

Funções AWS Lambda para lidar com solicitações de API (NodeJS).

Amazon Atenaspara realizar consultas federadas que armazenam resultados em buckets do Amazon S3.

AWS Step Functions para orquestrar o ciclo de vida assíncrono de execução de consultas.

Armazenamentos de dados do Amazon DynamoDB para consultas salvas, histórico de consultas e cache de consultas.

Serviço de análise/renderização de consultas : responsável pela manipulação de consultas SQL. Isso é dissociado do serviço de consulta para fornecer flexibilidade na biblioteca de análise SQL.

Funções AWS Lambda para lidar com solicitações de API (NodeJS e Java).

Serviço de governança: permite definir termos ou classificações comuns de dados em todo o negócio e definir políticas de governança com base em grupos de usuários.

Funções AWS Lambda para lidar com solicitações de API (NodeJS).

Armazenamentos de dados do Amazon DynamoDB para armazenar metadados de governança.

7 Infraestrutura dinâmica: cada produto de dados implanta uma pilha AWS CloudFormation dedicada com recursos variados dependendo do tipo de fonte e dos dados, juntamente com regras do Amazon EventBridge para integração com serviços principais.

Funções AWS Lambda para lidar com importação de origem.

Pilha AWS CloudFormation para gerenciar recursos.

AWS Step Functions para orquestrar o gerenciamento do ciclo de vida.

Rastreadores, catálogos de dados e trabalhos do AWS Glue para ETL.

Gerenciador de segredos da AWSpara armazenar credenciais externas.

Amazon ECS tarefas para processar grandes trabalhos de ingestão de dados.

Amazon Athena e Amazon Comprehendpara detectar entidades PII.

8 Entrada (conectores de dados): a análise automatizada de dados na AWS oferece suporte a vários conectores de dados de origem prontos para uso, incluindo Amazon S3, Amazon Kinesis Stream, Amazon CloudWatch, Amazon CloudTrail, Amazon Redshift, File Upload, Google Cloud Storage, Google Analytics, Google BigQuery, MySQL5, Oracle, PostgreSQL, Microsoft SQL Server, DynamoDB ou MongoDB. Os recursos necessários para dar suporte a essas fontes de dados só são implantados durante a criação de um novo produto de dados de determinado tipo; não há recursos ociosos.

9 Saída (ferramentas de terceiros): a análise automatizada de dados na AWS oferece suporte aos padrões JDBC e ODBC para consumir dados de clientes comuns.
