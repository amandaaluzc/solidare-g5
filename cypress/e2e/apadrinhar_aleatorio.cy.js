beforeEach(() => {
  // Limpa o sistema
  cy.request('POST', '/teste/limpar-geral/');

  // Cadastra uma criança antes de cada teste
  cy.visit('/login_admin');
  cy.get('input[name="nome"]').type('Solidareadmin');
  cy.get('input[name="password"]').type('ADM12345');
  cy.get('form').submit();
  cy.url().should('not.include', '/login_admin');

  cy.visit('/criancas/cadastrar/');
  cy.get('input[name="nome"]').type('Maria Aleatoria');
  cy.get('input[name="idade"]').type('8');
  cy.get('select[name="genero"]').select('Feminino');
  cy.get('textarea[name="descricao"]').type('Criança cadastrada antes do teste aleatório.');
  cy.get('button.btn-cadastrar').click();

  // Logout admin
  cy.visit('/');
  cy.contains('button', 'Sair').click();
});

describe('História 02: Apadrinhar uma criança aleatoriamente', () => {
  it('Cenário: Usuário apadrinha uma criança clicando no botão "Escolha por mim"', () => {
    cy.visit('/');
    cy.contains('button', 'Torne-se padrinho').click();

    cy.url().should('include', '/pagina-exibicao');

    cy.get('#btn-aleatorio').click();

    cy.get('.modal:visible').should('be.visible');
    cy.get('.modal:visible').find('.btn-apadrinhar').click();

    cy.url().should('include', '/login');

    cy.contains('a', 'Cadastre-se aqui').click();
    cy.url().should('include', '/registrar');

    const email = `teste.${Date.now()}@email.com`;

    cy.get('input[name="first_name"]').type('João');
    cy.get('input[name="last_name"]').type('Silva');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password1"]').type('senhaSegura123!');
    cy.get('input[name="password2"]').type('senhaSegura123!');
    cy.get('input[name="telefone"]').type('11999999999');
    cy.get('input[name="cpf"]').type('12345678900');
    cy.get('form').submit();

    cy.url().should('include', '/');
    cy.contains('button', 'Torne-se padrinho').click();

    cy.get('#btn-aleatorio').click();

    cy.url().should('include', '/pagina-exibicao');

    cy.get('.card').first().click({ force: true });

    cy.get('.modal:visible').should('be.visible')
      .find('.btn-apadrinhar').click();

    cy.url().then(url => {
      if (url.includes('/login')) {
        cy.get('input[name="email"]').type(email);
        cy.get('input[name="password"]').type('senhaSegura123!');
        cy.get('form').submit();

        cy.url().should('include', '/pagamento/');
      } else {
        expect(url).to.include('/pagamento/');
      }
    });

    cy.get('button.btn-confirmar:visible').first().click();

    cy.get('#modal-confirmacao').should('not.have.class', 'hidden');
    cy.get('#modal-confirmacao form').submit();

    cy.on('window:alert', (text) => {
      expect(text).to.contains('Criança apadrinhada com sucesso');
    });

    cy.url().should('include', '/pagina-exibicao');
  });
});
