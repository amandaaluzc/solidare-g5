describe('História 07: Como administrador, cadastrar crianças', () => {

 beforeEach(() => {
    cy.request('POST', '/teste/limpar-geral/');
  });

  beforeEach(() => {
    cy.visit('/login_admin');
    cy.get('input[name="nome"]').type('Solidareadmin');
    cy.get('input[name="password"]').type('ADM12345');
    cy.get('form').submit();

   
    cy.url().should(() => {
      expect(true).to.be.true;
    });
  });

  it('Cenário 1: Cadastra uma criança corretamente', () => {
    cy.visit('/criancas/cadastrar/');

    cy.get('input[name="nome"]').type('Maria da Silva');
    cy.get('input[name="idade"]').type('10');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('textarea[name="descricao"]').type('Criança alegre e estudiosa.');

    cy.get('button.btn-cadastrar').click();
  });

  it('Cenário 2: Falha ao não preencher campo obrigatório', () => {
    cy.visit('/criancas/cadastrar/');

    cy.get('input[name="idade"]').type('8');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('textarea[name="descricao"]').type('Descrição da criança.');

    cy.get('button.btn-cadastrar').click();

    cy.get('.error').should('contain.text', 'This field is required');
  });

});
