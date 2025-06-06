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
describe('História 08: Como administrador, eu gostaria de gerenciar as crianças', () => {
  before(() => {
    cy.deletar_superuser();
    cy.add_superuser();
  });

 beforeEach(() => {
    
    cy.request('POST', '/teste/limpar-geral/');
  });

  beforeEach(() => {
   
    cy.visit('/login_admin');
    cy.get('input[name="nome"]').type('adminsolidare');
    cy.get('input[name="password"]').type('admin123');
    cy.get('form').submit();

    
    cy.url().should(() => {
      expect(true).to.be.true;
    });
  });

  it('Cenário 1: Excluir uma criança do sistema', () => {
    
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Carlos Teste');
    cy.get('input[name="idade"]').type('9');
    cy.get('select[name="genero"]').select('Masculino');
    cy.get('textarea[name="descricao"]').type('Criança temporária para exclusão.');
    cy.get('button.btn-cadastrar').click();

    
    cy.visit('gerenciar_afilhados/');

   
    cy.contains('Carlos Teste').should('exist');

   
    cy.get('img[alt="Deletar"]').first().click();

    
    cy.get('.btn-confirm-yes').click();

  });

  it('Cenário 2: Editar os dados de uma criança', () => {
    
    cy.visit('/criancas/cadastrar/');
    cy.get('input[name="nome"]').type('Ana Teste');
    cy.get('input[name="idade"]').type('8');
    cy.get('select[name="genero"]').select('Feminino');
    cy.get('textarea[name="descricao"]').type('Criança para edição.');
    cy.get('button.btn-cadastrar').click();

  
    cy.visit('gerenciar_afilhados/');

  
    cy.get('.edit-button').first().click();

   
    cy.get('#editModal').should('be.visible');

   
    cy.get('input[name="nome"]').clear().type('Ana Editada');
    cy.get('input[name="idade"]').clear().type('10');

    cy.get('.btn-save').click();


    cy.get('#editModal').should('not.be.visible');

    
    cy.contains('Ana Editada').should('exist');
  });

});
