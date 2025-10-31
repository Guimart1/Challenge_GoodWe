# Challenge_GoodWe  
**Integração de assistente virtual com inversores e dashboard interativa**

##  Contribuidores
- Guilherme Martins Dos Santos 566570
- Julia Lopes De Souza 566557
- Daniel Castro Sanches 563333
- Gabriel Rodrigues Barbosa 566475
- Gabriel do Vale Vergueiro 564439
- Matheus Cordeiro Alves 563107

##  Visão Geral  
Este projeto foi desenvolvido como parte de um challenge da empresa GoodWe, com o objetivo de criar uma **solução completa de interação** entre:  
- Um assistente virtual capaz de se comunicar com os inversores da GoodWe;  
- Um back‑end que coleta, processa e disponibiliza dados dos inversores;  
- Um dashboard interativo para visualização e controle.  

O repositório contém a parte de **backend**, além dos assets estáticos e templates que alimentam a aplicação web.

##  Objetivos do Projeto  
- Permitir ao usuário **consultar o estado** dos inversores GoodWe (produção, consumo, falhas, etc) via assistente virtual;  
- Expor endpoints para integração com hardware/inversores ou API da GoodWe;  
- Apresentar um dashboard responsivo que visualize os dados em tempo real ou quase real;  
- Prover uma arquitetura modular que pode ser estendida para outros cenários IoT ou energia renovável.

##  Estrutura do Repositório  
```
/
│  app.py                   # Entrada principal da aplicação
│  main.py                  # Script adicional (ex: inicialização, CLI)
│  requirements.txt         # Dependências Python
│  .env.example             # Exemplo de variáveis de ambiente
│
├── backend/                # Código do backend (APIs, modelos de dados, lógica)
├── blueprints/             # Blueprints Flask (ou estrutura similar) para modularização
├── controles/              # Módulos de controle para hardware ou lógica de inversores
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── templates/              # Templates HTML para renderização do dashboard
└── voz_ia/                 # Módulo de assistente de voz / IA para interações verbais
```

## Tecnologias Utilizadas  
- **Python** — Linguagem principal  
- **Flask** — Framework web para criação da API e renderização de páginas  
- **HTML, CSS, JavaScript** — Front‑end do dashboard  
- **dotenv** — Gerenciamento de variáveis de ambiente  
- **SpeechRecognition / Pyttsx3** — Módulos para o assistente de voz

##  Como Rodar o Projeto (Setup)  
1. Clone o repositório:  
   ```bash
   git clone https://github.com/Guimart1/Challenge_GoodWe.git
   cd Challenge_GoodWe
   ```  
2. Crie um ambiente virtual (recomendado):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate     # Windows
   ```  
3. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Copie o arquivo `.env.example` para `.env` e configure as variáveis conforme necessário.  
5. Execute a aplicação:  
   ```bash
   python app.py
   ```  
6. Acesse o dashboard no navegador: `http://localhost:5000`

##  Funcionalidades Implementadas  
- Leitura e exibição de dados dos inversores GoodWe  
- Dashboard com indicadores e gráficos de desempenho  
- Interação por comandos de voz  
- Estrutura modular de código para manutenção e expansão

##  Roadmap / Funcionalidades Futuras  
- Autenticação e perfis de usuário  
- Integração com APIs externas de previsão solar  
- Alertas e notificações em tempo real  
- Suporte a múltiplos inversores  
- Otimização mobile e PWA

##  Contribuição  
1. Faça um fork do projeto  
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)  
3. Faça commit das mudanças (`git commit -m 'Descrição da feature'`)  
4. Envie para o repositório remoto (`git push origin feature/nova-feature`)  
5. Abra um Pull Request  

##  Licença  
Este projeto está licenciado sob [MIT License](LICENSE).  

##  Autores  
- **Guimart1** — Autor principal do projeto  
- **Daniel Castro Sanches** — Contribuidor  

---
 *Desenvolvido com foco em inovação e eficiência energética.*
