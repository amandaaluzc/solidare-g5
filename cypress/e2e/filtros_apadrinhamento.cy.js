Cypress.Commands.add('deletar_superuser', () => {
  cy.exec('python delete_superuser.py', { failOnNonZeroExit: false }).then((result) => {
    console.log(result.stdout);
    if (result.stderr) {
      console.error(result.stderr);
    }
  });
});

Cypress.Commands.add('add_superuser', () => {
  cy.exec('python create_superuser.py', { failOnNonZeroExit: false }).then((result) => {
    console.log(result.stdout);
    if (result.stderr) {
      console.error(result.stderr);
    }
  });
});
describe('História 04: Apadrinhamento com Filtro', () => {
  before(() => {
    cy.deletar_superuser();
    cy.add_superuser();
  });
  const dadosPadrinho = {
    primeiroNome: 'Padrinho',
    sobrenome: 'Filtrado',
    senha: 'senhaSegura123!',
    telefone: '11999999999',
  };

  let emailUnico;
  let cpfUnico;

  before(() => {
    cy.request('POST', '/teste/limpar-geral/');
    cy.log('Dados limpos antes de todos os testes de apadrinhamento com filtro.');

    // Login como admin para cadastrar as 3 crianças
    cy.visit('/login_admin');
    cy.get('input[name="nome"]').type('adminsolidare');
    cy.get('input[name="password"]').type('admin123');
    cy.get('form').submit();
    cy.url().should('not.include', '/login_admin');

    // Cadastro criança 1
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Ana');
    cy.get('input[name="idade"]').type('7');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('textarea[name="descricao"]').type('Criança Ana.');
    cy.get('button.btn-cadastrar').click();

    // Cadastro criança 2
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Bruno');
    cy.get('input[name="idade"]').type('9');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('textarea[name="descricao"]').type('Criança Bruno.');
    cy.get('button.btn-cadastrar').click();

    // Cadastro criança 3
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Carla');
    cy.get('input[name="idade"]').type('12');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('textarea[name="descricao"]').type('Criança Carla.');
    cy.get('button.btn-cadastrar').click();

    // Logout admin
    cy.visit('/');
    cy.contains('button', 'Sair').click();
  });

  beforeEach(() => {
    emailUnico = `padrinho.filtrado.${Cypress._.uniqueId()}@example.com`;
    cpfUnico = `123${Cypress._.uniqueId().substring(0, 8)}`;

    cy.visit('/');
    cy.contains('button', 'Torne-se padrinho').click();
    cy.url().should('include', '/pagina-exibicao');

    cy.get('.card').first().click();
    cy.get('.modal:visible').should('be.visible')
      .find('.btn-apadrinhar').click();

    cy.url().should('include', '/login');

    cy.log('Redirecionado para o login. Agora, cadastrando novo padrinho...');
    cy.contains('a', 'Cadastre-se aqui').click();
    cy.url().should('include', '/registrar');

    cy.get('input[name="first_name"]').type(dadosPadrinho.primeiroNome);
    cy.get('input[name="last_name"]').type(dadosPadrinho.sobrenome);
    cy.get('input[name="email"]').type(emailUnico);
    cy.get('input[name="password1"]').type(dadosPadrinho.senha);
    cy.get('input[name="password2"]').type(dadosPadrinho.senha);
    cy.get('input[name="telefone"]').type(dadosPadrinho.telefone);
    cy.get('input[name="cpf"]').type(cpfUnico);
    cy.get('form').submit();

    cy.url().should('include', '/');
  });

  it('Cenário 1: Filtrar por Gênero "Menina" e apadrinhar', () => {
    cy.visit('/pagina-exibicao');
    cy.url().should('include', '/pagina-exibicao');

    cy.get('#filtro-genero').select('F');

    cy.wait(500);

    cy.get('.card[data-genero="M"]').should('not.be.visible');
    cy.get('.card[data-genero="F"]').each(($el) => {
      cy.wrap($el).should('be.visible');
    });

    cy.get('.card[data-genero="F"]').first().click();
    cy.get('.modal:visible').should('be.visible')
      .find('.btn-apadrinhar').click();

    cy.url().should('include', '/login');

    cy.get('input[name="email"]').type(emailUnico);
    cy.get('input[name="password"]').type(dadosPadrinho.senha);
    cy.get('form').submit();

    cy.get('button.btn-confirmar:visible').first().click();
    cy.get('#modal-confirmacao').should('not.have.class', 'hidden');
    cy.get('#modal-confirmacao form').submit();

    cy.on('window:alert', (text) => {
      expect(text).to.contains('Criança apadrinhada com sucesso');
    });
    cy.url().should('include', '/pagina-exibicao');
  });

  it('Cenário 2: Filtrar por Idade "6-10 anos" e apadrinhar', () => {
    cy.visit('/pagina-exibicao');
    cy.url().should('include', '/pagina-exibicao');

    cy.get('#filtro-idade').select('6-10');

    cy.wait(500);

    cy.get('.card').each(($card) => {
      const idade = parseInt($card.attr('data-idade'));
      if (idade >= 6 && idade <= 10) {
        cy.wrap($card).should('be.visible');
      } else {
        cy.wrap($card).should('not.be.visible');
      }
    });

    cy.get('.card:visible').first().click();
    cy.get('.modal:visible').should('be.visible')
      .find('.btn-apadrinhar').click();

    cy.url().should('include', '/login');

    cy.get('input[name="email"]').type(emailUnico);
    cy.get('input[name="password"]').type(dadosPadrinho.senha);
    cy.get('form').submit();

    cy.get('button.btn-confirmar:visible').first().click();
    cy.get('#modal-confirmacao').should('not.have.class', 'hidden');
    cy.get('#modal-confirmacao form').submit();

    cy.on('window:alert', (text) => {
      expect(text).to.contains('Criança apadrinhada com sucesso');
    });
    cy.url().should('include', '/pagina-exibicao');
  });
});
