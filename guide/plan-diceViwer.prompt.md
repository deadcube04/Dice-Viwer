## Plan: Aprendizado Guiado de Visão Computacional para Dados

Objetivo: te ensinar do zero, em etapas, para você mesmo montar 2 notebooks:
1. Treino (reconhecer tipo de dado pela geometria + ler número visível).
2. Inferência (receber imagem, identificar dado, ler número e calcular face oposta).

Abordagem recomendada:
- YOLOv11 para detectar e classificar o tipo de dado (D4, D6, D8, D10, D12, D20).
- OpenCV para leitura do número.
- Duas estratégias para face oposta: fórmula matemática e tabela de mapeamento (lookup).

**Fases**
1. Fase 0 - Preparação do ambiente (bloqueante)
1. Instalar stack Python com CUDA, Ultralytics, OpenCV e dependências.
2. Validar GPU ativa e inferência mínima em uma imagem.
3. Definir padrão de organização de pastas, nomes e versionamento de dados/modelos.

2. Fase 1 - Base conceitual enxuta (pode rodar junto com início da coleta)
1. Entender diferença entre detecção, classificação e leitura de número.
2. Entender por que YOLO resolve forma/tipo e OpenCV resolve face/número.
3. Definir métricas de sucesso por tarefa:
- Tipo do dado (acurácia/precision/recall por classe).
- Número visível (taxa de leitura correta).
- Resultado final (tipo + número + oposto correto).

3. Fase 2 - Coleta do dataset próprio (bloqueia treino de qualidade)
1. Fotografar cada tipo de dado com variação de luz, fundo, ângulo, distância e rotação.
2. Garantir balanceamento por classe.
3. Separar treino, validação e teste sem vazamento.
4. Criar protocolo de captura para repetibilidade.

4. Fase 3 - Notebook 1 (YOLOv11 para tipo de dado)
1. Rotular caixas dos dados com a classe correta.
2. Treinar com modelo pré-treinado e fine-tuning.
3. Ajustar só hiperparâmetros essenciais no começo.
4. Avaliar matriz de confusão e erros por classe.
5. Salvar melhor checkpoint para uso no Notebook 2.

5. Fase 4 - Notebook 1 (OpenCV para número da face)
1. Recortar a região do dado detectado.
2. Aplicar pré-processamento (contraste, limiarização, redução de ruído, correção geométrica).
3. Ler número com OCR/classificador de dígito.
4. Medir taxa de acerto por tipo de dado e por condição de iluminação.
5. Implementar fallback para baixa confiança.

6. Fase 5 - Face oposta com dois métodos
1. Método A: fórmula por tipo quando houver convenção confiável.
2. Método B: tabela de mapeamento por tipo/face para validar casos reais.
3. Comparar os dois métodos com amostras reais e registrar divergências.

7. Fase 6 - Notebook 2 (pipeline ponta a ponta)
1. Carregar modelo YOLO treinado.
2. Detectar tipo do dado na imagem.
3. Ler número visível com OpenCV.
4. Calcular face oposta com método escolhido (e opcionalmente comparar com o outro).
5. Retornar resultado final com score de confiança e logs simples.

8. Fase 7 - Robustez e depuração
1. Tratar blur, reflexo, oclusão e perspectiva extrema.
2. Definir thresholds de confiança e reprocessamento.
3. Criar casos de teste difíceis para evitar falsa sensação de acerto.

9. Fase 8 - Rotina didática em modo ask
1. Ciclo fixo por sessão: conceito curto → tarefa manual → revisão comigo → correção.
2. Critério de avanço por fase: só avança quando bater métrica mínima acordada.
3. Registro de erros comuns e decisões para consolidar aprendizado.

**Verificação**
1. Ambiente: imports e GPU funcionando.
2. Dataset: volume mínimo por classe e split correto.
3. Tipo do dado: desempenho por classe, não só média global.
4. Número visível: taxa de leitura correta em condições variadas.
5. Face oposta: validação em exemplos reais por tipo.
6. End-to-end: acerto final em imagens nunca vistas.

**Decisões já alinhadas**
1. Ambiente com GPU NVIDIA.
2. Dataset com fotos feitas por você.
3. Nível didático intermediário.
4. Você quer aprender os dois métodos de face oposta.

**Escopo**
1. Inclui: 2 notebooks, treino + inferência, YOLOv11 + OpenCV, cálculo de oposto por fórmula e tabela.
2. Exclui neste primeiro ciclo: deploy web/API, otimização avançada de latência, pipeline distribuído.

Se você aprovar este plano, na próxima interação eu já entro no modo ask e começo pela Fase 0 com checklist prático e perguntas curtas para te guiar passo a passo.