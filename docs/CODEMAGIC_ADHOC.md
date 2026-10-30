# Configuracao do MiniWatts no Codemagic (teste em iPhone)

## Objetivo

Compilar o fork como aplicativo iOS nativo em Swift, validar o build sem assinatura e, em seguida, produzir um IPA **Ad Hoc assinado** para iPhone 15 Pro Max com iOS 27.0. Esta etapa **nao** publica no TestFlight nem na App Store.

O codigo de sensores do projeto original foi mantido. As leituras reais e a compatibilidade com o iOS 27.0 so podem ser certificadas em teste no dispositivo.

## Identificadores desta branch

- App: `com.ubereatsoss.miniwatts`
- Extensao widget: `com.ubereatsoss.miniwatts.Widget`
- App Group compartilhado: `group.com.ubereatsoss.miniwatts`
- Xcode project / scheme: `MiniWatts.xcodeproj` / `MiniWatts`
- Compilador: Xcode 27.1, Swift 6.x
- Distribuicao: `ad_hoc`

Os IDs do aplicativo, da extensao e do App Group precisam ser criados na **mesma equipe** do Apple Developer Program. O App Group deve estar habilitado nos dois App IDs.

## Preparar Apple Developer

1. Confirmar inscricao ativa no Apple Developer Program.
2. Em Certificates, Identifiers & Profiles > Identifiers, registrar os dois App IDs explicitos acima.
3. Registrar o App Group acima e habilitar a capacidade App Groups para os dois App IDs.
4. Registrar o UDID do iPhone em Devices.
5. Gerar um certificado **Apple Distribution** e dois provisioning profiles **Ad Hoc** (app e widget). Ambos devem usar o mesmo certificado e incluir o iPhone; os perfis precisam conter a capacidade App Groups correspondente.
6. Nao colocar certificados, arquivos privados `.p8`, senhas, perfis de assinatura ou UDIDs neste repositorio publico.

## Preparar Codemagic

1. Conectar `ubereats-oss/MiniWatts` ao Codemagic e escolher esta branch.
2. Em Team settings > codemagic.yaml settings > Code signing identities, adicionar o certificado Apple Distribution e os dois perfis Ad Hoc. O perfil da extensao e obrigatorio.
3. Se usar App Store Connect API Key para importar os perfis, configurar a chave apenas na integracao segura do Codemagic.
4. Executar o workflow **ios-compile-check**, que nao exige assinatura, para testar o codigo.
5. Depois executar **ios-adhoc**. Ele aplica os perfis e produz `build/ios/ipa/*.ipa` em Artifacts.
6. Validar o IPA e o embedded provisioning profile da aplicacao e da extensao antes de tentar instalar.

## Instalacao

Um arquivo `.ipa` baixado isoladamente do Codemagic **nao e um link de instalacao no Safari**. A distribuicao diretamente ao iPhone requer uma pagina HTTPS e um manifesto `itms-services` (OTA), ou um instalador compativel. O fluxo de hospedagem OTA sera preparado depois da primeira compilacao assinada, sem usar Sideloadly. O UDID do iPhone deve estar no provisioning profile Ad Hoc.

## Validacao no dispositivo

Verificar ao menos:
- app abre no iPhone 15 Pro Max / iOS 27.0;
- leitura de nivel de bateria e status de carregamento;
- corrente, tensao e potencia reportadas, incluindo sinal durante descarga;
- temperatura, propriedades USB-C, sessoes e historico;
- widgets, App Group e Live Activities;
- comparacao das leituras com instrumento externo quando disponivel;
- indicar "indisponivel" quando algum sensor nao fornecer valor; nao converter ausencia em zero nem afirmar que estimativa e medicao.

## Regras para publicacao futura

MiniWatts usa APIs privadas do iOS. O fato de conseguir compilar e instalar Ad Hoc **nao** torna o aplicativo elegivel para publicacao na App Store. Uma versao publica precisara substituir os acessos privados por meios permitidos e revisar as funcionalidades afetadas.

Preservar `LICENSE` e `NOTICE` do projeto Apache-2.0.

## Referencias

- Codemagic iOS nativo: https://docs.codemagic.io/yaml-quick-start/building-a-native-ios-app/
- Assinatura iOS: https://docs.codemagic.io/yaml-code-signing/signing-ios/
- Cadastro de dispositivos: https://docs.codemagic.io/yaml-testing/ios-provisioning/
- Regras App Store: https://developer.apple.com/app-store/review/guidelines/
